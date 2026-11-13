# shi-pin-zhizuo-v2 竖屏漫画制作

## 一、正式交付目录

### 1. `v2` 新角色原创第一话：《陪妹妹出门约会》
- **角色定稿立绘**：`new_character.png`
- **角色正式设定卡**：`deliverables/v2-chapter-01/character-card-xiaomian.png`
- **无字原画归档**：`art/chapter-01/raw-01.png` ～ `raw-04.png`
- **3:4 高清阅读与运镜版（1440×1920）**：
  - `deliverables/v2-chapter-01/page-01.png` ～ `page-04.png`
  - `deliverables/v2-chapter-01/陪妹妹出门约会_第一话.pdf`
- **9:16 B 站竖屏视频直导版（1080×1920，已预留底部进度条安全区）**：
  - `deliverables/v2-chapter-01-vertical/page-01.png` ～ `page-04.png`
  - `deliverables/v2-chapter-01-vertical/陪妹妹出门约会_9x16竖屏视频版.pdf`

### 2. `v3` 四页全面重制升级版：《婚书截胡篇》（四幕光影递进 + 幼年小满重塑 + 古风实景）
- **无字原画归档**：`art/v3-chapter-01/raw-01.png` ～ `raw-04.png`
- **9:16 竖屏高清成品（1440×2580，含手绘风数值条/碎裂特效、宣纸选项框与分句气泡）**：
  - `deliverables/v3-chapter-01/page-01.png` ～ `page-04.png`
  - `deliverables/v3-chapter-01/婚书截胡篇_完整漫画.pdf`

### 3. 台词脚本与视频剪辑文档
- `docs/定稿台词与B站视频剪辑对照表.md`：`v2` 与 `v3` 全页定稿分框台词、配乐建议、剪映每页停留秒数与运镜对照表。
- `docs/v2_人设与第一话脚本草案.md`：`v2` 小眠人设与高甜互动脚本。
- `docs/v3_视觉诊断与优化方案.md`：`v3` 光影递进与第 1 页幼态重塑方案记录。

## 二、排版与构建脚本

- `scripts/build_v2_chapter01.py`：`v2` 第一话留白定制排版与 PDF 导出。
- `scripts/build_v3_chapter01.py`：`v3` 重制版数值条、互动选项框、连体双气泡与分句对话框排版。
- `scripts/build_extras.py`：小眠角色设定卡与 `v2` 9:16 竖屏视频安全区版本构建。
