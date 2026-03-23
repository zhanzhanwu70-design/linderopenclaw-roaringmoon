# Behavior Tree 流程骨架與用途摘要

來源：Linder 提供的 subtree XML 封包（共 34 個 BT XML）
目的：把核心流程骨架與每棵樹的一句話用途整理成單一文件，方便後續查閱。

---

## 一、核心流程骨架

### `apriltag_positioning.xml`
```text
Sequence
├── publish status=1
├── switch apriltag topic
└── ApriltagDetectionControllerDecorator
    └── Fallback
        ├── Sequence（主成功流程）
        │   ├── calibration
        │   ├── close hardware collision
        │   ├── broadcast spot
        │   ├── open software collision monitor
        │   ├── sleep
        │   ├── lookup transform
        │   ├── script(close_monitor=false)
        │   ├── RecoveryNode(MoveToGoalSmoothControl, retries=3)
        │   │   ├── PipelineSequence
        │   │   │   ├── RateController(10Hz)
        │   │   │   │   └── Sequence
        │   │   │   │       ├── check collision
        │   │   │   │       ├── lookup transform
        │   │   │   │       └── Precondition(!close_monitor)
        │   │   │   │           └── IfThenElse
        │   │   │   │               ├── check monitor distance
        │   │   │   │               ├── always success
        │   │   │   │               └── Sequence
        │   │   │   │                   ├── close all software monitors
        │   │   │   │                   └── script(close_monitor=true)
        │   │   │   └── smooth move
        │   │   └── wait
        │   ├── RecoveryNode(MoveToGoalPIDControl, retries=3)
        │   │   ├── PipelineSequence
        │   │   │   ├── RateController(10Hz)
        │   │   │   │   └── Sequence
        │   │   │   │       ├── check collision
        │   │   │   │       ├── lookup transform
        │   │   │   │       ├── ForceSuccess
        │   │   │   │       │   └── lookup transform
        │   │   │   │       └── Precondition(!close_monitor)
        │   │   │   │           └── IfThenElse
        │   │   │   │               ├── check monitor distance
        │   │   │   │               ├── always success
        │   │   │   │               └── Sequence
        │   │   │   │                   ├── close all software monitors
        │   │   │   │                   └── script(close_monitor=true)
        │   │   │   └── PID move
        │   │   └── wait
        │   ├── open hardware collision
        │   ├── close all software monitors
        │   └── publish status=2
        └── ForceFailure
            └── Sequence（失敗清理流程）
                ├── publish status=3
                ├── open hardware collision
                └── close all software monitors
```

### `pattern_positioning.xml`
```text
Sequence
├── publish status=1
└── PatternDetectionControllerDecorator
    └── Fallback
        ├── Sequence（主成功流程）
        │   ├── close hardware collision
        │   ├── SelectPatternTypeService
        │   ├── broadcast spot
        │   ├── open software collision monitor
        │   ├── sleep
        │   ├── lookup transform
        │   ├── script(close_monitor=false)
        │   ├── RecoveryNode(MoveToGoalSmoothControl, retries=3)
        │   │   ├── PipelineSequence
        │   │   │   ├── RateController(10Hz)
        │   │   │   │   └── Sequence
        │   │   │   │       ├── check collision
        │   │   │   │       ├── ForceSuccess(lookup transform)
        │   │   │   │       └── Precondition(!close_monitor)
        │   │   │   │           └── IfThenElse
        │   │   │   │               ├── check monitor distance
        │   │   │   │               ├── always success
        │   │   │   │               └── Sequence
        │   │   │   │                   ├── close precise monitor
        │   │   │   │                   └── script(close_monitor=true)
        │   │   │   └── smooth move
        │   │   └── wait
        │   ├── script(close_monitor=false)
        │   ├── RecoveryNode(MoveToGoalPIDControl, retries=3)
        │   │   ├── PipelineSequence
        │   │   │   ├── RateController(10Hz)
        │   │   │   │   └── Sequence
        │   │   │   │       ├── check collision
        │   │   │   │       ├── ForceSuccess(lookup transform)
        │   │   │   │       ├── ForceSuccess(lookup transform)
        │   │   │   │       └── Precondition(!close_monitor)
        │   │   │   │           └── IfThenElse
        │   │   │   │               ├── check monitor distance
        │   │   │   │               ├── always success
        │   │   │   │               └── Sequence
        │   │   │   │                   ├── close all software monitors
        │   │   │   │                   └── script(close_monitor=true)
        │   │   │   └── PID move
        │   │   └── wait
        │   ├── open hardware collision
        │   ├── close all software monitors
        │   └── publish status=2
        └── ForceFailure
            └── Sequence（失敗清理流程）
                ├── publish status=3
                ├── open hardware collision
                └── close all software monitors
```

