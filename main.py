import os

import pandas as pd

from collections import defaultdict
from dotenv import load_dotenv
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape

from http.server import HTTPServer, SimpleHTTPRequestHandler



def get_year_of_founder():
    date_now = datetime.now()
    founder_year = (date_now.year - 1920)

    if founder_year == 100:
        text_year = "лет"
        return founder_year, text_year
    elif founder_year == 101:
        text_year = "год"
        return founder_year, text_year
    elif 101 < founder_year <= 104:
        text_year = "годa"
        return founder_year, text_year
    elif founder_year > 104:
        text_year = "лет"
        return founder_year, text_year


def give_data_for_site_fill(path_to_file):
    wine_table = pd.read_excel(path_to_file, sheet_name='Лист1',
                               na_values='nan', keep_default_na=False)
    wines = wine_table.to_dict(orient="records")
    final_form = defaultdict(list)

    for wine in wines:
        category = wine.get("Категория")
        final_form[category].append(wine)
    return final_form


def main():
    load_dotenv()
    path_to_file = os.getenv("PATH_TO_FILE")

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    founder_year, text_year = get_year_of_founder()

    final_form_of_wines = give_data_for_site_fill(path_to_file)

    rendered_page = template.render(
        founder_date=f"Уже {founder_year} {text_year} с вами",
        categories=final_form_of_wines.keys(),
        wines=final_form_of_wines
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
