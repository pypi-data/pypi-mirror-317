import tkinter as tk; from tkinter import simpledialog, messagebox;
import time
import cv2
import base64
from http.server import SimpleHTTPRequestHandler, HTTPServer
import socket
import os
import sys
import logging
import requests
import pyperclip
import pyttsx3
import speech_recognition as sr
import random,psutil,smtplib,subprocess,shutil,json,math,mouse,uuid,pyautogui
import smtplib
def switch_case(_v, _c, d=None): return _c.get(_v, d)() if callable(_c.get(_v, d)) else _c.get(_v, d)
def pop(_m, _t="Information"): tk.Tk().withdraw() or messagebox.showinfo(_t, _m) or tk.Tk().destroy()
def popinp(_p, _t="Input"): return simpledialog.askstring(_t, _p) or None
def ifnull(_v, _d): return _d if _v is None or _v == "" else _v
def popp(_a, _b): return _a + _b
def pop_with_image(_m, _img_path, _t="Information"): _img = tk.PhotoImage(file=_img_path); tk.Tk().withdraw(); messagebox.showinfo(_t, _m, _icon=_img)
def set_theme(root, theme="light"): [root.configure(bg="black") for widget in root.winfo_children()] if theme == "dark" else [root.configure(bg="white") for widget in root.winfo_children()]
def pop_switch(_c, _d=None, _n="User"): pop(f"{switch_case(popinp(f'Select an option:', _t=_n), _c, _d)}", t="Result")
def create_main_window(): return tk.Tk()
def set_window_size(_root, width=300, height=200): _root.geometry(f"{width}x{height}")
def set_window_title(_root, _title): _root.title(_title)
def set_window_icon(_root, _icon_path): _root.iconbitmap(_icon_path)
def minimize_window(_root): _root.iconify()
def maximize_window(_root): _root.state('zoomed')
def destroy_window(_root): _root.destroy()
def center_window(_root, width=300, height=200): _root.geometry(f"{width}x{height}+{(_root.winfo_screenwidth()//2)-(width//2)}+{(_root.winfo_screenheight()//2)-(height//2)}")
def set_window_bg_color(_root, color): _root.configure(bg=color)
def set_window_always_on_top(_root): _root.attributes("-topmost", True)
def remove_window_always_on_top(_root): _root.attributes("-topmost", False)
def set_window_opacity(_root, opacity): _root.attributes("-alpha", opacity)
def hide_window(_root): _root.withdraw()
def show_window(_root): _root.deiconify()
def set_window_fixed_size(_root): _root.resizable(False, False)
def enable_window_resizing(_root): _root.resizable(True, True)
def set_window_bg_image(_root, image_path): img = tk.PhotoImage(file=image_path); tk.Label(_root, image=img).place(relwidth=1, relheight=1); img.image = img
def change_window_icon(_root, icon_path): _root.iconbitmap(icon_path)
def create_label(_root, _text): return tk.Label(_root, text=_text).pack()
def create_button(_root, _text, _command): return tk.Button(_root, text=_text, command=_command).pack()
def create_entry(_root): return tk.Entry(_root).pack()
def create_text_widget(_root, _width=30, _height=10): return tk.Text(_root, width=_width, height=_height).pack()
def create_checkbox(_root, _text, _command): return tk.Checkbutton(_root, text=_text, command=_command).pack()
def create_radio_buttons(_root, _options, _command): var = tk.StringVar(); [tk.Radiobutton(_root, text=option, variable=var, value=option, command=_command).pack() for option in _options]; return var
def create_dropdown(_root, _options, _command): var = tk.StringVar(); tk.OptionMenu(_root, var, * _options, command=_command).pack(); return var
def create_listbox(_root, _items, _command): listbox = tk.Listbox(_root); [listbox.insert(tk.END, item) for item in _items]; listbox.pack(); return listbox
def create_canvas(_root, _width=400, _height=300): return tk.Canvas(_root, width=_width, height=_height).pack()
def create_progress_bar(_root): return tk.Progressbar(_root, length=200, mode='indeterminate').pack()
def create_scrollbar(_root, _widget): scrollbar = tk.Scrollbar(_root, orient=tk.VERTICAL, command=_widget.yview); _widget.config(yscrollcommand=scrollbar.set); scrollbar.pack(side=tk.RIGHT, fill=tk.Y); return scrollbar
def create_frame(_root): return tk.Frame(_root).pack()
def create_menu_bar(_root): return tk.Menu(_root)
def bind_key_press(_root, _key, _function): _root.bind(_key, _function)
def bind_mouse_click(_root, _function): _root.bind("<Button-1>", _function)
def bind_mouse_enter(_widget, _function): _widget.bind("<Enter>", _function)
def bind_mouse_leave(_widget, _function): _widget.bind("<Leave>", _function)
def bind_mouse_wheel(_root, _function): _root.bind("<MouseWheel>", _function)
def trigger_event(_widget, _event): _widget.event_generate(_event)
def update_label_text(_label, _new_text): _label.config(text=_new_text)
def update_entry_text(_entry, _new_text): _entry.delete(0, tk.END); _entry.insert(0, _new_text)
def update_text_widget(_text_widget, _new_content): _text_widget.delete(1.0, tk.END); _text_widget.insert(tk.END, _new_content)
def update_checkbox_state(_checkbox, _state): _checkbox.select() if _state else _checkbox.deselect()
def update_radio_selection(_var, _value): _var.set(_value)
def update_progress_bar(_progress, _value): _progress["value"] = _value
def disable_widget(_widget): _widget.config(state=tk.DISABLED)
def enable_widget(_widget): _widget.config(state=tk.NORMAL)
def change_widget_bg_color(_widget, _color): _widget.config(bg=_color)
def change_widget_fg_color(_widget, _color): _widget.config(fg=_color)
def change_widget_font(_widget, _font_name, _font_size): _widget.config(font=(_font_name, _font_size))
def add_widget_border(_widget, _border_width=2, _border_color="black"): _widget.config(borderwidth=_border_width, relief="solid", highlightbackground=_border_color)
def pack_with_padding(_widget, _padx=10, _pady=10): _widget.pack(padx=_padx, pady=_pady)
def grid_widget(_widget, _row, _col, _rowspan=1, _columnspan=1): _widget.grid(row=_row, column=_col, rowspan=_rowspan, columnspan=_columnspan)
def place_widget(_widget, _x, _y): _widget.place(x=_x, y=_y)
def set_grid_widget_sticky(_widget, _sticky="nsew"): _widget.grid(sticky=_sticky)
def show_info_messagebox(_message): messagebox.showinfo("Information", _message)
def show_error_messagebox(_message): messagebox.showerror("Error", _message)
def show_warning_messagebox(_message): messagebox.showwarning("Warning", _message)
def ask_yes_no_question(_question): return messagebox.askyesno("Question", _question)
def ask_for_input(_prompt): return simpledialog.askstring("Input", _prompt)
def show_messagebox_with_image(_message, _image_path): _img = tk.PhotoImage(file=_image_path); messagebox.showinfo("Information", _message, icon=_img)
def show_confirmation_messagebox(_message): return messagebox.askokcancel("Confirmation", _message)
def create_modal_dialog(_root, _message): dialog = tk.Toplevel(_root); dialog.title("Modal Dialog"); tk.Label(dialog, text=_message).pack(); tk.Button(dialog, text="OK", command=dialog.destroy).pack()
def prn(pnt):return print(pnt)
def delayed_pop(message, delay=3):time.sleep(delay);pop(message)
def create_checkbox_widget(root, text, default=False):
    checkbox = create_checkbox(root, text, command=lambda: pop(f"Selected: {checkbox.isChecked()}"))
    if default:checkbox.setChecked(True)