### `navigate_to_pose.xml`
```text
RecoveryNode(retries=3)
├── Sequence（主成功流程）
│   ├── publish status=1
│   ├── planner setup
│   ├── controller setup
│   ├── goal checker setup
│   ├── sleep
│   ├── PipelineSequence
│   │   ├── RateController(2Hz)
│   │   │   └── IfThenElse
│   │   │       ├── turn signal condition
│   │   │       ├── Switch2(signal direction)
│   │   │       │   ├── Sequence(left signal)
│   │   │       │   ├── Sequence(right signal)
│   │   │       │   └── turn on red light
│   │   │       └── ForceSuccess(turn on blue light)
│   │   ├── ForceSuccess
│   │   │   └── Sequence
│   │   │       ├── goal pose updated
│   │   │       └── set blackboard
│   │   └── navigate to pose
│   ├── planner setup
│   ├── controller setup
│   ├── goal checker setup
│   └── publish status=2
└── Sequence（失敗清理流程）
    ├── publish status=3
    ├── turn on red light
    ├── turn on red warning light
    ├── wait
    ├── turn on blue light
    └── turn on green warning light
```

### `navigate_through_poses.xml`
```text
RecoveryNode(retries=3)
├── Sequence（主成功流程）
│   ├── publish status=1
│   ├── planner setup
│   ├── controller setup
│   ├── goal checker setup
│   ├── sleep
│   ├── PipelineSequence
│   │   ├── RateController(2Hz)
│   │   │   └── IfThenElse
│   │   │       ├── turn signal condition
│   │   │       ├── Switch2(signal direction)
│   │   │       │   ├── Sequence(left signal)
│   │   │       │   ├── Sequence(right signal)
│   │   │       │   └── turn on red light
│   │   │       └── ForceSuccess(turn on blue light)
│   │   ├── ForceSuccess(goal poses updated)
│   │   └── navigate through poses
│   ├── planner setup
│   ├── controller setup
│   ├── goal checker setup
│   └── publish status=2
└── Sequence（失敗清理流程）
    ├── publish status=3
    ├── turn on red light
    ├── turn on red warning light
    ├── wait
    ├── turn on blue light
    └── turn on green warning light
```

### `motion_by_speed_control.xml`
```text
Fallback
├── Sequence（主成功流程）
│   ├── publish status=1
│   ├── Precondition(use_monitor)
│   │   └── open software collision monitor
│   ├── PipelineSequence
│   │   ├── RateController(10Hz)
│   │   │   └── Sequence
│   │   │       ├── lookup transform
│   │   │       └── check collision
│   │   └── RateController(10Hz)
│   │       └── motion by speed control
│   ├── close position control monitor
│   └── publish status=2
└── ForceFailure
    └── Sequence（失敗清理流程）
        ├── publish status=3
        └── close all software monitors
```

### `narrow_aisle_control.xml`
```text
Fallback
├── Sequence（主成功流程）
│   ├── publish status=1
│   ├── GetAmrFootprintCondition
│   ├── Timeout
│   │   └── RetryUntilSuccessful
│   │       └── Sequence
│   │           ├── wall detection
│   │           ├── select parallel wall detection mode
│   │           └── lookup transform
│   ├── close hardware collision
│   ├── open software collision monitor
│   ├── PipelineSequence
│   │   ├── RateController(10Hz)
│   │   │   └── Sequence
│   │   │       ├── check collision
│   │   │       ├── ForceSuccess
│   │   │       │   └── RetryUntilSuccessful
│   │   │       │       └── Sequence
│   │   │       │           ├── wall detection
│   │   │       │           ├── select parallel wall detection mode
│   │   │       │           └── lookup transform
│   │   │       └── ForceSuccess
│   │   │           └── Sequence
│   │   │               ├── visualize left wall marker
│   │   │               └── visualize right wall marker
│   │   └── curvature PID control
│   ├── open software collision monitor
│   ├── Precondition(remaining_distance != 0)
│   │   └── SubTree(MotionBySpeedControlTree)
│   ├── close position control monitor
│   ├── open hardware collision
│   └── publish status=2
└── ForceFailure
    └── Sequence（失敗清理流程）
        ├── publish status=3
        ├── close all software monitors
        └── open hardware collision
```

