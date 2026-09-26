# 💱 환율 계산기 Pro

Python Tkinter를 사용한 풀스택 환율 계산기 애플리케이션

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🎯 프로젝트 목표

```
초급 → 중급 개발자를 위한 핸즈온 프로젝트
├─ GUI 프로그래밍 (Tkinter)
├─ REST API 연동 (실시간 데이터)
├─ 데이터베이스 관리 (SQLite)
├─ 데이터 시각화 (Matplotlib)
└─ 배포 & 공유 (PyInstaller, GitHub)
```

---

## ✨ 주요 기능

### 1️⃣ 실시간 환율 변환
- **API**: exchangerate.host (무료, 제한 없음)
- **지원 통화**: USD, EUR, JPY, KRW, CNY, GBP, AUD, CAD, HKD, SGD
- **응답 시간**: < 1초
- **자동 갱신**: 매번 계산할 때마다

### 2️⃣ 계산기 자판
```
온스크린 자판:
┌─────────────────┐
│ 7 8 9 ÷         │
│ 4 5 6 ×         │
│ 1 2 3 −         │
│ 0 . + (2칸)    │
│ AC    ← 삭제    │
└─────────────────┘
```
- 숫자 입력 (0-9)
- 연산자 (+, -, ×, ÷)
- 소수점 지원
- AC (전체 삭제), 한 글자 삭제

### 3️⃣ 환율 변동 그래프
- **Matplotlib** 기반 라인 차트
- **최근 7일** 환율 추세 시각화
- **실시간** 데이터 반영
- 통화 선택 후 "그래프 갱신" 버튼으로 업데이트

### 4️⃣ 거래 기록 관리
- **SQLite 데이터베이스**에 자동 저장
- 거래 내역: 금액, 통화, 환율, 시간
- 최대 **100개** 최근 거래 표시
- "데이터베이스에서 로드" 버튼으로 동기화
- "전체 삭제" 버튼으로 초기화

### 5️⃣ 한국은행 기준 환율 지원
- **data.go.kr** API 연동 (선택)
- 한국 공식 기준 환율
- 설정 탭에서 API 키 입력 가능

---

## 📦 설치

### 요구사항
- Python 3.7 이상
- pip (Python 패키지 관리자)
- Windows, macOS, Linux 지원

### Step 1: 필수 라이브러리 설치

```bash
pip install requests matplotlib
```

### Step 2: 실행

```bash
# Windows / macOS / Linux
python currency_converter_full.py
```

또는

```bash
python3 currency_converter_full.py
```

---

## 💻 사용 방법

### 탭 1: 💻 계산기
```
1. 금액 입력 (또는 계산식)
   예: 100, 50+30, 1000/2

2. 출발지/도착지 통화 선택
   예: USD → KRW

3. 온스크린 자판으로 입력
   - 숫자 및 연산자 클릭
   - 또는 직접 키보드 입력

4. 결과 자동 표시
   100 USD = 130,000 KRW
```

### 탭 2: 📊 그래프
```
- 환율 변동 추이를 라인 차트로 표시
- 통화 선택 후 "그래프 갱신" 클릭
- 7일간의 데이터를 시각화
```

### 탭 3: 📝 거래 기록
```
- 모든 거래 기록 확인
- "데이터베이스에서 로드": 최신 정보 동기화
- "전체 삭제": 기록 초기화 (신중하게!)
```

### 탭 4: ⚙️ 설정
```
- 현재 API 정보 확인 (exchangerate.host)
- 한국은행 API 키 입력 (선택)
- .exe 변환 가이드
- 앱 버전 & 기술 스택 정보
```

---

## 📊 기술 스택

| 역할 | 기술 | 설명 |
|------|------|------|
| GUI | **Tkinter** | Python 표준 GUI 프레임워크 |
| 데이터베이스 | **SQLite** | 경량 파일 기반 DB |
| 그래프 | **Matplotlib** | 파이썬 데이터 시각화 라이브러리 |
| API | **Requests** | HTTP 클라이언트 라이브러리 |
| 배포 | **PyInstaller** | Python 스크립트를 .exe로 변환 |
| 버전관리 | **Git/GitHub** | 코드 관리 & 배포 |

---

## 🔧 고급 사용법

### 계산식 입력
금액 필드에 직접 계산식 입력 가능:

```
입력 예시:
- 50+30 → 80
- 100*1.1 → 110
- 1000/2 → 500
```

### API 키 등록
한국은행 기준 환율을 사용하려면:

1. https://www.data.go.kr/ 접속
2. "기준 환율" 검색
3. "한국은행_기준_환율" 선택
4. "활용신청" 클릭 (자동 승인)
5. API 키 복사
6. 앱의 설정 탭에 붙여넣기

---

## 📦 .exe 변환

