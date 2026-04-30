const https = require('https');
const url = 'https://datasets-server.huggingface.co/first-rows?dataset=open-llm-leaderboard/contents&config=default&split=train&limit=100&cache=false';
https.get(url, res => {
  let data='';
  res.on('data', c => data += c);
  res.on('end', () => {
    const json = JSON.parse(data);
    const rows = json.rows.map(r => r.row);
    const clean = rows.filter(r => !r.Flagged && typeof r['Average ⬆️'] === 'number');
    clean.sort((a,b)=>b['Average ⬆️']-a['Average ⬆️']);
    const top = clean.slice(0,20).map((r,i)=>({
      rank:i+1,
      name:r.fullname,
      avg:r['Average ⬆️'],
      params:r['#Params (B)'],
      ifeval:r['IFEval'],
      bbh:r['BBH'],
      math:r['MATH Lvl 5'],
      gpqa:r['GPQA'],
      musr:r['MUSR'],
      mmlu:r['MMLU-PRO'],
      date:r['Submission Date']
    }));
    const valueRows = clean.filter(r => r['#Params (B)'] > 0).map(r => ({...r, valueScore:r['Average ⬆️']/r['#Params (B)']})).sort((a,b)=>b.valueScore-a.valueScore);
    const best = {
      reasoning: clean.slice().sort((a,b)=>((b['BBH']+b['GPQA']+b['MUSR'])-(a['BBH']+a['GPQA']+a['MUSR'])))[0],
      code: clean.slice().sort((a,b)=>((b['IFEval']+b['MATH Lvl 5'])-(a['IFEval']+a['MATH Lvl 5'])))[0],
      knowledge: clean.slice().sort((a,b)=>b['MMLU-PRO']-a['MMLU-PRO'])[0],
      value: valueRows[0]
    };
    console.log(JSON.stringify({top,best}, null, 2));
  });
});