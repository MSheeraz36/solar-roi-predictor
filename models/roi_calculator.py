class SolarROICalculator:
    def __init__(self):
        # Industry standard values
        self.panel_efficiency = 0.20  # 20%
        self.performance_ratio = 0.75  # Accounts for losses
        self.system_cost_per_kw = 1000  # USD
        self.degradation_rate = 0.005  # 0.5% per year
        
    def calculate_roi(self, avg_solar_irradiance, system_size_kw, electricity_rate=0.12, years=25):
        """
        Calculate ROI for solar installation
        
        Parameters:
        - avg_solar_irradiance: Average daily solar irradiance (kWh/m²/day)
        - system_size_kw: System size in kilowatts
        - electricity_rate: Cost per kWh in USD
        - years: Investment period (default 25 years)
        
        Returns: Dictionary with financial metrics
        """
        # Annual energy production
        annual_kwh = (
            system_size_kw * 
            avg_solar_irradiance * 
            365 * 
            self.performance_ratio
        )
        
        # Financial calculations
        capex = system_size_kw * self.system_cost_per_kw
        
        total_revenue = 0
        for year in range(1, years + 1):
            # Account for panel degradation
            year_production = annual_kwh * ((1 - self.degradation_rate) ** year)
            year_revenue = year_production * electricity_rate
            total_revenue += year_revenue
        
        # Calculate metrics
        roi_percent = ((total_revenue - capex) / capex) * 100
        payback_period = capex / (annual_kwh * electricity_rate)
        
        return {
            'annual_production_kwh': annual_kwh,
            'total_investment': capex,
            'total_revenue_25y': total_revenue,
            'net_profit': total_revenue - capex,
            'roi_percent': roi_percent,
            'payback_period_years': payback_period
        }

# Test the calculator
if __name__ == "__main__":
    print("Testing ROI Calculator...")
    calc = SolarROICalculator()
    results = calc.calculate_roi(
        avg_solar_irradiance=5.5,  # kWh/m²/day (Phoenix-like conditions)
        system_size_kw=100,
        electricity_rate=0.12
    )
    print("✅ ROI Calculator works!")
    print(f"ROI: {results['roi_percent']:.1f}%")
    print(f"Payback Period: {results['payback_period_years']:.1f} years")
    print(f"Net Profit: ${results['net_profit']:,.0f}")
    print(f"Annual Production: {results['annual_production_kwh']:,.0f} kWh")