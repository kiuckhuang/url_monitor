#!/usr/bin/python3

import configparser
import urllib.request
import json
import re
# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.message import EmailMessage

config = configparser.ConfigParser()
config.read('config.ini')

phones = {
    "iphone13": 'https://shop.theclub.com.hk/iphone-13.html',
    "iphone13pro": 'https://shop.theclub.com.hk/iphone-13-pro.html',
    "iphone13promax": 'https://shop.theclub.com.hk/iphone13-promax.html'
}

http_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4644.0 Safari/537.36 Edg/96.0.1028.0'
}

global_has_stock = False

smtp_server = config['DEFAULT']['SMTP_Server']
msg = EmailMessage()
msg['Subject'] = config['DEFAULT']['Subject']
msg['From'] = config['DEFAULT']['From']
msg['To'] = config['DEFAULT']['To']

msg_text = ''


for phone, phone_url in phones.items():
    rq = urllib.request.Request(phone_url, headers=http_headers, method='GET')
    fp = urllib.request.urlopen(rq)
    mybytes = fp.read()
    html = mybytes.decode("utf8")
    fp.close()

    JSON = re.compile(
        '\"\#product_addtocart_form\"\:\s+({.*?}),\s+\"\*\"', flags=re.DOTALL | re.MULTILINE)
    matches = JSON.search(html)
    inventory = json.loads(matches.group(1))

    salable = inventory["configurable"]["spConfig"]["isSalableOptions"]

    model_has_stock = False
    for key, values in salable.items():
        if values["is_salable"]:
            global_has_stock = True
            model_has_stock = True

    msg_text += phone + ", " + phone_url + " ," + str(model_has_stock) + '\n'

if global_has_stock:
    msg.set_content(msg_text)
    s = smtplib.SMTP(smtp_server)
    s.send_message(msg)
    s.quit()
