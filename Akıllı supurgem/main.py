import tkinter as tk
from abc import ABC, abstractmethod
import time
import threading

# Haritanın genişliği ve yüksekliği
map_width = 12
map_height = 12


class Robot(ABC):
    def __init__(self, x, y, battery, speed):
        self.x = x
        self.y = y
        self.battery = battery
        self.speed = speed
        self.stop = False  # Durdurma bayrağı

    @abstractmethod
    def move(self, target_x, target_y, mode):
        pass

    def go_to_charging_station(self):
        self.x = 0
        self.y = 0
        print("Robot şarj istasyonuna döndü.")

    def charge(self):
        self.battery = 100
        print("Robot %100 şarj oldu.")

    # Robotun konumu haritanın sınırları içinde mi kontrol edilir
    def check_boundary(self, direction_x, direction_y):
        if self.x < 0 or self.x >= map_width or self.y < 0 or self.y >= map_height:
            # Robotun konumu haritanın sınırlarına ayarlanır
            self.x -= direction_x
            self.y -= direction_y
            # Robotun hareketi durdurulur
            print(f"Robotun konumu haritanın sınırlarını aştı. Hareket edilemiyor.")
            return False
        return True


class RobotSweeper(Robot):
    def __init__(self, x, y, battery, speed):
        super().__init__(x, y, battery, speed)
        self.initial_battery = battery

    def move(self, target_x, target_y, mode):
        while self.x != target_x or self.y != target_y:
            if self.stop:  # Eğer durdurma bayrağı True ise temizlik işlemi durdurulur
                return False
            if self.battery <= 50:
                print("Pil seviyesi düşük. Şarj istasyonuna gidiliyor.")
                last_x = self.x
                last_y = self.y
                self.go_to_charging_station()
                self.charge()
                self.x = last_x
                self.y = last_y
                print("Temizliğe devam ediliyor.")
                return True
            else:
                dx = target_x - self.x
                dy = target_y - self.y
                if dx > 0:
                    direction_x = 1
                elif dx < 0:
                    direction_x = -1
                else:
                    direction_x = 0
                if dy > 0:
                    direction_y = 1
                elif dy < 0:
                    direction_y = -1
                else:
                    direction_y = 0

                self.x += direction_x
                self.y += direction_y

                if not self.check_boundary(direction_x, direction_y):
                    return False

                if self.speed == 1:
                    self.battery -= 0.1
                    time.sleep(2)
                elif self.speed == 2:
                    self.battery -= 0.2
                    time.sleep(1)

                print(f"Robotun konumu: ({self.x}, {self.y})")
                print(f"Robotun pil seviyesi: %{self.battery}")

                if mode == "süpürme":
                    pass
                elif mode == "silme":
                    if self.speed == 1:
                        self.battery -= 0.2
                    elif self.speed == 2:
                        self.battery -= 0.3
                    print(f"Robot ({self.x}, {self.y}) noktasını sildi.")
        return False


def read_map_file(file_path):
    room_list = []
    with open(file_path, "r") as file:
        for line in file:
            room_info = line.strip().split(",")
            room_name = room_info[0]
            room_x = int(room_info[1])
            room_y = int(room_info[2])
            room_width = int(room_info[3])
            room_height = int(room_info[4])
            obstacle_count = int(room_info[5])
            obstacle_list = []

            for i in range(obstacle_count):
                obstacle_x = int(room_info[6 + i * 2]) + room_x  # room_x eklendi
                obstacle_y = int(room_info[7 + i * 2]) + room_y  # room_y eklendi
                obstacle_list.append((obstacle_x, obstacle_y))

            room = {
                "name": room_name,
                "x": room_x,
                "y": room_y,
                "width": room_width,
                "height": room_height,
                "obstacles": obstacle_list
            }
            room_list.append(room)
    return room_list


def start_cleaning():
    global cleaning_thread
    file_path = file_entry.get()
    mode = mode_var.get()
    speed = speed_var.get()
    clean_type = clean_type_var.get()

    if clean_type == "tüm":
        cleaning_thread = threading.Thread(target=clean_all_rooms, args=(file_path, mode, speed))
    elif clean_type == "belirli":
        selected_rooms = selected_rooms_entry.get().split()
        cleaning_thread = threading.Thread(target=select_and_clean_specific_rooms,
                                           args=(file_path, mode, speed, selected_rooms))

    cleaning_thread.start()


def stop_cleaning():
    global cleaning_thread
    if cleaning_thread and cleaning_thread.is_alive():
        robot.stop = True  # Temizlik işlemini durdurmak için bayrağı True olarak ayarla
        print("Temizlik işlemi durduruldu.")
    else:
        print("Aktif bir temizlik işlemi yok.")


def clean_all_rooms(file_path, mode, speed):
    global robot
    room_list = read_map_file(file_path)
    robot = RobotSweeper(0, 0, 100, speed)  # Robotu başlat
    clean_rooms(room_list, mode, speed)


