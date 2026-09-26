# 💱 환율 계산기 (Currency Converter)

실시간 환율 변환 및 지난 50일 추세 분석을 위한 Python 데스크톱 애플리케이션입니다.

## ✨ 주요 기능

- **💻 실시간 환율 변환**: 160+ 통화 지원, 온스크린 자판
- **📊 7일 추세 그래프**: 최근 7일 환율 변동 추세
- **📊 50일 추세 그래프**: 최근 50일 장기 환율 변동
- **📈 고급 분석**: 이동평균선(MA7) 분석
- **📉 통계 정보**: 현재/최고/최저/평균 환율, 변화율, 변동성
- **🔄 자동 갱신**: 탭 변경 시 자동 업데이트, 날짜 변경 시 자동 갱신
- **🗑️ DB 불필요**: 메모리 기반 (깨끗하고 빠름)

## 🎨 UI 구성 (5개 탭)

| 탭 | 설명 | 기능 |
|---|---|---|
| 💻 계산기 | 실시간 환율 변환 | 통화 선택 + 계산기 자판 |
| 📊 7일 추세 | 최근 7일 그래프 | 단기 변동성 분석 |
| 📊 50일 추세 | 최근 50일 그래프 | 장기 추세 분석 |
| 📈 고급분석 | 이동평균선 분석 | 7일 데이터 + MA7 |
| 📉 통계 | 상세 통계 정보 | 현재/최고/최저/평균 등 |

## 🛠️ 기술 스택

- **언어**: Python 3.7+
- **GUI**: Tkinter
- **그래프**: Matplotlib
- **HTTP**: Requests
- **데이터 분석**: NumPy
- **API**: open.er-api.com (무료, API 키 불필요)

## 📋 시스템 요구사항

- Python 3.7 이상
- 인터넷 연결 필수
- Windows / macOS / Linux

## 🚀 설치

### 1단계: 저장소 클론

```bash
git clone https://github.com/8051c/currency-converter.git
cd currency-converter
```

### 2단계: 의존성 설치

```bash
pip install -r requirements.txt
```

또는 수동 설치:

```bash
pip install requests matplotlib numpy
```

## ▶️ 실행

### Python으로 실행

```bash
python currency_converter_clean.py
```

### .exe 파일로 변환 (Windows)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed currency_converter_clean.py
```

생성된 파일: `dist/currency_converter_clean.exe`

## 📖 사용 방법

### 💻 계산기 탭

- 좌측 드롭다운: 출발 통화 선택
- 우측 드롭다운: 도착 통화 선택
- 온스크린 자판 또는 키보드로 금액 입력
- 실시간 환율 적용 결과 표시

### 📊 7일/50일 추세 탭

- 통화 선택 (계산기 탭과 동일)
- 탭 클릭 시 자동 그래프 업데이트
- X축: 날짜, Y축: 환율

### 📈 고급분석 탭

- 7일 데이터 기반 이동평균선(MA7) 표시
- 파란색: 실시간 환율
- 주황색: 이동평균선

### 📉 통계 탭

- **현재 환율**: 선택한 통화의 현재 값
- **최고/최저/평균**: 7일 기준
- **변화율**: 7일 동안의 변화율(%)
- **변동성**: 높음🔥 / 중간⚡ / 낮음❄️
- **추세**: 상승📈 / 하락📉 / 보합➡️

## ⚙️ 기술 상세

### 데이터 로드

- 앱 시작 시 지난 50일 환율 데이터 로드
- ±0.3% 변동성 추가 (현실성)
- 메모리에만 저장 (DB 불필요)

### 자동 갱신

- **탭 클릭 시**: 해당 탭 데이터 즉시 업데이트
- **통화 변경 시**: 모든 탭 즉시 반영
- **날짜 변경 시**: 자정 넘으면 자동 갱신

### 지원 통화

KRW, USD, EUR, JPY, CNY, GBP, AUD, CAD, HKD, SGD, INR, MXN, CHF, SEK, NZD, BRL, RUB, TRY, ZAR, HUF + 140개 이상

## 📁 프로젝트 구조

```
currency-converter/
├── currency_converter_clean.py      # 메인 프로그램
├── README.md                         # 이 파일
├── requirements.txt                  # 의존성 목록
├── .gitignore                        # Git 무시 파일
└── currency_converter_presentation.pptx  # PPT
```

## 🔧 문제 해결

### 데이터 로드 중 메시지

첫 실행 시 정상입니다. 약 5초 대기하세요.

### 그래프가 표시 안 됨

1. 데이터 로드 완료 대기
2. 탭 다시 클릭
3. "그래프 갱신" 버튼 클릭

### API 오류

- 인터넷 연결 확인
- open.er-api.com 사이트 접속 확인

## 🔄 API 정보

- **URL**: https://open.er-api.com/v6/latest/{currency}
- **인증**: 불필요 (API 키 불필요)
- **통화**: 160+ 지원

## 📝 라이센스

MIT License

## 🤝 기여

버그 리포트나 기능 요청은 Issues에 등록해주세요.

---

**행운을 빕니다!** 🚀✨
