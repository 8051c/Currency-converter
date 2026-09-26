import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json
from datetime import datetime
from collections import deque
import threading

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("환율 계산기")
        self.root.geometry("600x900")
        self.root.resizable(False, False)
        
        # 환율 데이터 저장
        self.exchange_rates = {}
        self.last_update = None
        self.history = deque(maxlen=10)  # 최근 10개 거래
        
        # 기본 통화
        self.currencies = ['KRW', 'USD', 'EUR', 'JPY', 'CNY', 'GBP', 'AUD', 'CAD']
        
        # UI 구성
        self.create_ui()
        
        # 환율 정보 로드
        self.load_exchange_rates()
    
    def create_ui(self):
        """UI 구성"""
        # 제목
        title_label = tk.Label(
            self.root,
            text="💱 환율 계산기",
            font=("Arial", 20, "bold"),
            fg="#2a78d6"
        )
        title_label.pack(pady=10)
        
        # --- 입력 영역 ---
        input_frame = tk.Frame(self.root)
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
        
        tk.Label(input_frame, text="도착지", font=("Arial", 11, "bold")).grid(row=1, column=2, sticky="w")
        self.to_var = tk.StringVar(value="KRW")
        to_combo = ttk.Combobox(input_frame, textvariable=self.to_var, values=self.currencies, state="readonly", width=15)
        to_combo.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)
        
        # --- 환율 정보 ---
        rate_frame = tk.LabelFrame(self.root, text="실시간 환율 (한국은행 기준)", font=("Arial", 11, "bold"), padx=10, pady=10)
        rate_frame.pack(padx=15, pady=10, fill="x")
        
        self.rate_label = tk.Label(rate_frame, text="환율 로딩 중...", font=("Arial", 14, "bold"), fg="#0ca30c")
        self.rate_label.pack()
        
        self.update_label = tk.Label(rate_frame, text="마지막 업데이트: -", font=("Arial", 9), fg="#999999")
        self.update_label.pack()
        
        # --- 계산 결과 ---
        result_frame = tk.LabelFrame(self.root, text="변환 결과", font=("Arial", 11, "bold"), padx=10, pady=10)
        result_frame.pack(padx=15, pady=10, fill="x")
        
        self.result_label = tk.Label(result_frame, text="0 KRW", font=("Arial", 20, "bold"), fg="#2a78d6")
        self.result_label.pack()
        
        # --- 계산 버튼 ---
        button_frame = tk.Frame(self.root)
        button_frame.pack(padx=15, pady=10, fill="x")
        
        tk.Button(button_frame, text="변환하기", font=("Arial", 12, "bold"), bg="#2a78d6", fg="white", 
                 command=self.convert_currency, padx=20, pady=8).pack(side="left", padx=5)
        
        tk.Button(button_frame, text="환율 새로고침", font=("Arial", 10), bg="#f0f0f0", 
                 command=self.load_exchange_rates, padx=15, pady=5).pack(side="left", padx=5)
        
        # --- 온스크린 자판 ---
        keyboard_frame = tk.LabelFrame(self.root, text="계산기 자판", font=("Arial", 11, "bold"), padx=10, pady=10)
        keyboard_frame.pack(padx=15, pady=10, fill="x")
        
        # 숫자 버튼
        buttons = [
            ['7', '8', '9', '÷'],
            ['4', '5', '6', '×'],
            ['1', '2', '3', '−'],
            ['0', '.', '+', '+'],
        ]
        
        for row in buttons:
            row_frame = tk.Frame(keyboard_frame)
            row_frame.pack(fill="x", pady=3)
            for btn_text in row:
                if btn_text in ['÷', '×', '−', '+']:
                    btn = tk.Button(row_frame, text=btn_text, font=("Arial", 12, "bold"), bg="#f0ad4e", fg="white", 
                                   command=lambda t=btn_text: self.add_to_input(t), width=6, pady=5)
                else:
                    btn = tk.Button(row_frame, text=btn_text, font=("Arial", 12), bg="#f5f5f5", 
                                   command=lambda t=btn_text: self.add_to_input(t), width=6, pady=5)
                btn.pack(side="left", padx=3)
        
        # 삭제 버튼
        footer_frame = tk.Frame(keyboard_frame)
        footer_frame.pack(fill="x", pady=3)
        tk.Button(footer_frame, text="AC", font=("Arial", 11, "bold"), bg="#d9534f", fg="white", 
                 command=self.clear_input, width=14, pady=5).pack(side="left", padx=3)
        tk.Button(footer_frame, text="← 삭제", font=("Arial", 11, "bold"), bg="#5cb85c", fg="white", 
                 command=self.delete_char, width=14, pady=5).pack(side="left", padx=3)
        
        # --- 최근 거래 ---
        history_frame = tk.LabelFrame(self.root, text="최근 거래", font=("Arial", 11, "bold"), padx=10, pady=10)
        history_frame.pack(padx=15, pady=10, fill="both", expand=True)
        
        self.history_text = scrolledtext.ScrolledText(history_frame, height=6, font=("Arial", 9), state="disabled")
        self.history_text.pack(fill="both", expand=True)
    
    def load_exchange_rates(self):
        """환율 정보 로드 (별도 스레드에서 실행)"""
        def fetch_rates():
            try:
                # api.exchangerate.host 사용 (무료, 제한 없음)
                response = requests.get('https://api.exchangerate.host/latest?base=USD', timeout=5)
                data = response.json()
                
                if data.get('success', False) or 'rates' in data:
                    self.exchange_rates = data.get('rates', {})
                    self.last_update = datetime.now()
                    
                    # UI 업데이트
                    from_curr = self.from_var.get()
                    to_curr = self.to_var.get()
                    
                    # 환율 계산 (USD 기준)
                    if from_curr == 'USD':
                        rate = self.exchange_rates.get(to_curr, 1)
                    else:
                        from_to_usd = self.exchange_rates.get(from_curr, 1)
                        to_rate = self.exchange_rates.get(to_curr, 1)
                        rate = to_rate / from_to_usd if from_to_usd != 0 else 1
                    
                    # UI 업데이트
                    self.root.after(0, self.update_rate_label, from_curr, to_curr, rate)
            except Exception as e:
                print(f"환율 로드 실패: {e}")
                self.root.after(0, lambda: messagebox.showerror("오류", f"환율 로드 실패: {e}"))
        
        # 별도 스레드에서 실행
        thread = threading.Thread(target=fetch_rates, daemon=True)
        thread.start()
    
    def update_rate_label(self, from_curr, to_curr, rate):
        """환율 라벨 업데이트"""
        self.rate_label.config(text=f"1 {from_curr} = {rate:,.2f} {to_curr}")
        if self.last_update:
            self.update_label.config(text=f"마지막 업데이트: {self.last_update.strftime('%H:%M:%S')}")
        
        # 자동으로 변환
        self.convert_currency()
    
    def convert_currency(self):
        """환율 변환"""
        try:
            amount = float(self.amount_var.get())
            from_curr = self.from_var.get()
            to_curr = self.to_var.get()
            
            if not self.exchange_rates:
                messagebox.showwarning("경고", "환율 정보를 먼저 로드하세요.")
                return
            
            # 환율 계산 (USD 기준)
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
            self.update_history_display()
            
        except ValueError:
            messagebox.showerror("오류", "올바른 금액을 입력하세요.")
    
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
        """거래 기록 업데이트"""
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", tk.END)
        
        for idx, item in enumerate(self.history, 1):
            self.history_text.insert(tk.END, f"{idx}. {item}\n")
        
        self.history_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()
