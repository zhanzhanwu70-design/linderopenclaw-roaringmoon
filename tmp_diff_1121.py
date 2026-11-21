#!/usr/bin/env python3
"""Build today's AA snapshot (2026-11-17) and diff vs snapshot-2026-11-17.json.

New AA payload shape (2026-11): model objects start with {"id":"..."},
carry release.slug (family-level) + suffix (effort variant).
We reconstruct the legacy slug scheme (family-<effort>) so diffs against
older snapshots keep working.
"""
import json, re, sys, datetime, collections

SUF_RE = re.compile(r'-(xhigh|high|medium|low|max|minimal|non-reasoning|thinking|reasoning|daily|extended)$')


def family(slug):
    base = slug
    for _ in range(3):
        b2 = SUF_RE.sub('', base)
        if b2 == base:
            break
        base = b2
    return base


def extract_objects(s, marker='{"id":"'):
    out, i, n = [], 0, len(s)
    while True:
        j = s.find(marker, i)
        if j < 0:
            break
        depth, instr, esc = 0, False, False
        k = j
        while k < n:
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
            o = json.loads(s[j:k + 1])
            if isinstance(o, dict):
                out.append(o)
        except Exception:
            pass
        i = j + len(marker)
    return out


def build_slug(o):
    """family slug + effort suffix, matching the legacy slug scheme."""
    rel = o.get('release') or {}
    base = rel.get('slug') or o.get('slug') or ''
    if not base:
        return None
    suf = (o.get('suffix') or '').lower()
    for eff in ('xhigh', 'minimal', 'non-reasoning', 'medium', 'high', 'low', 'max'):
        if suf.startswith(eff):
            return f"{base}-{eff}"
    return base


def load_models():
    html = open('/tmp/aa_models.html', encoding='utf-8', errors='ignore').read()
    s = html.replace('\\"', '"').replace('\\\\', '\\')
    objs = extract_objects(s)
    by_slug = {}
    for o in objs:
        sl = build_slug(o)
        if not sl:
            continue
        o['_slug'] = sl
        # keep the richest object per slug
        prev = by_slug.get(sl)
        if prev is None:
            by_slug[sl] = o
        else:
            def q(x):
                sc = isinstance(x.get('intelligenceIndex'), (int, float)) and not x.get('deprecated')
                return (1 if sc else 0, len(json.dumps(x)))
            if q(o) > q(prev):
                by_slug[sl] = o
    return list(by_slug.values())


