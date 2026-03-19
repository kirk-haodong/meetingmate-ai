# Meeting Search

## 描述
智能会议知识库检索系统，支持自然语言查询历史会议内容，快速找到相关决策和信息。

## 使用场景
- "查找关于Q2预算的所有讨论"
- "张三负责的任务有哪些"
- "上个月关于产品发布的决策"

## 安装
```bash
openclaw skill install meeting-search
```

## 使用
```bash
# 自然语言搜索
openclaw run meeting-search --query "Q2预算讨论"

# 按人员搜索
openclaw run meeting-search --assignee "张三"

# 按日期范围搜索
openclaw run meeting-search --from "2026-01-01" --to "2026-03-01" --query "产品发布"
```
