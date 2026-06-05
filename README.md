# OpenClaw Skills by mayf3

A collection of original, handcrafted skills for [OpenClaw](https://github.com/openclaw/openclaw) AI agents.

These skills are designed to be practical, well-structured, and ready to use. Each skill follows the [AgentSkills specification](https://docs.openclaw.ai).

## Skills

### 🌐 Browser Automation

| Skill | Description |
|-------|-------------|
| [brave-browser-agent](skills/brave-browser-agent/) | Control Brave Browser via CDP — content extraction, screenshots, JS execution, anti-detection clicks, React/Vue framework-aware interaction |
| [gpt-image-gen](skills/gpt-image-gen/) | Generate images with ChatGPT's GPT-Image-2 via browser automation |
| [gemini-image-gen](skills/gemini-image-gen/) | Generate images with Google Gemini's free Imagen via browser automation |
| [add-to-cart](skills/add-to-cart/) | Multi-platform add-to-cart automation (Taobao, JD, Pinduoduo, Xianyu) via CDP |

### 🔍 Search & Research

| Skill | Description |
|-------|-------------|
| [smart-search](skills/smart-search/) | Multi-engine parallel search with auto-fallback, result parsing, and quality scoring |

### 🎨 Image Prompt Engineering

| Skill | Description |
|-------|-------------|
| [image-prompt-engineer](skills/image-prompt-engineer/) | Craft and optimize prompts for Midjourney, Stable Diffusion, DALL-E, Flux |
| [ai-image-prompt](skills/ai-image-prompt/) | AI image prompt optimization with anti-AI-detection and realism enhancement |

### 📚 Learning & Knowledge

| Skill | Description |
|-------|-------------|
| [daily-learning](skills/daily-learning/) | Standardized daily learning framework — study → notes → wiki ingestion → review |
| [learning-review](skills/learning-review/) | Post-learning review, weekly internalization, and application tracking |

### 🛒 Daily Utilities

| Skill | Description |
|-------|-------------|
| [shopping-list](skills/shopping-list/) | Persistent shopping list management with categories, priorities, and store tracking |

## Installation

Each skill can be installed individually. Choose one:

**Option A: Clone the whole repo**
```bash
git clone https://github.com/mayf3/openclaw-skills.git
# Then copy or symlink desired skills to your OpenClaw workspace
```

**Option B: Copy a single skill**
```bash
# Copy to your workspace skills directory
cp -r skills/<skill-name> ~/.openclaw/skills/
```

## Dependencies

Some skills depend on others:

- `gpt-image-gen`, `gemini-image-gen`, `add-to-cart` → require `brave-browser-agent`
- `daily-learning` → optionally uses `smart-search` for research
- `learning-review` → designed as companion to `daily-learning`

## License

MIT

## Contributing

These are personal skills shared for the community. Issues and suggestions welcome!
