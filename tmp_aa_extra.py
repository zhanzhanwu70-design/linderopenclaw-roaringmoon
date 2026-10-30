import json
ms = json.load(open('/tmp/aa_models.json'))
d={}
for o in ms:
    if o.get('slug') not in d: d[o['slug']]=o
have=[o for o in d.values() if isinstance(o.get('intelligenceIndex'),(int,float)) and not o.get('deprecated')]
print("keys sample:", sorted(have[0].keys()))
print()
print("=== Gemini 4 Carbon detail ===")
g = d.get('gemini-4-carbon')
print(json.dumps(g, ensure_ascii=False, indent=1)[:1500] if g else "not found")
