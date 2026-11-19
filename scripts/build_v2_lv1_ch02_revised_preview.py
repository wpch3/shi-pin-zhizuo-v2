#!/usr/bin/env python3
"""Build an explicitly provisional, five-page, one-illustration-per-page review PDF.

Requires Pillow and a CJK font. Set CJK_FONT to an installed font or put
NotoSansCJKsc-Regular.otf in .cache/fonts. Original illustrations are preserved.
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / 'art/v2-lv1-chapter-02-revised'
OUT = ROOT / 'deliverables/v2-lv1-chapter-02-revised-preview'
FONT = Path(os.environ.get('CJK_FONT', ROOT / '.cache/fonts/NotoSansCJKsc-Regular.otf'))
W, H = 1440, 1920
PAGES = [
    ('今天听我的', ['小眠：今天不许哥哥偷偷安排哦。', '小眠：我要把你喜欢的地方，和我的小秘密都带给你。', '哥哥：好，今天听你的。', '哥哥：不过手腕要一直让你牵着吗？']),
    ('先抱一下', ['小眠：我明明查了好久……还是没能带哥哥看到。', '小眠：这样的约会，会不会很无聊？', '哥哥：和你在一起就不会。', '哥哥：先让我抱一下，好不好？']),
    ('她的小秘密', ['小眠：其实我还准备了第二个地方。', '小眠：坐沿河的车，可以和哥哥挨着坐很久。', '哥哥：原来这就是你的小秘密。', '哥哥：那就把旁边的位置留给我。']),
    ('再靠近一点', ['小眠：今天这个位置，我早就想留给哥哥了。', '小眠：我可以再靠近一点吗？', '哥哥：当然可以。', '哥哥：我也一直想离你近一点。']),
    ('最喜欢的人', ['小眠：电影没看到，不过我想要的约会已经有了。', '小眠：因为我最喜欢的人，就在这里。', '哥哥：我最喜欢的人也是你。', '哥哥：这张小车票，我会好好收着。']),
]


def main():
    if not FONT.exists():
        raise SystemExit(f'CJK font not found: {FONT}. Set CJK_FONT to a suitable font.')
    OUT.mkdir(parents=True, exist_ok=True)
    header_font = ImageFont.truetype(str(FONT), 36)
    body_font = ImageFont.truetype(str(FONT), 31)
    small_font = ImageFont.truetype(str(FONT), 26)
    pages = []
    for i, (title, lines) in enumerate(PAGES, 1):
        raw = Image.open(RAW / f'page-{i:02d}.png').convert('RGB')
        raw.thumbnail((1160, 1535), Image.Resampling.LANCZOS)
        canvas = Image.new('RGB', (W, H), '#f9f5ee')
        draw = ImageDraw.Draw(canvas)
        draw.text((70, 24), f'陪妹妹出门约会 2  ·  {i}  {title}', font=header_font, fill='#302925')
        x = (W - raw.width) // 2
        y = 90
        canvas.paste(raw, (x, y))
        y += raw.height + 12
        if i == 2:
            draw.text((82, y), '场景说明：露天电影因雨取消。', font=small_font, fill='#62554b')
            y += 36
        for line in lines:
            if draw.textlength(line, font=body_font) > W - 160:
                raise ValueError(f'Line does not fit on page {i}: {line}')
            draw.text((82, y), line, font=body_font, fill='#302925')
            y += 47
        if y > H - 50:
            raise ValueError(f'Text overflow on page {i}: {y}')
        draw.text((W - 440, H - 45), '首版试排 · 原画待修', font=small_font, fill='#8b6454')
        canvas.save(OUT / f'page-{i:02d}.png', optimize=True)
        pages.append(canvas)
    pages[0].save(OUT / '雨后的沿河线_首版试排.pdf', save_all=True,
                  append_images=pages[1:], resolution=144.0)
    print(f'Created {len(pages)} review pages and PDF in {OUT}')


if __name__ == '__main__':
    main()
