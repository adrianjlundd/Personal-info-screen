import tkinter as tk
from datetime import datetime
from calendar_fetch import CalendarFetcher
from bus_frame import BusFetcher
from weather_frame import WeatherFetcher

class PersonalInfoApp:
    def __init__(self):
        self.calendar_fetcher = CalendarFetcher()
        self.bus_fetcher = BusFetcher(stop_id="NSR:StopPlace:43133")
        self.weather_fetcher = WeatherFetcher()
        
        self.setup_gui()
        self.start_updates()
    
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Personal Dashboard")
        self.root.geometry("700x800")
        self.root.configure(bg='#2C3E50')
        
        # Main container with padding
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        # Header with datetime
        self.datetime_label = tk.Label(
            main_frame, 
            text="", 
            font=("Helvetica", 20, "bold"),
            fg='#ECF0F1',
            bg='#2C3E50'
        )
        self.datetime_label.pack(pady=(0, 20))
        
        # Calendar section
        self.create_section(main_frame, "📅 Kalender - Neste 2 dager", self.create_calendar_widget)
        
        # Bus section
        self.create_section(main_frame, "🚌 Buss til Sentrum", self.create_bus_widget)
        
        # Weather section
        self.create_section(main_frame, "☀️ Vær", self.create_weather_widget)
    
    def create_section(self, parent, title, widget_creator):
        """Create a consistent section with title and content"""
        section_frame = tk.Frame(parent, bg='#34495E', relief='raised', bd=1)
        section_frame.pack(fill='x', pady=10)
        
        title_label = tk.Label(
            section_frame,
            text=title,
            font=("Helvetica", 16, "bold"),
            fg='#ECF0F1',
            bg='#34495E',
            pady=10
        )
        title_label.pack()
        
        content_frame = tk.Frame(section_frame, bg='#34495E')
        content_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        widget_creator(content_frame)
    
    def create_calendar_widget(self, parent):
        self.calendar_listbox = tk.Listbox(
            parent,
            width=80,
            height=6,
            font=("Helvetica", 11),
            bg='#ECF0F1',
            fg='#2C3E50',
            selectbackground='#3498DB'
        )
        self.calendar_listbox.pack(fill='x')
    
    def create_bus_widget(self, parent):
        self.bus_listbox = tk.Listbox(
            parent,
            width=80,
            height=4,
            font=("Helvetica", 12),
            bg='#ECF0F1',
            fg='#2C3E50',
            selectbackground='#3498DB'
        )
        self.bus_listbox.pack(fill='x')
    
    def create_weather_widget(self, parent):
        self.weather_label = tk.Label(
            parent,
            text="",
            font=("Helvetica", 14),
            fg='#ECF0F1',
            bg='#34495E',
            pady=10
        )
        self.weather_label.pack()
    
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
            events = self.calendar_fetcher.list_upcoming_events(days=2)
            for event in events:
                self.calendar_listbox.insert(tk.END, event)
        except Exception as e:
            self.calendar_listbox.insert(tk.END, f"Feil ved henting av kalender: {e}")
        
        self.root.after(3600000, self.update_calendar)  # Hver time
    
    def update_buses(self):
        self.bus_listbox.delete(0, tk.END)
        try:
            buses = self.bus_fetcher.list_next_buses()
            for bus in buses:
                self.bus_listbox.insert(tk.END, bus)
        except Exception as e:
            self.bus_listbox.insert(tk.END, f"Feil ved henting av busser: {e}")
        
        self.root.after(60000, self.update_buses)  # Hvert minutt
    
    def update_weather(self):
        try:
            weather_text = self.weather_fetcher.get_weather()
            self.weather_label.config(text=weather_text)
        except Exception as e:
            self.weather_label.config(text=f"Feil ved henting av vær: {e}")
        
        self.root.after(1800000, self.update_weather)  # Hver 30 minutt
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PersonalInfoApp()
    app.run()