#!/usr/bin/env python3

import json
import shared

def get(office):
    return shared.get_all(office, "https://outlook.office.com/api/v2.0/me/contacts")

def dump_data(office, path):
    with open(path, "w") as f:
        c = shared.StreamList(get(office))
        json.dump(c, f, sort_keys=True, indent=4, separators=(",", ": "))

def dump_photos(office, path, contacts):
    pass

def fix_birthdays(office, contacts=None):
    pass
