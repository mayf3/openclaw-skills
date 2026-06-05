---
name: add-to-cart
description: |
  多平台加购物车工具。支持淘宝、京东、拼多多（收藏）、闲鱼（想要）。通过 Brave Browser Agent (CDP) 自动化操作。
  依赖：brave-browser-agent skill（Brave 浏览器需开启 --remote-debugging-port=9222）。
  ⚠️ 不涉及支付，只做到加入购物车/收藏为止。
---

# 多平台加购物车 Skill

通过 Brave Browser Agent 的 CDP 协议，自动化多个电商平台的搜索、加购物车/收藏操作。

**支持平台**: 淘宝、京东、拼多多（收藏）、闲鱼（想要）

> ⚠️ **重要原则：不涉及支付！** 只做到"加入购物车/收藏"为止。下单付款由用户自己完成。

---

## 目录

1. [前置依赖](#前置依赖)
2. [通用工作流程](#通用工作流程)
3. [各平台操作指南](#各平台操作指南)
   - [淘宝](#淘宝-taobao)
   - [京东](#京东-jd)
   - [拼多多（收藏）](#拼多多-pdd)
   - [闲鱼（想要）](#闲鱼-xianyu)
4. [验证购物车/收藏列表](#验证购物车收藏列表)
5. [常见问题](#常见问题)
6. [操作规范](#操作规范)
7. [经验记录](#经验记录)

---

## 前置依赖

### 1. Brave 浏览器

必须以远程调试模式运行：

```bash
/Applications/Brave\ Browser.app/Contents/MacOS/Brave\ Browser --remote-debugging-port=9222
```

### 2. 登录状态

| 平台 | 需要登录 | 说明 |
|------|---------|------|
| 淘宝 | ✅ 必须 | 未登录无法加入购物车 |
| 京东 | ⚠️ 建议登录 | 未登录可浏览，但加购物车功能受限 |
| 拼多多 | ✅ 必须 | 收藏功能需要登录 |
| 闲鱼 | ✅ 必须 | "想要"功能需要登录 |

> 操作前先在浏览器中确认已登录各平台账号。

### 3. brave-browser-agent skill

CDP 操作脚本路径：
```
{{SKILL_DIR}}/../brave-browser-agent/scripts/cdp_exec.py
```

### 4. 快捷脚本

本 skill 提供统一搜索脚本：
```
{{SKILL_DIR}}/scripts/add_to_cart.sh
```

---

## 通用工作流程

```
搜索商品 → 浏览结果 → 进入详情 → 选择规格 → 加购物车/收藏 → 验证
```

### 详细步骤

```
Step 1: 搜索商品
  ┌─────────────────────────────────────────┐
  │  使用脚本或手动导航到搜索页                │
  │  ./add_to_cart.sh <platform> <keyword>   │
  │  或手动: cdp_exec.py eval <tab> "..."    │
  └─────────────────┬───────────────────────┘
                    ↓
Step 2: 浏览搜索结果
  ┌─────────────────────────────────────────┐
  │  提取 innerText 或截图查看               │
  │  识别目标商品（名称、价格、销量）           │
  └─────────────────┬───────────────────────┘
                    ↓
Step 3: 进入商品详情页
  ┌─────────────────────────────────────────┐
  │  点击商品链接或直接导航到商品URL           │
  │  sleep 3 等待加载                       │
  │  截图确认页面正确                        │
  └─────────────────┬───────────────────────┘
                    ↓
Step 4: 选择规格（如有）
  ┌─────────────────────────────────────────┐
  │  颜色、尺码、版本等                      │
  │  先截图查看规格选项                       │
  │  逐个点击需要的规格                      │
  └─────────────────┬───────────────────────┘
                    ↓
Step 5: 加购物车/收藏
  ┌─────────────────────────────────────────┐
  │  淘宝/京东: 点击"加入购物车"按钮          │
  │  拼多多:   点击"收藏"按钮                │
  │  闲鱼:     点击"想要"按钮                │
  └─────────────────┬───────────────────────┘
                    ↓
Step 6: 验证
  ┌─────────────────────────────────────────┐
  │  查看购物车/收藏列表                     │
  │  截图确认                               │
  └─────────────────────────────────────────┘
```

---

## 各平台操作指南

### 淘宝 (Taobao)

#### 搜索商品

```bash
SKILL_DIR="{{SKILL_DIR}}/../brave-browser-agent"
CART_DIR="{{SKILL_DIR}}"

# 快捷方式（推荐）
$CART_DIR/scripts/add_to_cart.sh taobao "牛奶" price-asc

# 或手动操作
python3 $SKILL_DIR/scripts/cdp_exec.py list
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://s.taobao.com/search?q=%E7%89%9B%E5%A5%B6&sort=price-asc'"
sleep 3
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "document.body.innerText.substring(0, 8000)"
```

**排序参数**：
| 参数 | 说明 |
|------|------|
| `sort=default` | 综合排序 |
| `sort=price-asc` | 价格从低到高 |
| `sort=price-desc` | 价格从高到低 |
| `sort=sale-desc` | 销量从高到低 |

#### 进入商品详情

```bash
# 方法1: 用商品ID直接导航
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://item.taobao.com/item.htm?id=<商品ID>'"

# 方法2: 点击搜索结果中的第一个商品
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "document.querySelectorAll('a[href*=\"item.taobao.com\"]')[0].click()"

sleep 3
python3 $SKILL_DIR/scripts/cdp_exec.py screenshot <tab_id> /tmp/taobao_item.png
```

#### 选择规格并加购物车

```bash
# 先截图查看规格选项
python3 $SKILL_DIR/scripts/cdp_exec.py screenshot <tab_id> /tmp/taobao_sku.png

# 点击规格（颜色/尺码）
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "document.querySelectorAll('[class*=\"sku\"]')[<index>].click(); 'selected sku'"

# 点击加入购物车
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "(
    document.querySelector('button[action*=\"cart\"]') ||
    document.querySelector('[class*=\"addCart\"]') ||
    document.querySelector('[class*=\"cart\"]')
  ).click(); 'clicked cart button'"

sleep 2

# 确认结果
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "document.body.innerText.substring(0, 3000)"
```

---

### 京东 (JD)

#### 搜索商品

```bash
# 快捷方式
$CART_DIR/scripts/add_to_cart.sh jd "耳机" price-asc

# 手动操作
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://search.jd.com/Search?keyword=%E8%80%B3%E6%9C%BA&psort=3'"
# psort=3 价格升序, psort=4 价格降序, psort=5 销量, psort=0 综合
sleep 3
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "document.body.innerText.substring(0, 8000)"
```

**排序参数**：
| 参数 | 说明 |
|------|------|
| `psort=0` | 综合排序 |
| `psort=3` | 价格从低到高 |
| `psort=4` | 价格从高到低 |
| `psort=5` | 销量从高到低（评论数） |

#### 进入商品详情

```bash
# 方法1: 用商品ID直接导航
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://item.jd.com/<商品ID>.html'"

# 方法2: 点击搜索结果
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "document.querySelector('.p-name a').click()"

sleep 3
python3 $SKILL_DIR/scripts/cdp_exec.py screenshot <tab_id> /tmp/jd_item.png
```

#### 选择规格并加购物车

```bash
# 截图查看规格
python3 $SKILL_DIR/scripts/cdp_exec.py screenshot <tab_id> /tmp/jd_sku.png

# 选择规格（颜色/版本）
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "document.querySelectorAll('#choose-attr-1 a')[<index>].click(); 'selected'"

# 点击加入购物车
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "(
    document.querySelector('#InitCartUrl') ||
    document.querySelector('#btn-addtocart') ||
    document.querySelector('[class*=\"add-to-cart\"]')
  ).click(); 'clicked add to cart'"

sleep 2
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "document.body.innerText.substring(0, 3000)"
```

**京东特点**：
- ✅ 京东自营商品页面结构较稳定
- ⚠️ 第三方商家页面结构可能不同
- ⚠️ 某些商品需要选择配送地址后才显示价格

---

### 拼多多 (PDD) ✅ 已验证

> ⚠️ 拼多多没有传统购物车，操作目标为"收藏"商品。

#### 搜索商品

```bash
# 快捷方式
$CART_DIR/scripts/add_to_cart.sh pdd "货车满当当"

# 手动操作
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://mobile.yangkeduo.com/search_result.html?search_key=%E8%B4%A7%E8%BD%A6%E6%BB%A1%E5%BD%93%E5%BD%93'"
sleep 5
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "document.body.innerText.substring(0, 8000)"
```

#### 进入商品详情并收藏

**已验证的方法**（2026-05-11 成功收藏"鳐鳐鱼货车满当当"）：

```bash
# 方法1：如果已有商品详情页URL，直接导航
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://mobile.yangkeduo.com/goods1.html?goods_id=<商品ID>'"

sleep 3

# 截图确认已进入正确商品页面
python3 $SKILL_DIR/scripts/cdp_exec.py screenshot <tab_id> /tmp/pdd_item.png

# ✅ 验证过的收藏方法：通过 innerText 匹配 SPAN 元素
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "(function(){
    var spans = document.querySelectorAll('span');
    for(var i=0; i<spans.length; i++){
      if(spans[i].innerText === '收藏'){
        spans[i].scrollIntoView({behavior: 'instant', block: 'center'});
        setTimeout(function(){ spans[i].click(); }, 500);
        return '找到收藏按钮，正在点击...';
      }
    }
    return '未找到收藏按钮';
  })()"

sleep 2

# 验证：检查"收藏"是否变为"已收藏"
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "(function(){
    var spans = document.querySelectorAll('span');
    for(var i=0; i<spans.length; i++){
      if(spans[i].innerText === '已收藏'){
        return '✅ 收藏成功！';
      }
    }
    return '⚠️ 可能未收藏成功';
  })()"

# 提取商品信息
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "document.body.innerText.substring(0, 3000)"
```

**备选方法**（如果 SPAN 方式失效，尝试 CSS 选择器）：
```bash
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "(
    document.querySelector('[class*=\"collect\"]') ||
    document.querySelector('[class*=\"favorite\"]') ||
    document.querySelector('[class*=\"star\"]')
  ).click(); 'clicked collect'"
```

**拼多多特点**：
- ⚠️ 使用移动版页面 (`mobile.yangkeduo.com`)，结构更稳定
- ⚠️ 没有购物车概念，用"收藏"替代
- ✅ SPAN 元素匹配 `innerText === '收藏'` 方式经验证可靠
- ✅ 收藏成功后文本变为"已收藏"，可据此验证
- ✅ 需先 scrollIntoView 再 click（收藏按钮在页面底部）

---

### 闲鱼 (Xianyu)

> ⚠️ 闲鱼的操作目标是点击"想要"按钮。

#### 搜索商品

```bash
# 快捷方式
$CART_DIR/scripts/add_to_cart.sh xianyu "二手书"

# 手动操作
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://www.goofish.com/search?q=%E4%BA%8C%E6%89%8B%E4%B9%A6'"
sleep 3
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "document.body.innerText.substring(0, 8000)"
```

#### 进入商品详情并点击"想要"

```bash
# 点击搜索结果
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "document.querySelectorAll('a[href*=\"item\"]')[0].click()"

sleep 3
python3 $SKILL_DIR/scripts/cdp_exec.py screenshot <tab_id> /tmp/xianyu_item.png

# 点击"想要"按钮
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "(
    document.querySelector('[class*=\"want\"]') ||
    document.querySelector('[class*=\"Want\"]') ||
    document.querySelector('button[class*=\"chat\"]')
  ).click(); 'clicked want'"

sleep 2
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "document.body.innerText.substring(0, 3000)"
```

**闲鱼特点**：
- ⚠️ 闲鱼页面结构变化频繁，选择器可能需要调整
- ⚠️ "想要"按钮可能打开聊天界面，这是正常的
- ⚠️ 某些商品需要先验证才能查看详情

---

## 验证购物车/收藏列表

### 淘宝购物车

```bash
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://cart.taobao.com/cart.htm'"
sleep 3
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "document.body.innerText.substring(0, 8000)"
python3 $SKILL_DIR/scripts/cdp_exec.py screenshot <tab_id> /tmp/taobao_cart.png
```

### 京东购物车

```bash
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://cart.jd.com'"
sleep 3
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "document.body.innerText.substring(0, 8000)"
python3 $SKILL_DIR/scripts/cdp_exec.py screenshot <tab_id> /tmp/jd_cart.png
```

### 拼多多收藏夹

```bash
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://mobile.yangkeduo.com/user_fav.html'"
sleep 3
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "document.body.innerText.substring(0, 8000)"
python3 $SKILL_DIR/scripts/cdp_exec.py screenshot <tab_id> /tmp/pdd_fav.png
```

### 闲鱼个人中心

```bash
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://www.goofish.com/personal'"
sleep 3
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "document.body.innerText.substring(0, 8000)"
python3 $SKILL_DIR/scripts/cdp_exec.py screenshot <tab_id> /tmp/xianyu_personal.png
```

---

## 常见问题

### 反爬/验证码

| 平台 | 常见问题 | 解决方案 |
|------|---------|---------|
| 淘宝 | 滑块验证码 | 用户手动完成，间隔 5-10 秒再操作 |
| 京东 | 频繁访问限制 | 降低操作频率，使用 `sleep 5` |
| 拼多多 | 登录态失效 | 重新在浏览器中登录 |
| 闲鱼 | 页面跳转验证 | 用户手动完成验证 |

### 页面结构变化

- 电商平台前端**频繁更新**，CSS 类名可能随时变化
- 建议：先用 `screenshot` 截图查看实际页面，再调整选择器
- 参考选择器文档：`references/platform-selectors.md`
- 通用策略：按文字匹配按钮（见下方）

**通用按钮匹配**（当选择器失效时使用）：
```javascript
const buttons = [...document.querySelectorAll('button, a, span, div')];
const target = buttons.find(b => b.innerText.includes('加入购物车'));
if (target) { target.click(); 'clicked'; } else { 'button not found'; }
```

### 规格选择

- 不同商品的规格选择器**差异很大**
- 建议：先截图查看规格区域，确定选择器后再操作
- 常见模式：
  - 淘宝: `[class*="sku"]`
  - 京东: `#choose-attr-1 a`
  - 拼多多: 通常无需选规格
  - 闲鱼: 通常无需选规格

### ⚠️ SKU（款式）绑定问题（2026-06-03）

天猫新版本详情页（`detail.tmall.com`）的"加入购物车"按钮是**动态JS加载**，DOM中不可见。
使用旧版API `add_cart_item.htm` 添加商品时，需要正确传递 SKU ID 才能绑定款式。

#### 正确做法：先进入详情页选中SKU，再从购物车页调API

```bash
# 步骤1：导航到商品详情页
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href = 'https://detail.tmall.com/item.htm?id=<商品ID>'"
sleep 5

# 步骤2：提取SKU映射数据（从script标签中的JSON）
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "document.querySelectorAll('script')[44].text" | jq -r '...'

# 提取关键数据：
# - valueMap: 属性值ID → 显示名称的映射
# - skus: propPath → skuId的映射数组
# - props: 属性定义（名称列表）

# 步骤3：通过文本匹配点击选中正确的SKU
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "var all = document.querySelectorAll('span,label,div,a');
   for(var i=0; i<all.length; i++){
     var t = all[i].innerText || '';
     if(t.includes('五件套') && t.includes('700ML')){
       all[i].click(); break;
     }
   }"
sleep 2

# 步骤4：回到购物车页，从同域调API
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "window.location.href='https://cart.taobao.com/cart.htm'"
sleep 4

# 步骤5：从购物车页（同域）调用API
# 获取token
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "document.cookie.match(/_tb_token_=([^;]+)/)[1]"

# 调用API（必须从cart.taobao.com域）
python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> \
  "var xhr = new XMLHttpRequest();
   xhr.open('POST', '/add_cart_item.htm', false);
   xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
   xhr.send('itemId=<ID>&skuId=<SKU_ID>&quantity=1&_tb_token_=<TOKEN>');
   xhr.responseText"
```

#### 获取SKU ID的标准流程

商品页的script[44]（或附近）包含完整的SKU数据，结构如下：

```json
// skuBase.props - 属性定义
"props": [{
  "name": "颜色分类",
  "values": [{"vid": "38271728708", "name": "【五件套】700ML..."}]
}]

// skuBase.skus - SKU映射
"skus": [{
  "propPath": "1627207:38271728708",
  "skuId": "5779409133677"
}]

// skuCore.sku2info - SKU库存/价格
"sku2info": {
  "0": {"quantity": 200, ...},  // 默认
  "5779409133677": {"quantity": 200, ...}  // 具体SKU
}
```

**选择步骤**：
1. 从 `props[0].values` 中找到目标选项的 `vid`
2. 从 `skus` 数组中找 `propPath` 包含该 `vid` 的 `skuId`
3. 使用该 `skuId` 作为API参数

#### ⚠️ 已知问题
- API会响应成功（`cartQuantity`增加），但如果SKU ID不正确或API不认，购物车会显示**"请选择款式"** / **"重新选择规格"**
- 从`cart.taobao.com`域调API成功率高，但建议先在该页面加载确保登录态
- 频繁调用会触发风控（`rgv587_flag: "sm"`），需间隔10-15秒
- 多属性商品（颜色+尺寸+数量等）需要找到组合后的正确SKU ID

### 登录态失效

- 长时间未操作后，登录态可能过期
- 症状：页面跳转到登录页，或操作无响应
- 解决：在浏览器中手动重新登录

---

## 操作规范

### ⚠️ 强制规范

1. **每次操作前先 `list` 获取最新 tab 列表**
   ```bash
   python3 $SKILL_DIR/scripts/cdp_exec.py list
   ```

2. **操作后 `sleep 3-5` 等待页面加载**
   ```bash
   sleep 3  # 普通操作
   sleep 5  # 搜索、页面跳转
   ```

3. **用 `screenshot` + `innerText` 双重确认页面状态**
   ```bash
   python3 $SKILL_DIR/scripts/cdp_exec.py screenshot <tab_id> /tmp/confirm.png
   python3 $SKILL_DIR/scripts/cdp_exec.py eval <tab_id> "document.body.innerText.substring(0, 3000)"
   ```

4. **不要连续快速操作，避免触发反爬**
   - 每次点击后等待 2-3 秒
   - 搜索间隔至少 5 秒
   - 同一平台每分钟不超过 5 次操作

5. **截图保存到 `/tmp/` 目录**，便于查看和调试

### 操作顺序建议

```
1. list → 获取 tab
2. navigate → 打开搜索页
3. sleep 5 → 等待
4. screenshot + innerText → 确认搜索结果
5. click → 进入详情页
6. sleep 3 → 等待
7. screenshot → 确认详情页
8. click → 选择规格
9. sleep 2 → 等待
10. click → 加购物车/收藏
11. sleep 2 → 等待
12. screenshot + innerText → 确认结果
```

---

## 经验记录

### 2026-04-27: 欧瑞博小圆红外控制器（淘宝）
- **平台**: 淘宝
- **搜索关键词**: `全向红外遥控器 智能`
- **商品ID**: `827144498080`
- **店铺**: 智能家居厂家直销店
- **价格**: 券后 ￥80
- **操作结果**: ✅ 成功加入购物车
- **备注**: 商品页面已有"成功加入购物车"提示，之前可能已添加过
- **经验**:
  - 淘宝详情页截图很重要，文字提取可能遗漏图片中的信息
  - 加购物车按钮选择器需要根据实际页面调整
  - `button[action*="cart"]` 在此商品页面有效

### 2026-05-11: 鳐鳐鱼货车满当当（拼多多收藏 ✅ 已验证）
- **平台**: 拼多多
- **搜索关键词**: `鳐鳐鱼 货车满当当 桌游`
- **商品ID**: `753946420431`
- **店铺**: 朝花夕誓益智玩具屋（6年老店，已拼8.3万件）
- **价格**: 券后 ¥46（已优惠¥8）
- **销量**: 已拼215件
- **操作结果**: ✅ 成功收藏（验证：按钮由"收藏"变为"已收藏"）
- **关键发现**:
  - 收藏按钮是 SPAN 元素，用 `innerText === '收藏'` 匹配
  - 收藏按钮在页面底部，需要先 `scrollIntoView` 再 `click()`
  - `setTimeout(500ms)` 确保滚动完成后再点击
  - 验证方式：查找 `innerText === '已收藏'` 确认
- **经验**:
  - CSS 类名选择器容易因页面更新失效，SPAN 文本匹配更稳定
  - 拼多多无需选择规格，直接收藏即可

### 2026-05-11: 创建多平台 Skill
- **变更**: 从 `taobao-cart` 扩展为 `add-to-cart`，支持淘宝、京东、拼多多、闲鱼
- **新增**:
  - 统一搜索脚本 `scripts/add_to_cart.sh`
  - 多平台选择器参考 `references/platform-selectors.md`
  - 各平台操作指南
- **经验**:
  - 拼多多使用移动版页面更稳定
  - 闲鱼页面结构变化频繁，建议多用截图
  - 京东自营页面结构比第三方商家稳定
