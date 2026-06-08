# 机器人视觉专家知识索引

这个目录是 Pagurus 的研究认知底座。它的目标不是保存零散资料，而是把机器人视觉研究中需要反复调用的判断依据组织起来。

核心问题：

> 一个机器人视觉 idea 是否值得做，它站在谁的肩膀上，解决了什么 failure mode，应该如何被证伪，最后能形成什么 claim？

## 目录结构

| 路径 | 作用 | 第一批内容 |
| --- | --- | --- |
| [00_foundations](00_foundations/README.md) | 数学和研究地基 | 线性代数、概率、优化、李群李代数 |
| [01_geometry_vision](01_geometry_vision/README.md) | 几何视觉 | 相机模型、多视图几何、PnP、BA、光流、深度 |
| [02_sensors_calibration](02_sensors_calibration/README.md) | 传感器与标定 | Camera、IMU、LiDAR、时间同步、外参、噪声模型 |
| [03_state_estimation](03_state_estimation/README.md) | 状态估计 | EKF、factor graph、preintegration、sliding window |
| [04_method_families](04_method_families/README.md) | 方法族 | VO、VIO、Visual SLAM、RGB-D SLAM、relocalization |
| [05_baselines](05_baselines/README.md) | 强 baseline | ORB-SLAM3、VINS-Mono、DROID-SLAM 等 |
| [06_failure_modes](06_failure_modes/README.md) | 失败模式库 | 弱纹理、动态遮挡、地图过期、tracking lost |
| [07_datasets](07_datasets/README.md) | 数据集与场景 | EuRoC、KITTI、TUM、自采场景、退化场景集合 |
| [08_metrics](08_metrics/README.md) | 指标与评测 | ATE、RPE、failure rate、latency、闭环成功率 |
| [09_experiments](09_experiments/README.md) | 实验记录 | baseline、消融、压力测试、最小证伪实验 |
| [10_idea_cards](10_idea_cards/README.md) | 研究想法卡片 | 每个 idea 的问题、假设、prior art、证伪实验 |
| [11_papers](11_papers/README.md) | 论文节点 | 论文结构化笔记和方法关系 |
| [12_claims](12_claims/README.md) | 研究 claim | 方法真正证明了什么，以及边界条件 |
| [13_semantic_scene](13_semantic_scene/README.md) | 语义与场景理解 | 动态物体、可通行区域、语义地图、开放词汇感知 |
| [14_world_models](14_world_models/README.md) | 视觉世界模型 | 时序表示、future prediction、occupancy flow、planning 可用性 |
| [15_expert_workflows](15_expert_workflows/README.md) | 专家工作流 | prior art 审查、baseline gate、failure 诊断、claim 审查 |

## 第一阶段聚焦

第一阶段只追求跑通：

> 视觉定位 / VIO / SLAM 研究专家。

优先填充这些目录：

1. `10_idea_cards`
2. `11_papers`
3. `04_method_families`
4. `05_baselines`
5. `06_failure_modes`
6. `08_metrics`
7. `09_experiments`
8. `12_claims`
9. `15_expert_workflows`

数学、几何和状态估计先做成“够用的检索入口”，后续遇到具体问题再扩展。

## 推荐节点关系

一个研究方向应该尽量形成下面的关系链：

```text
IdeaCard
  -> related Paper
  -> belongs to MethodFamily
  -> depends on Assumption
  -> targets FailureMode
  -> compares with Baseline
  -> verified by Experiment
  -> supports or rejects Claim
```

如果一个 idea 无法连到 `FailureMode`、`Baseline` 或 `Experiment`，它通常还不够成熟。

## 新 idea 进入流程

每个新 idea 先不要直接实现，先按这个流程进入知识图谱：

1. 写一张 `IdeaCard`。
2. 查找相似 `Paper` 和 `MethodFamily`。
3. 通过 `Baseline Gate` 判断必须比较谁。
4. 匹配或新增 `FailureMode`。
5. 设计 `Minimum Falsification Experiment`。
6. 写出预期 `Claim`。
7. 实验后更新 claim 或否定假设。

## 扩展原则

- 每个节点都要服务研究判断，而不是百科式收集。
- 每篇论文至少记录核心假设、方法机制、baseline、失败场景和 claim。
- 每个 baseline 都要记录适用条件、运行成本和典型失效情况。
- 每个 failure mode 都要能关联到真实案例或可复现实验。
- 每个实验都必须回到一个明确假设。

