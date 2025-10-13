import tkinter as tk
from datetime import datetime
from calendar_fetch import CalendarFetcher
from bus_frame import BusFetcher
from weather_frame import WeatherFetcher

calendar_fetcher = CalendarFetcher()
bus_fetcher = BusFetcher(stop_id="NSR:StopPlace:43133")
weather_fetcher = WeatherFetcher()

root = tk.Tk()
root.title("Personal Info Screen")
root.geometry("600x650")

# --- Dagens dato og klokkeslett ---
datetime_label = tk.Label(root, text="", font=("Helvetica", 16, "bold"))
datetime_label.pack(pady=5)

# --- Kalender ---
tk.Label(root, text="📅 Kalender", font=("Helvetica", 16, "bold")).pack(pady=5)
calendar_listbox = tk.Listbox(root, width=80, height=8)
calendar_listbox.pack(pady=5)

# --- Buss ---
tk.Label(root, text="🚌 Buss avganger", font=("Helvetica", 16, "bold")).pack(pady=5)
bus_listbox = tk.Listbox(root, width=80, height=6)
bus_listbox.pack(pady=5)

# --- Vær ---
tk.Label(root, text="☀️ Vær", font=("Helvetica", 16, "bold")).pack(pady=5)
weather_label = tk.Label(root, text="", font=("Helvetica", 14))
weather_label.pack(pady=5)

# --- Oppdateringsfunksjoner ---
def update_datetime():
    now = datetime.now()
    datetime_label.config(text=now.strftime("%A %d. %b %Y %H:%M:%S"))
    root.after(1000, update_datetime)  # oppdater hvert sekund

def update_calendar():
    calendar_listbox.delete(0, tk.END)
    for event in calendar_fetcher.list_upcoming_events():
        calendar_listbox.insert(tk.END, event)
    root.after(3600*1000, update_calendar)  # hver time

def update_buses():
    bus_listbox.delete(0, tk.END)
    for bus in bus_fetcher.list_next_buses():
        # Fjern dato, vis kun minutter
        if "om" in bus:
            bus_listbox.insert(tk.END, bus.split("om")[0].strip() + "om " + bus.split("om")[1])
        else:
            bus_listbox.insert(tk.END, bus)
    root.after(60*1000, update_buses)  # hvert minutt

def update_weather():
    weather_label.config(text=weather_fetcher.get_weather())
    root.after(1800*1000, update_weather)  # hver 30 min

# --- Første oppdatering ---
update_datetime()
update_calendar()
update_buses()
update_weather()

root.mainloop()
