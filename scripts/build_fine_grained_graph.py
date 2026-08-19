#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fine-Grained Semantic Knowledge Graph & Bidirectional Link Builder for System Integration Project Management Engineer (3rd Edition)
Generates:
1. Comprehensive Chapter Topics & 49 Management Process Nodes
2. Dedicated High-Value Artifacts / Deliverables / Tools & Techniques / Models Entity Nodes
3. Full Cross-Chapter Obsidian [[wikilinks]] Network
"""

import os
import sys
import glob
import re
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = BASE_DIR
RAW_DIR = os.path.join(PROJECT_DIR, "raw")
GRAPH_DIR = os.path.join(PROJECT_DIR, "graph")

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def sanitize_filename(name):
    name = re.sub(r'[\\/:*?"<>|]', '_', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

IMG_PATTERN = re.compile(r'!\[.*?\]\(.*?\)\s*\n?')

def clean_text_images(text):
    return IMG_PATTERN.sub('', text)

CH15_CUSTOM_TITLES = {
    "15.1.1": "信息系统信息与文档",
    "15.1.2": "信息(文档)管理规则和方法",
    "15.2.1": "配置管理基本概念",
    "15.2.2": "配置管理角色与职责",
    "15.2.3": "配置管理目标与方针",
    "15.2.4": "配置管理活动",
    "15.3.1": "变更管理基本概念",
    "15.3.2": "变更管理角色与职责",
    "15.3.3": "变更管理工作程序",
    "15.3.4": "变更控制",
    "15.3.5": "版本发布和回退计划"
}

# Rich Dedicated Entity Definitions
CORE_DEDICATED_ENTITIES = [
    # Chapter 10
    {
        "ch_num": 10,
        "filename": "项目章程.md",
        "title": "项目章程 (Project Charter)",
        "category": "核心交付物/管理文件",
        "section": "10.1 制定项目章程",
        "tags": ["第10章", "启动过程组", "核心输出", "正式授权", "高频考点"],
        "aliases": ["项目章程", "Project Charter", "章程"],
        "content": """# 项目章程 (Project Charter)

## 1. 概念定义与核心作用
项目章程是编写一份**正式批准项目并授权项目经理在项目活动中使用组织资源**的文件。
- **确立正式地位**：标志着项目的正式启动，赋予项目经理动用组织资源的法定权力。
- **签发者**：由项目发起人、PMO 或项目组合治理委员会主席签发。
- **任命时机**：项目经理应在规划开始之前任命，**最好在制定项目章程时就任命**。
- **法律性质**：项目章程**不能当作合同**，用于建立组织内部的合作关系。

## 2. 包含的核心要素 (12大主要内容)
1. 项目目的和批准项目的理由（商业论证）；
2. 可测量的项目目标和相关的成功标准；
3. 高层级需求、高层级项目描述、边界定义；
4. 整体项目风险；
5. 总体里程碑进度计划；
6. 预先批准的财务资源（总体预算）；
7. 关键干系人清单；
8. 项目审批要求（成功标准、签署人等）；
9. 项目退出标准；
10. 委派的项目经理及其职责和职权；
11. 发起人或其他批准项目章程的人员的姓名和职权。

## 3. 全生命周期过程流转网络
- **产生本文件的过程**：
  - 由 [[10.1 制定项目章程]] 作为核心主要输出产生。
- **作为主要输入的后续过程 (共12个)**：
  - [[10.2 识别干系人]]
  - [[11.1 制订项目管理计划]]
  - [[11.2 规划范围管理]]
  - [[11.6 规划进度管理]]
  - [[11.11 规划成本管理]]
  - [[11.14 规划质量管理]]
  - [[11.15 规划资源管理]]
  - [[11.17 规划沟通管理]]
  - [[11.18 规划风险管理]]
  - [[11.23 规划采购管理]]
  - [[11.24 规划干系人参与]]
  - [[14.1 结束项目或阶段]]

---
### 关联概念双链
[[10.1 制定项目章程]], [[立项管理文件]], [[协议]], [[假设日志]], [[项目管理计划]]
"""
    },
    {
        "ch_num": 10,
        "filename": "立项管理文件.md",
        "title": "立项管理文件 (Project Authorization Documents)",
        "category": "核心交付物/管理文件",
        "section": "10.1 制定项目章程",
        "tags": ["第10章", "启动过程组", "立项管理", "商业论证"],
        "aliases": ["立项管理文件", "商业论证", "可行性研究报告", "项目评估报告"],
        "content": """# 立项管理文件 (Project Authorization Documents)

## 1. 概念定义与组成
立项管理文件是立项管理阶段经批准的结果或相关文件，是用于制定项目章程的关键依据，通常包括：
1. **项目建议书 (Project Proposal)**：项目最初的概念性描述。
2. **可行性研究报告 (Feasibility Study Report)**：从技术、经济、运行、法律等方面进行论证。
3. **项目评估报告 (Project Evaluation Report)**：组织对项目投资价值做出的综合评审结论。

## 2. 核心考点与管理原则
- **非项目文件属性**：立项管理文件在项目启动前由组织高层制定，**不是项目文件**。项目经理**不可以对它们进行更新或修改**，只可以提出修改建议。
- **决策依据**：高层管理者使用立项管理文件作为决策依据，确定项目的期望结果是否值得所需投资。
- **引发因素**：通常由市场需求、组织需要、客户要求、技术进步、法律法规、社会需要等因素引发。

## 3. 全生命周期过程流转网络
- **源头关联**：源自 [[9.5.2 项目可行性研究]] 与 [[9.5.3 项目评估与决策]]。
- **输入过程**：作为主要输入参与 [[10.1 制定项目章程]]。

---
### 关联概念双链
[[10.1 制定项目章程]], [[项目章程]], [[9.5.2 项目可行性研究]], [[协议]]
"""
    },
    {
        "ch_num": 10,
        "filename": "假设日志.md",
        "title": "假设日志 (Assumption Log)",
        "category": "核心交付物/管理文件",
        "section": "10.1 制定项目章程",
        "tags": ["第10章", "启动过程组", "假设条件", "制约因素"],
        "aliases": ["假设日志", "Assumption Log"],
        "content": """# 假设日志 (Assumption Log)

