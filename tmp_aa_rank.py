import json, re, collections
ms = json.load(open('/tmp/aa_models.json'))
d = {}
for o in ms:
    sl = o.get('slug')
    if sl not in d: d[sl] = o
have = [o for o in d.values() if isinstance(o.get('intelligenceIndex'), (int,float)) and not o.get('deprecated')]
have.sort(key=lambda o: -o['intelligenceIndex'])

SUF = re.compile(r'-(xhigh|high|medium|low|max|minimal|non-reasoning|thinking|reasoning|daily|extended)$')
def family(slug):
    base = slug
    for _ in range(3):
        b2 = SUF.sub('', base)
        if b2 == base: break
        base = b2
    return base

fam = {}
for o in have:
    f = family(o['slug'])
    if f not in fam or o['intelligenceIndex'] > fam[f]['intelligenceIndex']:
        fam[f] = o

print("=== AA v5 TOP 15 (raw, by reasoning setting) ===")
for i,o in enumerate(have[:15],1):
    print(f"{i:2d}. {o['shortName'][:45]:47s} {o['intelligenceIndex']:.1f}  {o['modelCreatorName']}")

print()
print("=== FAMILY-DEDUP TOP 15 ===")
fams = sorted(fam.values(), key=lambda o: -o['intelligenceIndex'])
for i,o in enumerate(fams[:15],1):
    print(f"{i:2d}. {o['shortName'][:45]:47s} {o['intelligenceIndex']:.1f}  {o['modelCreatorName']}  open={o.get('isOpenWeights')}")

def best(key, n=3, filt=None):
    rows=[]
    for o in have:
        v = (o.get('scores') or {}).get(key)
        if isinstance(v,(int,float)):
            if filt and not filt(o): continue
            rows.append((v,o))
    rows.sort(key=lambda t:-t[0])
    return rows[:n]

domains = {
 '推理 HLE-Diamond':'hle-diamond',
 '推理 CritPt v2 hard':'critpt-v2-hard',
 '推理 長上下文推理':'artificial-analysis-long-context-reasoning',
 '推理 AIME 2025':'aime-2025',
 '程式 FrontierCode 2.0':'frontiercode-2-0',
 '程式 Terminal-Bench 4.0':'terminalbench-4-0',
 '程式 LiveCodeBench':'livecodebench',
 '程式 GDP.pdf 專業文件':'gdp-pdf',
 '知識 GDP.pdf':'gdp-pdf',
 '知識 Omniscience 準確率':'omniscience-accuracy',
 '知識 非幻覺率':'omniscience-non-hallucination',
 '知識 GPQA Diamond':'gpqa-diamond',
 '知識 MMMU-Pro':'mmmu-pro',
 'Agent AA-Briefcase':'aa-briefcase',
 'Agent AutomationBench-AA':'automationbench-aa',
 'Agent Terminal-Bench-Science':'terminal-bench-science',
 'Agent APEX-Agents-AA':'apex-agents-aa',
 'Agent AA-Analyst-Agent':'aa-analyst-agent',
 'Agent Tau3-Banking':'tau3-banking',
}
print()
for label,key in domains.items():
    rows = best(key,3)
    if not rows: 
        print(f"{label:28s} (無資料)"); continue
    print(f"{label:28s} -> " + " | ".join(f"{o['shortName'][:34]} {v*100:.1f}" for v,o in rows))

# open weights best
print()
print("=== 開放權重最佳 ===")
ow = [o for o in fams if o.get('isOpenWeights')]
for i,o in enumerate(ow[:10],1):
    print(f"{i:2d}. {o['shortName'][:42]:44s} {o['intelligenceIndex']:.1f} {o['modelCreatorName']}")

# speed / latency / cost
print()
print("=== 速度/延遲/成本 ===")
sp=[(o.get('medianTokensPerSecond'),o) for o in have if isinstance(o.get('medianTokensPerSecond'),(int,float))]
sp.sort(key=lambda t:-t[0])
print("fastest:", [(o['shortName'][:26],round(v)) for v,o in sp[:5]])
lt=[(o.get('medianTimeToFirstTokenSeconds'),o) for o in have if isinstance(o.get('medianTimeToFirstTokenSeconds'),(int,float))]
lt.sort(key=lambda t:t[0])
print("lowest latency:", [(o['shortName'][:26],round(v,1)) for v,o in lt[:5]])
co=[(o.get('intelligenceIndexCostPerTask'),o) for o in have if isinstance(o.get('intelligenceIndexCostPerTask'),(int,float))]
co.sort(key=lambda t:t[0])
print("cheapest/task:", [(o['shortName'][:26],round(v,2)) for v,o in co[:6]])
