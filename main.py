import os
import pandas as pd
from collections import defaultdict
from dotenv import load_dotenv
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape

load_dotenv()

path_to_file = os.getenv("PATH_TO_FILE")


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

date_now = datetime.now()
founder_year = (date_now.year - 1920)

if founder_year == 100:
    text_year = "лет"
elif founder_year == 101:
    text_year = "год"
elif 101 < founder_year <= 104:
    text_year = "годa"
elif founder_year > 104:
    text_year = "лет"


wine_table = pd.read_excel(path_to_file, sheet_name='Лист1',
                           na_values='nan', keep_default_na=False)

wines = wine_table.to_dict(orient="records")
final_form_of_wines = defaultdict(list)

for wine in wines:
    category = wine.get("Категория")
    final_form_of_wines[category].append(wine)

rendered_page = template.render(
    founder_date=f"Уже {founder_year} {text_year} с вами",
    categories=final_form_of_wines.keys(),
    wines=final_form_of_wines
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
# server.serve_forever()