## 1. 概念定义与核心作用
假设日志用于记录整个项目生命周期中的所有**假设条件 (Assumptions)** 和 **制约因素 (Constraints)**。
- **高层级记录**：在制定项目章程时，记录高层级的战略和运营假设条件及制约因素。
- **渐进明细**：在后续规划过程中，随着需求分析、WBS分解、进度与成本估算，较低层级的具体假设条件和制约因素会被持续记录到假设日志中。

## 2. 核心考点
- **动态更新**：假设日志贯穿项目始终，必须定期审核。当假设条件被证实为不成立时，通常会演变成**项目风险**或导致**变更请求**。
- **与风险分析的关联**：定性风险分析过程中，假设日志用于评估假设条件对项目风险优先级的影响。

## 3. 全生命周期过程流转网络
- **产生过程**：由 [[10.1 制定项目章程]] 首次输出生成。
- **输入/更新过程**：
  - [[11.3 收集需求]]
  - [[11.4 定义范围]]
  - [[11.9 估算活动持续时间]]
  - [[11.12 估算成本]]
  - [[11.19 识别风险]]
  - [[11.20 实施定性风险分析]]
  - [[13.11 监控项目工作]]

---
### 关联概念双链
[[10.1 制定项目章程]], [[项目章程]], [[11.19 识别风险]], [[11.20 实施定性风险分析]]
"""
    },
    {
        "ch_num": 10,
        "filename": "干系人登记册.md",
        "title": "干系人登记册 (Stakeholder Register)",
        "category": "核心交付物/管理文件",
        "section": "10.2 识别干系人",
        "tags": ["第10章", "启动过程组", "干系人管理", "核心输出"],
        "aliases": ["干系人登记册", "Stakeholder Register"],
        "content": """# 干系人登记册 (Stakeholder Register)

## 1. 概念定义与组成信息
干系人登记册是记录已识别干系人的详细信息的文件，主要包括三大类信息：
1. **身份信息**：姓名、组织职位、所在位置、在项目中的角色、联系方式。
2. **评估信息**：主要需求、主要期望、对项目的潜在影响程度、在项目生命周期中最关注的阶段。
3. **干系人分类**：内部/外部、支持者/中立者/反对者、权力/利益矩阵分类、关注重点。

## 2. 全生命周期过程流转网络
- **产生过程**：由 [[10.2 识别干系人]] 主要输出产生，并在项目全生命周期中动态更新。
- **作为输入的后续过程**：
  - [[11.3 收集需求]]
  - [[11.14 规划质量管理]]
  - [[11.17 规划沟通管理]]
  - [[11.18 规划风险管理]]
  - [[11.19 识别风险]]
  - [[11.24 规划干系人参与]]
  - [[12.10 管理干系人参与]]
  - [[13.10 监督干系人参与]]

---
### 关联概念双链
[[10.2 识别干系人]], [[11.24 规划干系人参与]], [[11.17 规划沟通管理]], [[12.10 管理干系人参与]]
"""
    },
    # Chapter 11
    {
        "ch_num": 11,
        "filename": "项目管理计划.md",
        "title": "项目管理计划 (Project Management Plan)",
        "category": "核心交付物/综合基准",
        "section": "11.1 制订项目管理计划",
        "tags": ["第11章", "规划过程组", "整合管理", "基准集成"],
        "aliases": ["项目管理计划", "Project Management Plan"],
        "content": """# 项目管理计划 (Project Management Plan)

## 1. 概念定义与特征
项目管理计划是定义、准备和协调所有计划组件，并把它们整合为一份综合项目管理计划的过程产物。
- **综合性与正式性**：是指导项目执行、监控和收尾的总纲领文件，必须经 **CCB 或主要干系人正式审批签署**。
- **基准变更控制**：项目管理计划一旦被批准确立为基准，后续任何修改必须走 [[13.12 实施整体变更控制]] 程序。

## 2. 组成结构 (10大子计划 + 3大基线)
1. **10大子管理计划**：
   - [[11.2 规划范围管理|范围管理计划]]、需求管理计划、[[11.6 规划进度管理|进度管理计划]]、[[11.11 规划成本管理|成本管理计划]]、[[11.14 规划质量管理|质量管理计划]]、[[11.15 规划资源管理|资源管理计划]]、[[11.17 规划沟通管理|沟通管理计划]]、[[11.18 规划风险管理|风险管理计划]]、[[11.23 规划采购管理|采购管理计划]]、[[11.24 规划干系人参与|干系人参与计划]]。
2. **3大核心基准 (性能测量基准 PMB)**：
   - [[范围基准]] (范围说明书 + WBS + WBS字典)
   - [[进度基准]]
   - [[成本基准]]
3. **其他组件**：变更管理计划、配置管理计划、绩效测量基准、项目生命周期描述、开发方法等。

---
### 关联概念双链
[[11.1 制订项目管理计划]], [[12.1 指导与管理项目工作]], [[13.11 监控项目工作]], [[13.12 实施整体变更控制]], [[范围基准]], [[进度基准]], [[成本基准]]
"""
    },
    {
        "ch_num": 11,
        "filename": "WBS与WBS字典.md",
        "title": "WBS与WBS字典 (Work Breakdown Structure & Dictionary)",
        "category": "核心交付物/范围管理",
        "section": "11.5 创建WBS",
        "tags": ["第11章", "规划过程组", "范围基准", "核心考点"],
        "aliases": ["WBS", "工作分解结构", "WBS字典", "工作包"],
        "content": """# WBS与WBS字典 (Work Breakdown Structure & Dictionary)

## 1. WBS 核心概念与分解原则
**工作分解结构 (WBS)** 是把项目可交付成果和项目工作分解成较小、更易于管理的组件的过程。
- **100% 原则 (包含全部工作)**：WBS 必须包含项目团队要完成的全部工作，不能遗漏也不能超出范围（防镀金）。
- **工作包 (Work Package)**：WBS 的最底层组件，具有可独立估算成本和工期、可分配给专人负责的特点。通常符合 **8/80 小时原则**。
- **控制账户 (Control Account)**：高层管理控制点，把范围、预算、实际成本和进度整合在一起，并与挣值相比较。每个工作包只能属于一个控制账户。

## 2. WBS字典 (WBS Dictionary)
WBS 字典是详细描述 WBS 中每个组件（特别是工作包）的文件，内容包括：
1. 账户编码标识；
2. 工作描述；
3. 假设条件和制约因素；
4. 负责的组织/人员；
5. 里程碑清单；
6. 相关的进度活动；
7. 所需资源和成本估算；
8. 质量要求与验收标准；
9. 技术参考文献与合同信息。

