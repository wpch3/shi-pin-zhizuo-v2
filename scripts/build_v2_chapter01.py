#!/usr/bin/env python3
"""
Build Chapter 01 of shi-pin-zhizuo-v2: 《陪妹妹出门约会》
4 vertical POV comic pages (1440x1920, 3:4) + combined PDF.
All coordinates are custom-fitted per page around faces, flower hairclip, hands, and props.
Multi-beat male-lead responses use TWO separate rounded dialogue boxes per user specification.
"""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import img2pdf

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "art" / "chapter-01"
OUT_DIR = ROOT / "deliverables" / "v2-chapter-01"
FONT_BOLD = ROOT / ".cache" / "fonts" / "NotoSansCJKsc-Bold.otf"
FONT_REG = ROOT / ".cache" / "fonts" / "NotoSansCJKsc-Regular.otf"

TARGET_W, TARGET_H = 1440, 1920
SS = 2  # 2x supersampling for crisp anti-aliased vector borders & bubble tails

PAPER_FILL = (250, 245, 234, 250)      # Warm ivory comic bubble fill (#FAF5EA)
BOX_FILL = (250, 244, 232, 248)        # Warm cream box fill for title & POV boxes
BORDER_COLOR = (30, 26, 23, 255)       # Crisp dark charcoal ink border
TEXT_COLOR = (28, 24, 21, 255)         # Deep warm ink text


def load_font(bold: bool, size: int) -> ImageFont.FreeTypeFont:
    path = FONT_BOLD if bold else FONT_REG
    return ImageFont.truetype(str(path), size * SS)


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


def draw_centered_lines(
    draw: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    lines: list[str],
    font: ImageFont.FreeTypeFont,
    line_gap: int = 12,
    align: str = "center",
):
    total_w, total_h, step_h = measure_multiline(draw, lines, font, line_gap)
    start_y = cy - total_h / 2.0
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        lw = bbox[2] - bbox[0]
        y_pos = start_y + i * (step_h + line_gap * SS) - bbox[1]
        if align == "left":
            x_pos = cx - total_w / 2.0 - bbox[0]
        else:
            x_pos = cx - lw / 2.0 - bbox[0]
        draw.text((x_pos, y_pos), line, font=font, fill=TEXT_COLOR)


def draw_title_box(overlay: Image.Image, x1: int, y1: int, lines: list[str], font_size: int = 34):
    draw = ImageDraw.Draw(overlay)
    font = load_font(True, font_size)
    line_gap = 12
    tw, th, _ = measure_multiline(draw, lines, font, line_gap)
    pad_x, pad_y = 30 * SS, 22 * SS
    bx1, by1 = x1 * SS, y1 * SS
    bx2, by2 = bx1 + tw + 2 * pad_x, by1 + th + 2 * pad_y
    stroke = int(round(3.6 * SS))
    draw.rectangle([bx1, by1, bx2, by2], fill=BOX_FILL, outline=BORDER_COLOR, width=stroke)
    draw_centered_lines(draw, (bx1 + bx2) / 2, (by1 + by2) / 2, lines, font, line_gap=line_gap, align="left")


