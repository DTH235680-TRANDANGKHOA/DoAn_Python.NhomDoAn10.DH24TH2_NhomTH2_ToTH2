import tkinter as tk 
from tkinter import ttk, messagebox # Thư viện giao diện để thông báo/lỗi
from db import connect_db # Kết nối CSDL

def create_view(parent_frame): # Tạo giao diện quản lý hóa đơn
    frame = tk.Frame(parent_frame, bg="#f4f4f4") # Màu nền khung chính
    frame.pack(fill="both", expand=True) # Đặt khung chính để chiếm toàn bộ không gian

    tk.Label(frame, text="QUẢN LÝ HÓA ĐƠN", font=("Arial", 20, "bold"), bg="#f4f4f4").pack(pady=20) # Tiêu đề

    # --- Frame chứa 2 TreeView ---
    main_view_frame = tk.Frame(frame, bg="#f4f4f4")
    main_view_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # ---  Danh sách Hóa đơn  ---
    hoadon_frame = tk.LabelFrame(main_view_frame, text="Danh sách Hóa đơn", padx=10, pady=10)
    hoadon_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
    #-- TreeView Hóa đơn ---
    hoadon_cols = ('ma_hd', 'ngay_lap', 'nhan_vien', 'khach_hang', 'tong_tien')
    hoadon_tree = ttk.Treeview(hoadon_frame, columns=hoadon_cols, show='headings', height=20)
    # Định nghĩa cột
    hoadon_tree.heading('ma_hd', text='Mã HĐ')
    hoadon_tree.heading('ngay_lap', text='Ngày lập')
    hoadon_tree.heading('nhan_vien', text='Nhân viên')
    hoadon_tree.heading('khach_hang', text='Khách hàng')
    hoadon_tree.heading('tong_tien', text='Tổng tiền')
    # Định nghĩa kích thước cột
    hoadon_tree.column('ma_hd', width=60, anchor="center")
    hoadon_tree.column('ngay_lap', width=100,anchor="center")
    hoadon_tree.column('nhan_vien', width=150,anchor="center")
    hoadon_tree.column('khach_hang', width=150,anchor="center")
    hoadon_tree.column('tong_tien', width=100, anchor="center")
    # Đặt TreeView vào frame
    hoadon_tree.pack(fill="both", expand=True)

    # ---  Chi tiết Hóa đơn  ---
    chitiet_frame = tk.LabelFrame(main_view_frame, text="Chi tiết Hóa đơn", padx=10, pady=10)
    chitiet_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
    #-- TreeView Chi tiết Hóa đơn ---
    chitiet_cols = ('ten_tivi', 'so_luong', 'don_gia')
    chitiet_tree = ttk.Treeview(chitiet_frame, columns=chitiet_cols, show='headings', height=20)
    # Định nghĩa cột
    chitiet_tree.heading('ten_tivi', text='Tên Tivi')
    chitiet_tree.heading('so_luong', text='Số lượng')
    chitiet_tree.heading('don_gia', text='Đơn giá')
    # Định nghĩa kích thước cột
    chitiet_tree.column('ten_tivi', width=200,anchor="center")
    chitiet_tree.column('so_luong', width=80, anchor="center")
    chitiet_tree.column('don_gia', width=100, anchor="center")
    # Đặt TreeView vào frame
    chitiet_tree.pack(fill="both", expand=True)

    # --- Các hàm xử lý ---
    
    def load_hoadon_data():
        # Tải dữ liệu hóa đơn từ CSDL vào TreeView
        for item in hoadon_tree.get_children():
            hoadon_tree.delete(item)
        
        try:
            conn = connect_db()
            cursor = conn.cursor()
            
            query = """
                SELECT hd.ma_hd, hd.ngay_lap, nv.ho_ten, kh.ho_ten, hd.tong_tien
                FROM hoadon hd
                JOIN nhanvien nv ON hd.ma_nv = nv.ma_nv
                JOIN khachhang kh ON hd.ma_kh = kh.ma_kh
                ORDER BY hd.ngay_lap DESC, hd.ma_hd DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                # Format lại tiền tệ và ngày tháng 
                formatted_row = (row[0], row[1], row[2], row[3], f"{row[4]:,.0f} VNĐ")
                hoadon_tree.insert('', 'end', values=formatted_row)
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải danh sách hóa đơn: {e}")
        finally:
            if conn:
                conn.close()

    def show_chitiet_data(event):
        # Hiển thị chi tiết hóa đơn khi chọn một hóa đơn
        for item in chitiet_tree.get_children():
            chitiet_tree.delete(item)
            
        selected_item = hoadon_tree.focus()
        if not selected_item:
            return
            
        values = hoadon_tree.item(selected_item, 'values')
        ma_hd = values[0] # Lấy mã hóa đơn từ cột đầu tiên

        try:
            conn = connect_db()
            cursor = conn.cursor()
            # Dùng JOIN để lấy tên Tivi
            query = """
                SELECT tv.ten_tivi, cthd.so_luong_mua, cthd.don_gia
                FROM chitiet_hoadon cthd
                JOIN tivi tv ON cthd.ma_tivi = tv.ma_tivi
                WHERE cthd.ma_hd = %s
            """
            cursor.execute(query, (ma_hd,))
            rows = cursor.fetchall()
            for row in rows:
                formatted_row = (row[0], row[1], f"{row[2]:,.0f} VNĐ")
                chitiet_tree.insert('', 'end', values=formatted_row)
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải chi tiết hóa đơn: {e}")
        finally:
            if conn:
                conn.close()

    # Gán sự kiện click (chọn) vào TreeView hóa đơn
    hoadon_tree.bind('<<TreeviewSelect>>', show_chitiet_data)

    # Nút Tải lại dữ liệu
    refresh_btn = tk.Button(frame, text="Tải lại danh sách", command=load_hoadon_data)
    refresh_btn.pack(pady=10)

    # Tải dữ liệu lần đầu khi mở tab
    load_hoadon_data()