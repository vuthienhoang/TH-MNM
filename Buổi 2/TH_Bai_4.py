import tkinter as tk
import pandas as pd
from numpy import array
import matplotlib.pyplot as plt
import numpy as np
from tkinter import messagebox

df = pd.read_csv('diemPython.csv', index_col=0, header=0)
in_data = array(df.iloc[:, :])
def read_text_file():
    # Tạo một cửa sổ mới để hiển thị dữ liệu
    new_window = tk.Toplevel(window)
    new_window.title('Dữ liệu từ tệp văn bản')
    text_widget = tk.Text(new_window)
    text_widget.insert(tk.END, in_data)
    text_widget.pack()
def tong_SV_di_thi():
    new_window = tk.Toplevel(window)
    new_window.title('Tong so sinh vien di thi :')
    tongsv = in_data[:, 1]
    Tong = np.sum(tongsv)
    label = tk.Label(new_window, text=f"Tổng số sinh viên tham gia thi: {Tong}")
    label.pack()

def diem_A():
    new_window = tk.Toplevel(window)
    new_window.title('Du lieu ve sl diem A :')
    diemA = in_data[:, 3]
    diemBc = in_data[:, 4]
    maxa = diemA.max()
    indexes = np.where(diemA == maxa)
    lop_nhieu_diem_A = [in_data[i, 0] for i in indexes]
    label = tk.Label(new_window, text=f"lop co nhieu diem A la: {lop_nhieu_diem_A}")
    label.pack()

    plt.plot(range(len(diemA)), diemA, 'r-', label="Diem A")
    plt.plot(range(len(diemBc)), diemBc, 'g-', label="Diem B +")
    plt.xlabel('Lơp')
    plt.ylabel(' So sv dat diem ')
    plt.legend(loc='upper right')
    plt.show()


window = tk.Tk()
window.title('Giao diện Python')
window.geometry('600x600')

button = tk.Button(window, text='Hiển thị dữ liệu', command=read_text_file)
button.grid(column=1, row=0)


button2 = tk.Button(window, text='Tổng sinh viên đi thi', command=tong_SV_di_thi)
button2.grid(column=2, row=0)

button3 = tk.Button(window, text='DL diem A', command=diem_A)
button3.grid(column=3, row=0)


window.mainloop()
