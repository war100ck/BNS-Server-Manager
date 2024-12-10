import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
import subprocess
import os
import json

# Путь к конфигурационному файлу
CONFIG_FILE = "config.json"

# Функция для создания конфигурационного файла с дефолтными значениями
def create_default_config():
    default_services = [
        {"name": "RankingDaemon", "path": "D:\\service\\RankingDaemon\\bin\\RankingDaemon.exe", "interval": 15, "enabled": True},
        {"name": "AccountInventoryDaemon", "path": "D:\\service\\AccountInventoryDaemon\\bin\\AccountInventoryDaemon.exe", "interval": 10, "enabled": True},
        {"name": "CacheDaemon", "path": "D:\\service\\CacheDaemon01\\bin\\CacheDaemon.exe", "interval": 8, "enabled": True},
        {"name": "CacheGate", "path": "D:\\service\\CacheGate\\bin\\CacheGate.exe", "interval": 8, "enabled": True},
        {"name": "PostOfficeDaemon", "path": "D:\\service\\PostOfficeDaemon\\bin\\PostOfficeDaemon.exe", "interval": 8, "enabled": True},
        {"name": "LobbyDaemon", "path": "D:\\service\\LobbyDaemon\\bin\\LobbyDaemon.exe", "interval": 15, "enabled": True},
        {"name": "CraftDaemon", "path": "D:\\service\\CraftDaemon\\bin\\CraftDaemon.exe", "interval": 10, "enabled": True},
        {"name": "MarketReaderDaemon", "path": "D:\\service\\MarketReaderDaemon\\bin\\MarketReaderDaemon.exe", "interval": 8, "enabled": True},
        {"name": "MarketReaderAgent", "path": "D:\\service\\MarketReaderAgent\\bin\\MarketReaderAgent.exe", "interval": 8, "enabled": True},
        {"name": "MarketDealerDaemon", "path": "D:\\service\\MarketDealerDaemon\\bin\\MarketDealerDaemon.exe", "interval": 8, "enabled": True},
        {"name": "MarketDealerAgent", "path": "D:\\service\\MarketDealerAgent\\bin\\MarketDealerAgent.exe", "interval": 8, "enabled": True},
        {"name": "ArenaLobby", "path": "D:\\service\\ArenaLobby\\bin\\ArenaLobby.exe", "interval": 8, "enabled": True},
        {"name": "AchievementDaemon", "path": "D:\\service\\AchievementDaemon\\bin\\AchievementDaemon.exe", "interval": 25, "enabled": True},
        {"name": "DuelBotDaemon", "path": "D:\\service\\DuelbotDaemon\\bin\\DuelBotDaemon.exe", "interval": 25, "enabled": True},
        {"name": "GameDaemon", "path": "D:\\service\\GameDaemon01\\bin\\GameDaemon.exe", "interval": 180, "enabled": True},
        {"name": "InfoGateDaemon", "path": "D:\\service\\InfoGateDaemon\\bin\\InfoGateDaemon.exe", "interval": 10, "enabled": True},
        {"name": "LobbyGate", "path": "D:\\service\\LobbyGate\\bin\\LobbyGate.exe", "interval": 8, "enabled": True},
        {"name": "Dungeon", "path": "D:\\service\\DungeonDaemon01\\bin\\GameDaemon.exe", "interval": 180, "enabled": False},
        {"name": "Arena", "path": "D:\\service\\ArenaDaemon01\\bin\\GameDaemon.exe", "interval": 180, "enabled": False},
    ]
    with open(CONFIG_FILE, "w") as f:
        json.dump(default_services, f, indent=4)
    print("Default config created.")

# Загрузка конфигурации
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            print("Config loaded.")
            return config
    return []

# Сохранение конфигурации
def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(services, f, indent=4)
    print("Config saved.")

# Функция для изменения пути сервиса
def change_path(service, path_label):
    new_path = filedialog.askopenfilename(title="Select Service Executable", filetypes=[("Executable Files", "*.exe")])
    if new_path:
        service["path"] = new_path
        path_label.config(text=new_path)

# Список сервисов (загружается из конфигурации)
services = load_config()

# Если конфигурация пуста, создаем дефолтный конфиг
if not services:
    create_default_config()
    services = load_config()

# Функция для обновления интервала
def update_interval(service, interval_label, interval_entry):
    try:
        new_interval = int(interval_entry.get())  # Получаем новое значение интервала
        if new_interval <= 0:
            raise ValueError("Interval must be greater than 0.")
        service['interval'] = new_interval  # Обновляем интервал
        interval_label.config(text=f"Interval: {new_interval} sec")  # Обновляем отображаемый текст
        save_config()  # Сохраняем изменения в конфигурации
        log_message(f"Interval for {service['name']} updated to {new_interval} sec.")  # Логируем обновление интервала
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid interval: {e}")

