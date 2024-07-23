class DCCalculator:
    def __init__(self):
        self.annual_growth_rate = 0.05  # Example: 5% annual growth

    def calculate_pension_pot(self, contributions, years):
        total_pot = contributions * ((1 + self.annual_growth_rate) ** years - 1) / self.annual_growth_rate
        return round(total_pot, 2)

    def calculate_annuity(self, pension_pot, annuity_rate):
        annual_pension = pension_pot * annuity_rate
        return round(annual_pension, 2)