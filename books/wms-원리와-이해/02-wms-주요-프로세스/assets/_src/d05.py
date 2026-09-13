# -*- coding: utf-8 -*-
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import *

W, H = 660, 650
s = Svg(W, H, "재고이동 작업 — WMS 또는 관리자의 지시와 작업자의 실행")
s.text(W/2, 40, "재고이동 작업", 19, INK, 700)
s.text(W/2, 62, "이동지시는 정보로 전달되고, 실제 재고는 로케이션 사이를 이동", 13, INK3)

s.edge([(245, 187), (245, 274), (290, 274)], DASH, True)
s.edge([(495, 187), (495, 274), (370, 274)], DASH, True)
s.edge([(199, 307), (20, 307), (20, 125), (34, 125)], DASH, True)
s.edge([(266, 446), (394, 446)])
s.card(40, 90, 250, "WMS", ["작업 효율 판단"], GREEN, title_size=20)
s.card(370, 90, 250, "관리자", ["관리 목적 지시"], SLATE)
s.card(205, 280, 250, "작업자", (), SLATE)
s.card(50, 410, 210, "로케이션 A", (), AMBER)
s.card(400, 410, 210, "로케이션 B", (), AMBER)
s.pill(245, 225, "이동지시 생성", DASH)
s.pill(490, 225, "이동지시 생성", DASH)
s.pill(100, 307, "작업 결과 입력 → 완료", DASH)
s.pill(330, 446, "실재고 이동", SOLID)
s.legend(40, H - 24, [("solid", "재고의 물리적 이동"), ("dash", "정보 흐름")])

pathlib.Path(sys.argv[1]).write_text(s.render(), encoding="utf-8")