## 3. 范围基准的构成
$$
范围基准 (Scope Baseline) = 项目范围说明书 + WBS + WBS字典
$$

---
### 关联概念双链
[[11.5 创建WBS]], [[11.4 定义范围]], [[11.7 定义活动]], [[13.2 确认范围]], [[13.3 控制范围]], [[范围基准]]
"""
    },
    {
        "ch_num": 11,
        "filename": "范围基准.md",
        "title": "范围基准 (Scope Baseline)",
        "category": "核心交付物/范围管理",
        "section": "11.5 创建WBS",
        "tags": ["第11章", "规划过程组", "范围基准", "基准管理"],
        "aliases": ["范围基准", "Scope Baseline"],
        "content": """# 范围基准 (Scope Baseline)

## 1. 范围基准的三个核心组成
$$
范围基准 = 项目范围说明书 + WBS + WBS字典
$$
- **项目范围说明书**：包含产品范围、项目范围、可交付成果、验收标准、除外责任和制约假设。
- **WBS**：层次化的工作分解结构，定义了项目的 100% 工作边界。
- **WBS字典**：提供每个工作包的详细技术说明与验收标准。

## 2. 变更控制与流转
- **输出过程**：由 [[11.5 创建WBS]] 输出确立。
- **输入过程**：作为基准输入参与 [[13.2 确认范围]]（客户验收依据）与 [[13.3 控制范围]]（范围防蔓延）。

---
### 关联概念双链
[[11.5 创建WBS]], [[WBS与WBS字典]], [[13.2 确认范围]], [[13.3 控制范围]], [[项目管理计划]]
"""
    },
    {
        "ch_num": 11,
        "filename": "关键路径法(CPM).md",
        "title": "关键路径法 (CPM - Critical Path Method)",
        "category": "核心工具/进度管理",
        "section": "11.10 制订进度计划",
        "tags": ["第11章", "规划过程组", "进度计算", "网络图", "高频必考"],
        "aliases": ["关键路径法", "CPM", "总浮动时间", "自由浮动时间", "网络图计算"],
        "content": """# 关键路径法 (CPM)

## 1. 核心定义
关键路径法是在不考虑任何资源限制的情况下，沿着项目进度网络路径顺推与逆推分析，计算所有活动的最早开始时间(ES)、最早完成时间(EF)、最迟开始时间(LS)和最迟完成时间(LF)，从而确定项目网络中**耗时最长的那条路径（关键路径）**。

## 2. 浮动时间计算公式
- **总浮动时间 (TF, Total Float)**：在不延误项目完工时间的前提下，活动可以推迟的最大时间。
  $$TF = LS - ES = LF - EF$$
  - **关键路径上的活动总浮动时间通常为 0**（或小于等于0）。
- **自由浮动时间 (FF, Free Float)**：在不延误任何紧后活动最早开始时间的前提下，活动可以推迟的最大时间。
  $$FF = \min(紧后活动 ES) - 本活动 EF$$

## 3. 六标时网络图顺推逆推法则
- **顺推法 (计算 ES & EF，从前向后)**：
  - $ES = \max(所有紧前活动的 EF)$
  - $EF = ES + 工期 - 1$ (或 $EF = ES + 工期$)
- **逆推法 (计算 LF & LS，从后向前)**：
  - $LF = \min(所有紧后活动的 LS)$
  - $LS = LF - 工期 + 1$ (或 $LS = LF - 工期$)

---
### 关联概念双链
[[11.10 制订进度计划]], [[11.8 排列活动顺序]], [[13.4 控制进度]], [[三点估算(PERT)]]
"""
    },
    {
        "ch_num": 11,
        "filename": "三点估算(PERT).md",
        "title": "三点估算与计划评审技术 (PERT)",
        "category": "核心工具/估算技术",
        "section": "11.9 估算活动持续时间",
        "tags": ["第11章", "规划过程组", "数学公式", "工期估算", "必考考点"],
        "aliases": ["三点估算", "PERT", "计划评审技术", "期望工期", "标准差"],
        "content": """# 三点估算与计划评审技术 (PERT)

## 1. 三个估算值定义
- **最可能时间 ($t_m$)**：基于正常条件和资源下完成活动的最可能工期。
- **最乐观时间 ($t_o$)**：基于最好情况和条件下的最短工期。
- **最悲观时间 ($t_p$)**：基于最不利情况和条件下的最长工期。

## 2. 核心计算公式 (基于 $\beta$ 分布)
- **期望工期均值 ($t_e$)**：
  $$t_e = \frac{t_o + 4t_m + t_p}{6}$$
- **标准差 ($\sigma$)**：
  $$\sigma = \frac{t_p - t_o}{6}$$
- **方差 ($\sigma^2$)**：
  $$\sigma^2 = \left(\frac{t_p - t_o}{6}\right)^2$$

## 3. 正态分布完工概率对照表
- $t_e \pm 1\sigma$：完工概率约为 **68.26%**
- $t_e \pm 2\sigma$：完工概率约为 **95.46%**
- $t_e \pm 3\sigma$：完工概率约为 **99.73%**

---
### 关联概念双链
[[11.9 估算活动持续时间]], [[11.10 制订进度计划]], [[关键路径法(CPM)]], [[11.12 估算成本]]
"""
    },
    {
        "ch_num": 11,
        "filename": "合同类型.md",
        "title": "合同类型与风险分配 (Contract Types)",
        "category": "核心概念/采购管理",
        "section": "11.23 规划采购管理",
        "tags": ["第11章", "采购管理", "合同管理", "高频考点"],
        "aliases": ["合同类型", "固定总价合同", "成本补偿合同", "工料合同", "FFP", "CPFF"],
        "content": """# 合同类型与风险分配 (Contract Types)

## 1. 三大主要合同类型对比
| 合同大类 | 主要子类型 | 适用场景与特征 | 买方风险 | 卖方风险 |
| :--- | :--- | :--- | :--- | :--- |
| **总价合同 (Fixed-Price)** | **固定总价 (FFP)**<br>总价加激励费用 (FPIF)<br>总价加经济价格调整 (FP-EPA) | 范围定义非常明确、需求变更少时采用。价格固定。 | **极低** | **极高** (承担超支风险) |
| **成本补偿合同 (Cost-Reimbursable)** | **成本加固定费用 (CPFF)**<br>成本加激励费用 (CPIF)<br>成本加奖励费用 (CPAF) | 范围不明确、存在高度不确定性或研发型项目。支付实际成本加利润。 | **极高** (承担超支风险) | **极低** |
| **工料合同 (Time and Material, T&M)** | 工料合同 | 短期聘用专家、工作量不明确、需快速开工的临时支持。结合总价与成本补偿特征。 | 中等 | 中等 |

