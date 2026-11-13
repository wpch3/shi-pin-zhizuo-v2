#!/usr/bin/env python3
"""
Generate:
1. deliverables/v2-chapter-01/character-card-xiaomian.png (小眠正式人设卡)
2. deliverables/v2-chapter-01-vertical/page-01..04.png + PDF (1080x1920 9:16 B站竖屏视频直导版，上下暖纸纹留白避开播放栏)
"""
import io
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import img2pdf

ROOT = Path(__file__).resolve().parent.parent
FONT_BOLD = ROOT / ".cache" / "fonts" / "NotoSansCJKsc-Bold.otf"
FONT_REG = ROOT / ".cache" / "fonts" / "NotoSansCJKsc-Regular.otf"


def f_bold(sz: int):
    return ImageFont.truetype(str(FONT_BOLD), sz)


def f_reg(sz: int):
    return ImageFont.truetype(str(FONT_REG), sz)


def make_paper_canvas(w: int, h: int, base_rgb=(244, 237, 225)) -> Image.Image:
    """Warm matte hand-drawn paper background with subtle grain."""
    im = Image.new("RGB", (w, h), base_rgb)
    # Fast tileable 128x128 subtle paper grain
    rng = random.Random(42)
    tile = Image.new("RGB", (128, 128))
    tpx = tile.load()
    for y in range(128):
        for x in range(128):
            d = rng.randint(-4, 4)
            tpx[x, y] = (
                max(0, min(255, base_rgb[0] + d)),
                max(0, min(255, base_rgb[1] + d)),
                max(0, min(255, base_rgb[2] + d)),
            )
    for y in range(0, h, 128):
        for x in range(0, w, 128):
            im.paste(tile, (x, y))
    return im


def build_character_card():
    out_dir = ROOT / "deliverables" / "v2-chapter-01"
    out_dir.mkdir(parents=True, exist_ok=True)
    W, H = 1920, 1280
    card = make_paper_canvas(W, H, (245, 239, 228))
    draw = ImageDraw.Draw(card)

    # Outer frame
    draw.rounded_rectangle([32, 32, W - 32, H - 32], radius=24, outline=(52, 46, 40), width=4)

    # Left portrait from new_character.png (3:4 -> 840 x 1120)
    portrait = Image.open(ROOT / "new_character.png").convert("RGB").resize((840, 1120), Image.LANCZOS)
    px, py = 76, 80
    card.paste(portrait, (px, py))
    draw.rectangle([px - 2, py - 2, px + 842, py + 1122], outline=(42, 36, 32), width=4)

    # Right info sheet
    rx = 975
    draw.text((rx, 92), "角色设定卡｜小眠", font=f_bold(54), fill=(32, 28, 24))
    draw.text((rx, 168), "《陪妹妹出门约会》女主 · 视觉与性格锁定基准", font=f_reg(28), fill=(102, 92, 82))
    draw.line([(rx, 224), (W - 84, 224)], fill=(165, 152, 136), width=3)

    sections = [
        ("【称呼与关系】", [
            "哥哥最偏爱的妹妹“小眠”。日常同住、亲密无间，",
            "在双向宠溺与直球偏爱中自然升温的甜蜜依恋关系。",
        ]),
        ("【外貌锁定特征】", [
            "• 发型：低饱和浅亚麻奶茶色松散双低马尾 + 头顶一根微翘呆毛",
            "• 眉眼：半透明碎刘海、粗黑微垂半睁上眼睑、灰蓝色无高光瞳孔",
            "• 细节：幼态短圆脸、淡红棕卧蚕阴影、极简点鼻与细线嘴",
        ]),
        ("【固定穿搭规范】", [
            "• 居家常服：鼠尾草绿宽松针织开衫（手绘短排线袖口）+ 米白圆领内搭",
            "• 外出约会服：同款鼠尾草绿开衫 + 米白小翻领双扣连衣裙 + 浅米斜挎包",
            "• 剧情定情物：哥哥亲手别在画面右侧刘海边的奶油白小花发夹",
        ]),
        ("【性格与互动温度】", [
            "• 安静慢热、带一点软糯犯困感，在哥哥面前极度粘人坦率",
            "• 哥哥（第一人称 POV）全程温和直球宠溺，主动捧脸、戴发夹、",
            "  擦唇角奶油、牵紧双手回应每一句心意",
        ]),
    ]

    cy = 258
    for title, bullets in sections:
        draw.text((rx, cy), title, font=f_bold(32), fill=(48, 62, 50))
        cy += 50
        for line in bullets:
            draw.text((rx + 14, cy), line, font=f_reg(26), fill=(40, 35, 30))
            cy += 42
        cy += 22

    out_path = out_dir / "character-card-xiaomian.png"
    card.save(out_path, optimize=True)
    print("Saved character card:", out_path)


def build_v2_vertical_video_edition():
    """
    1080x1920 (9:16) ready-to-import Bilibili vertical comic pages:
    Centers the 3:4 comic page cleanly at 1020x1360 on a warm matte paper 1080x1920 frame
    with generous top (240px) & bottom (320px) Bilibili player UI safe zones.
    """
    src_dir = ROOT / "deliverables" / "v2-chapter-01"
    out_dir = ROOT / "deliverables" / "v2-chapter-01-vertical"
    out_dir.mkdir(parents=True, exist_ok=True)

    VW, VH = 1080, 1920
    PW, PH = 1020, 1360
    ox, oy = (VW - PW) // 2, 230  # Extra bottom margin (330px) avoids Bilibili caption/progress bar!

    rendered = []
    for i in range(1, 5):
        canvas = make_paper_canvas(VW, VH, (244, 237, 225))
        d = ImageDraw.Draw(canvas)
        page = Image.open(src_dir / f"page-0{i}.png").convert("RGB").resize((PW, PH), Image.LANCZOS)
        canvas.paste(page, (ox, oy))
        d.rectangle([ox - 2, oy - 2, ox + PW + 2, oy + PH + 2], outline=(42, 36, 32), width=3)
        out_p = out_dir / f"page-0{i}.png"
        canvas.save(out_p, optimize=True)
        rendered.append(out_p)

    jpg_streams = []
    for p in rendered:
        buf = io.BytesIO()
        Image.open(p).save(buf, format="JPEG", quality=95, subsampling=0)
        jpg_streams.append(buf.getvalue())
    pdf_path = out_dir / "陪妹妹出门约会_9x16竖屏视频版.pdf"
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(jpg_streams))
    print("Saved 9:16 vertical edition:", pdf_path)


if __name__ == "__main__":
    build_character_card()
    build_v2_vertical_video_edition()
