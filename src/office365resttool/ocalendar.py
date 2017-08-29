#!/usr/bin/env python3

import json
import shared

def get(office, start_datetime, end_datetime, timezone=None):
    url = "https://outlook.office.com/api/v2.0/me/calendarview?startDateTime=%s&endDateTime=%s" % (start_datetime.strftime('%Y-%m-%dT%H:%M:%SZ'), end_datetime.strftime('%Y-%m-%dT%H:%M:%SZ'))
    headers = {}
    if timezone is not None:
        headers["Prefer"] = 'outlook.timezone="%s"' % timezone
    return shared.get_all(office, url, headers)

def dump_data(office, start_datetime, end_datetime, path, timezone=None):
    with open(path, "w") as f:
        c = shared.StreamList(get(office, start_datetime, end_datetime, timezone=timezone))
        json.dump(c, f, sort_keys=True, indent=4, separators=(",", ": "))

