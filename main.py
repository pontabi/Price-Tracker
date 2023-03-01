from google_sheet import GoogleSheet
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

FROM_ADDR = "Your gmail address sending email from"
FROM_PASS = "Your Password for FROM_ADDR"
TO_ADDR = "Your gmail address sending email to"


def send_msg(name, price):
    message = MIMEMultipart()
    message['From'] = FROM_ADDR
    message['To'] = TO_ADDR
    message['Subject'] = 'Price Tracker'
    mail_content = f'''
Your registered product priced down to the target price.
----------------------
{name}

{price}¥

{target_url}
----------------------
'''
    message.attach(MIMEText(mail_content, 'plain'))

    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(FROM_ADDR, FROM_PASS)
    text = message.as_string()
    session.sendmail(FROM_ADDR, TO_ADDR, text)
    session.quit()


gs = GoogleSheet()
for item in gs.records:
    target_url = item["link"]
    target_price = int(item["target_price"])
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Accept-Language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7,es-ES;q=0.6,es;q=0.5"
    }

    # --------- Scraping websites and fetch current price --------- #
    res = requests.get(target_url, headers=header)
    soup = BeautifulSoup(res.text, "html.parser")
    price_el = soup.find(name="span", class_="a-price-whole")
    cur_price = int(price_el.getText().replace(",", ""))
    product_name = soup.find(name="span", id="productTitle").getText()

    # --------- If price is low enough, send email --------- #
    if cur_price <= target_price:
        send_msg(name=product_name, price=cur_price)
        print("Mail Sent")
    else:
        print("Current price is higher than the target, mail was not sent.")



