from typing import NamedTuple, TYPE_CHECKING
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import sqlite3
import datetime
import time

# compitition=[]
equipA = []
equipB = []
scA = []
scB = []
temps = []

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://www.espn.com/soccer/scoreboard")

# create connection
conn = sqlite3.connect('test.db')
c = conn.cursor()
# c.execute("drop table soccer")
c.execute('''CREATE TABLE soccer(equipeA TEXT, resultatA INT, equipeB TEXT, resultatB INT,GameTime TEXT, GameDate DATE)''')

html = driver.page_source
soup = BeautifulSoup(html, "lxml")
equipeA = soup.find_all("div", {"class": "team-a"})
equipeB = soup.find_all("div", {"class": "team-b"})
status = soup.find_all("div", {"class": "game-status"})


def find_equipesA():
    #print("equipe A")
    for eqA in equipeA:
        eA = eqA.find_all("span", {"class": "short-name"})
        for e in eA:
            # print(e.text)
            equipA.extend([e.text])
    # print(equipA)


def find_equipesB():
    #print("equipe B")
    for eqB in equipeB:
        eB = eqB.find_all("span", {"class": "short-name"})
        for e in eB:
            # print(e.text)
            equipB.extend([e.text])
    # print(equipB)


def findResultat():
    #print("Les score d'équipe A")
    for resA in equipeA:
        rA = resA.find_all("span", {"class": "score"})
        for r in rA:
            # print(r.text)
            scA.extend([r.text])
    # print(scA)

    # print("--\n")
    #print("Les score d'équipe B")
    for resB in equipeB:
        rB = resB.find_all("span", {"class": "score"})
        for r in rB:
            # print(r.text)
            scB.extend([r.text])
    # print(scB)


def findGameTime():
    #print(" Time Game")
    for stat in status:
        st = stat.find_all("span", {"class": "game-time"})
        for t in st:
            # print(time.text)
            temps.extend([t.text])
    # print(temps)

# def findNomCompetition():
    #print("nom de compétition")
    #comp = soup.find_all("a", {"class": "date-heading js-show"})
    # for c in comp:
        #a = c.text
        # compitition.extend([a])
    # print(compitition)


now = datetime.datetime.now()
# ajout=1


def ajouter():
    for i in range(len(temps)):
        c.execute('''INSERT INTO soccer VALUES(?,?,?,?,?,?)''',
                  (equipA[i], scA[i], equipB[i], scB[i], temps[i], now.strftime(" %d/%m/%Y ")))
        # return ajout + 1
        # ajout + 1)
# print(ajout)


def modifier():
    for i in range(len(temps)):
        c.execute("""UPDATE soccer SET resultatA = ?, resultatB = ?, GameTime = ?  WHERE GameDate = ?""",
                  (scA[i], scB[i], temps[i], now.strftime(" %d/%m/%Y ")))
# def delete():
    #c.execute('''DELETE FROM soccer''')

# run funtion and commit changes to DB
# find_equipesA()
# find_equipesB()
# findResultat()
# findGameTime()
# findNomCompetition()
# print(len(equipA))
# print(len(equipB))
# print(len(scA))
# print(len(scB))
# # print(len(compitition))
# print(len(temps))
# # print(len(date))
# ajouter()


if __name__ == '_main_':
    while True:
        find_equipesA()
        find_equipesB()
        findResultat()
        findGameTime()
        c.execute('''SELECT GameDate FROM soccer WHERE GameDate = ?''',
                  (now.strftime(" %d/%m/%Y "),))
        results = c.fetchall()
        # print(results)
        if len(results) == 0:
            ajouter()
        else:
            modifier()
        conn.commit()
        # select all from table
        print("toute la base")
        c.execute('''SELECT * FROM soccer''')
        results = c.fetchall()
        print(results)
        time_wait = 1
        print(f"Waiting {time_wait} minutes..")
        time.sleep(time_wait*60)
        # delete()

# close connection
conn.close()
driver.quit()
