#!/usr/bin/env python3
"""Read back today's 9 leaderboard segments from Discord REST and verify.
Token read in-process from gateway config; never printed, never in argv, never written out.
UA must be DiscordBot (...).
"""
import json, os, urllib.request, urllib.error, hashlib

CFG = os.path.expanduser('~/.openclaw/openclaw.json')
CHANNEL = '1482561255955763293'
ACCOUNT = 'roaringmoon'
UA = 'DiscordBot (https://github.com/openclaw/openclaw, 1.0)'
API = 'https://discord.com/api/v10'
EXPECTED_IDS = [
    '1575527974957097164',  # 1 總覽
    '1575527993311232213',  # 2 日差分
    '1575528009320898651',  # 3 前十 1-5
    '1575528026802880583',  # 4 前十 6-10 + 榜外
    '1575528043726770187',  # 5 推理
    '1575528061552558221',  # 6 程式 + 知識
    '1575528077990035689',  # 7 Agent
    '1575528096537256059',  # 8 開放權重
    '1575528118263881849',  # 9 效率 + 落差
]


def token():
    cfg = json.load(open(CFG))
    return cfg['channels']['discord']['accounts'][ACCOUNT]['token'].strip()


def req(method, path):
    r = urllib.request.Request(API + path, method=method)
    r.add_header('Authorization', 'Bot ' + token())
    r.add_header('User-Agent', UA)
    with urllib.request.urlopen(r, timeout=30) as resp:
        raw = resp.read().decode()
        return json.loads(raw) if raw else None


msgs = req('GET', f'/channels/{CHANNEL}/messages?limit=40')
json.dump(msgs, open('/tmp/msgs_1126_readback.json', 'w'), ensure_ascii=False)
by_id = {m['id']: m.get('content', '') for m in msgs}
expected = json.load(open('/tmp/msgs_1126.json'))

ok = 0
for i, (mid, exp) in enumerate(zip(EXPECTED_IDS, expected), 1):
    got = by_id.get(mid)
    if got == exp:
        ok += 1
        print(f'verify seg{i} {mid} MATCH chars={len(exp)} lines={len(exp.splitlines())}')
    else:
        print(f'verify seg{i} {mid} MISMATCH exp={len(exp)} got={None if got is None else len(got)}')
        if got is not None:
            for a, b in zip(exp.splitlines(), got.splitlines()):
                if a != b:
                    print('   exp:', repr(a))
                    print('   got:', repr(b))
                    break

total = ''.join(expected)
print(f'\nexact-match {ok}/{len(expected)}; chars={len(total)} sha256={hashlib.sha256(total.encode()).hexdigest()}')

present = [m['id'] for m in msgs if m['id'] in EXPECTED_IDS]
print('expected order exact:', present == EXPECTED_IDS)
print('count in window:', len(present), 'unique:', len(set(present)))

# leftover duplicates: any other message today whose content equals one of ours
dupes = [m['id'] for m in msgs if m.get('content') in expected and m['id'] not in EXPECTED_IDS]
print('duplicate leftovers:', dupes if dupes else 'none')
# strays from the first (mis-ordered) parallel send
STRAYS = ['1575527712104390677', '1575527712825806880', '1575527712913625149']
print('strays still present:', [s for s in STRAYS if s in by_id] or 'none')

# continuity: did yesterday's round land?
prev_ids = ['1575166219152138403', '1575166248193626366', '1575166269693624371', '1575166300609585235',
            '1575166320658350213', '1575166342158360607', '1575166366611415274', '1575166401885245614']
print('yesterday round still present:', sum(1 for p in prev_ids if p in by_id), '/8')