def draw_oval_bubble(
    overlay: Image.Image,
    box: tuple[int, int, int, int],
    lines: list[str],
    tail_tip: tuple[int, int],
    tail_base_angle_deg: float,
    font_size: int = 33,
    tail_half_deg: float = 9.5,
):
    """
    Draw a clean anti-aliased oval speech bubble with a seamless pointed tail
    (no internal border seam across the base of the tail).
    """
    x1, y1, x2, y2 = [v * SS for v in box]
    cx, cy = (x1 + x2) / 2.0, (y1 + y2) / 2.0
    rx, ry = (x2 - x1) / 2.0, (y2 - y1) / 2.0
    tx, ty = tail_tip[0] * SS, tail_tip[1] * SS
    stroke = int(round(3.6 * SS))

    # Build shape mask at SS resolution: union of ellipse + curved/pointed tail triangle
    a0 = math.radians(tail_base_angle_deg - tail_half_deg)
    a1 = math.radians(tail_base_angle_deg + tail_half_deg)
    # Inset base points slightly inside ellipse so union is 100% seamless
    p0 = (cx + rx * 0.92 * math.cos(a0), cy + ry * 0.92 * math.sin(a0))
    p1 = (cx + rx * 0.92 * math.cos(a1), cy + ry * 0.92 * math.sin(a1))

    # Create binary mask of outer shape, then erode or draw border cleanly
    layer = Image.new("RGBA", overlay.size, (0, 0, 0, 0))
    ldraw = ImageDraw.Draw(layer)

    # First draw outer black silhouette (expanded by stroke) then inner cream fill!
    # For crisp uniform stroke around both ellipse and tail:
    # Step 1: Draw black ellipse + black tail polygon with thick outline
    ldraw.ellipse([x1 - stroke, y1 - stroke, x2 + stroke, y2 + stroke], fill=BORDER_COLOR)
    ldraw.polygon([p0, (tx, ty), p1], fill=BORDER_COLOR)
    ldraw.line([p0, (tx, ty), p1], fill=BORDER_COLOR, width=stroke * 2, joint="curve")

    # Step 2: Carve inner fill (ellipse + inset tail triangle) so border is uniform & seamless!
    # Compute inward normal shift for the two tail edges
    def shift_edge_inward(pa, pb, interior_pt, dist):
        vx, vy = pb[0] - pa[0], pb[1] - pa[1]
        length = math.hypot(vx, vy) or 1.0
        nx, ny = -vy / length, vx / length
        # Ensure normal points toward interior_pt
        if (interior_pt[0] - pa[0]) * nx + (interior_pt[1] - pa[1]) * ny < 0:
            nx, ny = -nx, -ny
        return (pa[0] + nx * dist, pa[1] + ny * dist), (pb[0] + nx * dist, pb[1] + ny * dist)

    mid_base = ((p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0)
    e0_a, e0_b = shift_edge_inward(p0, (tx, ty), mid_base, stroke)
    e1_a, e1_b = shift_edge_inward(p1, (tx, ty), mid_base, stroke)

    # Intersect shifted edges near tip so inner tip doesn't overshoot
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

    inner_tip = line_intersect(e0_a, e0_b, e1_a, e1_b)
    ldraw.ellipse([x1, y1, x2, y2], fill=PAPER_FILL)
    ldraw.polygon([e0_a, inner_tip, e1_a], fill=PAPER_FILL)

    overlay.alpha_composite(layer)

    draw = ImageDraw.Draw(overlay)
    font = load_font(True, font_size)
    draw_centered_lines(draw, cx, cy, lines, font, line_gap=11, align="center")


def draw_pov_box(
    overlay: Image.Image,
    cx: int,
    y1: int,
    lines: list[str],
    font_size: int = 32,
    pad_x: int = 34,
    pad_y: int = 20,
    align_box: str = "center",  # "center", "left" (cx treated as x1), "right" (cx treated as x2)
):
    draw = ImageDraw.Draw(overlay)
    font = load_font(True, font_size)
    line_gap = 11
    tw, th, _ = measure_multiline(draw, lines, font, line_gap)
    bw = tw + 2 * pad_x * SS
    bh = th + 2 * pad_y * SS

    if align_box == "left":
        bx1 = cx * SS
        bx2 = bx1 + bw
    elif align_box == "right":
        bx2 = cx * SS
        bx1 = bx2 - bw
    else:
        bx1 = cx * SS - bw / 2.0
        bx2 = cx * SS + bw / 2.0
    by1 = y1 * SS
    by2 = by1 + bh

    stroke = int(round(3.6 * SS))
    radius = int(round(20 * SS))
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=radius, fill=BOX_FILL, outline=BORDER_COLOR, width=stroke)
    draw_centered_lines(draw, (bx1 + bx2) / 2.0, (by1 + by2) / 2.0, lines, font, line_gap=line_gap, align="center")


