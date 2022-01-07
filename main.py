import requests
from bs4 import BeautifulSoup
import mysql.connector

letters = ['a', 'b', 'c', 'ç', 'd', 'e', 'ə', 'f', 'g', 'h', 'x', 'i', 'j', 'k', 'q',   'l', 'm', 'n', 'o', 'ö', 'p', 'r', 's', 'ş', 't', 'u', 'ü', 'v', 'y', 'z']

# 25593
# mysql connection®
cnx = mysql.connector.connect(user='root', database='aze_dictonary', password='secret123')
cursor = cnx.cursor()
total_inserted_counts = 0
for letter in letters:

    i, flag = 1, True

    while flag:
        url = f"https://obastan.com/azerbaycan-dilinin-izahli-lugeti/{letter}/?l=az&p={i}"

        result = []

        response = requests.get(url)
        soup = BeautifulSoup(response.text, features="html.parser")
        words = soup.find_all("li", {'class': 'wli'})

        for word in words:
            title = word.find("h3", {'class': 'wli-title'}).text
            description = word.find("p", {'class': 'wli-description'}).text

            if title.isalnum() is False:
                title = ''.join(e for e in title if e.isalnum())

            if title[0].lower() != letter:
                flag = False
                break

            result.append(
                {
                    "title": title,
                    "description": description,
                }
            )

        if len(result) == 0:
            break

        for item in result:
            cursor.execute("INSERT INTO words(text, description) VALUES (%s, %s)", (item["title"], item["description"]))

        cnx.commit()
        total_inserted_counts += len(result)
        print(f"{total_inserted_counts} rows inserted..")

        i += 1

        if flag is False:
            break

print("finished")
