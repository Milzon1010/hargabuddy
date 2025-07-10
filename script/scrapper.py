# scrapper.py

import requests
import pandas as pd

def scrape_tokopedia_graphql(keyword: str, start_page: int = 1, end_page: int = 1, min_price: int = 0, max_price: int = 999999999) -> pd.DataFrame:
    """
    Scrape produk Tokopedia dengan filter harga dan multi-page.
    """
    url = "https://gql.tokopedia.com/graphql/SearchProductV5Query"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Origin": "https://www.tokopedia.com",
        "Referer": "https://www.tokopedia.com/"
    }

    all_products = []

    for page in range(start_page, end_page + 1):
        query_string = (
            f"device=desktop&enter_method=normal_search&l_name=sre&navsource=&ob=23"
            f"&page={page}&q={keyword}&related=true&rows=60&safe_search=false"
            f"&sc=&scheme=https&shipping=&show_adult=false&source=search&st=product&start=0"
        )

        payload = [{
            "operationName": "SearchProductV5Query",
            "variables": {
                "params": query_string
            },
            "query": "query SearchProductV5Query($params: String!) { searchProductV5(params: $params) { data { products { name url price { text number } shop { name city } rating }}}}"
        }]

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            continue

        try:
            response_data = response.json()
            if isinstance(response_data, list):
                response_data = response_data[0]

            products = response_data['data']['searchProductV5']['data']['products']

            for p in products:
                price = p['price']['number']
                if min_price <= price <= max_price:
                    all_products.append({
                        'Nama Produk': p['name'],
                        'Harga': p['price']['text'],
                        'Harga Numeric': price,
                        'Toko': p['shop']['name'],
                        'Kota': p['shop']['city'],
                        'Rating': p.get('rating', 'N/A'),
                        'Link': p['url']
                    })
        except Exception as e:
            print("❌ Error:", e)
            continue

    return pd.DataFrame(all_products)
