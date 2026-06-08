# 14 World Models

这里保存视觉世界模型知识。

## 知识范围

- Video prediction。
- Latent dynamics model。
- Action-conditioned prediction。
- Occupancy prediction。
- Scene flow / occupancy flow。
- Memory representation。
- Uncertainty-aware prediction。
- Model-based planning。

## 专家需要回答的问题

- 世界模型预测什么？
- 预测对象是像素、深度、occupancy、状态，还是 collision risk？
- 训练目标是否服务 planning？
- 离线预测 loss 和闭环任务收益是否一致？
- 世界模型在动态场景、长 horizon 和分布外场景下如何失败？

## 第一批条目

- `latent_world_model.md`
- `occupancy_prediction.md`
- `action_conditioned_prediction.md`
- `planning_utility.md`

