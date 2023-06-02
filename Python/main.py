import requests
from bs4 import BeautifulSoup
import mysql.connector as mysql
import os
from dotenv import load_dotenv

'''load_dotenv()
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']    
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']'''

db = mysql.connect(host="sql9.freesqldatabase.com",
                   user="sql9622826",
                   password="hQNVN4TgY4",
                   database="sql9622826")

cursor = db.cursor()

url = "http://192.168.188.175/"  # http://192.168.1.212/   http://192.168.188.251/

try:
    # cursor.execute("""TRUNCATE TABLE device1""")
    while True:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        # print(soup.prettify())

        data = []
        for p in soup.find_all("p"):
            data.append(float(p.text))

        print(data)

        # time.sleep(0.02)

        # query = "INSERT INTO sensorData (temperature, moisture, humidity, sunlight) VALUES " \
        #         "({}, {}, {}, {}, {}, {}, {})".format(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
        # print(query)
        #
        # cursor.execute(query)
        # db.commit()

except:
    pass
finally:
    cursor.close()
    db.close()
    print('close')
