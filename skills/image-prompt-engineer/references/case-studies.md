# 实战案例库

## 案例 1：中文需求 → 多平台 Prompt

**用户需求**："一只橘猫在窗台上晒太阳，午后，温馨"

**Midjourney**：
```
A chubby orange tabby cat lounging on a wooden windowsill, warm afternoon sunlight streaming through the window, dust motes floating in the light, cozy home atmosphere, soft shadows, shallow depth of field, photorealistic, warm color palette, 8K --ar 4:3 --style raw --s 50 --v 6
```

**Stable Diffusion**：
```
(masterpiece, best quality:1.2), 1cat, orange tabby, fat cat, lying on windowsill, wooden sill, afternoon sun, god rays, volumetric lighting, cozy atmosphere, soft shadows, depth of field, bokeh, warm colors, photorealistic, 8K
Negative prompt: low quality, blurry, ugly, bad anatomy, text, watermark, cgi
Steps: 30, CFG: 7, Sampler: DPM++ 2M Karras
```

**DALL-E 3**：
```
A cozy afternoon scene featuring a chubby orange tabby cat lounging on a wooden windowsill. Warm golden sunlight streams through the window, creating soft shadows and illuminating floating dust motes. The atmosphere is warm and peaceful. Photorealistic style with natural lighting. 4:3 aspect ratio. No text or watermark.
```

---

## 案例 2：痛点解决 — "太假了" → 去 AI 感

**用户反馈**：生成的图片虽然好看，但是一眼看出是 AI 画的

**问题诊断**：

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 皮肤太光滑 | 缺少皮肤纹理词 | 加 `skin pores, natural skin texture, subtle imperfections` |
| 光影太完美 | 缺少真实环境光 | 加 `mixed lighting, natural shadows, slight overexposure` |
| 构图太对称 | 缺少自然随性感 | 加 `candid, slightly off-center, natural pose` |
| 色彩太鲜艳 | 饱和度偏高 | 加 `muted colors, film-like, slightly desaturated` |

**优化示例**：

```
优化前：A beautiful woman in a garden, perfect lighting, stunning
优化后：A candid photograph of a woman with natural skin texture, standing in a garden,
mixed daylight and shade, subtle skin imperfections visible, slightly overexposed
background creating natural bokeh, film-like color grading, shot on 35mm film
```

---

## 案例 3：电商产品图

**需求**：白色陶瓷咖啡杯，极简，北欧风

```
Professional product photography of a matte white ceramic coffee cup,
minimalist Scandinavian design, smooth matte texture, placed on light
wooden surface, soft natural light from left, subtle shadow cast,
clean composition, commercial grade, high end product shot,
white background with slight gradient, 8K --ar 1:1 --style raw --s 30 --v 6
```

要点：材质（matte ceramic）、光线（soft natural）、构图（clean）、背景（white gradient）

---

## 案例 4：风格迁移

**需求**：把一张照片变成宫崎骏风格

```
A vibrant scenic landscape in the style of Studio Ghibli and Hayao Miyazaki,
lush green rolling hills, fluffy white clouds in bright blue sky,
charming rustic houses with red roofs, whimsical atmosphere,
warm golden light, hand-painted texture, soft pastel color palette,
gentle breeze through tall grass, idyllic countryside --ar 16:9 --s 600 --v 6
```

注意：Ghibli style 在 MJ 中需要高 stylize 值（`--s 400-600`）

---

## 案例 5：跨平台转换实战

**SD prompt 转 MJ**：

```
SD: (masterpiece:1.2), 1girl, hanfu, playing guzheng, cherry blossoms,
outdoors, golden hour, cinematic lighting, depth of field, bokeh,
traditional Chinese aesthetic, photorealistic, 8K
```

```
MJ（转换后）：
A graceful Chinese woman in flowing traditional hanfu playing guzheng
under falling cherry blossoms, golden hour light, cinematic depth of field,
warm tones, traditional Chinese aesthetic, photorealistic, 8K --ar 16:9
```

| 转换项 | 说明 |
|--------|------|
| 删权重 | `(masterpiece:1.2)` → 去掉，用自然描述替代 |
| 去 emoji | `1girl` → `a Chinese woman` |
| 保留关键元素 | 人物/动作/环境/光线 不变 |
| 重排语法 | 堆叠词 → 通顺句子 |
| 加参数 | 根据需求加 `--ar` `--s` 等 |