def main():
    models = load_models()
    have = [o for o in models
            if isinstance(o.get('intelligenceIndex'), (int, float)) and not o.get('deprecated')]
    have.sort(key=lambda o: -o['intelligenceIndex'])
    print(f'slugs={len(models)} active_scored={len(have)}')

    # family dedup (best effort variant per model)
    fam = {}
    for o in have:
        f = family(o['_slug'])
        if f not in fam or o['intelligenceIndex'] > fam[f]['intelligenceIndex']:
            fam[f] = o
    fams = sorted(fam.values(), key=lambda o: -o['intelligenceIndex'])

    ver = 'unknown'
    # index version lives in the page markup, not the model objects
    try:
        raw = open('/tmp/aa_models.html', encoding='utf-8', errors='ignore').read()
        m = re.search(r'Intelligence Index v[0-9.]+', raw)
        if m:
            ver = m.group(0)
    except Exception:
        pass

    base_path = sys.argv[1] if len(sys.argv) > 1 else 'memory/leaderboard/snapshot-2026-11-20.json'
    prev = {}
    prev_ver = None
    try:
        pj = json.load(open(base_path))
        prev = {r['slug']: r for r in pj.get('top20', [])}
        prev_ver = pj.get('index')
    except Exception as e:
        print('baseline load failed:', e)

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
        ('推理 HLE-Diamond', 'hle-diamond', 100),
        ('推理 CritPt v2 Hard', 'critpt-v2-hard', 100),
        ('推理 GPQA Diamond', 'gpqa-diamond', 100),
        ("推理 Humanity's Last Exam", 'humanitys-last-exam', 100),
        ('推理 長上下文推理', 'artificial-analysis-long-context-reasoning', 100),
        ('程式 FrontierCode 2.0', 'frontiercode-2-0', 100),
        ('程式 Terminal-Bench 4.0', 'terminalbench-4-0', 100),
        ('程式 SciCode', 'scicode', 100),
        ('程式 GDP.pdf', 'gdp-pdf', 100),
        ('知識 Omniscience 準確率', 'omniscience-accuracy', 100),
        ('知識 非幻覺率', 'omniscience-non-hallucination', 100),
        ('知識 MMMU-Pro', 'mmmu-pro', 100),
        ('知識 MKA 多模態知識', 'mka', 100),
        ('Agent AA-Briefcase', 'aa-briefcase', 1),
        ('Agent AutomationBench-AA', 'automationbench-aa', 100),
        ('Agent Terminal-Bench-Science', 'terminal-bench-science', 100),
        ('Agent GDPval-AA', 'gdpval-aa-normalized', 100),
        ('Agent AA-Analyst-Agent', 'aa-analyst-agent', 100),
        ('Agent APEX-Agents-AA', 'apex-agents-aa', 100),
        ('Agent Tau3-Banking', 'tau3-banking', 100),
    ]

    print('\n=== TOP 12 (family dedup) ===')
    rows_out = []
    for i, o in enumerate(fams[:20], 1):
        sl = family(o['_slug'])          # family-level key matches legacy snapshot scheme
        pr = prev.get(sl)
        dy = (o['intelligenceIndex'] - pr['idx']) if pr else None
        rank = i
        prev_rank = pr.get('rank') if pr else None
        rows_out.append((rank, o, dy, prev_rank, pr))
        flag = ''
        if pr is None:
            flag = '  ★NEW'
        elif prev_rank != rank:
            flag = f"  rank {prev_rank}→{rank}"
        print(f"{i:2d}. {o.get('shortName','?')[:40]:42s} {o['intelligenceIndex']:6.2f} "
              f"dy={dy if dy is None else round(dy,2)} prev_rank={prev_rank}{flag} ow={o.get('isOpenWeights')}")

    print('\n=== 各領域最佳 ===')
    dom_out = {}
    for label, key, mul in domains:
        r = best(key, 3)
        if not r:
            print(f'{label:28s} (無資料)')
            continue
        dom_out[key] = [(round(v, 4), o['_slug'], o.get('shortName')) for v, o in r]
        fmt = (lambda v: f'{v:.0f}') if mul == 1 else (lambda v: f'{v*100:.1f}')
        print(f'{label:28s} -> ' + ' | '.join(f"{o.get('shortName','?')[:30]} {fmt(v)}" for v, o in r))

    print('\n=== 開放權重 TOP 8 ===')
    ow = [o for o in fams if o.get('isOpenWeights')][:8]
    for i, o in enumerate(ow, 1):
        print(f"{i:2d}. {o.get('shortName','?')[:40]:42s} {o['intelligenceIndex']:6.2f}")

    print('\n=== 開放權重各領域最佳 ===')
    ow_dom = {}
    for label, key, mul in [('Terminal-Bench 4.0', 'terminalbench-4-0', 100),
                            ('HLE-Diamond', 'hle-diamond', 100),
                            ('GPQA Diamond', 'gpqa-diamond', 100),
                            ('AutomationBench-AA', 'automationbench-aa', 100),
                            ('FrontierCode 2.0', 'frontiercode-2-0', 100),
                            ("Humanity's Last Exam", 'humanitys-last-exam', 100),
                            ('AA-Briefcase', 'aa-briefcase', 1)]:
        r = best(key, 3, openonly=True)
        if r:
            ow_dom[key] = [(round(v, 4), o['_slug'], o.get('shortName')) for v, o in r]
            fmt = (lambda v: f'{v:.0f}') if mul == 1 else (lambda v: f'{v*100:.1f}')
            print(f'{label:24s} -> ' + ' | '.join(f"{o.get('shortName','?')[:26]} {fmt(v)}" for v, o in r))

    sp = sorted([(o.get('outputSpeed'), o) for o in have
                 if isinstance(o.get('outputSpeed'), (int, float))], key=lambda t: -t[0])[:5]
    lt = sorted([(o.get('timeToFirstToken'), o) for o in have
                 if isinstance(o.get('timeToFirstToken'), (int, float))], key=lambda t: t[0])[:5]
    co = sorted([(o.get('intelligenceIndexCostPerTask'), o) for o in have
                 if isinstance(o.get('intelligenceIndexCostPerTask'), (int, float))], key=lambda t: t[0])[:5]
    print('\n最快輸出:', [(o.get('shortName', '?')[:24], round(v)) for v, o in sp])
    print('最低延遲:', [(o.get('shortName', '?')[:24], round(v, 1)) for v, o in lt])
    print('每任務最便宜:', [(o.get('shortName', '?')[:24], round(v, 2)) for v, o in co])

    snap = {
        'fetched_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'source': 'https://artificialanalysis.ai/leaderboards/models',
        'index': ver,
        'index_prev': prev_ver,
        'index_version_changed': bool(prev_ver and ver != prev_ver),
        'slugs_parsed': len(models),
        'active_scored': len(have),
        'baseline': base_path,
        'top20': [{
            'slug': family(o['_slug']), 'variant': o['_slug'], 'name': o.get('shortName'),
            'idx': o['intelligenceIndex'],
            'ow': bool(o.get('isOpenWeights')), 'rank': rank,
            'creator': o.get('modelCreatorName'),
            'price_in': o.get('price1mInputTokens'), 'price_out': o.get('price1mOutputTokens'),
            'tok_s': o.get('outputSpeed'), 'ttft': o.get('timeToFirstToken'),
            'cost_per_task': o.get('intelligenceIndexCostPerTask'),
        } for rank, o, dy, pr, _ in rows_out],
        'domains': dom_out,
        'domains_open_weights': ow_dom,
        'all_scored_slugs': sorted(o['_slug'] for o in have),
    }
    out = 'memory/leaderboard/snapshot-2026-11-21.json'
    json.dump(snap, open(out, 'w'), ensure_ascii=False, indent=1)
    print('\nwrote', out)


if __name__ == '__main__':
    main()
