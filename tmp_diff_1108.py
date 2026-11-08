#!/usr/bin/env python3
"""Diff today's AA parse against the previous snapshot; emit snapshot-2026-11-08.json."""
import json, re, sys, datetime

SUF = re.compile(r'-(xhigh|high|medium|low|max|minimal|non-reasoning|thinking|reasoning|daily|extended)$')


def family(slug):
    base = slug
    for _ in range(3):
        b2 = SUF.sub('', base)
        if b2 == base:
            break
        base = b2
    return base


ms = json.load(open('/tmp/aa_models.json'))
d = {}
for o in ms:
    if not isinstance(o, dict):
        continue
    sl = o.get('slug')
    if sl not in d or len(o) > len(d[sl]):
        d[sl] = o
have = [o for o in d.values()
        if isinstance(o.get('intelligenceIndex'), (int, float)) and not o.get('deprecated')]

# index version from payload
ver = 'unknown'
for o in have:
    nm = o.get('intelligenceIndexName') or ''
    if nm:
        ver = nm
        break

fam = {}
for o in have:
    f = family(o['slug'])
    if f not in fam or o['intelligenceIndex'] > fam[f]['intelligenceIndex']:
        fam[f] = o
fams = sorted(fam.values(), key=lambda o: -o['intelligenceIndex'])
cur_rank = {o['slug']: i for i, o in enumerate(fams, 1)}

prev = json.load(open('memory/leaderboard/snapshot-2026-11-07.json'))
prev_top = prev['top20']
prev_by_slug = {t['slug']: t for t in prev_top}
prev_rank = {t['slug']: t['rank'] for t in prev_top}

print(f"index: {ver} | prev index: {prev.get('index')}")
print(f"active scored: {len(have)} (prev {prev.get('active_scored')})")
print(f"slugs parsed: {len(d)} (prev {prev.get('slugs_parsed')})")
print()

rows = []
for i, o in enumerate(fams[:20], 1):
    sl = o['slug']
    p = prev_by_slug.get(sl)
    dy = (o['intelligenceIndex'] - p['idx']) if p else None
    pr = prev_rank.get(sl)
    rows.append({
        'slug': sl,
        'name': o.get('shortName', '?'),
        'idx': round(o['intelligenceIndex'], 4),
        'ow': bool(o.get('isOpenWeights')),
        'dy': round(dy, 3) if dy is not None else None,
        'prev_idx': p['idx'] if p else None,
        'prev_rank': pr,
        'rank': i,
        'tok_s': o.get('outputSpeed'),
        'ttft': o.get('timeToFirstToken'),
        'ttat': o.get('timeToFirstAnswerToken'),
        'cost_per_task': o.get('intelligenceIndexCostPerTask'),
    })

print('=== TOP 20 (family dedup) with diff vs 11-07 ===')
for r in rows:
    if r['prev_idx'] is None:
        print(f"{r['rank']:2d}. {r['name'][:40]:42s} {r['idx']:5.2f}  NEW  ow={r['ow']}")
    else:
        print(f"{r['rank']:2d}. {r['name'][:40]:42s} {r['idx']:5.2f}  dy={r['dy']:+6.2f}  prev_rank={r['prev_rank']:2d}  ow={r['ow']}")

# newcomers / dropouts in scored set
prev_slugs = set(prev_by_slug)
new_fams = [o for o in fams if o['slug'] not in prev_slugs]
print('\n=== 新進 scored（family 去重後未在 11-07 前 20 者）===')
for o in new_fams[:15]:
    print(f"  {o.get('shortName','?')[:44]:46s} {o['intelligenceIndex']:5.2f} ow={o.get('isOpenWeights')}")

# families that were in prev top20 and now dropped out
cur_slugs = set(cur_rank)
dropped = [t for t in prev_top if t['slug'] not in cur_slugs]
print('\n=== 跌出 scored（11-07 前 20 內）===')
for t in dropped:
    print(f"  {t['name'][:44]:46s} {t['idx']:5.2f}")

# all newly scored slugs (not just families)
prev_all_slugs = set(prev.get('all_scored_slugs', []))
print('\n=== 新增 scored slug 總數 ===', len(have))