### `pallet_control.xml`
```text
Sequence
├── publish status=1
├── switch pallet topic
└── PalletDetectionControllerDecorator
    └── Fallback
        ├── Sequence（主成功流程）
        │   ├── close hardware collision
        │   ├── broadcast spot
        │   ├── sleep
        │   ├── lookup transform
        │   ├── RecoveryNode(MoveToGoalSmoothControl, retries=3)
        │   │   ├── PipelineSequence
        │   │   │   ├── RateController(10Hz)
        │   │   │   │   └── Sequence
        │   │   │   │       ├── check collision
        │   │   │   │       └── ForceSuccess(lookup transform)
        │   │   │   └── smooth move
        │   │   └── wait
        │   ├── broadcast spot
        │   ├── sleep
        │   ├── lookup transform
        │   ├── RecoveryNode(MoveToGoalSmoothControl, retries=3)
        │   │   ├── PipelineSequence
        │   │   │   ├── RateController(10Hz)
        │   │   │   │   └── Sequence
        │   │   │   │       ├── check collision
        │   │   │   │       └── ForceSuccess(lookup transform)
        │   │   │   └── smooth move
        │   │   └── wait
        │   ├── SubTree(MotionBySpeedControlTree)
        │   ├── open hardware collision
        │   ├── close all software monitors
        │   └── publish status=2
        └── ForceFailure
            └── Sequence（失敗清理流程）
                ├── publish status=3
                ├── open hardware collision
                └── close all software monitors
```

### `shelves_control.xml`
```text
Fallback
├── Sequence（主成功流程）
│   ├── publish status=1
│   ├── GetAmrFootprintCondition
│   ├── Timeout
│   │   └── RetryUntilSuccessful
│   │       └── Sequence
│   │           ├── wall detection
│   │           ├── select parallel wall detection mode
│   │           ├── four legs detection
│   │           └── lookup transform
│   ├── RecoveryNode(MoveToGoalSmoothControl, retries=3)
│   │   ├── PipelineSequence
│   │   │   ├── RateController(10Hz)
│   │   │   │   └── Sequence
│   │   │   │       ├── check collision
│   │   │   │       ├── Timeout
│   │   │   │       │   └── RetryUntilSuccessful
│   │   │   │       │       └── Sequence
│   │   │   │       │           ├── wall detection
│   │   │   │       │           ├── select parallel wall detection mode
│   │   │   │       │           └── four legs detection
│   │   │   │       └── ForceSuccess
│   │   │   │           └── visualize four legs
│   │   │   └── smooth move
│   │   └── wait
│   ├── PipelineSequence
│   │   ├── RateController(10Hz)
│   │   │   └── Sequence
│   │   │       ├── check collision
│   │   │       ├── Timeout
│   │   │       │   └── RetryUntilSuccessful
│   │   │       │       └── Sequence
│   │   │       │           └── wall detection
│   │   │       └── ForceSuccess
│   │   │           └── Sequence
│   │   │               ├── select parallel wall detection mode
│   │   │               ├── four legs detection
│   │   │               ├── lookup transform
│   │   │               └── visualize four legs
│   │   └── PID move
│   └── publish status=2
└── ForceFailure
    └── Sequence（失敗清理流程）
        ├── publish status=3
        └── close all software monitors
```

---

## 二、每棵樹一句話用途摘要

