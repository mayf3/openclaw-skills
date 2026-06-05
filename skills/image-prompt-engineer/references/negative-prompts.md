# 负面提示词库 (Negative Prompts)

## 一、通用负面提示词（适用所有平台）

```
low quality, worst quality, bad anatomy, bad hands, text, error,
missing fingers, extra digit, fewer digits, cropped, jpeg artifacts,
signature, watermark, username, blurry, deformed, ugly, duplicate,
morbid, extra fingers, mutated hands, poorly drawn hands,
poorly drawn face, mutation, extra limbs, extra arms, extra legs,
malformed limbs, fused fingers, too many fingers, long neck,
cross-eyed, mutated, bad proportions, cloned face, disfigured,
gross, out of frame, cut off, lowres, bad composition,
amputee, missing arms, missing legs
```

## 二、去 AI 感/提升写实度

```
smooth skin, airbrushed skin, plastic skin, wax skin, porcelain skin,
doll-like face, mannequin, CGI, render, 3D render, software render,
unnatural skin texture, blurred textures, polished surface,
overexposed, underexposed, oversaturated, HDR, plastic-looking,
fake looking, artificial, synthetic, glossy skin, oily skin
```

## 三、去伪影/修复质量

```
bad quality, low quality, normal quality, mediocre, grainy, noisy,
pixelated, blurry, motion blur, out of focus, soft focus,
jpeg artifacts, compression artifacts, ringing artifacts,
blocky, aliasing, moire pattern, color banding, posterization,
overexposed, underexposed, blown out highlights, crushed shadows
```

## 四、去人物伪影

```
bad anatomy, bad proportions, bad hands, bad feet, bad face,
extra fingers, missing fingers, fused fingers, too many fingers,
mutated hands, mutated arms, extra arms, extra limbs,
cross-eyed, deformed eyes, weird eyes, bad eyes, asymmetrical eyes,
missing eyes, extra eyes, closed eyes (if not intended),
deformed mouth, bad teeth, missing teeth, extra teeth,
long neck, short neck, twisted neck, double chin,
bad pose, awkward pose, contorted, unnatural pose
```

## 五、去多余元素

```
text, watermark, signature, username, logo, stamp, label,
caption, title, date, timestamp, frame, border,
artist name, website, URL, handle, tag, QR code,
barcode, copyright, trademark, ®, ©, ™
```

## 六、平台特化

### Midjourney（用 `--no` 参数）

```
--no text, watermark, logo, ugly, deformed, blurry, low quality
```

### Stable Diffusion / Flux（独立文本框）

```
(worst quality, low quality:1.4), normal quality, bad anatomy,
bad hands, extra fingers, missing fingers, deformed, mutated,
ugly, blurry, text, watermark, signature, username,
lowres, bad proportions, cloned face, disfigured,
cross-eyed, long neck, fused fingers, too many fingers,
mutated hands, extra limbs, missing arms, missing legs
```

### DALL-E 3（不支持负面词，用正面引导）

```
Please do NOT include: text, watermarks, signatures, logos, or any written
language. Ensure the image looks natural and realistic with proper anatomy.
```

## 七、负面词使用技巧

1. **优先级排序**：最重要的负面词放前面（SD 中给予更高权重）
2. **适度使用**：过多的负面词会限制模型创意
3. **用正面替代**：`well-proportioned, natural hands` > `bad hands, deformed`
4. **权重平衡**：`(worst quality, low quality:1.4)` — 单个权重不宜超过 1.5
5. **避免冲突**：不要同时要求某元素又禁止它
6. **对中差异**：MJ 的 `--no` 效果较弱，SD 的独立文本框效果强劲
