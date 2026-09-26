# 💱 환율 계산기 Pro - 완벽 가이드

## 📋 목차
1. [설치 방법](#설치-방법)
2. [사용 방법](#사용-방법)
3. [기능](#기능)
4. [.exe 변환](#exe-변환)
5. [GitHub 배포](#github-배포)
6. [API 연동](#api-연동)

---

## 🚀 설치 방법

### 요구사항
- Python 3.7 이상
- pip (Python 패키지 관리자)
- Windows, macOS, Linux 모두 지원

### Step 1: 필수 라이브러리 설치

```bash
# 기본 라이브러리
pip install requests

# 그래프 관련
pip install matplotlib

# (선택) .exe 변환 시
pip install pyinstaller
```

### Step 2: 파일 다운로드
```
currency_converter_full.py 를 원하는 폴더에 저장
```

### Step 3: 실행

```bash
# Windows
python currency_converter_full.py

# macOS / Linux
python3 currency_converter_full.py
```

---

## 💻 사용 방법

### 탭 1: 💻 계산기
```
1. 금액 입력 (또는 계산식 입력 가능)
   예: 100, 50+30, 1000/2

2. 출발지/도착지 통화 선택
   - USD, EUR, JPY, KRW, CNY 등 10가지 통화

3. 온스크린 자판으로 입력
   - 숫자: 0-9
   - 연산자: ÷, ×, −, +
   - AC (초기화), 삭제

4. 변환 결과 자동 표시
```

### 탭 2: 📊 그래프
```
- 최근 7일 환율 변동 시각화
- 라인 차트로 추세 확인
- 통화 선택 후 "그래프 갱신" 버튼 클릭
```

### 탭 3: 📝 거래 기록
```
- 모든 거래 기록 저장 (SQLite)
- 최대 100개 거래 표시
- "데이터베이스에서 로드" 버튼으로 최신 정보 동기화
- "전체 삭제" 버튼으로 기록 초기화
```

### 탭 4: ⚙️ 설정
```
- 현재 사용 중인 API 확인 (exchangerate.host)
- 한국은행 기준 환율 API 키 입력
- .exe 변환 가이드
- 앱 정보
```

---

## ✨ 기능

### 1️⃣ 실시간 환율 변환
- **API**: exchangerate.host (무료, 제한 없음)
- **응답 시간**: < 1초
- **지원 통화**: 150+ 개국

### 2️⃣ 계산기 자판
- 숫자 0-9
- 연산자: +, -, ×, ÷
- 소수점 지원
- AC (전체 삭제), 한 글자 삭제

### 3️⃣ 환율 변동 그래프
- Chart.js → Matplotlib 렌더링
- 최근 7일 추세 시각화
- 실시간 업데이트

### 4️⃣ 거래 기록 저장
- SQLite 데이터베이스
- 거래 내역: 금액, 통화, 환율, 시간
- 최대 100개 최근 기록 표시

### 5️⃣ 한국은행 API 지원 (선택)
- 한국은행 기준 환율 사용 가능
- 더 신뢰도 높은 데이터
- data.go.kr에서 무료 신청

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

### Step 3: 실행 파일 위치
```
dist/currency_converter_full.exe
```

### Step 4: 배포
```
- dist 폴더의 .exe 파일을 복사
- 다른 컴퓨터에서 바로 실행 가능 (Python 설치 불필요)
- 친구들과 공유 가능!
```

### ⚠️ 주의사항
- 윈도우 Defender 경고 무시 (안전함)
- 파일 크기: 약 100-150MB (matplotlib 포함)
- 첫 실행 시 약간 느릴 수 있음 (정상)

---

## 🔧 GitHub 배포

### Step 0: GitHub 계정 생성
https://github.com (무료)

### Step 1: 저장소 생성
```
1. GitHub 로그인
2. 오른쪽 위 + 아이콘 → "New repository"
3. Repository name: currency_converter
4. 설명: "환율 계산기 - Python Tkinter 앱"
5. Create repository
```

### Step 2: Git 설정 (처음 1회)
```bash
git config --global user.name "당신의 이름"
git config --global user.email "당신의 이메일"
```

### Step 3: 로컬 폴더에서 초기화
```bash
# 프로젝트 폴더로 이동
cd path/to/your/folder

# Git 초기화
git init

# 모든 파일 추가
git add .

# 첫 번째 커밋
git commit -m "Initial commit: Currency Converter Pro"

# 원격 저장소 추가 (GitHub에서 복사한 URL)
git remote add origin https://github.com/your-username/currency_converter.git

# 메인 브랜치로 변경
git branch -M main

# Push
git push -u origin main
```

### Step 4: 이후 업데이트
```bash
# 파일 수정 후
git add .
git commit -m "Fix: 그래프 성능 개선"
git push
```

---

## 📁 폴더 구조

```
currency_converter/
├── currency_converter_full.py    # 메인 애플리케이션
├── currency_converter.db          # SQLite 데이터베이스 (자동 생성)
├── api_config.json               # API 키 설정 (자동 생성)
├── README.md                      # 프로젝트 설명
└── CURRENCY_CONVERTER_GUIDE.md    # 이 파일
```

---

## 🔌 API 연동

### 현재 사용 중: exchangerate.host
```
✅ 완전 무료
✅ 가입 불필요
✅ 150+ 통화 지원
✅ 응답 빠름
```

### 선택사항: 한국은행 기준 환율

#### 1단계: API 키 신청
```
1. https://www.data.go.kr/ 접속
2. 검색창에 "기준 환율" 입력
3. "한국은행_기준_환율" API 선택
4. "활용신청" 버튼 클릭
5. 약 1-2분 후 승인 (자동)
6. API 키 발급
```

#### 2단계: 앱에 설정
```
1. 환율 계산기 실행
2. "⚙️ 설정" 탭 이동
3. "API 키" 입력란에 붙여넣기
4. "저장" 버튼 클릭
```

---

## 💡 팁

### 계산식 입력
```
금액 필드에 직접 계산식 입력 가능:
- 50+30 → 80
- 100*1.1 → 110
- 1000/2 → 500
```

### 빠른 환율 업데이트
```
"환율 새로고침" 버튼 클릭 (5-10초 대기)
```

### 거래 기록 관리
```
📝 거래 기록 탭에서 모든 기록 확인 가능
최대 100개까지 저장
"전체 삭제"로 초기화 가능
```

---

## 🐛 문제 해결

### 1. "ModuleNotFoundError: No module named 'matplotlib'"
```bash
pip install matplotlib
```

### 2. 환율이 로드되지 않음
```bash
# 인터넷 연결 확인
# 방화벽 설정 확인
# API 사이트 상태 확인: https://exchangerate.host/
```

### 3. 데이터베이스 오류
```bash
# currency_converter.db 파일 삭제
# 앱 재시작 (자동으로 새 데이터베이스 생성)
```

### 4. .exe 변환 실패
```bash
# Python이 PATH에 등록되어 있는지 확인
python --version

# PyInstaller 재설치
pip install --upgrade pyinstaller
```

---

## 📚 다음 단계

### 웹 버전
```
HTML/CSS/JavaScript로 웹앱 만들기
Vercel/GitHub Pages에 배포
```

### 모바일 앱
```
Kivy 프레임워크 사용
Android/iOS 앱 빌드
```

### 고급 기능
```
- 음성 입력 (텍스트-투-스피치)
- 오프라인 모드
- 다크 테마 추가
- 여러 계산기 창 지원
```

---

## 📞 지원

문제가 발생하면:
1. README.md 파일 확인
2. GitHub Issues 확인
3. 커뮤니티 포럼 검색

---

## 📄 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

---

**버전**: 1.0.0  
**마지막 업데이트**: 2026년 9월  
**개발자**: Claude  

🚀 즐거운 사용되길!
