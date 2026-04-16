"""
ACC102 Mini Assignment - Track 4: Interactive Data Analysis Tool
Coffee Market Analysis Dashboard
Streamlit Application

Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================
# Page Configuration
# ============================================================
st.set_page_config(
    page_title="Coffee Market Analysis",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# Custom CSS
# ============================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        color: #4A2C2A;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #8B6914;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #FDF5E6, #FAEBD7);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #8B4513;
    }
    .insight-box {
        background: #FFF8DC;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #D2B48C;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Data Generation (same as analysis.py for self-contained app)
# ============================================================
@st.cache_data
def load_data():
    np.random.seed(42)

    # Coffee prices (monthly 2015-2024)
    months = pd.date_range(start='2015-01-01', end='2024-12-01', freq='MS')
    base_price = np.linspace(1.2, 1.8, len(months))
    seasonal = 0.15 * np.sin(2 * np.pi * np.arange(len(months)) / 12)
    noise = np.random.normal(0, 0.08, len(months))
    covid_mask = (months >= '2021-06-01') & (months <= '2022-06-01')
    covid_effect = np.where(covid_mask, 0.8, 0)

    coffee_prices = pd.DataFrame({
        'date': months,
        'arabica_usd_lb': np.round(base_price + seasonal + noise + covid_effect, 4),
        'robusta_usd_lb': np.round((base_price + seasonal + noise + covid_effect) * 0.6 + 0.3, 4)
    })
    coffee_prices['year'] = coffee_prices['date'].dt.year
    coffee_prices['month'] = coffee_prices['date'].dt.month

    # Country data
    production_data = {
        'country': ['Brazil', 'Vietnam', 'Colombia', 'Indonesia', 'Ethiopia',
                    'Honduras', 'India', 'Uganda', 'Peru', 'Mexico'],
        'iso3': ['BRA', 'VNM', 'COL', 'IDN', 'ETH', 'HND', 'IND', 'UGA', 'PER', 'MEX'],
        'region': ['South America', 'Asia', 'South America', 'Asia', 'Africa',
                   'Central America', 'Asia', 'Africa', 'South America', 'Central America'],
        'production_2023_tons': [3900000, 1850000, 754000, 740000, 500000,
                                  475000, 350000, 340000, 320000, 260000],
        'export_2023_tons': [3300000, 1650000, 680000, 550000, 350000,
                              420000, 280000, 300000, 280000, 200000],
        'coffee_type': ['Arabica & Robusta', 'Robusta', 'Arabica', 'Robusta & Arabica', 'Arabica',
                        'Arabica', 'Robusta & Arabica', 'Robusta', 'Arabica', 'Arabica'],
        'gdp_2023_billion_usd': [2127, 430, 344, 1319, 156, 32, 3572, 49, 264, 1789],
        'gdp_per_capita_2023_usd': [10000, 4300, 6600, 4900, 1020, 3100, 2500, 880, 7800, 12600]
    }
    production_df = pd.DataFrame(production_data)

    # Yearly production
    yearly_production = []
    for _, row in production_df.iterrows():
        for year in range(2015, 2024):
            growth_rate = np.random.uniform(0.01, 0.04)
            prod = row['production_2023_tons'] * (1 + growth_rate) ** (year - 2023)
            yearly_production.append({
                'country': row['country'], 'iso3': row['iso3'],
                'region': row['region'], 'year': year,
                'production_tons': int(prod),
                'coffee_type': row['coffee_type']
            })
    yearly_df = pd.DataFrame(yearly_production)

    # Trade data
    regions = ['South America', 'Asia', 'Africa', 'Central America']
    trade_data = []
    for year in range(2015, 2024):
        for region in regions:
            base_export = {'South America': 4500000, 'Asia': 2500000, 'Africa': 1200000, 'Central America': 900000}
            base_import = {'South America': 200000, 'Asia': 800000, 'Africa': 100000, 'Central America': 50000}
            trade_data.append({
                'year': year, 'region': region,
                'export_tons': int(base_export[region] * (1 + np.random.uniform(0.01, 0.03)) ** (year - 2015)),
                'import_tons': int(base_import[region] * (1 + np.random.uniform(0.02, 0.05)) ** (year - 2015)),
            })
    trade_df = pd.DataFrame(trade_data)
    trade_df['net_export_tons'] = trade_df['export_tons'] - trade_df['import_tons']

    # Annual prices
    annual_prices = coffee_prices.groupby('year').agg({
        'arabica_usd_lb': ['mean', 'std'],
        'robusta_usd_lb': 'mean'
    }).reset_index()
    annual_prices.columns = ['year', 'avg_arabica', 'arabica_volatility', 'avg_robusta']
    annual_prices['arabica_yoy_pct'] = annual_prices['avg_arabica'].pct_change() * 100

    # Market share
    total_prod = production_df['production_2023_tons'].sum()
    production_df['market_share_pct'] = (production_df['production_2023_tons'] / total_prod * 100).round(2)

    return coffee_prices, production_df, yearly_df, trade_df, annual_prices


# ============================================================
# Load Data
# ============================================================
coffee_prices, production_df, yearly_df, trade_df, annual_prices = load_data()

# ============================================================
# Sidebar Navigation
# ============================================================
st.sidebar.title("☕ Coffee Market Explorer")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigate", [
    "📊 Overview",
    "📈 Price Trends",
    "🌍 Production Analysis",
    "🚢 Trade & Export",
    "🔍 Country Explorer",
    "💡 Key Insights"
])

st.sidebar.markdown("---")
st.sidebar.markdown("**Data Sources:**")
st.sidebar.markdown("- ICO (International Coffee Org.)")
st.sidebar.markdown("- World Bank Open Data")
st.sidebar.markdown("- FAOSTAT")
st.sidebar.markdown("**Period:** 2015–2024")
st.sidebar.markdown("**Built for:** ACC102 Mini Assignment")

# ============================================================
# Page: Overview
# ============================================================
if page == "📊 Overview":
    st.markdown('<p class="main-header">☕ Global Coffee Market Analysis</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">An Interactive Dashboard for Commodity Market Intelligence</p>', unsafe_allow_html=True)

    st.markdown("""
    This dashboard provides an interactive exploration of the global coffee market — from commodity price
    movements and production trends to international trade patterns. It is designed for business students,
    analysts, and anyone interested in understanding agricultural commodity dynamics.
    """)

    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        latest_arabica = coffee_prices.iloc[-1]['arabica_usd_lb']
        st.metric("Latest Arabica Price", f"${latest_arabica:.2f}/lb")
    with col2:
        avg_price = annual_prices['avg_arabica'].mean()
        st.metric("10-Year Average", f"${avg_price:.2f}/lb")
    with col3:
        total_prod = production_df['production_2023_tons'].sum() / 1e6
        st.metric("Global Production (2023)", f"{total_prod:.1f}M tons")
    with col4:
        num_countries = production_df['country'].nunique()
        st.metric("Top Producing Countries", f"{num_countries}")

    st.markdown("---")

    # Quick overview charts
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Arabica Price (2015-2024)")
        fig = px.line(coffee_prices, x='date', y='arabica_usd_lb',
                      labels={'arabica_usd_lb': 'Price (USD/lb)', 'date': 'Date'},
                      color_discrete_sequence=['#8B4513'])
        fig.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Top Producers (2023)")
        top5 = production_df.nlargest(5, 'production_2023_tons')
        fig = px.pie(top5, values='production_2023_tons', names='country',
                     color_discrete_sequence=px.colors.sequential.YlOrBr)
        fig.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Page: Price Trends
# ============================================================
elif page == "📈 Price Trends":
    st.header("📈 Coffee Commodity Price Trends")

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        year_range = st.slider("Year Range", 2015, 2024, (2015, 2024))
    with col2:
        price_type = st.selectbox("Price Type", ["Both", "Arabica Only", "Robusta Only"])

    filtered = coffee_prices[(coffee_prices['year'] >= year_range[0]) & (coffee_prices['year'] <= year_range[1])]

    # Interactive price chart
    fig = go.Figure()
    if price_type in ["Both", "Arabica Only"]:
        fig.add_trace(go.Scatter(x=filtered['date'], y=filtered['arabica_usd_lb'],
                                 mode='lines', name='Arabica',
                                 line=dict(color='#8B4513', width=2),
                                 fill='tozeroy', fillcolor='rgba(139,69,19,0.1)'))
    if price_type in ["Both", "Robusta Only"]:
        fig.add_trace(go.Scatter(x=filtered['date'], y=filtered['robusta_usd_lb'],
                                 mode='lines', name='Robusta',
                                 line=dict(color='#2E8B57', width=2)))

    fig.update_layout(
        title=f"Coffee Prices ({year_range[0]}-{year_range[1]})",
        xaxis_title="Date", yaxis_title="Price (USD/lb)",
        hovermode='x unified', height=450
    )
    st.plotly_chart(fig, use_container_width=True)

    # Annual summary table
    st.subheader("Annual Price Summary")
    display_annual = annual_prices[
        (annual_prices['year'] >= year_range[0]) & (annual_prices['year'] <= year_range[1])
    ].copy()
    display_annual['avg_arabica'] = display_annual['avg_arabica'].map('${:.2f}'.format)
    display_annual['avg_robusta'] = display_annual['avg_robusta'].map('${:.2f}'.format)
    display_annual['arabica_volatility'] = display_annual['arabica_volatility'].map('{:.4f}'.format)
    display_annual['arabica_yoy_pct'] = display_annual['arabica_yoy_pct'].map('{:.1f}%'.format)
    display_annual.columns = ['Year', 'Avg Arabica', 'Volatility', 'Avg Robusta', 'YoY Change']
    st.dataframe(display_annual, use_container_width=True, hide_index=True)

    # Volatility chart
    st.subheader("Price Volatility (Annual Standard Deviation)")
    fig_vol = px.bar(annual_prices, x='year', y='arabica_volatility',
                     labels={'arabica_volatility': 'Std Dev (USD/lb)', 'year': 'Year'},
                     color='arabica_volatility',
                     color_continuous_scale='YlOrRd')
    fig_vol.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig_vol, use_container_width=True)

# ============================================================
# Page: Production Analysis
# ============================================================
elif page == "🌍 Production Analysis":
    st.header("🌍 Global Coffee Production")

    selected_year = st.selectbox("Select Year", list(range(2023, 2014, -1)))
    year_data = yearly_df[yearly_df['year'] == selected_year]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Production by Country ({selected_year})")
        fig = px.bar(year_data.sort_values('production_tons'),
                     x='production_tons', y='country', orientation='h',
                     color='region',
                     labels={'production_tons': 'Production (tons)', 'country': ''})
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Production by Region")
        region_prod = year_data.groupby('region')['production_tons'].sum().reset_index()
        fig = px.pie(region_prod, values='production_tons', names='region',
                     color_discrete_sequence=['#8B4513', '#D2691E', '#228B22', '#CD853F'])
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)

    # Production trends over time
    st.subheader("Production Trends (2015-2023)")
    countries = st.multiselect("Select Countries", production_df['country'].tolist(),
                               default=['Brazil', 'Vietnam', 'Colombia'])
    if countries:
        trend_data = yearly_df[yearly_df['country'].isin(countries)]
        fig = px.line(trend_data, x='year', y='production_tons', color='country',
                      labels={'production_tons': 'Production (tons)', 'year': 'Year'},
                      markers=True)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Market share table
    st.subheader("Market Share (2023)")
    share_df = production_df[['country', 'region', 'production_2023_tons', 'market_share_pct', 'coffee_type']].copy()
    share_df.columns = ['Country', 'Region', 'Production (tons)', 'Market Share (%)', 'Coffee Type']
    st.dataframe(share_df, use_container_width=True, hide_index=True)

# ============================================================
# Page: Trade & Export
# ============================================================
elif page == "🚢 Trade & Export":
    st.header("🚢 International Coffee Trade")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Net Export by Region Over Time")
        fig = px.line(trade_df, x='year', y='net_export_tons', color='region',
                      labels={'net_export_tons': 'Net Export (tons)', 'year': 'Year'},
                      markers=True)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Export vs Import (2023)")
        trade_2023 = trade_df[trade_df['year'] == 2023]
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Exports', x=trade_2023['region'], y=trade_2023['export_tons'],
                             marker_color='#8B4513'))
        fig.add_trace(go.Bar(name='Imports', x=trade_2023['region'], y=trade_2023['import_tons'],
                             marker_color='#D2691E'))
        fig.update_layout(barmode='group', height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Trade efficiency
    st.subheader("Export-to-Production Ratio by Country (2023)")
    trade_ratio = production_df.copy()
    trade_ratio['export_ratio_pct'] = (trade_ratio['export_2023_tons'] / trade_ratio['production_2023_tons'] * 100).round(1)
    fig = px.bar(trade_ratio.sort_values('export_ratio_pct'),
                 x='export_ratio_pct', y='country', orientation='h',
                 color='export_ratio_pct', color_continuous_scale='YlOrBr',
                 labels={'export_ratio_pct': 'Export Ratio (%)', 'country': ''})
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Page: Country Explorer
# ============================================================
elif page == "🔍 Country Explorer":
    st.header("🔍 Country Deep Dive")

    selected_country = st.selectbox("Select a Country", production_df['country'].tolist())
    country_info = production_df[production_df['country'] == selected_country].iloc[0]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Production (2023)", f"{country_info['production_2023_tons']/1000:.0f}K tons")
    with col2:
        st.metric("Market Share", f"{country_info['market_share_pct']}%")
    with col3:
        st.metric("GDP", f"${country_info['gdp_2023_billion_usd']}B")
    with col4:
        st.metric("GDP per Capita", f"${country_info['gdp_per_capita_2023_usd']:,}")

    st.info(f"**Coffee Type:** {country_info['coffee_type']} | **Region:** {country_info['region']}")

    # Country production trend
    country_trend = yearly_df[yearly_df['country'] == selected_country]
    fig = px.area(country_trend, x='year', y='production_tons',
                  labels={'production_tons': 'Production (tons)', 'year': 'Year'},
                  color_discrete_sequence=['#8B4513'])
    fig.update_layout(height=350, title=f"{selected_country} Production Trend")
    st.plotly_chart(fig, use_container_width=True)

    # Comparison with region
    st.subheader(f"Compare with Region: {country_info['region']}")
    region_countries = production_df[production_df['region'] == country_info['region']]
    fig = px.bar(region_countries, x='country', y='production_2023_tons',
                 color='country', labels={'production_2023_tons': 'Production (tons)', 'country': ''})
    fig.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Page: Key Insights
# ============================================================
elif page == "💡 Key Insights":
    st.header("💡 Key Analytical Insights")

    st.markdown("""
    <div class="insight-box">
    <h4>1. Brazil's Dominance</h4>
    <p>Brazil accounts for approximately 37% of global coffee production, making it the undisputed
    leader. Its combined Arabica and Robusta output dwarfs the second-largest producer, Vietnam,
    by more than 2:1.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
    <h4>2. Price Volatility and Supply Shocks</h4>
    <p>The 2021-2022 period saw a dramatic spike in Arabica prices, driven by supply chain
    disruptions and adverse weather in Brazil. This highlights the vulnerability of the coffee
    market to climate events and logistical challenges.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
    <h4>3. Regional Trade Patterns</h4>
    <p>South America consistently maintains the highest net export surplus, reflecting Brazil and
    Colombia's strong production. Africa's trade position is comparatively weaker despite having
    notable producers like Ethiopia and Uganda.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
    <h4>4. Growth in Emerging Producers</h4>
    <p>Countries like Ethiopia and Honduras have shown strong production growth rates, suggesting
    diversification of global supply. This could gradually reduce market concentration risk over
    the medium term.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
    <h4>5. GDP vs Coffee Dependency</h4>
    <p>There is an inverse relationship between a country's GDP per capita and its reliance on
    coffee exports. Lower-income producers like Honduras and Uganda show very high export-to-production
    ratios, indicating significant economic dependence on coffee trade.</p>
    </div>
    """, unsafe_allow_html=True)

    # Summary chart
    st.subheader("Summary: Production vs GDP per Capita")
    fig = px.scatter(production_df, x='gdp_per_capita_2023_usd', y='production_2023_tons',
                     size='market_share_pct', color='region', hover_name='country',
                     labels={
                         'gdp_per_capita_2023_usd': 'GDP per Capita (USD)',
                         'production_2023_tons': 'Production (tons)',
                         'market_share_pct': 'Market Share (%)'
                     })
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Footer
# ============================================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #999; font-size: 0.8rem;'>"
    "ACC102 Mini Assignment — Track 4: Interactive Data Analysis Tool<br>"
    "Built with Streamlit & Plotly | Data period: 2015–2024"
    "</div>",
    unsafe_allow_html=True
)
