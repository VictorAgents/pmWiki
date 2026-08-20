#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Full-Coverage Fine-Grained Knowledge Graph & Bidirectional Link Master Builder
For System Integration Project Management Engineer (3rd Edition)

Generates:
1. 49 Standard Project Management Process Nodes (with embedded [[wikilinks]])
2. 80+ Fine-Grained ITTO Deliverables, Management Documents, Tools & Techniques
3. 80+ Fine-Grained Technology, Architecture, Engineering, Governance & Law Concepts (Chapters 1-9, 15-17)
4. Comprehensive Global MOC INDEX.md and AI Agent Index knowledge_index.json
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

# Import or define the master entity dictionary
from fine_grained_entities_data import MASTER_DEDICATED_ENTITIES, CORE_WIKILINK_KEYWORDS

# Pre-compile wikilink patterns once at module level for performance
# Filter to keywords >= 3 chars to avoid false-positive matches (e.g. "CI", "CV", "SV")
_SORTED_KW = sorted([kw for kw in CORE_WIKILINK_KEYWORDS if len(kw) >= 3],
                     key=lambda x: len(x), reverse=True)
_COMPILED_PATTERNS = []
for _kw in _SORTED_KW:
    _pat = re.compile(rf'(?<!\[\[)(?<![\w\u4e00-\u9fa5]){re.escape(_kw)}(?!\]\])(?![\w\u4e00-\u9fa5])')
    _COMPILED_PATTERNS.append((_kw, _pat))

def auto_wikilink_text(text, current_title=""):
    for kw, pattern in _COMPILED_PATTERNS:
        if kw == current_title:
            continue
        text = pattern.sub(f'[[{kw}]]', text, count=3)
    return text

def build_full_graph():
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
        for ent in MASTER_DEDICATED_ENTITIES:
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

本知识图谱根据全国计算机技术与软件专业技术资格（水平）考试《系统集成项目管理工程师教程（第三版）》重构提炼，包含全书 17 个章节的核心技术专题、49 个项目管理标准过程以及全量核心管理文件/交付物/工具技术独立实体，支持 Obsidian `[[双链]]` 全景互联与 AI 考点溯源检索。

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
    print(f"Master Fine-grained Knowledge Graph rebuilt successfully in {GRAPH_DIR}!")
    print(f"Total Nodes: {len(all_nodes_data)}")
    print(f"Global index written to {json_index_path}")
    print(f"Global MOC written to {index_md_path}")
    print("="*50)

if __name__ == "__main__":
    build_full_graph()
