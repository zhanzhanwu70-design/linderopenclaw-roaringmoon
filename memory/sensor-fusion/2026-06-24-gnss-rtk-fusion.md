# 傳感器融合研究：GNSS/RTK + 感測器融合

**來源：** rowlet 每日研究（2026-06-24）
**主題：** GNSS/RTK + 感測器融合

## 涵蓋內容

### RTK / PPP-RTK / PPP 技術比較
- RTK: 即時動態定位，需基站，公分級精度
- PPP-RTK: 精密單點定位 + RTK，結合兩者優點
- PPP: 精密單點定位，無需基站，但收斂時間長

### GNSS + IMU 耦合層次
- **Loose Coupling:** GNSS 和 IMU 獨立，結果融合
- **Tight Coupling:** 原始測量值層級融合
- **Ultra-Tight Coupling:** IMU 幫助追蹤 GNSS 信號

### 城市環境挑戰
- NLOS（非視距）訊號問題
- Shadow matching（陰影匹配）
- Wi-Fi RTT 備援
- 視覺里程計輔助

### ROS2 實作
- `robot_localization` EKF
- `navsat_transform_node` 設定

## 與 elle_ws 的關聯
AMR（自動導航機器人）需要精確定位，GNSS + IMU 融合是室外定位的關鍵技術。
