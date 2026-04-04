const https = require('https');
const url = 'https://datasets-server.huggingface.co/first-rows?dataset=open-llm-leaderboard/contents&config=default&split=train&limit=100&cache=false';
https.get(url, res => {
  let data='';
  res.on('data', c => data += c);
  res.on('end', () => {
    const j = JSON.parse(data);
    const rows = j.rows.map(r => r.row).filter(r => !r.Flagged);
    rows.sort((a,b)=>(b['Average ⬆️']||-1)-(a['Average ⬆️']||-1));
    const top = rows.slice(0,20).map((r,i)=>(
      {rank:i+1, model:r.fullname, avg:r['Average ⬆️'], ifeval:r['IFEval'], bbh:r['BBH'], math:r['MATH Lvl 5'], gpqa:r['GPQA'], musr:r['MUSR'], mmlu:r['MMLU-PRO'], params:r['#Params (B)'], type:r['Type'], date:r['Submission Date']}
    ));
    const reasonScore = r => ((r['BBH']||0)+(r['GPQA']||0)+(r['MATH Lvl 5']||0)+(r['MUSR']||0))/4;
    const best = {
      reasoning: rows.slice().sort((a,b)=>reasonScore(b)-reasonScore(a))[0],
      coding: rows.slice().sort((a,b)=>(b['IFEval']||-1)-(a['IFEval']||-1))[0],
      knowledge: rows.slice().sort((a,b)=>(b['MMLU-PRO']||-1)-(a['MMLU-PRO']||-1))[0],
      value: rows.filter(r=>r['#Params (B)']>0).slice().sort((a,b)=>((b['Average ⬆️']/b['#Params (B)']) - (a['Average ⬆️']/a['#Params (B)'])))[0],
    };
    console.log(JSON.stringify({top,best}, null, 2));
  });
});