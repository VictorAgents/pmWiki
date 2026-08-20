#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Adversarial search test: verify all previously-missing keywords now have hits"""
import sys, json, os
sys.stdout.reconfigure(encoding='utf-8')

# Load the search index
idx = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'graph', 'knowledge_index.json'), 'r', encoding='utf-8'))

CRITICAL_KEYWORDS = [
    # Previously missing baselines
    "进度基准",
    # Previously missing ITTO docs
    "风险登记册", "风险报告", "经验教训登记册", "问题日志", "变更请求", "变更日志",
    "活动清单", "活动属性", "里程碑清单", "项目进度网络图",
    "资源分解结构", "RACI", "团队章程",
    "沟通管理计划", "沟通渠道", "干系人参与计划", "干系人参与度评估矩阵",
    "风险管理计划", "概率和影响矩阵", "采购管理计划", "采购工作说明书",
    "招标文件", "供方选择标准", "可交付成果", "项目最终报告",
    "质量管理计划", "质量测量指标", "资源管理计划", "协议",
    "范围管理计划", "需求文件", "进度管理计划", "成本管理计划",
    # Previously missing tools & techniques
    "赶工", "快速跟进", "关键链法", "资源平衡", "资源平滑",
    "类比估算", "参数估算", "自下而上估算",
    "紧前关系绘图法", "箭线图法", "提前量和滞后量",
    "决策树分析", "EMV", "敏感性分析", "龙卷风图", "蒙特卡洛模拟",
    "储备分析", "风险应对策略",
    "马斯洛需求层次理论", "双因素理论", "期望理论", "XY理论",
    "德尔菲技术", "头脑风暴", "专家判断",
    "配置审计",
    # Previously missing Ch1-9 concepts
    "信息系统生命周期", "新基建", "数字经济",
    "元宇宙", "大数据5V", "区块链", "人工智能",
    "PPTR", "IT服务生命周期", "ITSS",
    "TOGAF", "云原生架构", "安全架构",
    "QFD", "UML", "软件测试",
    "数据模型", "数据质量", "数据仓库",
    "系统集成", "企业应用集成", "ISMS",
    "人才三角",
    # Previously missing Ch15-17 concepts  
    "监理五大阶段", "监理三大核心文件", "监理技术参考模型",
    "知识产权法", "民法典", "网络安全法", "数据安全法",
    "国标编号",
]

hits = 0
misses = 0
miss_list = []

for kw in CRITICAL_KEYWORDS:
    found = False
    kw_lower = kw.lower()
    for node in idx['nodes']:
        searchable = (node.get('title','') + ' ' + node.get('summary','') + ' ' + ' '.join(node.get('tags',[])) + ' ' + ' '.join(node.get('aliases', []) if isinstance(node.get('aliases'), list) else [])).lower()
        if kw_lower in searchable:
            found = True
            break
    if found:
        hits += 1
    else:
        misses += 1
        miss_list.append(kw)

print(f"=== ADVERSARIAL SEARCH TEST RESULTS ===")
print(f"Total keywords tested: {len(CRITICAL_KEYWORDS)}")
print(f"HITS:   {hits} ({100*hits/len(CRITICAL_KEYWORDS):.1f}%)")
print(f"MISSES: {misses} ({100*misses/len(CRITICAL_KEYWORDS):.1f}%)")
if miss_list:
    print(f"\nStill missing:")
    for m in miss_list:
        print(f"  ❌ {m}")
else:
    print(f"\n✅ ALL KEYWORDS HIT - ZERO MISSES!")
