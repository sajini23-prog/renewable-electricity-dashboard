import streamlit as st
import pandas as pd
import plotly.express as px

#Page configuration
st.set_page_config(
    page_title="Renewable Electricity Dashboard",
    layout="wide"
)

#Styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #050816 0%, #0A1022 100%);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070C1A 0%, #0B1430 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .dashboard-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 0.35rem;
        letter-spacing: -0.02em;
    }

    .dashboard-subtitle {
        font-size: 1rem;
        color: #CBD5E1;
        margin-bottom: 1.4rem;
        max-width: 980px;
    }

    .section-title {
        font-size: 1.45rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-top: 0.4rem;
        margin-bottom: 0.6rem;
    }

    .sidebar-box {
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 14px 12px 10px 12px;
        background: linear-gradient(145deg, rgba(20,25,48,0.95), rgba(28,37,74,0.82));
        box-shadow: 0 10px 24px rgba(0,0,0,0.22);
        margin-bottom: 14px;
    }

    .sidebar-title {
        color: #F8FAFC;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .sidebar-note {
        color: #94A3B8;
        font-size: 0.86rem;
        line-height: 1.5;
        margin-top: 8px;
    }

    .kpi-card {
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 18px 18px 16px 18px;
        background: linear-gradient(145deg, rgba(18,24,48,0.96), rgba(25,36,72,0.88));
        box-shadow: 0 10px 24px rgba(0,0,0,0.22);
        min-height: 132px;
    }

    .kpi-label {
        color: #CBD5E1;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }

    .kpi-value-purple {
        color: #8B5CF6;
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.1;
    }

    .kpi-value-blue {
        color: #3B82F6;
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.1;
    }

    .kpi-value-lightblue {
        color: #38BDF8;
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.1;
    }

    .kpi-value-teal {
        color: #14B8A6;
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.1;
    }

    .kpi-note {
        color: #94A3B8;
        font-size: 0.82rem;
        margin-top: 0.45rem;
    }

    .insight-card {
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 18px;
        background: linear-gradient(145deg, rgba(15,23,42,0.95), rgba(30,41,59,0.86));
        box-shadow: 0 10px 24px rgba(0,0,0,0.22);
        min-height: 190px;
    }

    .insight-title {
        font-size: 1rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.55rem;
    }

    .insight-text {
        font-size: 0.95rem;
        color: #CBD5E1;
        line-height: 1.55;
        margin-top: 0.6rem;
    }

    .decor-line {
        margin-top: 0.4rem;
        margin-bottom: 0.2rem;
    }

    .small-caption {
        color: #94A3B8;
        font-size: 0.88rem;
        margin-bottom: 0.9rem;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        overflow: hidden;
    }

    hr {
        border: none;
        height: 1px;
        background: linear-gradient(to right, rgba(139,92,246,0), rgba(59,130,246,0.55), rgba(20,184,166,0));
        margin-top: 26px;
        margin-bottom: 26px;
    }
</style>
""", unsafe_allow_html=True)

#Helper Functions
@st.cache_data
def load_data():
    df = pd.read_csv("data/final_renewable_electricity.csv")
    df["Year"] = df["Year"].astype(int)
    df["Renewable Output"] = pd.to_numeric(df["Renewable Output"], errors="coerce")
    df = df.dropna(subset=["Renewable Output"])
    return df

def format_value(value):
    return f"{value:.2f}"

def kpi_card(label, value, color_class, note=""):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="{color_class}">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def insight_card(title, text, stroke_color):
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">{title}</div>
            <div class="decor-line">
                <svg width="100%" height="34" viewBox="0 0 240 34" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4 26 C 42 5, 74 8, 103 19 C 131 29, 164 27, 196 13 C 212 7, 224 7, 236 11"
                          stroke="{stroke_color}" stroke-width="3" stroke-linecap="round"/>
                </svg>
            </div>
            <div class="insight-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

#Load data
df = load_data()
years = sorted(df["Year"].unique())
countries = sorted(df["Country Name"].unique())
latest_year = max(years)

#Colour palettes
discrete_palette = ["#8B5CF6", "#3B82F6", "#38BDF8", "#14B8A6", "#6366F1", "#06B6D4"]
continuous_scale = [
    [0.0, "#8B5CF6"],
    [0.25, "#6366F1"],
    [0.5, "#3B82F6"],
    [0.75, "#38BDF8"],
    [1.0, "#14B8A6"]
]

#Navigation bar
st.sidebar.markdown('<div class="sidebar-box">', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-title">Navigation</div>', unsafe_allow_html=True)

section = st.sidebar.radio(
    "Choose a section",
    [
        "Overview",
        "Top 10 Ranking",
        "Comparison Analysis",
        "Trend Over Time",
        "World Map",
        "Filtered Table",
        "Insight Summary",
        "Change Between Two Years"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown(
    """
    <div class="sidebar-note">
        Use the menu above to move between sections.
        Each section contains its own controls for focused analysis.
    </div>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

#Title
st.markdown('<div class="dashboard-title">Renewable Electricity Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="dashboard-subtitle">
        This dashboard presents renewable electricity output as a percentage of total electricity output.
        It supports ranking, comparison, geographic exploration, time-series analysis, and filtered data review
        in a professional dark-mode layout suitable for presentation.
    </div>
    """,
    unsafe_allow_html=True
)

#Section overview
if section == "Overview":
    st.markdown('<div class="section-title">Overview</div>', unsafe_allow_html=True)

    overview_year = st.selectbox("Select year", years, index=len(years) - 1, key="overview_year")
    overview_data = df[df["Year"] == overview_year].copy()

    country_count = overview_data["Country Name"].nunique()
    avg_output = overview_data["Renewable Output"].mean()
    max_output = overview_data["Renewable Output"].max()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Selected Year", overview_year, "kpi-value-purple", "Current dashboard year")
    with c2:
        kpi_card("Countries Covered", country_count, "kpi-value-blue", "Country-level observations")
    with c3:
        kpi_card("Average Output (%)", format_value(avg_output), "kpi-value-lightblue", "Mean value across countries")
    with c4:
        kpi_card("Highest Output (%)", format_value(max_output), "kpi-value-teal", "Highest country value")

    st.markdown("---")

    overview_top = overview_data.sort_values("Renewable Output", ascending=False).head(10)

    fig_overview = px.bar(
        overview_top,
        x="Country Name",
        y="Renewable Output",
        text="Renewable Output",
        color="Renewable Output",
        color_continuous_scale=continuous_scale
    )

    fig_overview.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
        marker_line_color="rgba(255,255,255,0.14)",
        marker_line_width=1.2,
        hovertemplate="<b>%{x}</b><br>Renewable Output: %{y:.2f}%<extra></extra>"
    )

    fig_overview.update_layout(
        height=540,
        xaxis_title="Country",
        yaxis_title="Renewable Electricity Output (%)",
        coloraxis_showscale=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=110),
        font=dict(size=14, color="white")
    )

    fig_overview.update_xaxes(tickangle=-30, showgrid=False, tickfont=dict(color="#E5E7EB"))
    fig_overview.update_yaxes(gridcolor="rgba(255,255,255,0.08)", tickfont=dict(color="#E5E7EB"))

    st.plotly_chart(fig_overview, use_container_width=True)

#Top 10 ranking
elif section == "Top 10 Ranking":
    st.markdown('<div class="section-title">Top 10 Ranking</div>', unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    with f1:
        ranking_year = st.selectbox("Ranking year", years, index=len(years) - 1, key="ranking_year")
    with f2:
        ranking_mode = st.selectbox("Ranking type", ["Top", "Bottom"], key="ranking_mode")
    with f3:
        ranking_n = st.slider("Number of countries", min_value=5, max_value=12, value=10, key="ranking_n")

    ranking_data = df[df["Year"] == ranking_year].copy()

    ascending_order = True if ranking_mode == "Bottom" else False
    ranking_title = f"{ranking_mode} {ranking_n} Countries by Renewable Output in {ranking_year}"

    ranking_display = ranking_data.sort_values("Renewable Output", ascending=ascending_order).head(ranking_n).copy()
    ranking_display = ranking_display.sort_values("Renewable Output", ascending=(ranking_mode == "Bottom"))
    ranking_display["Rank"] = range(1, len(ranking_display) + 1)

    st.markdown(f'<div class="small-caption">{ranking_title}</div>', unsafe_allow_html=True)

    fig_rank = px.bar(
        ranking_display,
        x="Country Name",
        y="Renewable Output",
        text="Renewable Output",
        color="Renewable Output",
        color_continuous_scale=continuous_scale
    )

    fig_rank.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
        marker_line_color="rgba(255,255,255,0.14)",
        marker_line_width=1.2,
        hovertemplate="<b>%{x}</b><br>Renewable Output: %{y:.2f}%<extra></extra>"
    )

    fig_rank.update_layout(
        height=620,
        xaxis_title="Country",
        yaxis_title="Renewable Electricity Output (%)",
        coloraxis_showscale=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=110),
        font=dict(size=14, color="white")
    )

    fig_rank.update_xaxes(tickangle=-30, showgrid=False, tickfont=dict(color="#E5E7EB"))
    fig_rank.update_yaxes(gridcolor="rgba(255,255,255,0.08)", tickfont=dict(color="#E5E7EB"))

    st.plotly_chart(fig_rank, use_container_width=True)

    st.markdown('<div class="small-caption">Ranking table</div>', unsafe_allow_html=True)
    ranking_table = ranking_display[["Rank", "Country Name", "Renewable Output"]].copy()
    ranking_table["Renewable Output"] = ranking_table["Renewable Output"].round(2)
    st.dataframe(ranking_table, use_container_width=True, hide_index=True)

#Comparison analysis
elif section == "Comparison Analysis":
    st.markdown('<div class="section-title">Comparison Analysis</div>', unsafe_allow_html=True)

    default_compare_countries = [c for c in ["Sri Lanka", "India", "China"] if c in countries]

    f1, f2, f3 = st.columns([2, 2, 1.5])
    with f1:
        compare_countries = st.multiselect(
            "Select countries to compare",
            countries,
            default=default_compare_countries,
            key="compare_countries"
        )
    with f2:
        compare_years = st.multiselect(
            "Select years",
            years,
            default=years[-3:] if len(years) >= 3 else years,
            key="compare_years"
        )
    with f3:
        compare_chart = st.selectbox(
            "Chart type",
            ["Column Chart", "Bar Chart"],
            key="compare_chart"
        )

    compare_data = df[
        (df["Country Name"].isin(compare_countries)) &
        (df["Year"].isin(compare_years))
    ].copy()

    if not compare_data.empty:
        compare_data["Year"] = compare_data["Year"].astype(str)

        if compare_chart == "Column Chart":
            fig_compare = px.bar(
                compare_data,
                x="Country Name",
                y="Renewable Output",
                color="Year",
                barmode="group",
                color_discrete_sequence=discrete_palette,
                text="Renewable Output"
            )
        else:
            fig_compare = px.bar(
                compare_data,
                y="Country Name",
                x="Renewable Output",
                color="Year",
                orientation="h",
                barmode="group",
                color_discrete_sequence=discrete_palette,
                text="Renewable Output"
            )

        fig_compare.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside"
        )

        fig_compare.update_layout(
            height=600,
            xaxis_title="Country" if compare_chart == "Column Chart" else "Renewable Electricity Output (%)",
            yaxis_title="Renewable Electricity Output (%)" if compare_chart == "Column Chart" else "Country",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=20, b=100),
            font=dict(size=14, color="white"),
            legend_title="Year"
        )

        if compare_chart == "Column Chart":
            fig_compare.update_xaxes(tickangle=-25, showgrid=False, tickfont=dict(color="#E5E7EB"))
            fig_compare.update_yaxes(gridcolor="rgba(255,255,255,0.08)", tickfont=dict(color="#E5E7EB"))
        else:
            fig_compare.update_xaxes(gridcolor="rgba(255,255,255,0.08)", tickfont=dict(color="#E5E7EB"))
            fig_compare.update_yaxes(showgrid=False, tickfont=dict(color="#E5E7EB"))

        st.plotly_chart(fig_compare, use_container_width=True)

        compare_table = compare_data.sort_values(["Year", "Renewable Output"], ascending=[True, False]).copy()
        compare_table["Renewable Output"] = compare_table["Renewable Output"].round(2)
        st.dataframe(compare_table[["Country Name", "Year", "Renewable Output"]], use_container_width=True, hide_index=True)
    else:
        st.warning("Please select at least one country and one year.")

#Trend over time
elif section == "Trend Over Time":
    st.markdown('<div class="section-title">Trend Over Time</div>', unsafe_allow_html=True)

    default_trend_countries = [c for c in ["Sri Lanka", "India", "China"] if c in countries]

    f1, f2 = st.columns([2, 2])
    with f1:
        trend_countries = st.multiselect(
            "Select countries for trend analysis",
            countries,
            default=default_trend_countries,
            key="trend_countries"
        )
    with f2:
        trend_year_range = st.slider(
            "Select year range",
            min_value=min(years),
            max_value=max(years),
            value=(min(years), max(years)),
            key="trend_year_range"
        )

    trend_data = df[
        (df["Country Name"].isin(trend_countries)) &
        (df["Year"] >= trend_year_range[0]) &
        (df["Year"] <= trend_year_range[1])
    ].copy()

    if not trend_data.empty:
        fig_trend = px.line(
            trend_data,
            x="Year",
            y="Renewable Output",
            color="Country Name",
            markers=True,
            color_discrete_sequence=discrete_palette
        )

        fig_trend.update_traces(
            line=dict(width=3),
            marker=dict(size=7),
            hovertemplate="<b>%{fullData.name}</b><br>Year: %{x}<br>Output: %{y:.2f}%<extra></extra>"
        )

        fig_trend.update_layout(
            height=560,
            xaxis_title="Year",
            yaxis_title="Renewable Electricity Output (%)",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=20, b=20),
            font=dict(size=14, color="white"),
            legend_title="Country"
        )

        fig_trend.update_xaxes(showgrid=False, tickfont=dict(color="#E5E7EB"))
        fig_trend.update_yaxes(gridcolor="rgba(255,255,255,0.08)", tickfont=dict(color="#E5E7EB"))

        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.warning("Please select at least one country.")

#World map
elif section == "World Map":
    st.markdown('<div class="section-title">World Map</div>', unsafe_allow_html=True)

    map_year = st.selectbox("Map year", years, index=len(years) - 1, key="map_year")
    map_data = df[df["Year"] == map_year].copy()

    fig_map = px.choropleth(
        map_data,
        locations="Country Code",
        color="Renewable Output",
        hover_name="Country Name",
        hover_data={"Renewable Output":":.2f"},
        color_continuous_scale=continuous_scale,
        projection="mercator"
    )

    fig_map.update_layout(
        height=760,
        paper_bgcolor="#050816",
        plot_bgcolor="#050816",
        margin=dict(l=0, r=0, t=20, b=0),
        font=dict(color="white"),
        coloraxis_colorbar_title="Output (%)",
        geo=dict(
            showframe=False,
            showcoastlines=False,
            bgcolor="#050816",
            projection_scale=1.0
        )
    )

    st.plotly_chart(fig_map, use_container_width=True)

#Filtered table
elif section == "Filtered Table":
    st.markdown('<div class="section-title">Filtered Table</div>', unsafe_allow_html=True)

    f1, f2 = st.columns([2, 2])
    with f1:
        table_countries = st.multiselect(
            "Select countries",
            countries,
            default=[],
            key="table_countries"
        )
    with f2:
        table_year_range = st.slider(
            "Select year range",
            min_value=min(years),
            max_value=max(years),
            value=(min(years), max(years)),
            key="table_year_range"
        )

    table_data = df[
        (df["Year"] >= table_year_range[0]) &
        (df["Year"] <= table_year_range[1])
    ].copy()

    if table_countries:
        table_data = table_data[table_data["Country Name"].isin(table_countries)]

    table_data = table_data.sort_values(["Country Name", "Year"]).copy()
    table_data["Renewable Output"] = table_data["Renewable Output"].round(2)

    st.dataframe(
        table_data[["Country Name", "Country Code", "Year", "Renewable Output"]],
        use_container_width=True,
        hide_index=True
    )

#Insight summary
elif section == "Insight Summary":
    st.markdown('<div class="section-title">Insight Summary</div>', unsafe_allow_html=True)

    insight_year = st.selectbox("Insight year", years, index=len(years) - 1, key="insight_year")
    insight_data = df[df["Year"] == insight_year].copy()

    top_country = insight_data.loc[insight_data["Renewable Output"].idxmax(), "Country Name"]
    top_value = insight_data["Renewable Output"].max()

    bottom_country = insight_data.loc[insight_data["Renewable Output"].idxmin(), "Country Name"]
    bottom_value = insight_data["Renewable Output"].min()

    avg_by_year = df.groupby("Year")["Renewable Output"].mean().reset_index()
    start_avg = avg_by_year.iloc[0]["Renewable Output"]
    latest_avg = avg_by_year.iloc[-1]["Renewable Output"]
    avg_change = latest_avg - start_avg

    y1, y2, y3 = st.columns(3)

    with y1:
        insight_card(
            "Leading Country",
            f"In {insight_year}, {top_country} recorded the highest renewable electricity output at {top_value:.2f}%. This indicates a very strong renewable share within national electricity production.",
            "#8B5CF6"
        )

    with y2:
        insight_card(
            "Lowest Country",
            f"In {insight_year}, {bottom_country} recorded the lowest renewable electricity output at {bottom_value:.2f}%. This can suggest greater reliance on non-renewable electricity sources during that year.",
            "#3B82F6"
        )

    with y3:
        direction = "increased" if avg_change >= 0 else "decreased"
        insight_card(
            "Long-Term Pattern",
            f"The average renewable electricity output across countries has {direction} by {abs(avg_change):.2f} percentage points from the earliest available year to the latest available year in the dataset.",
            "#14B8A6"
        )

#Chnage between two years
elif section == "Change Between Two Years":
    st.markdown('<div class="section-title">Change Between Two Years</div>', unsafe_allow_html=True)

    default_change_countries = (
        df[df["Year"] == latest_year]
        .sort_values("Renewable Output", ascending=False)
        .head(8)["Country Name"]
        .tolist()
    )

    f1, f2, f3 = st.columns([2, 1, 1])

    with f1:
        change_countries = st.multiselect(
            "Select countries",
            countries,
            default=default_change_countries,
            key="change_countries"
        )

    with f2:
        start_year = st.selectbox(
            "Start year",
            years,
            index=max(0, len(years) - 11),
            key="start_year"
        )

    with f3:
        end_year = st.selectbox(
            "End year",
            years,
            index=len(years) - 1,
            key="end_year"
        )

    if start_year >= end_year:
        st.warning("Start year must be earlier than end year.")
    else:
        change_data = df[
            (df["Country Name"].isin(change_countries)) &
            (df["Year"].isin([start_year, end_year]))
        ].copy()

        if not change_data.empty:
            pivot_change = change_data.pivot(
                index="Country Name",
                columns="Year",
                values="Renewable Output"
            ).dropna()

            if not pivot_change.empty:
                plot_rows = []

                for country in pivot_change.index:
                    plot_rows.append({
                        "Country Name": country,
                        "Year Label": str(start_year),
                        "Renewable Output": pivot_change.loc[country, start_year]
                    })
                    plot_rows.append({
                        "Country Name": country,
                        "Year Label": str(end_year),
                        "Renewable Output": pivot_change.loc[country, end_year]
                    })

                plot_df = pd.DataFrame(plot_rows)

                fig_change = px.line(
                    plot_df,
                    x="Year Label",
                    y="Renewable Output",
                    color="Country Name",
                    markers=True,
                    color_discrete_sequence=discrete_palette
                )

                fig_change.update_traces(
                    line=dict(width=3),
                    marker=dict(size=10)
                )

                fig_change.update_layout(
                    height=580,
                    xaxis_title="Year",
                    yaxis_title="Renewable Electricity Output (%)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=20, r=20, t=20, b=20),
                    font=dict(size=14, color="white"),
                    legend_title="Country"
                )

                fig_change.update_xaxes(showgrid=False, tickfont=dict(color="#E5E7EB"))
                fig_change.update_yaxes(gridcolor="rgba(255,255,255,0.08)", tickfont=dict(color="#E5E7EB"))

                st.plotly_chart(fig_change, use_container_width=True)

                st.markdown('<div class="small-caption">Change summary table</div>', unsafe_allow_html=True)

                summary_table = pivot_change.reset_index().copy()
                summary_table["Change"] = summary_table[end_year] - summary_table[start_year]
                summary_table = summary_table.sort_values("Change", ascending=False)
                summary_table.columns = ["Country Name", f"{start_year}", f"{end_year}", "Change"]
                summary_table[[f"{start_year}", f"{end_year}", "Change"]] = summary_table[[f"{start_year}", f"{end_year}", "Change"]].round(2)

                st.dataframe(summary_table, use_container_width=True, hide_index=True)
            else:
                st.warning("No complete country data is available for the selected years.")
        else:
            st.warning("Please select at least one country.")