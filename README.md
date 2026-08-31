# Music-Cache-Optimization
# 🎵 Music Cache Optimization

A Spotify-inspired backend application that optimizes repeated music metadata requests using a custom **Least Recently Used (LRU) caching strategy**.

## 🚀 Overview

Music streaming platforms receive repeated requests for popular songs, artists and metadata. Fetching the same information repeatedly from a database can increase latency and server load.

This project implements a custom **LRU Cache** to store recently accessed music metadata and provide faster retrieval for repeated requests.

The cache combines a **Python Dictionary (HashMap)** for O(1) lookup with a **Doubly Linked List** for O(1) insertion, deletion and LRU eviction.

---

## 🏗️ Architecture

```text
Client Request
      │
      ▼
   FastAPI
      │
      ▼
   LRU Cache
   │       │
   │       │
 Cache     Cache
 Hit       Miss
   │         │
   ▼         ▼
Return    Database
Cached       │
Data         ▼
          Store in Cache
              │
              ▼
           Response
