#!/usr/bin/env python3
"""
Build the `v2 · lv2` new-character card for 阿澄.
Reuses the warm matte paper canvas + font helpers from build_extras.py.
"""
from pathlib import Path
from PIL import Image, ImageDraw

import build_extras as extras

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "deliverables" / "v2-lv2"
PORTRAIT = ROOT / "new_character_lv2.png"


def build_lv2_character_card():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    W, H = 1920, 1280
    card = extras.make_paper_canvas(W, H, (245, 239, 228))
    draw = ImageDraw.Draw(card)
    f_bold, f_reg = extras.f_bold, extras.f_reg

    draw.rounded_rectangle([32, 32, W - 32, H - 32], radius=24, outline=(52, 46, 40), width=4)

    portrait = Image.open(PORTRAIT).convert("RGB").resize((840, 1120), Image.LANCZOS)
    px, py = 76, 80
    card.paste(portrait, (px, py))
    draw.rectangle([px - 2, py - 2, px + 842, py + 1122], outline=(42, 36, 32), width=4)

    rx = 975
    draw.text((rx, 88), "角色设定卡｜阿澄", font=f_bold(54), fill=(32, 28, 24))
    draw.text((rx, 164), "v2 · lv2 新漫画《一起躲雨的书店》女主 · 视觉与性格锁定基准",
              font=f_reg(26), fill=(102, 92, 82))
    draw.line([(rx, 220), (W - 84, 220)], fill=(165, 152, 136), width=3)

    sections = [
        ("【称呼与关系】", [
            "阿澄。与哥哥自然亲昵无间、双向偏爱，",
            "由她明快主动的直球，把关系一点点带近。",
        ]),
        ("【外貌锁定特征】", [
            "• 发型：深栗／黑茶色齐肩内扣短发，偏分无刘海、无呆毛",
            "• 眉眼：上挑细长眼、暖琥珀色无高光瞳孔、浅浅梨涡",
            "• 细节：鹅蛋脸偏长、细金属框圆眼镜、极简点鼻与细线嘴",
        ]),
        ("【固定穿搭规范】", [
            "• 上装：雾蓝衬衫 + 浅灰针织背心（手绘短排线织纹）",
            "• 配件：深色细腰带、细金属框眼镜",
            "• 剧情定情物：雨天书店里手捧的一本书",
        ]),
        ("【与小眠的硬反差｜防同人】", [
            "• 禁：浅亚麻奶茶双低马尾、碎刘海、呆毛、圆脸半睁眼",
            "• 禁：灰蓝瞳、鼠尾草绿开衫、米白连衣裙、奶油白小花发夹",
            "• 差异：由「安静软糯被宠」改为「明快主动带节奏」",
        ]),
        ("【画风锁定】", [
            "• 素描感 2D 手绘铅笔线稿 + 平涂哑光赛璐璐、低饱和柔和色",
            "• 无高光瞳孔、暖调虚化背景；排除水彩／厚涂／写实光影",
        ]),
    ]

    cy = 252
    for title, bullets in sections:
        draw.text((rx, cy), title, font=f_bold(32), fill=(48, 62, 50))
        cy += 50
        for line in bullets:
            draw.text((rx + 14, cy), line, font=f_reg(26), fill=(40, 35, 30))
            cy += 42
        cy += 22

    out_path = OUT_DIR / "character-card-acheng.png"
    card.save(out_path, optimize=True)
    print("Saved lv2 character card:", out_path)


if __name__ == "__main__":
    build_lv2_character_card()
