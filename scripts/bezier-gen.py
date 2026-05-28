#!/usr/bin/env python3
"""Thick, round, playful outlines tuned to Supercell-Magic proportions.
Key insight: CoC O is 1.03× cap-height wide. We compress to 0.75× for monospace.
"""
from __future__ import annotations
import xml.etree.ElementTree as ET
from pathlib import Path
from math import ceil

ROOT = Path(__file__).resolve().parents[1]
GLYPH_DIR = ROOT / "sources" / "masters" / "Regular.ufo" / "glyphs"
ET.register_namespace("", "http://www.w3.org/2000/svg")

K = 0.552
CAP = 700
XH = 500
CELL = 600

def O(x,y,t="curve"): return (x,y,t)
def off(x,y): return (x,y,"offcurve")
def L(x,y): return O(x,y,"line")
def M(x,y): return O(x,y,"move")
def d(r): return ceil(K*r)

def bc(sx,sy,ex,ey,d1x,d1y,d2x,d2y,r):
    dd=d(r)
    return [off(sx+d1x*dd,sy+d1y*dd),off(ex-d2x*dd,ey-d2y*dd),O(ex,ey)]

def wr(pts):
    c=ET.Element("contour")
    for x,y,t in pts:
        attrs={"x":str(x),"y":str(y)}
        if t!="offcurve": attrs["type"]=t
        ET.SubElement(c,"point",attrs)
    return c

def build(contours):
    el=ET.Element("outline")
    for c in contours: el.append(wr(c))
    return el

def save(path,contours):
    tree=ET.parse(path)
    root=tree.getroot()
    old=root.find("./outline")
    if old is not None: root.remove(old)
    root.append(build(contours))
    ET.indent(tree,space="  ")
    tree.write(path,encoding="UTF-8",xml_declaration=True)

# Rounded rects — wider outer, narrower inner = thicker
def rr_o(x1,y1,x2,y2,r):
    mx=(x1+x2)//2
    return [M(mx,y2),L(x2-r,y2),*bc(x2-r,y2,x2,y2-r,1,0,0,-1,r),
            L(x2,y1+r),*bc(x2,y1+r,x2-r,y1,0,-1,-1,0,r),
            L(x1+r,y1),*bc(x1+r,y1,x1,y1+r,-1,0,0,1,r),
            L(x1,y2-r),*bc(x1,y2-r,x1+r,y2,0,1,1,0,r),L(mx,y2)]

def rr_i(x1,y1,x2,y2,r):
    mx=(x1+x2)//2
    return [M(mx,y2),L(x1+r,y2),*bc(x1+r,y2,x1,y2-r,-1,0,0,-1,r),
            L(x1,y1+r),*bc(x1,y1+r,x1+r,y1,0,-1,1,0,r),
            L(x2-r,y1),*bc(x2-r,y1,x2,y1+r,1,0,0,1,r),
            L(x2,y2-r),*bc(x2,y2-r,x2-r,y2,0,1,-1,0,r),L(mx,y2)]

# ── glyphs (proportions matched to Supercell-Magic, fitted to 600 cell) ──

def O_g(): return [rr_o(80,0,520,CAP,65),rr_i(155,75,445,CAP-75,52)]
def zero_g(): return [rr_o(85,5,515,CAP-5,62),rr_i(158,77,442,CAP-77,48),
                       [M(340,CAP-85),L(260,70),L(230,70),L(310,CAP-85)]]
def C_g():
    r,xl,xr,yt,yb=60,95,505,CAP,0
    return [[M(xr-r,yt),*bc(xr-r,yt,xr,yt-r,-1,0,0,-1,r),
             L(xr,yb+r),*bc(xr,yb+r,xr-r,yb,0,-1,-1,0,r),
             L(xl+r,yb),*bc(xl+r,yb,xl,yb+r,-1,0,0,1,r),
             L(xl,yt-r),*bc(xl,yt-r,xl+r,yt,0,1,1,0,r),L(xr-r,yt)]]
def G_g():
    r,xl,xr,yt,yb=60,95,505,CAP,0
    return [[M(xr-r,yt),*bc(xr-r,yt,xr,yt-r,-1,0,0,-1,r),
             L(xr,yb+r),*bc(xr,yb+r,xr-r,yb,0,-1,-1,0,r),
             L(xl+r,yb),*bc(xl+r,yb,xl,yb+r,-1,0,0,1,r),
             L(xl,yt-r),*bc(xl,yt-r,xl+r,yt,0,1,1,0,r),L(xr-r,yt)],
            [M(280,285),L(xr,285),L(xr,315),L(280,315)]]
