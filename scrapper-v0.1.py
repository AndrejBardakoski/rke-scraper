import requests
from bs4 import BeautifulSoup

url = 'https://www.erc.org.mk/ceni.aspx'
header = {"Content-Type": "application/x-www-form-urlencoded"}
pages = {"elekrricna_energija": "e=2",
         "priroden_gas": "e=4",
         "toplinska_energija": "e=3",
         "nafta": "e=1",
         "obnovlivi_izvori": "e=5"}

data = []

for category, code in pages.items():
    req = requests.post(url, data=code, headers=header)
    parsed_html = BeautifulSoup(req.text)
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

print(data)
