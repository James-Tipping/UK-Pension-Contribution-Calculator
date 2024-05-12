import numpy as np
np.random.seed(42)


class Calculate:

    @staticmethod
    def calculate_uk_income_tax(salary):
        if salary <= 12570:
            return 0  # No tax for income within the personal allowance
        
        # Income within the basic rate band
        if salary <= 50270:
            tax = (salary - 12570) * 0.20
            return tax
        
        # Income within the higher rate band
        if salary <= 150000:
            basic_tax = (50270 - 12570) * 0.20
            higher_tax = (salary - 50270) * 0.40
            return basic_tax + higher_tax
        
        # Income within the additional rate band
        basic_tax = (50270 - 12570) * 0.20
        higher_tax = (150000 - 50270) * 0.40
        additional_tax = (salary - 150000) * 0.45
        return basic_tax + higher_tax + additional_tax

    @staticmethod
    def calculate_annual_ni_contributions(salary):
        primary_threshold = 12_570  # Annual primary threshold
        upper_limit = 50_270  # Annual upper earnings limit
        
        if salary <= primary_threshold:
            return 0  # No contributions if salary is below the primary threshold
        
        # Contributions between the primary threshold and upper earnings limit
        if salary <= upper_limit:
            ni_contributions = (salary - primary_threshold) * 0.08
        else:
            # Contributions at the 12% rate up to the upper limit
            normal_contributions = (upper_limit - primary_threshold) * 0.08
            # Contributions at the 2% rate above the upper limit
            additional_contributions = (salary - upper_limit) * 0.02
            ni_contributions = normal_contributions + additional_contributions
        
        return ni_contributions

    @staticmethod
    def calculate_employer_ni_contributions(annual_salary):
        secondary_threshold = 9100  # Annual secondary threshold
        ni_rate = 0.138  # Employer NI rate
        
        if annual_salary <= secondary_threshold:
            return 0  # No contributions if salary is below the secondary threshold
        
        # Contributions on the amount above the secondary threshold
        ni_contributions = (annual_salary - secondary_threshold) * ni_rate
        
        return ni_contributions

    @staticmethod
    def calculate_salary_after_pension_deductions(salary, pension_contribution_rate):
        return salary * (1 - pension_contribution_rate)

    @staticmethod
    def calculate_personal_pension_contributions(salary, pension_contribution_rate):
        return salary * pension_contribution_rate

    @staticmethod
    def calculate_employer_pension_contributions(salary, employer_contribution_rate):
        return salary * employer_contribution_rate
    
    @staticmethod
    def net_salary_after_pension_tax_ni(salary, personal_contribution):
        salary_after_pension = Calculate.calculate_salary_after_pension_deductions(salary, personal_contribution)
        income_tax = Calculate.calculate_uk_income_tax(salary_after_pension)
        ni = Calculate.calculate_annual_ni_contributions(salary_after_pension)
        return salary_after_pension - (income_tax + ni)
    
    @staticmethod
    def calculate_company_saving(salary, scheme_personal_contribution):
        # Calculate salary difference from 5% to scheme_personal_contribution
        taxable_salary_5_pc_pension = Calculate.calculate_salary_after_pension_deductions(salary, 0.05)
        taxable_salary = Calculate.calculate_salary_after_pension_deductions(salary, scheme_personal_contribution)
        
        # Calculate NI difference from 5% to scheme_personal_contribution
        initial_ni = Calculate.calculate_employer_ni_contributions(taxable_salary_5_pc_pension)
        final_ni = Calculate.calculate_employer_ni_contributions(taxable_salary)
        
        return (initial_ni - final_ni) / 2
    
    @staticmethod
    def get_salary_distribution(mean_salary: float | int, sigma: float | int, n_employees: int) -> np.ndarray:

        # Calculate mu for the log-normal distribution
        mu = np.log(mean_salary) - sigma**2 / 2
        
        return np.random.lognormal(mu, sigma, n_employees)
    
    @staticmethod
    def calculate_company_savings(salary_distribution: np.ndarray, percent_increase: float | int, new_contribution_amount: float | int) -> float:
    
        # Select random employees to increase their pension contributions
        n_employees_increase = int(len(salary_distribution) * percent_increase / 100)
        employees_increase = np.random.choice(salary_distribution, n_employees_increase)
        
        # Calculate company savings from NI contributions
        company_savings = 0
        for salary in employees_increase:
            
            previous_taxable_salary = Calculate.calculate_salary_after_pension_deductions(salary, 0.05)
            previous_contributions = Calculate.calculate_employer_ni_contributions(previous_taxable_salary)
            
            new_taxable_salary = Calculate.calculate_salary_after_pension_deductions(salary, new_contribution_amount)
            new_contributions = Calculate.calculate_employer_ni_contributions(new_taxable_salary)
            
            company_savings += ((previous_contributions - new_contributions) / 2)
        
        return company_savings
        
        