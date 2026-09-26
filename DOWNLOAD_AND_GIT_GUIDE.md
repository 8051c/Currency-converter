# 📦 다운로드 & Git/GitHub 배포 가이드

## 1️⃣ 다운로드할 파일 목록

### 필수 파일 (다운로드 받아야 함)

```
📁 downloads/
├── currency_converter_clean.py           ⭐ 메인 프로그램 (필수!)
├── currency_converter_presentation.pptx  📊 PPT 프레젠테이션
├── README.md                             📖 사용 설명서
├── requirements.txt                      📋 의존성 목록
└── .gitignore                            🔒 Git 무시 파일
```

### 사용하지 않을 파일 (다운로드 불필요)

```
❌ create_currency_converter_ppt.js  (PPT 생성 스크립트, 이미 PPT 생성됨)
❌ create_currency_converter_ppt.py  (구형 PPT 생성 스크립트)
❌ currency_converter_*.py           (구버전 파일들)
❌ CURRENCY_CONVERTER_GUIDE.md       (구형 가이드)
❌ DEPLOYMENT_CHECKLIST.md           (구형 체크리스트)
❌ README_CURRENCY_CONVERTER.md      (구형 설명서)
```

---

## 2️⃣ GitHub 배포 단계별 가이드

### Step 1: GitHub 저장소 생성

1. https://github.com/new 접속
2. Repository name: `currency_converter` 입력
3. Description: `Real-time currency converter with 50-day trend analysis`
4. "Create repository" 클릭

### Step 2: 로컬 폴더 준비

```bash
# 로컬 폴더 생성
mkdir currency_converter
cd currency_converter

# 다운로드한 파일 이 폴더에 복사:
#  - currency_converter_clean.py
#  - README.md
#  - requirements.txt
#  - .gitignore
```

### Step 3: Git 초기화 및 커밋

```bash
# Git 초기화
git init

# 사용자 정보 설정 (처음 한 번만)
git config user.name "Your Name"
git config user.email "your-email@example.com"

# 모든 파일 스테이징
git add .

# 첫 번째 커밋
git commit -m "Initial commit: Currency converter application"
```

### Step 4: 원격 저장소 연결

```bash
# GitHub에서 복사한 저장소 URL 사용 (예시)
git remote add origin https://github.com/your-username/currency_converter.git

# 브랜치명 변경 (GitHub 권장)
git branch -M main

# 푸시
git push -u origin main
```

### Step 5: GitHub에서 확인

- https://github.com/your-username/currency_converter 접속
- 파일 확인:
  - ✅ currency_converter_clean.py
  - ✅ README.md
  - ✅ requirements.txt
  - ✅ .gitignore

---

## 3️⃣ 이후 업데이트 방법

### 파일 수정 후 커밋

```bash
# 변경사항 확인
git status

# 모든 변경사항 스테이징
git add .

# 커밋
git commit -m "Fix: 버그 수정 설명"

# 푸시
git push
```

### 여러 커밋 예시

```bash
# 기능 추가
git commit -m "Feature: 새로운 기능 추가"

# 버그 수정
git commit -m "Fix: 버그 수정 설명"

# 문서 수정
git commit -m "Docs: README 업데이트"

# 성능 개선
git commit -m "Perf: 성능 개선 설명"
```

---

## 4️⃣ 최종 폴더 구조

GitHub 업로드 후 최종 모습:

```
currency_converter/
├── currency_converter_clean.py    # 메인 프로그램 (Python 스크립트)
├── README.md                       # 프로젝트 설명
├── requirements.txt                # 의존성 (pip install -r requirements.txt)
└── .gitignore                      # Git이 추적하지 않을 파일
```

---

## 5️⃣ 추가 옵션

### GitHub Pages (선택사항)

프로젝트 페이지를 웹에 공개하려면:

1. GitHub 저장소 설정 → Pages
2. Source: main branch
3. 저장
4. https://your-username.github.io/currency_converter 에서 확인

### Releases 생성 (선택사항)

```bash
# 태그 생성
git tag v1.0.0 -m "First release"

# 푸시
git push origin v1.0.0
```

그 다음 GitHub에서:
1. Releases → Create a new release
2. Tag: v1.0.0 선택
3. Title: "Version 1.0.0"
4. Release notes 작성
5. "Publish release" 클릭

---

## 6️⃣ 문제 해결

### "fatal: not a git repository" 오류
```bash
# git이 초기화되지 않음
git init
```

### "remote already exists" 오류
```bash
# 기존 원격 제거 후 다시 추가
git remote remove origin
git remote add origin https://github.com/your-username/currency_converter.git
```

### "Permission denied" 오류
```bash
# SSH 키 설정 또는 GitHub 토큰 사용
# https://docs.github.com/en/authentication
```

### 모든 것을 초기화하고 싶음
```bash
# 주의: 모든 커밋 히스토리 삭제됨
rm -rf .git
git init
git add .
git commit -m "Initial commit"
```

---

## 7️⃣ 체크리스트

- [ ] 5개 필수 파일 준비
  - [ ] currency_converter_clean.py
  - [ ] README.md
  - [ ] requirements.txt
  - [ ] .gitignore
  - [ ] (선택) currency_converter_presentation.pptx

- [ ] GitHub 저장소 생성

- [ ] 로컬 폴더에서 Git 초기화

- [ ] 파일 커밋 및 푸시

- [ ] GitHub에서 파일 확인

- [ ] README 한국어/영문 정리 (선택)

- [ ] 릴리스 생성 (선택)

---

**성공! 🎉 이제 GitHub에 프로젝트가 배포되었습니다!**

