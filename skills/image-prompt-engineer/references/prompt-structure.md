# Prompt 架构指南 — 通用原则

## 提示词基本结构（平台通用）

```
[主体] + [动作/姿态] + [环境/背景] + [光线] + [构图] + [风格] + [画质/技术参数]
```

### 1. 主体 (Subject)

| 要素 | 示例 |
|------|------|
| 人物 | `a young Asian woman, 25 years old, long black hair, red dress` |
| 动物 | `a fluffy orange cat, green eyes, sitting on windowsill` |
| 物体 | `a vintage Leica camera, brass and leather texture` |
| 场景 | `a futuristic city at night, neon lights, rain-slicked streets` |

**量化原则**：具体 > 抽象。用 `a 30-year-old man with graying temples and a trimmed beard` 优于 `a middle-aged man`。

### 2. 动作/姿态 (Action/Pose)

| 类型 | 示例 |
|------|------|
| 静态 | `standing confidently, looking over shoulder` |
| 动态 | `running through shallow water, splashing` |
| 交互 | `holding a cup of coffee, steam rising` |
| 表情 | `laughing naturally, eyes crinkling` |

### 3. 环境/背景 (Environment)

指定场景和氛围。越具体越好：
- 室内：`in a cozy bookstore, warm wooden shelves, soft lamp light`
- 室外：`on a misty mountain trail at dawn, pine trees, wildflowers`
- 抽象：`in a surreal dreamscape, floating islands, impossible geometry`

### 4. 光线 (Lighting)

| 光线类型 | 关键词 | 效果 |
|----------|--------|------|
| 自然光 | golden hour, soft daylight, overcast | 温暖/柔和 |
| 人工光 | studio lighting, rim light, neon | 专业/戏剧 |
| 特殊 | moonlight, firelight, bioluminescent | 氛围感 |
| 时间 | dawn, sunset, midnight, blue hour | 色温 |

### 5. 构图 (Composition)

| 景别 | 关键词 | 效果 |
|------|--------|------|
| 特写 | close-up, macro, extreme close-up | 细节突出 |
| 中景 | medium shot, waist up | 人物+环境 |
| 全景 | wide shot, full body, establishing shot | 场景展示 |
| 视角 | low angle, bird's eye view, POV, dutch angle | 特殊观感 |

### 6. 风格 (Style)

见 `references/style-library.md` 完整风格词汇库。

### 7. 画质/技术参数 (Quality)

通用：`8K, highly detailed, sharp focus, photorealistic, masterpiece`
平台特定：MJ 用 `--q 2`，SD 用 `(masterpiece, best quality:1.2)`

---

## 三大平台 Prompt 风格差异

| 维度 | Midjourney | Stable Diffusion | DALL-E 3 / Flux |
|------|-----------|----------------|-----------------|
| **语法** | 自然英语句子，`,` 分隔 | 关键词堆叠，`,` 分隔 | 自然语言段落 |
| **权重** | 双 `::` 分隔 | `(word:1.2)` 或 `(word)` | 不支持 |
| **负面词** | `--no xxx` | `negative prompt:` 区域 | 不支持 |
| **参数** | `--ar 16:9 --s 250 --v 6` | `CFG:7, Steps:30` | 自动处理 |
| **长prompt** | 易于处理 | 偏好中等长度 | 最长可接受 |
| **垫图** | `image_url text prompt --iw 2` | `img2img` 或 ControlNet | 不支持垫图 |

---

## 中文需求 → 英文 Prompt 工作流

```
用户中文需求
    ↓
[Step 1] 拆要素 → 主体 / 环境 / 动作 / 风格 / 画质
    ↓
[Step 2] 加修饰 → 每个要素加2-3个精准修饰词
    ↓
[Step 3] 定参数 → 根据平台添加技术参数
    ↓
[Step 4] 加负面词 → 针对平台添加负面提示词
    ↓
输出：平台特化 Prompt
```

### 示例

**用户需求**："一个穿汉服的女孩在樱花树下弹古筝，古风，电影感"

**Midjourney 版**：
```
A graceful Chinese woman in flowing hanfu, playing guzheng under cherry blossom trees, pink petals falling, soft golden sunset light filtering through branches, traditional ancient Chinese aesthetic, cinematic composition, shallow depth of field, warm color palette, photorealistic, 8K --ar 16:9 --s 400 --v 6
```

**Stable Diffusion 版**：
```
1girl, hanfu, playing guzheng, cherry blossoms, falling petals, outdoors, golden hour, cinematic lighting, depth of field, bokeh, traditional Chinese aesthetic, masterpiece, best quality, photorealistic, 8K
Negative prompt: bad anatomy, ugly, extra fingers, low quality, watermark, text
```

---

## 去 AI 感核心技巧

### DO（要加）
- `skin pores, realistic skin texture` — 皮肤纹理
- `subtle imperfections, natural asymmetry` — 自然瑕疵
- `catchlight in eyes, natural eye reflection` — 眼神光
- `fine lines, natural wrinkles` — 细纹
- `soft focus, film grain` — 胶片感

### DON'T（避免）
- `perfect skin, flawless, porcelain skin` — 假滑
- `beautiful, gorgeous, stunning` — 空洞
- `dramatic lighting, high contrast` — 过度雕琢
- `intricate details, hyperdetailed` — 密集恐惧

---

## 常见负面提示词（通用）

```
low quality, worst quality, bad anatomy, bad hands, weird fingers,
extra digits, missing fingers, deformed, mutated, ugly, disfigured,
poorly drawn face, cloned face, text, watermark, signature,
blurry, jpeg artifacts, compression artifacts, oversaturated,
overexposed, underexposed, bad proportions, unnatural,
plastic skin, smooth skin, airbrushed, smooth surface
```
