from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

# PPT 생성
prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

# 색상 정의
COLOR_PRIMARY = RGBColor(42, 120, 214)  # 파란색
COLOR_ACCENT = RGBColor(240, 173, 78)  # 주황색
COLOR_DANGER = RGBColor(217, 83, 79)   # 빨간색
COLOR_SUCCESS = RGBColor(92, 184, 92)  # 초록색
COLOR_TEXT = RGBColor(51, 51, 51)      # 진회색
COLOR_LIGHT = RGBColor(245, 245, 245)  # 밝은회색

def add_title_slide(prs, title, subtitle):
    """제목 슬라이드 추가"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # 빈 레이아웃
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_PRIMARY
    
    # 제목
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(9), Inches(1.5))
    title_frame = title_box.text_frame
    title_frame.word_wrap = True
    title_p = title_frame.paragraphs[0]
    title_p.text = title
    title_p.font.size = Pt(54)
    title_p.font.bold = True
    title_p.font.color.rgb = RGBColor(255, 255, 255)
    title_p.alignment = PP_ALIGN.CENTER
    
    # 부제
    subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(4.2), Inches(9), Inches(1))
    subtitle_frame = subtitle_box.text_frame
    subtitle_p = subtitle_frame.paragraphs[0]
    subtitle_p.text = subtitle
    subtitle_p.font.size = Pt(24)
    subtitle_p.font.color.rgb = RGBColor(255, 255, 255)
    subtitle_p.alignment = PP_ALIGN.CENTER

def add_content_slide(prs, title, content_list):
    """콘텐츠 슬라이드 추가"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 제목
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_p = title_frame.paragraphs[0]
    title_p.text = title
    title_p.font.size = Pt(40)
    title_p.font.bold = True
    title_p.font.color.rgb = COLOR_PRIMARY
    
    # 제목 아래 줄
    line_shape = slide.shapes.add_shape(1, Inches(0.5), Inches(1.3), Inches(9), Inches(0))
    line_shape.line.color.rgb = COLOR_PRIMARY
    line_shape.line.width = Pt(3)
    
    # 콘텐츠
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(8.4), Inches(5.4))
    text_frame = content_box.text_frame
    text_frame.word_wrap = True
    
    for idx, content in enumerate(content_list):
        if idx > 0:
            text_frame.add_paragraph()
        
        p = text_frame.paragraphs[idx]
        p.text = content
        p.font.size = Pt(16)
        p.font.color.rgb = COLOR_TEXT
        p.space_before = Pt(8)
        p.space_after = Pt(8)
        p.level = 0

