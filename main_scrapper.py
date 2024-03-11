import requests
from bs4 import BeautifulSoup
import firebase_connection as fc

if __name__ == '__main__':

    firebase = fc.FirebaseConnection()

    url = 'https://www.erc.org.mk/ceni.aspx'
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    pages = {"electricity": "e=2",
             "natural_gas": "e=4",
             "district_heating": "e=3",
             "oil_and_oil_derivatives": "e=1",
             "renewable_sources": "e=5"}

    data = []

    for category, code in pages.items():
        req = requests.post(url, data=code, headers=header)
        parsed_html = BeautifulSoup(req.text, features="html.parser")
        rows = parsed_html.find_all('tr')
        rows = rows[1:]  # remove header row

        for row in rows:
            tds = row.find_all('td')
            obj = {}
            obj["category"] = category
            obj['name'] = tds[0].text
            price_str = tds[1].text
            price_str = price_str.replace(',', '.')  # 12,4 -> 12.4
            obj['price'] = float(price_str)
            obj['unit'] = tds[2].text
            obj['valid_from'] = tds[3].text
            data.append(obj)
            firebase.push_data(category, tds[0].text, obj)
            firebase.push_agg_data(tds[0].text, obj)
