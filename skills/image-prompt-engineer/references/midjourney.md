# Midjourney Prompt 特化指南

## 基础语法

```
[image_prompt] --ar [aspect_ratio] --v [version] --s [stylize] --c [chaos] --iw [image_weight]
```

### 核心参数

| 参数 | 范围 | 默认 | 说明 |
|------|------|------|------|
| `--ar` | 任意比例 | 1:1 | 宽高比，如 `--ar 16:9` `--ar 9:16` |
| `--v` | 5/6 | 6 | 模型版本，`--v 6` 最新 |
| `--s` | 0-1000 | 100 | 风格化程度，`--s 0` 严格遵循 prompt，`--s 1000` 极强创意 |
| `--c` | 0-100 | 0 | 混沌度，越高结果越多样化 |
| `--iw` | 0.5-2 | 1 | 垫图权重（仅垫图时用） |
| `--no` | - | - | 排除元素：`--no text watermark people` |
| `--style` | raw/expressive | - | 风格模式，`--style raw` 更写实 |

### 最佳实践

**写实摄影：**
```markdown
--style raw --s 50 --v 6
```

**艺术创作：**
```markdown
--s 400 --v 6
```

**垫图（Image Prompt）：**
```markdown
[image_url] [text prompt] --iw 1.5 --ar 16:9 --v 6
```

---

## Prompt 权重控制

使用双冒号 `::` 分隔不同部分并分配权重：

```
element::2 another::1 third::0.5
```

高权重部分会被更严格遵循。

**示例**：
```
a majestic castle on a hill::2 stormy sky with lightning::1 misty forest foreground::0.5 --ar 16:9
```

---

## 常用风格修饰词

### 摄影风格
| 风格 | 关键词 |
|------|--------|
| 胶片 | film photography, Kodak Portra 400, Fuji Pro 400H, grain |
| 纪实 | documentary style, candid, street photography, natural light |
| 商业 | commercial photography, studio lighting, product shot |
| 人像 | portrait photography, soft lighting, professional headshot |
| 电影 | cinematic, anamorphic, film still, color graded |

### 艺术风格
| 风格 | 关键词 |
|------|--------|
| 水彩 | watercolor, wet on wet, paper texture, artistic |
| 油画 | oil painting, impasto, canvas texture, Van Gogh style |
| 水墨 | Chinese ink wash painting, sumi-e, brush strokes |
| 赛博朋克 | cyberpunk, neon noir, dystopian, blade runner |
| 吉卜力 | Studio Ghibli, Miyazaki style, whimsical, hand-drawn |
| 像素 | pixel art, 8-bit, retro gaming, chunky pixels |

### 画质标签
```
photorealistic, hyperrealistic, highly detailed, intricate details,
8K, UHD, sharp focus, masterpiece, award-winning photograph,
National Geographic, trending on ArtStation
```

---

## 避免的常见错误

| 错误 | 原因 | 正确做法 |
|------|------|----------|
| prompt 过长 | MJ v6 仍有限制 | 控制在 60-80 词内 |
| 过多否定词 | `--no` 效果有限 | 用正面描述替代 |
| 多重风格混搭 | 每张图 1-2 种风格 | 聚焦单一风格 |
| 忽视 `--style raw` | 写实场景不加 raw 会偏艺术化 | 写实必加 `--style raw` |
| 垫图权重过高 | `--iw 2` 会过度复制 | 从 `--iw 1` 开始微调 |

---

## 常用预设搭配

**产品摄影**：
```
[product] product photography, studio lighting, white background, soft shadows, commercial grade, 8K --ar 4:3 --style raw --s 30 --v 6
```

**人像写实**：
```
[subject] candid portrait, natural lighting, shallow depth of field, skin texture, realistic skin, soft focus background, shot on Canon R5 --ar 3:4 --style raw --s 50 --v 6
```

**概念艺术**：
```
[concept] concept art, intricate details, epic composition, dramatic lighting, trending on ArtStation --ar 16:9 --s 400 --v 6
```

**风景**：
```
[scene] landscape photography, golden hour, dramatic sky, ultra wide angle, high dynamic range, National Geographic --ar 16:9 --style raw --s 100 --v 6
```
