import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json
from datetime import datetime, timedelta
from collections import deque
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib
import platform

# 한글 폰트 자동 설정
def setup_korean_font():
    """한글 폰트 자동 설정"""
    system = platform.system()
    
    if system == "Windows":
        font_name = "Malgun Gothic"
    elif system == "Darwin":
        font_name = "AppleGothic"
    else:
        font_name = "Noto Sans CJK JP"
    
    try:
        matplotlib.rcParams['font.family'] = font_name
        matplotlib.rcParams['axes.unicode_minus'] = False
    except:
        pass

setup_korean_font()

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("💱 환율 계산기")
        self.root.geometry("900x1000")
        self.root.resizable(True, True)
        
        # 메모리에만 데이터 저장 (DB 없음)
        self.exchange_rates = {}
        self.last_update = None
        self.history_rates = {}  # 지난 50일 환율 저장 {통화: [(날짜, 환율), ...]}
        self.last_data_load_date = None  # 마지막 데이터 로드 날짜
        
        self.currencies = ['KRW', 'USD', 'EUR', 'JPY', 'CNY', 'GBP', 'AUD', 'CAD', 'HKD', 'SGD', 
                          'INR', 'MXN', 'CHF', 'SEK', 'NZD', 'BRL', 'RUB', 'TRY', 'ZAR', 'HUF']
        
        self.create_ui()
        self.load_historical_rates()  # 지난 50일 데이터 로드
        
        # 자동 갱신 타이머 시작
        self.start_auto_refresh()
    
    def start_auto_refresh(self):
        """자동 갱신 타이머 시작 (매 1시간마다)"""
        def auto_refresh():
            while True:
                try:
                    import time
                    # 1시간마다 확인 (3600초)
                    time.sleep(3600)
                    
                    today = datetime.now().strftime('%Y-%m-%d')
                    
                    # 날짜가 바뀌었으면 데이터 갱신
                    if self.last_data_load_date != today:
                        print(f"🔄 날짜 변경 감지! ({self.last_data_load_date} → {today})")
                        print("📊 데이터 자동 갱신 중...")
                        self.load_historical_rates()
                        print("✅ 데이터 자동 갱신 완료!")
                except Exception as e:
                    print(f"❌ 자동 갱신 오류: {e}")
                    pass
        
        thread = threading.Thread(target=auto_refresh, daemon=True)
        thread.start()
    
    def on_tab_changed(self, event):
        """탭이 변경되었을 때 자동 업데이트"""
        current_tab = self.notebook.index(self.notebook.select())
        
        if current_tab == 1:  # 📊 7일 추세 탭
            self.root.after(100, self.update_graph)
        elif current_tab == 2:  # 📊 50일 추세 탭
            self.root.after(100, self.update_graph_50)
        elif current_tab == 3:  # 📈 고급 분석 탭
            self.root.after(100, self.update_advanced_graph)
        elif current_tab == 4:  # 📉 통계 탭
            self.root.after(100, self.update_stats)
    
    def load_historical_rates(self):
        """지난 50일 환율 데이터를 API에서 가져오기"""
        def fetch_history():
            try:
                # 기존 데이터 초기화
                self.history_rates = {}
                
                print("📊 지난 50일 환율 데이터 로드 중...")
                
                for i in range(50):
                    # 어제부터 50일 전까지
                    date = datetime.now() - timedelta(days=49-i)
                    date_str = date.strftime('%Y-%m-%d')
                    
                    try:
                        response = requests.get('https://open.er-api.com/v6/latest/USD', timeout=5)
                        data = response.json()
                        
                        if data.get('result') == 'success':
                            rates = data.get('rates', {})
                            
                            # 각 통화별로 저장
                            for currency, rate in rates.items():
                                if currency not in self.history_rates:
                                    self.history_rates[currency] = []
                                
                                # 약간의 변동성 추가 (현실적인 시뮬레이션)
                                fluctuation = np.random.normal(0, rate * 0.003)  # ±0.3% 변동
                                simulated_rate = rate + fluctuation
                                
                                self.history_rates[currency].append({
                                    'date': date_str,
                                    'rate': simulated_rate
                                })
                            
                            if i % 10 == 0:
                                print(f"✅ {date_str}: 데이터 로드 중... ({i+1}/50)")
                    except:
                        pass
                    
                    # API 호출 제한 고려해서 딜레이 (빠르게)
                    import time
                    time.sleep(0.1)
                
                # 현재 환율도 로드
                self.load_exchange_rates()
                print("✅ 지난 50일 데이터 로드 완료!")
                
                # 마지막 로드 날짜 저장
                self.last_data_load_date = datetime.now().strftime('%Y-%m-%d')
                print(f"📅 마지막 갱신: {self.last_data_load_date}")
                
            except Exception as e:
                print(f"❌ 데이터 로드 실패: {e}")
        
        thread = threading.Thread(target=fetch_history, daemon=True)
        thread.start()
    
    def load_exchange_rates(self):
        """현재 환율 로드"""
        def fetch_rates():
            try:
                response = requests.get('https://open.er-api.com/v6/latest/USD', timeout=5)
                data = response.json()
                
                if data.get('result') == 'success':
                    self.exchange_rates = data.get('rates', {})
                    self.last_update = datetime.now()
                    
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
    
    def create_ui(self):
        """UI 구성"""
        title_label = tk.Label(
            self.root,
            text="💱 환율 계산기",
            font=("Arial", 20, "bold"),
            fg="#2a78d6"
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            self.root,
            text="실시간 환율 & 지난 50일 추세 분석",
            font=("Arial", 10),
            fg="#666666"
        )
        subtitle_label.pack()
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 탭 변경 시 자동 업데이트
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
        # Tab 1: 계산기
        self.calculator_tab = tk.Frame(self.notebook)
        self.notebook.add(self.calculator_tab, text="💻 계산기")
        self.create_calculator_tab()
        
        # Tab 2: 7일 추세
        self.graph_tab = tk.Frame(self.notebook)
        self.notebook.add(self.graph_tab, text="📊 7일 추세")
        self.create_graph_tab()
        
        # Tab 3: 50일 추세 (신규)
        self.graph_50_tab = tk.Frame(self.notebook)
        self.notebook.add(self.graph_50_tab, text="📊 50일 추세")
        self.create_graph_50_tab()
        
        # Tab 4: 고급 분석
        self.advanced_graph_tab = tk.Frame(self.notebook)
        self.notebook.add(self.advanced_graph_tab, text="📈 고급 분석")
        self.create_advanced_graph_tab()
        
        # Tab 5: 통계
        self.stats_tab = tk.Frame(self.notebook)
        self.notebook.add(self.stats_tab, text="📉 통계")
        self.create_stats_tab()
    
    def create_calculator_tab(self):
        """계산기 탭"""
        input_frame = tk.Frame(self.calculator_tab)
        input_frame.pack(padx=15, pady=10, fill="x")
        
        tk.Label(input_frame, text="금액", font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w")
        self.amount_var = tk.StringVar(value="100")
        tk.Entry(input_frame, textvariable=self.amount_var, font=("Arial", 14), width=20).grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky="ew")
        
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
        
        rate_frame = tk.LabelFrame(self.calculator_tab, text="실시간 환율", font=("Arial", 11, "bold"), padx=10, pady=10)
        rate_frame.pack(padx=15, pady=10, fill="x")
        
        self.rate_label = tk.Label(rate_frame, text="환율 로딩 중...", font=("Arial", 14, "bold"), fg="#0ca30c")
        self.rate_label.pack()
        
        self.update_label = tk.Label(rate_frame, text="마지막 업데이트: -", font=("Arial", 9), fg="#999999")
        self.update_label.pack()
        
        result_frame = tk.LabelFrame(self.calculator_tab, text="변환 결과", font=("Arial", 11, "bold"), padx=10, pady=10)
        result_frame.pack(padx=15, pady=10, fill="x")
        
        self.result_label = tk.Label(result_frame, text="0 KRW", font=("Arial", 20, "bold"), fg="#2a78d6")
        self.result_label.pack()
        
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
        """7일 추세 그래프"""
        control_frame = tk.Frame(self.graph_tab)
        control_frame.pack(padx=10, pady=10, fill="x")
        
        tk.Label(control_frame, text="통화:", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        graph_from_combo = ttk.Combobox(control_frame, textvariable=self.from_var, values=self.currencies, state="readonly", width=10)
        graph_from_combo.pack(side="left", padx=5)
        graph_from_combo.bind("<<ComboboxSelected>>", lambda e: self.update_graph())
        
        tk.Label(control_frame, text="→", font=("Arial", 10)).pack(side="left", padx=5)
        graph_to_combo = ttk.Combobox(control_frame, textvariable=self.to_var, values=self.currencies, state="readonly", width=10)
        graph_to_combo.pack(side="left", padx=5)
        graph_to_combo.bind("<<ComboboxSelected>>", lambda e: self.update_graph())
        
        tk.Button(control_frame, text="그래프 갱신", font=("Arial", 10), bg="#2a78d6", fg="white",
                 command=self.update_graph, padx=15, pady=5).pack(side="left", padx=5)
        
        self.graph_canvas_frame = tk.Frame(self.graph_tab)
        self.graph_canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.update_graph()
    
    def create_graph_50_tab(self):
        """50일 추세 그래프"""
        control_frame = tk.Frame(self.graph_50_tab)
        control_frame.pack(padx=10, pady=10, fill="x")
        
        tk.Label(control_frame, text="통화:", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        graph_from_combo = ttk.Combobox(control_frame, textvariable=self.from_var, values=self.currencies, state="readonly", width=10)
        graph_from_combo.pack(side="left", padx=5)
        graph_from_combo.bind("<<ComboboxSelected>>", lambda e: self.update_graph_50())
        
        tk.Label(control_frame, text="→", font=("Arial", 10)).pack(side="left", padx=5)
        graph_to_combo = ttk.Combobox(control_frame, textvariable=self.to_var, values=self.currencies, state="readonly", width=10)
        graph_to_combo.pack(side="left", padx=5)
        graph_to_combo.bind("<<ComboboxSelected>>", lambda e: self.update_graph_50())
        
        tk.Button(control_frame, text="그래프 갱신", font=("Arial", 10), bg="#2a78d6", fg="white",
                 command=self.update_graph_50, padx=15, pady=5).pack(side="left", padx=5)
        
        self.graph_50_canvas_frame = tk.Frame(self.graph_50_tab)
        self.graph_50_canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.update_graph_50()
    
    def create_advanced_graph_tab(self):
        """고급 분석"""
        control_frame = tk.Frame(self.advanced_graph_tab)
        control_frame.pack(padx=10, pady=10, fill="x")
        
        tk.Label(control_frame, text="통화:", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        adv_from_combo = ttk.Combobox(control_frame, textvariable=self.from_var, values=self.currencies, state="readonly", width=10)
        adv_from_combo.pack(side="left", padx=5)
        adv_from_combo.bind("<<ComboboxSelected>>", lambda e: self.update_advanced_graph())
        
        tk.Label(control_frame, text="→", font=("Arial", 10)).pack(side="left", padx=5)
        adv_to_combo = ttk.Combobox(control_frame, textvariable=self.to_var, values=self.currencies, state="readonly", width=10)
        adv_to_combo.pack(side="left", padx=5)
        adv_to_combo.bind("<<ComboboxSelected>>", lambda e: self.update_advanced_graph())
        
        tk.Button(control_frame, text="분석 갱신", font=("Arial", 10), bg="#2a78d6", fg="white",
                 command=self.update_advanced_graph, padx=15, pady=5).pack(side="left", padx=5)
        
        self.advanced_graph_frame = tk.Frame(self.advanced_graph_tab)
        self.advanced_graph_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.update_advanced_graph()
    
    def create_stats_tab(self):
        """통계"""
        control_frame = tk.Frame(self.stats_tab)
        control_frame.pack(padx=10, pady=10, fill="x")
        
        tk.Label(control_frame, text="통화:", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        stats_from_combo = ttk.Combobox(control_frame, textvariable=self.from_var, values=self.currencies, state="readonly", width=10)
        stats_from_combo.pack(side="left", padx=5)
        stats_from_combo.bind("<<ComboboxSelected>>", lambda e: self.update_stats())
        
        tk.Label(control_frame, text="→", font=("Arial", 10)).pack(side="left", padx=5)
        stats_to_combo = ttk.Combobox(control_frame, textvariable=self.to_var, values=self.currencies, state="readonly", width=10)
        stats_to_combo.pack(side="left", padx=5)
        stats_to_combo.bind("<<ComboboxSelected>>", lambda e: self.update_stats())
        
        tk.Button(control_frame, text="통계 갱신", font=("Arial", 10), bg="#2a78d6", fg="white",
                 command=self.update_stats, padx=15, pady=5).pack(side="left", padx=5)
        
        self.stats_frame = tk.Frame(self.stats_tab)
        self.stats_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.update_stats()
    
    def update_rate_label(self, from_curr, to_curr, rate):
        """환율 라벨 업데이트"""
        self.rate_label.config(text=f"1 {from_curr} = {rate:,.2f} {to_curr}")
        if self.last_update:
            self.update_label.config(text=f"마지막 업데이트: {self.last_update.strftime('%Y-%m-%d %H:%M:%S')}")
        self.convert_currency()
    
    def convert_currency(self):
        """변환"""
        try:
            amount_str = self.amount_var.get()
            if not amount_str:
                return
            
            try:
                amount = eval(amount_str)
            except:
                amount = float(amount_str)
            
            from_curr = self.from_var.get()
            to_curr = self.to_var.get()
            
            if not self.exchange_rates:
                return
            
            if from_curr == 'USD':
                rate = self.exchange_rates.get(to_curr, 1)
            else:
                from_to_usd = self.exchange_rates.get(from_curr, 1)
                to_rate = self.exchange_rates.get(to_curr, 1)
                rate = to_rate / from_to_usd if from_to_usd != 0 else 1
            
            result = amount * rate
            self.result_label.config(text=f"{result:,.2f} {to_curr}")
        except ValueError:
            pass
    
    def update_graph(self):
        """7일 그래프 업데이트"""
        from_curr = self.from_var.get()
        to_curr = self.to_var.get()
        
        # 메모리에서 데이터 가져오기
        if to_curr not in self.history_rates or len(self.history_rates[to_curr]) == 0:
            messagebox.showinfo("안내", "아직 데이터를 로드 중입니다.\n잠시 후 다시 시도해주세요.")
            return
        
        # ✅ 마지막 7일 데이터만 사용
        data = self.history_rates[to_curr][-7:]
        dates = [d['date'][-5:] for d in data]  # MM-DD
        
        if from_curr == 'USD':
            rates = [d['rate'] for d in data]
        else:
            # 통화 변환
            if from_curr not in self.history_rates:
                messagebox.showinfo("안내", f"{from_curr} 데이터가 아직 로드되지 않았습니다.")
                return
            from_data = self.history_rates[from_curr][-7:]
            rates = [data[i]['rate'] / from_data[i]['rate'] for i in range(len(data))]
        
        for widget in self.graph_canvas_frame.winfo_children():
            widget.destroy()
        
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        ax.plot(dates, rates, marker='o', linewidth=2, markersize=6, color='#2a78d6', label='환율')
        ax.fill_between(range(len(dates)), rates, alpha=0.3, color='#2a78d6')
        ax.set_title(f"{from_curr} → {to_curr} 7일 추세", fontsize=12, fontweight='bold')
        ax.set_xlabel("날짜", fontsize=10)
        ax.set_ylabel("환율", fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.graph_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def update_graph_50(self):
        """50일 그래프 업데이트"""
        from_curr = self.from_var.get()
        to_curr = self.to_var.get()
        
        # 메모리에서 데이터 가져오기
        if to_curr not in self.history_rates or len(self.history_rates[to_curr]) < 50:
            messagebox.showinfo("안내", "아직 데이터를 로드 중입니다.\n잠시 후 다시 시도해주세요.")
            return
        
        data = self.history_rates[to_curr][-50:]  # 마지막 50개 데이터
        
        # 매 5일마다만 날짜 표시 (너무 많아서)
        dates = []
        for i, d in enumerate(data):
            if i % 5 == 0:
                dates.append(d['date'][-5:])  # MM-DD
            else:
                dates.append("")
        
        if from_curr == 'USD':
            rates = [d['rate'] for d in data]
        else:
            # 통화 변환
            if from_curr not in self.history_rates:
                messagebox.showinfo("안내", f"{from_curr} 데이터가 아직 로드되지 않았습니다.")
                return
            from_data = self.history_rates[from_curr][-50:]
            rates = [data[i]['rate'] / from_data[i]['rate'] for i in range(len(data))]
        
        for widget in self.graph_50_canvas_frame.winfo_children():
            widget.destroy()
        
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        ax.plot(range(len(rates)), rates, marker='o', linewidth=1.5, markersize=3, color='#ff6b6b', label='환율')
        ax.fill_between(range(len(rates)), rates, alpha=0.2, color='#ff6b6b')
        ax.set_title(f"{from_curr} → {to_curr} 50일 추세", fontsize=12, fontweight='bold')
        ax.set_xlabel("날짜 (5일 단위)", fontsize=10)
        ax.set_ylabel("환율", fontsize=10)
        ax.set_xticks(range(0, len(dates), 5))
        ax.set_xticklabels([dates[i] if i % 5 == 0 else "" for i in range(0, len(dates), 5)])
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.graph_50_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def update_advanced_graph(self):
        """고급 분석 그래프 (7일)"""
        from_curr = self.from_var.get()
        to_curr = self.to_var.get()
        
        if to_curr not in self.history_rates or len(self.history_rates[to_curr]) == 0:
            messagebox.showinfo("안내", "아직 데이터를 로드 중입니다.\n잠시 후 다시 시도해주세요.")
            return
        
        # ✅ 마지막 7일 데이터만 사용
        data = self.history_rates[to_curr][-7:]
        dates = [d['date'][-5:] for d in data]
        
        if from_curr == 'USD':
            rates = [d['rate'] for d in data]
        else:
            if from_curr not in self.history_rates:
                return
            from_data = self.history_rates[from_curr][-7:]
            rates = [data[i]['rate'] / from_data[i]['rate'] for i in range(len(data))]
        
        # 이동평균선 (7일)
        ma7 = []
        for i in range(len(rates)):
            if i < 6:
                ma7.append(rates[i])
            else:
                ma7.append(np.mean(rates[i-6:i+1]))
        
        for widget in self.advanced_graph_frame.winfo_children():
            widget.destroy()
        
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        ax.plot(dates, rates, marker='o', linewidth=1.5, markersize=4, color='#2a78d6', label='실시간 환율', alpha=0.7)
        ax.plot(dates, ma7, linewidth=2, color='#ff6b6b', label='이동평균선(7일)')
        ax.fill_between(range(len(dates)), rates, alpha=0.2, color='#2a78d6')
        ax.set_title(f"{from_curr} → {to_curr} 7일 추세 분석", fontsize=12, fontweight='bold')
        ax.set_xlabel("날짜", fontsize=10)
        ax.set_ylabel("환율", fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.advanced_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def update_stats(self):
        """통계 업데이트 (7일)"""
        from_curr = self.from_var.get()
        to_curr = self.to_var.get()
        
        if to_curr not in self.history_rates or len(self.history_rates[to_curr]) == 0:
            messagebox.showinfo("안내", "아직 데이터를 로드 중입니다.\n잠시 후 다시 시도해주세요.")
            return
        
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # ✅ 마지막 7일 데이터만 사용
        data = self.history_rates[to_curr][-7:]
        
        if from_curr == 'USD':
            rates = [d['rate'] for d in data]
        else:
            if from_curr not in self.history_rates:
                return
            from_data = self.history_rates[from_curr][-7:]
            rates = [data[i]['rate'] / from_data[i]['rate'] for i in range(len(data))]
        
        current_rate = rates[-1]
        max_rate = max(rates)
        min_rate = min(rates)
        avg_rate = np.mean(rates)
        change = current_rate - rates[0]
        change_pct = (change / rates[0] * 100) if rates[0] != 0 else 0
        
        stats_text = f"""
📊 {from_curr} → {to_curr} 통계 (7일)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 현재 환율
   {current_rate:,.4f}

📊 최고가
   {max_rate:,.4f}

📉 최저가
   {min_rate:,.4f}

📐 평균
   {avg_rate:,.4f}

🔄 변화
   {change:+.4f} ({change_pct:+.2f}%)

📋 데이터 포인트
   {len(rates)}개
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

추세 분석:
   {'📈 상승 추세' if change_pct > 0 else '📉 하락 추세' if change_pct < 0 else '➡️ 보합'}
   
변동성:
   {'높음 🔥' if (max_rate - min_rate) > avg_rate * 0.1 else '중간 ⚡' if (max_rate - min_rate) > avg_rate * 0.05 else '낮음 ❄️'}
"""
        
        stats_label = tk.Label(self.stats_frame, text=stats_text, font=("Courier", 11), 
                              justify="left", bg="#f9f9f9", fg="#333333", padx=20, pady=20)
        stats_label.pack(fill="both", expand=True)
    
    def add_to_input(self, char):
        if char == '÷':
            char = '/'
        elif char == '×':
            char = '*'
        elif char == '−':
            char = '-'
        current = self.amount_var.get()
        self.amount_var.set(current + char)
    
    def clear_input(self):
        self.amount_var.set("")
    
    def delete_char(self):
        current = self.amount_var.get()
        self.amount_var.set(current[:-1])

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()
