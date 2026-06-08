# 03 State Estimation

这里保存机器人定位、VIO 和 SLAM 的状态估计知识。

## 知识范围

- Kalman Filter / EKF / UKF。
- Particle Filter。
- Factor Graph。
- IMU Preintegration。
- Sliding Window Optimization。
- Marginalization。
- Pose Graph Optimization。
- Loop Closure。

## 专家需要回答的问题

- 方法到底估计什么状态？
- 状态中包含 pose、velocity、bias、landmark 还是 map？
- 使用了哪些观测？
- 观测噪声如何建模？
- 估计是否可观？

## 第一批条目

- `ekf.md`
- `factor_graph.md`
- `imu_preintegration.md`
- `sliding_window.md`
- `pose_graph_optimization.md`