## 2. 核心考点
- 范围越清晰明确，越优先选用 **固定总价合同 (FFP)**。
- 范围边界模糊、探索性研发项目，选用 **成本补偿合同 (CPFF/CPIF)**。

---
### 关联概念双链
[[11.23 规划采购管理]], [[12.9 实施采购]], [[13.9 控制采购]], [[协议]]
"""
    },
    # Chapter 12
    {
        "ch_num": 12,
        "filename": "塔克曼团队发展阶段模型.md",
        "title": "塔克曼团队发展阶段模型 (Tuckman Team Stages)",
        "category": "核心理论/资源与团队管理",
        "section": "12.5 建设团队",
        "tags": ["第12章", "资源管理", "团队建设", "高频考点"],
        "aliases": ["塔克曼模型", "团队发展阶段", "形成阶段", "震荡阶段", "规范阶段", "发挥阶段", "解散阶段"],
        "content": """# 塔克曼团队发展阶段模型 (Tuckman Team Stages)

## 1. 团队发展的五个阶段
1. **形成阶段 (Forming)**：团队成员相互认识，了解项目背景和各自职责。倾向于独立工作，不甚开朗。
2. **震荡阶段 (Storming)**：团队开始开展项目工作，不同的工作风格和观点产生冲突与争执。如果不能妥善管理，会影响团队氛围。
3. **规范阶段 (Norming)**：团队成员开始协同工作，调整工作习惯和行为以支持团队，信任逐渐建立。
4. **发挥阶段 (Performing)**：团队组织有序，成员之间配合默契，成为一个高效运转的团队，能够平稳高效解决问题。
5. **解散阶段 (Adjourning)**：项目团队完成所有工作并解散，成员离队，知识归档。

## 2. 管理要点与考点
- 尽管各阶段通常按顺序发生，但团队成员的变动或重大事件可能导致团队退回到早期阶段。
- 项目经理在不同阶段需采用不同的领导风格（形成期指导型 -> 震荡期教练型 -> 规范期支持型 -> 发挥期授权型）。

---
### 关联概念双链
[[12.5 建设团队]], [[12.6 管理团队]], [[冲突管理策略]], [[11.15 规划资源管理]]
"""
    },
    {
        "ch_num": 12,
        "filename": "冲突管理策略.md",
        "title": "冲突管理5大策略 (Conflict Management Techniques)",
        "category": "核心工具/团队管理",
        "section": "12.6 管理团队",
        "tags": ["第12章", "团队管理", "人际技能", "高频考点"],
        "aliases": ["冲突管理", "冲突解决", "合作解决问题", "妥协", "强迫", "撤退"],
        "content": """# 冲突管理 5 大策略

## 1. 五种处理冲突的常用方法
1. **合作/解决问题 (Collaborating / Problem Solving)**：综合考虑多方观点，引导各方达成共识。**这是最理想的双赢 (Win-Win) 策略**。
2. **妥协/调解 (Compromising / Reconciling)**：各退一步，寻找能使各方都在一定程度上满意的解决方案。属于双方都有所让步的双输或中间方案。
3. **缓和/包容 (Smoothing / Accommodating)**：强调一致之处，淡化差异与分歧，维持和谐与关系。属于暂时退让。
4. **强迫/命令 (Forcing / Directing)**：利用权力强行推行自己的观点，牺牲他人的利益。属于赢-输 (Win-Lose) 策略。
5. **撤退/回避 (Withdrawing / Avoiding)**：从实际或潜在冲突中退出，拖延解决冲突或置身事外。

## 2. 冲突来源排名
根据软考与项目管理统计，项目中最常见的冲突来源排名前三为：
1. **项目进度计划 (Schedule)**；
2. **项目优先级 (Priorities)**；
3. **资源分配 (Resources)**。

---
### 关联概念双链
[[12.6 管理团队]], [[12.5 建设团队]], [[塔克曼团队发展阶段模型]]
"""
    },
    # Chapter 13
    {
        "ch_num": 13,
        "filename": "挣值分析(EVM).md",
        "title": "挣值分析与挣值管理 (EVM - Earned Value Management)",
        "category": "核心工具/成本与进度控制",
        "section": "13.5 控制成本",
        "tags": ["第13章", "监控过程组", "计算公式", "必考考点"],
        "aliases": ["挣值分析", "挣值管理", "EVM", "Earned Value Management"],
        "content": """# 挣值分析与挣值管理 (EVM)

## 1. 三大基本参数
- **计划价值 (PV, Planned Value)**：截至某时间点，计划完成工作的预算成本。
- **挣值 (EV, Earned Value)**：截至某时间点，实际已完成工作的预算成本。
- **实际成本 (AC, Actual Cost)**：截至某时间点，完成已做工作所发生的实际总成本。
- **完工预算 (BAC, Budget At Completion)**：整个项目的总预算。

## 2. 偏差与绩效指标公式
| 指标名称 | 计算公式 | 判断标准 | 状态解读 |
| :--- | :--- | :--- | :--- |
| **成本偏差 (CV)** | $CV = EV - AC$ | $CV > 0$ 结余；$CV < 0$ 超支 | $CV=0$ 成本符合计划 |
| **进度偏差 (SV)** | $SV = EV - PV$ | $SV > 0$ 提前；$SV < 0$ 滞后 | $SV=0$ 进度符合计划 |
| **成本绩效指数 (CPI)** | $CPI = EV / AC$ | $CPI > 1$ 资金利用高效；$CPI < 1$ 超支 | 每花费 1 元产生的挣值 |
| **进度绩效指数 (SPI)** | $SPI = EV / PV$ | $SPI > 1$ 进度提前；$SPI < 1$ 滞后 | 实际进度相对计划的效率 |

## 3. 完工预测公式 (EAC & ETC)
1. **典型偏差 (未来绩效保持当前 CPI)**：
   $$EAC = BAC / CPI$$
   $$ETC = EAC - AC = (BAC - EV) / CPI$$
