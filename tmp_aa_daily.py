#!/usr/bin/env python3
"""Fetch + rank Artificial Analysis leaderboard (v5.0 Intelligence Index).

Usage:
    python3 tmp_aa_daily.py fetch    # download AA leaderboard page -> /tmp/aa_models.html
    python3 tmp_aa_daily.py parse    # parse -> /tmp/aa_models.json
    python3 tmp_aa_daily.py rank     # print top list + domain bests + speed/cost

Notes (2026-10-30):
  * AA moved its payload: the authoritative full model list lives on
    https://artificialanalysis.ai/leaderboards/models (NOT /models, which only
    returns a ~28-model chart subset).
  * Each model object carries a nested `scores` dict (hle-diamond,
    frontiercode-2-0, terminalbench-4-0, omniscience-accuracy, ...).
    Per-eval scores are NOT top-level fields.
  * /api/v2/data/llms/models requires an API key (401) -> use the page payload.
"""
import json, re, subprocess, sys, collections

URL = 'https://artificialanalysis.ai/leaderboards/models'
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36'


def fetch():
    subprocess.run(['curl', '-sL', '--max-time', '60', '-A', UA, URL,
                    '-o', '/tmp/aa_models.html'], check=True)
    print('fetched', len(open('/tmp/aa_models.html', 'rb').read()), 'bytes')


def parse():
    html = open('/tmp/aa_models.html', encoding='utf-8', errors='ignore').read()
    s = html.replace('\\"', '"').replace('\\\\', '\\')
    models, i = [], 0
    while True:
        j = s.find('"slug":', i)
        if j < 0:
            break
        start = s.rfind('{', 0, j)
        if start < 0:
            i = j + 6
            continue
        depth, instr, esc, k = 0, False, False, start
        while k < len(s):
            c = s[k]
            if instr:
                if esc:
                    esc = False
                elif c == '\\':
                    esc = True
                elif c == '"':
                    instr = False
            else:
                if c == '"':
                    instr = True
                elif c == '{':
                    depth += 1
                elif c == '}':
                    depth -= 1
                    if depth == 0:
                        break
            k += 1
        try:
            o = json.loads(s[start:k + 1])
        except Exception:
            i = j + 6
            continue
        if isinstance(o, dict) and 'intelligenceIndex' in o:
            models.append(o)
        i = j + 6
    d = {}
    for o in models:
        sl = o.get('slug')
        if sl not in d or len(o) > len(d[sl]):
            d[sl] = o
    json.dump(list(d.values()), open('/tmp/aa_models.json', 'w'), ensure_ascii=False)
    have = [o for o in d.values() if isinstance(o.get('intelligenceIndex'), (int, float)) and not o.get('deprecated')]
    print('parsed slugs:', len(d), '| active scored:', len(have))


SUF = re.compile(r'-(xhigh|high|medium|low|max|minimal|non-reasoning|thinking|reasoning|daily|extended)$')


def family(slug):
    base = slug
    for _ in range(3):
        b2 = SUF.sub('', base)
        if b2 == base:
            break
        base = b2
    return base


