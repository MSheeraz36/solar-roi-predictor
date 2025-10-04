import streamlit as st
import sys
import os

# Add current directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.solar_data import get_solar_data
from models.roi_calculator import SolarROICalculator

st.set_page_config(page_title="Solar ROI Predictor", layout="wide")

# Initialize session state
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
if 'results' not in st.session_state:
    st.session_state.results = None
if 'solar_df' not in st.session_state:
    st.session_state.solar_df = None
if 'avg_irradiance' not in st.session_state:
    st.session_state.avg_irradiance = None

# Header
st.title("☀️ Solar Farm ROI Predictor")
st.subheader("Analyze Solar Investment Returns using NASA Satellite Data")

# Sidebar
with st.sidebar:
    st.header("📍 Location & Parameters")
    
    col1, col2 = st.columns(2)
    latitude = col1.number_input("Latitude", -90.0, 90.0, 37.77)
    longitude = col2.number_input("Longitude", -180.0, 180.0, -122.42)
    
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
    st.write("**Phoenix, AZ**")
    st.caption("Lat: 33.45, Lon: -112.07")
    st.write("**Las Vegas, NV**")
    st.caption("Lat: 36.17, Lon: -115.14")
    st.write("**Miami, FL**")
    st.caption("Lat: 25.76, Lon: -80.19")

# Main area
if st.session_state.analyzed:
    # Only fetch data if we don't have it yet or parameters changed
    if (st.session_state.results is None or 
        st.session_state.latitude != latitude or 
        st.session_state.longitude != longitude or
        st.session_state.system_size != system_size or
        st.session_state.electricity_rate != electricity_rate):
        
        with st.spinner("🛰️ Fetching NASA satellite data..."):
            solar_df = get_solar_data(st.session_state.latitude, st.session_state.longitude, '2023-01-01', '2023-12-31')
            
        if solar_df is not None:
            avg_irradiance = solar_df['solar_irradiance'].mean()
            
            # Calculate ROI
            calculator = SolarROICalculator()
            results = calculator.calculate_roi(avg_irradiance, st.session_state.system_size, st.session_state.electricity_rate)
            
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
        st.subheader("📈 Daily Solar Irradiance - 2023")
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
        
else:
    # Welcome screen
    st.info("👈 Enter location and system parameters in the sidebar, then click 'Analyze Investment'")
    
    st.markdown("---")
    
    st.subheader("How it works:")
    st.markdown("""
    1. **Enter GPS coordinates** of your desired location
    2. **Set system size** and electricity rate
    3. **Get real NASA satellite data** for solar irradiance
    4. **See detailed ROI analysis** with 25-year projections
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
    """)