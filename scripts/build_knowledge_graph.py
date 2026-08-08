import os
import re
import json
import glob
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = BASE_DIR
GRAPH_DIR = os.path.join(PROJECT_DIR, "graph")

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

ensure_dir(GRAPH_DIR)

# Get list of all chapter files
chapter_files = sorted(glob.glob(os.path.join(PROJECT_DIR, "系统集成项目管理工程师教程-第三版-第*章 *.md")), 
                       key=lambda x: int(re.search(r"第(\d+)章", os.path.basename(x)).group(1)))

print(f"Found {len(chapter_files)} chapter files.")

# Store index data for knowledge_index.json
index_data = []

# Collect all concept names across the book for cross-linking
all_concepts_set = set()

# Helper to sanitize filename
def sanitize_filename(name):
    name = re.sub(r'[\\/:*?"<>|]', '_', name)
    return name.strip()

# Step 1: First pass - Parse chapters to discover concepts & build structure
chapters_data = []

for filepath in chapter_files:
    fname = os.path.basename(filepath)
    match = re.search(r"第(\d+)章\s*(.*)\.md", fname)
    if not match:
        continue
    ch_num = int(match.group(1))
    ch_title = match.group(2).strip()
    full_ch_name = f"第{ch_num}章 {ch_title}"
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    ch_dir_name = f"第{ch_num:02d}章-{sanitize_filename(ch_title)}"
    ch_dir_path = os.path.join(GRAPH_DIR, ch_dir_name)
    
    # Parse lines into sections and concepts
    current_sec_code = f"{ch_num}.0"
    current_sec_title = "本章概述"
    current_concept_title = "章节简介"
    
    concepts = [] # list of dicts: {concept_title, sec_code, sec_title, content_lines}
    curr_lines = []
    
    def add_concept(c_title, s_code, s_title, c_lines):
        text = "".join(c_lines).strip()
        if text:
            concepts.append({
                "title": c_title,
                "sec_code": s_code,
                "sec_title": s_title,
                "lines": c_lines,
                "text": text
            })
            all_concepts_set.add(c_title)

    for line in lines:
        line_s = line.strip()
        # Check chapter heading
        if line_s.startswith("# 第") and "章" in line_s:
            continue
        
        # Check section heading e.g. # 1.1 信息与信息化 or ## 1.1 信息与信息化
        sec_match = re.match(r"^#+\s*(\d+\.\d+)\s+(.*)", line_s)
        sub_sec_match = re.match(r"^#+\s*(\d+\.\d+\.\d+)\s+(.*)", line_s)
        concept_match = re.match(r"^#+\s*(\d+[\.\)]|\d+\))\s*(.*)", line_s)
        
        if sub_sec_match:
            # Save previous concept
            add_concept(current_concept_title, current_sec_code, current_sec_title, curr_lines)
            curr_lines = [line]
            current_sec_code = sub_sec_match.group(1)
            current_sec_title = sub_sec_match.group(2).strip()
            current_concept_title = f"{current_sec_code} {current_sec_title}"
        elif sec_match:
            add_concept(current_concept_title, current_sec_code, current_sec_title, curr_lines)
            curr_lines = [line]
            current_sec_code = sec_match.group(1)
            current_sec_title = sec_match.group(2).strip()
            current_concept_title = f"{current_sec_code} {current_sec_title}"
        elif concept_match and len(line_s) < 50:
            # Sub-concept level e.g. # 1. 信息的定义
            c_name = concept_match.group(2).strip()
            # Remove trailing numbers if any (e.g. "信息基础 2")
            c_name = re.sub(r"\s+\d+$", "", c_name)
            if c_name:
                add_concept(current_concept_title, current_sec_code, current_sec_title, curr_lines)
                curr_lines = [line]
                current_concept_title = c_name
        else:
            curr_lines.append(line)
            
    # Flush remaining
    add_concept(current_concept_title, current_sec_code, current_sec_title, curr_lines)
    
    chapters_data.append({
        "ch_num": ch_num,
        "ch_title": ch_title,
        "full_ch_name": full_ch_name,
        "ch_dir_name": ch_dir_name,
        "ch_dir_path": ch_dir_path,
        "concepts": concepts
    })

print(f"Total unique concept nodes discovered: {len(all_concepts_set)}")

# Step 2: Write Concept Markdown Files with Frontmatter and [[Wikilinks]]
concept_keywords_map = {}

