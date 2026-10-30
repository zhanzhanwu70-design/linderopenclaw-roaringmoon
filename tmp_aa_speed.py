import json
ms=json.load(open('/tmp/aa_models.json'))
d={}
for o in ms:
    if o.get('slug') not in d: d[o['slug']]=o
have=[o for o in d.values() if isinstance(o.get('intelligenceIndex'),(int,float)) and not o.get('deprecated')]
sp=[(o.get('medianOutputTokensPerSecond'),o) for o in have if isinstance(o.get('medianOutputTokensPerSecond'),(int,float))]
sp.sort(key=lambda t:-t[0]); print("最快輸出:", [(o['shortName'][:24],round(v)) for v,o in sp[:6]])
lt=[(o.get('medianTimeToFirstTokenSeconds'),o) for o in have if isinstance(o.get('medianTimeToFirstTokenSeconds'),(int,float))]
lt.sort(key=lambda t:t[0]); print("最低延遲:", [(o['shortName'][:24],round(v,1)) for v,o in lt[:6]])
co=[(o.get('intelligenceIndexCostPerTask'),o) for o in have if isinstance(o.get('intelligenceIndexCostPerTask'),(int,float))]
co.sort(key=lambda t:t[0]); print("每任務成本最低:", [(o['shortName'][:24],round(v,2)) for v,o in co[:6]])
print("總評測模型數:", len(have))
# context window largest
cw=[(o.get('contextWindowTokens'),o) for o in have if isinstance(o.get('contextWindowTokens'),(int,float))]
cw.sort(key=lambda t:-t[0]); print("最大context:", [(o['shortName'][:24],v) for v,o in cw[:4]])
# Kimi K3.1 pro openweights?
for s in ['kimi-3-1-pro','deepseek-v4-pro-0813']:
    o=d.get(s)
    if o: print(s, 'open=',o.get('isOpenWeights'), o.get('intelligenceIndex'))
