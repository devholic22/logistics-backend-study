# -*- coding: utf-8 -*-
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import *

W, H = 620, 650
s = Svg(W, H, "재고 할당 — 출고 주문 수량을 WMS가 로케이션별로 예약")
s.text(W/2, 40, "재고 할당", 19, INK, 700)
s.text(W/2, 62, "출고 주문을 받아 WMS가 로케이션별 피킹 수량을 예약", 13, INK3)

s.edge([(310, 162), (310, 250)], DASH, True)
s.edge([(290, 341), (290, 400), (155, 400), (155, 470)], DASH, True)
s.edge([(330, 341), (330, 400), (465, 400), (465, 470)], DASH, True)
s.card(160, 90, 300, "출고 주문", ["오더별 물량"], SLATE)
s.card(130, 250, 360, "WMS", ["*할당 = 로케이션별 수량 예약"], GREEN, title_size=20)
s.card(40, 470, 230, "로케이션 A5", ["3개 예약"], AMBER)
s.card(350, 470, 230, "로케이션 B2", ["2개 예약"], AMBER)
s.pill(310, 206, "출고지시", DASH)
s.pill(155, 400, "예약", DASH)
s.pill(465, 400, "예약", DASH)

pathlib.Path(sys.argv[1]).write_text(s.render(), encoding="utf-8")