def Q_g():
    return [rr_o(80,0,520,CAP,65),rr_i(155,75,445,CAP-75,52),
            [M(310,130),off(360,75),off(430,40),O(460,0),
             L(415,0),off(385,35),off(310,70),O(270,130)]]
def S_g():
    r=60
    return [[M(405,680),*bc(405,680,205,615,1,0,-1,-1,r),
             L(195,500),*bc(195,500,405,400,0,-1,1,-1,r),
             L(405,300),*bc(405,300,195,200,1,0,-1,-1,r),
             L(185,95),*bc(185,95,405,20,0,-1,1,-1,r)]]
def B_g():
    stem=[M(155,0),L(235,0),L(235,CAP),L(155,CAP)]
    top=[M(235,310),off(270,270),off(325,240),O(325,240),
         off(395,155),off(395,55),O(395,0),L(235,0)]
    bot=[M(235,310),off(270,350),off(325,380),O(325,380),
         off(395,555),off(395,645),O(395,CAP),L(235,CAP)]
    return [stem,top,bot]
def D_g():
    stem=[M(155,0),L(235,0),L(235,CAP),L(155,CAP)]
    bowl=[M(235,0),off(400,0),off(465,75),O(465,165),
          off(465,330),off(465,535),O(400,640),
          off(400,CAP),off(235,CAP),O(235,CAP)]
    return [stem,bowl]
def P_g():
    stem=[M(155,0),L(235,0),L(235,CAP),L(155,CAP)]
    bowl=[M(235,360),off(395,360),off(465,435),O(465,495),
          off(465,580),off(395,650),O(395,CAP),L(235,CAP)]
    return [stem,bowl]
def R_g():
    stem=[M(155,0),L(235,0),L(235,CAP),L(155,CAP)]
    bowl=[M(235,360),off(395,360),off(465,435),O(465,495),
          off(465,575),off(395,635),O(395,CAP),L(235,CAP)]
    leg=[M(275,360),L(420,200),L(455,265),L(310,425)]
    return [stem,bowl,leg]
