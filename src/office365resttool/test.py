#!/usr/bin/env python3

import json
import datetime
from office365resttool import shared
import ocontacts
import ocalendar

client_id = "03fee41b-949d-4021-8860-df0585bb8a64"
#scope = ["https://outlook.office.com/contacts.readwrite"]
scope = ["Calendars.ReadWrite", "Contacts.ReadWrite"]
resource = "https://outlook.office.com"
token_path = "token.json"

office = shared.login_auto(client_id, scope, resource, token_path)

ocontacts.dump_data(office, "contacts.json")
ocalendar.dump_data(office, datetime.datetime(2016, 1, 1, 0, 0, 0), datetime.datetime(2016, 12, 31, 0, 0, 0), "calendar_2016.json")

"""
id = "AAMkAGU0ZTk5ZmU3LTdkMDYtNDQyOC1hYWMxLWZjNmM5NGQwZjdmYwBGAAAAAAAvRMPsp7eMTaZhFZTrzxdYBwCMBU9ana4AQ7DpjpDP8WH4AAAAAAEOAACMBU9ana4AQ7DpjpDP8WH4AACde3RAAAA="
url = "https://outlook.office.com/api/v2.0/me/contacts/" + id
r = office.get(url)
print(json.dumps(r.json(), indent=4))

data = json.dumps({"Birthday": "1992-09-14T22:00:00Z"})
r = office.patch(url, data=data, headers={'content-type': 'application/json'})
print(r)
r = office.get(url)
print(r.json()["Birthday"])
"""

