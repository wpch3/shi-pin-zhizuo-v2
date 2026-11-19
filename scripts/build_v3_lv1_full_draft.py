#!/usr/bin/env python3
"""Typeset the complete nine-page Yuzu/NTR-author punishment draft."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / 'art' / 'v3-lv1'
OUT = ROOT / 'deliverables' / 'v3-lv1-full-draft'
VERT = ROOT / 'deliverables' / 'v3-lv1-full-draft-vertical'
FONT = ROOT / '.cache' / 'fonts' / 'NotoSansSC-variable.ttf'
W, H, M = 1440, 1920, 36
PAPER = (247, 242, 232)
INK = (41, 36, 32)
FILL = (250, 247, 239, 248)


def fnt(size):
    return ImageFont.truetype(str(FONT), size)


def box(draw, xy, lines, size=37, radius=20, pad=18, fill=FILL, align='center', shape='rect'):
    x1,y1,x2,y2 = xy
    if shape == 'bubble':
        draw.ellipse(xy, fill=fill, outline=INK, width=4)
    else:
        draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=INK, width=4)
    ft=fnt(size); line_h=size+10
    total=line_h*len(lines)-10
    y=y1+(y2-y1-total)//2
    for line in lines:
        bb=draw.textbbox((0,0),line,font=ft,stroke_width=1)
        tw=bb[2]-bb[0]
        x=x1+pad if align=='left' else x1+(x2-x1-tw)//2
        draw.text((x,y),line,font=ft,fill=INK,stroke_width=1,stroke_fill=INK)
        y+=line_h


def make_page(src, captions=(), cover=False):
    raw=Image.open(ART/src).convert('RGB').resize((W-2*M,H-2*M),Image.Resampling.LANCZOS)
    page=Image.new('RGB',(W,H),PAPER); page.paste(raw,(M,M))
    d=ImageDraw.Draw(page,'RGBA')
    d.rectangle((M,M,W-M,H-M),outline=INK,width=4)
    if cover:
        # title occupies the intentionally empty upper-left wall
        d.rounded_rectangle((74,74,650,150),radius=12,fill=FILL,outline=INK,width=4)
        ft=fnt(38); label='第 1 话'
        bb=d.textbbox((0,0),label,font=ft,stroke_width=1)
        d.text((98,90),label,font=ft,fill=INK,stroke_width=1,stroke_fill=INK)
        d.rounded_rectangle((74,174,725,405),radius=10,fill=FILL,outline=INK,width=5)
        ft=fnt(58)
        for txt,y in [('被拒绝的 NTR',199),('老师',273)]:
            d.text((105,y),txt,font=ft,fill=INK,stroke_width=2,stroke_fill=INK)
        box(d,(74,430,675,540),['她看我的眼神，像看一页废稿'],size=30,radius=6)
    for c in captions:
        box(d,c['box'],c['lines'],size=c.get('size',37),radius=c.get('radius',18),align=c.get('align','center'),shape=c.get('shape','rect'))
    return page


def main():
    OUT.mkdir(parents=True,exist_ok=True); VERT.mkdir(parents=True,exist_ok=True)
    specs=[
      ('full-cover.png',[],True,'page-00-cover.png'),
      ('full-01.png',[{'box':(72,68,800,246),'lines':['我靠画 NTR 漫画吃饭。','读者越生气，我的连载越热。'],'size':38}],False,'page-01.png'),
      ('full-02.png',[{'box':(72,68,800,246),'lines':['速写本上写着「柚子」。','我先记住的，却只有她的脸。'],'size':38}],False,'page-02.png'),
      ('full-03.png',[{'box':(72,68,790,246),'lines':['然后，她男朋友坐到了她身边。','她看他的眼神，和看我完全不同。'],'size':36}],False,'page-03.png'),
      ('full-04.png',[{'box':(72,68,780,246),'lines':['我连她的声音都没听过。','表白的台词，倒练了十几遍。'],'size':37}],False,'page-04.png'),
      ('full-05.png',[{'box':(72,68,835,260),'lines':['柚子，我喜欢你。','可以把联系方式给我吗？'],'size':39,'shape':'bubble'}],False,'page-05.png'),
      ('full-06.png',[{'box':(800,58,1360,158),'lines':['请不要用那种眼神看我。'],'size':30,'shape':'bubble'}],False,'page-06.png'),
      ('full-07.png',[{'box':(72,68,700,218),'lines':['我不接受。','请你以后别再来找我。'],'size':34,'shape':'bubble'}],False,'page-07.png'),
      ('full-08.png',[{'box':(72,68,520,162),'lines':['她没有回头。'],'size':38}],False,'page-08.png'),
      ('full-09.png',[{'box':(72,68,760,244),'lines':['我把她画进最后一格。','她走出了画框。'],'size':38},
                      {'box':(930,1578,1358,1700),'lines':['评论：0'],'size':34}],False,'page-09.png'),
    ]
    pages=[]
    for src,caps,iscover,outname in specs:
        im=make_page(src,caps,iscover)
        im.save(OUT/outname,optimize=True)
        pages.append(im)
    pages[0].save(OUT/'被拒绝的NTR老师_第一话_试作.pdf','PDF',save_all=True,append_images=pages[1:],resolution=144.0)

    vpages=[]
    VW,VH=1080,1920; PW,PH=1020,1360; ox,oy=(VW-PW)//2,230
    for i,im in enumerate(pages):
        canvas=Image.new('RGB',(VW,VH),(244,237,225))
        canvas.paste(im.resize((PW,PH),Image.Resampling.LANCZOS),(ox,oy))
        vd=ImageDraw.Draw(canvas); vd.rectangle((ox-2,oy-2,ox+PW+2,oy+PH+2),outline=INK,width=3)
        name=specs[i][3]; canvas.save(VERT/name,optimize=True); vpages.append(canvas)
    vpages[0].save(VERT/'被拒绝的NTR老师_第一话_9x16试作.pdf','PDF',save_all=True,append_images=vpages[1:],resolution=144.0)
    print('Built cover + 9 pages in 3:4 and 9:16 editions.')

if __name__=='__main__': main()
