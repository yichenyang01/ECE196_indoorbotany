import requests
from bs4 import BeautifulSoup
import mysql.connector as mysql
import time
import os
from dotenv import load_dotenv

'''load_dotenv()
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']    
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']'''

db = mysql.connect(host="sql9.freesqldatabase.com",
                   user="sql9624220",
                   password="2J5k7RIybG",
                   database="sql9624220")

cursor = db.cursor()
print('DB connected')
url = "http://192.168.207.7/"  # http://192.168.1.212/   http://192.168.188.251/

try:
    # cursor.execute("""TRUNCATE TABLE device1""")
    while True:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        # print(soup.prettify())
        print('Done scraping')
        data = []
        for p in soup.find_all("p"):
            text = p.text
            if text[0] == 'H' or text[0] == 'S' or text[0] == 'M':
                data.append(p.text[11:])
            else:
                data.append(p.text[14:])

        # print(data)
        data2 = [int(x) for x in data]
        print(data2)
        query = "INSERT INTO plant_data (moisture, temp, humidity, light, profile_id) VALUES " \
                "({}, {}, {}, {}, {})".format(data2[3], data2[1], data2[0], data2[2], 1)
        print(query)

        cursor.execute(query)
        db.commit()

        time.sleep(5)

except:
    pass
finally:
    cursor.close()
    db.close()
    print('closed all')
