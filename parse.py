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
global_has_stock = False

smtp_server = config['DEFAULT']['SMTP_Server']
msg = EmailMessage()
msg['Subject'] = config['DEFAULT']['Subject']
msg['From'] = config['DEFAULT']['From']
msg['To'] = config['DEFAULT']['To']

msg_text = ''


for phone, phone_url in phones.items():
    fp = urllib.request.urlopen(phone_url)
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
