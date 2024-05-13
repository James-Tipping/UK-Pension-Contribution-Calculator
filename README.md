# UK salary sacrifice pension contribution calculator

When utilising a salary sacrifice scheme, employers and employees typically both contribute towards an employee's pension. However, an employee
contributing under said scheme reduces their taxable salary. Given that income tax, and both employee and employer national insurance (NI) 
contributions are based on the taxable salary, increasing employee/personal pension contributions can be a tax efficient way of increasing effective overall renumeration. Increasing employee pension contributions decreases taxes paid by both parties.

![Pension Calculator](Screenshot-1.png)

## Aim of this calculator

The calculator calculates:

- Annual income tax
- Annual NI payments for employee and employer
- Salary after pension, income tax, and NI (take home salary)
- Total pension contributions

However, this calculator also aims to explain an innovative scheme that can be used to **encourage** larger employee pension contributions.
When employee pension contributions are increased, the employer pays less NI. Encouraging employees to increase their contributions increases their 
effective overall renumeration, and decreases employer costs. Therefore, this UI breaks down how giving **50%** of the employer NI savings to
the employee in the form of additional pension contributions can benefit both employee and employer.

A breakdown of the savings for the employer and employee are calculated in a table, based on the new pension contribution.

![Pension Savings Breakdown](Screenshot-2.png)

Finally, variables can be altered to show how much money a company could save by using such a scheme, assuming the scheme indeed encourages
employees to increase contributions. The variables to be altered are:

- Average salary (of employees at relevant company)
- Number of employees
- Percentage of employees increasing contributions
- New personal pension contributions as a percentage of gross salary
- Standard deviation of salary values in the underlying log-normal distribution.

The company saving based on all variables selected is calculated, along with a graph showing the estimated distribution of salaries at the company.

![Company Savings 1](Screenshot-3.png)
![Company Savings 2](Screenshot-4.png)

## How to install & use

As this program with written in a Conda Python environment, no such 'requirements.txt' (common to Pip environments) can be given. However, an 
'environment.yml' file has been generated to aid reproducibility. A Conda environment can be created and used by running the following command
in your terminal (assuming you have Conda installed and accessible through your shell of choice):

```bash
conda env create -f environment.yml
```

## Disclaimer

The data and opinions presented in this calculator are for illustrative purposes only, and should not be taken as financial advice.
I am not a financial advisor, and the information presented may not be accurate or up-to-date. 
Please consult a suitably qualified financial advisor before making any financial decisions.