def validate_input(prompt, valid_type, error_message="Invalid input!"):
    while True:
        user_input = popinp(prompt)
        if valid_type == "int" and user_input.isdigit():return int(user_input)
        elif valid_type == "float" and is_valid_float(user_input):return float(user_input)
        else:pop(error_message)
def is_valid_float(value):
    try:float(value);return True
    except ValueError:return False
def depop(message, delay=3):time.sleep(delay);pop(message)
def pfk(task_name, progress, total):progress_percentage = (progress / total) * 100;message = f"{task_name} - Progress: {progress_percentage:.2f}%";pop(message)
def so(options, prompt="Select an option:"):selection = pop_switch(options, default="Invalid selection", name=prompt);return selection
def msgbox(message): pop(message)
def aynq(question):response = pop_switch({"Yes": True, "No": False}, default=False, name=question) ;return response
def show_error_messagebox(message): show_error_messagebox(message)
def show_warning_messagebox(message): show_warning_messagebox(message)
def bind_key_press(root, key, function): bind_key_press(root, key, function)
def bind_mouse_click(root, function):bind_mouse_click(root, function)
def bind_mouse_enter(widget, function):bind_mouse_enter(widget, function)
def bind_mouse_leave(widget, function):bind_mouse_leave(widget, function)
def bind_mouse_wheel(root, function):bind_mouse_wheel(root, function)
def set_window_size(root, width=300, height=200): set_window_size(root, width, height)
def animate_widget(widget, start_x, start_y, end_x, end_y, duration=1000):
    for t in range(duration):progress = t / duration;new_x = start_x + (end_x - start_x) * progress;new_y = start_y + (end_y - start_y) * progress;widget.place(x=new_x, y=new_y);time.sleep(0.01)
