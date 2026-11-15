#!/usr/bin/env python3
"""
Build the 1080x1920 (9:16) Bilibili-safe vertical edition of
`v2 · lv1` chapter 02 《陪妹妹出门约会 2 · 不否认的那句》.
Reuses the warm matte paper canvas helper from build_extras.py.
"""
import io
from pathlib import Path
from PIL import Image, ImageDraw
import img2pdf

import build_extras as extras

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "deliverables" / "v2-chapter-02"
OUT_DIR = ROOT / "deliverables" / "v2-chapter-02-vertical"


def build_vertical_edition():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    VW, VH = 1080, 1920
    PW, PH = 1020, 1360
    ox, oy = (VW - PW) // 2, 230  # 330px bottom margin avoids Bilibili player UI

    rendered = []
    for i in range(1, 5):
        canvas = extras.make_paper_canvas(VW, VH, (244, 237, 225))
        d = ImageDraw.Draw(canvas)
        page = Image.open(SRC_DIR / f"page-0{i}.png").convert("RGB").resize((PW, PH), Image.LANCZOS)
        canvas.paste(page, (ox, oy))
        d.rectangle([ox - 2, oy - 2, ox + PW + 2, oy + PH + 2], outline=(42, 36, 32), width=3)
        out_p = OUT_DIR / f"page-0{i}.png"
        canvas.save(out_p, optimize=True)
        rendered.append(out_p)

    jpg_streams = []
    for p in rendered:
        buf = io.BytesIO()
        Image.open(p).save(buf, format="JPEG", quality=95, subsampling=0)
        jpg_streams.append(buf.getvalue())
    pdf_path = OUT_DIR / "陪妹妹出门约会_第二话_9x16竖屏视频版.pdf"
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(jpg_streams))
    print("Saved 9:16 vertical edition:", pdf_path)


if __name__ == "__main__":
    build_vertical_edition()
