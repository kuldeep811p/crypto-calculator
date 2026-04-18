import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, getcontext
import json
from urllib.request import urlopen
import threading

# Set high precision for Bitcoin calculations
getcontext().prec = 50

class BitcoinCalculatorGUI:
    def __init__(self):
        self.SATOSHI_PER_BTC = Decimal('100000000')
        
        # Create main window
        self.window = tk.Tk()
        self.window.title("Bitcoin Calculator - 100% Accurate")
        self.window.geometry("500x600")  # Changed from 600x700 to 500x600
        self.window.configure(bg='#1a1a2e')
        
        # Set icon (optional - remove if error)
        try:
            self.window.iconbitmap(default='bitcoin.ico')
        except:
            pass
        
        # Make window resizable (changed from False to True)
        self.window.resizable(True, True)
        
        # Set minimum window size to prevent it from becoming too small
        self.window.minsize(450, 550)
        
        # Center the window on screen
        self.center_window()
        
        # Create GUI elements
        self.create_widgets()
        
        # Start live price update thread
        self.update_live_price()
        
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        width = 500  # Changed from 600 to 500
        height = 600  # Changed from 700 to 600
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create all GUI elements"""
        
        # Title Frame
        title_frame = tk.Frame(self.window, bg='#1a1a2e')
        title_frame.pack(pady=(15, 10)) # Reduced padding from (20, 10) to (15, 10)
        
        title_label = tk.Label(
            title_frame,
            text="💰 BITCOIN CALCULATOR 💰",
            font=('Arial', 20, 'bold'),  # Reduced font size from 24 to 20
            fg='#f2a900',
            bg='#1a1a2e'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="100% Accurate Calculations | Satoshi Precision",
            font=('Arial', 9),  # Reduced from 10 to 9
            fg='#888888',
            bg='#1a1a2e'
        )
        subtitle_label.pack()
        
        # Live Price Frame
        price_frame = tk.Frame(self.window, bg='#16213e', relief=tk.RAISED, bd=2)
        price_frame.pack(pady=8, padx=15, fill='x')  # Reduced padding
        
        price_label = tk.Label(
            price_frame,
            text="Live Bitcoin Price",
            font=('Arial', 11, 'bold'),  # Reduced from 12 to 11
            fg='#ffffff',
            bg='#16213e'
        )
        price_label.pack(pady=3)  # Reduced from 5 to 3
        
        self.live_price_label = tk.Label(
            price_frame,
            text="$ --,---.--",
            font=('Arial', 18, 'bold'),  # Reduced from 20 to 18
            fg='#00ff00',
            bg='#16213e'
        )
        self.live_price_label.pack(pady=3)  # Reduced from 5 to 3
        
        price_update_label = tk.Label(
            price_frame,
            text="Auto-updates every 10 seconds",
            font=('Arial', 7),  # Reduced from 8 to 7
            fg='#888888',
            bg='#16213e'
        )
        price_update_label.pack(pady=2)
        
        # Input Frame
        input_frame = tk.Frame(self.window, bg='#1a1a2e')
        input_frame.pack(pady=15, padx=15, fill='x')  # Reduced padding
        
        # BTC Price Input
        tk.Label(
            input_frame,
            text="Bitcoin Price (USD):",
            font=('Arial', 10),  # Reduced from 11 to 10
            fg='#ffffff',
            bg='#1a1a2e'
        ).pack(anchor='w', pady=(0, 3))  # Reduced pady
        
        self.price_entry = tk.Entry(
            input_frame,
            font=('Arial', 12),  # Reduced from 14 to 12
            bg='#0f3460',
            fg='#ffffff',
            insertbackground='white',
            relief=tk.FLAT
        )
        self.price_entry.pack(fill='x', pady=(0, 10))  # Reduced from 15 to 10
        self.price_entry.insert(0, "50000")
        
        # USD Amount Input
        tk.Label(
            input_frame,
            text="USD Amount to Spend:",
            font=('Arial', 10),  # Reduced from 11 to 10
            fg='#ffffff',
            bg='#1a1a2e'
        ).pack(anchor='w', pady=(0, 3))  # Reduced pady
        
        self.usd_entry = tk.Entry(
            input_frame,
            font=('Arial', 12),  # Reduced from 14 to 12
            bg='#0f3460',
            fg='#ffffff',
            insertbackground='white',
            relief=tk.FLAT
        )
        self.usd_entry.pack(fill='x', pady=(0, 10))  # Reduced from 15 to 10
        self.usd_entry.insert(0, "100")
        
        # BTC Amount Input (for selling)
        tk.Label(
            input_frame,
            text="BTC Amount to Sell:",
            font=('Arial', 10),  # Reduced from 11 to 10
            fg='#ffffff',
            bg='#1a1a2e'
        ).pack(anchor='w', pady=(0, 3))  # Reduced pady
        
        self.btc_entry = tk.Entry(
            input_frame,
            font=('Arial', 12),  # Reduced from 14 to 12
            bg='#0f3460',
            fg='#ffffff',
            insertbackground='white',
            relief=tk.FLAT
        )
        self.btc_entry.pack(fill='x', pady=(0, 10))  # Reduced from 15 to 10
        self.btc_entry.insert(0, "0.001")
        
        # Button Frame
        button_frame = tk.Frame(self.window, bg='#1a1a2e')
        button_frame.pack(pady=8)  # Reduced from 10 to 8
        
        # Calculate Buy Button
        self.buy_button = tk.Button(
            button_frame,
            text="🟢 CALCULATE PURCHASE",
            font=('Arial', 10, 'bold'),  # Reduced from 12 to 10
            bg='#00a8ff',
            fg='white',
            activebackground='#0097e6',
            activeforeground='white',
            relief=tk.FLAT,
            padx=15,  # Reduced from 20 to 15
            pady=8,   # Reduced from 10 to 8
            command=self.calculate_purchase
        )
        self.buy_button.pack(side='left', padx=8)  # Reduced from 10 to 8
        
        # Calculate Sell Button
        self.sell_button = tk.Button(
            button_frame,
            text="🔴 CALCULATE SALE",
            font=('Arial', 10, 'bold'),  # Reduced from 12 to 10
            bg='#e84118',
            fg='white',
            activebackground='#c23616',
            activeforeground='white',
            relief=tk.FLAT,
            padx=15,  # Reduced from 20 to 15
            pady=8,   # Reduced from 10 to 8
            command=self.calculate_sale
        )
        self.sell_button.pack(side='left', padx=8)  # Reduced from 10 to 8
        
        # Results Frame
        results_frame = tk.Frame(self.window, bg='#16213e', relief=tk.RAISED, bd=2)
        results_frame.pack(pady=15, padx=15, fill='both', expand=True)  # Reduced padding
        
        results_title = tk.Label(
            results_frame,
            text="📊 RESULTS 📊",
            font=('Arial', 12, 'bold'),  # Reduced from 14 to 12
            fg='#f2a900',
            bg='#16213e'
        )
        results_title.pack(pady=8)  # Reduced from 10 to 8
        
        # Results Text Widget with Scrollbar
        text_frame = tk.Frame(results_frame, bg='#16213e')
        text_frame.pack(fill='both', expand=True, padx=8, pady=5)  # Reduced padding
        
        self.results_text = tk.Text(
            text_frame,
            font=('Courier', 9),  # Reduced from 10 to 9
            bg='#0f3460',
            fg='#00ff00',
            relief=tk.FLAT,
            wrap=tk.WORD,
            height=10  # Reduced from 12 to 10
        )
        self.results_text.pack(side='left', fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(text_frame, command=self.results_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.results_text.config(yscrollcommand=scrollbar.set)
        
        # Status Bar
        self.status_label = tk.Label(
            self.window,
            text="Ready ✓",
            font=('Arial', 8),  # Reduced from 9 to 8
            fg='#888888',
            bg='#1a1a2e',
            anchor='w'
        )
        self.status_label.pack(side='bottom', fill='x', padx=15, pady=8)  # Reduced padding
        
        # Clear Results Button
        clear_button = tk.Button(
            self.window,
            text="Clear Results",
            font=('Arial', 9),  # Reduced from 10 to 9
            bg='#353b48',
            fg='white',
            command=self.clear_results
        )
        clear_button.pack(pady=(0, 8))  # Reduced from 10 to 8
        
    def btc_to_satoshi(self, btc_amount):
        """Convert Bitcoin to Satoshis"""
        return (Decimal(str(btc_amount)) * self.SATOSHI_PER_BTC).quantize(Decimal('1'))
    
    def satoshi_to_btc(self, satoshi_amount):
        """Convert Satoshis to Bitcoin"""
        return (Decimal(str(satoshi_amount)) / self.SATOSHI_PER_BTC).quantize(Decimal('0.00000001'))
    
    def get_live_btc_price(self):
        """Fetch live Bitcoin price"""
        try:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
            with urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode())
                return Decimal(str(data['bitcoin']['usd']))
        except:
            return None
    
    def update_live_price(self):
        """Update live price in background"""
        def fetch_price():
            price = self.get_live_btc_price()
            if price:
                self.live_price_label.config(text=f"${price:,.2f}")
                self.price_entry.delete(0, tk.END)
                self.price_entry.insert(0, str(price))
                self.status_label.config(text=f"✓ Live price updated: ${price:,.2f}")
            else:
                self.status_label.config(text="⚠ Could not fetch live price (using manual input)")
            
            # Schedule next update after 10 seconds
            self.window.after(10000, self.update_live_price)
        
        # Run in separate thread to not block UI
        thread = threading.Thread(target=fetch_price, daemon=True)
        thread.start()
    
    def calculate_purchase(self):
        """Calculate BTC purchase from USD"""
        try:
            btc_price = Decimal(self.price_entry.get())
            usd_amount = Decimal(self.usd_entry.get())
            
            # Perform calculation
            btc_amount = (usd_amount / btc_price).quantize(Decimal('0.00000001'))
            satoshi_amount = self.btc_to_satoshi(btc_amount)
            
            # Format results
            result = f"""
