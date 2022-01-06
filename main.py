import requests
from bs4 import BeautifulSoup
import mysql.connector

# mysql connection
cnx = mysql.connector.connect(user='root', database='aze_dictonary', password='secret123')
cursor = cnx.cursor()


for i in range(40, 50):
    url = f"https://obastan.com/azerbaycan-dilinin-izahli-lugeti/a/?l=az&p={i}"

    result = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    words = soup.find_all("li", {'class': 'wli'})


    for word in words:
        title = word.find("h3", {'class': 'wli-title'})
        description = word.find("p", {'class': 'wli-description'})
        result.append(
            {
                "title": title.text,
                "description": description.text,
            }
        )

    for item in result:
        cursor.execute("INSERT INTO words(text, description) VALUES (%s, %s)", (item["title"], item["description"]))

    cnx.commit()
    print(f"{len(result)} rows inserted..")
# query = "SELECT * FROM words"
#
# cursor.execute(query)
#
# print(cursor.fetchall())

#
# cursor.close()
# cnx.close()


