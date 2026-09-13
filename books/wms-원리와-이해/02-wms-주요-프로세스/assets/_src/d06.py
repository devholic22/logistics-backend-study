# -*- coding: utf-8 -*-
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import *

W, H = 540, 460
s = Svg(W, H, "재고보충 — 보관존 재고를 피킹존으로 사전 이동")
s.text(W/2, 40, "재고보충", 19, INK, 700)
s.text(W/2, 62, "피킹 전에 보관 재고를 작업자가 접근하기 쉬운 위치로 이동", 13, INK3)

s.edge([(270, 181), (270, 300)])
s.card(100, 90, 340, "보관존", ["보관 전담 · 높은 층 포함"], GREEN)
s.card(100, 300, 340, "피킹존", ["1단 · 손이 닿는 로케이션"], AMBER)
s.pill(270, 241, "재고보충 (사전 이동)", SOLID)

pathlib.Path(sys.argv[1]).write_text(s.render(), encoding="utf-8")
