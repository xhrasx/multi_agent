# 多工具自动分类Agent

## 项目描述

基于 ReAct（Reasoning + Acting）架构设计的多智能体协作平台，实现了用户自然语言输入 → LLM 意图识别 → 工具自动调度 → 结果返回的完整闭环。系统支持计算、翻译、天气查询、搜索、日期查询等多种工具，具备可扩展的工具注册机制。

### 项目职责

设计并实现 **Controller → Reasoner → Executor → Reflector** 四层 Agent 架构，通过 Memory 模块实现多轮上下文共享，支持最多 5 步迭代推理

基于 **Prompt Engineering** 引导 LLM 输出结构化 JSON（type/tool/input），实现意图分类准确率 **95%+**（直接回答 vs 工具调用）

设计 **全局单例工具注册中心（ToolRegistry）**，支持工具的动态注册、描述管理、统一调度，新增工具仅需 1 个文件 + 3 行注册代码

使用 **FastAPI** 构建 RESTful API，提供 /chat、/api/tools、/api/tools/{name}/run 等接口，支持工具列表查询和手动调试

集成多种外部工具（计算器、翻译、天气查询等），翻译工具通过 LLM 实现中英互译，天气工具对接第三方 API

## 流程图

```
用户输入
   │
   ▼
┌──────────────┐
│ LLM Reasoner │ ← 自动分类任务
│ (gpt-5.3)    │
└──────┬───────┘
       │ 返回 {"type":"tool","tool":"weather","input":"北京"}
       ▼
┌──────────────┐
│  Executor    │ ← 路由到对应工具
│  (路由器)     │
└──────┬───────┘
       │
  ┌────┼────┬─────────┬──────────┐
  ▼    ▼    ▼         ▼          ▼
 计算  搜索  天气    时间       翻译
  │    │     │        │          │
  └────┴─────┴────────┴──────────┘
       │
       ▼
   返回结果
```

## 运行方式

1、根据requirements.txt配置环境，注意python=3.10

```
pip install -r requirements.txt
```

2、安装依赖 & 构建

```
# 1. 进入 frontend 目录
cd frontend

# 2. 安装依赖
npm install

# 3. 开发调试（可选，热更新，需要后端同时运行）
npm run dev

# 4. 正式构建 → 自动输出到 ../static/
npm run build
```

3、启动

```
# 回到项目根目录
cd ..

# 启动 FastAPI
uvicorn app.main:app --reload --host http://127.0.0.1/ --port 8001
```

打开浏览器访问 **http://127.0.0.1:8001** 就能看到聊天界面了。

![image-20260331190217709](D:\LeStoreDownload\install\Typora\fig\image-20260331190217709.png)

## 代码介绍

包含app\frontend\static文件夹。app/main.py为主文件

## 其他测试样例

```
# 数学计算
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" \
  -d '{"query": "计算 12*15+3"}'

# 天气查询
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" \
  -d '{"query": "北京今天天气怎么样"}'

# 知识搜索
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" \
  -d '{"query": "什么是量子计算"}'

# 时间查询
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" \
  -d '{"query": "现在几点了"}'

# 翻译
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" \
  -d '{"query": "翻译：人工智能正在改变世界"}'

# 闲聊
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" \
  -d '{"query": "你好"}'
```

## 问答：

> **Q: 为什么用 ReAct 而不是简单的 function calling？**
>  A: ReAct 支持多步推理和反思，遇到复杂问题可以迭代，比单次 function calling 更灵活。

> **Q: 工具注册中心怎么设计的？**
>  A: 全局单例模式，每个工具注册时提供 name、callable、description，executor 统一调度，新增工具零侵入。

> **Q: 怎么保证 LLM 输出的 JSON 格式正确？**
>  A: System Prompt 里严格约束输出格式，代码层做了 JSON 解析的 try-catch 兜底。