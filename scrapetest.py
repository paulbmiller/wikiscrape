"""
Just a small script which reads the table from the Wikipedia page List of 
Largest Companies to calculate the ratio of revenue to employees and create
a Pandas DataFrame.
"""

import requests
from bs4 import BeautifulSoup
from pandas import DataFrame

url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue'

content = requests.get(url).text
soup = BeautifulSoup(content, 'lxml')

tb = soup.find('table')

cells = tb.find_all('td')

nb_cols = 6

companies = []
revenues = []
employees = []
ratios = []

# Add only company names, revenue and nb of employees to lists
for i in range(50):
    for j in range(nb_cols):
        if j == 0:
            companies.append(cells[i*(nb_cols+1)+j].text)
        if j == 2:
            revenues.append(cells[i*(nb_cols+1)+j].text)
        if j == 4:
            employees.append(cells[i*(nb_cols+1)+j].text)
    
# Remove unnecessary return, comma and $ characters and convert numbers
for i in range(len(companies)):
    companies[i] = companies[i].replace('\n', '')
    revenues[i] = revenues[i].replace('\n', '')   
    employees[i] = employees[i].replace('\n', '')
    
    revenues[i] = revenues[i].replace(',', '')
    revenues[i] = revenues[i].replace('$', '')
    
    employees[i] = employees[i].replace(',', '')
    
    revenues[i] = int(revenues[i]) * 1e6
    
    employees[i] = int(employees[i])
    
for i in range(len(companies)):
    ratios.append(revenues[i] / employees[i])
    
cols = ['Companies', 'Revenue', 'Employees', 'Ratio']

data = {
        cols[0]: companies,
        cols[1]: revenues,
        cols[2]: employees,
        cols[3]: ratios
        }

df = DataFrame(data, columns = cols)

df.sort_values(by='Ratio', ascending=0, inplace = True)

print(df)
