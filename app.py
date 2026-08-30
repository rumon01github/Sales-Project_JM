"""
Local Sales Analysis Platform
-----------------------------
Streamlit app: pick a local folder, choose a CSV, preview it, then run each
analysis behind its own button. Every chart is a Plotly figure (native zoom /
pan / box-select) plus a controls panel for dynamic axis ranges, log scale and
height.

Run:
    .venv/Scripts/streamlit run app.py
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Sales Analysis Platform", layout="wide")

# Superstore schema: logical name -> list of accepted column names
SCHEMA = {
    "sales": ["Sales"],
    "profit": ["Profit"],
    "discount": ["Discount"],
    "quantity": ["Quantity"],
    "order_date": ["Order Date", "OrderDate", "Order_Date"],
    "region": ["Region"],
    "category": ["Category"],
    "segment": ["Segment"],
    "sub_category": ["Sub-Category", "Sub Category", "SubCategory"],
}


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def list_csvs(folder: str):
    p = Path(folder).expanduser()
    if not p.is_dir():
        return None, []
    return p, sorted(f.name for f in p.iterdir() if f.suffix.lower() == ".csv")


@st.cache_data(show_spinner="Loading CSV...")
def load_csv(path: str, mtime: float) -> pd.DataFrame:
    # mtime is part of the cache key so edits on disk invalidate the cache
    return pd.read_csv(path, encoding="latin-1")


def auto_map(columns) -> dict:
    cols = list(columns)
    lower = {c.lower(): c for c in cols}
    mapping = {}
    for logical, candidates in SCHEMA.items():
        hit = next((c for c in candidates if c in cols), None)
        if hit is None:
            hit = next((lower[c.lower()] for c in candidates if c.lower() in lower), None)
        mapping[logical] = hit
    return mapping


def col(logical: str):
    """Resolve a logical column name to the real one via the sidebar mapping."""
    return st.session_state.mapping.get(logical)


def need(*logicals) -> bool:
    missing = [l for l in logicals if not col(l)]
    if missing:
        st.warning(
            "This analysis needs column(s): "
            + ", ".join(missing)
            + ". Map them in the sidebar."
        )
        return False
    return True


def axis_controls(fig: go.Figure, key: str, *, default_logy: bool = False):
    """Render a Plotly chart with a dynamic-axis control panel."""
    with st.expander("Axis & view controls", expanded=False):
        c1, c2, c3, c4, c5 = st.columns(5)
        xmin = c1.text_input("X min", key=f"{key}_xmin")
        xmax = c2.text_input("X max", key=f"{key}_xmax")
        ymin = c3.text_input("Y min", key=f"{key}_ymin")
        ymax = c4.text_input("Y max", key=f"{key}_ymax")
        logy = c5.checkbox("Log Y", value=default_logy, key=f"{key}_logy")
        height = st.slider("Height (px)", 300, 1000, 500, 50, key=f"{key}_h")

    def _rng(a, b):
        try:
            return [float(a), float(b)] if a != "" and b != "" else None
        except ValueError:
            return None

    xr, yr = _rng(xmin, xmax), _rng(ymin, ymax)
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=40, b=10))
    if xr:
        fig.update_xaxes(range=xr)
    if yr:
        fig.update_yaxes(range=yr)
    fig.update_yaxes(type="log" if logy else "linear")
    st.plotly_chart(fig, width="stretch", key=f"{key}_chart")


def dt_series() -> pd.Series:
    s = pd.to_datetime(df[col("order_date")], errors="coerce")
    return s


# --------------------------------------------------------------------------- #
# Sidebar: folder + file + column mapping
# --------------------------------------------------------------------------- #
st.sidebar.header("1. Data source")
folder = st.sidebar.text_input("Folder path", value=str(Path.cwd()))
p, csvs = list_csvs(folder)

if p is None:
    st.sidebar.error("Not a folder.")
    st.stop()
if not csvs:
    st.sidebar.warning("No .csv files in that folder.")
    st.stop()

fname = st.sidebar.selectbox("CSV file", csvs)
fpath = p / fname
df = load_csv(str(fpath), fpath.stat().st_mtime)

if "mapping" not in st.session_state or st.session_state.get("mapped_for") != str(fpath):
    st.session_state.mapping = auto_map(df.columns)
    st.session_state.mapped_for = str(fpath)

st.sidebar.header("2. Column mapping")
opts = ["(none)"] + list(df.columns)
for logical in SCHEMA:
    cur = st.session_state.mapping.get(logical)
    idx = opts.index(cur) if cur in opts else 0
    pick = st.sidebar.selectbox(logical, opts, index=idx, key=f"map_{logical}")
    st.session_state.mapping[logical] = None if pick == "(none)" else pick


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
st.title("Sales Analysis Platform")
st.caption(f"{fpath}  —  {df.shape[0]:,} rows × {df.shape[1]} columns")

tab_data, tab_overview, tab_trend, tab_disc, tab_regcat = st.tabs(
    ["Data", "Overview", "Trend", "Discount vs Profit", "Region & Category"]
)

# ---- Data preview -------------------------------------------------------- #
with tab_data:
    st.subheader("Preview")
    n = st.slider("Rows to show", 5, min(2000, len(df)), 50, key="prev_n")
    text_cols = df.select_dtypes(exclude="number").columns.tolist()
    fcol = st.selectbox("Filter a text column (optional)", ["(none)"] + text_cols)
    view = df
    if fcol != "(none)":
        vals = st.multiselect(f"{fcol} values", sorted(df[fcol].dropna().unique()))
        if vals:
            view = df[df[fcol].isin(vals)]
    st.dataframe(view.head(n), width="stretch")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Dtypes")
        st.dataframe(
            pd.DataFrame({"column": df.columns, "dtype": df.dtypes.astype(str).values}),
            width="stretch",
            hide_index=True,
        )
    with c2:
        st.subheader("Numeric summary")
        st.dataframe(df.describe().T, width="stretch")

# ---- Overview ---------------------------------------------------------- #
with tab_overview:
    st.subheader("Headline totals & margins")
    if st.button("Run overview", key="run_overview") and need("sales", "profit"):
        s, pf = df[col("sales")], df[col("profit")]
        total_sales, total_profit = s.sum(), pf.sum()
        margin = total_profit / total_sales * 100 if total_sales else float("nan")
        loss = int((pf < 0).sum())

        m = st.columns(4)
        m[0].metric("Total sales", f"${total_sales:,.0f}")
        m[1].metric("Total profit", f"${total_profit:,.0f}")
        m[2].metric("Overall margin", f"{margin:.1f}%")
        m[3].metric("Loss-making lines", f"{loss:,} ({loss / len(df) * 100:.1f}%)")

        a = st.columns(3)
        a[0].metric("Avg sales / line", f"${s.mean():,.2f}")
        a[1].metric("Avg profit / line", f"${pf.mean():,.2f}")
        if col("discount"):
            a[2].metric("Avg discount", f"{df[col('discount')].mean() * 100:.1f}%")

        st.markdown("**Profit distribution per order line**")
        fig = px.histogram(df, x=col("profit"), nbins=80)
        fig.add_vline(x=0, line_color="red")
        axis_controls(fig, "ov_hist", default_logy=True)

# ---- Trend ----------------------------------------------------------- #
with tab_trend:
    st.subheader("Sales over time")
    if st.button("Run trend", key="run_trend") and need("order_date", "sales"):
        d = pd.DataFrame({"date": dt_series(), "sales": df[col("sales")]}).dropna()
        if d.empty:
            st.error("Could not parse any dates from the order_date column.")
        else:
            monthly = (
                d.set_index("date")
                .resample("MS")["sales"]
                .sum()
                .rename("sales")
                .reset_index()
            )
            d["year"] = d["date"].dt.year
            yearly = d.groupby("year")["sales"].sum()
            growth = (yearly.iloc[-1] - yearly.iloc[0]) / yearly.iloc[0] * 100

            c1, c2 = st.columns([1, 2])
            c1.metric(
                f"Growth {yearly.index[0]}→{yearly.index[-1]}", f"{growth:.1f}%"
            )
            c2.dataframe(
                yearly.reset_index().rename(columns={"sales": "total_sales"}),
                width="stretch",
                hide_index=True,
            )

            fig = px.line(monthly, x="date", y="sales", markers=True)
            fig.update_xaxes(rangeslider_visible=True)
            axis_controls(fig, "tr_line")

# ---- Discount vs Profit ------------------------------------------- #
with tab_disc:
    st.subheader("Does discounting help or hurt profit?")
    if st.button("Run discount analysis", key="run_disc") and need("discount", "profit"):
        dd, pp = df[col("discount")], df[col("profit")]
        corr = dd.corr(pp)
        st.metric("Correlation (discount, profit)", f"{corr:.3f}")

        avg = dd.to_frame("discount").assign(profit=pp).groupby("discount")["profit"].mean()
        st.markdown("**Average profit at each discount level**")
        bar = px.bar(avg.reset_index(), x="discount", y="profit")
        bar.add_hline(y=0, line_color="red")
        axis_controls(bar, "dc_bar")

        st.markdown("**Every order line**")
        sc = px.scatter(
            df, x=col("discount"), y=col("profit"),
            color=col("category") if col("category") else None,
            opacity=0.35,
        )
        sc.add_hline(y=0, line_color="red")
        axis_controls(sc, "dc_scatter")

# ---- Region & Category ------------------------------------------- #
with tab_regcat:
    st.subheader("Which parts of the business make money?")
    if st.button("Run region & category", key="run_rc") and need("sales", "profit"):
        def perf(group_logical):
            g = col(group_logical)
            if not g:
                return None
            t = df.groupby(g).agg(
                total_sales=(col("sales"), "sum"),
                total_profit=(col("profit"), "sum"),
            )
            t["margin_%"] = t["total_profit"] / t["total_sales"] * 100
            return t.round(2).reset_index()

        for logical, label in [("region", "Region"), ("category", "Category"),
                               ("segment", "Segment"), ("sub_category", "Sub-Category")]:
            t = perf(logical)
            if t is None:
                continue
            st.markdown(f"**Performance by {label}**")
            st.dataframe(t, width="stretch", hide_index=True)
            fig = go.Figure()
            fig.add_bar(x=t[col(logical)], y=t["total_profit"], name="Profit")
            fig.add_bar(x=t[col(logical)], y=t["total_sales"], name="Sales", visible="legendonly")
            fig.update_layout(barmode="group", title=f"By {label}")
            axis_controls(fig, f"rc_{logical}")