def add_two_column_slide(prs, title, left_title, left_items, right_title, right_items):
    """2열 슬라이드"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 제목
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_p = title_frame.paragraphs[0]
    title_p.text = title
    title_p.font.size = Pt(40)
    title_p.font.bold = True
    title_p.font.color.rgb = COLOR_PRIMARY
    
    # 제목 아래 줄
    line_shape = slide.shapes.add_shape(1, Inches(0.5), Inches(1.3), Inches(9), Inches(0))
    line_shape.line.color.rgb = COLOR_PRIMARY
    line_shape.line.width = Pt(3)
    
    # 왼쪽 컬럼
    left_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.6), Inches(4.5), Inches(5.4))
    left_frame = left_box.text_frame
    left_frame.word_wrap = True
    
    # 왼쪽 제목
    left_p = left_frame.paragraphs[0]
    left_p.text = left_title
    left_p.font.size = Pt(18)
    left_p.font.bold = True
    left_p.font.color.rgb = COLOR_ACCENT
    
    # 왼쪽 항목
    for item in left_items:
        p = left_frame.add_paragraph()
        p.text = item
        p.font.size = Pt(14)
        p.font.color.rgb = COLOR_TEXT
        p.level = 1
        p.space_before = Pt(4)
    
    # 오른쪽 컬럼
    right_box = slide.shapes.add_textbox(Inches(5.2), Inches(1.6), Inches(4.3), Inches(5.4))
    right_frame = right_box.text_frame
    right_frame.word_wrap = True
    
    # 오른쪽 제목
    right_p = right_frame.paragraphs[0]
    right_p.text = right_title
    right_p.font.size = Pt(18)
    right_p.font.bold = True
    right_p.font.color.rgb = COLOR_SUCCESS
    
    # 오른쪽 항목
    for item in right_items:
        p = right_frame.add_paragraph()
        p.text = item
        p.font.size = Pt(14)
        p.font.color.rgb = COLOR_TEXT
        p.level = 1
        p.space_before = Pt(4)

# 슬라이드 생성

# 1. 표지
add_title_slide(prs, "💱 환율 계산기 Pro", "Python Tkinter + SQLite + Matplotlib")

# 2. 프로젝트 개요
add_content_slide(prs, "프로젝트 개요", [
    "✅ 실시간 환율 변환 (150+ 통화)",
    "✅ 온스크린 자판 계산기",
    "✅ 환율 변동 그래프 시각화",
    "✅ 거래 기록 저장 & 관리",
    "✅ 한국은행 기준 환율 지원",
    "✅ 데스크톱 앱 (.exe 변환 가능)"
])

# 3. 핵심 기능
add_two_column_slide(prs, "핵심 기능", 
    "통화 환전",
    [
        "✓ 실시간 환율",
        "✓ 10가지 주요 통화",
        "✓ 양방향 변환",
        "✓ 정확한 계산"
    ],
    "데이터 관리",
    [
        "✓ SQLite DB",
        "✓ 거래 기록 저장",
        "✓ 최근 100개 기록",
        "✓ 시간별 환율 추적"
    ]
)

# 4. 기술 스택
add_content_slide(prs, "기술 스택", [
    "🐍 Python 3.7+",
    "🎨 Tkinter (GUI 프레임워크)",
    "📊 Matplotlib (그래프 시각화)",
    "💾 SQLite (데이터베이스)",
    "🌐 Requests (HTTP 요청)",
    "📦 PyInstaller (.exe 변환)"
])

# 5. UI 탭 구성
add_content_slide(prs, "UI 탭 구성", [
    "💻 Tab 1: 계산기",
    "    - 금액 입력, 통화 선택, 온스크린 자판",
    "",
    "📊 Tab 2: 그래프",
    "    - 최근 7일 환율 변동 시각화",
    "",
    "📝 Tab 3: 거래 기록",
    "    - SQLite에서 로드, 전체 보기",
    "",
    "⚙️ Tab 4: 설정",
    "    - API 키 입력, 정보, .exe 변환 가이드"
])

# 6. 환율 API
add_two_column_slide(prs, "환율 API",
    "현재 사용",
    [
        "✓ exchangerate.host",
        "✓ 무료, 제한 없음",
        "✓ 150+ 통화",
        "✓ 응답 빠름"
    ],
    "선택사항",
    [
        "✓ 한국은행 기준",
        "✓ data.go.kr",
        "✓ 더 신뢰도 높음",
        "✓ 한국 중심 데이터"
    ]
)

# 7. 설치 방법
add_content_slide(prs, "설치 방법 (3단계)", [
    "Step 1️⃣: 라이브러리 설치",
    "    pip install requests matplotlib",
    "",
    "Step 2️⃣: 프로젝트 파일 저장",
    "    currency_converter_full.py",
    "",
    "Step 3️⃣: 실행",
    "    python currency_converter_full.py"
])

# 8. 거래 기록 관리
add_content_slide(prs, "거래 기록 & 데이터 관리", [
    "💾 모든 거래를 SQLite에 자동 저장",
    "   - 거래 금액, 통화, 환율, 시간",
    "",
    "📊 환율 기록도 시계열로 저장",
    "   - 그래프 생성에 사용",
    "",
    "🔄 \"데이터베이스에서 로드\" 버튼",
    "   - 최근 100개 거래 표시",
    "",
    "🗑️ \"전체 삭제\" 버튼",
    "   - 기록 초기화 (신중하게 사용)"
])

# 9. .exe 변환
add_content_slide(prs, ".exe 변환 (배포)", [
    "Step 1️⃣: PyInstaller 설치",
    "    pip install pyinstaller",
    "",
    "Step 2️⃣: .exe 생성",
    "    pyinstaller --onefile --windowed currency_converter_full.py",
    "",
    "Step 3️⃣: 배포",
    "    dist/currency_converter_full.exe → 공유 가능!",
    "",
    "✅ Python 설치 없이 어디서나 실행 가능"
])

# 10. GitHub 배포
add_content_slide(prs, "GitHub 배포", [
    "1️⃣ GitHub에서 새 저장소 생성",
    "    https://github.com/new",
    "",
    "2️⃣ 로컬에서 Git 초기화",
    "    git init && git add . && git commit -m 'Initial commit'",
    "",
    "3️⃣ 원격 저장소 연결 & Push",
    "    git remote add origin <URL>",
    "    git push -u origin main",
    "",
    "4️⃣ 이후 업데이트",
    "    git add . && git commit -m '설명' && git push"
])

# 11. 프로젝트 구조
add_content_slide(prs, "프로젝트 구조", [
    "currency_converter/",
    "├── currency_converter_full.py  (메인 앱)",
    "├── currency_converter.db       (자동 생성)",
    "├── api_config.json            (자동 생성)",
    "├── README.md",
    "├── CURRENCY_CONVERTER_GUIDE.md",
    "└── .gitignore",
    "",
    "dist/",
    "└── currency_converter_full.exe (PyInstaller)"
])

# 12. 다음 단계
add_two_column_slide(prs, "다음 단계",
    "고급 기능",
    [
        "✓ 웹 버전 개발",
        "✓ 모바일 앱 (Kivy)",
        "✓ 음성 입력",
        "✓ 다크 테마"
    ],
    "포트폴리오",
    [
        "✓ 3개 프로젝트 완성",
        "✓ GitHub 배포",
        "✓ 이력서 추가",
        "✓ 면접 준비"
    ]
)

# 13. 마무리
add_title_slide(prs, "프로젝트 완성! 🎉", "GitHub에 배포하고 포트폴리오에 추가하세요!")

# PPT 저장
prs.save("currency_converter_pro.pptx")
print("✅ PPT 생성 완료: currency_converter_pro.pptx")
