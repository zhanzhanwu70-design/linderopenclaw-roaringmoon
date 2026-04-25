const https = require('https');
const url = 'https://datasets-server.huggingface.co/first-rows?dataset=open-llm-leaderboard%2Fcontents&config=default&split=train&limit=100&cache=false';
https.get(url, (res) => {
  let data='';
  res.on('data', c => data += c);
  res.on('end', () => {
    const j = JSON.parse(data);
    const rows = (j.rows || []).map(r => r.row || r).filter(r => typeof r['Average ⬆️'] === 'number');
    const top = [...rows].sort((a,b)=>b['Average ⬆️']-a['Average ⬆️']).slice(0,10).map(r=>({
      model:r.fullname, avg:r['Average ⬆️'], ifeval:r['IFEval'], bbh:r['BBH'], math:r['MATH Lvl 5'], gpqa:r['GPQA'], mmlu:r['MMLU-PRO'], params:r['#Params (B)']
    }));
    const maxBy = key => [...rows].sort((a,b)=>(b[key]||-1)-(a[key]||-1))[0];
    const cats = {
      ifeval: maxBy('IFEval'),
      bbh: maxBy('BBH'),
      gpqa: maxBy('GPQA'),
      mmlu: maxBy('MMLU-PRO'),
      avg: maxBy('Average ⬆️')
    };
    console.log(JSON.stringify({top,cats}, null, 2));
  })
}).on('error', console.error);
