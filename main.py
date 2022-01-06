import requests
from bs4 import BeautifulSoup
import mysql.connector

# letters
letters = ['a', 'b', 'c', 'ç', 'd', 'e', 'ə', 'f', 'g', 'h', 'x', 'i', 'j', 'k', 'q', 'l', 'm', 'n', 'o', 'ö', 'p', 'r', 's', 'ş', 't', 'u', 'ü', 'v', 'y', 'z']

# mysql connection
cnx = mysql.connector.connect(user='root', database='aze_dictonary', password='secret123')
cursor = cnx.cursor()

for letter in letters:

    i, flag = 1, True

    while flag:
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

        i += 1

