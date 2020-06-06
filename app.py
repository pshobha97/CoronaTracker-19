import os

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import pandas as pd
app=Flask(__name__)

@app.route("/",methods=["GET"])
@app.route("/home",methods=["GET"])

@cross_origin()
def homepage():

    if request.method=="GET":
        url="https://www.mohfw.gov.in/"
        load=uReq(url)

        page=load.read()
        load.close()

        covid_html=bs(page,"html.parser")

        data=covid_html.find("div",{"class":"site-stats-count"})

        datas=data.findAll("strong")
        data={}
        total=0
        for i,d in enumerate(datas):
            total+=int(d.text)
            data.update({"data"+str(i):d.text})
        data.update({"data4":total})

        table = covid_html.find("table")
        trs = table.find_all("tr")
        del trs[0]
        records = []
        for tr in trs:
            record = []
            for td in tr.find_all("td"):
                record.append(td.text)

            records.append(record)
        print(records)
        del records[-1:-5:-1]

        time_data = covid_html.find("section", {"class": "site-stats"})
        time = time_data.find("div", {"class": "status-update"}).h2.span.text

        #world
        world_url = "https://www.worldometers.info/coronavirus/#countries"
        html_page = requests.get(world_url).text
        soup = bs(html_page, "lxml")
        table = soup.find("table", id="main_table_countries_today")
        tbody = table.find("tbody")
        trs = tbody.find_all("tr")
        countries = []

        for tr in trs:
            country = []
            for td in tr.find_all("td"):
                country.append(td.text)
            c = []
            for i in range(0, 8):
                c.append(country[i])

            countries.append(c)

        world = countries[7]
        del countries[0:8]


        world_confirm = world[2]
        world_newcase = world[3]
        world_death = world[4]

    return render_template("home.html",data=data,time=time,records=records,countries=countries,world_confirm=world_confirm,world_death=world_death,world_newcase=world_newcase)
@app.route("/about",methods=["GET"])
@cross_origin()
def about():
    if request.method=="GET":
        return render_template("about.html")

@app.route("/contact",methods=["GET"])
@cross_origin()
def contact():
    if request.method=="GET":
        return render_template("contact.html")


if __name__=="__main__":
     app.run()
