#!/usr/bin/env python3

import json
import datetime
import dateutil.parser
from pprint import pprint
import shared

class NameContainer:
    def __init__(self, name):
        name = name.replace("'s Birthday", "").replace("Geburtstag von ", "")
        name = name.replace(" -", "")
        name = name.replace(". ", " ").replace(", ", " ")
        name = name.replace("MAS", "").replace("MBA", "").replace("MA", "").replace("BA", "").replace("GmbH", "").replace("Mag ", "").replace("MSc", "").replace("BSc", "").replace("MBA", "").replace("e.U.", "").replace("(FH)", "").replace("Prof ", "").replace("Ing ", "").replace("CMC", "").replace("DI", "").replace("Dr ", "").replace("med ", "")
        name = name.replace(".", "").replace(",", "")
        name = name.strip()
        
        self.__name = name
        self.__set = set(name.split())
    def __str__(self):
        return self.__name
    def __repr__(self):
        return str(self)
    def __hash__(self):
        return 0
    def __eq__(self, o):
        return len(self.__set.intersection(o.__set)) >= 2

def add(d, t, i):
    if t not in d:
        d[t] = {"count": 0, "ids": []}
    e = d[t]
    e["count"] = e["count"] + 1
    e["ids"].append(i)

def extract(data, date_cb, dt_cb):
    dt_dict = {}
    time_dict = {}
    date_dict = {}
    
    for i, entry in enumerate(data):
        bdt = date_cb(entry)
        bdt = dt_cb(bdt)
        btime = date_cb(entry)
        btime = btime[5:-1].split("T")[1]
        bdate = date_cb(entry)
        bdate = bdate[5:-1].split("T")[0]
        add(dt_dict, bdt, i)
        add(time_dict, btime, i)
        add(date_dict, bdate, i)
    
    return dt_dict, time_dict, date_dict

def contacts_date(entry):
    return entry["Birthday"]

def contacts_dt(dt):
    dt = dateutil.parser.parse(dt)
    dt = dt + datetime.timedelta(days=1)
    dt = dt.replace(hour=0, minute=0, second=0, year=2016, tzinfo=None)
    return dt

def calendar_date(entry):
    return entry["Start"]["DateTime"]

def calendar_dt(dt):
    return dateutil.parser.parse(dt)

def diff(contacts, con_ids, calendar, cal_ids):
    con_names = set([NameContainer(contacts[i]["DisplayName"]) for i in con_ids])
    cal_names = set([NameContainer(calendar[i]["Subject"]) for i in cal_ids])
    return con_names.difference(cal_names), cal_names.difference(con_names)

with open("contacts.json", "r") as f:
    contacts = json.load(f)
with open("calendar_2016.json", "r") as f:
    calendar = json.load(f)

contacts_tmp = []
for c in contacts:
    if c["Birthday"] is None: continue
    contacts_tmp.append(c)
contacts = contacts_tmp

calendar_tmp = []
for c in calendar:
    sub = c["Subject"].lower()
    if "birthday" in sub or "geburtstag" in sub:
        calendar_tmp.append(c)
calendar = calendar_tmp

print(len(contacts), len(calendar))

con_dt, con_time, con_date = extract(contacts, contacts_date, contacts_dt)
cal_dt, cal_time, cal_date = extract(calendar, calendar_date, calendar_dt)

dt = datetime.datetime(2016, 1, 1, 0, 0, 0)
while dt.timetuple().tm_year == 2016:
    con_count = con_dt[dt]["count"] if dt in con_dt else 0
    cal_count = cal_dt[dt]["count"] if dt in cal_dt else 0
    cal_miss, con_miss = diff(contacts, con_dt[dt]["ids"] if dt in con_dt else [], calendar, cal_dt[dt]["ids"] if dt in cal_dt else [])
    if con_count != cal_count and (cal_miss or con_miss):
        print(dt.strftime("%d.%m."), con_count, cal_count, cal_miss if cal_miss else "{}", con_miss if con_miss else "{}")
    dt += datetime.timedelta(days=1)

