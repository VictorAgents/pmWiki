---
title: "计算机网络体系与 OSI/TCP-IP 模型 (Network Architecture)"
chapter: "第2章 信息技术发展"
section: "2.1.2 计算机网络"
category: "计算机网络/网络体系"
tags: ["第2章", "计算机网络", "OSI七层模型", "TCP/IP", "核心基础"]
aliases: ["OSI七层模型", "TCP/IP模型", "网络协议", "IP地址", "MAC地址"]
---

> **所属章节**：[[第02章-信息技术发展/第2章-知识总览|第2章 信息技术发展]] > 2.1.2 计算机网络

# 计算机网络体系与 OSI / TCP-IP 模型

## 1. OSI 七层参考模型 vs TCP/IP 四层模型对照表
| OSI 7层参考模型 | 数据单元 (PDU) | TCP/IP 4层体系 | 典型协议与标准 | 主要网络设备 |
| :--- | :--- | :--- | :--- | :--- |
| **应用层 (Application)** | APDU | **应用层** | HTTP, HTTPS, FTP, DNS, SMTP, SNMP, DHCP | 网关 (Gateway) |
| **表示层 (Presentation)** | PPDU | 编码解码、加密解密 (ASCII, JPEG, SSL/TLS) | - |
| **会话层 (Session)** | SPDU | 会话建立与管理 (RPC, NetBIOS) | - |
| **传输层 (Transport)** | 段 (Segment) | **传输层** | **TCP** (可靠面向连接), **UDP** (不可靠无连接) | 负载均衡器、四层交换机 |
| **网络层 (Network)** | 包 (Packet) | **网络层 (网际层)** | **IP, ICMP, IGMP, ARP, RARP, OSPF, BGP** | **路由器 (Router)**、三层交换机 |
| **数据链路层 (Data Link)** | 帧 (Frame) | **网络接口层** | Ethernet (802.3), Wi-Fi (802.11), PPP, VLAN | **网桥、二层交换机 (Switch)** |
| **物理层 (Physical)** | 比特 (Bit) | 物理介质接口、电平规范 (RJ45, RS232, 光纤) | 中继器 (Repeater)、集线器 (Hub) |

---
### 关联概念双链
[[2.1.2 计算机网络]], [[网络存储技术(DAS_NAS_SAN)]], [[信息安全基础(CIA)]]