def capture_photo():
    cap = cv2.VideoCapture(0);ret, frame = cap.read()
    if ret:filename = "captured_photo.jpg";cv2.imwrite(filename, frame);print(f"Saved Captured Photo: {filename}");cap.release()
def record_video(duration=10):
    cap = cv2.VideoCapture(0);frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH));frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT));fourcc = cv2.VideoWriter_fourcc(*'XVID');out = cv2.VideoWriter('recorded_video.avi', fourcc, 20.0, (frame_width, frame_height));start_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:break;out.write(frame)
        if time.time() - start_time > duration:break;cv2.imshow('Recording Video Press q To Stop.', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):break
    cap.release();out.release();cv2.destroyAllWindows();print("Video Recorded.")
def get_camera_resolution():cap = cv2.VideoCapture(0);width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH));height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT));print(f"Kamera çözünürlüğü: {width}x{height}");cap.release()
def camera_zoom(factor=2.0):
    cap = cv2.VideoCapture(0);ret, frame = cap.read()
    if ret:
        height, width = frame.shape[:2];new_width = int(width * factor);new_height = int(height * factor);zoomed_frame = cv2.resize(frame, (new_width, new_height));cv2.imshow("Zoomed In", zoomed_frame)
        if cv2.waitKey(0) & 0xFF == ord('q'):pass
    cap.release();cv2.destroyAllWindows()
