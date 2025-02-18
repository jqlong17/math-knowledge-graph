# 初中数学知识图谱智能构建系统

本项目通过集成智谱AI接口和教学大纲配置，实现了初中数学知识图谱的自动构建与 CSV 数据输出。该系统能够根据教学大纲、LLM 智能解析生成知识节点和关联关系，以支持智能备课、跨学科教学等应用场景。

## 核心功能

### 教学大纲驱动
通过 YAML 格式的教学大纲配置，自动识别教学单元、章节和知识点。

### 智能知识解析
利用智谱AI接口（glm-4 模型）获取初中数学知识结构信息，包括定义、前置知识、应用场景和常见误区。

### 知识图谱构建
根据解析结果自动生成知识节点，并构建"前置知识"等关联关系，形成完整的知识网络。

### 数据导出
最终生成 CSV 文件（知识节点、知识关系、教学策略），便于后续数据存储、可视化或整合进教学系统。

### 安全机制
采用环境变量加载 API Key，避免在代码中硬编码密钥，并提供错误处理与超时设置。

## 快速开始

### 环境配置
1. 克隆仓库：
```bash
git clone https://github.com/jqlong17/math-knowledge-graph.git
cd math-knowledge-graph
```

2. 配置环境变量：
   - 复制 `.env.example` 为 `.env`
   - 在 `.env` 中填入您的智谱AI API密钥

### 教学大纲配置
在 `config/curriculum.yaml` 中根据实际教学需要配置教学大纲，例如：

```yaml
units:
  - grade: 7
    chapters:
      - title: "有理数"
        topics: ["正负数", "数轴", "绝对值"]
      - title: "几何基础"
        topics: ["线段与角", "相交线"]
  - grade: 8
    chapters:
      - title: "三角形"
        topics: ["勾股定理", "全等三角形"]
```

## 数据模型说明

### 知识节点（Nodes）
每个知识节点包含以下字段：

| 字段 | 类型 | 说明 |
|----------------|--------|---------------------------|
| id | String | 唯一标识符（如 N001） |
| name | String | 知识点名称 |
| type | String | 概念分类（基础/核心/拓展） |
| definition | String | 核心定义 |
| unit | String | 所属教学单元 |
| cognitive_level | String | 认知层级（记忆/理解/应用等） |
| example | String | 典型例题 |
| misconception | String | 常见误区 |

### 知识关系（Relations）
描述知识节点之间的关系（如"前置知识"），支持设置权重和描述信息，以体现知识间的逻辑与应用联系。

## 项目结构
```
.
├── config/                   # 教学大纲及其他配置文件
│   └── curriculum.yaml       # 教学大纲配置
├── data/                     # CSV 数据输出目录
│   ├── knowledge_nodes.csv
│   ├── knowledge_relations.csv
│   └── teaching_strategies.csv
├── src/
│   ├── knowledge_graph_builder.py  # 知识图谱构建器
│   ├── zhipu_client.py       # 智谱AI接口适配器
│   └── visualizer.py         # 图谱可视化模块
├── .env                      # 环境变量文件
├── .env.example             # 环境变量模板
└── readme.md                # 本文档