2. **非典型偏差 (未来工作按原计划预算执行)**：
   $$EAC = AC + (BAC - EV)$$
   $$ETC = BAC - EV$$
3. **完工偏差 (VAC)**：
   $$VAC = BAC - EAC$$
4. **完工尚需绩效指数 (TCPI)**：
   - 基于 BAC：$TCPI = (BAC - EV) / (BAC - AC)$
   - 基于 EAC：$TCPI = (BAC - EV) / (EAC - AC)$

---
### 关联概念双链
[[13.5 控制成本]], [[13.4 控制进度]], [[11.13 制定预算]], [[13.11 监控项目工作]]
"""
    },
    {
        "ch_num": 13,
        "filename": "绩效数据三阶流转模型.md",
        "title": "绩效数据三阶流转模型 (Data -> Information -> Reports)",
        "category": "核心机制/整合监控",
        "section": "13.11 监控项目工作",
        "tags": ["第13章", "项目整合管理", "核心概念", "高频考点"],
        "aliases": ["工作绩效数据", "工作绩效信息", "工作绩效报告", "绩效流转模型"],
        "content": """# 绩效数据三阶流转模型

## 1. 三阶演进定义与流转关系
项目执行中的绩效数据遵循严格的“**产生 -> 整合分析 -> 汇编决策**”的三阶流转机制：

```
┌─────────────────────────────────┐
│ 1. 工作绩效数据 (Work Performance Data) │
│    - 来源：[[12.1 指导与管理项目工作]] (执行产生)│
│    - 特征：原始观察结果与测量值 (实际成本、工时、完成百分比)│
└────────────────┬────────────────┘
                 │ 传递给各控制过程 (控制范围/进度/成本/质量等)
                 ▼
┌─────────────────────────────────┐
│ 2. 工作绩效信息 (Work Performance Info) │
│    - 来源：各领域控制过程 (13.1~13.10)   │
│    - 特征：与基准对比分析后的状态与偏差 (CV/SV/CPI/SPI/预测) │
└────────────────┬────────────────┘
                 │ 汇集输入到整体监控
                 ▼
┌─────────────────────────────────┐
│ 3. 工作绩效报告 (Work Performance Reports)│
│    - 来源：[[13.11 监控项目工作]] (整体整合)│
│    - 特征：汇编成图表/报告，用于分发沟通与 [[13.12 实施整体变更控制]]│
└─────────────────────────────────┘
```

## 2. 核心考点辨析
- **工作绩效数据**：只有执行过程组的 `12.1 指导与管理项目工作` 能够输出！
- **工作绩效信息**：由各具体的控制过程（控制范围、进度、成本、质量等）输出！
- **工作绩效报告**：只有 `13.11 监控项目工作` 能够输出！

---
### 关联概念双链
[[12.1 指导与管理项目工作]], [[13.11 监控项目工作]], [[13.12 实施整体变更控制]], [[12.7 管理沟通]]
"""
    },
    {
        "ch_num": 13,
        "filename": "变更控制委员会(CCB).md",
        "title": "变更控制委员会 (CCB - Change Control Board)",
        "category": "核心组织/变更管理",
        "section": "13.12 实施整体变更控制",
        "tags": ["第13章", "变更控制", "CCB", "决策机构", "高频考点"],
        "aliases": ["变更控制委员会", "CCB", "Change Control Board"],
        "content": """# 变更控制委员会 (CCB)

## 1. 概念定义与组织定位
**变更控制委员会 (CCB)** 是一个正式成立的干系人代表机构，负责审查、评价、批准、推迟或否决项目变更，以及记录和传达变更处理决定。
- **决策机构**：CCB 是项目变更的**最终决策机构**，不是作业机构。
- **成员组成**：通常包括项目发起人、客户代表、项目经理、技术专家、质量代表、配置管理员等。

## 2. 项目经理在 CCB 中的角色
- 项目经理是 CCB 的成员之一，但**项目经理不等于 CCB**。
- 项目经理可以审批某些**不影响项目基准的小范围内部变更**（根据项目章程和授权级别），但涉及项目三大基线（范围、进度、成本）的重大变更必须提交 CCB 审批。

## 3. 标准变更工作程序
1. 提出变更申请；
2. 对变更进行初审；
3. 变更影响综合分析（论证）；
4. **CCB 审查并做出审批决定**；
5. 发出变更通知并开始实施；
6. 监控变更实施过程；
7. 变更效果评估与配置库基准更新。

---
### 关联概念双链
[[13.12 实施整体变更控制]], [[15.3.3 变更管理工作程序]], [[15.2.2 配置管理角色与职责]], [[项目管理计划]]
"""
    },
    # Chapter 15
    {
        "ch_num": 15,
        "filename": "配置项与配置基线.md",
        "title": "配置项与配置基线 (CI & Baseline)",
        "category": "核心概念/组织保障",
        "section": "15.2 配置管理",
        "tags": ["第15章", "配置管理", "配置项", "配置基线", "高频考点"],
        "aliases": ["配置项", "CI", "配置基线", "基线配置项", "受控配置项"],
        "content": """# 配置项与配置基线 (CI & Baseline)

## 1. 配置项 (CI, Configuration Item)
凡是为配置管理所识别和控制的软硬件、文档等工作成果，都称为配置项。
- **分类**：
  1. **基线配置项**：经评审通过的正式技术文档和软件成果（如需求规格说明书、设计文档、发布源码）。
  2. **非基线配置项**：草稿文档、临时测试脚本等。
- **版本号规则**：
  - **草稿状态 (Draft)**：`0.YZ`（如 `0.1`, `0.2`）
  - **正式状态 (Released)**：`X.Y`（如 `1.0`, `1.1`）
  - **修改状态 (Changing)**：`X.YZ`（如 `1.01`, `1.12`）

## 2. 三大配置基线
1. **功能基线 (Functional Baseline)**：经评审批准的系统规格说明或需求规格说明。
2. **指派基线 (Allocated Baseline)**：经评审批准的软件/硬件架构设计规格说明。
3. **产品基线 (Product Baseline)**：经全面测试和验收通过的完整交付系统和用户手册。

## 3. 三大配置库 (三库管理)
- **开发库 (Development Library)**：开发人员存放草稿和动态修改的工作区。
- **受控库 (Controlled Library)**：存放已通过评审的基线配置项，修改必须走变更流程。
- **产品库 (Product Library)**：存放准备交付客户或已发行的最终产品版本。