def select_and_clean_specific_rooms(file_path, mode, speed, selected_rooms):
    global robot
    room_list = read_map_file(file_path)
    robot = RobotSweeper(0, 0, 100, speed)  # Robotu başlat
    selected_rooms_list = []
    for selected_room in selected_rooms:
        for room in room_list:
            if room["name"] == selected_room:
                selected_rooms_list.append(room)
    clean_rooms(selected_rooms_list, mode, speed)


def clean_rooms(room_list, mode, speed):
    total_obstacle_count = 0
    charge_count = 0
    total_time = 0
    total_area = 0

    robot.stop = False  # Durdurma bayrağını sıfırla
    robot.battery = 100  # Robotun pilini başlangıç değerine ayarla

    with open("temizlikraporu.txt", "w") as report_file:  # Rapor dosyasını açıyoruz
        for room in room_list:
            room_name = room["name"]
            room_x = room["x"]
            room_y = room["y"]
            room_width = room["width"]
            room_height = room["height"]
            obstacle_list = room["obstacles"]

            report_file.write(f"Temizlik işlemi başlatıldı: {room_name}\n")

            room_obstacle_count = 0
            encountered_obstacles = []

            for i in range(room_height):
                for j in range(room_width):
                    target_x = room_x + j
                    target_y = room_y + i

                    if (target_x, target_y) in obstacle_list:
                        report_file.write(f"({target_x}, {target_y}) noktasında engel var. Temizlik yapılmadı.\n")
                        total_obstacle_count += 1
                        room_obstacle_count += 1
                        encountered_obstacles.append((target_x, target_y))
                    else:
                        if robot.move(target_x, target_y, mode):
                            charge_count += 1

            total_area += room_width * room_height
            total_time += room_width * room_height

            report_file.write(f"{room_name} odası temizlendi.\n")
            report_file.write(f"{room_name} odasında karşılaşılan engel sayısı: {room_obstacle_count}\n")
            report_file.write(f"{room_name} odasında şarj sayısı: {charge_count}\n")
            report_file.write(f"{room_name} odasındaki son pil seviyesi: {robot.battery}\n\n")

    # Rapor dosyasını kapatmadan önce genel raporu da dosyaya ekliyoruz
    with open("temizlikraporu.txt", "a") as report_file:
        report_file.write("Genel Rapor\n")
        report_file.write(f"Toplam temizlik alanı: {total_area} birim2\n")
        report_file.write(f"Toplam temizlik süresi: {total_time} dakika\n")
        report_file.write(f"Toplam karşılaşılan engel sayısı: {total_obstacle_count}\n")
        report_file.write(f"Toplam şarj sayısı: {charge_count}\n")

    print("Temizlik işlemi tamamlandı.")


def show_report():
    report_window = tk.Toplevel()
    report_window.title("Temizlik Raporu")

    report_text = tk.Text(report_window, width=80, height=24)
    report_text.pack()

    with open("temizlikraporu.txt", "r") as report_file:
        report_text.insert(tk.END, report_file.read())


# Tkinter GUI
root = tk.Tk()
root.geometry("800x600")
root.title("Temizlik Robotu")

# Dosya yolu girişi
file_label = tk.Label(root, text="Harita dosyasının yolunu giriniz:")
file_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
file_entry = tk.Entry(root, width=50)
file_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

# Temizlik modu seçimi
mode_label = tk.Label(root, text="Temizlik modunu seçiniz:")
mode_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
mode_var = tk.StringVar()
mode_var.set("süpürme")
mode_option = tk.OptionMenu(root, mode_var, "süpürme", "silme")
mode_option.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# Hız seviyesi seçimi
speed_label = tk.Label(root, text="Hız seviyesini seçiniz:")
speed_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
speed_var = tk.IntVar()
speed_var.set(1)
speed_option = tk.OptionMenu(root, speed_var, 1, 2)
speed_option.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Temizlik tipi seçimi
clean_type_label = tk.Label(root, text="Temizlik tipini seçiniz:")
clean_type_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
clean_type_var = tk.StringVar()
clean_type_var.set("tüm")
clean_type_option = tk.OptionMenu(root, clean_type_var, "tüm", "belirli")
clean_type_option.grid(row=3, column=1, padx=5, pady=5, sticky="w")

# Seçili odalar girişi (Sadece belirli temizlik için)
selected_rooms_label = tk.Label(root,
                                text="Temizlemek istediğiniz odaların adlarını aralarında boşluk bırakarak girin:")
selected_rooms_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
selected_rooms_entry = tk.Entry(root, width=50)
selected_rooms_entry.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

# Temizliği başlat ve durdur düğmeleri
start_button = tk.Button(root, text="Temizliği Başlat", command=start_cleaning)
start_button.grid(row=5, column=1, padx=5, pady=5, sticky="w")

stop_button = tk.Button(root, text="Temizliği Durdur", command=stop_cleaning)
stop_button.grid(row=5, column=2, padx=5, pady=5, sticky="e")

# Raporu göster düğmesia1q1
show_report_button = tk.Button(root, text="Raporu Göster", command=show_report)
show_report_button.grid(row=6, column=1, padx=5, pady=5, sticky="w")

root.mainloop()
