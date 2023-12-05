import numpy as np
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.signal import firwin, lfilter

# Thông số tín hiệu
fs = 5000  # Tốc độ lấy mẫu (Hz)
t = np.arange(0, 1, 1/fs)

# Tạo tín hiệu x(t)


# Tạo cửa sổ giao diện
cua_so = tk.Tk()
cua_so.title("Ve do thi")
cua_so.geometry("1000x1000")

def tao_cac_truong_phuong_trinh():
    try:
        #ket_qua_text.delete(1.0, tk.END)
        for khung_phuong_trinh in cua_so.winfo_children():
            if isinstance(khung_phuong_trinh, tk.Frame):
                khung_phuong_trinh.destroy()
        nhap_bien_do.clear()
        nhap_tan_so.clear()

        n = int(nhap_n.get())
        nhap_bien_do.clear()
        nhap_tan_so.clear()

        for i in range(n):
            khung_phuong_trinh = tk.Frame(cua_so)
            khung_phuong_trinh.pack()

            danh_sach_bien = []
            for j in range(2):
                nhap_bien_do_var = tk.Entry(khung_phuong_trinh, width=5)
                nhap_bien_do_var.pack(side=tk.LEFT)
                danh_sach_bien.append(nhap_bien_do_var)

            nhap_bien_do.append(danh_sach_bien)

            nhan_tan_so = tk.Label(khung_phuong_trinh, text="Bien do + Tan so" )
            nhan_tan_so.pack(side=tk.LEFT)



    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def reset_fields():
    nhap_n.delete(0, tk.END)
    #ket_qua_text.delete(1.0, tk.END)
    for khung_phuong_trinh in cua_so.winfo_children():
        if isinstance(khung_phuong_trinh, tk.Frame):
            khung_phuong_trinh.destroy()
    nhap_bien_do.clear()
    nhap_tan_so.clear()


def xoa_truong_phuong_trinh():
    for danh_sach_bien in nhap_bien_do:
        for nhap_bien_do_var in danh_sach_bien:
            nhap_bien_do_var.delete(0, tk.END)
    for nhap_tan_so_var in nhap_tan_so:
        nhap_tan_so_var.delete(0, tk.END)
   # ket_qua_text.delete(1.0, tk.END)
# Hàm vẽ đồ thị trên miền thời gian
def ve_do_thi_mien_thoi_gian():
    try:
        # Lấy dữ liệu từ giao diện
        bien_do_tan_so = []
        for danh_sach_bien_do_var in nhap_bien_do:
            bien_do = float(danh_sach_bien_do_var[0].get())
            tan_so = float(danh_sach_bien_do_var[1].get())
            bien_do_tan_so.append((bien_do, tan_so))

        # Tạo tín hiệu từ dữ liệu nhập
        fig = Figure(figsize=(12, 8))

        # Vẽ đồ thị cho từng tín hiệu
        for i, (bien_do, tan_so) in enumerate(bien_do_tan_so, start=1):
            x_tu_du_lieu_nhap = bien_do * np.sin(2 * np.pi * tan_so * t)
            ax = fig.add_subplot(len(bien_do_tan_so) + 1, 1, i)
            ax.plot(t, x_tu_du_lieu_nhap, label=f'Tín hiệu {tan_so} Hz')
            ax.set_title(f'Tín hiệu {tan_so} Hz')
            ax.set_xlabel('Thời gian (s)')
            ax.set_ylabel('Amplitude')
            ax.legend()

        # Tính toán và vẽ đồ thị cho tín hiệu tổng
        x_tu_du_lieu_nhap = np.zeros_like(t)
        for bien_do, tan_so in bien_do_tan_so:
            x_tu_du_lieu_nhap += bien_do * np.sin(2 * np.pi * tan_so * t)

        # Vẽ đồ thị cho tín hiệu tổng
        ax = fig.add_subplot(len(bien_do_tan_so) + 1, 1, len(bien_do_tan_so) + 1)
        ax.plot(t, x_tu_du_lieu_nhap, label='Tín hiệu tổng', linewidth=2)
        ax.set_title('Tín hiệu tổng')
        ax.set_xlabel('Thời gian (s)')
        ax.set_ylabel('Amplitude')
        ax.legend()

        # Hiển thị đồ thị
        canvas = FigureCanvasTkAgg(fig, master=tk.Toplevel(cua_so))
        canvas.draw()
        canvas.get_tk_widget().pack()

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))


