import sys
from datetime import date
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTabWidget, QMessageBox, QComboBox
from db_calculator import DBCalculator
from dc_calculator import DCCalculator
from database import PensionDatabase

class PensionCalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Pension Calculator")
        self.setGeometry(100, 100, 500, 400)

        self.db_calculator = DBCalculator()
        self.dc_calculator = DCCalculator()
        self.db = PensionDatabase()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.create_widgets()

    def create_widgets(self):
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        # DB Pension Tab
        self.db_tab = QWidget()
        self.db_layout = QVBoxLayout(self.db_tab)

        self.db_scheme_layout = QHBoxLayout()
        self.db_scheme_layout.addWidget(QLabel("DB Scheme:"))
        self.db_scheme_combo = QComboBox()
        self.db_scheme_layout.addWidget(self.db_scheme_combo)
        self.db_layout.addLayout(self.db_scheme_layout)

        self.final_salary_layout = QHBoxLayout()
        self.final_salary_layout.addWidget(QLabel("Final Salary:"))
        self.final_salary = QLineEdit()
        self.final_salary_layout.addWidget(self.final_salary)
        self.db_layout.addLayout(self.final_salary_layout)

        self.years_of_service_layout = QHBoxLayout()
        self.years_of_service_layout.addWidget(QLabel("Years of Service:"))
        self.years_of_service = QLineEdit()
        self.years_of_service_layout.addWidget(self.years_of_service)
        self.db_layout.addLayout(self.years_of_service_layout)

        self.retirement_age_layout = QHBoxLayout()
        self.retirement_age_layout.addWidget(QLabel("Retirement Age:"))
        self.retirement_age = QLineEdit()
        self.retirement_age_layout.addWidget(self.retirement_age)
        self.db_layout.addLayout(self.retirement_age_layout)

        self.birth_year_layout = QHBoxLayout()
        self.birth_year_layout.addWidget(QLabel("Birth Year:"))
        self.birth_year = QLineEdit()
        self.birth_year_layout.addWidget(self.birth_year)
        self.db_layout.addLayout(self.birth_year_layout)

        self.commute_amount_layout = QHBoxLayout()
        self.commute_amount_layout.addWidget(QLabel("Amount to Commute:"))
        self.commute_amount = QLineEdit()
        self.commute_amount_layout.addWidget(self.commute_amount)
        self.db_layout.addLayout(self.commute_amount_layout)

        self.calculate_db_button = QPushButton("Calculate DB Pension")
        self.calculate_db_button.clicked.connect(self.calculate_db_pension)
        self.db_layout.addWidget(self.calculate_db_button)

        self.tab_widget.addTab(self.db_tab, "DB Pension")

        # DC Pension Tab
        self.dc_tab = QWidget()
        self.dc_layout = QVBoxLayout(self.dc_tab)

        self.dc_scheme_layout = QHBoxLayout()
        self.dc_scheme_layout.addWidget(QLabel("DC Scheme:"))
        self.dc_scheme_combo = QComboBox()
        self.dc_scheme_layout.addWidget(self.dc_scheme_combo)
        self.dc_layout.addLayout(self.dc_scheme_layout)

        self.annual_contribution_layout = QHBoxLayout()
        self.annual_contribution_layout.addWidget(QLabel("Annual Contribution:"))
        self.annual_contribution = QLineEdit()
        self.annual_contribution_layout.addWidget(self.annual_contribution)
        self.dc_layout.addLayout(self.annual_contribution_layout)

        self.years_to_retirement_layout = QHBoxLayout()
        self.years_to_retirement_layout.addWidget(QLabel("Years to Retirement:"))
        self.years_to_retirement = QLineEdit()
        self.years_to_retirement_layout.addWidget(self.years_to_retirement)
        self.dc_layout.addLayout(self.years_to_retirement_layout)

        self.annuity_rate_layout = QHBoxLayout()
        self.annuity_rate_layout.addWidget(QLabel("Annuity Rate (%):"))
        self.annuity_rate = QLineEdit()
        self.annuity_rate_layout.addWidget(self.annuity_rate)
        self.dc_layout.addLayout(self.annuity_rate_layout)

        self.dc_birth_year_layout = QHBoxLayout()
        self.dc_birth_year_layout.addWidget(QLabel("Birth Year:"))
        self.dc_birth_year = QLineEdit()
        self.dc_birth_year_layout.addWidget(self.dc_birth_year)
        self.dc_layout.addLayout(self.dc_birth_year_layout)

        self.calculate_dc_button = QPushButton("Calculate DC Pension")
        self.calculate_dc_button.clicked.connect(self.calculate_dc_pension)
        self.dc_layout.addWidget(self.calculate_dc_button)

        self.tab_widget.addTab(self.dc_tab, "DC Pension")

        # Load schemes from database
        self.load_schemes()

    def load_schemes(self):
        # Load DB schemes
        db_schemes = self.db.get_db_schemes()
        for scheme in db_schemes:
            self.db_scheme_combo.addItem(scheme[1], scheme)

        # Load DC schemes
        dc_schemes = self.db.get_dc_schemes()
        for scheme in dc_schemes:
            self.dc_scheme_combo.addItem(scheme[1], scheme)

    def calculate_db_pension(self):
        try:
            scheme = self.db_scheme_combo.currentData()
            if scheme:
                self.db_calculator.accrual_rate = scheme[2]
                self.db_calculator.normal_retirement_age = scheme[3]
            
            final_salary = float(self.final_salary.text())
            years_of_service = float(self.years_of_service.text())
            retirement_age = float(self.retirement_age.text())
            birth_year = int(self.birth_year.text())
            commute_amount = float(self.commute_amount.text())

            annual_pension = self.db_calculator.calculate_pension(final_salary, years_of_service)
            
            # Check minimum pension age
            if not self.db_calculator.check_minimum_pension_age(retirement_age):
                QMessageBox.warning(self, "Warning", f"Retirement age is below the Normal Minimum Pension Age of {self.db_calculator.normal_minimum_pension_age}")

            # Calculate early/late retirement adjustment
            if retirement_age < self.db_calculator.normal_retirement_age:
                annual_pension = self.db_calculator.calculate_early_retirement(annual_pension, retirement_age)
            elif retirement_age > self.db_calculator.normal_retirement_age:
                annual_pension = self.db_calculator.calculate_late_retirement(annual_pension, retirement_age)
            
            # Calculate commutation
            reduced_pension, lump_sum = self.db_calculator.calculate_commutation(annual_pension, commute_amount)

            # Check Lifetime Allowance
            pension_value, lta_excess = self.db_calculator.check_lifetime_allowance(annual_pension)

            # Check Annual Allowance
            pension_input_amount, aa_excess = self.db_calculator.check_annual_allowance(annual_pension)

            # Get State Pension Age
            state_pension_age = self.db_calculator.get_state_pension_age(birth_year)

            message = (f"Annual Pension (before commutation): £{annual_pension:,.2f}\n"
                       f"Annual Pension (after commutation): £{reduced_pension:,.2f}\n"
                       f"Lump Sum: £{lump_sum:,.2f}\n\n"
                       f"Pension Value for LTA: £{pension_value:,.2f}\n"
                       f"LTA Excess: £{lta_excess:,.2f}\n"
                       f"Pension Input Amount for AA: £{pension_input_amount:,.2f}\n"
                       f"AA Excess: £{aa_excess:,.2f}\n"
                       f"State Pension Age: {state_pension_age}")

            QMessageBox.information(self, "DB Pension Calculation", message)
        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter valid numerical values.")

    def calculate_dc_pension(self):
        try:
            scheme = self.dc_scheme_combo.currentData()
            if scheme:
                default_contribution_rate = scheme[2]
            else:
                default_contribution_rate = 0.05  # 5% default if no scheme selected

            annual_salary = float(self.annual_contribution.text()) / default_contribution_rate
            years = float(self.years_to_retirement.text())
            annuity_rate = float(self.annuity_rate.text()) / 100
            birth_year = int(self.dc_birth_year.text())

            pension_pot = self.dc_calculator.calculate_pension_pot(annual_salary * default_contribution_rate, years)
            annual_pension = self.dc_calculator.calculate_annuity(pension_pot, annuity_rate)

            # Check Lifetime Allowance
            lta_excess = max(0, pension_pot - self.db_calculator.lifetime_allowance)

            # Check Annual Allowance
            aa_excess = max(0, annual_salary * default_contribution_rate - self.db_calculator.annual_allowance)

            # Get State Pension Age
            state_pension_age = self.db_calculator.get_state_pension_age(birth_year)

            message = (f"Projected Pension Pot: £{pension_pot:,.2f}\n"
                       f"Estimated Annual Pension: £{annual_pension:,.2f}\n\n"
                       f"LTA Excess: £{lta_excess:,.2f}\n"
                       f"AA Excess: £{aa_excess:,.2f}\n"
                       f"State Pension Age: {state_pension_age}")

            QMessageBox.information(self, "DC Pension Calculation", message)
        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter valid numerical values.")

def main():
    app = QApplication(sys.argv)
    window = PensionCalculatorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()