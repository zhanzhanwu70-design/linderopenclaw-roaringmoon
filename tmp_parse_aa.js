const https = require('https');
const url = 'https://artificialanalysis.ai/leaderboards/models';
https.get(url, (res) => {
  let data='';
  res.on('data', c => data += c);
  res.on('end', () => {
    const pattern = /position:sticky;left:0px;[^>]*>([^<]+)<\/td>[\s\S]{0,800}?min-width:100px;[^>]*>([^<]+)<\/td>[\s\S]{0,400}?min-width:160px;[^>]*>([^<]+)<\/td>[\s\S]{0,400}?min-width:160px;[^>]*>([^<]+)<\/td>[\s\S]{0,400}?min-width:120px;[^>]*>(\$?[^<]+)<\/td>/g;
    let m; let out=[];
    while((m = pattern.exec(data)) && out.length < 20){
      out.push({model:m[1], context:m[2], creator:m[3], intelligence:m[4], price:m[5]});
    }
    console.log(JSON.stringify(out,null,2));
  })
}).on('error', console.error);