---
### 关联概念双链
[[15.2.1 配置管理基本概念]], [[15.2.4 配置管理活动]], [[变更控制委员会(CCB)]], [[13.12 实施整体变更控制]]
"""
    }
]

CORE_ENTITIES = [
    # Artifacts & Documents
    "项目章程", "立项管理文件", "商业论证", "可行性研究报告", "假设日志", "协议",
    "项目管理计划", "范围管理计划", "需求管理计划", "需求文件", "需求跟踪矩阵",
    "范围说明书", "项目范围说明书", "WBS", "WBS字典", "范围基准",
    "进度管理计划", "活动清单", "活动属性", "里程碑清单", "项目进度网络图", "进度基准", "项目进度计划", "进度数据",
    "成本管理计划", "成本估算", "成本基准", "项目资金需求",
    "质量管理计划", "质量测量指标", "质量审计",
    "资源管理计划", "团队章程", "资源分解结构", "责任分配矩阵", "RACI矩阵",
    "沟通管理计划", "干系人登记册", "干系人参与计划", "干系人参与度评估矩阵",
    "风险管理计划", "风险登记册", "风险报告", "风险分解结构", "概率和影响矩阵",
    "采购管理计划", "采购策略", "采购工作说明书", "招标文件", "合同类型", "固定总价合同", "成本补偿合同", "工料合同",
    "可交付成果", "核实的可交付成果", "验收的可交付成果", "最终产品、服务或成果", "项目最终报告",
    "工作绩效数据", "工作绩效信息", "工作绩效报告", "绩效数据三阶流转模型",
    "变更请求", "变更日志", "批准的变更请求", "问题日志", "经验教训登记册",
    "配置项", "配置基线", "配置库", "配置管理数据库", "配置状态报告", "配置控制委员会", "CCB", "变更控制委员会",
    # Tools & Techniques
    "专家判断", "德尔菲技术", "头脑风暴", "焦点小组", "访谈", "标杆对照", "原型法",
    "因果图", "鱼骨图", "流程图", "帕累托图", "排列图", "直方图", "控制图", "散点图", "亲和图", "思维导图",
    "紧前关系绘图法", "单代号网络图", "箭线图法", "双代号网络图", "提前量和滞后量",
    "类比估算", "参数估算", "三点估算", "PERT", "自下而上估算",
    "关键路径法", "CPM", "关键链法", "资源平衡", "资源平滑", "赶工", "快速跟进",
    "挣值分析", "EVM", "挣值管理", "偏差分析", "趋势分析", "储备分析",
    "决策树分析", "敏感性分析", "蒙特卡洛模拟",
    "冲突管理", "塔克曼团队发展阶段模型", "马斯洛需求层次理论", "双因素理论", "期望理论",
    # Concepts & Tech
    "信息传输模型", "香农公式", "信息的特征", "信息的质量", "信息系统生命周期", "国家信息化体系",
    "新型基础设施建设", "新基建", "工业互联网", "城市物联网", "数字经济", "数字中国", "数字化转型", "元宇宙",
    "OSI七层模型", "TCP_IP协议", "网络存储", "DAS", "NAS", "SAN", "等保2.0", "网络安全法", "数据安全法",
    "云计算", "IaaS", "PaaS", "SaaS", "大数据", "区块链", "人工智能", "虚拟现实",
    "IT服务生命周期", "ITSS", "软件生命周期", "CMMI", "数据治理", "元数据", "数据仓库", "数据资产",
    "系统集成", "信创", "组织结构类型", "项目生命周期", "监理四控三管一协调", "民法典合同编"
]

def auto_wikilink_text(text, current_title=""):
    sorted_entities = sorted(CORE_ENTITIES, key=lambda x: len(x), reverse=True)
    for ent in sorted_entities:
        if ent == current_title or len(ent) < 2:
            continue
        pattern = re.compile(rf'(?<!\[\[)(?<![\w\u4e00-\u9fa5]){re.escape(ent)}(?!\]\])(?![\w\u4e00-\u9fa5])')
        text = pattern.sub(f'[[{ent}]]', text, count=3)
    return text

def build():
    ensure_dir(GRAPH_DIR)
    
    raw_files = sorted(glob.glob(os.path.join(RAW_DIR, "系统集成项目管理工程师教程-第三版-第*章 *.md")),
                        key=lambda x: int(re.search(r"第(\d+)章", os.path.basename(x)).group(1)))
    
    print(f"Found {len(raw_files)} raw chapter files.")
    
    all_nodes_data = []
    chapter_mocs = []
    
    for rf in raw_files:
        fname = os.path.basename(rf)
        match = re.search(r"第(\d+)章\s*(.*)\.md", fname)
        if not match:
            continue
        ch_num = int(match.group(1))
        ch_title = match.group(2).strip()
        full_ch_name = f"第{ch_num}章 {ch_title}"
        ch_dir_name = f"第{ch_num:02d}章-{sanitize_filename(ch_title)}"
        ch_dir_path = os.path.join(GRAPH_DIR, ch_dir_name)
        
        with open(rf, 'r', encoding='utf-8') as f:
            raw_text = f.read()
            
        raw_text = clean_text_images(raw_text)
        raw_text = re.sub(r'#+\s*1120\s+实施定性风险分析', '# 11.20 实施定性风险分析', raw_text)
        
        lines = raw_text.splitlines()
        
        print(f"Processing {full_ch_name}...")
        
        is_process_group = ch_num in [10, 11, 12, 13, 14]
        node_spans = []
        
        for idx, line in enumerate(lines):
            line_s = line.strip()
            
            if line_s.startswith("# 系统集成") or (line_s.startswith("# 第") and "章" in line_s):
                continue
                
            if re.search(r'本章练习|选择题|思考题', line_s):
                continue
                
            m2 = re.match(r'^#+\s*(\d+\.\d+)\s+(.*)', line_s)
            m3 = re.match(r'^#+\s*(\d+\.\d+\.\d+)\s+(.*)', line_s)
            
            if is_process_group:
                if m2:
                    code = m2.group(1)
                    title = m2.group(2).strip()
                    if not code.startswith(f"{ch_num}."):
                        continue
                    if '本章练习' in title:
                        continue
                    if any(k in title for k in ['主要输入', '主要输人', '主要输出', '主要工具与技术']):
                        continue
                    cat = "项目管理过程" if not ("重点工作" in title or "概述" in title) else "过程组重点工作"
                    node_spans.append({
                        "code": code,
                        "title": title,
                        "line_idx": idx,
                        "category": cat
                    })
                elif m3:
                    code = m3.group(1)
                    title = m3.group(2).strip()
                    if not code.startswith(f"{ch_num}."):
                        continue
                    if any(k in title for k in ['主要输入', '主要输人', '主要输出', '主要工具与技术']):
                        continue
                    if '本章练习' in title:
                        continue
                    if (ch_num == 10 and code.startswith("10.3.")) or (ch_num == 14 and code.startswith("14.2.")):
                        node_spans.append({
                            "code": code,
                            "title": title,
                            "line_idx": idx,
                            "category": "过程组重点工作"
                        })
            else:
                if m3:
                    code = m3.group(1)
                    title = m3.group(2).strip()
                    if '本章练习' in title:
                        continue
                    if ch_num == 15 and code in CH15_CUSTOM_TITLES:
                        title = CH15_CUSTOM_TITLES[code]
                    node_spans.append({
                        "code": code,
                        "title": title,
                        "line_idx": idx,
                        "category": "核心概念/技术"
                    })
                elif m2:
                    code = m2.group(1)
                    title = m2.group(2).strip()
                    if '本章练习' in title:
                        continue
                    node_spans.append({
                        "code": code,
                        "title": title,
                        "line_idx": idx,
                        "category": "知识专题"
                    })

        if not is_process_group:
            filtered_spans = []
            m3_parent_prefixes = set()
            for s in node_spans:
                parts = s["code"].split('.')
                if len(parts) == 3:
                    m3_parent_prefixes.add(f"{parts[0]}.{parts[1]}")
            
            for s in node_spans:
                parts = s["code"].split('.')
                if len(parts) == 2 and s["code"] in m3_parent_prefixes:
                    continue
                filtered_spans.append(s)
            node_spans = filtered_spans

        node_spans.sort(key=lambda x: x["line_idx"])
        
        ch_nodes = []
        for i, span in enumerate(node_spans):
            start_line = span["line_idx"]
            end_line = node_spans[i+1]["line_idx"] if i+1 < len(node_spans) else len(lines)
            
            for check_idx in range(start_line, end_line):
                if re.search(r'#+\s*(\d+\.\d+|\d+\.\d+\.\d+)?\s*本章练习', lines[check_idx]):
                    end_line = check_idx
                    break
                    
            chunk_lines = lines[start_line:end_line]
            chunk_text = "\n".join(chunk_lines).strip()
            
            if len(chunk_text) > 50:
                ch_nodes.append({
                    "code": span["code"],
                    "title": span["title"],
                    "category": span["category"],
                    "raw_text": chunk_text
                })
                
        ensure_dir(ch_dir_path)
        moc_entries = []
        
        for node in ch_nodes:
            raw_title = node["title"]
            clean_node_title = sanitize_filename(raw_title)
            clean_node_name = f"{node['code']} {clean_node_title}" if not clean_node_title.startswith(node['code']) else clean_node_title
            clean_node_name = sanitize_filename(clean_node_name)
            
            node_filename = f"{clean_node_name}.md"
            node_filepath = os.path.join(ch_dir_path, node_filename)
            
            tags = [f"第{ch_num}章", ch_title, node["category"]]
            aliases = [raw_title, f"{node['code']} {raw_title}"]
            
            frontmatter = f"""---