def rank():
    ms = json.load(open('/tmp/aa_models.json'))
    d = {}
    for o in ms:
        if not isinstance(o, dict):
            continue
        sl = o.get('slug')
        if sl not in d or len(o) > len(d[sl]):
            d[sl] = o
    have = [o for o in d.values() if isinstance(o.get('intelligenceIndex'), (int, float)) and not o.get('deprecated')]
    have.sort(key=lambda o: -o['intelligenceIndex'])
    fam = {}
    for o in have:
        f = family(o['slug'])
        if f not in fam or o['intelligenceIndex'] > fam[f]['intelligenceIndex']:
            fam[f] = o
    fams = sorted(fam.values(), key=lambda o: -o['intelligenceIndex'])

    print('\n=== TOP 15 (family dedup) ===')
    for i, o in enumerate(fams[:15], 1):
        print(f"{i:2d}. {o.get('shortName','?')[:42]:44s} {o['intelligenceIndex']:5.1f}  ow={o.get('isOpenWeights')}")

    def best(key, n=3, openonly=False):
        rows = []
        for o in have:
            v = (o.get('scores') or {}).get(key)
            if isinstance(v, (int, float)):
                if openonly and not o.get('isOpenWeights'):
                    continue
                rows.append((v, o))
        rows.sort(key=lambda t: -t[0])
        return rows[:n]

    domains = [
        ('推理 HLE-Diamond', 'hle-diamond', 100), ('推理 CritPt v2 hard', 'critpt-v2-hard', 100),
        ('推理 GPQA Diamond', 'gpqa-diamond', 100),
        ('推理 長上下文推理', 'artificial-analysis-long-context-reasoning', 100),
        ('程式 FrontierCode 2.0', 'frontiercode-2-0', 100),
        ('程式 Terminal-Bench 4.0', 'terminalbench-4-0', 100),
        ('程式 GDP.pdf', 'gdp-pdf', 100), ('程式 SciCode', 'scicode', 100),
        ('知識 Omniscience 準確率', 'omniscience-accuracy', 100),
        ('知識 非幻覺率', 'omniscience-non-hallucination', 100),
        ('知識 MMMU-Pro', 'mmmu-pro', 100),
        ('Agent AA-Briefcase', 'aa-briefcase', 1),
        ('Agent AutomationBench-AA', 'automationbench-aa', 100),
        ('Agent Terminal-Bench-Science', 'terminal-bench-science', 100),
        ('Agent APEX-Agents-AA', 'apex-agents-aa', 100),
        ('Agent AA-Analyst-Agent', 'aa-analyst-agent', 100),
        ('Agent Tau3-Banking', 'tau3-banking', 100),
        ('Agent GDPval-AA', 'gdpval-aa-normalized', 100),
    ]
    print('\n=== 各領域最佳 ===')
    for label, key, mul in domains:
        rows = best(key, 3)
        if not rows:
            print(f'{label:26s} (無)')
            continue
        fmt = (lambda v: f'{v:.0f}') if mul == 1 else (lambda v: f'{v*100:.1f}')
        print(f'{label:26s} -> ' + ' | '.join(f"{o.get('shortName','?')[:32]} {fmt(v)}" for v, o in rows))

    print('\n=== 開放權重 TOP 10 ===')
    for i, o in enumerate([x for x in fams if x.get('isOpenWeights')][:10], 1):
        print(f"{i:2d}. {o.get('shortName','?')[:42]:44s} {o['intelligenceIndex']:5.1f}")

    print('\n=== 開放權重各領域最佳 ===')
    for label, key, mul in [('Terminal-Bench 4.0', 'terminalbench-4-0', 100), ('HLE-Diamond', 'hle-diamond', 100),
                            ('GPQA Diamond', 'gpqa-diamond', 100), ('AutomationBench-AA', 'automationbench-aa', 100),
                            ('FrontierCode 2.0', 'frontiercode-2-0', 100), ('AA-Briefcase', 'aa-briefcase', 1)]:
        rows = best(key, 3, openonly=True)
        fmt = (lambda v: f'{v:.0f}') if mul == 1 else (lambda v: f'{v*100:.1f}')
        print(f'{label:22s} -> ' + (' | '.join(f"{o.get('shortName','?')[:28]} {fmt(v)}" for v, o in rows) if rows else '(無)'))

    print('\n=== 速度 / 延遲 / 成本 ===')
    sp = sorted([(o.get('outputSpeed'), o) for o in have
                 if isinstance(o.get('outputSpeed'), (int, float))], key=lambda t: -t[0])
    print('最快輸出:', [(o.get('shortName', '?')[:26], round(v)) for v, o in sp[:5]])
    lt = sorted([(o.get('timeToFirstToken'), o) for o in have
                 if isinstance(o.get('timeToFirstToken'), (int, float))], key=lambda t: t[0])
    print('最低延遲:', [(o.get('shortName', '?')[:26], round(v, 1)) for v, o in lt[:5]])
    co = sorted([(o.get('intelligenceIndexCostPerTask'), o) for o in have
                 if isinstance(o.get('intelligenceIndexCostPerTask'), (int, float))], key=lambda t: t[0])
    print('每任務最便宜:', [(o.get('shortName', '?')[:26], round(v, 2)) for v, o in co[:6]])
    print('\n總評測模型數:', len(have))


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if cmd in ('fetch', 'all'):
        fetch()
    if cmd in ('parse', 'all'):
        parse()
    if cmd in ('rank', 'all'):
        rank()