PAGES = [
    {
        "raw": "raw-01.png",
        "out": "page-01.png",
        "title": ["陪妹妹出门约会", "1：出门前的偏爱"],
        "title_pos": (42, 42),
        # Top-right oval bubble (clear of ahoge at x=650..790)
        "b1": {
            "box": (860, 44, 1404, 298),
            "lines": ["哥哥……", "这身真的好看吗？"],
            "tail_tip": (940, 345),
            "tail_angle": 122,
            "font_size": 37,
        },
        # Middle-left oval bubble (below ear y=700, left of hands x=675)
        "b2": {
            "box": (26, 860, 585, 1185),
            "lines": ["你手这么暖地贴着我的脸，", "我都要害羞得", "迈不动步子啦~"],
            "tail_tip": (512, 845),
            "tail_angle": -38,
            "font_size": 34,
        },
        # TWO separate rounded-rectangle male-lead dialogue boxes (answering each beat cleanly!)
        "pov_boxes": [
            {
                "cx": 610,
                "y1": 1515,
                "lines": ["我的妹妹这么好看，看得我都想抱起来亲你一口了"],
                "font_size": 34,
                "align_box": "center",
            },
            {
                "cx": 865,
                "y1": 1658,
                "lines": ["今天不赶时间，我们慢慢去吧"],
                "font_size": 34,
                "align_box": "center",
            },
        ],
    },
    {
        "raw": "raw-02.png",
        "out": "page-02.png",
        "title": ["陪妹妹出门约会", "2：亲手戴上的发夹"],
        "title_pos": (42, 42),
        # Top-right oval bubble strictly ABOVE the flower hairclip & male hand (which start at y=385 in 1440x1920!)
        "b1": {
            "box": (840, 40, 1408, 310),
            "lines": ["哥哥靠这么近帮我戴……", "心跳都要被你听见了"],
            "tail_tip": (935, 355),
            "tail_angle": 118,
            "font_size": 35,
        },
        # Middle-left oval bubble (left of her curled hands which start at x=535)
        "b2": {
            "box": (24, 862, 526, 1190),
            "lines": ["既然是哥哥亲手戴上的，", "那以后只准给", "我一个人买哦~"],
            "tail_tip": (495, 838),
            "tail_angle": -36,
            "font_size": 33,
        },
        "pov_boxes": [
            {
                "cx": 455,
                "y1": 1512,
                "lines": ["当然只给你一个人买"],
                "font_size": 35,
                "align_box": "center",
            },
            {
                "cx": 755,
                "y1": 1654,
                "lines": ["戴在小眠头上太可爱了，真想抱回家只给我一个人看"],
                "font_size": 33,
                "align_box": "center",
            },
        ],
    },
    {
        "raw": "raw-03.png",
        "out": "page-03.png",
        "title": ["陪妹妹出门约会", "3：同一根吸管的甜味"],
        "title_pos": (42, 42),
        # Top-right bubble strictly ABOVE flower hairclip (flower starts at y=420 in 1440x1920!)
        "b1": {
            "box": (840, 42, 1410, 330),
            "lines": ["哥哥快尝尝……", "我刚喝过的那一口", "是不是最甜？"],
            "tail_tip": (930, 378),
            "tail_angle": 120,
            "font_size": 34,
        },
        # Upper-left greenery bubble (below title box y=215, ABOVE ear y=590 and ABOVE male hand wiping cream y=735!)
        "b2": {
            "box": (24, 250, 506, 560),
            "lines": ["唔……连嘴角的奶油", "都被哥哥擦掉了，", "好犯规呀~"],
            "tail_tip": (518, 535),
            "tail_angle": 28,
            "font_size": 33,
        },
        # Below smoothie cup (cup ends at y=1300, wrists end at y=1380)
        "pov_boxes": [
            {
                "cx": 500,
                "y1": 1510,
                "lines": ["只要是小眠喂我的都甜"],
                "font_size": 35,
                "align_box": "center",
            },
            {
                "cx": 800,
                "y1": 1652,
                "lines": ["不过比起饮料……还是我家妹妹更甜一点"],
                "font_size": 34,
                "align_box": "center",
            },
        ],
    },
    {
        "raw": "raw-04.png",
        "out": "page-04.png",
        "title": ["陪妹妹出门约会", "4：牵紧不放的归途"],
        "title_pos": (42, 42),
        # Top-right bubble strictly ABOVE flower hairclip (flower starts at y=378 in 1440x1920!)
        "b1": {
            "box": (845, 40, 1410, 322),
            "lines": ["哥哥的手好暖和……", "真想一直这样", "牵着不松开"],
            "tail_tip": (935, 362),
            "tail_angle": 122,
            "font_size": 34,
        },
        # Middle-left bubble (over blurred sunset street & outer shoulder, left of chest hand x=570)
        "b2": {
            "box": (22, 846, 548, 1176),
            "lines": ["不只是下周……", "以后的每一次约会，我都想", "当哥哥唯一的那个人哦~"],
            "tail_tip": (495, 822),
            "tail_angle": -36,
            "font_size": 31,
        },
        # Positioned cleanly on the LEFT half (x < 835) so the held hands at x=860..1440, y=1385..1920 stay 100% UNCOVERED!
        "pov_boxes": [
            {
                "cx": 38,
                "y1": 1450,
                "lines": ["那就一直牵着别松手"],
                "font_size": 34,
                "align_box": "left",
            },
            {
                "cx": 38,
                "y1": 1588,
                "lines": ["不止下周，以后我的休息日和整个人，", "全都归我们家小眠"],
                "font_size": 32,
                "align_box": "left",
            },
        ],
    },
]


def render_page(spec: dict) -> Path:
    raw_im = Image.open(RAW_DIR / spec["raw"]).convert("RGBA")
    base = raw_im.resize((TARGET_W, TARGET_H), Image.LANCZOS)

    overlay = Image.new("RGBA", (TARGET_W * SS, TARGET_H * SS), (0, 0, 0, 0))

    draw_title_box(overlay, spec["title_pos"][0], spec["title_pos"][1], spec["title"])

    for b_key in ("b1", "b2"):
        b = spec[b_key]
        draw_oval_bubble(
            overlay,
            box=b["box"],
            lines=b["lines"],
            tail_tip=b["tail_tip"],
            tail_base_angle_deg=b["tail_angle"],
            font_size=b["font_size"],
        )

    for pbox in spec["pov_boxes"]:
        draw_pov_box(
            overlay,
            cx=pbox["cx"],
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
    import io
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rendered = [render_page(spec) for spec in PAGES]
    jpg_streams = []
    for p in rendered:
        buf = io.BytesIO()
        Image.open(p).save(buf, format="JPEG", quality=95, subsampling=0)
        jpg_streams.append(buf.getvalue())
    pdf_path = OUT_DIR / "陪妹妹出门约会_第一话.pdf"
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(jpg_streams))
    print("Generated:", [str(p) for p in rendered], "->", pdf_path)


if __name__ == "__main__":
    main()