for ch in chapters_data:
    ensure_dir(ch["ch_dir_path"])
    
    # We will create an overview MOC for this chapter
    moc_filename = f"第{ch['ch_num']}章-概览.md"
    moc_filepath = os.path.join(ch["ch_dir_path"], moc_filename)
    
    ch_concepts_links = []
    
    # Group concepts by section for MOC
    sec_groups = defaultdict(list)
    
    for concept in ch["concepts"]:
        raw_title = concept["title"]
        clean_title = sanitize_filename(raw_title)
        if not clean_title or clean_title == "章节简介":
            clean_title = f"第{ch['ch_num']}章-概述"
            
        concept_filename = f"{clean_title}.md"
        concept_filepath = os.path.join(ch["ch_dir_path"], concept_filename)
        
        # Determine tags
        tags = [f"第{ch['ch_num']}章", ch["ch_title"]]
        if concept["sec_title"]:
            tags.append(concept["sec_title"])
            
        # Build YAML Frontmatter
        frontmatter = f"""---
title: "{raw_title}"
chapter: "{ch['full_ch_name']}"
section: "{concept['sec_code']} {concept['sec_title']}"
tags: {json.dumps(tags, ensure_ascii=False)}
aliases: ["{raw_title}"]
---

"""
        # Build Wikilink headers
        breadcrumb = f"> **所属章节**：[[{moc_filename[:-3]}\|{ch['full_ch_name']}]] > {concept['sec_code']} {concept['sec_title']}\n\n"
        
        # Automatic Cross-linking in content: find mentions of other concepts and wrap with [[...]]
        content_text = concept["text"]
        
        # Prepare related concept links
        related_links = []
        for other_c in all_concepts_set:
            if len(other_c) > 2 and other_c != raw_title and other_c in content_text:
                related_links.append(f"[[{sanitize_filename(other_c)}\|{other_c}]]")
                if len(related_links) >= 8: # Cap at 8 related links
                    break
                    
        related_section = ""
        if related_links:
            related_section = f"\n\n---\n### 关联概念双链\n" + ", ".join(related_links) + "\n"
            
        full_node_content = frontmatter + breadcrumb + content_text + related_section
        
        with open(concept_filepath, 'w', encoding='utf-8') as cf:
            cf.write(full_node_content)
            
        # Add to index_data for AI Agent search
        summary_snippet = re.sub(r'#+\s*', '', content_text[:200]).replace('\n', ' ').strip()
        rel_path = os.path.relpath(concept_filepath, GRAPH_DIR).replace('\\', '/')
        
        index_data.append({
            "title": raw_title,
            "chapter": ch['full_ch_name'],
            "chapter_num": ch['ch_num'],
            "section": f"{concept['sec_code']} {concept['sec_title']}",
            "file_path": f"graph/{rel_path}",
            "tags": tags,
            "summary": summary_snippet
        })
        
        sec_key = f"{concept['sec_code']} {concept['sec_title']}"
        sec_groups[sec_key].append(clean_title)
        
    # Write Chapter MOC file
    moc_content = f"""---
title: "{ch['full_ch_name']} - 目录导引"
type: "MOC"
chapter: "{ch['full_ch_name']}"
---

# {ch['full_ch_name']} 知识图谱导引

> **上级地图**：[[INDEX|全局知识图谱总目录]]

## 本章知识节点分类

"""
    for sec_name, concept_titles in sec_groups.items():
        moc_content += f"### {sec_name}\n"
        for ct in concept_titles:
            moc_content += f"- [[{ct}]]\n"
        moc_content += "\n"
        
    with open(moc_filepath, 'w', encoding='utf-8') as mf:
        mf.write(moc_content)

# Step 3: Write Global INDEX.md
index_md_path = os.path.join(GRAPH_DIR, "INDEX.md")
index_md_content = """---
title: "系统集成项目管理工程师（第三版）- 全局双链知识图谱总目录"
type: "Global MOC"
---

# 系统集成项目管理工程师（第三版）知识图谱总览

本知识图谱将全书 17 个章节提炼重构为独立的 **概念级知识节点**，采用 Obsidian 原生 `[[双链]]` 进行交叉关联与层级索引。

---

## 章节知识导引 (Chapter MOCs)

"""

for ch in chapters_data:
    moc_name = f"第{ch['ch_num']}章-概览"
    rel_moc_path = f"第{ch['ch_num']:02d}章-{sanitize_filename(ch['ch_title'])}/{moc_name}"
    index_md_content += f"1. **[[{rel_moc_path}\|{ch['full_ch_name']}]]** ({len(ch['concepts'])} 个核心知识节点)\n"

index_md_content += f"""

---

## 统计信息
- **总章节数**：17 章
- **核心知识点节点数**：{len(index_data)} 个
- **检索接口**：支持直接调取 `graph/knowledge_index.json` 进行关键词与章节准确定位。
"""

with open(index_md_path, 'w', encoding='utf-8') as imf:
    imf.write(index_md_content)

# Step 4: Write Global knowledge_index.json
json_index_path = os.path.join(GRAPH_DIR, "knowledge_index.json")
with open(json_index_path, 'w', encoding='utf-8') as jf:
    json.dump({
        "total_chapters": 17,
        "total_nodes": len(index_data),
        "nodes": index_data
    }, jf, ensure_ascii=False, indent=2)

print(f"Successfully generated Knowledge Graph in {GRAPH_DIR}!")
print(f"Total concept nodes: {len(index_data)}")
print(f"Global index written to {json_index_path}")
