# -*- coding: utf-8 -*-
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import *

W, H = 660, 920
s = Svg(W, H, "크로스도킹 — 보관존을 거치지 않고 입고 당일 출고하는 흐름")
s.text(W/2, 40, "크로스도킹", 19, INK, 700)
s.text(W/2, 62, "입고 재고를 보관존에 적치하지 않고 분배해 바로 출고", 13, INK3)

s.edge([(250, 162), (250, 250)])
s.edge([(250, 322), (250, 440)])
s.edge([(250, 531), (250, 650)])
s.edge([(400, 286), (530, 286), (530, 420)], DASH, True)
s.card(100, 90, 300, "공장 · 공급사", (), SLATE)
s.card(100, 250, 300, "입고존", (), AMBER)
s.card(100, 440, 300, "분배존", ["대기 또는 분류 작업"], GREEN)
s.card(430, 420, 200, "보관존", ["적치 · 재고관리"], SLATE, title_size=15)
s.card(100, 650, 300, "출고존", (), AMBER)
s.pill(250, 206, "당일 입고", SOLID)
s.pill(250, 381, "크로스도킹", SOLID)
s.pill(250, 590, "바로 출고", SOLID)
s.pill(530, 350, "거치지 않음", DASH)
s.legend(40, H - 24, [("solid", "재고의 물리적 이동"), ("dash", "정보 흐름")])

pathlib.Path(sys.argv[1]).write_text(s.render(), encoding="utf-8")
