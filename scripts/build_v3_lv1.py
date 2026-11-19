#!/usr/bin/env python3
"""
Build `v3 · lv1` remastered vertical POV comic:
《被拒绝的 NTR 老师 · 我画的女生，从来不看我》
- 1440x1920 (3:4 reading & camera-pan edition) with clean unified outer frame & matte paper margin
- 1080x1920 (9:16 Bilibili vertical video edition with top/bottom player safe zones)
- Renders all currently available raw pages cleanly, and generates combined PDFs once complete.
"""
import io
import math
from pathlib import Path
from PIL import Image, ImageDraw
import img2pdf

import build_v2_chapter01 as base
import build_extras as extras

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "art" / "v3-lv1"
OUT_DIR = ROOT / "deliverables" / "v3-lv1"
OUT_VERT_DIR = ROOT / "deliverables" / "v3-lv1-vertical"

W, H = 1440, 1920
SS = base.SS
MARGIN = 36  # Unified outer comic border margin on all pages


def draw_oval_no_tail(overlay: Image.Image, box: tuple[int, int, int, int], lines: list[str], font_size: int = 33):
    """Draw a clean oval speech bubble without a tail (for continuation bubbles by the same speaker)."""
    x1, y1, x2, y2 = [v * SS for v in box]
    cx, cy = (x1 + x2) / 2.0, (y1 + y2) / 2.0
    stroke = int(round(3.6 * SS))

    layer = Image.new("RGBA", overlay.size, (0, 0, 0, 0))
    ldraw = ImageDraw.Draw(layer)
    ldraw.ellipse([x1 - stroke, y1 - stroke, x2 + stroke, y2 + stroke], fill=base.BORDER_COLOR)
    ldraw.ellipse([x1, y1, x2, y2], fill=base.PAPER_FILL)
    overlay.alpha_composite(layer)

    draw = ImageDraw.Draw(overlay)
    font = base.load_font(True, font_size)
    base.draw_centered_lines(draw, cx, cy, lines, font, line_gap=11, align="center")


def draw_cover_header(overlay: Image.Image):
    """Magazine-grade clean cover title block in upper-left cream space."""
    draw = ImageDraw.Draw(overlay)
    stroke = int(round(3.8 * SS))

    # Small episode tag
    base.draw_title_box(overlay, 68, 66, ["第 1 话"], font_size=28)

    # Main title block
    f_main = base.load_font(True, 68)
    lines_main = ["被拒绝的", "NTR 老师"]
    tw, th, _ = base.measure_multiline(draw, lines_main, f_main, line_gap=14)
    pad_x, pad_y = 34 * SS, 26 * SS
    bx1, by1 = 68 * SS, 148 * SS
    bx2, by2 = bx1 + tw + 2 * pad_x, by1 + th + 2 * pad_y
    draw.rectangle([bx1, by1, bx2, by2], fill=base.BOX_FILL, outline=base.BORDER_COLOR, width=stroke)
    base.draw_centered_lines(draw, (bx1 + bx2) / 2, (by1 + by2) / 2, lines_main, f_main, line_gap=14, align="left")

    # Subtitle bar
    base.draw_title_box(overlay, 68, 412, ["我画的女生，从来不看我"], font_size=33)


def make_framed_canvas(raw_path: Path) -> Image.Image:
    """Place raw full-bleed art inside a clean unified matte paper margin + crisp dark ink border."""
    canvas = extras.make_paper_canvas(W, H, (246, 240, 229)).convert("RGBA")
    inner_w, inner_h = W - 2 * MARGIN, H - 2 * MARGIN
    art = Image.open(raw_path).convert("RGB").resize((inner_w, inner_h), Image.LANCZOS)
    canvas.paste(art, (MARGIN, MARGIN))

    frame_layer = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    fdraw = ImageDraw.Draw(frame_layer)
    m = MARGIN * SS
    fdraw.rectangle([m, m, (W - MARGIN) * SS, (H - MARGIN) * SS], outline=base.BORDER_COLOR, width=int(round(4.0 * SS)))
    canvas.alpha_composite(frame_layer.resize((W, H), Image.LANCZOS))
    return canvas


