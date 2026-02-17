<div align="center">

# HowMuchLLM

</div>

**HowMuchLLM** 是一个专门帮你**估算 LLM 应用真实调用成本**的小工具。  
一句话：**给我 tokens 和调用次数，我告诉你这堆模型要烧多少钱。**🔥

CLI 命令风格简单直接：

```bash
tokenscope estimate config.yaml
```

它会读一个极简的 YAML 配置，然后输出一张 **Markdown 表格**，方便你直接贴进 PR 描述、技术方案、Notion、飞书文档里，和老板/团队一起围观「这玩意儿到底要花多少钱」😈。

---

### 项目动机 & 使用场景 🌈

- **做产品 / 做基础设施的人**经常会被问：
  - 「我们这个功能一个月大概要花多少钱？」
  - 「OpenAI / Claude / DeepSeek / Gemini 之间到底差多少成本？」
  - 「是不是可以上更大的模型，或者用便宜模型兜底？」
- 很多时候我们**已经有大概的调用画像**：
  - 每次调用平均 prompt tokens
  - 每次调用平均 completion tokens
  - 每月预估调用次数（DAU × 次数、CRON 任务等等）
- 但缺的是一个**一键把这些数字变成「钱」的工具**。

**HowMuchLLM / tokenscope** 就是干这件事的：

- 把「tokens」➡️「钱」
- 把「某一个模型」➡️「一整排模型对比」
- 把「随口估」➡️「有据可依的粗算」

---

### 功能总览 🧰

- **输入**
  - **prompt tokens**：每次调用的提示 tokens 数（如 system + user + few-shot）
  - **completion tokens**：每次调用产生的回复 tokens 数
  - **calls_per_month**：每月总调用次数
- **输出**
  - **不同模型的月成本对比表**
  - **成本拆分**：Input cost / Output cost / Total cost
  - **Markdown 表格**：直接复制到任何文档环境

---

### 支持的模型 & 价格来源 🏷️

目前内置了一批主流 API 模型（部分示例）：

- **OpenAI**
  - `openai:gpt-4o-mini`
  - `openai:gpt-4.1-mini`
  - `openai:gpt-4.1`
- **Anthropic**
  - `anthropic:claude-3.5-sonnet`
  - `anthropic:claude-3.5-haiku`
- **Google**
  - `google:gemini-1.5-pro`
  - `google:gemini-1.5-flash`
- **DeepSeek**
  - `deepseek:deepseek-v3`
  - `deepseek:deepseek-r1`

> **说明**：价格数据是按「每 1K tokens 成本」粗略写在 `pricing.py` 里的，方便本地快速比较。  
> 真正上生产之前，请一定对照官方文档校对一次单价 ✅。

---

### 安装依赖 ⚙️

在项目根目录执行：

```bash
pip install -r requirements.txt
```

`requirements.txt` 当前依赖：

```text
PyYAML>=6.0
```

只用到了一个最基础的 YAML 解析库，方便集成到各种环境。

---

### 配置文件示例 (`config.yaml`) 📄

最小配置只需要 3 个字段：

```yaml
prompt_tokens: 200          # 每次调用的 prompt tokens
completion_tokens: 400      # 每次调用的 completion tokens
calls_per_month: 10000      # 每月调用次数
```

语义非常直接：

- **prompt_tokens**：假设你已经有粗略评估（可以来自日志统计、观测数据、人工估计）
- **completion_tokens**：下游任务的平均输出长度（如问答、代码补全等）
- **calls_per_month**：通常来自「QPS × 秒数」换算，或者「日活 × 使用频次」

> 当前版本：**一个配置文件 = 一个统一 workload**。  
> 如果你有不同业务线/不同场景，可以写多个配置文件分别估算。

---

### 使用方式（开发环境）🚀

在项目根目录运行：

```bash
python -m HowMuchLLM.cli estimate config.yaml
```

如果你将本项目打包并安装为命令行工具，并暴露 entrypoint：

- `HowMuchLLM.cli:main` → `tokenscope`

那么就可以像正式 CLI 一样使用：

```bash
tokenscope estimate config.yaml
```

参数说明：

- **`estimate`**：子命令，用于「估算成本」
- **`config.yaml`**：上文所示的 YAML 配置路径

---

### 输出示例（Markdown 表格）📊

命令执行后，会在 **标准输出** 打印一张 Markdown 表，例如：

```markdown
| Provider | Model | Prompt tokens/call | Completion tokens/call | Calls/month | Total prompt tokens | Total completion tokens | Input cost | Output cost | Total cost |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OpenAI | gpt-4o-mini | 200 | 400 | 10,000 | 2,000,000 | 4,000,000 | USD 1.00 | USD 6.00 | USD 7.00 |
| Anthropic | Claude 3.5 Haiku | 200 | 400 | 10,000 | 2,000,000 | 4,000,000 | USD 1.60 | USD 16.00 | USD 17.60 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
```

你可以：

- 直接复制粘贴到：
  - README
  - 技术方案 / 决策文档
  - Notion / 飞书 / Confluence
- 或者把 stdout 重定向为一个 `.md` 文件：

```bash
python -m HowMuchLLM.cli estimate config.yaml > cost-report.md
```

---

