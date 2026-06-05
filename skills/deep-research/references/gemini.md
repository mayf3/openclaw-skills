# Gemini Deep Research 后端

通过 Brave Browser CDP 控制 Google Gemini 进行深度研究。

## 前置条件

- Brave Browser 运行在 `--remote-debugging-port=9222`
- 已登录 gemini.google.com，且有 Gemini Advanced 订阅
- Python 3 + websockets 库

## ⚠️ 浏览器管理

- **绝对禁止启动/重启/关闭 Brave！** Agent 只 attach
- 如 9222 无响应，告知用户手动启动

## 流程

### 1. 检查 Brave 状态

```bash
python3 {{SKILL_DIR}}/scripts/check_cdp.py
```

### 2. 获取/打开 Gemini 标签页

```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py list
# 找 Gemini 标签页，或新开：
python3 {{SKILL_DIR}}/scripts/cdp_exec.py open "https://gemini.google.com/app"
```

### 3. 激活 Deep Research 模式

```bash
# 点击"工具"按钮
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval $TAB_ID "
(() => {
  const toolBtn = Array.from(document.querySelectorAll('button')).find(b =>
    b.getAttribute('aria-label')?.includes('tool') || b.textContent?.includes('工具'));
  if (toolBtn) { toolBtn.click(); return '✅ 工具按钮已点击'; }
  return '❌ 未找到工具按钮';
})()
" --await-promise

# 选择 Deep Research
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval $TAB_ID "
(() => {
  const drOption = Array.from(document.querySelectorAll('[role=\"menuitem\"], [role=\"menuitemcheckbox\"], button')).find(el =>
    el.textContent?.includes('Deep Research'));
  if (drOption) { drOption.click(); return '✅ Deep Research 已选择'; }
  return '❌ 未找到';
})()
" --await-promise
```

### 4. 选择"快速"模式（免费账号关键步骤）

免费账号每天 5 次 Deep Research 配额**只适用于"快速"模式**。

```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval $TAB_ID "
(() => {
  const quickBtn = Array.from(document.querySelectorAll('button')).find(b =>
    b.textContent?.trim() === '快速' || b.getAttribute('aria-label')?.includes('快速'));
  if (!quickBtn) return { error: '未找到快速按钮' };
  quickBtn.click();
  return new Promise(resolve => {
    setTimeout(() => {
      const isActive = quickBtn.classList.contains('active') || quickBtn.getAttribute('aria-pressed') === 'true';
      resolve({ clicked: true, modeSelected: isActive });
    }, 1000);
  });
})()
" --await-promise
```

### 5. 输入研究主题

用 `execCommand('insertText')` 而非直接设 textContent：

```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval $TAB_ID "
(() => {
  const input = document.querySelector('[contenteditable=\"true\"], textarea, [role=\"textbox\"]');
  if (input) {
    input.focus();
    document.execCommand('insertText', false, '${RESEARCH_TOPIC}');
    input.dispatchEvent(new Event('input', { bubbles: true }));
    return '✅ 已输入';
  }
  return '❌ 未找到输入框';
})()
" --await-promise
```

### 6. 提交并等待研究方案

```bash
# 点击发送
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval $TAB_ID "
(() => {
  const sendBtn = Array.from(document.querySelectorAll('button')).find(b =>
    b.getAttribute('aria-label')?.includes('send') || b.textContent?.includes('发送'));
  if (sendBtn) { sendBtn.click(); return '✅ 已提交'; }
  return '❌ 未找到发送按钮';
})()
" --await-promise

# 等待方案生成（10-30 秒）
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval $TAB_ID "
new Promise(resolve => {
  const check = setInterval(() => {
    if (document.body.innerText.includes('开始研究') || document.body.innerText.includes('Start research')) {
      clearInterval(check); resolve('✅ 研究方案已生成');
    }
  }, 2000);
  setTimeout(() => { clearInterval(check); resolve('⏳ 仍在生成...'); }, 30000);
})()
" --await-promise
```

### 7. 点击"开始研究"（🔥 关键：Angular Material 按钮）

```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval $TAB_ID "
(async () => {
  const startBtn = Array.from(document.querySelectorAll('button')).find(b =>
    b.textContent?.includes('开始研究') || b.textContent?.includes('Start research'));
  if (!startBtn) return '❌ 未找到按钮';

  startBtn.scrollIntoView({ behavior: 'instant', block: 'center' });
  await new Promise(r => setTimeout(r, 500));

  const rect = startBtn.getBoundingClientRect();
  const x = rect.left + rect.width / 2;
  const y = rect.top + rect.height / 2;

  startBtn.focus();
  startBtn.dispatchEvent(new PointerEvent('pointerdown', { bubbles:true, cancelable:true, clientX:x, clientY:y, pointerType:'mouse', isPrimary:true }));
  await new Promise(r => setTimeout(r, 100));
  startBtn.dispatchEvent(new MouseEvent('click', { bubbles:true, cancelable:true, clientX:x, clientY:y, button:0, which:1 }));
  await new Promise(r => setTimeout(r, 100));
  startBtn.dispatchEvent(new PointerEvent('pointerup', { bubbles:true, cancelable:true, clientX:x, clientY:y, pointerType:'mouse', isPrimary:true }));

  return { success: true, x: Math.round(x), y: Math.round(y) };
})()
" --await-promise
```

### 8. 等待完成（30-90 分钟）

```bash
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval $TAB_ID "
(() => {
  const bodyText = document.body.innerText;
  return {
    isComplete: bodyText.includes('研究完成') || bodyText.includes('Research complete'),
    isRunning: bodyText.includes('正在搜索') || bodyText.includes('进行中'),
    hasError: bodyText.includes('错误') || bodyText.includes('error'),
    preview: bodyText.substring(bodyText.length - 300)
  };
})()
"
```

### 9. 提取结果

Gemini 没有 ChatGPT 的 sandbox iframe 问题，可直接提取：

```bash
# 截图
python3 {{SKILL_DIR}}/scripts/cdp_exec.py screenshot $TAB_ID $WORKSPACE/reports/.../screenshots/complete.png

# 提取文本
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval $TAB_ID "document.body.innerText" > report.txt

# 提取 HTML
python3 {{SKILL_DIR}}/scripts/cdp_exec.py eval $TAB_ID "document.documentElement.outerHTML" > report.html
```

### 10. 生成结构化文档（推荐）

基于原始报告生成 7 个标准文档：
1. `README.md` — 元信息
2. `00-executive-summary.md` — 摘要（300 字）
3. `01-top-picks.md` — Top 3 方案
4. `02-deep-dive.md` — 技术综述
5. `03-quickstart.md` — 快速上手
6. `04-comparison.md` — 方法对比
7. `05-benchmarks.md` — 性能基准

## 关键经验

| 问题 | 解决方案 |
|------|---------|
| "开始研究"按钮不可见 | 先 `scrollIntoView`，再用 PointerEvent 序列 |
| Angular Material 按钮 `.click()` 无效 | 用 PointerEvent + MouseEvent 序列 |
| `textContent` 赋值不触发监听 | 用 `execCommand('insertText')` |
| 免费账号配额限制 | 用"快速"模式，每天 5 次 |

## 限制

- 需要 Gemini Advanced 订阅（快速模式免费账号也可用）
- 研究时间 30-90 分钟
- 需要 stable 网络访问 Google
