# shi-pin-zhizuo-v2 竖屏漫画制作

> 编号约定：`v2` 为系列名；`lv1` = 《陪妹妹出门约会》这本漫画（第 1、2 话已完成）；`lv2` = 另一本全新漫画（筹备中）。

## 一、正式交付目录

### 1. `v2 · lv1` 第 1 话：《陪妹妹出门约会》
- **角色定稿立绘**：`new_character.png`
- **角色正式设定卡**：`deliverables/v2-chapter-01/character-card-xiaomian.png`
- **无字原画归档**：`art/chapter-01/raw-01.png` ～ `raw-04.png`
- **3:4 高清阅读与运镜版（1440×1920）**：
  - `deliverables/v2-chapter-01/page-01.png` ～ `page-04.png`
  - `deliverables/v2-chapter-01/陪妹妹出门约会_第一话.pdf`
- **9:16 B 站竖屏视频直导版（1080×1920，已预留底部进度条安全区）**：
  - `deliverables/v2-chapter-01-vertical/page-01.png` ～ `page-04.png`
  - `deliverables/v2-chapter-01-vertical/陪妹妹出门约会_9x16竖屏视频版.pdf`

### 2. `v2 · lv1` 第 2 话：《陪妹妹出门约会 2 · 不否认的那句》
- **无字原画归档**：`art/v2-chapter-02/raw-01.png` ～ `raw-04.png`（画风与角色完全沿用第 1 话）
- **3:4 高清阅读与运镜版（1440×1920）**：
  - `deliverables/v2-chapter-02/page-01.png` ～ `page-04.png`
  - `deliverables/v2-chapter-02/陪妹妹出门约会_第二话.pdf`
- **9:16 B 站竖屏视频直导版（1080×1920）**：
  - `deliverables/v2-chapter-02-vertical/page-01.png` ～ `page-04.png`
  - `deliverables/v2-chapter-02-vertical/陪妹妹出门约会_第二话_9x16竖屏视频版.pdf`
- 剧情：不新增角色，用一句误认把「妹妹」称呼轻轻推松，男主两问两答各自独立成框，末句留第三话钩子。

### 3. `v3` 四页全面重制升级版：《婚书截胡篇》（四幕光影递进 + 幼年小满重塑 + 古风实景）
- **无字原画归档**：`art/v3-chapter-01/raw-01.png` ～ `raw-04.png`
- **9:16 竖屏高清成品（1440×2580，含手绘风数值条/碎裂特效、宣纸选项框与分句气泡）**：
  - `deliverables/v3-chapter-01/page-01.png` ～ `page-04.png`
  - `deliverables/v3-chapter-01/婚书截胡篇_完整漫画.pdf`

### 4. `v2 · lv2` 新漫画筹备（全新角色，与 lv1 剧情独立）
- **角色定稿立绘**：`new_character_lv2.png`（阿澄，用户从两版候选中选定第 2 版）
- **角色正式设定卡**：`deliverables/v2-lv2/character-card-acheng.png`
- 外貌反差：深栗／黑茶色齐肩内扣短发、上挑细长眼、暖琥珀瞳、雾蓝衬衫＋浅灰针织背心、细金属框眼镜；画风仍以 `new_character.png` 为锚。
- 第 1 话《一起躲雨的书店》台词草案：`docs/v2_lv2_第一话脚本草案.md`（整话原画待画风确认后生成）。

### 5. 台词脚本与企划文档
- `docs/定稿台词与B站视频剪辑对照表.md`：`v2 · lv1` 第 1、2 话与 `v3` 全页定稿分框台词、配乐建议、剪映每页停留秒数与运镜对照表。
- `docs/v2_人设与第一话脚本草案.md`：`v2 · lv1` 小眠人设与高甜互动脚本。
- `docs/v2_lv1_后续剧情提案.md`：第 2 话《不否认的那句》分镜、台词与交付清单。
- `docs/v2_lv2_新角色企划.md`：`v2 · lv2` 新角色方向、外貌反差与画风锁定。
- `docs/v2_lv2_第一话脚本草案.md`：`v2 · lv2` 第 1 话 4 页分镜与分框台词草案。
- `docs/v3_视觉诊断与优化方案.md`：`v3` 光影递进与第 1 页幼态重塑方案记录。

## 二、排版与构建脚本

- `scripts/build_v2_chapter01.py`：`v2 · lv1` 第 1 话留白定制排版与 PDF 导出（提供可复用的手绘气泡／标题框／分框绘制函数）。
- `scripts/build_v2_chapter02.py`：`v2 · lv1` 第 2 话排版与 PDF 导出（复用第 1 话绘制函数）。
- `scripts/build_extras.py`：小眠角色设定卡与第 1 话 9:16 竖屏视频安全区版本构建（提供暖纸纹画布函数）。
- `scripts/build_extras_lv1_ch02.py`：第 2 话 9:16 竖屏视频安全区版本构建。
- `scripts/build_extras_lv2.py`：`v2 · lv2` 阿澄角色设定卡构建。
- `scripts/build_v3_chapter01.py`：`v3` 重制版数值条、互动选项框、连体双气泡与分句对话框排版。
