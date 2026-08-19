#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zero-dependency High-Precision Knowledge Graph Search Helper
Searches graph/knowledge_index.json and graph/ markdown files for concepts, processes, formulas, and topics.
Pure Python standard library (json, sys, os, re).
"""

import os
import sys
import json
import re

# Ensure standard output uses utf-8 on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
INDEX_PATH = os.path.join(PROJECT_DIR, "graph", "knowledge_index.json")

def search_knowledge(query, max_results=5, deep_search=True):
    if not os.path.exists(INDEX_PATH):
        print(f"Error: Index file not found at {INDEX_PATH}", file=sys.stderr)
        return []

    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    nodes = data.get("nodes", [])
    query_clean = query.strip()
    if not query_clean:
        return []

    # Generate keywords: full phrase, plus segmented sub-tokens
    keywords = [k for k in re.split(r'[\s,，、_—\(\)（）]+', query_clean) if k]
    if len(query_clean) >= 4 and query_clean not in keywords:
        keywords.insert(0, query_clean)

    scored_nodes = []
    
    for node in nodes:
        title = node.get("title", "")
        clean_title = node.get("clean_title", "")
        chapter = node.get("chapter", "")
        section = node.get("section", "")
        summary = node.get("summary", "")
        tags = node.get("tags", [])
        file_rel = node.get("file_path", "")
        
        score = 0
        
        # 1. Exact phrase matches
        if query_clean in title or query_clean in clean_title:
            score += 200
        if query_clean in section:
            score += 150
        if query_clean in summary:
            score += 80

        # 2. Token matches
        for kw in keywords:
            kw_l = kw.lower()
            if kw_l == title.lower() or kw_l == clean_title.lower():
                score += 100
            elif kw_l in title.lower() or kw_l in clean_title.lower():
                score += 50
            if any(kw_l in t.lower() for t in tags):
                score += 30
            if kw_l in section.lower():
                score += 25
            if kw_l in chapter.lower():
                score += 15
            if kw_l in summary.lower():
                score += 10

        # 3. Optional Deep Search in markdown body if score is low but query exists in file content
        if deep_search and score < 50:
            full_file_path = os.path.join(PROJECT_DIR, file_rel.replace('/', os.sep))
            if os.path.exists(full_file_path):
                try:
                    with open(full_file_path, 'r', encoding='utf-8') as fp:
                        body = fp.read()
                    if query_clean in body:
                        score += 70
                    else:
                        match_count = sum(1 for kw in keywords if kw in body)
                        if match_count > 0:
                            score += match_count * 15
                except Exception:
                    pass

        if score > 0:
            scored_nodes.append((score, node))

    scored_nodes.sort(key=lambda x: x[0], reverse=True)
    results = [node for score, node in scored_nodes[:max_results]]
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python search_knowledge.py <keyword1> [keyword2 ...]")
        print("Example: python search_knowledge.py 信息的特征")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    results = search_knowledge(query)

    output = {
        "query": query,
        "total_matches": len(results),
        "results": results
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
