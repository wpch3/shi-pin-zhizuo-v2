#!/usr/bin/env python3
"""
Build Upgraded Chapter 01 for v3 comic: 《婚书截胡篇》（四幕光影递进 + 幼年小满重塑 + 古风实景版）
Renders at 1440x2580 (9:16 vertical 2K) with 2x supersampling:
- Hand-inked top status bars (亲情度: 100% -> shattered 爱情度: MAX / 亲情度: 0%)
- Page 4 hand-inked rice-paper choice boxes (1.盖章婚书 / 2.撕掉退婚书 / 3.两份全盖)
- Seamless linked double-bubbles & split two-beat male-lead POV boxes
"""
import io
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import img2pdf

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "art" / "v3-chapter-01"
OUT_DIR = ROOT / "deliverables" / "v3-chapter-01"
FONT_BOLD = ROOT / ".cache" / "fonts" / "NotoSansCJKsc-Bold.otf"
FONT_REG = ROOT / ".cache" / "fonts" / "NotoSansCJKsc-Regular.otf"

TARGET_W, TARGET_H = 1440, 2580
SS = 2

PAPER_FILL = (250, 245, 235, 248)
POV_FILL = (248, 243, 232, 246)
CHOICE_FILL = (244, 240, 230, 246)
BORDER_COLOR = (28, 25, 22, 255)
TEXT_COLOR = (26, 23, 20, 255)
CRIMSON_TEXT = (146, 26, 28, 255)


def load_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REG), size * SS)


def measure_multiline(draw: ImageDraw.ImageDraw, lines: list[str], font: ImageFont.FreeTypeFont, line_gap: int):
    widths, heights = [], []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        widths.append(bbox[2] - bbox[0])
        heights.append(bbox[3] - bbox[1])
    total_w = max(widths) if widths else 0
    step_h = max(heights) if heights else 0
    total_h = step_h * len(lines) + (line_gap * SS) * max(0, len(lines) - 1)
    return total_w, total_h, step_h


def draw_centered_lines(draw: ImageDraw.ImageDraw, cx: float, cy: float, lines: list[str], font: ImageFont.FreeTypeFont, line_gap: int = 12, color=TEXT_COLOR):
    _, total_h, step_h = measure_multiline(draw, lines, font, line_gap)
    start_y = cy - total_h / 2.0
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        lw = bbox[2] - bbox[0]
        y_pos = start_y + i * (step_h + line_gap * SS) - bbox[1]
        x_pos = cx - lw / 2.0 - bbox[0]
        draw.text((x_pos, y_pos), line, font=font, fill=color)


def draw_text_with_soft_halo(overlay: Image.Image, cx: float, cy: float, text: str, font: ImageFont.FreeTypeFont, fill, halo_rgba=(248, 244, 235, 245)):
    """Crisp thin rice-paper outline around floating HUD text—100% legible over dark wood or bright sky with zero blurry glow."""
    d = ImageDraw.Draw(overlay)
    sw = int(round(3.2 * SS))
    bbox = d.textbbox((0, 0), text, font=font, stroke_width=sw)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = cx - tw / 2.0 - bbox[0]
    y = cy - th / 2.0 - bbox[1]
    d.text((x, y), text, font=font, fill=fill, stroke_width=sw, stroke_fill=halo_rgba)


