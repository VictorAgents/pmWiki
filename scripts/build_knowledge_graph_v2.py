#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
High-Cohesion Semantic Knowledge Graph Builder for System Integration Project Management Engineer (3rd Edition)
Extracts self-contained, structured concept and process nodes from raw/ files.
Filters out noise (主要输入/主要输出/本章练习/选择题) and merges them into complete, rich nodes.
"""

import os
import sys
import glob
import re
import json

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

def build_graph():
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
        
        # Pre-fix OCR typos
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
                    # Only accept processes belonging to current chapter e.g. 11.1 - 11.24
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
                    # Only accept focus work sub-items like 10.3.1, 10.3.2, 14.2.1, 14.2.2, 14.2.3
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
                
        print(f"  Extracted {len(ch_nodes)} high-cohesion nodes for {full_ch_name}")
        
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
            body_content = node["raw_text"]
            full_content = frontmatter + body_content + "\n"
            
            with open(node_filepath, 'w', encoding='utf-8') as nf:
                nf.write(full_content)
                
            summary_snippet = re.sub(r'#+\s*', '', body_content[:260]).replace('\n', ' ').strip()
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
            moc_content += f"- **[[{clean_name}|{code} {title}]]** `[{cat}]`\n"
            
        with open(moc_filepath, 'w', encoding='utf-8') as mf:
            mf.write(moc_content)
            
        chapter_mocs.append({
            "ch_num": ch_num,
            "full_name": full_ch_name,
            "dir_name": ch_dir_name,
            "count": len(moc_entries)
        })

    index_md_path = os.path.join(GRAPH_DIR, "INDEX.md")
    index_md = f"""---
title: "系统集成项目管理工程师（第三版）- 全局双链知识图谱总览"
type: "Global MOC"
---

# 《系统集成项目管理工程师教程（第三版）》知识图谱总览

本知识图谱根据全国计算机技术与软件专业技术资格（水平）考试《系统集成项目管理工程师教程（第三版）》重构提炼，包含全书 17 个章节的核心知识专题与 49 个项目管理标准过程，去除碎片化冗余，支持 Obsidian `[[双链]]` 关联与 AI 考点溯源检索。

---

## 章节知识导引 (Chapter MOCs)

"""
    for moc in chapter_mocs:
        moc_rel = f"{moc['dir_name']}/第{moc['ch_num']}章-知识总览"
        index_md += f"{moc['ch_num']}. **[[{moc_rel}|{moc['full_name']}]]** （包含 **{moc['count']}** 个高内聚核心知识节点）\n"
        
    index_md += f"""

---

## 统计信息
- **总章节数**：17 章
- **核心知识专题与过程节点总数**：{len(all_nodes_data)} 个
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
    print(f"Knowledge Graph rebuilt successfully in {GRAPH_DIR}!")
    print(f"Total High-Cohesion Nodes: {len(all_nodes_data)}")
    print(f"Global index written to {json_index_path}")
    print(f"Global MOC written to {index_md_path}")
    print("="*50)

if __name__ == "__main__":
    build_graph()
