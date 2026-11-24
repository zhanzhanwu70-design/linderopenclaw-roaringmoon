#!/usr/bin/env node
// 驗證某個 Discord 頻道是否真的有我預期的訊息（唯讀）。
// 教訓（2026-11-24）：讀不到 ≠ 沒貼上。命中 0 筆一律印 INCONCLUSIVE，絕不印「未落地」。
// 用法: node verify-discord-channel.mjs <channelId> <pattern> [maxPages]
//   pattern = 預期出現在訊息內的片段（標題行或獨特字串）
// 環境: DISCORD_BOT_TOKEN（或指定 token 檔案）＋ DISCORD_CHANNEL_ID
import fs from "node:fs";

const [channelId, pattern, maxPagesArg] = process.argv.slice(2);
const maxPages = Number(maxPagesArg || 10);
if (!channelId || !pattern) {
  console.error("usage: node verify-discord-channel.mjs <channelId> <pattern> [maxPages]");
  process.exit(2);
}
const token = process.env.DISCORD_BOT_TOKEN;
if (!token) {
  console.error("INCONCLUSIVE: DISCORD_BOT_TOKEN 未設定 → 沒有讀取權限，無法判定是否已發布");
  process.exit(2);
}
const H = { Authorization: `Bot ${token}`, "User-Agent": "roaringmoon-verify/1.0" };
let hits = [];
let pages = 0;
let forbidden = false;
let before;
while (pages < maxPages) {
  pages++;
  const url = `https://discord.com/api/v10/channels/${channelId}/messages?limit=100${before ? `&before=${before}` : ""}`;
  let res;
  try {
    res = await fetch(url, { headers: H });
  } catch (e) {
    console.log(`INCONCLUSIVE: 第 ${pages} 頁請求失敗（${e.message}）→ 無法判定`);
    process.exit(2);
  }
  if (res.status === 403) { forbidden = true; break; }
  if (res.status === 401) {
    console.log(`INCONCLUSIVE: HTTP 401 → token／header 格式錯（要用 Bot 前綴），不是權限問題`);
    process.exit(2);
  }
  if (!res.ok) {
    console.log(`INCONCLUSIVE: HTTP ${res.status} → 無法判定`);
    process.exit(2);
  }
  const page = await res.json();
  if (!page.length) break;
  for (const m of page) {
    const c = m.content || "";
    if (c.includes(pattern)) hits.push({ id: m.id, chars: c.length, lines: c.split("\n").length });
  }
  if (page.length < 100) break;
  before = page[page.length - 1].id;
}
if (forbidden) {
  console.log(`INCONCLUSIVE: HTTP 403（此 bot 對該頻道沒有 VIEW_CHANNEL）→ 「讀不到」不等於「沒貼上」，需改由有讀取權限的帳號驗證`);
  process.exit(2);
}
if (hits.length === 0) {
  console.log(`INCONCLUSIVE: 掃了 ${pages} 頁、命中 0 筆符合「${pattern}」→ 無法斷定未發布（可能是內容不在比對範圍、或頁數上限不足）`);
  process.exit(2);
}
console.log(`FOUND ${hits.length} hit(s) over ${pages} page(s):`);
for (const h of hits) console.log(`  ${h.id}  chars=${h.chars} lines=${h.lines}`);
console.log("VERIFIED: 內容確實存在於此頻道。");