def ve_do_thi_mien_tan_so():
    try:
        # Lấy dữ liệu từ giao diện
        bien_do_tan_so = []
        for danh_sach_bien_do_var in nhap_bien_do:
            bien_do = float(danh_sach_bien_do_var[0].get())
            tan_so = float(danh_sach_bien_do_var[1].get())
            bien_do_tan_so.append((bien_do, tan_so))

        # Tạo tín hiệu từ dữ liệu nhập
        fig = Figure(figsize=(12, 8))

        # Vẽ đồ thị cho từng tín hiệu trên miền tần số
        for i, (bien_do, tan_so) in enumerate(bien_do_tan_so, start=1):
            x_tu_du_lieu_nhap = bien_do * np.sin(2 * np.pi * tan_so * t)
            frequencies = np.fft.fftfreq(len(t), 1 / fs)
            X_tu_du_lieu_nhap = np.fft.fft(x_tu_du_lieu_nhap)
            ax = fig.add_subplot(len(bien_do_tan_so) + 1, 1, i)
            ax.plot(frequencies, np.abs(X_tu_du_lieu_nhap), label=f'Tín hiệu {tan_so} Hz')
            ax.set_title(f'Tín hiệu {tan_so} Hz')
            ax.set_xlabel('Tần số (Hz)')
            ax.set_ylabel('Amplitude')
            ax.legend()

        # Tính toán và vẽ đồ thị cho tín hiệu tổng trên miền tần số
        x_tu_du_lieu_nhap = np.zeros_like(t)
        for bien_do, tan_so in bien_do_tan_so:
            x_tu_du_lieu_nhap += bien_do * np.sin(2 * np.pi * tan_so * t)

        frequencies = np.fft.fftfreq(len(t), 1 / fs)
        X_tu_du_lieu_nhap = np.fft.fft(x_tu_du_lieu_nhap)
        ax = fig.add_subplot(len(bien_do_tan_so) + 1, 1, len(bien_do_tan_so) + 1)
        ax.plot(frequencies, np.abs(X_tu_du_lieu_nhap), label='Tín hiệu tổng', linewidth=2)
        ax.set_title('Tín hiệu tổng trên miền tần số')
        ax.set_xlabel('Tần số (Hz)')
        ax.set_ylabel('Amplitude')
        ax.legend()

        # Hiển thị đồ thị
        canvas = FigureCanvasTkAgg(fig, master=tk.Toplevel(cua_so))
        canvas.draw()
        canvas.get_tk_widget().pack()

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
# Hàm lọc và vẽ đồ thị
def loc_va_ve_do_thi():
    try:
        # Lấy dữ liệu từ giao diện
        bien_do_tan_so = []
        for danh_sach_bien_do_var in nhap_bien_do:
            bien_do = float(danh_sach_bien_do_var[0].get())
            tan_so = float(danh_sach_bien_do_var[1].get())
            bien_do_tan_so.append((bien_do, tan_so))

        # Tạo tín hiệu từ dữ liệu nhập
        x_tu_du_lieu_nhap = np.zeros_like(t)
        for bien_do, tan_so in bien_do_tan_so:
            x_tu_du_lieu_nhap += bien_do * np.sin(2 * np.pi * tan_so * t)
        tin_hieu_can_loc1 = int(nhap_tin_hieu_can_loc1.get())
        tin_hieu_can_loc2 = int(nhap_tin_hieu_can_loc2.get())
        # Thiết kế bộ lọc FIR
        cutoff_freqs = [tin_hieu_can_loc1, tin_hieu_can_loc2]
        nyquist = 0.5 * fs
        cutoff_normalized = [freq / nyquist for freq in cutoff_freqs]
        filter_order = 101  # Độ dài của bộ lọc FIR

        fir_filter = firwin(filter_order, cutoff_normalized, pass_zero=False)

        # Áp dụng bộ lọc cho tín hiệu
        filtered_x = lfilter(fir_filter, 1.0, x_tu_du_lieu_nhap)

        # Vẽ đồ thị trên miền thời gian sau lọc
        fig = Figure(figsize=(12, 6))
        ax = fig.add_subplot(2, 1, 1)
        ax.plot(t, x_tu_du_lieu_nhap, label='Tín hiệu nhập từ giao diện')
        ax.plot(t, filtered_x, label='Tín hiệu sau lọc', linewidth=2)
        ax.set_title('Biểu diễn tín hiệu từ dữ liệu nhập trên miền thời gian')
        ax.set_xlabel('Thời gian (s)')
        ax.set_ylabel('Amplitude')
        ax.legend()

        # Tính toán và vẽ đồ thị mô phỏng phổ tần số của tín hiệu sau lọc
        frequencies = np.fft.fftfreq(len(t), 1 / fs)
        filtered_X = np.fft.fft(filtered_x)

        ax = fig.add_subplot(2, 1, 2)
        ax.plot(frequencies, np.abs(filtered_X), label='|Tín hiệu sau lọc|', linewidth=2)
        ax.set_title('Biểu diễn tín hiệu sau lọc trên miền tần số')
        ax.set_xlabel('Tần số (Hz)')
        ax.set_ylabel('Amplitude')
        ax.legend()
        # Hiển thị đồ thị
        canvas = FigureCanvasTkAgg(fig, master=tk.Toplevel(cua_so))
        canvas.draw()
        canvas.get_tk_widget().pack()

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))