╔════════════════════════════════════════════════════╗
║              PURCHASE CALCULATION                  ║
╠════════════════════════════════════════════════════╣
║  BTC Price:     ${btc_price:>15,.2f}              ║
║  USD Spent:     ${usd_amount:>15,.2f}              ║
╠════════════════════════════════════════════════════╣
║  BTC Received:  {btc_amount:>15,.8f} BTC          ║
║  Satoshis:      {satoshi_amount:>15,} sat         ║
╠════════════════════════════════════════════════════╣
║  Human Readable:                                   ║
║  {self.format_btc_human_readable(btc_amount):^48}    ║
╚════════════════════════════════════════════════════╝
            """
            
            self.results_text.insert('1.0', result + "\n\n")
            self.status_label.config(text="✓ Purchase calculation completed")
            
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
    
    def calculate_sale(self):
        """Calculate USD from BTC sale"""
        try:
            btc_price = Decimal(self.price_entry.get())
            btc_amount = Decimal(self.btc_entry.get())
            
            # Perform calculation
            usd_amount = (btc_amount * btc_price).quantize(Decimal('0.01'))
            satoshi_amount = self.btc_to_satoshi(btc_amount)
            
            # Format results
            result = f"""
╔════════════════════════════════════════════════════╗
║                  SALE CALCULATION                  ║
╠════════════════════════════════════════════════════╣
║  BTC Price:     ${btc_price:>15,.2f}              ║
║  BTC Sold:      {btc_amount:>15,.8f} BTC          ║
║  Satoshis:      {satoshi_amount:>15,} sat         ║
╠════════════════════════════════════════════════════╣
║  USD Received:  ${usd_amount:>15,.2f}             ║
╠════════════════════════════════════════════════════╣
║  Human Readable:                                   ║
║  {self.format_btc_human_readable(btc_amount):^48}    ║
╚════════════════════════════════════════════════════╝
            """
            
            self.results_text.insert('1.0', result + "\n\n")
            self.status_label.config(text="✓ Sale calculation completed")
            
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
    
    def format_btc_human_readable(self, btc_amount):
        """Format BTC like a human would"""
        btc = Decimal(str(btc_amount))
        
        if btc >= 1:
            return f"{btc:.4f} BTC"
        elif btc >= 0.01:
            return f"{btc:.6f} BTC"
        elif btc >= 0.0001:
            return f"{btc:.8f} BTC"
        else:
            satoshi = self.btc_to_satoshi(btc)
            return f"{satoshi} satoshis"
    
    def clear_results(self):
        """Clear the results text widget"""
        self.results_text.delete('1.0', tk.END)
        self.status_label.config(text="✓ Results cleared")
    
    def run(self):
        """Start the GUI application"""
        self.window.mainloop()

# Run the application
if __name__ == "__main__":
    app = BitcoinCalculatorGUI()
    app.run()