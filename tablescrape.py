"""
Template creating pandas DataFrame objects from an URL which contains a table.
This template ignores tables which have cells spanning between 2 and 10
columns.
"""
import sys
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame


def get_tables_url(url):
    content = requests.get(url).text
    soup = BeautifulSoup(content, 'lxml')

    tables = soup.find_all('table')

    for table_content in tables:
        table_to_dataframe(table_content)


def table_to_dataframe(tb):
    # If there are cells spanning between 2 and 10 rows and columns, ignore the
    # table.
    for i in range(2, 11):
        if tb.find_all('th', attrs={'rowspan': i}) != []:
            return
        if tb.find_all('td', attrs={'colspan': i}) != []:
            return

    # Process the table headers
    headers = tb.find_all('th')
    headers_rows = tb.find_all('th', attrs={'scope': 'row'})
    headers_cols = []

    # Ignore the row headers
    for i in range(len(headers)):
        if headers[i] not in headers_rows:
            headers_cols.append(headers[i].text.replace('\n', ''))

    nb_cols = len(headers_cols)

    # Process the content of the table
    cells = tb.find_all('td')
    output_data = []
    a = []

    # Remove the first column in case there is a header on the first column
    if nb_cols > 0:
        if (len(cells) % nb_cols) != 0:
            headers_cols = headers_cols[1:]
            nb_cols = len(headers_cols)

    # Remove return character from cells
    for i in range(len(cells)):
        a.append(cells[i].text.replace('\n', ''))

        if len(a) == nb_cols:
            output_data.append(a)
            a = []

    # Create the pandas DataFrame object
    df = DataFrame(output_data)

    if not df.empty:
        print(df)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        url = 'https://en.wikipedia.org/wiki/List_of_largest_companies' \
            '_by_revenue'
    else:
        print(sys.argv)
        url = sys.argv[1]

    get_tables_url(url)
