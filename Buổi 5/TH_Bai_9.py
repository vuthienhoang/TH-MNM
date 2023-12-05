import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

# Define kernels
kernel_sharpen_1 = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
kernel_sharpen_2 = np.array([[1,1,1], [1,-7,1], [1,1,1]])
kernel_sharpen_3 = np.array([[-1,-1,-1,-1,-1],
                             [-1,2,2,2,-1],
                             [-1,2,8,2,-1],
                             [-1,2,2,2,-1],
                             [-1,-1,-1,-1,-1]]) / 8.0

def open_image():
    global img
    global original_img
    file_path = filedialog.askopenfilename()
    img = cv2.imread(file_path)
    img = cv2.resize(img, (500, 500))  # Thay đổi kích thước thành 500x500
    original_img = img.copy()  # Lưu ảnh gốc

    # Chuyển đổi ảnh sang định dạng RGB
    img_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)

    # Chuyển đổi ảnh thành đối tượng PhotoImage của Tkinter
    img_tk = ImageTk.PhotoImage(Image.fromarray(img_rgb))

    # Tạo một nhãn Tkinter và hiển thị ảnh
    label = tk.Label(root, image=img_tk)
    label.image = img_tk  # Giữ tham chiếu để tránh thu gom rác
    label.pack(pady=10)

def update_sharpness_and_brightness(kernel):
    global img
    sharpness = sharpness_var.get()
    brightness = brightness_var.get()
    sharpened = cv2.filter2D(img, -1, kernel * sharpness)
    adjusted_brightness = cv2.convertScaleAbs(sharpened, alpha=brightness, beta=0)

    # Hủy cửa sổ trước đó để tránh mở nhiều cửa sổ
    if hasattr(update_sharpness_and_brightness, 'window'):
        update_sharpness_and_brightness.window.destroy()

    # Tạo một cửa sổ Tkinter mới để hiển thị kết quả
    update_sharpness_and_brightness.window = tk.Toplevel(root)
    update_sharpness_and_brightness.window.title("Ảnh đã làm Sắc nét và Điều chỉnh Độ Sáng")

    # Chuyển đổi ảnh sang định dạng RGB
    result_img_rgb = cv2.cvtColor(adjusted_brightness, cv2.COLOR_BGR2RGB)
    result_img_tk = ImageTk.PhotoImage(Image.fromarray(result_img_rgb))

    # Hiển thị ảnh kết quả trong cửa sổ mới
    result_label = tk.Label(update_sharpness_and_brightness.window, image=result_img_tk)
    result_label.image = result_img_tk
    result_label.pack()

    # Lưu ảnh kết quả để sử dụng sau này
    global edited_img
    edited_img = adjusted_brightness


def save_image():
    if 'edited_img' in globals():
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if file_path:
            cv2.imwrite(file_path, edited_img)
            print(f"Saved edited image as {file_path}")
    else:
        print("Không có ảnh để lưu. Vui lòng chọn ảnh và thực hiện chỉnh sửa trước.")

root = tk.Tk()
root.title("Ứng dụng Tăng cường Sắc nét và Độ Sáng Ảnh")

btn_open = tk.Button(root, text="Chọn Ảnh", command=open_image)
btn_open.pack(pady=10)

sharpness_var = tk.DoubleVar()
sharpness_slider = ttk.Scale(root, from_=0.1, to=3.0, variable=sharpness_var, orient="horizontal", length=200)
sharpness_slider.pack(pady=10)
sharpness_slider.set(1.0)

brightness_var = tk.DoubleVar()
brightness_slider = ttk.Scale(root, from_=0.1, to=3.0, variable=brightness_var, orient="horizontal", length=200)
brightness_slider.pack(pady=10)
brightness_slider.set(1.0)

btn_sharpen_1 = tk.Button(root, text="Sử dụng Kernel 1", command=lambda: update_sharpness_and_brightness(kernel_sharpen_1))
btn_sharpen_1.pack(pady=5)

btn_sharpen_2 = tk.Button(root, text="Sử dụng Kernel 2", command=lambda: update_sharpness_and_brightness(kernel_sharpen_2))
btn_sharpen_2.pack(pady=5)

btn_sharpen_3 = tk.Button(root, text="Sử dụng Kernel 3", command=lambda: update_sharpness_and_brightness(kernel_sharpen_3))
btn_sharpen_3.pack(pady=5)

btn_save = tk.Button(root, text="Lưu Ảnh", command=save_image)
btn_save.pack(pady=5)

root.mainloop()