title: "{node['code']} {raw_title}"
chapter: "{full_ch_name}"
section: "{node['code']} {raw_title}"
category: "{node['category']}"
tags: {json.dumps(tags, ensure_ascii=False)}
aliases: {json.dumps(aliases, ensure_ascii=False)}
---

> **所属章节**：[[第{ch_num:02d}章-{sanitize_filename(ch_title)}/第{ch_num}章-知识总览|{full_ch_name}]] > {node['code']} {raw_title}

"""
            body_content = auto_wikilink_text(node["raw_text"], raw_title)
            full_content = frontmatter + body_content + "\n"
            
            with open(node_filepath, 'w', encoding='utf-8') as nf:
                nf.write(full_content)
                
            summary_snippet = re.sub(r'#+\s*', '', node["raw_text"][:260]).replace('\n', ' ').strip()
            rel_file_path = f"graph/{ch_dir_name}/{node_filename}"
            
            node_index_entry = {
                "title": f"{node['code']} {raw_title}",
                "clean_title": raw_title,
                "chapter": full_ch_name,
                "chapter_num": ch_num,
                "section": f"{node['code']} {raw_title}",
                "category": node["category"],
                "file_path": rel_file_path,
                "tags": tags,
                "summary": summary_snippet
            }
            all_nodes_data.append(node_index_entry)
            moc_entries.append((node['code'], raw_title, clean_node_name, node["category"]))
            
        # Append dedicated entity nodes for this chapter
        for ent in CORE_DEDICATED_ENTITIES:
            if ent["ch_num"] == ch_num:
                ent_filename = ent["filename"]
                ent_filepath = os.path.join(ch_dir_path, ent_filename)
                
                ent_frontmatter = f"""---
title: "{ent['title']}"
chapter: "{full_ch_name}"
section: "{ent['section']}"
category: "{ent['category']}"
tags: {json.dumps(ent['tags'], ensure_ascii=False)}
aliases: {json.dumps(ent['aliases'], ensure_ascii=False)}
---

> **所属章节**：[[第{ch_num:02d}章-{sanitize_filename(ch_title)}/第{ch_num}章-知识总览|{full_ch_name}]] > {ent['section']}

"""
                ent_full_content = ent_frontmatter + ent["content"] + "\n"
                with open(ent_filepath, 'w', encoding='utf-8') as ef:
                    ef.write(ent_full_content)
                    
                ent_summary = re.sub(r'#+\s*', '', ent["content"][:260]).replace('\n', ' ').strip()
                ent_rel_path = f"graph/{ch_dir_name}/{ent_filename}"
                
                all_nodes_data.append({
                    "title": ent["title"],
                    "clean_title": ent["filename"][:-3],
                    "chapter": full_ch_name,
                    "chapter_num": ch_num,
                    "section": ent["section"],
                    "category": ent["category"],
                    "file_path": ent_rel_path,
                    "tags": ent["tags"],
                    "summary": ent_summary
                })
                moc_entries.append(("核心实体", ent["filename"][:-3], ent["filename"][:-3], ent["category"]))
            
        moc_filename = f"第{ch_num}章-知识总览.md"
        moc_filepath = os.path.join(ch_dir_path, moc_filename)
        
        moc_content = f"""---
