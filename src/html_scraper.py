from bs4 import BeautifulSoup
import pandas as pd

def get_html(file_name):
    html_file = open(file_name, 'r')
    index = html_file.read()
    soup = BeautifulSoup(index, 'html.parser')
    return soup

def get_tables(soup):
    tables = soup.find_all("table", {"class": "spreadsheet"})
    tables_soup = BeautifulSoup(str(tables), 'html.parser')
    return tables_soup

def get_headers_list(tables_soup):
    headers_rset = tables_soup.find('tr', {"class": "columnTitles"})

    headers_list = []
    for h in headers_rset:
        if h.text == '\n':
            continue
        headers_list.append(h.text)
    
    return headers_list

def validate_field(field):
    if field.text == '\u00a0':
        return ""
    return field.text

def get_rows_list(tables_soup):
    rows_rset = tables_soup.find_all('tr', {"class": None})
    
    rows_list = []
    for row in rows_rset:
        fields_list = []
        for field in row:
            if field.text == '\n':
                continue
            fields_list.append(validate_field(field))
        rows_list.append(fields_list)

    return rows_list

def scrape(file_directory):
    soup = get_html(file_directory)
    tables_soup = get_tables(soup)

    headers_list = get_headers_list(tables_soup)
    rows_list = get_rows_list(tables_soup)

    df = pd.DataFrame(data=rows_list, columns=headers_list)
    return df