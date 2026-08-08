#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zero-dependency Knowledge Graph Search Helper
Searches graph/knowledge_index.json for keywords and returns exact chapter/section mapping and concept node paths.
Pure Python standard library (json, sys, os, re).
"""

import os
import sys
import json
import re

# Determine project directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
INDEX_PATH = os.path.join(PROJECT_DIR, "graph", "knowledge_index.json")

def search_knowledge(query, max_results=5):
    if not os.path.exists(INDEX_PATH):
        print(f"Error: Index file not found at {INDEX_PATH}", file=sys.stderr)
        return []

    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    nodes = data.get("nodes", [])
    query_lower = query.lower().strip()
    keywords = [k for k in re.split(r'\s+', query_lower) if k]

    if not keywords:
        return []

    scored_nodes = []
    for node in nodes:
        title = node.get("title", "").lower()
        chapter = node.get("chapter", "").lower()
        section = node.get("section", "").lower()
        summary = node.get("summary", "").lower()
        tags = [t.lower() for t in node.get("tags", [])]

        score = 0
        for kw in keywords:
            if kw == title:
                score += 100
            elif kw in title:
                score += 50
            if any(kw in t for t in tags):
                score += 30
            if kw in section:
                score += 20
            if kw in chapter:
                score += 15
            if kw in summary:
                score += 10

        if score > 0:
            scored_nodes.append((score, node))

    # Sort by score descending
    scored_nodes.sort(key=lambda x: x[0], reverse=True)
    results = [node for score, node in scored_nodes[:max_results]]
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python search_knowledge.py <keyword1> [keyword2 ...]")
        print("Example: python search_knowledge.py 挣值分析")
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
