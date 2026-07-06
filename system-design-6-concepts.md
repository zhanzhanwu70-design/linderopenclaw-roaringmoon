# System Design 六個核心概念
## Maddie — 900+ hours of Learning System Design in 9 Minutes

**影片：** https://www.youtube.com/watch?v=3Pusamd6BO4

---

## 核心理念

> 「Junior 和 Senior 工程師的差距不是年資，而是如何思考系統。」

傳統學習：背誦名詞（DNS, Sharding, CDN...）
正確學習：理解「為什麼」，建立心智模型

---

## 概念一：Statelessness（無狀態）

**定義：** Server 不記憶之前請求的資料，每個請求攜帶所有需要處理的資訊

```
有狀態：Sticky Session → Load Balancer 受限
無狀態：所有 Server 等同 → 自由路由
```

**做法：** 將狀態外推到 Redis / 分散式 cache

**問題：** 「每個 Server 持有哪些狀態？應該放在哪裡？」

---

## 概念二：Caching（快取）

**核心取捨：** Speed 換 Freshness

| 位置 | 用途 |
|------|------|
| CDN | 靜態內容，靠近用戶 |
| Redis | App-level，millisecond 延遲 |
| Database | 查詢結果 |

**重要概念：**
- TTL（Time To Live）
- Cache-aside patterns
- Write-through vs Write-back

**問題：** 「瓶頸在哪裡？資料可以多舊？」

---

## 概念三：CAP Theorem

**現實：** Partition Tolerance 是必然

| 選擇 | 意義 |
|------|------|
| **Consistency** | 每次讀取都獲得最新寫入 |
| **Availability** | 系統總是回應 |

**實務：** 不同服務可以有不同的選擇
- 強一致性：金融交易、權限
- 最終一致性：內容推薦

---

## 概念四：Message Queues（訊息佇列）

**同步問題：**
```
用戶下單 → 庫存服務 → 支付服務 → 通知服務
                ↑
         鏈條依賴，任何一個掛了全部失敗
```

**訊息佇列解法：**
```
用戶下單 → 發布事件（order_placed）
           ↓
        Kafka/SQS（佇列）
           ↓
    各服務獨立處理：庫存、支付、通知
```

**優點：** 服務間解耦，各自彈性處理失敗

---

## 概念五：Databases（資料庫）

### SQL = ACID

| 屬性 | 意義 |
|------|------|
| **Atomicity** | 交易全有或全無 |
| **Consistency** | 永遠在有效狀態間轉換 |
| **Isolation** | 併發交易不互相干擾 |
| **Durability** | 提交後永久保存 |

**NoSQL：** 犧牲部分 ACID 換取擴展性

| 何時用 SQL | 何時用 NoSQL |
|-----------|-------------|
| 金融交易 | Activity feeds |
| 庫存系統 | 產品目錄 |
| 部分失敗是災難 | 大量擴展需求 |

---

## 概念六：API Design

**API 是 contract，一旦出貨就難以改變。**

| REST | GraphQL |
|------|---------|
| 簡單、可快取 | 彈性、精確取用 |
| 公開 API、行動客戶端 | 多種客戶端需求不同 |

**好 API 設計原則：**
- 從第一天就明確版本控制
- 以資源為中心設計 endpoint
- 在別人需要 reverse engineer 之前先寫文件

---

## 面試技巧

1. **不要背誦，要理解「為什麼」**
2. **建立心智模型，不是詞彙表**
3. **具體說明應用場景**
   - 「Spotify 如何在不同層使用快取？」
   - 「Venmo 何時需要強一致性？」

---

## 與 OpenClaw 對應

| System Design 概念 | OpenClaw 實作 |
|------------------|--------------|
| Statelessness | Session 獨立，無共享狀態 |
| Caching | Session transcript、FTS index |
| CAP | 本地模型 = Consistent（無網路分割）|
| Message Queues | Cron、Heartbeat 事件驅動 |
| Databases | SQLite session 持久化 |
| API Design | Gateway API、ACP protocol |
