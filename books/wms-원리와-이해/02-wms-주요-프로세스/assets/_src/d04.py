# -*- coding: utf-8 -*-
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import *

W, H = 600, 720
s = Svg(W, H, "적치 작업 — WMS 지시와 작업 결과, 입고존에서 보관존으로의 이동")
s.text(W/2, 40, "적치 작업", 19, INK, 700)
s.text(W/2, 62, "점선은 작업 정보, 실선은 입고존에서 보관존으로의 재고 이동", 13, INK3)

s.panel(35, 440, 530, 170, "창고 현장", None, True)
s.edge([(282, 181), (282, 265)], DASH, True)
s.edge([(318, 337), (318, 390), (500, 390), (500, 125), (440, 125)], DASH, True)
s.edge([(235, 512), (365, 512)])
s.card(160, 90, 280, "WMS", ["카테고리 · 기존 재고 현황 분석"], GREEN, title_size=20)
s.card(160, 265, 280, "작업자", ["무선 모바일 장비"], SLATE)
s.card(55, 476, 180, "입고존", (), AMBER)
s.card(365, 476, 180, "보관존", ["지정된 최적 로케이션"], AMBER, title_size=15)
s.pill(282, 223, "적치지시", DASH)
s.pill(500, 250, "작업 결과 전송", DASH)
s.pill(300, 512, "재고 이동", SOLID)
s.legend(40, H - 24, [("solid", "재고의 물리적 이동"), ("dash", "정보 흐름")])

pathlib.Path(sys.argv[1]).write_text(s.render(), encoding="utf-8")
