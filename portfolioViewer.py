#!/usr/bin/python

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import json
import urllib.request
import sys


def cryptoAPI(crypto):

    # This is necessary so that the website doesn't know we are a bot and kick us out
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }

    URL = f"https://api.nomics.com/v1/currencies/ticker?key=6fea7ebf09a2867eafc389b4f19b33cbb60c2efd&convert=CAD&ids={crypto}"

    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    return eval(str(soup)[1:-2])


def myPortfolio(portfolio):

    id = ""

    for i in range(0, 9):
        id += portfolio[1][i]
        if (i != 8):
            id += ","

    jsonData = cryptoAPI(id)

    print("\n\n\n\n")

    #                                        --35             --57                                 --95
    print("----------------------------------- Portfolio Data --------------------------------------")
    print("Name                      Price           *           Owned            =            Total")
    print("----                      -----                       -----                         -----")

    total = 0
    day = 0
    week = 0
    month = 0
    year = 0

    for i in jsonData:

        index = 0
        owned = 0

        for j in range(0, 9):
            if i["id"] == portfolio[1][j]:
                index = j

        owned = portfolio[0][index] * float(i["price"])
        total += owned

        day += portfolio[0][index] * float(i["1d"]["price_change"])
        week += portfolio[0][index] * float(i["7d"]["price_change"])
        month += portfolio[0][index] * float(i["30d"]["price_change"])
        year += portfolio[0][index] * float(i["365d"]["price_change"])

        print(f'{i["name"]+":":23} {i["price"]:28} {str(portfolio[0][index]):29} ${owned:.2f}')

    print("\n\n")

    print(f"Total: ${total:.2f}")

    print("\n\n")

    print("------------------------------------- Historical ----------------------------------------")
    print("TimeFrame                 Change                      Percent                            ")
    print("---------                 ------                      -------                            ")

    print(f"1d:                       {str(round(day, 2)):27} {str(round(day/total * 100, 2))+'%':10}")
    print(f"7d:                       {str(round(week, 2)):27} {str(round(week/total * 100, 2))+'%':10}")
    print(f"30d:                      {str(round(month, 2)):27} {str(round(month/total * 100, 2))+'%':10}")
    print(f"365d:                     {str(round(year, 2)):27} {str(round(year/total * 100, 2))+'%':10}")


    print("\n\n\n\n")

    timeHour = int(jsonData[1]["price_timestamp"].split("T")[1].split(":")[0]) - 8
    if (timeHour < 0):
        timeHour = 24 + timeHour

    timeMinute = int(jsonData[1]["price_timestamp"].split("T")[1].split(":")[1])

    if len(str(timeMinute)) == 1:
        timeMinute = "0" + str(timeMinute)

    print(f"As of: {timeHour}:{timeMinute}")

    print("\n\n\n\n")


def main():

    if len(sys.argv) == 1:
        input = open("myPortfolio.txt", 'r')
    else:
        input = open(sys.argv[1], 'r')
    #
    # amounts = [float(i) for i in input.readline().split(", ")]
    # names = [i.strip() for i in input.readline().split(", ")]
    #
    # print(amounts)
    # print(names)
    #
    # portfolio = [amounts, names]
    #
    # myPortfolio(portfolio)

    # unreadable version of the above for fun:
    myPortfolio([[float(i) for i in input.readline().split(", ")], [i.strip() for i in input.readline().split(", ")]])


if __name__ == "__main__":
    main()