def reverse_string(string):reversed_str = string[::-1];print(f"Reversed String: {reversed_str}")
def encode_base64(data):encoded = base64.b64encode(data.encode('utf-8'));print(f"Base64: {encoded.decode('utf-8')}")
def decode_base64(encoded_data):decoded = base64.b64decode(encoded_data);print(f"UB16: {decoded.decode('utf-8')}")
def timer_function(func, seconds):time.sleep(seconds);func()
def start_http_server(ip="0.0.0.0", port=8000):server_address = (ip, port);httpd = HTTPServer(server_address, SimpleHTTPRequestHandler);print(f"Server started on {ip}:{port}");httpd.serve_forever()
def stop_http_server():print("Stopping server...");exit(0)
def get_server_status(url="http://localhost:8000"):
    try:
        response = requests.get(url)
        if response.status_code == 200:print("Server is up and running.")
        else:print(f"Server is down. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:print(f"Error connecting to server: {e}")
def set_server_timeout(timeout=10):socket.setdefaulttimeout(timeout);print(f"Server connection timeout set to {timeout} seconds.")
def upload_file_to_server(file_path, url="http://localhost:8000/upload"):
    with open(file_path, 'rb') as file:
        response = requests.post(url, files={'file': file})
        if response.status_code == 200:print(f"File successfully uploaded: {file_path}")
        else:print(f"File upload failed. Status Code: {response.status_code}")
def download_file_from_server(file_url, save_path):
    response = requests.get(file_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:file.write(response.content);print(f"File downloaded: {save_path}")
    else:print(f"File download failed. Status Code: {response.status_code}")
class CustomRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":self.send_response(200);self.send_header('Content-type', 'text/html');self.end_headers();self.wfile.write(b"Welcome! Server is running.")
        elif self.path == "/status":self.send_response(200);self.send_header('Content-type', 'application/json');self.end_headers();self.wfile.write(b'{"status": "online"}')
        else:self.send_response(404);self.end_headers()
def start_custom_http_server(ip="0.0.0.0", port=8000):server_address = (ip, port);httpd = HTTPServer(server_address, CustomRequestHandler);print(f"Custom server started on {ip}:{port}");httpd.serve_forever()
def set_server_access_logs(log_file="server_access.log"):logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s');print(f"Access logs are being saved to {log_file}")
def get_server_logs(log_file="server_access.log"):
    try:
        with open(log_file, 'r') as log:logs = log.readlines();print("".join(logs))
    except FileNotFoundError:print(f"{log_file} not found.")
def restart_http_server():print("Restarting server...");os.execv(sys.executable, ['python'] + sys.argv)
def iftrue(Var, function):
    if Var:function()
def iffalse(Var, function):
    if not Var:function()
def until(function):
    while True:
        if function():break
def repeat(function, times):
    for _ in range(times):function()
def oncondit(condition, function_true, function_false):
    if condition:function_true()
    else:function_false()
def repeat_forever(function):
    while True:function()
def safe_run(function, *args, **kwargs):
    try:return function(*args, **kwargs)
    except Exception as e:print(f"An error occurred: {e}");return None
def copy_to_clipboard(text):pyperclip.copy(text)
def paste_from_clipboard():return pyperclip.paste()
def text_to_speech(text):engine = pyttsx3.init();engine.say(text);engine.runAndWait()
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:print("Say something...");audio = recognizer.listen(source)
    try:return recognizer.recognize_google(audio)
    except sr.UnknownValueError:return "Could not understand audio"
    except sr.RequestError:return "Could not request results"
def start_timer(seconds, callback):
    for i in range(seconds, 0, -1):time.sleep(1);callback()
def generate_random_string(length=15):return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@/-*_', k=length))
def find_files_by_extension(directory, extension):return [f for f in os.listdir(directory) if f.endswith(extension)]
def get_ip_address():return socket.gethostbyname(socket.gethostname())
def send_email(subject, body, to_email, mailname, mailpass):server = smtplib.SMTP('smtp.gmail.com', 587);server.starttls();server.login(mailname, mailpass);message = f"Subject: {subject}\n\n{body}";server.sendmail(mailname, to_email, message);server.quit()
def convert_image_to_grayscale(image_path, output_path):image = cv2.imread(image_path);gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY);cv2.imwrite(output_path, gray_image)
def play_audio(text):engine = pyttsx3.init();engine.say(text);engine.runAndWait()
def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:print("Say something:");audio = recognizer.listen(source)
    try:return recognizer.recognize_google(audio)
    except sr.UnknownValueError:return "Sorry, I couldn't understand that."
    except sr.RequestError: return "Could not request results; check your network connection."
def get_cpu_usage():return psutil.cpu_percent(interval=1)
def get_memory_usage():return psutil.virtual_memory().percent
def open_url(url):subprocess.run(['open', url], check=True)
def create_zip_file(source_dir, output_zip):shutil.make_archive(output_zip, 'zip', source_dir)
def extract_zip_file(zip_file, extract_dir):shutil.unpack_archive(zip_file, extract_dir)
def capture_screenshot(output_path):screen = pyautogui.screenshot();screen.save(output_path)
def move_file(source, destination):shutil.move(source, destination)
def copy_file(source, destination):shutil.copy(source, destination)
def show_file_properties(file_path):stats = os.stat(file_path);return f"Size: {stats.st_size} bytes, Last Modified: {time.ctime(stats.st_mtime)}"
def check_website_status(url):response = requests.get(url);return response.status_code == 200
def run_shell_command(command):result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True);return result.stdout.decode(), result.stderr.decode()
def get_weather(city,api_key):url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}";response = requests.get(url);return response.json()
def monitor_file_changes(file_path, callback):
    last_modified = os.path.getmtime(file_path)
    while True:
        current_modified = os.path.getmtime(file_path)
        if current_modified != last_modified:last_modified = current_modified;callback();time.sleep(1)
def reverse_string(string):return string[::-1]
def calculate_factorial(number):
    if number == 0:return 1;return number * calculate_factorial(number - 1)
def swap_values(a, b):return b, a
def find_maximum(numbers):return max(numbers)
def find_minimum(numbers):return min(numbers)
def get_random_choice(choices):return random.choice(choices)
def generate_unique_id():return str(uuid.uuid4())
def concatenate_lists(list1, list2):return list1 + list2
def write_to_file(filename, content):
    with open(filename, 'w') as file:file.write(content)
def read_from_file(filename):
    with open(filename, 'r') as file:return file.read()
def parse_json(json_string):return json.loads(json_string)
def create_file_if_not_exists(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as file:file.write('')
def create_directory(directory):
    if not os.path.exists(directory):os.makedirs(directory)
def send_http_request(url, method='GET', data=None):
    if method == 'GET': response = requests.get(url)
    elif method == 'POST':response = requests.post(url, data=data);return response.text
def get_cpu_temperaturelinux():
    if sys.platform == 'linux':return float(subprocess.check_output(["cat", "/sys/class/thermal/thermal_zone0/temp"])) / 1000;return None
def calculate_square_root(number):return math.sqrt(number)
def track_mouse_position(callback):
    def on_move(x, y):callback(x, y)
    with mouse.Listener(on_move=on_move) as listener:listener.join()