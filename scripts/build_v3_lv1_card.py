#!/usr/bin/env python3
"""
Build the character card for `v3 · lv1` heroine (柚子 / 美术系女大)
and support building the 3:4 + 9:16 editions once all raw pages are ready.
"""
from pathlib import Path
from PIL import Image, ImageDraw

import build_extras as extras

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "art" / "v3-lv1"
OUT_DIR = ROOT / "deliverables" / "v3-lv1"


def build_v3_lv1_character_card():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    W, H = 1920, 1280
    card = extras.make_paper_canvas(W, H, (245, 239, 228))
    draw = ImageDraw.Draw(card)
    f_bold, f_reg = extras.f_bold, extras.f_reg

    draw.rounded_rectangle([32, 32, W - 32, H - 32], radius=24, outline=(52, 46, 40), width=4)

    portrait = Image.open(RAW_DIR / "ref-yuzu.png").convert("RGB").resize((840, 1120), Image.LANCZOS)
    px, py = 76, 80
    card.paste(portrait, (px, py))
    draw.rectangle([px - 2, py - 2, px + 842, py + 1122], outline=(42, 36, 32), width=4)

    rx = 975
    draw.text((rx, 88), "角色设定卡｜柚子（美术系读者）", font=f_bold(50), fill=(32, 28, 24))
    draw.text((rx, 162), "v3 · lv1 重制版《被拒绝的 NTR 老师》女主 · 视觉与画风锁定基准",
              font=f_reg(26), fill=(102, 92, 82))
    draw.line([(rx, 218), (W - 84, 218)], fill=(165, 152, 136), width=3)

    sections = [
        ("【身份与戏剧定位】", [
            "美术系在读女生，「夜画」四年连载的老读者。",
            "温柔、清醒、有礼貌，一眼看穿男主公式的贫瘠并干脆婉拒。",
        ]),
        ("【外貌锁定特征（全话严禁左右镜像漂移）】", [
            "• 发型：自然炭黑及下巴短波波头 + 画面左侧细麻花辫",
            "• 发饰：固定在画面左侧（她右耳上方）的芥末黄小方夹",
            "• 眉眼：暖琥珀色无高光哑光瞳孔、柔和圆润五官、淡粉红晕",
        ]),
        ("【固定穿搭与随身物件】", [
            "• 上装：奶油米白宽松针织开衫（手绘短排线袖口）+ 白圆领衬衫",
            "• 下装：深藏青百褶中裙 + 米白帆布包",
            "• 关键道具：环装速写本（纯铅笔交叉排线习作：肾蕨、睡猫、伞铺）",
        ]),
        ("【针对原代理版本的画风修正】", [
            "• 100% 对齐 v2 素描感 2D 铅笔线稿 + 低饱和平涂哑光赛璐璐",
            "• 彻底剔除水彩脏渍（watercolor wash）与突兀西洋写实油画插页",
            "• 全程严守男主第一人称 POV，统一程序绘制干净外框与安全边距",
        ]),
    ]

    cy = 250
    for title, bullets in sections:
        draw.text((rx, cy), title, font=f_bold(31), fill=(48, 62, 50))
        cy += 48
        for line in bullets:
            draw.text((rx + 14, cy), line, font=f_reg(26), fill=(40, 35, 30))
            cy += 42
        cy += 22

    out_path = OUT_DIR / "character-card-yuzu.png"
    card.save(out_path, optimize=True)
    print("Saved v3-lv1 character card:", out_path)


if __name__ == "__main__":
    build_v3_lv1_character_card()
