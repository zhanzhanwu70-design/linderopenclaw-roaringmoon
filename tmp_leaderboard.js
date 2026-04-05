const url='https://datasets-server.huggingface.co/first-rows?dataset=open-llm-leaderboard/contents&config=default&split=train&limit=100&cache=false';
const res=await fetch(url);
const data=await res.json();
const rows=data.rows.map(r=>r.row);
rows.sort((a,b)=>(b['Average ⬆️']??-1)-(a['Average ⬆️']??-1));
const top=rows.slice(0,20).map((r,i)=>(
  {rank:i+1, name:r.fullname, avg:r['Average ⬆️'], ifeval:r['IFEval'], bbh:r['BBH'], math:r['MATH Lvl 5'], gpqa:r['GPQA'], musr:r['MUSR'], mmlu:r['MMLU-PRO'], params:r['#Params (B)'], type:r['Type'], date:r['Submission Date']}
));
console.log(JSON.stringify({top,
  categories:(()=>{
    function best(key){return rows.reduce((a,b)=>(a==null||((b[key]??-1)>(a[key]??-1))?b:a),null)}
    const value=rows.filter(r=>r['#Params (B)']>0).reduce((a,b)=>{
      if(!a) return b;
      const sa=(a['Average ⬆️']/a['#Params (B)']);
      const sb=(b['Average ⬆️']/b['#Params (B)']);
      return sb>sa?b:a;
    },null)
    return {
      avg: best('Average ⬆️'),
      bbh: best('BBH'),
      math: best('MATH Lvl 5'),
      gpqa: best('GPQA'),
      mmlu: best('MMLU-PRO'),
      ifeval: best('IFEval'),
      musr: best('MUSR'),
      value
    };
  })()
},null,2));