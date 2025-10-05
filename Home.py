import streamlit as st
import sys
import os

# Add current directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.solar_data import get_solar_data
from models.roi_calculator import SolarROICalculator

st.set_page_config(
    page_title="Solar ROI Predictor - NASA Techies",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Top Navigation Bar */
    .top-nav {
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(10px);
        padding: 1rem 2rem;
        border-bottom: 1px solid rgba(96, 165, 250, 0.3);
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .nav-title {
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(to right, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .nav-team {
        color: #94a3b8;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Top Navigation
st.markdown("""
<div class="top-nav">
    <div>
        <div class="nav-title">☀️ Solar ROI Predictor</div>
        <div class="nav-team">by NASA Techies 🇵🇰</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
if 'results' not in st.session_state:
    st.session_state.results = None
if 'solar_df' not in st.session_state:
    st.session_state.solar_df = None
if 'avg_irradiance' not in st.session_state:
    st.session_state.avg_irradiance = None
if 'comparison_done' not in st.session_state:
    st.session_state.comparison_done = False
if 'comparison_data' not in st.session_state:
    st.session_state.comparison_data = None

# Sidebar
with st.sidebar:
    st.header("📍 Location & Parameters")

    # Initialize default values from session state if location was clicked
    default_lat = st.session_state.get('try_lat', 37.77)
    default_lon = st.session_state.get('try_lon', -122.42)

    col1, col2 = st.columns(2)
    latitude = col1.number_input("Latitude", -90.0, 90.0, default_lat)
    longitude = col2.number_input("Longitude", -180.0, 180.0, default_lon)

    system_size = st.slider("System Size (kW)", 10, 1000, 100)
    electricity_rate = st.slider("Electricity Rate ($/kWh)", 0.05, 0.30, 0.12, 0.01)

    if st.button("🔍 Analyze Investment", type="primary"):
        st.session_state.analyzed = True
        st.session_state.latitude = latitude
        st.session_state.longitude = longitude
        st.session_state.system_size = system_size
        st.session_state.electricity_rate = electricity_rate

    st.divider()
    st.subheader("🌍 Try These Locations")

    if st.button("☀️ Phoenix, AZ", use_container_width=True):
        st.session_state.try_lat = 33.45
        st.session_state.try_lon = -112.07
        st.rerun()
    st.caption("Lat: 33.45, Lon: -112.07")

    if st.button("🎰 Las Vegas, NV", use_container_width=True):
        st.session_state.try_lat = 36.17
        st.session_state.try_lon = -115.14
        st.rerun()
    st.caption("Lat: 36.17, Lon: -115.14")

    if st.button("🏖️ Miami, FL", use_container_width=True):
        st.session_state.try_lat = 25.76
        st.session_state.try_lon = -80.19
        st.rerun()
    st.caption("Lat: 25.76, Lon: -80.19")

# Main area
st.subheader("Analyze Solar Investment Returns using NASA Satellite Data")

if st.session_state.analyzed:
    # Only fetch data if we don't have it yet or parameters changed
    if (st.session_state.results is None or
        st.session_state.latitude != latitude or
        st.session_state.longitude != longitude or
        st.session_state.system_size != system_size or
        st.session_state.electricity_rate != electricity_rate):

        # Update session state with current values
        st.session_state.latitude = latitude
        st.session_state.longitude = longitude
        st.session_state.system_size = system_size
        st.session_state.electricity_rate = electricity_rate

        with st.spinner("🛰️ Fetching NASA satellite data..."):
            solar_df = get_solar_data(latitude, longitude, '2024-01-01', '2024-12-31')

        if solar_df is not None:
            avg_irradiance = solar_df['solar_irradiance'].mean()

            # Calculate ROI
            calculator = SolarROICalculator()
            results = calculator.calculate_roi(avg_irradiance, system_size, electricity_rate)

            # Store in session state
            st.session_state.solar_df = solar_df
            st.session_state.avg_irradiance = avg_irradiance
            st.session_state.results = results
        else:
            st.error("❌ Failed to fetch solar data. Please check your coordinates and try again.")
            st.session_state.analyzed = False

    # Display results from session state
    if st.session_state.results is not None:
        results = st.session_state.results
        solar_df = st.session_state.solar_df
        avg_irradiance = st.session_state.avg_irradiance

        st.success("✅ Analysis complete!")

        # Display metrics in columns
        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "ROI (25 years)",
            f"{results['roi_percent']:.1f}%",
            delta="Profit" if results['roi_percent'] > 0 else "Loss"
        )
        col2.metric(
            "Payback Period",
            f"{results['payback_period_years']:.1f} years"
        )
        col3.metric(
            "Annual Production",
            f"{results['annual_production_kwh']:,.0f} kWh"
        )
        col4.metric(
            "Total Investment",
            f"${results['total_investment']:,.0f}"
        )

        # Additional info
        st.divider()

        col_a, col_b = st.columns(2)

        with col_a:
            st.metric(
                "Net Profit (25 years)",
                f"${results['net_profit']:,.0f}"
            )

        with col_b:
            st.metric(
                "Average Solar Irradiance",
                f"{avg_irradiance:.2f} kWh/m²/day"
            )

        # Show irradiance chart
        st.divider()
        st.subheader("📈 Daily Solar Irradiance - 2024")
        st.line_chart(solar_df, use_container_width=True)

        # Download data option
        st.divider()
        csv = solar_df.to_csv()
        st.download_button(
            label="📥 Download Solar Data (CSV)",
            data=csv,
            file_name=f"solar_data_{st.session_state.latitude}_{st.session_state.longitude}.csv",
            mime="text/csv"
        )

        # Cash Flow Projection
        st.divider()
        st.subheader("💰 25-Year Cash Flow Projection")

        import plotly.graph_objects as go

        years = list(range(0, 26))
        cumulative_cash = [-results['total_investment']]
        cash = -results['total_investment']

        for year in range(1, 26):
            annual_revenue = (
                results['annual_production_kwh'] *
                st.session_state.electricity_rate *
                ((1 - 0.005) ** year)
            )
            cash += annual_revenue
            cumulative_cash.append(cash)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=years,
            y=cumulative_cash,
            fill='tozeroy',
            name='Cumulative Cash Flow',
            line=dict(color='#10b981', width=3),
            fillcolor='rgba(16, 185, 129, 0.2)'
        ))

        fig.add_hline(
            y=0,
            line_dash="dash",
            line_color="red",
            annotation_text="Break Even Point",
            annotation_position="right"
        )

        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Cumulative Cash Flow ($)",
            hovermode='x unified',
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

        breakeven_year = results['payback_period_years']
        st.info(f"💡 You'll break even in year {breakeven_year:.1f}. After that, it's pure profit!")

        # Interactive Map
        st.divider()
        st.subheader("🗺️ Location Map")

        import folium
        from streamlit_folium import st_folium

        m = folium.Map(
            location=[st.session_state.latitude, st.session_state.longitude],
            zoom_start=10,
            tiles='OpenStreetMap'
        )

        folium.Marker(
            [st.session_state.latitude, st.session_state.longitude],
            popup=f"""
            <b>Solar Site Analysis</b><br>
            Irradiance: {avg_irradiance:.2f} kWh/m²/day<br>
            ROI: {results['roi_percent']:.1f}%<br>
            Payback: {results['payback_period_years']:.1f} years
            """,
            icon=folium.Icon(color='orange', icon='sun', prefix='fa')
        ).add_to(m)

        folium.Circle(
            [st.session_state.latitude, st.session_state.longitude],
            radius=500,
            color='orange',
            fill=True,
            fillOpacity=0.2,
            popup='Proposed Solar Farm Area'
        ).add_to(m)

        st_folium(m, width=700, height=400)

        # Add comparison feature after analysis
        st.divider()
        st.subheader("🔄 Compare Multiple Locations")

        with st.expander("📍 Compare 2-3 Locations Side-by-Side", expanded=False):
            st.write("Enter coordinates for up to 3 locations to compare their solar potential:")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write("**Location 1**")
                lat1_post = st.number_input("Lat 1", -90.0, 90.0, 33.45, key="lat1_post")
                lon1_post = st.number_input("Lon 1", -180.0, 180.0, -112.07, key="lon1_post")
                name1_post = st.text_input("Name (optional)", "Phoenix, AZ", key="name1_post")

            with col2:
                st.write("**Location 2**")
                lat2_post = st.number_input("Lat 2", -90.0, 90.0, 36.17, key="lat2_post")
                lon2_post = st.number_input("Lon 2", -180.0, 180.0, -115.14, key="lon2_post")
                name2_post = st.text_input("Name (optional)", "Las Vegas, NV", key="name2_post")

            with col3:
                st.write("**Location 3**")
                lat3_post = st.number_input("Lat 3", -90.0, 90.0, 25.76, key="lat3_post")
                lon3_post = st.number_input("Lon 3", -180.0, 180.0, -80.19, key="lon3_post")
                name3_post = st.text_input("Name (optional)", "Miami, FL", key="name3_post")

            comp_system_size_post = st.slider("System Size for Comparison (kW)", 10, 1000, 100, key="comp_size_post")
            comp_elec_rate_post = st.slider("Electricity Rate for Comparison ($/kWh)", 0.05, 0.30, 0.12, 0.01, key="comp_rate_post")

            if st.button("🔍 Compare Locations", type="primary", key="compare_post"):
                st.session_state.comparison_done = True
                st.session_state.comparison_locations = [
                    (lat1_post, lon1_post, name1_post),
                    (lat2_post, lon2_post, name2_post),
                    (lat3_post, lon3_post, name3_post)
                ]
                st.session_state.comp_system_size = comp_system_size_post
                st.session_state.comp_elec_rate = comp_elec_rate_post
                st.session_state.comparison_data = None  # Reset comparison data

else:
    # Welcome screen
    st.info("👈 Enter location and system parameters in the sidebar, then click 'Analyze Investment'")

    st.markdown("---")

    # Add comparison feature
    st.subheader("🔄 Compare Multiple Locations")

    with st.expander("📍 Compare 2-3 Locations Side-by-Side", expanded=False):
        st.write("Enter coordinates for up to 3 locations to compare their solar potential:")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("**Location 1**")
            lat1 = st.number_input("Lat 1", -90.0, 90.0, 33.45, key="lat1")
            lon1 = st.number_input("Lon 1", -180.0, 180.0, -112.07, key="lon1")
            name1 = st.text_input("Name (optional)", "Phoenix, AZ", key="name1")

        with col2:
            st.write("**Location 2**")
            lat2 = st.number_input("Lat 2", -90.0, 90.0, 36.17, key="lat2")
            lon2 = st.number_input("Lon 2", -180.0, 180.0, -115.14, key="lon2")
            name2 = st.text_input("Name (optional)", "Las Vegas, NV", key="name2")

        with col3:
            st.write("**Location 3**")
            lat3 = st.number_input("Lat 3", -90.0, 90.0, 25.76, key="lat3")
            lon3 = st.number_input("Lon 3", -180.0, 180.0, -80.19, key="lon3")
            name3 = st.text_input("Name (optional)", "Miami, FL", key="name3")

        comp_system_size = st.slider("System Size for Comparison (kW)", 10, 1000, 100, key="comp_size")
        comp_elec_rate = st.slider("Electricity Rate for Comparison ($/kWh)", 0.05, 0.30, 0.12, 0.01, key="comp_rate")

        if st.button("🔍 Compare Locations", type="primary"):
            st.session_state.comparison_done = True
            st.session_state.comparison_locations = [
                (lat1, lon1, name1),
                (lat2, lon2, name2),
                (lat3, lon3, name3)
            ]
            st.session_state.comp_system_size = comp_system_size
            st.session_state.comp_elec_rate = comp_elec_rate

    st.markdown("---")

    st.subheader("How it works:")
    st.markdown("""
    1. **Enter GPS coordinates** of your desired location
    2. **Set system size** and electricity rate
    3. **Get real NASA satellite data** for solar irradiance
    4. **See detailed ROI analysis** with 25-year projections
    5. **Compare multiple locations** to find the best spot
    """)

    st.subheader("What you'll get:")
    st.markdown("""
    - ✅ Return on Investment (ROI) percentage
    - ✅ Payback period in years
    - ✅ Annual energy production estimates
    - ✅ 25-year profit projections
    - ✅ Historical solar irradiance data
    - ✅ Interactive cash flow charts
    - ✅ Location maps
    - ✅ Multi-location comparison
    """)

if st.session_state.comparison_done:
    locations = st.session_state.comparison_locations
    comp_system_size = st.session_state.comp_system_size
    comp_elec_rate = st.session_state.comp_elec_rate

    # Only fetch if we don't have data yet
    if st.session_state.comparison_data is None:
        comparison_data = []

        progress_bar = st.progress(0)
        status_text = st.empty()

        for idx, (lat, lon, name) in enumerate(locations):
            status_text.text(f"Fetching data for {name}...")

            solar_df = get_solar_data(lat, lon, '2024-01-01', '2024-12-31')

            if solar_df is not None:
                avg_irradiance = solar_df['solar_irradiance'].mean()

                calculator = SolarROICalculator()
                results = calculator.calculate_roi(avg_irradiance, comp_system_size, comp_elec_rate)

                comparison_data.append({
                    'Location': name,
                    'Latitude': lat,
                    'Longitude': lon,
                    'Avg Irradiance (kWh/m²/day)': f"{avg_irradiance:.2f}",
                    'ROI (%)': f"{results['roi_percent']:.1f}%",
                    'Payback (years)': f"{results['payback_period_years']:.1f}",
                    'Annual Production (kWh)': f"{results['annual_production_kwh']:,.0f}",
                    'Net Profit ($)': f"${results['net_profit']:,.0f}"
                })

            progress_bar.progress((idx + 1) / 3)

        status_text.text("✅ Comparison complete!")
        st.session_state.comparison_data = comparison_data
    else:
        comparison_data = st.session_state.comparison_data

    # Display comparison table
    st.subheader("📊 Comparison Results")

    import pandas as pd
    df_comparison = pd.DataFrame(comparison_data)
    st.dataframe(df_comparison, use_container_width=True)

    # Visual comparison charts
    st.subheader("📈 Visual Comparison")

    import plotly.graph_objects as go

    # ROI Comparison Bar Chart
    fig_roi = go.Figure(data=[
        go.Bar(
            x=[item['Location'] for item in comparison_data],
            y=[float(item['ROI (%)'].strip('%')) for item in comparison_data],
            text=[item['ROI (%)'] for item in comparison_data],
            textposition='auto',
            marker_color=['#10b981', '#3b82f6', '#f59e0b']
        )
    ])
    fig_roi.update_layout(
        title="ROI Comparison",
        xaxis_title="Location",
        yaxis_title="ROI (%)",
        height=400
    )
    st.plotly_chart(fig_roi, use_container_width=True)

    # Payback Period Comparison
    fig_payback = go.Figure(data=[
        go.Bar(
            x=[item['Location'] for item in comparison_data],
            y=[float(item['Payback (years)']) for item in comparison_data],
            text=[item['Payback (years)'] for item in comparison_data],
            textposition='auto',
            marker_color=['#ef4444', '#8b5cf6', '#ec4899']
        )
    ])
    fig_payback.update_layout(
        title="Payback Period Comparison",
        xaxis_title="Location",
        yaxis_title="Years",
        height=400
    )
    st.plotly_chart(fig_payback, use_container_width=True)

    # Map with all locations
    st.subheader("🗺️ All Locations on Map")

    import folium
    from streamlit_folium import st_folium

    # Calculate center point
    avg_lat = sum([loc[0] for loc in locations]) / 3
    avg_lon = sum([loc[1] for loc in locations]) / 3

    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=4)

    colors = ['red', 'blue', 'green']
    for idx, (lat, lon, name) in enumerate(locations):
        folium.Marker(
            [lat, lon],
            popup=f"<b>{name}</b><br>{comparison_data[idx]['ROI (%)']} ROI",
            icon=folium.Icon(color=colors[idx], icon='sun', prefix='fa')
        ).add_to(m)

    st_folium(m, width=700, height=500)
