import os
from datetime import datetime

import pandas as pd
from collections import defaultdict
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape

from http.server import HTTPServer, SimpleHTTPRequestHandler


def get_year_of_founder():
    date_now = datetime.now()
    year_of_founder = 1920
    number_of_years = (date_now.year - year_of_founder)

    if number_of_years == 100:
        text_year = "лет"
        return number_of_years, text_year
    elif number_of_years == 101:
        text_year = "год"
        return number_of_years, text_year
    elif 101 < number_of_years <= 104:
        text_year = "годa"
        return number_of_years, text_year
    elif number_of_years > 104:
        text_year = "лет"
        return number_of_years, text_year


def get_data_from_excel_table(path_to_file):
    wine_table = pd.read_excel(path_to_file, sheet_name='Лист1',
                               na_values='nan', keep_default_na=False)
    wines = wine_table.to_dict(orient="records")
    data_from_excel = defaultdict(list)

    for wine in wines:
        category = wine.get("Категория")
        data_from_excel[category].append(wine)
    return data_from_excel


def main():
    load_dotenv()
    path_to_file = os.getenv("PATH_TO_FILE")

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    founder_year, text_year = get_year_of_founder()

    table_with_wines = get_data_from_excel_table(path_to_file)

    rendered_page = template.render(
        string_with_year=f"Уже {founder_year} {text_year} с вами",
        wines=table_with_wines
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
