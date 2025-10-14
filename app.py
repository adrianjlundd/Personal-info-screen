import tkinter as tk
from datetime import datetime
from calendar_fetch import CalendarFetcher
from bus_frame import BusFetcher
from weather_frame import WeatherFetcher

class PersonalInfoApp:
    def __init__(self):
        self.calendar_fetchers = [
            CalendarFetcher('token_privat.json'),
            CalendarFetcher('token_samf.json'), 
            CalendarFetcher('token_abakus.json')
        ]
        self.bus_fetcher = BusFetcher(stop_id="NSR:StopPlace:43133")
        self.weather_fetcher = WeatherFetcher()
        
        self.setup_gui()
        self.start_updates()
    
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Personal Dashboard")
        self.root.configure(bg='#1a1a1a')
        self.root.attributes('-fullscreen', True)
        
        # Main grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Header with datetime - spans full width
        self.datetime_label = tk.Label(
            self.root, 
            text="", 
            font=("Helvetica", 28, "bold"),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        self.datetime_label.grid(row=0, column=0, columnspan=2, pady=(20, 30), sticky='ew')
        
        # Left column - Calendar
        calendar_frame = tk.Frame(self.root, bg='#1a1a1a')
        calendar_frame.grid(row=1, column=0, padx=(40, 20), pady=20, sticky='nsew')
        
        calendar_title = tk.Label(
            calendar_frame,
            text="📅 KALENDER",
            font=("Helvetica", 20, "bold"),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        calendar_title.pack(pady=(0, 15))
        
        self.calendar_listbox = tk.Listbox(
            calendar_frame,
            font=("Helvetica", 14),
            bg='#2d2d2d',
            fg='#ffffff',
            selectbackground='#404040',
            borderwidth=0,
            highlightthickness=0,
            height=20
        )
        self.calendar_listbox.pack(fill='both', expand=True)
        
        # Right column - Bus and Weather
        right_frame = tk.Frame(self.root, bg='#1a1a1a')
        right_frame.grid(row=1, column=1, padx=(20, 40), pady=20, sticky='nsew')
        right_frame.grid_rowconfigure(1, weight=1)
        
        # Bus section
        bus_frame = tk.Frame(right_frame, bg='#1a1a1a')
        bus_frame.grid(row=0, column=0, sticky='ew', pady=(0, 30))
        
        bus_title = tk.Label(
            bus_frame,
            text="🚌 BUSS TIL SENTRUM",
            font=("Helvetica", 20, "bold"),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        bus_title.pack(pady=(0, 15))
        
        self.bus_listbox = tk.Listbox(
            bus_frame,
            font=("Helvetica", 16),
            bg='#2d2d2d',
            fg='#ffffff',
            selectbackground='#404040',
            borderwidth=0,
            highlightthickness=0,
            height=8
        )
        self.bus_listbox.pack(fill='x')
        
        # Weather section
        weather_frame = tk.Frame(right_frame, bg='#1a1a1a')
        weather_frame.grid(row=1, column=0, sticky='ew')
        
        weather_title = tk.Label(
            weather_frame,
            text="☀️ VÆR I TRONDHEIM",
            font=("Helvetica", 20, "bold"),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        weather_title.pack(pady=(0, 15))
        
        self.weather_label = tk.Label(
            weather_frame,
            text="",
            font=("Helvetica", 18),
            fg='#ffffff',
            bg='#1a1a1a',
            pady=10
        )
        self.weather_label.pack()
        
        # Exit button
        exit_button = tk.Button(
            self.root,
            text="AVSLUTT (ESC)",
            font=("Helvetica", 12),
            command=self.root.quit,
            bg='#333333',
            fg='#ffffff',
            borderwidth=0,
            padx=20,
            pady=10
        )
        exit_button.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Bind ESC key to exit
        self.root.bind('<Escape>', lambda e: self.root.quit())
    
    def start_updates(self):
        """Start all update functions"""
        self.update_datetime()
        self.update_calendar()
        self.update_buses()
        self.update_weather()
    
    def update_datetime(self):
        now = datetime.now()
        datetime_str = now.strftime("%A %d. %B %Y   %H:%M:%S")
        self.datetime_label.config(text=datetime_str)
        self.root.after(1000, self.update_datetime)
    
    def update_calendar(self):
        self.calendar_listbox.delete(0, tk.END)
        try:
            all_events = []
            for fetcher in self.calendar_fetchers:
                events = fetcher.list_upcoming_events(days=2)
                if events:
                    all_events.extend(events)
            
            # Sort events and limit to reasonable number
            all_events.sort()
            for event in all_events[:15]:  # Show max 15 events
                self.calendar_listbox.insert(tk.END, event)
                
            if not all_events:
                self.calendar_listbox.insert(tk.END, "Ingen events de neste 2 dagene")
                
        except Exception as e:
            print(f"Calendar update error: {e}")
            self.calendar_listbox.insert(tk.END, "Feil ved henting av kalender")
        
        self.root.after(3600000, self.update_calendar)
    
    def update_buses(self):
        self.bus_listbox.delete(0, tk.END)
        try:
            buses = self.bus_fetcher.list_next_buses()
            for bus in buses:
                self.bus_listbox.insert(tk.END, bus)
        except Exception as e:
            print(f"Bus update error: {e}")
            self.bus_listbox.insert(tk.END, "Feil ved henting av busser")
        
        self.root.after(30000, self.update_buses)  # Oppdater hver 30 sekund
    
    def update_weather(self):
        try:
            weather_text = self.weather_fetcher.get_weather()
            self.weather_label.config(text=weather_text)
        except Exception as e:
            print(f"Weather update error: {e}")
            self.weather_label.config(text="Feil ved henting av vær")
        
        self.root.after(1800000, self.update_weather)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PersonalInfoApp()
    app.run()