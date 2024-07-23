from datetime import date

class DBCalculator:
    def __init__(self):
        self.accrual_rate = 0.0167  # Example: 1/60th
        self.normal_retirement_age = 65
        self.early_retirement_factor = 0.05  # 5% reduction per year early
        self.late_retirement_factor = 0.08  # 8% increase per year late
        self.commutation_factor = 12  # £12 lump sum for each £1 of pension given up
        self.lifetime_allowance = 1073100  # LTA for 2023/24
        self.annual_allowance = 60000  # AA for 2023/24
        self.normal_minimum_pension_age = 55  # NMPA as of 2023

    def calculate_pension(self, final_salary, years_of_service):
        annual_pension = final_salary * years_of_service * self.accrual_rate
        return round(annual_pension, 2)

    def calculate_lump_sum(self, annual_pension):
        lump_sum = annual_pension * 3  # Example: 3 times the annual pension
        return round(lump_sum, 2)

    def calculate_early_retirement(self, annual_pension, retirement_age):
        years_early = max(0, self.normal_retirement_age - retirement_age)
        reduction_factor = 1 - (years_early * self.early_retirement_factor)
        reduced_pension = annual_pension * reduction_factor
        return round(reduced_pension, 2)

    def calculate_late_retirement(self, annual_pension, retirement_age):
        years_late = max(0, retirement_age - self.normal_retirement_age)
        increase_factor = 1 + (years_late * self.late_retirement_factor)
        increased_pension = annual_pension * increase_factor
        return round(increased_pension, 2)

    def calculate_commutation(self, annual_pension, amount_to_commute):
        reduced_pension = annual_pension - amount_to_commute
        lump_sum = amount_to_commute * self.commutation_factor
        return round(reduced_pension, 2), round(lump_sum, 2)

    def check_lifetime_allowance(self, annual_pension):
        pension_value = annual_pension * 20  # Standard valuation factor for DB pensions
        excess = max(0, pension_value - self.lifetime_allowance)
        return pension_value, excess

    def check_annual_allowance(self, annual_pension):
        pension_input_amount = annual_pension * 16  # Pension Input Amount for DB schemes
        excess = max(0, pension_input_amount - self.annual_allowance)
        return pension_input_amount, excess

    def check_minimum_pension_age(self, retirement_age):
        return retirement_age >= self.normal_minimum_pension_age

    def get_state_pension_age(self, birth_year):
        # Simplified SPA calculation - this would be more complex in reality
        if birth_year < 1960:
            return 66
        elif birth_year < 1977:
            return 67
        else:
            return 68