### Step 1: PyInstaller 설치
```bash
pip install pyinstaller
```

### Step 2: .exe 생성
```bash
pyinstaller --onefile --windowed currency_converter_full.py
```

### Step 3: 배포
```
생성된 파일:
dist/currency_converter_full.exe

이 파일을 다른 컴퓨터로 옮겨서 바로 실행 가능!
(Python 설치 불필요)
```

---

## 🚀 GitHub 배포

### 저장소 생성
```bash
git init
git add .
git commit -m "Initial commit: Currency Converter Pro"
git remote add origin https://github.com/your-username/currency_converter.git
git branch -M main
git push -u origin main
```

### 이후 업데이트
```bash
git add .
git commit -m "Fix: 그래프 성능 개선"
git push
```

---

## 📁 폴더 구조

```
currency_converter/
├── currency_converter_full.py    # 메인 애플리케이션
├── currency_converter.db          # SQLite DB (자동 생성)
├── api_config.json               # API 키 설정 (자동 생성)
├── README.md
├── CURRENCY_CONVERTER_GUIDE.md    # 상세 가이드
└── .gitignore
```

---

## 🐛 문제 해결

### "ModuleNotFoundError: No module named 'matplotlib'"
```bash
pip install matplotlib
```

### 환율이 로드되지 않음
- 인터넷 연결 확인
- 방화벽 설정 확인
- API 사이트 상태 확인: https://exchangerate.host/

### 데이터베이스 오류
```bash
# DB 파일 삭제 후 재시작
rm currency_converter.db
python currency_converter_full.py
```

### .exe 변환 실패
```bash
# Python이 PATH에 등록되어 있는지 확인
python --version

# PyInstaller 재설치
pip install --upgrade pyinstaller
```

---

## 💡 학습 포인트

이 프로젝트를 통해 배울 수 있는 것들:

```
✅ GUI 프로그래밍
   - Tkinter 위젯 (Button, Entry, Label 등)
   - 탭 인터페이스 (Notebook)
   - 이벤트 처리

✅ API 통합
   - REST API 호출 (requests)
   - JSON 데이터 처리
   - 오류 처리

✅ 데이터베이스
   - SQLite 설계
   - CREATE TABLE, INSERT, SELECT
   - 데이터 조회 & 필터링

✅ 데이터 시각화
   - Matplotlib 그래프
   - Tkinter Canvas에 임베딩

✅ 배포 & 공유
   - PyInstaller로 .exe 변환
   - GitHub 버전 관리
   - 프로젝트 문서화
```

---

## 🎓 포트폴리오 활용

### 3개 프로젝트 포트폴리오

```
1️⃣ 계산기 (기초)
   - Tkinter GUI
   - 기본 이벤트 처리
   
2️⃣ 환율계산기 (중급)
   - API 연동
   - SQLite 데이터베이스
   - Matplotlib 그래프
   
3️⃣ 웹 버전 (고급)
   - HTML/CSS/JS
   - Flask/Django
   - 클라우드 배포
```

### 이력서/포트폴리오에 포함
```
- GitHub 링크
- 스크린샷
- 기술 스택 명시
- 주요 기능 설명
- 배운 점 정리
```

---

## 🔄 계속 개선하기

### 다음 버전 (v1.1)
```
- 오프라인 모드
- 다크 테마
- 알림 기능
- 여러 창 지원
```

### 고급 버전 (v2.0)
```
- 웹 버전 (Flask)
- 모바일 앱 (Kivy)
- 음성 입력
- 클라우드 동기화
```

---

## 📚 참고 자료

### 공식 문서
- [Tkinter Docs](https://docs.python.org/3/library/tkinter.html)
- [Matplotlib Docs](https://matplotlib.org/stable/contents.html)
- [SQLite Docs](https://www.sqlite.org/docs.html)
- [Requests Docs](https://docs.requests.library.org/)

### 튜토리얼
- Python GUI 프로그래밍
- REST API 통합
- SQLite 데이터베이스
- Matplotlib 데이터 시각화

---

## 📝 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

```
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

## 🙋 지원

문제가 발생하면:

1. **CURRENCY_CONVERTER_GUIDE.md** 파일 확인
2. **문제 해결** 섹션 확인
3. **GitHub Issues** 작성
4. 이메일로 문의

---

## 🎉 마무리

이 프로젝트를 완성하신 것을 축하합니다! 🚀

**다음 단계:**
- 친구들과 공유해보세요
- GitHub에 배포하세요
- 포트폴리오에 추가하세요
- 더 많은 기능을 추가해보세요

---

**개발자**: Claude  
**버전**: 1.0.0  
**마지막 업데이트**: 2026년 9월  
**상태**: ✅ 완성 & 배포 가능

🚀 **Happy Coding!**