PAGES = [
    {
        "raw": "raw-00-cover.png",
        "out": "page-00-cover.png",
        "is_cover": True,
        "items": [],
    },
    {
        "raw": "raw-01.png",
        "out": "page-01.png",
        "items": [
            ("pov", {"cx": 68, "y1": 68, "align_box": "left", "font_size": 36,
                     "lines": ["我二十四岁，是……画 NTR 的。"]}),
            ("pov", {"cx": 68, "y1": 182, "align_box": "left", "font_size": 33,
                     "lines": ["笔名「夜画」，四年没露过脸。", "读者只认得我的画。"]}),
            ("pov", {"cx": 1372, "y1": 1688, "align_box": "right", "font_size": 32,
                     "lines": ["我赚钱的公式只有一句：", "「原本属于我的人，被抢走了。」"]}),
        ],
    },
    {
        "raw": "raw-02.png",
        "out": "page-02.png",
        "items": [
            ("pov", {"cx": 68, "y1": 68, "align_box": "left", "font_size": 34,
                     "lines": ["下午去咖啡店改分镜时，", "我在窗边看见了她。"]}),
            ("pov", {"cx": 68, "y1": 236, "align_box": "left", "font_size": 33,
                     "lines": ["店里只剩她对面一个空位。", "我站了一会儿，才敢走过去拼桌。"]}),
        ],
    },
    {
        "raw": "raw-03.png",
        "out": "page-03.png",
        "items": [
            ("pov", {"cx": 68, "y1": 68, "align_box": "left", "font_size": 33,
                     "lines": ["坐下时，文件夹里的打印稿滑了出来。"]}),
            ("bubble", {"box": (68, 430, 596, 668), "tail_tip": (675, 650), "tail_angle": 12, "font_size": 36,
                        "lines": ["这根线条……", "是「夜画」老师画的吧？"]}),
        ],
    },
    {
        "raw": "raw-04.png",
        "out": "page-04.png",
        "items": [
            ("pov", {"cx": 64, "y1": 62, "align_box": "left", "font_size": 33,
                     "lines": ["她说，她追我的连载很久了，", "每一话都看。"]}),
            ("bubble", {"box": (956, 72, 1384, 286), "tail_tip": (1115, 425), "tail_angle": 106, "font_size": 33,
                        "lines": ["那作为读者……", "我可以说句实话吗？"]}),
            ("pov", {"cx": 1372, "y1": 1732, "align_box": "right", "font_size": 33,
                     "lines": ["我点头点得太快了。"]}),
        ],
    },
    {
        "raw": "raw-05.png",
        "out": "page-05.png",
        "items": [
            ("bubble", {"box": (866, 72, 1380, 286), "tail_tip": (812, 470), "tail_angle": 138, "font_size": 33,
                        "lines": ["老师笔下那些", "「被抢走」的女孩子……"]}),
            ("oval", {"box": (866, 312, 1380, 524), "font_size": 33,
                      "lines": ["好像从来都没有", "自己真正喜欢的东西。"]}),
            ("pov", {"cx": 68, "y1": 1736, "align_box": "left", "font_size": 32,
                     "lines": ["看着她本子里的画，我一时竟接不上话。"]}),
        ],
    },
    {
        "raw": "raw-06.png",
        "out": "page-06.png",
        "items": [
            ("bubble", {"box": (68, 96, 676, 336), "tail_tip": (730, 560), "tail_angle": 42, "font_size": 33,
                        "lines": ["在你的故事里，女生好像只有", "「属于男主」和「被抢走」两种状态。"]}),
            ("oval", {"box": (68, 364, 676, 598), "font_size": 33,
                      "lines": ["可现实里的我们，会挑喜欢的伞，", "下雨天也会自己去买甜品呀。"]}),
            ("pov", {"cx": 1372, "y1": 1732, "align_box": "right", "font_size": 32,
                     "lines": ["她说得很轻，却像把我的公式整个抽空了。"]}),
        ],
    },
    {
        "raw": "raw-07.png",
        "out": "page-07.png",
        "items": [
            ("pov", {"cx": 68, "y1": 68, "align_box": "left", "font_size": 33,
                     "lines": ["我鬼使神差地递出手机，", "想问还能不能再向她请教。"]}),
            ("bubble", {"box": (68, 256, 616, 480), "tail_tip": (685, 590), "tail_angle": 28, "font_size": 34,
                        "lines": ["抱歉呀，老师。", "来接我的人已经到窗外啦。"]}),
            ("oval", {"box": (68, 504, 656, 732), "font_size": 33,
                      "lines": ["希望下一本漫画里，", "你能画出真正开心看着你的女孩子。"]}),
        ],
    },
    {
        "raw": "raw-08.png",
        "out": "page-08.png",
        "items": [
            ("pov", {"cx": 68, "y1": 68, "align_box": "left", "font_size": 34,
                     "lines": ["她从来不属于谁，自然也无从「被抢走」。"]}),
            ("pov", {"cx": 68, "y1": 182, "align_box": "left", "font_size": 33,
                     "lines": ["那部连载，后来停更了。", "不是没时间，是真的再也画不下去。"]}),
        ],
    },
    {
        "raw": "raw-09.png",
        "out": "page-09.png",
        "items": [
            ("pov", {"cx": 68, "y1": 68, "align_box": "left", "font_size": 35,
                     "lines": ["四十年后，我还在画漫画。"]}),
            ("pov", {"cx": 68, "y1": 182, "align_box": "left", "font_size": 34,
                     "lines": ["只不过后来这辈子，我只画纯爱。"]}),
            ("bubble", {"box": (824, 336, 1372, 560), "tail_tip": (1220, 720), "tail_angle": 82, "font_size": 34,
                        "lines": ["爷爷，他们挑伞这一格", "笑得真好看！"]}),
        ],
    },
]


