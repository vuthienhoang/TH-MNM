import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk

# Khai báo biến toàn cục
img = None
drawing = False
ix, iy = -1, -1
fx, fy = -1, -1

# Hàm để hiển thị ảnh trên giao diện
def hien_thi_anh(image_to_display):
    img = Image.fromarray(cv2.cvtColor(image_to_display, cv2.COLOR_BGR2RGB))
    img = ImageTk.PhotoImage(image=img)
    panel.configure(image=img)
    panel.image = img

# Hàm xử lý sự kiện khi chuột được nhấn xuống để bắt đầu vẽ hình chữ nhật
def chuot_nhan_xuong(event):
    global drawing, ix, iy
    drawing = True
    ix, iy = event.x, event.y

# Hàm xử lý sự kiện khi chuột được kéo để vẽ hình chữ nhật
def chuot_keo(event):
    global img, drawing, ix, iy, fx, fy
    if drawing:
        fx, fy = event.x, event.y
        img_copy = img.copy()
        cv2.rectangle(img_copy, (ix, iy), (fx, fy), (0, 255, 0), 2)
        hien_thi_anh(img_copy)

# Hàm xử lý sự kiện khi chuột được thả ra sau khi vẽ xong hình chữ nhật
def chuot_tha(event):
    global drawing, ix, iy, fx, fy, img
    if drawing:
        drawing = False
        roi = img[iy:fy, ix:fx]
        # Áp dụng mờ Gaussian lên vùng đã khoanh vùng
        blurred_roi = cv2.GaussianBlur(roi, (15, 15), 0)
        img[iy:fy, ix:fx] = blurred_roi
        hien_thi_anh(img)

# Hàm khi nút "Mở ảnh" được nhấn
def mo_anh():
    global img
    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path)
        hien_thi_anh(img)

# Tạo cửa sổ giao diện
top = tk.Tk()
top.title("Xử Lý Ảnh")

# Tạo nút "Mở ảnh"
open_button = tk.Button(top, text="Mở ảnh", command=mo_anh)
open_button.pack()

# Panel để hiển thị ảnh
panel = tk.Label(top)
panel.pack()

# Gắn các sự kiện chuột để vẽ hình chữ nhật
panel.bind("<Button-1>", chuot_nhan_xuong)
panel.bind("<B1-Motion>", chuot_keo)
panel.bind("<ButtonRelease-1>", chuot_tha)

top.mainloop()