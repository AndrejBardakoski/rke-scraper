import requests
from bs4 import BeautifulSoup
import firebase_connection as fc

if __name__ == '__main__':

    # ===INIT FIREBASE===
    firebase = fc.FirebaseConnectionService()

    # ===CONFIG===
    url = 'https://www.erc.org.mk/ceni.aspx'
    header = {"Content-Type": "application/x-www-form-urlencoded",
              "User-Agent": "Defined"}
    pages = {"electricity": "e=2",
             "natural_gas": "e=4",
             "district_heating": "e=3",
             "oil_and_oil_derivatives": "e=1",
             "renewable_sources": "e=5"}
    data = []

    # Only exists to convert the badly formated warehouse collection to timeline collection, run once xd
    # firebase.read_warehouse_data()

    # ===LOOP THROUGH CATEGORIES===
    for category, code in pages.items():
        # break
        # ===SCRAPE DATA===
        req = requests.post(url, data=code, headers=header)
        parsed_html = BeautifulSoup(req.text, features="html.parser")
        rows = parsed_html.find_all('tr')
        rows = rows[1:]

        # ===PARSE DATA===
        for row in rows:
            tds = row.find_all('td')

            price_str = tds[1].text.replace(',', '.')  # 12,4 -> 12.4

            obj = {"category": category,
                   'name': tds[0].text,
                   'price': float(price_str),
                   'unit': tds[2].text,
                   'valid_from': tds[3].text}

            timelineObj = {"category": category,
                           'name': tds[0].text,
                           'unit': tds[2].text,
                           'timeline': {
                               f"{tds[3].text}": float(price_str),
                           }}

            # ===PUSH DATA TO FIREBASE===
            data.append(obj)
            firebase.push_data(category, tds[0].text, obj)
            firebase.push_timeline_data(tds[0].text, timelineObj)
