import urllib.request, re, json
html = urllib.request.urlopen('https://artificialanalysis.ai/leaderboards/models').read().decode('utf-8','ignore')
pattern = re.compile(r'<tr class="border-b[^>]*>\s*<td[^>]*position:sticky;left:0px;[^>]*><div class="font-semibold[^>]*>([^<]+)(?:<span[\s\S]*?)?</div></td>\s*<td[^>]*><div class="text-center">([^<]+)</div></td>\s*<td[^>]*><div class="flex gap-2">[\s\S]*?<span class="leading-\[16px\]">([^<]+)</span></div></td>\s*<td[^>]*><div class="text-center">([^<]+)</div></td>\s*<td[^>]*><div class="text-center">([^<]+)</div></td>\s*<td[^>]*><div class="text-center">([^<]+)</div></td>\s*<td[^>]*><div class="text-center">([^<]+)</div></td>', re.M)
out=[]
for m in pattern.finditer(html):
    out.append({
        'model': m.group(1).strip(),
        'context': m.group(2).strip(),
        'creator': m.group(3).strip(),
        'intelligence': m.group(4).strip(),
        'price': m.group(5).strip(),
        'speed': m.group(6).strip(),
        'latency': m.group(7).strip(),
    })
    if len(out) >= 15:
        break
print(json.dumps(out, ensure_ascii=False, indent=2))
