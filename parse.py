import urllib.request
import json
import re

phones = dict()

phones["iphone13"] = 'https://shop.theclub.com.hk/iphone-13.html'
phones["iphone13pro"] = 'https://shop.theclub.com.hk/iphone-13-pro.html'
phones["iphone13promax"] = 'https://shop.theclub.com.hk/iphone13-promax.html'


for phone, phone_url in phones.items():
    fp = urllib.request.urlopen(phone_url)
    mybytes = fp.read()
    html = mybytes.decode("utf8")
    fp.close()

    JSON = re.compile('\"\#product_addtocart_form\"\:\s+({.*?}),\s+\"\*\"', flags=re.DOTALL | re.MULTILINE)
    matches = JSON.search(html)
    inventory = json.loads(matches.group(1))

    salable=inventory["configurable"]["spConfig"]["isSalableOptions"]
    has_stock = False
    for key,values in  salable.items():
        if values["is_salable"]:
            has_stock = True

    print(phone + ": ", has_stock)