def two_g():
    r=50
    return [[M(210,CAP),*bc(210,CAP,400,CAP-r,1,0,0,-1,r),
             L(400,CAP//2+r),*bc(400,CAP//2+r,210,CAP//2-r,0,-1,-1,0,r),
             L(400,CAP//2-r),*bc(400,CAP//2-r,400,0,-1,0,0,-1,r),L(210,0)]]
def three_g():
    return [[M(200,CAP),*bc(200,CAP,400,CAP-50,1,0,0,-1,50),
             L(400,CAP//2+35),L(200,CAP//2-35),L(400,CAP//2-65),
             *bc(400,CAP//2-65,400,50,-1,0,0,-1,50),
             off(400,0),off(340,0),O(340,0),
             off(220,0),off(175,70),O(175,70)]]
def five_g():
    r=50
    return [[M(390,CAP),L(200,CAP),L(200,CAP//2+65),L(390,CAP//2+65),
             off(390,CAP//2+20),off(390,r),O(350,0),
             *bc(350,0,245,0,-1,0,-1,-1,r),
             off(185,50),off(185,90),O(185,90)]]
def six_g():
    outer=[M(390,CAP-85),off(340,CAP-20),off(230,CAP-20),O(180,CAP-85),
           off(180,CAP//2+50),off(180,50),O(250,0),
           off(345,0),off(395,50),O(395,110),
           off(395,190),off(340,255),O(245,255),
           off(180,190),off(180,65),O(180,65)]
    return [outer,rr_i(225,55,340,215,35)]
def eight_g():
    return [rr_o(175,0,425,CAP,56),rr_i(235,375,365,CAP-60,36),rr_i(235,60,365,325,36)]
def nine_g():
    outer=[M(180,80),off(240,20),off(340,20),O(395,80),
           off(395,255),off(395,430),O(340,480),
           off(245,480),off(185,430),O(185,410),
           off(185,325),off(245,265),O(340,265),
           off(395,325),off(395,460),O(395,460)]
    return [outer,rr_i(245,305,340,420,30)]
def a_g():
    bowl=[M(170,115),off(230,50),off(380,50),O(435,115),
          off(435,335),off(435,440),O(380,500),L(220,500),L(170,440)]
    stem=[M(345,120),L(435,120),L(435,500),L(345,500)]
    return [bowl,stem,rr_i(225,175,350,395,38)]
def c_g():
    r,xl,xr,yt,yb=48,160,440,XH-5,105
    return [[M(xr-r,yt),*bc(xr-r,yt,xr,yt-r,-1,0,0,-1,r),
             L(xr,yb+r),*bc(xr,yb+r,xr-r,yb,0,-1,-1,0,r),
             L(xl+r,yb),*bc(xl+r,yb,xl,yb+r,-1,0,0,1,r),
             L(xl,yt-r),*bc(xl,yt-r,xl+r,yt,0,1,1,0,r),L(xr-r,yt)]]
def e_g():
    outer=[M(435,305),off(435,255),off(435,210),O(380,180),
           off(270,180),off(170,205),O(170,305),
           off(170,430),off(270,500),O(380,500),
           off(435,460),off(435,420),O(435,410)]
    return [outer,[M(190,290),L(370,290),L(370,350),L(190,350)],rr_i(235,240,390,370,30)]
def g_g():
    bowl=rr_o(170,65,435,XH-5,48)
    hole=rr_i(225,120,380,XH-55,36)
    desc=[M(240,XH-55),L(335,XH-55),
          off(335,-100),off(280,-160),O(280,-170),
          *bc(280,-170,335,-200,0,-1,1,0,32),
          off(335,-150),off(335,XH-115),O(240,XH-115)]
    return [bowl,hole,desc]
def o_g(): return [rr_o(170,45,430,XH-5,52),rr_i(235,108,365,XH-62,38)]
def s_lc_g():
    r=46
    return [[M(385,XH-25),*bc(385,XH-25,210,XH-95,1,0,-1,-1,r),
             L(200,XH-155),*bc(200,XH-155,380,XH-250,0,-1,1,-1,r),
             L(380,XH-330),*bc(380,XH-330,210,XH-410,1,0,-1,-1,r),
             L(190,60)]]
def at_g():
    outer=rr_o(125,5,475,CAP-5,62)
    inner=[M(240,270),off(300,220),off(365,220),O(365,270),
           off(365,350),off(365,480),O(300,520),
           off(240,480),off(240,285),O(240,285),
           off(240,270),off(240,270),O(240,270)]
    return [outer,inner,rr_i(275,318,330,480,32)]
def ampersand_g():
    r=50
    return [[M(380,210),*bc(380,210,445,160,-1,0,0,1,r),
             off(445,75),off(380,40),O(380,40),
             off(275,40),off(195,100),O(195,160),
             off(195,260),off(310,350),O(435,410),
             off(435,570),off(370,630),O(285,670),
             off(195,670),off(170,630),O(170,590),
             off(170,515),off(270,455),O(285,445),
             off(210,405),off(170,345),O(170,285),
             off(170,145),off(270,80),O(330,80),
             off(360,80),off(395,120),O(395,160),
             off(395,190),off(380,210),O(380,210)]]

GLYPHS={
    "O":("upper",O_g),"C":("upper",C_g),"G":("upper",G_g),"Q":("upper",Q_g),
    "S":("upper",S_g),"B":("upper",B_g),"D":("upper",D_g),"P":("upper",P_g),
    "R":("upper",R_g),"zero":("core",zero_g),"two":("core",two_g),
    "three":("core",three_g),"five":("core",five_g),"six":("core",six_g),
    "eight":("core",eight_g),"nine":("core",nine_g),
    "a":("lower",a_g),"c":("lower",c_g),"e":("lower",e_g),
    "g":("lower",g_g),"o":("lower",o_g),"s":("lower",s_lc_g),
    "at":("core",at_g),"ampersand":("core",ampersand_g),
}

def main():
    for name,(subdir,fn) in GLYPHS.items():
        path=GLYPH_DIR/subdir/f"{name}.glif"
        if not path.exists(): print(f"SKIP:{path}"); continue
        save(path,fn())
        print(f"OK:{subdir}/{name}.glif")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