# Tạo các nút trên giao diện
# Nhập số hệ phương trình
nhan_n = tk.Label(cua_so, text="Nhập số lương tin hieu:")
nhan_n.pack()
nhap_n = tk.Entry(cua_so)
nhap_n.pack()

label1 = tk.Label(cua_so, text="Nhap tin hieu can loc")
label1.pack()
nhap_tin_hieu_can_loc1 = tk.Entry(cua_so)
nhap_tin_hieu_can_loc1.pack()

label2 = tk.Label(cua_so, text="Nhap tin hieu can loc")
label2.pack()
nhap_tin_hieu_can_loc2 = tk.Entry(cua_so)
nhap_tin_hieu_can_loc2.pack()
# Tạo danh sách các biến và hằng số
nhap_bien_do = []
nhap_tan_so = []

tao_button = tk.Button(cua_so, text="Tạo", command=tao_cac_truong_phuong_trinh)
tao_button.pack()

xoa_button = tk.Button(cua_so, text="Xóa", command=xoa_truong_phuong_trinh)
xoa_button.pack()

reset_button = tk.Button(cua_so, text="Reset", command=reset_fields)
reset_button.pack()

Ve_do_thi_mien_t_button = tk.Button(cua_so, text="Vẽ đồ thị miền thời gian", command=ve_do_thi_mien_thoi_gian)
Ve_do_thi_mien_t_button.pack()

Ve_do_thi_mien_f_button = tk.Button(cua_so, text="Vẽ đồ thị miền tần số", command=ve_do_thi_mien_tan_so)
Ve_do_thi_mien_f_button.pack()

Loc_va_ve_do_thi_button = tk.Button(cua_so, text="Lọc và vẽ đồ thị", command=loc_va_ve_do_thi)
Loc_va_ve_do_thi_button.pack()

# Chạy chương trình
cua_so.mainloop()