def render_page(spec: dict) -> Path | None:
    raw_p = RAW_DIR / spec["raw"]
    if not raw_p.exists():
        return None
    canvas = make_framed_canvas(raw_p)
    overlay = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))

    if spec.get("is_cover"):
        draw_cover_header(overlay)

    for kind, kw in spec["items"]:
        if kind == "pov":
            base.draw_pov_box(
                overlay,
                cx=kw["cx"],
                y1=kw["y1"],
                lines=kw["lines"],
                font_size=kw.get("font_size", 33),
                align_box=kw.get("align_box", "center"),
            )
        elif kind == "bubble":
            base.draw_oval_bubble(
                overlay,
                box=kw["box"],
                lines=kw["lines"],
                tail_tip=kw["tail_tip"],
                tail_base_angle_deg=kw["tail_angle"],
                font_size=kw.get("font_size", 34),
            )
        elif kind == "oval":
            draw_oval_no_tail(
                overlay,
                box=kw["box"],
                lines=kw["lines"],
                font_size=kw.get("font_size", 34),
            )

    overlay_1x = overlay.resize((W, H), Image.LANCZOS)
    final_im = Image.alpha_composite(canvas, overlay_1x).convert("RGB")
    out_p = OUT_DIR / spec["out"]
    final_im.save(out_p, optimize=True)
    return out_p


def build_all():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_VERT_DIR.mkdir(parents=True, exist_ok=True)

    rendered = []
    for spec in PAGES:
        out_p = render_page(spec)
        if out_p:
            rendered.append(out_p)
            print("Rendered 3:4:", out_p.name)
        else:
            print("Pending raw:", spec["raw"])

    # Also build 9:16 vertical counterparts for all rendered pages
    VW, VH = 1080, 1920
    PW, PH = 1020, 1360
    ox, oy = (VW - PW) // 2, 230
    rendered_vert = []
    for p in rendered:
        v_canvas = extras.make_paper_canvas(VW, VH, (244, 237, 225))
        d = ImageDraw.Draw(v_canvas)
        pg = Image.open(p).convert("RGB").resize((PW, PH), Image.LANCZOS)
        v_canvas.paste(pg, (ox, oy))
        d.rectangle([ox - 2, oy - 2, ox + PW + 2, oy + PH + 2], outline=(42, 36, 32), width=3)
        vp = OUT_VERT_DIR / p.name
        v_canvas.save(vp, optimize=True)
        rendered_vert.append(vp)

    if len(rendered) == len(PAGES):
        for plist, pdf_path in [
            (rendered, OUT_DIR / "被拒绝的NTR老师_第一话.pdf"),
            (rendered_vert, OUT_VERT_DIR / "被拒绝的NTR老师_第一话_9x16竖屏视频版.pdf"),
        ]:
            streams = []
            for p in plist:
                buf = io.BytesIO()
                Image.open(p).save(buf, format="JPEG", quality=95, subsampling=0)
                streams.append(buf.getvalue())
            with open(pdf_path, "wb") as f:
                f.write(img2pdf.convert(streams))
            print("Saved complete PDF:", pdf_path)


if __name__ == "__main__":
    build_all()
