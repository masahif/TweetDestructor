#!/usr/bin/env python
# -*- coding: utf-8 -*-

# self tweet destructor like efemr
# 2016/03/03 Masahiro Fukuda

from twitter import *
from datetime import time, datetime, timedelta
import re


def destructor(token, token_key, con_secret, con_secret_key):
    t = Twitter(auth=OAuth(token, token_key, con_secret, con_secret_key))
    user_timeline = t.statuses.user_timeline(count=200)

    for tweet in user_timeline:
        match = re.search('#([0-9])([dmh])(\s|$)', tweet['text'])
        if not match:
            continue

        # #5m, #1h, #3d
        num = int(match.group(1))
        unit = match.group(2)

        if unit == 'd':
            tdelta = timedelta(num) # days
        elif unit == 'h':
            tdelta = timedelta(0, 60 * 60 * num) # hours
        elif unit == 'm':
            tdelta = timedelta(0, 60 * num) # minutes
        else:
            continue

        c = datetime.strptime(
            tweet['created_at'].replace('+0000','UTC'),
            '%a %b %d %H:%M:%S %Z %Y')
        ctime = datetime.combine(
            c.date(),
            time(c.time().hour, c.time().minute, c.time().second))

        if datetime.utcnow() - ctime > tdelta:
            t.statuses.destroy(id = tweet['id'])
            print("%d will be deleted : %s" % (tweet['id'], tweet['text']))
        else:
            print("%d will not be deleted : %s" % (tweet['id'], tweet['text']))


if __name__ == "__main__":
    import sys, json

    if not len(sys.argv) == 2:
        print("usage: python3 %s auth_key.json" % (sys.argv[0]))
        sys.exit(1)

    f = open(sys.argv[1])
    keys = json.load(f)
    f.close()

    destructor(
        keys["access_token"],
        keys["access_token_secret"],
        keys["consumer_key"],
        keys["consumer_secret"])