# ---- domains ----
DOM = [
    ('hle-diamond', 100), ('critpt-v2-hard', 100), ('gpqa-diamond', 100),
    ('artificial-analysis-long-context-reasoning', 100),
    ('frontiercode-2-0', 100), ('terminalbench-4-0', 100), ('gdp-pdf', 100), ('scicode', 100),
    ('omniscience-accuracy', 100), ('omniscience-non-hallucination', 100), ('mmmu-pro', 100),
    ('aa-briefcase', 1), ('automationbench-aa', 100), ('terminal-bench-science', 100),
    ('apex-agents-aa', 100), ('aa-analyst-agent', 100), ('tau3-banking', 100),
    ('gdpval-aa-normalized', 100),
]


def best(key, n=3, openonly=False):
    out = []
    for o in have:
        v = (o.get('scores') or {}).get(key)
        if isinstance(v, (int, float)):
            if openonly and not o.get('isOpenWeights'):
                continue
            out.append((v, o))
    out.sort(key=lambda t: -t[0])
    return out[:n]


domains, domains_ow = {}, {}
for key, mul in DOM:
    domains[key] = [[o['slug'], v, o.get('shortName', '?')] for v, o in best(key, 3)]
    domains_ow[key] = [[o['slug'], v, o.get('shortName', '?')] for v, o in best(key, 3, openonly=True)]

print('\n=== 各領域最佳 vs 昨日 ===')
prev_dom = prev.get('domains', {})
for key, mul in DOM:
    cur = domains[key]
    if not cur:
        continue
    p = prev_dom.get(key, [])
    pmap = {x[0]: x[1] for x in p}
    tag = ''
    if cur[0][0] != (p[0][0] if p else None):
        tag = '  ★榜首更換'
    print(f"{key:44s} {cur[0][1] if mul==1 else round(cur[0][1]*100,1):>9} {cur[0][2][:34]:36s}{tag}")

# open weights
ow = sorted([o for o in fams if o.get('isOpenWeights')], key=lambda o: -o['intelligenceIndex'])
print('\n=== 開放權重 TOP 12 ===')
for i, o in enumerate(ow[:12], 1):
    print(f"{i:2d}. {o.get('shortName','?')[:44]:46s} {o['intelligenceIndex']:5.2f}")

# speed / latency / cost
sp = sorted([(o.get('outputSpeed'), o) for o in have if isinstance(o.get('outputSpeed'), (int, float))], key=lambda t: -t[0])
lt = sorted([(o.get('timeToFirstToken'), o) for o in have if isinstance(o.get('timeToFirstToken'), (int, float))], key=lambda t: t[0])
ta = sorted([(o.get('timeToFirstAnswerToken'), o) for o in have if isinstance(o.get('timeToFirstAnswerToken'), (int, float))], key=lambda t: t[0])
co = sorted([(o.get('intelligenceIndexCostPerTask'), o) for o in have if isinstance(o.get('intelligenceIndexCostPerTask'), (int, float))], key=lambda t: t[0])

snap = {
    'fetched_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'source': 'https://artificialanalysis.ai/leaderboards/models',
    'index': ver,
    'index_prev': prev.get('index'),
    'index_version_changed': ver != prev.get('index'),
    'slugs_parsed': len(d),
    'active_scored': len(have),
    'prev_active_scored': prev.get('active_scored'),
    'baseline': 'snapshot-2026-11-07.json',
    'top20': rows,
    'domains': domains,
    'domains_open_weights': domains_ow,
    'fastest_output': [[o.get('shortName', '?'), v] for v, o in sp[:8]],
    'lowest_latency': [[o.get('shortName', '?'), v] for v, o in lt[:8]],
    'lowest_ttat': [[o.get('shortName', '?'), v] for v, o in ta[:8]],
    'cheapest': [[o.get('shortName', '?'), v] for v, o in co[:8]],
    'open_weights_top12': [[o['slug'], o['intelligenceIndex'], o.get('shortName', '?')] for o in ow[:12]],
    'all_scored_slugs': sorted(o['slug'] for o in have),
    'gap_top1_vs_open1': round(fams[0]['intelligenceIndex'] - ow[0]['intelligenceIndex'], 4) if ow else None,
}
json.dump(snap, open('memory/leaderboard/snapshot-2026-11-08.json', 'w'), ensure_ascii=False, indent=1)
print('\nsaved memory/leaderboard/snapshot-2026-11-08.json')
print('gap top1 vs open1:', snap['gap_top1_vs_open1'])
print('fastest:', [(n[:24], round(v)) for n, v in snap['fastest_output'][:5]])
print('lowest latency:', [(n[:24], round(v, 2)) for n, v in snap['lowest_latency'][:5]])
print('cheapest:', [(n[:24], round(v, 4)) for n, v in snap['cheapest'][:5]])
