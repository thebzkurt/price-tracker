import smtplib
from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv

load_dotenv()

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

Url = "https://www.amazon.com.tr/COSORI-frit%C3%B6z%C3%BC-dokunmatik-programl%C4%B1-%C3%A7alkalama/dp/B07N8N6C85/ref=sr_1_2?_encoding=UTF8&content-id=amzn1.sym.2fe73be5-6685-405c-aef1-14470eaedee0&dib=eyJ2IjoiMSJ9.CkTvyIKi9_8eMyafLlZNAHcqB3B3BL57d2kg2LnhE0yy_YCCz1hP4JLHj3zNrqdVrQDSLfWXIpfiAwOVa5QEf5fwqEGCV4r9__XFbYFLfVF_Q-xETgzpVpmWtN-03Emg7y04Kx3kR9uFeZDUqoXeBr-EvC42T2J_Y5sQPCV3TBUmBnnq-EJxVXFxtjO-N_sqdDD8YG4ZWGBA2B9b5ZmbmbxL0w6ShnHS6qVScL82wpgRydvoVKFe92WBfPzv8h8bkWkOZKdbTXMR4nlC0kSZF7aQQYy-GUvDB03kdHtToLc.HJPK1z4XY6L2YQt7grgkYcFO65KB0E0KfHhWe9UZLTg&dib_tag=se&pd_rd_r=29cf5c21-6b56-4808-93a2-7ebc6b56ed64&pd_rd_w=XVeSN&pd_rd_wg=ryLQx&pf_rd_p=2fe73be5-6685-405c-aef1-14470eaedee0&pf_rd_r=6P3Q7YBFJKQXBF6Q38AD&qid=1733155309&refinements=p_n_deal_type%3A26902947031&s=kitchen&sr=1-2&th=1"

response = requests.get(Url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    price_elemant = soup.find(class_="a-offscreen")
    if price_elemant:
        price = price_elemant.get_text()
        price_without_currency = price.replace("TL","").replace(",",'').strip()
        price_as_float = float(price_without_currency)
        print(f"Urun fiyatu {price_as_float} TL")

# -------------------------------------------------- email yolama -------------------------------------------------- #
        title = soup.find(id="productTitle").get_text().strip()
        print(title)

        BUY_PRICE = 3000

        if price_as_float < BUY_PRICE:
            messages = f"{title} is on sale for {price}!"

            with smtplib.SMTP(os.environ["SMTP_ADDRESS"], 587) as connection:
                connection.starttls()
                result = connection.login(os.environ["EMAIL_ADDRESS"],os.environ["EMAIL_PASSWORD"])
                msg=f"Subject:Amazon Price Alert!\n\n{messages}\n{Url}".encode("utf-8")
    else:
        print("Fiyat bilgisi bulunamadi")
else:
    print(f"İstek başarısız oldu. Durum kodu: {response.status_code}")


