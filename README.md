# 《系统集成项目管理工程师教程-第三版》Obsidian 双链知识图谱 & 通用 Agent Skill

> 包含全书 17 个章节、1,260 个概念节点的 Obsidian 原生双链知识图谱，配有零依赖快速检索工具与通用 AI Agent 考点问答助手（`SKILL.md`）。

---

## 🌟 核心特性

- 🧠 **Obsidian 原生双链图谱**：全书被重构提炼为 1,260 个独立的 Markdown 概念节点。每个节点均包含规范的 YAML Frontmatter 元数据、面包屑导航及交叉 `[[双链]]`。
- 🤖 **通用 Agent Skill (`SKILL.md`)**：任何支持 Skill 规范的 AI Agent 均可加载本项目，精准解答软考疑问，**杜绝 AI 幻觉**。
- 📍 **严格考点出处溯源**：AI Agent 回答问题时，强制附带标准出处后缀（如：`【出处：第1章 信息化发展 - 1.1.1 信息基础 - 信息的传输模型】`）。
- ⚡ **零额外依赖检索 (`scripts/search_knowledge.py`)**：基于 Python 3 标准库（`json`, `re`, `sys`），无需安装任何 pip 包即可在控制台中毫秒级定位知识点。
- 📦 **精简空间占用**：去除了大体积原始单体文本，全书知识集中存放在 `graph/` 中，轻量高效。

---

## 📁 目录结构

```
pmWiki/
├── README.md                      # 项目说明文档
├── SKILL.md                       # 通用 AI Agent Skill 规范说明
├── 目录.md                          # 原始教材大纲目录
├── graph/                         # Obsidian 双链知识图谱数据库
│   ├── INDEX.md                   # 全局 MOC (Map of Content) 目录
│   ├── knowledge_index.json       # AI Agent 全局检索索引库
│   ├── 第01章-信息化发展/          # 章节知识节点文件夹
│   │   ├── 第1章-概览.md           # 章节 MOC
│   │   ├── 信息的传输模型.md       # 概念节点文件
│   │   └── ...
│   ├── 第02章-信息技术发展/
│   └── ... (共 17 个章节目录)
├── images/                        # 教材架构图与插图资源
└── scripts/
    ├── search_knowledge.py        # [运行时] 零依赖知识检索脚本
    └── build_knowledge_graph.py   # [离线] 知识图谱构建解析脚本
```

---

## 🚀 使用指南

### 1. 作为 Obsidian 知识库使用
1. 打开 [Obsidian](https://obsidian.md/) 软件。
2. 选择 **Open folder as vault**（打开文件夹作为仓库）。
3. 选择本项目中的 `graph/` 目录。
4. 打开 `INDEX.md` 开始探索知识图谱，或按 `Ctrl + G` 开启 **Graph View (关系图谱)** 查阅整体网络关联。

---

### 2. 作为 AI Agent Skill 使用
把本项目路径提供给 AI Agent，Agent 将会自动读取 `SKILL.md`。

#### Agent 检索命令示例：
```bash
python scripts/search_knowledge.py "信息传输模型"
```
**检索返回 JSON**：
```json
{
  "query": "信息传输模型",
  "total_matches": 1,
  "results": [
    {
      "title": "信息的传输模型",
      "chapter": "第1章 信息化发展",
      "section": "1.1.1 信息基础",
      "file_path": "graph/第01章-信息化发展/信息的传输模型.md",
      "summary": "信息传输通常包括信源、信宿、信道、编码器、译码器和噪声等..."
    }
  ]
}
```

---

### 3. Agent 对话效果示例

**用户**：
> 请问什么是信息的传输模型？包含哪些要素？

**Agent**：
> 信息的传输模型是用来描述信息如何从信源流动到信宿的抽象模型。包含以下 6 个主要部件：
> 1. **信源**：产生信息的实体。
> 2. **信宿**：信息的归宿或接收者。
> 3. **信道**：传送信息的通道（如 TCP/IP 网络、光纤等）。
> 4. **编码器**：变换信号的设备（包含调制器、压缩编码器、加密设备等）。
> 5. **译码器**：编码器的逆变换设备。
> 6. **噪声**：传输过程中的干扰。
> 
> ---
> **【出处：第1章 信息化发展 - 1.1.1 信息基础 - 信息的传输模型】**  
> 详细节点：[信息的传输模型.md](file:///d:/AgentsWorkspace/pmWiki/graph/第01章-信息化发展/信息的传输模型.md)

---

## 📜 许可与说明

- 本知识图谱基于《系统集成项目管理工程师教程-第三版》整理提炼，仅供个人学习、备考及 AI 辅助教学研究使用。