def draw_sketchy_rect(draw: ImageDraw.ImageDraw, x1: float, y1: float, x2: float, y2: float, fill, stroke_w: int):
    """Double-pass hand-inked rectangle matching the sketchy manga style."""
    draw.rectangle([x1, y1, x2, y2], fill=fill, outline=BORDER_COLOR, width=stroke_w)
    # Subtle second sketchy ink pass slightly offset for authentic hand-drawn feel
    off = max(2, stroke_w // 3)
    draw.line([(x1 - off, y1 + off), (x2 + off, y1 - off)], fill=(35, 32, 28, 190), width=max(2, stroke_w // 2))
    draw.line([(x1 + off, y2 + off), (x2 - off, y2 - off)], fill=(35, 32, 28, 190), width=max(2, stroke_w // 2))


def draw_status_bar(overlay: Image.Image, spec: dict):
    """
    Modes:
    - 'full_100': 亲情度：100% + full luminous jade-silver bar
    - 'shattered_max': 爱情度：MAX (crimson) + 亲情度：0% + cracked snapped bar in middle
    - 'compact_split': 亲情度：0% ｜ 爱情度：MAX + crimson-glow bar (upper-left on Page 4)
    """
    mode = spec["mode"]
    cx = spec["cx"] * SS
    stroke = int(round(3.6 * SS))
    draw = ImageDraw.Draw(overlay)

    if mode == "full_100":
        ty = spec["text_y"] * SS
        font = load_font(48)
        draw_text_with_soft_halo(overlay, cx, ty, "亲情度：100%", font, TEXT_COLOR)
        draw = ImageDraw.Draw(overlay)
        bw, bh = 620 * SS, 42 * SS
        bx1, by1 = cx - bw / 2, ty + 48 * SS
        bx2, by2 = cx + bw / 2, by1 + bh
        draw_sketchy_rect(draw, bx1, by1, bx2, by2, fill=(215, 224, 228, 235), stroke_w=stroke)
        # Inner soft highlight strip
        draw.rounded_rectangle([bx1 + 10 * SS, by1 + 8 * SS, bx2 - 10 * SS, by2 - 10 * SS], radius=8 * SS, fill=(242, 247, 249, 225))

    elif mode == "shattered_max":
        y_love = spec["love_y"] * SS
        y_kin = spec["kin_y"] * SS
        f_love = load_font(54)
        f_kin = load_font(44)
        draw_text_with_soft_halo(overlay, cx, y_love, "爱情度：MAX", f_love, CRIMSON_TEXT)
        draw_text_with_soft_halo(overlay, cx, y_kin, "亲情度：0%", f_kin, TEXT_COLOR)
        draw = ImageDraw.Draw(overlay)

        bw, bh = 640 * SS, 42 * SS
        bx1, by1 = cx - bw / 2, y_kin + 46 * SS
        bx2, by2 = cx + bw / 2, by1 + bh
        gap = 14 * SS

        # Left broken half (tilted slightly)
        l_pts = [
            (bx1, by1),
            (cx - gap, by1 + 3 * SS),
            (cx - gap - 14 * SS, (by1 + by2) / 2),
            (cx - gap + 4 * SS, by2 + 2 * SS),
            (bx1, by2),
        ]
        # Right broken half
        r_pts = [
            (cx + gap + 4 * SS, by1 + 2 * SS),
            (bx2, by1),
            (bx2, by2),
            (cx + gap + 12 * SS, by2),
            (cx + gap - 10 * SS, (by1 + by2) / 2),
        ]
        draw.polygon(l_pts, fill=(208, 214, 218, 225), outline=BORDER_COLOR, width=stroke)
        draw.polygon(r_pts, fill=(208, 214, 218, 225), outline=BORDER_COLOR, width=stroke)
        # Tiny red residual sliver on far left
        draw.rectangle([bx1 + stroke, by1 + stroke, bx1 + 16 * SS, by2 - stroke], fill=(165, 42, 42, 235))
        # Crack lines & flying shards around break
        crack_w = max(2, stroke // 2)
        draw.line([(cx - gap - 14 * SS, (by1 + by2) / 2), (cx - 58 * SS, by1 + 10 * SS)], fill=BORDER_COLOR, width=crack_w)
        draw.line([(cx - 36 * SS, by1 + 18 * SS), (cx - 72 * SS, by2 - 8 * SS)], fill=BORDER_COLOR, width=crack_w)
        draw.line([(cx + gap - 10 * SS, (by1 + by2) / 2), (cx + 56 * SS, by1 + 12 * SS)], fill=BORDER_COLOR, width=crack_w)
        draw.line([(cx + 32 * SS, by1 + 16 * SS), (cx + 68 * SS, by2 - 9 * SS)], fill=BORDER_COLOR, width=crack_w)
        # Small flying shards above/below break
        draw.polygon([(cx - 6 * SS, by1 - 18 * SS), (cx + 6 * SS, by1 - 28 * SS), (cx + 2 * SS, by1 - 8 * SS)], fill=(215, 220, 224, 230), outline=BORDER_COLOR, width=crack_w)
        draw.polygon([(cx + 10 * SS, by2 + 12 * SS), (cx + 22 * SS, by2 + 24 * SS), (cx + 4 * SS, by2 + 22 * SS)], fill=(215, 220, 224, 230), outline=BORDER_COLOR, width=crack_w)

    elif mode == "compact_split":
        ty = spec["text_y"] * SS
        f_bar = load_font(38)
        # Render "亲情度：0% ｜ " in dark ink + "爱情度：MAX" in crimson side by side!
        part1 = "亲情度：0% ｜ "
        part2 = "爱情度：MAX"
        b1 = draw.textbbox((0, 0), part1, font=f_bar)
        b2 = draw.textbbox((0, 0), part2, font=f_bar)
        w1, w2 = b1[2] - b1[0], b2[2] - b2[0]
        total_w = w1 + w2
        c1 = cx - total_w / 2.0 + w1 / 2.0
        c2 = cx - total_w / 2.0 + w1 + w2 / 2.0
        draw_text_with_soft_halo(overlay, c1, ty, part1, f_bar, TEXT_COLOR)
        draw_text_with_soft_halo(overlay, c2, ty, part2, f_bar, CRIMSON_TEXT)
        draw = ImageDraw.Draw(overlay)

        bw, bh = 460 * SS, 32 * SS
        bx1, by1 = cx - bw / 2, ty + 38 * SS
        bx2, by2 = cx + bw / 2, by1 + bh
        draw_sketchy_rect(draw, bx1, by1, bx2, by2, fill=(196, 188, 186, 220), stroke_w=int(round(3.2 * SS)))
        # Subtle crimson MAX aura bar inside
        draw.rectangle([bx1 + 6 * SS, by1 + 6 * SS, bx1 + 26 * SS, by2 - 6 * SS], fill=(162, 38, 40, 235))


def draw_choice_boxes(overlay: Image.Image, boxes_spec: list[dict]):
    draw = ImageDraw.Draw(overlay)
    stroke = int(round(3.8 * SS))
    font = load_font(44)
    for item in boxes_spec:
        x1, y1, x2, y2 = [v * SS for v in item["box"]]
        # Slight hand-drawn organic tilt polygon (1-2px hand-inked paper feel)
        pts = [
            (x1 + 3 * SS, y1 + 2 * SS),
            (x2, y1),
            (x2 - 3 * SS, y2 - 2 * SS),
            (x1, y2),
        ]
        draw.polygon(pts, fill=CHOICE_FILL, outline=BORDER_COLOR, width=stroke)
        draw_centered_lines(draw, (x1 + x2) / 2.0, (y1 + y2) / 2.0, [item["label"]], font)


def draw_oval_bubble(
    overlay: Image.Image,
    box: tuple[int, int, int, int],
    lines: list[str],
    tail_tip: tuple[int, int],
    tail_base_angle_deg: float,
    font_size: int = 34,
    tail_half_deg: float = 9.0,
):
    x1, y1, x2, y2 = [v * SS for v in box]
    cx, cy = (x1 + x2) / 2.0, (y1 + y2) / 2.0
    rx, ry = (x2 - x1) / 2.0, (y2 - y1) / 2.0
    tx, ty = tail_tip[0] * SS, tail_tip[1] * SS
    stroke = int(round(3.8 * SS))

    a0 = math.radians(tail_base_angle_deg - tail_half_deg)
    a1 = math.radians(tail_base_angle_deg + tail_half_deg)
    p0 = (cx + rx * 0.92 * math.cos(a0), cy + ry * 0.92 * math.sin(a0))
    p1 = (cx + rx * 0.92 * math.cos(a1), cy + ry * 0.92 * math.sin(a1))

    layer = Image.new("RGBA", overlay.size, (0, 0, 0, 0))
    ldraw = ImageDraw.Draw(layer)
    ldraw.ellipse([x1 - stroke, y1 - stroke, x2 + stroke, y2 + stroke], fill=BORDER_COLOR)
    ldraw.polygon([p0, (tx, ty), p1], fill=BORDER_COLOR)
    ldraw.line([p0, (tx, ty), p1], fill=BORDER_COLOR, width=stroke * 2, joint="curve")

    def shift_edge_inward(pa, pb, interior_pt, dist):
        vx, vy = pb[0] - pa[0], pb[1] - pa[1]
        length = math.hypot(vx, vy) or 1.0
        nx, ny = -vy / length, vx / length
        if (interior_pt[0] - pa[0]) * nx + (interior_pt[1] - pa[1]) * ny < 0:
            nx, ny = -nx, -ny
        return (pa[0] + nx * dist, pa[1] + ny * dist), (pb[0] + nx * dist, pb[1] + ny * dist)

    def line_intersect(a1_, a2_, b1_, b2_):
        x1_, y1_ = a1_
        x2_, y2_ = a2_
        x3_, y3_ = b1_
        x4_, y4_ = b2_
        den = (x1_ - x2_) * (y3_ - y4_) - (y1_ - y2_) * (x3_ - x4_)
        if abs(den) < 1e-6:
            return ((a2_[0] + b2_[0]) / 2, (a2_[1] + b2_[1]) / 2)
        px_ = ((x1_ * y2_ - y1_ * x2_) * (x3_ - x4_) - (x1_ - x2_) * (x3_ * y4_ - y3_ * x4_)) / den
        py_ = ((x1_ * y2_ - y1_ * x2_) * (y3_ - y4_) - (y1_ - y2_) * (x3_ * y4_ - y3_ * x4_)) / den
        return (px_, py_)

    mid_base = ((p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0)
    e0_a, e0_b = shift_edge_inward(p0, (tx, ty), mid_base, stroke)
    e1_a, e1_b = shift_edge_inward(p1, (tx, ty), mid_base, stroke)
    inner_tip = line_intersect(e0_a, e0_b, e1_a, e1_b)

    ldraw.ellipse([x1, y1, x2, y2], fill=PAPER_FILL)
    ldraw.polygon([e0_a, inner_tip, e1_a], fill=PAPER_FILL)
    overlay.alpha_composite(layer)

    draw = ImageDraw.Draw(overlay)
    font = load_font(font_size)
    draw_centered_lines(draw, cx, cy, lines, font, line_gap=12)


def draw_pov_box(
    overlay: Image.Image,
    x_anchor: int,
    y1: int,
    lines: list[str],
    font_size: int = 33,
    pad_x: int = 32,
    pad_y: int = 19,
    align_box: str = "center",
):
    draw = ImageDraw.Draw(overlay)
    font = load_font(font_size)
    line_gap = 11
    tw, th, _ = measure_multiline(draw, lines, font, line_gap)
    bw = tw + 2 * pad_x * SS
    bh = th + 2 * pad_y * SS

    if align_box == "left":
        bx1 = x_anchor * SS
        bx2 = bx1 + bw
    elif align_box == "right":
        bx2 = x_anchor * SS
        bx1 = bx2 - bw
    else:
        bx1 = x_anchor * SS - bw / 2.0
        bx2 = x_anchor * SS + bw / 2.0
    by1 = y1 * SS
    by2 = by1 + bh

    stroke = int(round(3.8 * SS))
    radius = int(round(20 * SS))
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=radius, fill=POV_FILL, outline=BORDER_COLOR, width=stroke)
    draw_centered_lines(draw, (bx1 + bx2) / 2.0, (by1 + by2) / 2.0, lines, font, line_gap=line_gap)


PAGES = [
    {
        # Page 1: 童年回忆 · 青暮暖灯 · 幼态小团子 (1440 x 2580)
        "raw": "raw-01.png",
        "out": "page-01.png",
        "status_bar": {"mode": "full_100", "cx": 760, "text_y": 215},
        "pov_boxes": [
            {
                "x": 720,
                "y1": 38,
                "lines": ["那时候她刚来家里不久，话很少，总喜欢抓着我的袖子不放"],
                "font_size": 34,
                "align_box": "center",
            },
        ],
        "bubbles": [
            {
                "box": (60, 2045, 865, 2450),
                "lines": ["哥哥……", "以后我也会一直待在", "你身边的，对吧？"],
                "tail_tip": (685, 1955),
                "tail_angle": -58,
                "font_size": 37,
            },
        ],
        "choices": [],
    },
    {
        # Page 2: 门前错交婚书 · 清朗白昼门庭 (1440 x 2580)
        "raw": "raw-02.png",
        "out": "page-02.png",
        "status_bar": {"mode": "full_100", "cx": 720, "text_y": 125},
        "pov_boxes": [],
        "bubbles": [
            {
                "box": (26, 285, 695, 550),
                "lines": ["那、那个……这是两家定好的婚书，", "我才不是特意跑一趟呢！"],
                "tail_tip": (405, 608),
                "tail_angle": 82,
                "font_size": 31,
            },
            {
                "box": (28, 1945, 715, 2240),
                "lines": ["你拿进去签好名字就行，", "我先走了……"],
                "tail_tip": (365, 1860),
                "tail_angle": -92,
                "font_size": 34,
            },
            {
                "box": (725, 2195, 1414, 2530),
                "lines": ["嗯，只要签上名字按好手印", "就行了，对吧？", "谢谢姐姐，我会转交的。"],
                "tail_tip": (1075, 2105),
                "tail_angle": -88,
                "font_size": 32,
            },
        ],
        "choices": [],
    },
    {
        # Page 3: 亲情归零·按手印截胡 · 书房窗影聚光 (1440 x 2580)
        "raw": "raw-03.png",
        "out": "page-03.png",
        "status_bar": {"mode": "shattered_max", "cx": 720, "love_y": 96, "kin_y": 190},
        "pov_boxes": [
            {
                "x": 28,
                "y1": 1358,
                "lines": ["等等……小满，我刚才以为只是普通文书，", "你怎么把自己的名字也签上去了？"],
                "font_size": 29,
                "align_box": "left",
            },
            {
                "x": 28,
                "y1": 1528,
                "lines": ["还有，你这亲情度怎么突然掉成 0 了？"],
                "font_size": 30,
                "align_box": "left",
            },
        ],
        "bubbles": [
            {
                "box": (785, 1920, 1418, 2365),
                "lines": ["因为按完手印之后，", "我就不是以妹妹的身份", "喜欢哥哥了呀。"],
                "tail_tip": (1015, 1805),
                "tail_angle": -105,
                "font_size": 35,
            },
        ],
        "choices": [],
    },
    {
        # Page 4: 退婚修罗场 · 厅堂冷暖对照 (1440 x 2580)
        "raw": "raw-04.png",
        "out": "page-04.png",
        "status_bar": {"mode": "compact_split", "cx": 405, "text_y": 385},
        "bubbles": [
            {
                "box": (780, 28, 1412, 276),
                "lines": ["哪有这样的啊……", "明明是我先拿来的婚书……"],
                "tail_tip": (1096, 345),
                "tail_angle": 90,
                "font_size": 32,
                "bridge_only": True,
            },
            {
                "box": (774, 310, 1416, 580),
                "lines": ["不管了，你要是不给我个说法，", "这婚我真退了啊！"],
                "tail_tip": (1100, 632),
                "tail_angle": 90,
                "font_size": 31,
            },
            {
                "box": (20, 1392, 650, 1612),
                "lines": ["哥哥，族规说落印就不能反悔了哦。", "不过……印章现在在你手里呢。"],
                "tail_tip": (315, 1336),
                "tail_angle": -92,
                "font_size": 27,
            },
        ],
        "pov_boxes": [
            {
                "x": 1070,
                "y1": 1648,
                "lines": ["左边是刚变成零的亲情度，", "右边是眼泪快掉下来的退婚书……"],
                "font_size": 29,
                "align_box": "center",
            },
            {
                "x": 1070,
                "y1": 1802,
                "lines": ["这印章，到底该往哪边盖？"],
                "font_size": 31,
                "align_box": "center",
            },
        ],
        "choices": [
            {"box": (758, 1922, 1384, 2088), "label": "1. 盖章婚书"},
            {"box": (758, 2132, 1384, 2298), "label": "2. 撕掉退婚书"},
            {"box": (758, 2342, 1384, 2508), "label": "3. 两份全盖"},
        ],
    },
]


def render_page(spec: dict) -> Path:
    raw_im = Image.open(RAW_DIR / spec["raw"]).convert("RGBA")
    base = raw_im.resize((TARGET_W, TARGET_H), Image.LANCZOS)
    overlay = Image.new("RGBA", (TARGET_W * SS, TARGET_H * SS), (0, 0, 0, 0))

    if spec.get("status_bar"):
        draw_status_bar(overlay, spec["status_bar"])

    if spec.get("choices"):
        draw_choice_boxes(overlay, spec["choices"])

    bubbles = spec["bubbles"]
    i = 0
    while i < len(bubbles):
        b = bubbles[i]
        if b.get("bridge_only") and i + 1 < len(bubbles):
            b_next = bubbles[i + 1]
            stroke = int(round(3.8 * SS))
            layer = Image.new("RGBA", overlay.size, (0, 0, 0, 0))
            ldraw = ImageDraw.Draw(layer)

            x1a, y1a, x2a, y2a = [v * SS for v in b["box"]]
            x1b, y1b, x2b, y2b = [v * SS for v in b_next["box"]]
            cxb, cyb = (x1b + x2b) / 2.0, (y1b + y2b) / 2.0
            rxb, ryb = (x2b - x1b) / 2.0, (y2b - y1b) / 2.0
            tx, ty = b_next["tail_tip"][0] * SS, b_next["tail_tip"][1] * SS
            a0 = math.radians(b_next["tail_angle"] - 9.0)
            a1 = math.radians(b_next["tail_angle"] + 9.0)
            p0 = (cxb + rxb * 0.92 * math.cos(a0), cyb + ryb * 0.92 * math.sin(a0))
            p1 = (cxb + rxb * 0.92 * math.cos(a1), cyb + ryb * 0.92 * math.sin(a1))
            bx_mid = ((x1a + x2a) / 2.0 + (x1b + x2b) / 2.0) / 2.0
            bw_half = 22 * SS

            ldraw.ellipse([x1a - stroke, y1a - stroke, x2a + stroke, y2a + stroke], fill=BORDER_COLOR)
            ldraw.ellipse([x1b - stroke, y1b - stroke, x2b + stroke, y2b + stroke], fill=BORDER_COLOR)
            ldraw.rectangle([bx_mid - bw_half - stroke, y2a - 28 * SS, bx_mid + bw_half + stroke, y1b + 28 * SS], fill=BORDER_COLOR)
            ldraw.polygon([p0, (tx, ty), p1], fill=BORDER_COLOR)
            ldraw.line([p0, (tx, ty), p1], fill=BORDER_COLOR, width=stroke * 2, joint="curve")

            ldraw.ellipse([x1a, y1a, x2a, y2a], fill=PAPER_FILL)
            ldraw.ellipse([x1b, y1b, x2b, y2b], fill=PAPER_FILL)
            ldraw.rectangle([bx_mid - bw_half, y2a - 28 * SS, bx_mid + bw_half, y1b + 28 * SS], fill=PAPER_FILL)
            ldraw.polygon([(p0[0] + stroke * 0.9, p0[1]), (tx, ty - stroke * 1.9), (p1[0] - stroke * 0.9, p1[1])], fill=PAPER_FILL)
            overlay.alpha_composite(layer)

            draw = ImageDraw.Draw(overlay)
            draw_centered_lines(draw, (x1a + x2a) / 2.0, (y1a + y2a) / 2.0, b["lines"], load_font(b["font_size"]), line_gap=12)
            draw_centered_lines(draw, cxb, cyb, b_next["lines"], load_font(b_next["font_size"]), line_gap=12)
            i += 2
        else:
            draw_oval_bubble(
                overlay,
                box=b["box"],
                lines=b["lines"],
                tail_tip=b["tail_tip"],
                tail_base_angle_deg=b["tail_angle"],
                font_size=b["font_size"],
            )
            i += 1

    for pbox in spec["pov_boxes"]:
        draw_pov_box(
            overlay,
            x_anchor=pbox["x"],
            y1=pbox["y1"],
            lines=pbox["lines"],
            font_size=pbox["font_size"],
            align_box=pbox["align_box"],
        )

    overlay_down = overlay.resize((TARGET_W, TARGET_H), Image.LANCZOS)
    final_im = Image.alpha_composite(base, overlay_down).convert("RGB")
    out_path = OUT_DIR / spec["out"]
    final_im.save(out_path, optimize=True)
    return out_path


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rendered = [render_page(spec) for spec in PAGES]
    jpg_streams = []
    for p in rendered:
        buf = io.BytesIO()
        Image.open(p).save(buf, format="JPEG", quality=95, subsampling=0)
        jpg_streams.append(buf.getvalue())
    pdf_path = OUT_DIR / "婚书截胡篇_完整漫画.pdf"
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(jpg_streams))
    print("Generated upgraded v3:", [str(p) for p in rendered], "->", pdf_path)


if __name__ == "__main__":
    main()
