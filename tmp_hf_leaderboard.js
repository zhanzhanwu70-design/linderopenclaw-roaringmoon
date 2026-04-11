const https = require('https');
const url = 'https://datasets-server.huggingface.co/first-rows?dataset=open-llm-leaderboard/contents&config=default&split=train&limit=100&cache=false';
https.get(url, res => {
  let data = '';
  res.on('data', c => data += c);
  res.on('end', () => {
    const j = JSON.parse(data);
    const rows = j.rows.map(r => r.row).filter(r => !r.Flagged && r['Average ⬆️'] != null);
    rows.sort((a,b)=> b['Average ⬆️'] - a['Average ⬆️']);
    const top10 = rows.slice(0,10).map((r,i)=>({rank:i+1, model:r.fullname, avg:r['Average ⬆️'], bbh:r['BBH'], gpqa:r['GPQA'], mmlu:r['MMLU-PRO'], ifeval:r['IFEval'], math:r['MATH Lvl 5'], params:r['#Params (B)'], type:r['Type'], date:r['Submission Date']}));
    const best = {
      reasoning: rows.slice().sort((a,b)=> (b['BBH']+b['GPQA']) - (a['BBH']+a['GPQA']))[0],
      coding: rows.slice().sort((a,b)=> (b['IFEval']+b['MATH Lvl 5']) - (a['IFEval']+a['MATH Lvl 5']))[0],
      knowledge: rows.slice().sort((a,b)=> b['MMLU-PRO'] - a['MMLU-PRO'])[0],
      value: rows.filter(r => r['#Params (B)'] > 0).slice().sort((a,b)=> (b['Average ⬆️']/b['#Params (B)']) - (a['Average ⬆️']/a['#Params (B)']))[0],
    };
    console.log(JSON.stringify({top10,best}, null, 2));
  });
}).on('error', err => { console.error(err); process.exit(1); });
