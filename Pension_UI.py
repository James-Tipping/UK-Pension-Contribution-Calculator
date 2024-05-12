import streamlit as st
import numpy as np
from Pension_Functions import Calculate
import pandas as pd
import plotly.express as px

def main():
    np.random.seed(42)
    st.set_page_config(layout="wide")
    
    st.title('Standard Pension Salary Sacrifice Calculator')

    salary = st.number_input(
        'Annual Salary (£)',
        min_value=25_000,
        max_value=200_000,
        value=45_000,
        step=1_000)
    
    # Add a selectbox to the sidebar:
    personal_contribution = st.slider(
        'Personal Pension Contribution (%)',
        min_value=0, max_value=100, value=5, step=1)
    
    company_contribution = st.slider(
        'Company Pension Contribution (%)',
        min_value=0, max_value=100, value=5, step=1)
    
    
    salary_after_pension = Calculate.calculate_salary_after_pension_deductions(salary, personal_contribution/100)

    # Display the selected option with 'st.write()'
    st.write(f'''With an annual salary of :green[£{salary:,.0f}],
             a personal pension contribution of :green[{personal_contribution:,.0f}%] 
             and an employer pension contribution of :green[{company_contribution:,.0f}%]:''')
    
    st.write(f'Your annual income tax is: :green[£{Calculate.calculate_uk_income_tax(salary_after_pension):,.2f}]')
    st.write(f'Your annual NI payments are: :green[£{Calculate.calculate_annual_ni_contributions(salary_after_pension):,.2f}]')
    st.write(f'The annual employer NI payments are: :green[£{Calculate.calculate_employer_ni_contributions(salary_after_pension):,.2f}]')
    st.write(f'Your salary after pension deductions, NI, and income tax is: :green[£{Calculate.net_salary_after_pension_tax_ni(salary, personal_contribution/100):,.2f}]')
    st.write(f'''The total pension contributions are: 
             :green[£{Calculate.calculate_employer_pension_contributions(salary, company_contribution/100) +
             Calculate.calculate_personal_pension_contributions(salary, personal_contribution/100):,.2f}]''')

    st.title('The Proposed Pension Scheme')
    
    st.write('''
            When personal pension contributions are increased using a salary sacrifice scheme (as used at many major UK corporations),
            both the employee and employer save on National Insurance contributions. This is due to the fact that pension contributions
            via salary sacrifice decrease the taxable salary, resulting in less NI being paid by both parties.
            ''')
    
    st.write('''
            If companies were to :red[offer 50%] of the relevant employer NI savings to the employee in the form of :red[additional pension 
            contributions], this would incentive employees to save more towards their pension. This would be :red[beneficial to employees] and 
            :red[save the company money]. This is a method of offering an :red[effective pay increase] to employees whilst :red[decreasing company costs].
            ''')
    
    st.title('Breakdown of the Proposed Scheme')
    
    st.write('''
                - The data below assumes that the employee is currently contributing 5% of their salary to their pension, and the company contributes 4%.
                - It is also assumed that the employee has no student loan repayments, with other deductions and benefits not considered. 
                - Only employee pension contributions above 5% attract the additional 50% employer NI savings.
                - The company saving is equal to the pension increase under the scheme for the employee. This is calculated by
                halving the difference in employer NI contributions between the 5% and the new pension contribution. Therefore, the 
                employer and employee equally share the employer NI savings.
                - The "New Total Pension Contributions" column shows the total pension contributions under the proposed scheme, including 
                50% of the employer NI savings.
              ''')
        
    scheme_personal_contribution = st.slider(
        'Personal Pension Contribution (%)',
        max_value=100, min_value=5, value=5, step=1)
    
    salaries_list = np.arange(30_000, 100_000, 1000)
    df = pd.DataFrame({
                        'Salary Net of Deductions & Tax': [
                            Calculate.net_salary_after_pension_tax_ni(salary, scheme_personal_contribution/100)
                            for salary in salaries_list
                            ],
                        'Annual Employer NI Payments': [
                            Calculate.calculate_employer_ni_contributions(Calculate.calculate_salary_after_pension_deductions(salary, scheme_personal_contribution/100)) 
                            for salary in salaries_list
                            ],
                        'Pre-Scheme Total Pension (5+4)%': [
                            Calculate.calculate_employer_pension_contributions(salary, 0.04) 
                            + Calculate.calculate_personal_pension_contributions(salary, 0.05) 
                            for salary in salaries_list
                            ],
                        'New Total Pension Contributions': [
                            Calculate.calculate_employer_pension_contributions(salary, 0.04) 
                            + Calculate.calculate_personal_pension_contributions(salary, scheme_personal_contribution/100) 
                            + Calculate.calculate_company_saving(salary, scheme_personal_contribution/100) 
                            for salary in salaries_list
                            ],
                        'Pension Increase Under Scheme / Company Saving': [
                            Calculate.calculate_company_saving(salary, scheme_personal_contribution/100) 
                            for salary in salaries_list]},
                    index=salaries_list,
                    )
    df.index.name = 'Annual Salary'
    
    st.write(df)
    
    st.title('Company Savings From The Scheme')
    
    st.write('''
            Using the sliders below, decide your average salary for the company.
            A range of salaries will be created using a log-normal distribution to simulate the company's salary distribution.
            Then, choose the percentage of employees you expect to increase their pension contributions, and the new pension contributions
            of those chosen employees as a percentage of gross salary. Also, choose the number of employees,
            and the standard deviation of salary values in the underlying distribution. Increasing the standard deviation increases the range of salaries in the company.
            The company savings are calculated by summing the employer NI savings from all employees who increase their pension contributions.
            
            Notes: 
             - The salary range is pseduorandomly generated, and so may vary when particular values are changed.
             - The employees who increase their pension contributions are also pseudorandomly selected.
             - A 'seed' value of 42 is used to ensure reproducibility. This means that if the same values are used, the same pseudorandom results will be produced. However, choosing different values may vary the distribution significantly.
             - The company saving is calculated by summing the employer NI savings from all employees who increase their personl pension 
             contributions from an original figure of 5%.
             ''')
    
    average_salary = st.number_input('Average Salary (£)', value=45_000, step=5_000)
    n_employees = st.number_input('Number of Employees', value=500, step=50)
    percent_employees_increase_contribution = st.slider('Percentage of Employees Increasing Pension Contributions', min_value=0, max_value=100, value=50, step=1)
    new_contribution_amount = st.slider('New Personal Pension Contribution (%)', min_value=5, max_value=100, value=10, step=1)
    mu = st.slider('Standard Deviation of Salary Values', min_value=0.0, max_value=1.0, value=0.1)
    
    salary_distribution = Calculate.get_salary_distribution(average_salary, mu, int(n_employees))
    
    company_savings = Calculate.calculate_company_savings(salary_distribution, percent_employees_increase_contribution, new_contribution_amount/100)
    st.write(f'## **The company :green[saves £{company_savings:,.2f}] per year by offering the proposed pension scheme.**')

    fig = px.histogram(salary_distribution, nbins=20, title='Salary Distribution')
    fig.update_xaxes(title_text='Annual Salary (£)')
    fig.update_yaxes(title_text='Number of Employees')
    st.plotly_chart(fig, use_container_width=True)
    
    

if __name__ == "__main__":
    main()