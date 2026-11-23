#!/usr/bin/env python3
"""Repost the 11/22 leaderboard segments in strict order via Discord REST.

Token is read in-process from the gateway config; never printed, never in argv,
never written to a file. UA must be DiscordBot (...).
"""
import json, os, time, urllib.request, urllib.error, hashlib, sys

CFG = os.path.expanduser('~/.openclaw/openclaw.json')
CHANNEL = '1482561255955763293'
ACCOUNT = 'roaringmoon'
UA = 'DiscordBot (https://github.com/openclaw/openclaw, 1.0)'
OLD_IDS = [
    '1574079234232815637',  # 前十 6-10 (landed first)
    '1574079234370969726',  # header
    '1574079234396266650',  # 各領域最佳 推理/程式
    '1574079234807439452',  # 前十 1-5 (landed last)
]
API = 'https://discord.com/api/v10'


def token():
    cfg = json.load(open(CFG))
    t = cfg['channels']['discord']['accounts'][ACCOUNT]['token']
    return t.strip()


def req(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(API + path, data=data, method=method)
    r.add_header('Authorization', 'Bot ' + token())
    r.add_header('User-Agent', UA)
    if data:
        r.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            raw = resp.read().decode()
            return resp.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]


def post_with_retry(text, tries=5):
    for i in range(tries):
        st, body = req('POST', f'/channels/{CHANNEL}/messages', {'content': text})
        if st in (200, 201):
            return body['id']
        if st == 429:
            time.sleep(2.0)
            continue
        raise RuntimeError(f'POST failed status={st} body={body}')
    raise RuntimeError('POST failed after retries')


def main():
    msgs = json.load(open('/tmp/msgs_1122.json'))
    new_ids = []
    for i, m in enumerate(msgs, 1):
        mid = post_with_retry(m)
        new_ids.append(mid)
        print(f'sent seg{i} -> {mid} (chars={len(m)} lines={len(m.splitlines())})')
        time.sleep(0.7)

    for old in OLD_IDS:
        st, body = req('DELETE', f'/channels/{CHANNEL}/messages/{old}')
        print(f'delete {old} -> status={st}' + ('' if st == 204 else f' body={body}'))
        time.sleep(0.4)

    st, body = req('GET', f'/channels/{CHANNEL}/messages?limit=30')
    if st != 200:
        print('READBACK FAILED', st, body)
        sys.exit(1)
    by_id = {m['id']: m['content'] for m in body}
    ok = 0
    for i, (mid, m) in enumerate(zip(new_ids, msgs), 1):
        got = by_id.get(mid)
        if got == m:
            ok += 1
            print(f'verify seg{i} {mid} MATCH ({len(m)} chars)')
        else:
            print(f'verify seg{i} {mid} MISMATCH got={None if got is None else len(got)} chars')
    total = ''.join(msgs)
    print(f'\nreadback {ok}/{len(msgs)} exact-match; chars={len(total)} sha256={hashlib.sha256(total.encode()).hexdigest()}')
    leftover = [o for o in OLD_IDS if o in by_id]
    print('old mis-ordered ids still present:', leftover if leftover else 'none')
    print('channel tail order:', [m['id'] for m in body[-len(new_ids):]])
    print('new ids in channel order:', [m['id'] for m in body if m['id'] in new_ids])


if __name__ == '__main__':
    main()
