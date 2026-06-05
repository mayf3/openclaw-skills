# ChatGPT Deep Research 后端

通过 Brave Browser CDP 控制 ChatGPT 进行深度研究。

## 前置条件

- Brave Browser 运行在 `--remote-debugging-port=9222`
- 已登录 chatgpt.com，且有 Plus/Team 订阅（Deep Research 权限）
- Python 3 + websockets 库

## ⚠️ 浏览器管理

- **绝对禁止启动/重启/关闭 Brave！** Agent 只 attach
- 如 9222 无响应，告知用户手动启动

## 流程

### 1. 检查登录状态（必须）

```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval $TAB_ID "
(() => {
  const title = document.title;
  const url = window.location.href;
  const isLoginPage = title.includes('登录') || title.includes('Log in') || url.includes('auth');
  const hasInputBox = !!document.querySelector('textarea, div[contenteditable=\"true\"]');
  return {
    title,
    isLoginPage,
    hasInputBox,
    status: isLoginPage ? '❌ NOT_LOGGED_IN' : hasInputBox ? '✅ READY' : '⚠️ UNKNOWN'
  };
})()
" --await-promise
```

如果 `NOT_LOGGED_IN` → 立即停止，告知用户登录。

### 2. 导航到 ChatGPT 主页面（⚠️ 无独立 Deep Research URL）

```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py navigate $TAB_ID "https://chatgpt.com/"
```

**使用主页面**：Deep Research 没有独立页面。在聊天界面：
- 点击输入框下方的工具/附件按钮
- 在弹出的菜单中选择"Deep Research"或"深度研究"
- 也可参考步骤 4 用 JS 自动触发

### 3. 输入研究主题

React textarea 必须用 CDP `Input.insertText`：

```bash
# 先聚焦输入框
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval $TAB_ID "
(() => {
  const input = document.querySelector('textarea');
  if (!input) return { error: '未找到输入框' };
  input.focus();
  return { success: true };
})()
" --await-promise

# 用 CDP 输入文本
python3 -c "
import asyncio, json, urllib.request, websockets
with urllib.request.urlopen('http://localhost:9222/json') as r:
    tabs = json.loads(r.read())
tab = next(t for t in tabs if t['id'] == '$TAB_ID')
ws_url = tab['webSocketDebuggerUrl']
async def type_text():
    async with websockets.connect(ws_url) as ws:
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate',
            'params': {'expression': 'document.querySelector(\"textarea\")?.focus()', 'returnByValue': True}}))
        await ws.recv()
        await asyncio.sleep(0.5)
        await ws.send(json.dumps({'id': 2, 'method': 'Input.insertText',
            'params': {'text': '$RESEARCH_TOPIC'}}))
        await ws.recv()
asyncio.run(type_text())
"
```

### 4. 提交研究

```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval $TAB_ID "
(() => {
  const btn = document.querySelector('button[data-testid=\"fruitfly-submit-button\"]') ||
              document.querySelector('button[aria-label*=\"submit\"]');
  if (btn) { btn.click(); return 'submitted'; }
  const ta = document.querySelector('textarea');
  if (ta) { ta.dispatchEvent(new KeyboardEvent('keydown', {key:'Enter',code:'Enter',keyCode:13})); return 'enter sent'; }
  return 'no submit found';
})()
" --await-promise
```

### 5. 等待完成（30-60 分钟）

**60 秒自动触发机制**：提交后 ChatGPT 生成推荐路线，60s 不操作自动开始。

```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval $TAB_ID "
(() => {
  const bodyText = document.body.innerText;
  const iframe = document.querySelector('iframe');
  return {
    isComplete: bodyText.includes('完成') || bodyText.includes('研究报告'),
    isRunning: bodyText.includes('正在') || bodyText.includes('搜索'),
    iframeHeight: iframe?.offsetHeight || 0,  // > 200 = 报告已渲染
    preview: bodyText.substring(bodyText.length - 300)
  };
})()
"
```

### 6. 提取报告（🔥 关键：嵌套 iframe 穿透）

**必须新建标签页！** 直接导航到 sandbox 域名会破坏 session cookie。

```python
import asyncio, json, urllib.request, websockets

with urllib.request.urlopen('http://localhost:9222/json') as r:
    tabs = json.loads(r.read())

# 新建标签页 → 从 deep-research 列表页点击报告进入对话页
# 找到 sandbox iframe（通过 parentId 匹配）
iframe = next((t for t in tabs if
    'deep_research' in t.get('url', '') and t.get('parentId', '') == '$NEW_TAB_ID'), None)

ws_url = iframe['webSocketDebuggerUrl']

async def extract():
    async with websockets.connect(ws_url, max_size=50*1024*1024) as ws:
        # 1. 获取 frame tree
        await ws.send(json.dumps({'id': 1, 'method': 'Page.getFrameTree'}))
        result = json.loads(await ws.recv())
        children = result['result']['frameTree']['childFrames']
        child_id = children[0]['frame']['id']

        # 2. 创建隔离执行上下文（绕过跨域）
        await ws.send(json.dumps({
            'id': 2, 'method': 'Page.createIsolatedWorld',
            'params': {'frameId': child_id, 'grantUniveralAccess': True}
        }))
        ctx_id = json.loads(await ws.recv())['result']['executionContextId']

        # 3. 分段提取完整文本
        full_text = ''
        for start in range(0, total, 8000):
            await ws.send(json.dumps({
                'id': 100 + start, 'method': 'Runtime.evaluate',
                'params': {
                    'expression': f'document.body.innerText.substring({start}, {min(start+8000, total)})',
                    'contextId': ctx_id, 'returnByValue': True
                }
            }))
            chunk = json.loads(await ws.recv())['result']['result'].get('value', '')
            full_text += chunk

        with open(REPORT_FILE, 'w') as f:
            f.write(full_text)

asyncio.run(extract())
```

**也可通过导出 UI**：展开 → 导出 → Markdown/Word/PDF

## 关键经验

| 问题 | 解决方案 |
|------|---------|
| React textarea 不响应 | 用 CDP `Input.insertText`，不要用 JS 设 value |
| iframe 跨域限制 | `Page.createIsolatedWorld`，不要用 `iframe.contentDocument` |
| Session 损坏 | 必须新建标签页，不能直接导航到 sandbox 域名 |
| 60 秒等待焦虑 | 正常行为，ChatGPT 先生成路线再自动开始 |

## 限制

- 需要 ChatGPT Plus/Team 订阅
- 研究时间 30-60 分钟
- 需要 stable 网络访问 chatgpt.com
