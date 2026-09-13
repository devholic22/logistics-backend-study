# -*- coding: utf-8 -*-
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import *

W, H = 700, 830
s = Svg(W, H, "피킹과 출고 — 출고존 인수인계와 출고전표 증빙 흐름")
s.text(W/2, 40, "피킹과 출고", 19, INK, 700)
s.text(W/2, 62, "실선은 재고 이동, 점선은 출고전표의 출력·서명·증빙 흐름", 13, INK3)

s.edge([(270, 162), (270, 270)])
s.edge([(270, 361), (270, 580)])
s.edge([(420, 315), (505, 315), (505, 430)], DASH, True)
s.edge([(505, 521), (505, 615), (420, 615)], DASH, True)
s.card(120, 90, 300, "피킹존", (), AMBER)
s.card(120, 270, 300, "출고존", ["출고 시 재고 차감"], GREEN)
s.card(460, 430, 210, "출고전표", ["거래명세서 · 송장"], AMBER, title_size=15)
s.card(120, 580, 300, "출고처 · 고객", ["배송 차량 상차"], SLATE)
s.pill(270, 215, "⑥ 피킹", SOLID)
s.pill(270, 470, "⑦ 출고 · 인수인계", SOLID)
s.pill(505, 370, "출력 → 사인", DASH)
s.pill(505, 570, "사인 → 상호 증빙", DASH)
s.legend(40, H - 24, [("solid", "재고의 물리적 이동"), ("dash", "정보 흐름")])

pathlib.Path(sys.argv[1]).write_text(s.render(), encoding="utf-8")
