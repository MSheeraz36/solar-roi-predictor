# Solar ROI Predictor 🌞

A web application built for the **NASA Space App Challenge** that predicts the financial return on investment (ROI) for solar farm installations using real-time NASA satellite data on solar irradiance.

![Solar ROI Predictor](https://img.shields.io/badge/NASA-Space%20App%20Challenge-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red)

## 🎯 Project Overview

The Solar ROI Predictor helps investors, homeowners, and businesses make data-driven decisions about solar energy investments. By leveraging NASA's POWER (Prediction Of Worldwide Energy Resources) API, the application provides accurate solar irradiance data for any location on Earth and calculates comprehensive financial metrics over a 25-year projection period.

### Key Features

- **Real NASA Satellite Data**: Fetches daily solar irradiance data from NASA POWER API
- **Accurate ROI Calculations**: Calculates payback period, net profit, and ROI percentage
- **Interactive Visualizations**:
  - Solar irradiance trends throughout the year
  - 25-year cash flow projections
  - Interactive location maps
- **Multi-Location Comparison**: Compare ROI across up to 3 different locations
- **User-Friendly Interface**: Built with Streamlit for easy interaction
- **Session State Caching**: Avoids redundant API calls for better performance

## 🚀 Demo

**Live App**: [https://solar-roi-predictor.streamlit.app/](https://solar-roi-predictor.streamlit.app/)

### Single Location Analysis
Enter GPS coordinates, system size, and electricity rate to get:
- Average daily solar irradiance
- Annual energy production estimate
- Total investment required
- 25-year revenue projection
- Net profit and ROI percentage
- Payback period

### Multi-Location Comparison
Compare multiple locations side-by-side to find the optimal site for your solar farm investment.

## 🛠️ Technology Stack

- **Python 3.8+**: Core programming language
- **Streamlit**: Web application framework
- **NASA POWER API**: Solar irradiance data source
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive data visualizations
- **Folium**: Interactive mapping
- **Requests**: API communication

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/waqadArshad/solar-roi-predictor-waqad.git
cd solar-roi-predictor-waqad
```

2. **Navigate to the application directory**
```bash
cd solar-roi-predictor
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run Home.py
```

5. **Access the application**
Open your browser and navigate to `http://localhost:8501`

## 🎮 Usage

### Single Location Analysis

1. **Enter Location Details**
   - Latitude (e.g., 33.6846 for Karachi)
   - Longitude (e.g., 73.0479 for Islamabad)

2. **Configure System Parameters**
   - System Size (kW): Size of your solar installation
   - Electricity Rate ($/kWh): Your current electricity cost

3. **Click "Analyze Location"**
   - View solar irradiance data
   - See financial projections
   - Explore interactive charts

### Multi-Location Comparison

1. **Switch to "Compare Multiple Locations" mode**
2. **Enter details for 2-3 locations**
3. **Click "Compare Locations"**
4. **Review side-by-side comparison**
   - ROI percentages
   - Payback periods
   - Net profits
   - Interactive map with markers

## 📊 How It Works

### Data Flow

```
User Input → NASA POWER API → Data Processing → ROI Calculation → Visualization
```

1. **User Input**: Collects GPS coordinates, system size, and electricity rate
2. **NASA API**: Fetches daily solar irradiance data (`ALLSKY_SFC_SW_DWN`) for 2024
3. **ROI Calculation**: Processes irradiance data using industry-standard formulas
4. **Visualization**: Displays results with interactive charts and maps

### ROI Calculation Parameters

- **Panel Efficiency**: 20%
- **Performance Ratio**: 75% (accounts for system losses)
- **System Cost**: $1,000 per kW
- **Annual Degradation**: 0.5%
- **Projection Period**: 25 years

### Formula

```
Annual Energy Production = Avg Irradiance × System Size × Panel Efficiency × Performance Ratio × 365

Annual Revenue = Annual Energy Production × Electricity Rate

Total Investment = System Size × Cost per kW

ROI (%) = (Total Revenue - Total Investment) / Total Investment × 100

Payback Period = Total Investment / Annual Revenue
```

## 📁 Project Structure

```
solar-roi-predictor-waqad/
├── solar-roi-predictor/
│   ├── Home.py                    # Main Streamlit application
│   ├── data/
│   │   └── solar_data.py          # NASA API data fetching module
│   ├── models/
│   │   ├── roi_calculator.py      # ROI calculation logic
│   │   └── ml_model.py            # Placeholder for ML features
│   ├── utils/
│   │   └── visualizations.py      # Visualization utilities (placeholder)
│   └── requirements.txt           # Python dependencies
├── CLAUDE.md                      # Development guide
└── README.md                      # This file
```

## 🔧 Key Modules

### `Home.py`
Main application file with Streamlit UI, session state management, and visualization logic.

### `data/solar_data.py`
- `get_solar_data(lat, lon, start_date, end_date)`: Fetches solar irradiance from NASA POWER API
- Returns pandas DataFrame with daily irradiance values

### `models/roi_calculator.py`
- `SolarROICalculator`: Class for calculating ROI metrics
- `calculate_roi()`: Returns annual production, investment, revenue, profit, ROI%, and payback period

## 🌍 NASA POWER API

This application uses NASA's POWER API to access global solar irradiance data:

- **Endpoint**: `https://power.larc.nasa.gov/api/temporal/daily/point`
- **Parameter**: `ALLSKY_SFC_SW_DWN` (All Sky Surface Shortwave Downward Irradiance)
- **Units**: kWh/m²/day
- **Coverage**: Global, any location on Earth
- **Authentication**: None required (public API)

## 🎯 Use Cases

- **Homeowners**: Determine if solar panels are a good investment for your property
- **Businesses**: Evaluate solar installations for commercial buildings
- **Investors**: Compare potential solar farm locations
- **Researchers**: Analyze solar energy potential across different regions
- **Policy Makers**: Assess renewable energy viability for specific areas

## 🔮 Future Enhancements

- [ ] Add machine learning predictions for future irradiance
- [ ] Include weather pattern analysis
- [ ] Support for different panel types and efficiencies
- [ ] Integration with electricity pricing APIs
- [ ] Carbon offset calculations
- [ ] Export reports to PDF
- [ ] Historical comparison (multi-year data)
- [ ] Mobile-responsive design improvements

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b waqadArshad/solar-roi-predictor-waqad`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin waqadArshad/solar-roi-predictor-waqad`)
5. Open a Pull Request

## 📝 License

This project was created for the NASA Space App Challenge.

## 👥 Team NASA Techies 🇵🇰

Created with ❤️ for the NASA Space App Challenge 2025

## 🙏 Acknowledgments

- **NASA POWER Project**: For providing free access to global solar irradiance data
- **Streamlit**: For the amazing web framework
- **NASA Space App Challenge**: For inspiring this project

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Note**: This application uses 2024 solar irradiance data. The 25-year ROI projections are estimates based on current industry standards and may vary with actual installation conditions, policy changes, and technological improvements.
