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

        self.is_dark_mode = None
        self.setup_gui()
        self.start_updates()

    # === MODUS-FARGER (mer harmonisk og rolig) ===
    LIGHT_COLORS = {
        "bg_main": "#f3f4f6",     # Lys gråblå bakgrunn
        "bg_panel": "#ffffff",    # Panel
        "bg_list": "#f0f0f0",     # Listefelt
        "fg_text": "#1a1a1a",     # Primærtekst
        "header_bg": "#cfd6f6",   # Myk blå toppstripe
        "button_bg": "#e0e3f0",
        "button_fg": "#1a1a1a"
    }

    DARK_COLORS = {
        "bg_main": "#0f111a",     # Dyp nøytral base
        "bg_panel": "#1c1f2a",    # Panel
        "bg_list": "#2b2f3c",     # Listefelt
        "fg_text": "#f8f8f8",     # Lys tekst
        "header_bg": "#101526",   # Diskret blågrå toppstripe
        "button_bg": "#2e3240",
        "button_fg": "#ffffff"
    }

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Personal Dashboard")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg=self.DARK_COLORS["bg_main"])

        # Layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        # === HEADER ===
        self.datetime_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 28, "bold"),
            pady=10
        )
        self.datetime_label.grid(row=0, column=0, columnspan=2, pady=(20, 30), sticky="ew")


        self.toggle_theme_button = tk.Button(
            self.root,
            text="🌓 Bytt tema",
            font=("Helvetica", 10, "bold"),
            command=self.toggle_theme,
            relief="flat",
            bd=0,
            highlightthickness=0,
            cursor="hand2",
            padx=10,
            pady=5
        )
        self.toggle_theme_button.grid(row=0, column=1, sticky="ne", padx=20, pady=10)

        # === KALENDER ===
        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.grid(row=1, column=0, padx=(40, 20), pady=20, sticky="nsew")

        self.calendar_title = tk.Label(
            self.calendar_frame,
            text="📅 KALENDER",
            font=("Helvetica", 20, "bold"),
            pady=5
        )
        self.calendar_title.pack(pady=(0, 15))

        self.calendar_listbox = tk.Listbox(
            self.calendar_frame,
            font=("Helvetica", 14),
            borderwidth=0,
            highlightthickness=0,
            height=20
        )
        self.calendar_listbox.pack(fill="both", expand=True, padx=10, pady=10)

        # === HØYRE SIDE ===
        self.right_frame = tk.Frame(self.root)
        self.right_frame.grid(row=1, column=1, padx=(20, 40), pady=20, sticky="nsew")
        self.right_frame.grid_rowconfigure(1, weight=1)

        # BUSS
        self.bus_frame = tk.Frame(self.right_frame)
        self.bus_frame.grid(row=0, column=0, sticky="ew", pady=(0, 30))
        self.bus_title = tk.Label(self.bus_frame, text="🚌 BUSS TIL SENTRUM", font=("Helvetica", 20, "bold"))
        self.bus_title.pack(pady=(0, 15))
        self.bus_listbox = tk.Listbox(
            self.bus_frame,
            font=("Helvetica", 16),
            borderwidth=0,
            highlightthickness=0,
            height=8
        )
        self.bus_listbox.pack(fill="x", padx=10)

        # VÆR
        self.weather_frame = tk.Frame(self.right_frame)
        self.weather_frame.grid(row=1, column=0, sticky="ew")
        self.weather_title = tk.Label(self.weather_frame, text="☀️ VÆR I TRONDHEIM", font=("Helvetica", 20, "bold"))
        self.weather_title.pack(pady=(0, 15))
        self.weather_label = tk.Label(self.weather_frame, font=("Helvetica", 18), pady=10)
        self.weather_label.pack()

        # EXIT
        self.exit_button = tk.Button(
            self.root,
            text="AVSLUTT (ESC)",
            font=("Helvetica", 12, "bold"),
            command=self.root.quit,
            padx=20,
            pady=10,
            relief="flat",
            bd=0,
            highlightthickness=0,
            cursor="hand2"
        )
        self.exit_button.grid(row=2, column=0, columnspan=2, pady=25)

        self.root.bind("<Escape>", lambda e: self.root.quit())

        # Start med riktig tema
        self.update_theme()

    def toggle_theme(self):
        """Bytter til motsatt modus manuelt."""
        self.is_dark_mode = not self.is_dark_mode
        self.manual_override = True   # ny flagg
        self.update_theme()

    def update_theme(self):
        """Bytter tema basert på klokke, men tar hensyn til manuell overstyring."""
        if getattr(self, "manual_override", False):
            dark_mode = self.is_dark_mode  # beholder manuell modus
        else:
            hour = datetime.now().hour
            dark_mode = (hour >= 19 or hour < 7)
            if dark_mode == self.is_dark_mode:
                return
            self.is_dark_mode = dark_mode
    
        c = self.DARK_COLORS if dark_mode else self.LIGHT_COLORS
    
        # Oppdater alle komponenter
        self.root.configure(bg=c["bg_main"])
        self.datetime_label.configure(bg=c["header_bg"], fg=c["fg_text"])
        self.calendar_frame.configure(bg=c["bg_panel"])
        self.calendar_title.configure(bg=c["bg_panel"], fg=c["fg_text"])
        self.calendar_listbox.configure(bg=c["bg_list"], fg=c["fg_text"], selectbackground=c["header_bg"])
        self.right_frame.configure(bg=c["bg_panel"])
        self.bus_frame.configure(bg=c["bg_panel"])
        self.bus_title.configure(bg=c["bg_panel"], fg=c["fg_text"])
        self.bus_listbox.configure(bg=c["bg_list"], fg=c["fg_text"], selectbackground=c["header_bg"])
        self.weather_frame.configure(bg=c["bg_panel"])
        self.weather_title.configure(bg=c["bg_panel"], fg=c["fg_text"])
        self.weather_label.configure(bg=c["bg_panel"], fg=c["fg_text"])
        self.exit_button.configure(bg=c["button_bg"], fg=c["button_fg"], activebackground=c["header_bg"])

    def start_updates(self):
        self.update_datetime()
        self.update_calendar()
        self.update_buses()
        self.update_weather()
        self.schedule_theme_check()

    def schedule_theme_check(self):
        self.update_theme()
        self.root.after(300000, self.schedule_theme_check)

    def update_datetime(self):
        now = datetime.now()
    
        # Manuelle norske navn (store forbokstaver)
        norwegian_days = [
            "Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"
        ]
        norwegian_months = [
            "januar", "februar", "mars", "april", "mai", "juni",
            "juli", "august", "september", "oktober", "november", "desember"
        ]
    
        weekday = norwegian_days[now.weekday()]         # 0 = mandag
        month = norwegian_months[now.month - 1]
    
        datetime_str = f"{weekday} {now.day}. {month} {now.year}   {now:%H:%M:%S}"
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
            all_events.sort()
            for event in all_events[:15]:
                self.calendar_listbox.insert(tk.END, event)
            if not all_events:
                self.calendar_listbox.insert(tk.END, "Ingen events de neste 2 dagene")
        except Exception as e:
            print(f"Calendar update error: {e}")
            self.calendar_listbox.insert(tk.END, "Feil ved henting av kalender")
        self.root.after(300000, self.update_calendar)  # 5 min

    def update_buses(self):
        self.bus_listbox.delete(0, tk.END)
        try:
            buses = self.bus_fetcher.list_next_buses()
            for bus in buses:
                self.bus_listbox.insert(tk.END, bus)
        except Exception as e:
            print(f"Bus update error: {e}")
            self.bus_listbox.insert(tk.END, "Feil ved henting av busser")
        self.root.after(30000, self.update_buses)

    def update_weather(self):
        try:
            weather_text = self.weather_fetcher.get_weather()
            self.weather_label.config(text=weather_text)
        except Exception as e:
            print(f"Weather update error: {e}")
            self.weather_label.config(text="Feil ved henting av vær")
        self.root.after(900000, self.update_weather)  # 15 min

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = PersonalInfoApp()
    app.run()
