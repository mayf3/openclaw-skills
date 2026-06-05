# Legacy Scripts

这些脚本已从活跃目录移出，保留供参考。

## 移出原因

### Python 脚本
- **research_engine.py** — Claude Code 时代的研究引擎，当前后端流程不使用
- **citation_manager.py** — 引用管理器，未被任何活跃文档引用
- **verify_html.py** — HTML 验证，仅被已归档的 html-generation.md 引用

### Shell 脚本
- **init_research_entry.sh** — 依赖 RESEARCH-CHECKLIST.md（不存在），硬编码路径
- **check_research_status.sh** — 同上
- **update_checklist.sh** — 同上

所有 shell 脚本硬编码了 workspace 路径，且引用的 RESEARCH-CHECKLIST.md 不存在于当前工作区。
