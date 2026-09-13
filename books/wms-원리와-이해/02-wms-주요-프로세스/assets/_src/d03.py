# -*- coding: utf-8 -*-
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import *

W, H = 540, 600
s = Svg(W, H, "입고와 검수 — 상품 도착 후 입고존에 임시 보관되는 흐름")
s.text(W/2, 40, "입고와 검수", 19, INK, 700)
s.text(W/2, 62, "입고존의 재고는 검수를 마쳐도 아직 판매 가능 재고가 아니다", 13, INK3)

s.edge([(270, 162), (270, 248)])
s.edge([(270, 339), (270, 440)], DASH, True)
s.card(110, 90, 320, "공급처 · 공장", (), SLATE)
s.card(110, 248, 320, "입고존", ["임시 보관"], GREEN)
s.card(110, 440, 320, "판매 가능 재고", (), SLATE)
s.pill(270, 205, "상품 도착 → 검수 → 인수", SOLID)
s.pill(270, 390, "가용재고에는 미반영", DASH)
s.legend(40, H - 24, [("solid", "재고의 물리적 이동"), ("dash", "정보 흐름")])

pathlib.Path(sys.argv[1]).write_text(s.render(), encoding="utf-8")