### Apriltag 系列
- `apriltag_positioning.xml`：用 Apriltag 做精定位，先平滑靠近再 PID 微調。
- `apriltag_positioning_by_distance.xml`：先由距離資訊推算停車點，再進入 Apriltag 精定位。
- `apriltag_positioning_by_position.xml`：先把輸入位置轉為目標 pose，再進入 Apriltag 精定位。
- `apriltag_positioning_by_landmark.xml`：從 landmark 查詢目標，再進入 Apriltag 精定位。
- `apriltag_pose_initial.xml`：用 Apriltag 觀測結果設定 AMR 初始位姿。
- `apriltag_pose_saving.xml`：把 Apriltag 對應的位置存成 landmark。
- `apriltag_positioning_backup.xml`：Apriltag 精定位的備援版本，含水平位移策略與殘距離補走。
- `apriltag_positioning_recovery.xml`：Apriltag 精定位的恢復版，失敗時可用 odom 更新目標再重試。

### Pattern 系列
- `pattern_positioning.xml`：用 pattern 視覺標記做精定位，流程和 Apriltag 版相似。
- `pattern_positioning_by_distance.xml`：由距離推算停車點後，再進入 pattern 精定位。
- `pattern_positioning_by_position.xml`：從指定位置直接切入 pattern 精定位。
- `pattern_positioning_by_landmark.xml`：由 landmark 查詢位置後，再進入 pattern 精定位。
- `pattern_pose_initial.xml`：用 pattern 偵測結果設定初始位姿。
- `pattern_pose_saving.xml`：把 pattern 對應位置存為 landmark。
- `pattern_positioning_backup.xml`：pattern 精定位的備援版本，帶水平位移與補走流程。

### Navigation 系列
- `navigate_to_pose.xml`：單點導航主流程，含燈號控制、目標更新、重試與失敗警示。
- `navigate_through_poses.xml`：多點導航主流程，支援路徑中途更新與轉向燈提示。
- `navigate_to_pose_landmark.xml`：從 landmark 查詢導航目標後執行單點導航。
- `navigate_to_pose_saving.xml`：把目前位置存為 landmark。

### SLAM / 地圖系列
- `open_slam.xml`：開啟 SLAM 前的燈號與 localization 切換。
- `close_slam.xml`：關閉 SLAM 後恢復 localization 並釋放燈號覆蓋。
- `load_map.xml`：載入地圖與各種 filter/costmap，並設定初始位姿。
- `save_map.xml`：儲存地圖前切換燈號狀態，然後執行 map save。
- `set_initial_pose.xml`：設定初始位姿後稍作等待讓系統穩定。

### Motion / Control 系列
- `motion_by_speed_control.xml`：通用速度控制移動子樹，帶碰撞監控與失敗清理。
- `move_aside_control.xml`：利用牆面偵測暫時側移到避讓位置。
- `narrow_aisle_control.xml`：在狹窄走道內持續看牆、控曲率、修正路徑。
- `wait_control.xml`：等待流程，開綠燈、等待、釋放燈號，再發布成功。

### 場景作業系列
- `pallet_control.xml`：托盤對位與靠近控制，分兩段平滑接近後再速度微調。
- `shelves_control.xml`：貨架對位控制，利用牆面與四腳特徵做平滑 + PID 接近。
- `shelves_control_backup.xml`：貨架控制備援版，加入水平位移策略。

### 任務前後收尾
- `setup_before_task.xml`：任務開始前只做藍燈提示。
- `teardown_after_task.xml`：任務結束後切換成綠燈提示。

---

## 三、最值得先讀的幾棵樹

如果要快速理解整包邏輯，建議先看：
1. `navigate_to_pose.xml` — 看導航主線
2. `motion_by_speed_control.xml` — 看共用移動子樹
3. `apriltag_positioning.xml` — 看精定位主線
4. `pattern_positioning.xml` — 看另一種視覺定位主線
5. `load_map.xml` / `open_slam.xml` — 看地圖與 SLAM 切換
6. `pallet_control.xml` / `shelves_control.xml` — 看場景任務控制

---

## 四、一句話總結

這整包 XML 的核心其實是：
- **導航主樹** 負責移動到區域
- **精定位主樹** 負責靠近標記或圖樣做最後修正
- **共用控制子樹** 負責速度控制、等待、地圖切換、任務燈號
- **場景任務樹** 負責 pallet / shelves / aisle 等特殊工況

