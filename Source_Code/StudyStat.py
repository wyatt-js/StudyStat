import platform
import subprocess
import requests
import sys
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QVBoxLayout
import api_vars

time_total: int = 0
connected: bool = False
client_name: str = ""

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    layout, window , timer = gen_start_gui()
    sys.exit(app.exec())


def gen_start_gui():
    window = QWidget()
    window.setWindowTitle("StudyStat")
    window.setStyleSheet("background-color: rgba(153, 173, 180, 1);")
    layout = QVBoxLayout()
    label = QLabel("Enter First & Last Name: ")
    label.setStyleSheet("color: black;")
    enter = QLineEdit()
    enter.setPlaceholderText("Type Here...")
    enter.setStyleSheet("""
        QLineEdit {
            color: black;
        }
        QLineEdit::placeholder {
            color: black;
        }
    """)
    timer = QTimer()
    def on_enter():
        global client_name
        client_name = enter.text()
        label.setText(f"Hi, {enter.text()}")
        timer.timeout.connect(lambda: gen_main_gui(layout))
        timer.start(1000)
    enter.returnPressed.connect(on_enter)
    layout.addWidget(label)
    layout.addWidget(enter)
    window.setLayout(layout)
    window.show()
    return layout, window, timer


def gen_main_gui(layout):
    global connected
    check_connection()
    if connected:
        label = QLabel("You are connected to eduroam and logging time")
    else:
        label = QLabel("You are not connected to eduroam")
    label.setStyleSheet("color: black;")
    item = layout.takeAt(1)
    widget = item.widget()
    widget.deleteLater()
    layout.addWidget(label)


def check_connection():
    global connected, time_total, client_name
    ssid: str = ""
    if platform.system() == "Darwin":
        ssid = mac_get_ssid()
    else:
        ssid = win_get_ssid()
    if ssid:
        if "eduroam" in ssid and not connected:  # Newly joining the newtwork
            connected = True
        if "eduroam" not in ssid and connected:  # Leaving the network
            connected = False
    if connected:   # Logs data every minute
        time_total += 1
        if time_total > 59:
            sendData(client_name, time_total)
            time_total = 0


def sendData(client_name, time_total):
    data = {
        "client_id": client_name,
        "data": time_total
    }
    print(f"Logged {time_total} seconds")
    try:        # GitHub, censor API link by importing another file w/ var, and adding file to .gitignore
        status = requests.post("http://wyattjs.pythonanywhere.com/send_data", json=data, timeout=5)
        print(status.status_code)
    except requests.exceptions.RequestException as e:
        print(e)


def mac_get_ssid() -> str:
    result = subprocess.check_output(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"])
    result = result.decode('utf-8')
    count = 0
    for line in result.split('\n'):
        if "SSID" in line:
            count += 1
        if "SSID" in line and count > 1:
            return line.split(":")[1]


def win_get_ssid() -> str:
    subprocess_result = subprocess.Popen('netsh wlan show interfaces',shell=True,stdout=subprocess.PIPE)
    subprocess_output = subprocess_result.communicate()[0],subprocess_result.returncode
    network_name = subprocess_output[0].decode('utf-8')
    for line in network_name.split('\n'):
        if "SSID" in line:
            return line.split(":")[1]
    

if __name__ == "__main__":
    main()