title: "{full_ch_name} - 知识总览"
type: "Chapter MOC"
chapter: "{full_ch_name}"
---

# {full_ch_name} 知识总览导引

> **上级地图**：[[INDEX|全局知识图谱总目录]]

## 本章核心知识节点列表（共 {len(moc_entries)} 个）

"""
        for code, title, clean_name, cat in moc_entries:
            moc_content += f"- **[[{clean_name}|{title}]]** `[{cat}]`\n"
            
        with open(moc_filepath, 'w', encoding='utf-8') as mf:
            mf.write(moc_content)
            
        chapter_mocs.append({
            "ch_num": ch_num,
            "full_name": full_ch_name,
            "dir_name": ch_dir_name,
            "count": len(moc_entries)
        })

    # Step 2: Write Global INDEX.md
    index_md_path = os.path.join(GRAPH_DIR, "INDEX.md")
    index_md = f"""---
title: "系统集成项目管理工程师（第三版）- 全局双链知识图谱总览"
type: "Global MOC"
---

# 《系统集成项目管理工程师教程（第三版）》知识图谱总览

本知识图谱根据全国计算机技术与软件专业技术资格（水平）考试《系统集成项目管理工程师教程（第三版）》重构提炼，包含全书 17 个章节的核心知识专题、49 个项目管理标准过程以及核心管理文件/交付物实体，支持 Obsidian `[[双链]]` 全景互联与 AI 考点溯源检索。

---

## 章节知识导引 (Chapter MOCs)

"""
    for moc in chapter_mocs:
        moc_rel = f"{moc['dir_name']}/第{moc['ch_num']}章-知识总览"
        index_md += f"{moc['ch_num']}. **[[{moc_rel}|{moc['full_name']}]]** （包含 **{moc['count']}** 个高内聚核心知识节点）\n"
        
    index_md += f"""

---

## 核心过程组与知识领域对照矩阵

| 知识领域 \\ 过程组 | 启动过程组 | 规划过程组 | 执行过程组 | 监控过程组 | 收尾过程组 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **项目整合管理** | [[10.1 制定项目章程]] | [[11.1 制订项目管理计划]] | [[12.1 指导与管理项目工作]]<br>[[12.2 管理项目知识]] | [[13.11 监控项目工作]]<br>[[13.12 实施整体变更控制]] | [[14.1 结束项目或阶段]] |
| **项目范围管理** | - | [[11.2 规划范围管理]]<br>[[11.3 收集需求]]<br>[[11.4 定义范围]]<br>[[11.5 创建WBS]] | - | [[13.2 确认范围]]<br>[[13.3 控制范围]] | - |
| **项目进度管理** | - | [[11.6 规划进度管理]]<br>[[11.7 定义活动]]<br>[[11.8 排列活动顺序]]<br>[[11.9 估算活动持续时间]]<br>[[11.10 制订进度计划]] | - | [[13.4 控制进度]] | - |
| **项目成本管理** | - | [[11.11 规划成本管理]]<br>[[11.12 估算成本]]<br>[[11.13 制定预算]] | - | [[13.5 控制成本]] | - |
| **项目质量管理** | - | [[11.14 规划质量管理]] | [[12.3 管理质量]] | [[13.1 控制质量]] | - |
| **项目资源管理** | - | [[11.15 规划资源管理]]<br>[[11.16 估算活动资源]] | [[12.4 获取资源]]<br>[[12.5 建设团队]]<br>[[12.6 管理团队]] | [[13.6 控制资源]] | - |
| **项目沟通管理** | - | [[11.17 规划沟通管理]] | [[12.7 管理沟通]] | [[13.7 监督沟通]] | - |
| **项目风险管理** | - | [[11.18 规划风险管理]]<br>[[11.19 识别风险]]<br>[[11.20 实施定性风险分析]]<br>[[11.21 实施定量风险分析]]<br>[[11.22 规划风险应对]] | [[12.8 实施风险应对]] | [[13.8 监督风险]] | - |
| **项目采购管理** | - | [[11.23 规划采购管理]] | [[12.9 实施采购]] | [[13.9 控制采购]] | - |
| **项目干系人管理** | [[10.2 识别干系人]] | [[11.24 规划干系人参与]] | [[12.10 管理干系人参与]] | [[13.10 监督干系人参与]] | - |

---

## 核心管理文件与实体速查索引
- **启动与立项**：[[项目章程]]、[[立项管理文件]]、[[假设日志]]、[[干系人登记册]]
- **范围与需求**：[[WBS与WBS字典]]、[[范围基准]]、[[项目管理计划]]
- **进度与估算**：[[关键路径法(CPM)]]、[[三点估算(PERT)]]
- **成本与控制**：[[挣值分析(EVM)]]、[[合同类型]]
- **团队与组织**：[[塔克曼团队发展阶段模型]]、[[冲突管理策略]]
- **绩效与变更控制**：[[绩效数据三阶流转模型]]、[[变更控制委员会(CCB)]]、[[配置项与配置基线]]

---

## 统计信息
- **总章节数**：17 章
- **核心知识专题、过程与细粒度实体节点总数**：{len(all_nodes_data)} 个
- **检索接口**：支持调用 `scripts/search_knowledge.py` 或直接检索 `graph/knowledge_index.json`。
"""
    with open(index_md_path, 'w', encoding='utf-8') as imf:
        imf.write(index_md)

    json_index_path = os.path.join(GRAPH_DIR, "knowledge_index.json")
    with open(json_index_path, 'w', encoding='utf-8') as jf:
        json.dump({
            "total_chapters": 17,
            "total_nodes": len(all_nodes_data),
            "nodes": all_nodes_data
        }, jf, ensure_ascii=False, indent=2)

    print("\n" + "="*50)
    print(f"Fine-grained Knowledge Graph rebuilt successfully in {GRAPH_DIR}!")
    print(f"Total Nodes: {len(all_nodes_data)}")
    print(f"Global index written to {json_index_path}")
    print(f"Global MOC written to {index_md_path}")
    print("="*50)

if __name__ == "__main__":
    build()
