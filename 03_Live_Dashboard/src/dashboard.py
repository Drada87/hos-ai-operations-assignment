from datetime import datetime, timezone

import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_autorefresh import st_autorefresh


def render_dashboard(df: pd.DataFrame, metrics: dict) -> None:
    """
    Render the Live Air Traffic Dashboard.
    """

    # -----------------------
    # Page configuration
    # -----------------------

    st.set_page_config(
        page_title="Live Air Traffic Dashboard",
        page_icon="✈️",
        layout="wide",
    )

    # Automatically refresh every 60 seconds
    st_autorefresh(
        interval=60_000,
        key="dashboard_refresh",
    )

    # -----------------------
    # Dashboard header
    # -----------------------

    st.title("✈️ Live Air Traffic Dashboard")

    st.markdown(
        "Real-time aircraft activity powered by **OpenSky Network**"
    )

    last_updated = datetime.now(timezone.utc).strftime(
        "%d %b %Y · %H:%M UTC"
    )

    st.caption(f"Last updated: {last_updated}")

    if df.empty:
        st.warning(
            "Live data is temporarily unavailable. "
            "The dashboard will automatically retry in 60 seconds."
        )
        return

    # Dashboard metrics
    kpis = metrics["kpis"]
    charts = metrics["charts"]
    
    # -----------------------
    # KPI Section
    # -----------------------

    row_1 = st.columns(3)

    row_1[0].metric(
        label="✈ Aircraft Tracked",
        value=f"{kpis['total_aircraft']:,}",
    )

    row_1[1].metric(
        label="🛫 Airborne",
        value=f"{kpis['airborne_aircraft']:,}",
    )

    row_1[2].metric(
        label="🛬 On Ground",
        value=f"{kpis['ground_aircraft']:,}",
    )

    row_2 = st.columns(3)

    row_2[0].metric(
        label="🌍 Countries",
        value=f"{kpis['countries_represented']:,}",
    )

    row_2[1].metric(
        label="🚀 Highest Speed",
        value=f"{kpis['highest_speed'] * 3.6:,.0f} km/h",
    )

    row_2[2].metric(
        label="📏 Highest Altitude",
        value=f"{kpis['highest_altitude']:,.0f} m",
    )

    st.divider()

    # -----------------------
    # Charts
    # -----------------------

    chart_left, chart_right = st.columns(2)

    # -----------------------
    # Top Countries
    # -----------------------

    with chart_left:
        st.subheader("Top Countries by Aircraft")

        fig = px.bar(
            charts["top_countries"],
            x="aircraft_count",
            y="origin_country",
            orientation="h",
        )

        fig.update_layout(
            height=420,
            xaxis_title="Aircraft",
            yaxis_title=None,
            yaxis={"categoryorder": "total ascending"},
            showlegend=False,
            margin=dict(l=20, r=20, t=30, b=20),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # -----------------------
    # Aircraft Status
    # -----------------------

    with chart_right:
        st.subheader("Aircraft Status")

        fig = px.pie(
            charts["ground_distribution"],
            names="status",
            values="count",
            hole=0.65,
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate="%{label}<br>%{value} aircraft<extra></extra>",

        )

        fig.update_layout(
            height=420,
            showlegend=False,
            margin=dict(l=20, r=20, t=30, b=20),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.divider()

    # -----------------------
    # Latest Aircraft States
    # -----------------------

    st.subheader("Latest Aircraft States")

    # Build table
    table = df[
        [
            "callsign",
            "origin_country",
            "on_ground",
            "velocity",
            "geo_altitude",
        ]
    ].copy()

    # Rename columns
    table.columns = [
        "Callsign",
        "Country",
        "Status",
        "Speed (km/h)",
        "Altitude (m)",
    ]

    # Format values
    table["Speed (km/h)"] = (
        table["Speed (km/h)"]
        .fillna(0)
        .mul(3.6)
        .round()
        .astype(int)
    )

    table["Altitude (m)"] = (
        table["Altitude (m)"]
        .fillna(0)
        .round()
        .astype(int)
    )

    table["Status"] = table["Status"].map(
        {
            True: "On Ground",
            False: "Airborne",
        }
    )

    # Remove empty callsigns
    table = table[
        table["Callsign"].str.strip().ne("")
    ]

    # -----------------------
    # Filters
    # -----------------------

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        selected_country = st.selectbox(
            "Country",
            ["All"] + sorted(table["Country"].dropna().unique().tolist()),
        )

    with filter_col2:
        selected_status = st.selectbox(
            "Status",
            ["All", "Airborne", "On Ground"],
        )

    with filter_col3:
        search_callsign = st.text_input(
        "Search Callsign",
        placeholder="e.g. AAL1234",
        )

    # -----------------------
    # Apply filters
    # -----------------------

    filtered_table = table.copy()

    if selected_country != "All":
        filtered_table = filtered_table[
            filtered_table["Country"] == selected_country
        ]

    if selected_status != "All":
        filtered_table = filtered_table[
            filtered_table["Status"] == selected_status
        ]

    if search_callsign:
        filtered_table = filtered_table[
            filtered_table["Callsign"].str.contains(
                search_callsign,
                case=False,
                na=False,
            )
        ]

    st.caption(
        f"Showing {len(filtered_table):,} aircraft"
    )

    st.dataframe(
        filtered_table.head(100),
        use_container_width=True,
        hide_index=True,
        height=420,
    )

    st.divider()

    st.caption(
        "Data source: OpenSky Network API • Dashboard built with Streamlit"
    )

    