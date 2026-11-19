#!/usr/bin/env python3
"""
Build `v2 · lv1` chapter 02 《陪妹妹出门约会 2 · 不否认的那句》.
4 vertical POV comic pages (1440x1920, 3:4) + combined PDF.
Reuses the hand-fitted typesetting helpers from build_v2_chapter01.py.
Every multi-beat male-lead answer is split into TWO separate rounded boxes.
"""
import io
from pathlib import Path
from PIL import Image
import img2pdf

import build_v2_chapter01 as base

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "art" / "v2-chapter-02"
OUT_DIR = ROOT / "deliverables" / "v2-chapter-02"

base.RAW_DIR = RAW_DIR
base.OUT_DIR = OUT_DIR

TITLE = "陪妹妹出门约会 2"

PAGES = [
    {
        "raw": "raw-01.png",
        "out": "page-01.png",
        "title": [TITLE, "1：出门前的第二次"],
        "title_pos": (42, 42),
        "b1": {
            "box": (860, 44, 1404, 292),
            "lines": ["哥哥，我今天自己", "把发夹别好了哦"],
            "tail_tip": (940, 340),
            "tail_angle": 122,
            "font_size": 36,
        },
        "b2": {
            "box": (24, 852, 578, 1170),
            "lines": ["你上次说以后每次约会", "都陪我，还算数吗？"],
            "tail_tip": (505, 838),
            "tail_angle": -38,
            "font_size": 34,
        },
        "pov_boxes": [
            {
                "cx": 600,
                "y1": 1508,
                "lines": ["别得比我还好看，我家小眠真乖"],
                "font_size": 34,
                "align_box": "center",
            },
            {
                "cx": 830,
                "y1": 1652,
                "lines": ["当然算数，今天一整天都只陪你"],
                "font_size": 34,
                "align_box": "center",
            },
        ],
    },
    {
        "raw": "raw-02.png",
        "out": "page-02.png",
        "title": [TITLE, "2：不否认的那句"],
        "title_pos": (42, 42),
        "b1": {
            "box": (846, 42, 1408, 310),
            "lines": ["哥、哥哥……", "她刚才叫我什么呀？"],
            "tail_tip": (930, 352),
            "tail_angle": 120,
            "font_size": 35,
        },
        "b2": {
            "box": (24, 848, 540, 1090),
            "lines": ["你为什么不解释呢？"],
            "tail_tip": (500, 832),
            "tail_angle": -36,
            "font_size": 34,
        },
        "pov_boxes": [
            {
                "cx": 590,
                "y1": 1500,
                "lines": ["因为你低头红到耳根的样子，我舍不得打断"],
                "font_size": 31,
                "align_box": "center",
            },
            {
                "cx": 810,
                "y1": 1646,
                "lines": ["而且那句话，我一点都不想否认"],
                "font_size": 34,
                "align_box": "center",
            },
        ],
    },
    {
        "raw": "raw-03.png",
        "out": "page-03.png",
        "title": [TITLE, "3：慢慢挑的称呼"],
        "title_pos": (42, 42),
        "b1": {
            "box": (842, 42, 1410, 322),
            "lines": ["唔……被那样叫了一次，", "心跳到现在还没停"],
            "tail_tip": (928, 368),
            "tail_angle": 120,
            "font_size": 33,
        },
        "b2": {
            "box": (22, 300, 500, 570),
            "lines": ["那哥哥希望", "我是那样的人吗？"],
            "tail_tip": (510, 545),
            "tail_angle": 28,
            "font_size": 34,
        },
        "pov_boxes": [
            {
                "cx": 560,
                "y1": 1504,
                "lines": ["我希望你是我身边最靠近的那个人"],
                "font_size": 33,
                "align_box": "center",
            },
            {
                "cx": 790,
                "y1": 1648,
                "lines": ["至于是哪个称呼，我们慢慢挑，你说了算"],
                "font_size": 31,
                "align_box": "center",
            },
        ],
    },
    {
        "raw": "raw-04.png",
        "out": "page-04.png",
        "title": [TITLE, "4：早就不只是妹妹"],
        "title_pos": (42, 42),
        "b1": {
            "box": (846, 40, 1410, 318),
            "lines": ["刚才那点慌张，", "已经被哥哥牵住了"],
            "tail_tip": (932, 360),
            "tail_angle": 122,
            "font_size": 34,
        },
        "b2": {
            "box": (22, 842, 548, 1130),
            "lines": ["下次约会……", "我可以不只当妹妹吗？"],
            "tail_tip": (495, 820),
            "tail_angle": -36,
            "font_size": 33,
        },
        # Left-aligned so the interlaced hands on the lower right stay uncovered.
        "pov_boxes": [
            {
                "cx": 38,
                "y1": 1450,
                "lines": ["你想当什么，我都陪你慢慢来"],
                "font_size": 34,
                "align_box": "left",
            },
            {
                "cx": 38,
                "y1": 1588,
                "lines": ["不过在我这里，你早就不只是妹妹了"],
                "font_size": 32,
                "align_box": "left",
            },
        ],
    },
]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rendered = [base.render_page(spec) for spec in PAGES]
    jpg_streams = []
    for p in rendered:
        buf = io.BytesIO()
        Image.open(p).save(buf, format="JPEG", quality=95, subsampling=0)
        jpg_streams.append(buf.getvalue())
    pdf_path = OUT_DIR / "陪妹妹出门约会_第二话.pdf"
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(jpg_streams))
    print("Generated:", [str(p) for p in rendered], "->", pdf_path)


if __name__ == "__main__":
    main()
