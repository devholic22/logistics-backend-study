# -*- coding: utf-8 -*-
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import *

W, H = 540, 930
s = Svg(W, H, "창고의 존 구성 — 입고·보관·작업·분배·피킹·출고 구역")
s.text(W/2, 40, "창고의 존 구성", 19, INK, 700)
s.text(W/2, 62, "입고에서 출고까지 기능별로 나뉜 물리적 구역", 13, INK3)

s.card(130, 90, 280, "입고존", (), AMBER)
s.panel(80, 205, 380, 476, "창고 중앙", None, True, "center")
s.card(140, 240, 260, "보관존 A", (), BLUE)
s.card(140, 322, 260, "보관존 B", (), BLUE)
s.card(140, 404, 260, "보관존 C", (), BLUE)
s.card(140, 500, 260, "작업존", (), SLATE)
s.card(140, 582, 260, "분배존", (), SLATE)
s.card(130, 720, 280, "피킹존", (), GREEN)
s.card(130, 820, 280, "출고존", (), AMBER)

pathlib.Path(sys.argv[1]).write_text(s.render(), encoding="utf-8")