# Функция для запуска сервиса
def start_service(service, state_canvas):
    try:
        # Определяем рабочую директорию
        service_dir = os.path.dirname(service["path"])
        
        # Проверяем, что это .bat файл
        if service["path"].endswith(".bat"):
            subprocess.Popen(
                f'start cmd /k "{service["path"]}"', 
                shell=True, 
                cwd=service_dir
            )
        else:
            subprocess.Popen(
                service["path"],
                shell=True,
                cwd=service_dir,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        
        update_indicator(state_canvas, "Running")
        log_message(f"Service {service['name']} started.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start {service['name']}: {e}")
        update_indicator(state_canvas, "Stopped")

# Функция для остановки сервиса
def stop_service(service, state_canvas):
    try:
        subprocess.run(["taskkill", "/f", "/im", service["name"] + ".exe"], check=True)
        update_indicator(state_canvas, "Stopped")  # Обновляем индикатор в красный цвет
        service['enabled'] = True  # Включаем сервис после остановки, чтобы его можно было снова запустить
        save_config()
        log_message(f"Service {service['name']} stopped.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to stop {service['name']}: {e}")
        update_indicator(state_canvas, "Running")  # Если не удалось остановить, возвращаем индикатор в зеленый

# Функция для остановки всех сервисов
def stop_all_services():
    for service in services:
        if service['enabled']:
            try:
                subprocess.run(["taskkill", "/f", "/im", service["name"] + ".exe"], check=True)
                # Не сбрасываем флаг enabled на False
                log_message(f"Stopped {service['name']}")
            except subprocess.CalledProcessError as e:
                log_message(f"Failed to stop {service['name']}: {e}")
            # Обновляем индикатор каждого сервиса
            state_canvas = service_buttons[service["name"]]["state_canvas"]
            update_indicator(state_canvas, "Stopped")
    save_config()

# Обновление индикатора состояния
def update_indicator(canvas, state):
    color = "green" if state == "Running" else "red"
    canvas.itemconfig("indicator", fill=color)

# Функция для старта всех сервисов с интервалами
def start_all_services():
    current_time = 0  # Время начала для первого запуска
    for service in services:
        if service["enabled"]:  # Только активные сервисы
            start_with_delay(service, current_time)
            current_time += service["interval"]  # Добавляем интервал к следующему запуску

# Запуск сервиса с задержкой по интервалу
def start_with_delay(service, start_time):
    def delayed_start():
        state_canvas = service_buttons[service["name"]]["state_canvas"]
        start_service(service, state_canvas)
    app.after(start_time * 1000, delayed_start)

# Функция для вывода логов в консоль
def log_message(message):
    console_output.insert("end", message + "\n")
    console_output.yview("end")

# Создание GUI
app = ttk.Window(themename="superhero")
app.title("BNS Server Manager")
app.geometry("1000x600")
app.resizable(True, True)

# Устанавливаем окно всегда поверх других окон
app.attributes("-topmost", True)

# Создание вкладок
notebook = ttk.Notebook(app)
notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Вкладка "Management"
management_tab = ttk.Frame(notebook)
notebook.add(management_tab, text="Management")

columns_frame = ttk.Frame(management_tab)
columns_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

left_column = ttk.Frame(columns_frame)
left_column.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

right_column = ttk.Frame(columns_frame)
right_column.pack(side=RIGHT, fill=BOTH, expand=True, padx=10)

half = len(services) // 2
left_services = services[:half]
right_services = services[half:]

service_buttons = {}

# Функция для добавления сервисов в колонку
def add_services_to_column(column, service_list):
    for service in service_list:
        row = ttk.Frame(column, padding=5)
        row.pack(fill=X, pady=2)

        ttk.Label(row, text=service["name"], width=20, anchor="w").pack(side=LEFT, padx=5)

        enabled_var = ttk.BooleanVar(value=service['enabled'])
        ttk.Checkbutton(row, variable=enabled_var, text="Enabled", command=lambda s=service, var=enabled_var: toggle_service(s, var)).pack(side=LEFT, padx=5)

        ttk.Button(
            row, text="Start", bootstyle=SUCCESS, command=lambda s=service: start_service(s, service_buttons[s["name"]]["state_canvas"])
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            row, text="Stop", bootstyle=DANGER, command=lambda s=service: stop_service(s, service_buttons[s["name"]]["state_canvas"])
        ).pack(side=LEFT, padx=5)

        # Добавляем индикатор сразу справа от кнопки Stop
        state_canvas = ttk.Canvas(row, width=20, height=20)
        state_canvas.create_oval(2, 2, 18, 18, fill="red", tags="indicator")
        state_canvas.pack(side=LEFT, padx=15)  # Расстояние между кнопкой Stop и индикатора

        service_buttons[service["name"]] = {
            "state_canvas": state_canvas,
        }

# Функция для включения/отключения сервиса
def toggle_service(service, var):
    service['enabled'] = var.get()
    save_config()

# Добавление сервисов в колонки
add_services_to_column(left_column, left_services)
add_services_to_column(right_column, right_services)

# Вкладка "Settings"
settings_tab = ttk.Frame(notebook)
notebook.add(settings_tab, text="Settings")

# Оборачиваем контейнер для настроек в Canvas с прокруткой
canvas = ttk.Canvas(settings_tab)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar = ttk.Scrollbar(settings_tab, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.configure(yscrollcommand=scrollbar.set)

settings_frame = ttk.Frame(canvas, padding=10)
canvas.create_window((0, 0), window=settings_frame, anchor="nw")

# Добавляем настройки в settings_frame
for service in services:
    row = ttk.Frame(settings_frame, padding=5)
    row.pack(fill=X, pady=2)

    ttk.Label(row, text=service["name"], width=20, anchor="w").pack(side=LEFT, padx=5)

    path_label = ttk.Label(row, text=service["path"], anchor="w", width=70)
    path_label.pack(side=LEFT, padx=5)

    control_frame = ttk.Frame(row)  # Добавляем новый фрейм для кнопок и полей
    control_frame.pack(side=RIGHT, padx=5)

    ttk.Button(
        control_frame, text="Browse", bootstyle=INFO, command=lambda s=service, l=path_label: change_path(s, l)
    ).pack(side=LEFT, padx=5)

    interval_label = ttk.Label(control_frame, text=f"Interval: {service['interval']} sec", width=20, anchor="w")
    interval_label.pack(side=LEFT, padx=5)

    interval_entry = ttk.Entry(control_frame, width=10)
    interval_entry.insert(0, str(service['interval']))
    interval_entry.pack(side=LEFT, padx=5)

    # Кнопка Save для каждого сервиса
    ttk.Button(
        control_frame, text="Save", bootstyle=PRIMARY, command=lambda s=service, i_label=interval_label, i_entry=interval_entry: update_interval(s, i_label, i_entry)
    ).pack(side=LEFT, padx=5)

# Устанавливаем правильный размер канвы с прокруткой
settings_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Вкладка для добавления нового сервиса
add_service_tab = ttk.Frame(notebook)
notebook.add(add_service_tab, text="Add New Service")

add_service_frame = ttk.Frame(add_service_tab, padding=10)
add_service_frame.pack(fill=X, pady=10)

# Поле для ввода имени сервиса
ttk.Label(add_service_frame, text="Service Name:").pack(side=LEFT, padx=10)
service_name_entry = ttk.Entry(add_service_frame, width=50)
service_name_entry.pack(side=LEFT, padx=10)

# Функция для выбора пути с помощью диалогового окна
def browse_file():
    new_path = filedialog.askopenfilename(title="Select Service Executable", filetypes=[("Executable Files", "*.exe *.bat")])
    if new_path:
        service_path_entry.delete(0, "end")
        service_path_entry.insert(0, new_path)

# Кнопка Browse для выбора пути
ttk.Button(add_service_frame, text="Browse", bootstyle=INFO, command=browse_file).pack(side=LEFT, padx=10)

# Поле для ввода пути (скрыто, но сохраняется для использования)
service_path_entry = ttk.Entry(add_service_frame, width=50)
service_path_entry.pack(side=LEFT, padx=10)
service_path_entry.insert(0, "No file selected")  # Задать начальный текст

# Функция для добавления нового сервиса
def add_new_service():
    service_name = service_name_entry.get()
    service_path = service_path_entry.get()  # Получаем путь из поля ввода
    if service_name and service_path and service_path != "No file selected":
        new_service = {
            "name": service_name,
            "path": service_path,
            "interval": 10,  # По умолчанию интервал 10 секунд
            "enabled": True
        }
        services.append(new_service)
        save_config()

        # Обновляем список сервисов на вкладке "Management" сразу после добавления
        add_services_to_column(left_column, [new_service]) if len(services) % 2 == 0 else add_services_to_column(right_column, [new_service])

        messagebox.showinfo("Success", f"Service {service_name} added successfully!")
        service_name_entry.delete(0, "end")
        service_path_entry.delete(0, "end")  # Очищаем путь
        service_path_entry.insert(0, "No file selected")  # Вставляем начальный текст
    else:
        messagebox.showerror("Error", "Please fill in both fields.")

# Кнопка для добавления сервиса
ttk.Button(add_service_frame, text="Add Service", bootstyle=PRIMARY, command=add_new_service).pack(side=LEFT, padx=10)


# Вкладка "Console"
console_tab = ttk.Frame(notebook)
notebook.add(console_tab, text="Console")

# Текстовое поле для вывода логов
console_output = ttk.Text(console_tab, wrap="word", height=20, width=80)
console_output.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Кнопки управления на вкладке "Management"
control_frame = ttk.Frame(app, padding=10)  # Вместо использования 'management_tab' используем 'app'
control_frame.pack(side=BOTTOM, fill=X, pady=10)  # Размещаем внизу окна

# Кнопка "Start All Services"
ttk.Button(control_frame, text="Start All Services", bootstyle=SUCCESS, command=start_all_services).pack(side=LEFT, padx=10)

# Кнопка "Stop All Services"
ttk.Button(control_frame, text="Stop All Services", bootstyle=DANGER, command=stop_all_services).pack(side=LEFT, padx=10)

# Кнопка "Exit"
ttk.Button(control_frame, text="Exit", bootstyle=SECONDARY, command=lambda: (save_config(), app.quit())).pack(side=RIGHT, padx=10)


# Запуск главного цикла приложения
app.mainloop()
