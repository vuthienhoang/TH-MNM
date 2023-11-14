import tkinter as tk
from tkinter import ttk, messagebox
import math

class GeometryCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Ung dung hinh hoc")

        self.shape_var = tk.StringVar()
        self.shape_var.set("Square")

        self.create_widgets()

    def create_widgets(self):
        # Combobox to select shape
        shape_label = tk.Label(self.master, text="Select Shape:")
        shape_label.grid(row=0, column=0, pady=10)

        shape_options = ["Hinh vuong", "Hinh chu nhat", "Hinh tron"]
        shape_combobox = ttk.Combobox(self.master, textvariable=self.shape_var, values=shape_options)
        shape_combobox.grid(row=0, column=1, pady=10)
        shape_combobox.bind("<<ComboboxSelected>>", self.update_shape)

        # Entry widgets for dimensions
        self.side_label = tk.Label(self.master, text="Do dai canh:")
        self.side_entry = tk.Entry(self.master)

        self.length_label = tk.Label(self.master, text="Chieu dai:")
        self.length_entry = tk.Entry(self.master)

        self.width_label = tk.Label(self.master, text="Chieu rong:")
        self.width_entry = tk.Entry(self.master)

        self.radius_label = tk.Label(self.master, text="Ban kinh:")
        self.radius_entry = tk.Entry(self.master)

        # Buttons for calculations
        calculate_button = tk.Button(self.master, text="Tinh toan", command=self.calculate)
        calculate_button.grid(row=4, column=0, columnspan=2, pady=10)

        draw_button = tk.Button(self.master, text="Ve hinh", command=self.ve_hinh)
        draw_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Canvas for illustration
        self.canvas = tk.Canvas(self.master, width=200, height=200)
        self.canvas.grid(row=5, column=0, columnspan=2, pady=10)

        # Initial setup
        self.update_shape()

    def update_shape(self, event=None):
        shape = self.shape_var.get()

        self.side_label.grid_forget()
        self.side_entry.grid_forget()
        self.length_label.grid_forget()
        self.length_entry.grid_forget()
        self.width_label.grid_forget()
        self.width_entry.grid_forget()
        self.radius_label.grid_forget()
        self.radius_entry.grid_forget()

        if shape == "Hinh vuong":
            self.side_label.grid(row=1, column=0)
            self.side_entry.grid(row=1, column=1)
        elif shape == "Hinh chu nhat":
            self.length_label.grid(row=1, column=0)
            self.length_entry.grid(row=1, column=1)
            self.width_label.grid(row=2, column=0)
            self.width_entry.grid(row=2, column=1)
        elif shape == "Hinh tron":
            self.radius_label.grid(row=1, column=0)
            self.radius_entry.grid(row=1, column=1)

    def calculate(self):
        shape = self.shape_var.get()

        try:
            if shape == "Hinh vuong":
                side_length = float(self.side_entry.get())
                perimeter = 4 * side_length
                area = side_length ** 2
                self.display_results(perimeter, area)
            elif shape == "Hinh chu nhat":
                length = float(self.length_entry.get())
                width = float(self.width_entry.get())
                perimeter = 2 * (length + width)
                area = length * width
                self.display_results(perimeter, area)
            elif shape == "Hinh tron":
                radius = float(self.radius_entry.get())
                perimeter = 2 * math.pi * radius
                area = math.pi * radius ** 2
                self.display_results(perimeter, area)
        except ValueError:
            messagebox.showerror("Error", "Du lieu vao khong phu hop. Hay nhap gia tri dung.")

    def ve_hinh(self):
        self.canvas.delete("all")  # Xóa mọi nội dung trước khi vẽ hình mới

        shape = self.shape_var.get()
        try:
            if shape == "Hinh vuong":
                side_length = float(self.side_entry.get())
                if side_length > 0:
                    self.canvas.create_rectangle(10, 10, 100 + side_length, 100 + side_length, outline="black")
                else:
                    messagebox.showwarning("Cảnh báo", "Độ dài cạnh phải lớn hơn 0.")


            elif shape == "Hinh chu nhat":
                length = float(self.length_entry.get())
                width = float(self.width_entry.get())
                if length > 0 and width > 0:
                    self.canvas.create_rectangle(10, 10, 100 + length, 100 + width, outline="black")
                else:
                    messagebox.showwarning("Cảnh báo", "Độ dài cạnh phải lớn hơn 0.")

            elif shape == "Hinh tron":
                radius = float(self.radius_entry.get())
                if radius > 0:
                    self.canvas.create_oval(10, 10, 100 + 2 * radius, 100 + 2 * radius, outline="black")
                else:
                    messagebox.showwarning("Cảnh báo", "Độ dài cạnh phải lớn hơn 0.")
        except ValueError:
            messagebox.showerror("Error", "Du lieu vao khong phu hop. Hay nhap gia tri dung.")

    def display_results(self, perimeter, area):
        messagebox.showinfo("Results", f"Perimeter: {perimeter}\nArea: {area}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GeometryCalculator(root)
    root.mainloop()
