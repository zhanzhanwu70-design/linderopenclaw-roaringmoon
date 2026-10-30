import re, json, collections
html = open('/tmp/aa_models.html', encoding='utf-8', errors='ignore').read()
# unescape RSC payload
s = html.replace('\\"', '"').replace('\\\\', '\\')
models = []
i = 0
keyset = collections.Counter()
while True:
    j = s.find('{"slug":"', i)
    if j < 0: break
    depth = 0; k = j; instr = False; esc = False
    while k < len(s):
        c = s[k]
        if instr:
            if esc: esc = False
            elif c == '\\': esc = True
            elif c == '"': instr = False
        else:
            if c == '"': instr = True
            elif c == '{': depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    break
        k += 1
    blob = s[j:k+1]
    try:
        o = json.loads(blob)
    except Exception:
        i = j + 8; continue
    if isinstance(o, dict) and 'slug' in o:
        models.append(o)
        for kk in (o.get('scores') or {}): keyset[kk]+=1
    i = j + 8
print("parsed models:", len(models))
print("score keys:", dict(keyset))
json.dump(models, open('/tmp/aa_models.json','w'), ensure_ascii=False)