### 代码结构 🧩

```text
HowMuchLLM/
├── HowMuchLLM/
│   ├── pricing.py   # 模型价格配置（每 1K tokens 成本）
│   ├── estimator.py # 成本估算逻辑（从 tokens -> 金额）
│   ├── report.py    # Markdown 报表生成
│   └── cli.py       # CLI 入口（tokenscope estimate）
├── example.yaml     # 示例配置（可直接修改试跑）
├── README.md
└── requirements.txt
```

下面是对核心模块的**稍微深一点解析** 👇

---

### `pricing.py`：模型价格表 🧾

- **核心数据结构**：`ModelPricing`
  - **字段**
    - `model_id`: 逻辑上的唯一 ID（如 `openai:gpt-4o-mini`）
    - `provider`: 厂商（OpenAI / Anthropic / Google / DeepSeek）
    - `display_name`: 展示名称
    - `input_per_1k`: 每 1000 个 prompt tokens 的价格
    - `output_per_1k`: 每 1000 个 completion tokens 的价格
    - `unit_tokens`: 计费单位，默认是 1000
    - `currency`: 货币，默认 `USD`
- **核心函数**：`get_default_pricing()`
  - 返回一个 `Dict[str, ModelPricing]`
  - key 是 `model_id`，方便在估算逻辑里迭代所有模型

> 如果你想：
> - 增加自家私有部署模型
> - 调整价格
> 只需要在 `get_default_pricing()` 里增删对应的 `ModelPricing` 即可。

---

### `estimator.py`：成本估算核心 🧮

- **数据结构**：`CostBreakdown`
  - 包含：
    - 模型信息：`model_id` / `provider` / `display_name`
    - 用量信息：每次调用 tokens & 每月调用次数
    - 总 tokens：`total_prompt_tokens` / `total_completion_tokens`
    - 成本拆分：`input_cost` / `output_cost`
    - 以及一个 `total_cost` 属性 = input + output

- **核心函数**
  - **`estimate_for_model(...)`**
    - 输入：单模型的 `ModelPricing` + workload 信息
    - 输出：该模型下的 `CostBreakdown`
    - 算法非常直接：

      ```python
      total_prompt = prompt_tokens * calls_per_month
      total_completion = completion_tokens * calls_per_month

      input_cost = (total_prompt / model.unit_tokens) * model.input_per_1k
      output_cost = (total_completion / model.unit_tokens) * model.output_per_1k
      ```

  - **`estimate_all(...)`**
    - 对 `pricing_table` 中的所有模型跑一遍 `estimate_for_model`
    - 返回 `Dict[model_id, CostBreakdown]`

  - **`estimate_from_config(config)`**
    - 直接接受一个字典（通常来自 YAML 解析）
    - 负责做：
      - 字段校验（缺失字段 / 非整数会抛异常）
      - 非负检查（不允许负 tokens / 负调用数）
      - 然后调用 `estimate_all`

> 你在别的 Python 代码里，可以直接 import 这个模块做内部估算，而不必通过 CLI。

---

### `report.py`：Markdown 报表 ✍️

- **核心函数**：`generate_markdown_table(results)`
  - 输入：`Dict[str, CostBreakdown]`
  - 输出：一个 Markdown 格式的字符串
  - 特点：
    - 会按 `total_cost` 对结果排序，**最便宜的在最上面**
    - 把数字做了 `,` 分隔（例如 `10,000`）
    - 把价格统一格式化为：`USD 1.23`

用于直接喂给 CLI 做 stdout，也可以在 notebook / web 服务中复用。

---

### `cli.py`：命令行入口 🖥️

- 使用 `argparse` 实现一个轻量的 CLI：
  - 顶层命令：`tokenscope`
  - 子命令：`estimate`
  - 调用格式：`tokenscope estimate config.yaml`

- 主流程（简化伪代码）：

```python
config = load_config(config_path)         # 用 PyYAML 解析
pricing_table = get_default_pricing()     # 取默认价目表
results = estimate_from_config(config, pricing_table=pricing_table)
markdown = generate_markdown_table(results)
print(markdown)
```

- 错误处理：
  - 文件不存在 / YAML 解析失败 / 配置字段不合法
  - 会打印到 `stderr`，并返回非 0 退出码

---

### 下一步可以怎么玩？🧪

- **接入你自己的日志系统**
  - 从生产日志中聚合出「平均 prompt / completion tokens」
  - 把聚合结果喂给 `estimate_from_config`
- **拆分业务线 / 功能模块**
  - 为不同场景写多个 `config-*.yaml`
  - 一键生成多份成本表，支撑预算 & 型号选择
- **做一个 Web UI / 前端表单**
  - 前端输入 tokens、调用次数、模型过滤
  - 后端复用当前 Python 模块，实时展示成本曲线

---

### 免责声明 🙏

- 本项目主要用于 **快速粗略估算**，并非严格的财务结算工具。
- 所有内置价格可能会**随时间过期**，请在重要决策前：
  - 对照官方 pricing 页
  - 校对当前 currency / region / 计费方式

欢迎直接在代码里魔改、fork、或内嵌到你自己的 AI Infra 工具链中，让「看懂 LLM 花了多少钱」变成一件顺手的小事 ✨。





