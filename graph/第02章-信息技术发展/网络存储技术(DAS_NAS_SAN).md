---
title: "网络存储技术对比 (DAS vs NAS vs SAN)"
chapter: "第2章 信息技术发展"
section: "2.1.3 存储和数据库"
category: "系统硬件/数据存储"
tags: ["第2章", "存储技术", "DAS", "NAS", "SAN", "必考对比"]
aliases: ["DAS", "NAS", "SAN", "网络存储", "IP-SAN", "FC-SAN"]
---

> **所属章节**：[[第02章-信息技术发展/第2章-知识总览|第2章 信息技术发展]] > 2.1.3 存储和数据库

# 网络存储技术对比 (DAS vs NAS vs SAN)

## 1. 三大网络存储技术全面对比
| 维度 | 直连式存储 (DAS) | 网络附加存储 (NAS) | 存储区域网络 (SAN) |
| :--- | :--- | :--- | :--- |
| **英文全称** | Direct Attached Storage | Network Attached Storage | Storage Area Network |
| **连接方式** | SCSI / SATA / SAS 线缆直连服务器 | 通过标准以太网 (TCP/IP) 连接 | 专用高速光纤网 (FC) 或 IP 网络 |
| **访问级别** | **块级别 (Block Level)** | **文件级别 (File Level)** | **块级别 (Block Level)** |
| **协议标准** | SCSI, ATA | NFS (Linux), CIFS/SMB (Windows) | FC (Fibre Channel), iSCSI |
| **性能表现** | 较高，受限于单机扩展 | 一般，受网络带宽与文件系统协议开销影响 | **极高**，带宽大、时延低 |
| **适用场景** | 小型单机服务器、PC | 文件共享、非结构化文档办公协作 | 大型数据库、高性能关键业务、虚拟化集群 |

---
### 关联概念双链
[[2.1.3 存储和数据库]], [[数据存储备份与容灾(RPO_RTO)]]

