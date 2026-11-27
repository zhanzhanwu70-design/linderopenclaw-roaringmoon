#!/usr/bin/env python3
"""Delete mis-ordered duplicates landed by the parallel plugin send (11/26).
Token read in-process from gateway config; never printed, never in argv, never written out.
UA must be DiscordBot (...).
"""
import json, os, urllib.request, urllib.error, time

CFG = os.path.expanduser('~/.openclaw/openclaw.json')
CHANNEL = '1482561255955763293'
ACCOUNT = 'roaringmoon'
UA = 'DiscordBot (https://github.com/openclaw/openclaw, 1.0)'
API = 'https://discord.com/api/v10'
STRAYS = ['1575527712104390677', '1575527712825806880', '1575527712913625149']


def token():
    cfg = json.load(open(CFG))
    return cfg['channels']['discord']['accounts'][ACCOUNT]['token'].strip()


def req(method, path):
    r = urllib.request.Request(API + path, method=method)
    r.add_header('Authorization', 'Bot ' + token())
    r.add_header('User-Agent', UA)
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            raw = resp.read().decode()
            return resp.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:200]


for mid in STRAYS:
    st, body = req('DELETE', f'/channels/{CHANNEL}/messages/{mid}')
    print(f'delete {mid} -> {st}' + ('' if st == 204 else f' {body}'))
    time.sleep(0.4)
