import requests
from bs4 import BeautifulSoup
import json
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://www.kfc.com.uz'
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
}

print('Парсинг начался.')

# pages folder for html pages
if not os.path.exists('pages'):
    os.makedirs('pages')

# --------------------------------------------------------------
# creating index.html
if not os.path.exists('pages/index.html'):
    request = requests.get(url + '/ru/main', headers=headers, verify=False)
    src = request.text

    with open('pages/index.html', mode='w', encoding='utf-8') as file:
        file.write(src)

# html file for parsing
# --------------------------------------------------------------
with open("pages/index.html", encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")

# --------------------------------------------------------------
# category dict
all_categories = soup.find('ul', class_='sub-nav').find_all('li')
rep = [",", " ", "-", "'"]
categories_dict = {}

# --------------------------------------------------------------
# Iteration
iteration_count = int(len(all_categories))
count = 1
print(f"Всего итераций по категориям: {iteration_count}")
# --------------------------------------------------------------
for category in all_categories:

    title = category.get_text(strip=True)
    for item in rep:
        if item in title:
            title = title.replace(item, "_")
    href = category.find('a').get('href')
    categories_dict[title] = url + href

if not os.path.exists('json'):
    os.makedirs('json')

# creating category json
with open("json/categories.json", mode="w", encoding='utf-8') as file:
    json.dump(categories_dict, file, indent=4, ensure_ascii=False)

# --------------------------------------------------------------
# getting json data [Category]
with open("json/categories.json", encoding='utf-8') as file:
    all_categories = json.load(file)

# --------------------------------------------------------------
if not os.path.exists(f'pages/categories'):
    os.makedirs(f'pages/categories')
    all_products = []
    # --------------------------------------------------------------
    # creating html page for category_detail
    for category_name, category_href in all_categories.items():
        request = requests.get(url=category_href, headers=headers, verify=False)
        src = request.text

        # -------------------------------------------------------------
        with open(f'pages/categories/{category_name}.html', mode='w', encoding='utf-8') as file:
            file.write(src)

        soup = BeautifulSoup(src, "lxml")
        products = soup.find('ul', class_='products-detail-list').find_all('li')

        if not os.path.exists(f'pages/categories/{category_name}'):
            os.makedirs(f'pages/categories/{category_name}')

            products_lst = []
            for product in products:
                title = product.find('h4').get_text(strip=True)
                href = url + product.find('a').get('href')
                for item in rep:
                    if item in title:
                        title = title.replace(item, "_")

                request = requests.get(href, headers=headers, verify=False)
                src = request.text

                # --------------------------------------------------------------
                # # creating html page for product detail
                with open(f"pages/categories/{category_name}/{title}.html", mode='w', encoding='utf-8') as file:
                    file.write(src)

                # --------------------------------------------------------------
                # product detail parsing
                soup = BeautifulSoup(src, "lxml")
                product_data = soup.find('div', class_='product-info-wrp')
                title = product_data.find('h3').get_text(strip=True)
                description = product_data.find('div').get_text(strip=True)
                price = product_data.find('h3', class_='price').get_text(strip=True)[:-3]
                image = soup.find('div', class_='product-photo-wrp').find('img').get('src')
                products_lst.append({
                    'title': title,
                    'description': description,
                    'price': price,
                    'image': image}
                )
                all_products.append({
                    'title': title,
                    'description': description,
                    'price': price,
                    'image': image}
                )

            # --------------------------------------------------------------
            # category products json
            if not os.path.exists(f'json/{category_name}'):
                os.makedirs(f'json/{category_name}')
            with open(f"json/{category_name}/{category_name}.json", mode="w", encoding='utf-8') as file:
                json.dump(products_lst, file, indent=4, ensure_ascii=False)

        print(f'Итерация - {count}...')
        count += 1
    print('Парсинг прошел успешно!')

    with open(f"json/products.json", mode="w", encoding='utf-8') as file:
        json.dump(all_products, file, indent=4, ensure_ascii=False)
