import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json
import sqlite3
from datetime import datetime, timedelta
from collections import deque
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("환율 계산기 - Pro")
        self.root.geometry("750x950")
        self.root.resizable(False, False)
        
        # 데이터베이스 초기화
        self.init_database()
        
        # 환율 데이터 저장
        self.exchange_rates = {}
        self.exchange_rates_history = {}  # 시계열 데이터
        self.last_update = None
        self.history = deque(maxlen=10)
        
        # 기본 통화
        self.currencies = ['KRW', 'USD', 'EUR', 'JPY', 'CNY', 'GBP', 'AUD', 'CAD', 'HKD', 'SGD']
        
        # API 키 로드
        self.bok_api_key = self.load_api_key()
        
        # UI 구성
        self.create_ui()
        
        # 환율 정보 로드
        self.load_exchange_rates()
        self.load_history_from_db()
    
    def init_database(self):
        """SQLite 데이터베이스 초기화"""
        self.db_path = "currency_converter.db"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 거래 기록 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                from_currency TEXT NOT NULL,
                to_currency TEXT NOT NULL,
                result REAL NOT NULL,
                rate REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 환율 기록 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exchange_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_currency TEXT NOT NULL,
                to_currency TEXT NOT NULL,
                rate REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_api_key(self):
        """API 키 로드 (저장된 파일에서)"""
        try:
            if os.path.exists("api_config.json"):
                with open("api_config.json", "r") as f:
                    config = json.load(f)
                    return config.get("bok_api_key", "")
        except:
            pass
        return ""
    
    def save_api_key(self, api_key):
        """API 키 저장"""
        config = {"bok_api_key": api_key}
        with open("api_config.json", "w") as f:
            json.dump(config, f)
    
    def create_ui(self):
        """UI 구성 (탭 방식)"""
        # 제목
        title_label = tk.Label(
            self.root,
            text="💱 환율 계산기 Pro",
            font=("Arial", 18, "bold"),
            fg="#2a78d6"
        )
        title_label.pack(pady=10)
        
        # 탭 생성
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: 계산기
        self.calculator_tab = tk.Frame(self.notebook)
        self.notebook.add(self.calculator_tab, text="💻 계산기")
        self.create_calculator_tab()
        
        # Tab 2: 그래프
        self.graph_tab = tk.Frame(self.notebook)
        self.notebook.add(self.graph_tab, text="📊 그래프")
        self.create_graph_tab()
        
        # Tab 3: 거래 기록
        self.history_tab = tk.Frame(self.notebook)
        self.notebook.add(self.history_tab, text="📝 거래 기록")
        self.create_history_tab()
        
        # Tab 4: 설정
        self.settings_tab = tk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text="⚙️ 설정")
        self.create_settings_tab()
    
    def create_calculator_tab(self):
        """계산기 탭"""
        # 입력 영역
        input_frame = tk.Frame(self.calculator_tab)
        input_frame.pack(padx=15, pady=10, fill="x")
        
        # 금액 입력
        tk.Label(input_frame, text="금액", font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w")
        self.amount_var = tk.StringVar(value="100")
        amount_entry = tk.Entry(input_frame, textvariable=self.amount_var, font=("Arial", 14), width=20)
        amount_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky="ew")
        
        # 통화 선택
        tk.Label(input_frame, text="출발지", font=("Arial", 11, "bold")).grid(row=1, column=0, sticky="w")
        self.from_var = tk.StringVar(value="USD")
        from_combo = ttk.Combobox(input_frame, textvariable=self.from_var, values=self.currencies, state="readonly", width=15)
        from_combo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        from_combo.bind("<<ComboboxSelected>>", lambda e: self.convert_currency())
        
        tk.Label(input_frame, text="도착지", font=("Arial", 11, "bold")).grid(row=1, column=2, sticky="w")
        self.to_var = tk.StringVar(value="KRW")
        to_combo = ttk.Combobox(input_frame, textvariable=self.to_var, values=self.currencies, state="readonly", width=15)
        to_combo.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        to_combo.bind("<<ComboboxSelected>>", lambda e: self.convert_currency())
        
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)
        
        # 환율 정보
        rate_frame = tk.LabelFrame(self.calculator_tab, text="실시간 환율", font=("Arial", 11, "bold"), padx=10, pady=10)
        rate_frame.pack(padx=15, pady=10, fill="x")
        
        self.rate_label = tk.Label(rate_frame, text="환율 로딩 중...", font=("Arial", 14, "bold"), fg="#0ca30c")
        self.rate_label.pack()
        
        self.update_label = tk.Label(rate_frame, text="마지막 업데이트: -", font=("Arial", 9), fg="#999999")
        self.update_label.pack()
        
        self.api_label = tk.Label(rate_frame, text="API: exchangerate.host (무료)", font=("Arial", 8), fg="#999999")
        self.api_label.pack()
        
        # 계산 결과
        result_frame = tk.LabelFrame(self.calculator_tab, text="변환 결과", font=("Arial", 11, "bold"), padx=10, pady=10)
        result_frame.pack(padx=15, pady=10, fill="x")
        
        self.result_label = tk.Label(result_frame, text="0 KRW", font=("Arial", 20, "bold"), fg="#2a78d6")
        self.result_label.pack()
        
        # 계산 버튼
        button_frame = tk.Frame(self.calculator_tab)
        button_frame.pack(padx=15, pady=10, fill="x")
        
        tk.Button(button_frame, text="변환하기", font=("Arial", 12, "bold"), bg="#2a78d6", fg="white",
                 command=self.convert_currency, padx=20, pady=8).pack(side="left", padx=5)
        
        tk.Button(button_frame, text="환율 새로고침", font=("Arial", 10), bg="#f0f0f0",
                 command=self.load_exchange_rates, padx=15, pady=5).pack(side="left", padx=5)
        
        # 온스크린 자판
        keyboard_frame = tk.LabelFrame(self.calculator_tab, text="계산기 자판", font=("Arial", 10, "bold"), padx=10, pady=8)
        keyboard_frame.pack(padx=15, pady=10, fill="x")
        
        buttons = [
            ['7', '8', '9', '÷'],
            ['4', '5', '6', '×'],
            ['1', '2', '3', '−'],
            ['0', '.', '+', '+'],
        ]
        
        for row in buttons:
            row_frame = tk.Frame(keyboard_frame)
            row_frame.pack(fill="x", pady=2)
            for btn_text in row:
                if btn_text in ['÷', '×', '−', '+']:
                    btn = tk.Button(row_frame, text=btn_text, font=("Arial", 10, "bold"), bg="#f0ad4e", fg="white",
                                   command=lambda t=btn_text: self.add_to_input(t), width=6, pady=4)
                else:
                    btn = tk.Button(row_frame, text=btn_text, font=("Arial", 10), bg="#f5f5f5",
                                   command=lambda t=btn_text: self.add_to_input(t), width=6, pady=4)
                btn.pack(side="left", padx=2)
        
        footer_frame = tk.Frame(keyboard_frame)
        footer_frame.pack(fill="x", pady=2)
        tk.Button(footer_frame, text="AC", font=("Arial", 10, "bold"), bg="#d9534f", fg="white",
                 command=self.clear_input, width=14, pady=4).pack(side="left", padx=2)
        tk.Button(footer_frame, text="← 삭제", font=("Arial", 10, "bold"), bg="#5cb85c", fg="white",
                 command=self.delete_char, width=14, pady=4).pack(side="left", padx=2)
    
    def create_graph_tab(self):
        """그래프 탭"""
        control_frame = tk.Frame(self.graph_tab)
        control_frame.pack(padx=10, pady=10, fill="x")
        
        tk.Label(control_frame, text="통화 선택:", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        self.graph_from_var = tk.StringVar(value="USD")
        graph_from_combo = ttk.Combobox(control_frame, textvariable=self.graph_from_var, values=self.currencies[:5], state="readonly", width=10)
        graph_from_combo.pack(side="left", padx=5)
        
        tk.Label(control_frame, text="→", font=("Arial", 10)).pack(side="left", padx=5)
        
        self.graph_to_var = tk.StringVar(value="KRW")
        graph_to_combo = ttk.Combobox(control_frame, textvariable=self.graph_to_var, values=self.currencies[:5], state="readonly", width=10)
        graph_to_combo.pack(side="left", padx=5)
        
        tk.Button(control_frame, text="그래프 갱신", font=("Arial", 10), bg="#2a78d6", fg="white",
                 command=self.update_graph, padx=15, pady=5).pack(side="left", padx=5)
        
        self.graph_canvas_frame = tk.Frame(self.graph_tab)
        self.graph_canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 초기 그래프 생성
        self.update_graph()
    
    def create_history_tab(self):
        """거래 기록 탭"""
        button_frame = tk.Frame(self.history_tab)
        button_frame.pack(padx=10, pady=10, fill="x")
        
        tk.Button(button_frame, text="데이터베이스에서 로드", font=("Arial", 10), bg="#2a78d6", fg="white",
                 command=self.load_history_from_db, padx=15, pady=5).pack(side="left", padx=5)
        
        tk.Button(button_frame, text="전체 삭제", font=("Arial", 10), bg="#d9534f", fg="white",
                 command=self.clear_all_history, padx=15, pady=5).pack(side="left", padx=5)
        
        self.history_text = scrolledtext.ScrolledText(self.history_tab, height=20, font=("Arial", 9), state="disabled")
        self.history_text.pack(padx=10, pady=10, fill="both", expand=True)
    
    def create_settings_tab(self):
        """설정 탭"""
        settings_frame = tk.Frame(self.settings_tab)
        settings_frame.pack(padx=15, pady=15, fill="both", expand=True)
        
        # 환율 API 선택
        tk.Label(settings_frame, text="현재 사용 중인 API", font=("Arial", 12, "bold")).pack(anchor="w", pady=10)
        tk.Label(settings_frame, text="🔹 exchangerate.host (무료, 제한 없음)", font=("Arial", 10), fg="#0ca30c").pack(anchor="w")
        tk.Label(settings_frame, text="빠른 응답, 150+ 통화 지원", font=("Arial", 9), fg="#666666").pack(anchor="w", padx=20, pady=5)
        
        # 한국은행 API
        tk.Label(settings_frame, text="\n한국은행 기준 환율 API", font=("Arial", 12, "bold")).pack(anchor="w", pady=10)
        
        api_frame = tk.Frame(settings_frame)
        api_frame.pack(anchor="w", fill="x", pady=5)
        
        tk.Label(api_frame, text="API 키:", font=("Arial", 10)).pack(side="left", padx=5)
        self.api_key_var = tk.StringVar(value=self.bok_api_key)
        api_entry = tk.Entry(api_frame, textvariable=self.api_key_var, font=("Arial", 10), width=30, show="*")
        api_entry.pack(side="left", padx=5)
        
        tk.Button(api_frame, text="저장", font=("Arial", 10), bg="#5cb85c", fg="white",
                 command=self.save_bok_api_key, padx=10, pady=3).pack(side="left", padx=5)
        
        tk.Label(settings_frame, text="1️⃣ https://www.data.go.kr/ 접속", font=("Arial", 9), fg="#666666").pack(anchor="w", pady=3)
        tk.Label(settings_frame, text="2️⃣ '기준 환율' 검색 후 활용신청", font=("Arial", 9), fg="#666666").pack(anchor="w", pady=3)
        tk.Label(settings_frame, text="3️⃣ API 키 복사 후 위에 붙여넣기", font=("Arial", 9), fg="#666666").pack(anchor="w", pady=3)
        
        # 정보
        tk.Label(settings_frame, text="\n앱 정보", font=("Arial", 12, "bold")).pack(anchor="w", pady=10)
        tk.Label(settings_frame, text="환율 계산기 Pro v1.0", font=("Arial", 10)).pack(anchor="w", pady=3)
        tk.Label(settings_frame, text="데이터베이스: SQLite", font=("Arial", 10)).pack(anchor="w", pady=3)
        tk.Label(settings_frame, text="그래프: Matplotlib", font=("Arial", 10)).pack(anchor="w", pady=3)
        
        # .exe 변환 가이드
        tk.Label(settings_frame, text="\n.exe 변환 가이드", font=("Arial", 12, "bold")).pack(anchor="w", pady=10)
        tk.Label(settings_frame, text="1️⃣ pip install pyinstaller", font=("Arial", 9), fg="#666666").pack(anchor="w", pady=3)
        tk.Label(settings_frame, text="2️⃣ pyinstaller --onefile --windowed currency_converter_full.py", font=("Arial", 9), fg="#666666").pack(anchor="w", pady=3)
        tk.Label(settings_frame, text="3️⃣ dist/currency_converter_full.exe 사용", font=("Arial", 9), fg="#666666").pack(anchor="w", pady=3)
    
    def save_bok_api_key(self):
        """한국은행 API 키 저장"""
        api_key = self.api_key_var.get()
        if api_key:
            self.save_api_key(api_key)
            messagebox.showinfo("성공", "API 키가 저장되었습니다.")
            self.bok_api_key = api_key
        else:
            messagebox.showwarning("경고", "API 키를 입력하세요.")
    
    def load_exchange_rates(self):
        """환율 정보 로드"""
        def fetch_rates():
            try:
                response = requests.get('https://api.exchangerate.host/latest?base=USD', timeout=5)
                data = response.json()
                
                if data.get('success', False) or 'rates' in data:
                    self.exchange_rates = data.get('rates', {})
                    self.last_update = datetime.now()
                    
                    # 환율 기록 저장
                    self.save_exchange_rates_to_db()
                    
                    # UI 업데이트
                    from_curr = self.from_var.get()
                    to_curr = self.to_var.get()
                    
                    if from_curr == 'USD':
                        rate = self.exchange_rates.get(to_curr, 1)
                    else:
                        from_to_usd = self.exchange_rates.get(from_curr, 1)
                        to_rate = self.exchange_rates.get(to_curr, 1)
                        rate = to_rate / from_to_usd if from_to_usd != 0 else 1
                    
                    self.root.after(0, self.update_rate_label, from_curr, to_curr, rate)
            except Exception as e:
                print(f"환율 로드 실패: {e}")
        
        thread = threading.Thread(target=fetch_rates, daemon=True)
        thread.start()
    
    def save_exchange_rates_to_db(self):
        """환율 데이터 데이터베이스에 저장"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for to_curr, rate in self.exchange_rates.items():
            cursor.execute('''
                INSERT INTO exchange_rates (from_currency, to_currency, rate)
                VALUES (?, ?, ?)
            ''', ('USD', to_curr, rate))
        
        conn.commit()
        conn.close()
    
    def update_rate_label(self, from_curr, to_curr, rate):
        """환율 라벨 업데이트"""
        self.rate_label.config(text=f"1 {from_curr} = {rate:,.2f} {to_curr}")
        if self.last_update:
            self.update_label.config(text=f"마지막 업데이트: {self.last_update.strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.convert_currency()
    
    def convert_currency(self):
        """환율 변환"""
        try:
            amount_str = self.amount_var.get()
            if not amount_str:
                return
            
            # 계산식이 있으면 계산
            try:
                amount = eval(amount_str)
            except:
                amount = float(amount_str)
            
            from_curr = self.from_var.get()
            to_curr = self.to_var.get()
            
            if not self.exchange_rates:
                return
            
            # 환율 계산
            if from_curr == 'USD':
                rate = self.exchange_rates.get(to_curr, 1)
            else:
                from_to_usd = self.exchange_rates.get(from_curr, 1)
                to_rate = self.exchange_rates.get(to_curr, 1)
                rate = to_rate / from_to_usd if from_to_usd != 0 else 1
            
            result = amount * rate
            
            # 결과 표시
            self.result_label.config(text=f"{result:,.2f} {to_curr}")
            
            # 거래 기록 저장
            history_item = f"{amount:,.0f} {from_curr} → {result:,.2f} {to_curr} ({datetime.now().strftime('%H:%M')})"
            self.history.appendleft(history_item)
            
            # 데이터베이스에 저장
            self.save_transaction_to_db(amount, from_curr, to_curr, result, rate)
            self.update_history_display()
            
        except ValueError:
            pass
    
    def save_transaction_to_db(self, amount, from_curr, to_curr, result, rate):
        """거래 기록 데이터베이스 저장"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO transactions (amount, from_currency, to_currency, result, rate)
            VALUES (?, ?, ?, ?, ?)
        ''', (amount, from_curr, to_curr, result, rate))
        
        conn.commit()
        conn.close()
    
    def load_history_from_db(self):
        """데이터베이스에서 거래 기록 로드"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM transactions ORDER BY timestamp DESC LIMIT 100')
        transactions = cursor.fetchall()
        conn.close()
        
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", tk.END)
        
        for idx, trans in enumerate(transactions, 1):
            id, amount, from_curr, to_curr, result, rate, timestamp = trans
            text = f"{idx}. {amount:,.0f} {from_curr} → {result:,.2f} {to_curr} (환율: {rate:,.4f}) | {timestamp}\n"
            self.history_text.insert(tk.END, text)
        
        self.history_text.config(state="disabled")
    
    def clear_all_history(self):
        """전체 거래 기록 삭제"""
        if messagebox.askyesno("확인", "전체 거래 기록을 삭제하시겠습니까?"):
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM transactions')
            conn.commit()
            conn.close()
            
            self.load_history_from_db()
            messagebox.showinfo("완료", "거래 기록이 삭제되었습니다.")
    
    def update_graph(self):
        """그래프 업데이트 (최근 7일)"""
        from_curr = self.graph_from_var.get()
        to_curr = self.graph_to_var.get()
        
        # 데이터베이스에서 최근 7일 환율 조회
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DATE(timestamp), AVG(rate) 
            FROM exchange_rates 
            WHERE from_currency = ? AND to_currency = ?
            AND timestamp >= datetime('now', '-7 days')
            GROUP BY DATE(timestamp)
            ORDER BY timestamp
        ''', (from_curr, to_curr))
        
        results = cursor.fetchall()
        conn.close()
        
        # 그래프 생성
        if results:
            dates = [r[0][-5:] for r in results]  # MM-DD
            rates = [r[1] for r in results]
        else:
            # 데이터가 없으면 현재 환율로 표시
            dates = ['오늘']
            if from_curr == 'USD':
                rate = self.exchange_rates.get(to_curr, 1)
            else:
                from_to_usd = self.exchange_rates.get(from_curr, 1)
                to_rate = self.exchange_rates.get(to_curr, 1)
                rate = to_rate / from_to_usd if from_to_usd != 0 else 1
            rates = [rate]
        
        # 이전 캔버스 제거
        for widget in self.graph_canvas_frame.winfo_children():
            widget.destroy()
        
        # 새 그래프 생성
        fig = Figure(figsize=(7, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        ax.plot(dates, rates, marker='o', linewidth=2, markersize=6, color='#2a78d6')
        ax.fill_between(range(len(dates)), rates, alpha=0.3, color='#2a78d6')
        ax.set_title(f"{from_curr} → {to_curr} 최근 환율 변동", fontsize=12, fontweight='bold')
        ax.set_xlabel("날짜", fontsize=10)
        ax.set_ylabel("환율", fontsize=10)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.graph_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def add_to_input(self, char):
        """자판 입력"""
        if char == '÷':
            char = '/'
        elif char == '×':
            char = '*'
        elif char == '−':
            char = '-'
        
        current = self.amount_var.get()
        self.amount_var.set(current + char)
    
    def clear_input(self):
        """입력 초기화"""
        self.amount_var.set("")
    
    def delete_char(self):
        """마지막 문자 삭제"""
        current = self.amount_var.get()
        self.amount_var.set(current[:-1])
    
    def update_history_display(self):
        """거래 기록 업데이트 (메모리)"""
        # 계산기 탭에서 사용하지 않음
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()
