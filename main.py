import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # cài: python -m pip install pillow
import os
from db import connect_db  

# Import các tab chức năng
import tivi_tab
import nhanvien_tab
import khachhang_tab
import tonkho_tab
import banhang_tab
import hoadon_tab

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- CÀI ĐẶT MÀU SẮC (Cho Giao diện chính) ---
        self.sidebar_bg = "#343a40"
        self.button_bg = "#007bff"
        self.fg_color = "white"
        self.main_bg = "#f4f4f4"

        
        # Tạo giao diện đăng nhập đầu tiên
        self._create_login_ui()

    def _create_login_ui(self):
        ## Tạo giao diện đăng nhập
        self.title("Đăng nhập - Quản lý cửa hàng tivi")
        self.attributes('-fullscreen', True) # Fullscreen
        self.resizable(False, False)

        # Đường dẫn cơ sở để tải ảnh
        base_path = os.path.dirname(__file__)

        # --- Ảnh nền ---
        try:
            bg_img_path = os.path.join(base_path, "anhgiaodien", "dienmayxanh_background.jpg")
            bg_image = Image.open(bg_img_path)
            
            # Lấy kích thước màn hình để resize ảnh nền
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
            
            self.bg_photo = ImageTk.PhotoImage(bg_image) # Lưu lại tham chiếu
            
            self.bg_label = tk.Label(self, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Lỗi tải ảnh nền: {e}. Dùng nền trơn.")
            self.config(bg="#F0F0F0")

        # --- 2. Khung đăng nhập ---
        self.login_frame = tk.Frame(self, bg="white", relief="solid", bd=1)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=400)

        # --- 3. Logo ---
        try:
            logo_img_path = os.path.join(base_path, "anhgiaodien", "logodienmayxanh.jpg")
            logo_image = Image.open(logo_img_path)
            logo_image = logo_image.resize((100, 100), Image.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image) # Lưu lại tham chiếu
            
            logo_label = tk.Label(self.login_frame, image=self.logo_photo, bg="white")
            logo_label.pack(pady=(20, 10))
        except Exception as e:
            print(f"Lỗi tải logo: {e}")
            logo_label = tk.Label(self.login_frame, text="Logo", bg="white")
            logo_label.pack(pady=(20, 10))

        # --- Tiêu đề  ---
        title_label = tk.Label(self.login_frame, text="QUẢN LÝ CỬA HÀNG TIVI", 
                               font=("Arial", 16, "bold"), bg="white", fg="#007bff")
        title_label.pack(pady=10)

        # --- Form nhập liệu ---
        user_label = tk.Label(self.login_frame, text="Tên người dùng", font=("Arial", 12), bg="white")
        user_label.pack(pady=(10, 5))

        # Lưu entry vào 'self' để _check_login có thể truy cập
        self.entry_user = tk.Entry(self.login_frame, font=("Arial", 12), width=30)
        self.entry_user.pack()

        pass_label = tk.Label(self.login_frame, text="Mật khẩu", font=("Arial", 12), bg="white")
        pass_label.pack(pady=(10, 5))

        self.entry_pass = tk.Entry(self.login_frame, font=("Arial", 12), width=30, show="*")
        self.entry_pass.pack()

        # --- Nút Đăng nhập ---
        login_button = tk.Button(self.login_frame, text="Đăng nhập", font=("Arial", 12, "bold"), 
                                 width=28, command=self._check_login, bg="#000000", fg="white")
        login_button.pack(pady=20)
        
        # Gán phím Enter để đăng nhập
        self.bind('<Return>', self._check_login_event)
        
        

    def _check_login_event(self, event):
        # Xử lý sự kiện nhấn Enter
        self._check_login()

    def _check_login(self):
        # Lấy thông tin đăng nhập
        username = self.entry_user.get()
        password = self.entry_pass.get()

        conn = None
        try:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)
            # Kiểm tra trong bảng 'nhanvien'
            query = "SELECT ho_ten FROM nhanvien WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

            if user:
                # ĐĂNG NHẬP THÀNH CÔNG 
                messagebox.showinfo("Thành công", f"Chào mừng {user['ho_ten']}!")
                # Xóa UI đăng nhập và xây dựng Giao diện chính
                self._build_main_app()
            else:
                messagebox.showerror("Lỗi Đăng Nhập", "Tên người dùng hoặc mật khẩu không đúng!")
        
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể kiểm tra đăng nhập.\nLỗi: {e}\nĐảm bảo CSDL đang chạy và bảng 'nhanvien' có cột 'username', 'password'.")
        finally:
            if conn:
                conn.close()

    def _build_main_app(self):
        #  Xóa giao diện đăng nhập
        
        self.unbind('<Return>') # Hủy gán phím Enter
        if hasattr(self, 'bg_label'): # Xóa ảnh nền
            self.bg_label.destroy()
        self.login_frame.destroy() # Xóa khung trắng

        #  Cấu hình lại cửa sổ cho Giao diện chính
        self.title("Hệ Thống Quản Lý Cửa Hàng Tivi NK")
        self.attributes('-fullscreen', True)
        self.resizable(True, True)
        self.minsize(900, 600)

        #  Vẽ Giao diện chính với sidebar và khung chính
        self._create_sidebar()
        self._create_main_frame()
        
        # Hiển thị trang chủ mặc định
        self.show_trangchu_view()

    
    
    def _create_sidebar(self):
        # Tạo khung sidebar bên trái
        self.sidebar_frame = tk.Frame(self, bg=self.sidebar_bg, width=220)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)

        tk.Label(self.sidebar_frame, text="Chào sếp ạ!",
                 font=("Arial", 16, "bold"),
                 bg=self.sidebar_bg, fg=self.fg_color).pack(pady=20, padx=10)

        # Các nút điều hướng
        buttons_info = [
            ("Trang chủ", self.show_trangchu_view),
            ("Bán Hàng", self.show_banhang_view),
            ("Quản lý Hóa đơn", self.show_hoadon_view),
            ("Quản lý Tivi", self.show_tivi_view),
            ("Quản lý Nhân viên", self.show_nhanvien_view),
            ("Quản lý Khách hàng", self.show_khachhang_view),
            ("Quản lý Tồn kho", self.show_tonkho_view),
        ]

        for text, command in buttons_info:
            btn = tk.Button(
                self.sidebar_frame, text=text, bg=self.button_bg, fg=self.fg_color,
                font=("Arial", 12, "bold"), relief="flat", anchor="w",
                padx=20, pady=10, command=command
            )
            btn.pack(fill="x", pady=5, padx=10)

        # Nút Đăng xuất
        logout_btn = tk.Button(
            self.sidebar_frame, text="Đăng xuất", bg="#dc3545", fg=self.fg_color,
            font=("Arial", 12, "bold"), relief="flat", anchor="center",
            padx=20, pady=10, command=self.on_logout
        )
        logout_btn.pack(side="bottom", fill="x", pady=20, padx=10)

    def _create_main_frame(self):
        # Tạo khung chính bên phải để hiển thị nội dung
        self.main_frame = tk.Frame(self, bg=self.main_bg)
        self.main_frame.pack(side="right", fill="both", expand=True)

    def clear_main_frame(self):
        # Xóa hết widget trong khung chính
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # --- CÁC HÀM CHUYỂN ĐỔI VIEW ---

    def show_trangchu_view(self):
        self.clear_main_frame()
        tk.Label(self.main_frame, text="TRANG CHỦ",
                 font=("Arial", 40, "bold"), bg=self.main_bg,
                 fg="#333").pack(expand=True)
        tk.Label(self.main_frame, text="Chào mừng đến với hệ thống quản lý cửa hàng tivi NK!",
                 font=("Arial", 30), bg=self.main_bg).pack(expand=True)
    def show_banhang_view(self):
        self.clear_main_frame()
        banhang_tab.create_view(self.main_frame)

    def show_hoadon_view(self):
        self.clear_main_frame()
        hoadon_tab.create_view(self.main_frame)

    def show_tivi_view(self):
        self.clear_main_frame()
        tivi_tab.create_view(self.main_frame)

    def show_nhanvien_view(self):
        self.clear_main_frame()
        nhanvien_tab.create_view(self.main_frame)

    def show_khachhang_view(self):
        self.clear_main_frame()
        khachhang_tab.create_view(self.main_frame)

    def show_tonkho_view(self):
        self.clear_main_frame()
        tonkho_tab.create_view(self.main_frame)

    def on_logout(self):
        # Xử lý đăng xuất
        if messagebox.askyesno("Đăng xuất", "Bạn có chắc muốn đăng xuất?"):
            self.destroy()

#  ĐIỂM KHỞI CHẠY CHÍNH CỦA ỨNG DỤNG 
if __name__ == "__main__":
    # Khởi tạo App.
    
    app = App()
    app.mainloop()