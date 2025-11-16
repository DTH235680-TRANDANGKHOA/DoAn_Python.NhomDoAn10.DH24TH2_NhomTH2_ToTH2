import tkinter as tk
from tkinter import ttk, messagebox
from db import connect_db

def create_view(parent_frame):
    
    # --- Màu sắc ---
    bg_color = "#f4f4f4" # Màu nền khung chính
    btn_add_bg = "#28a745" # Màu nút Thêm
    btn_edit_bg = "#007bff" # Màu nút Sửa
    btn_save_bg = "#ffc107" # Màu nút Lưu
    btn_del_bg = "#dc3545" # Màu nút Xóa
    btn_clear_bg = "#6c757d" # Màu nút Huỷ
    btn_fg_white = "white" # Màu chữ nút trắng
    btn_fg_black = "black" # Màu chữ nút đen

    # --- Tiêu đề ---
    tk.Label(parent_frame, text="QUẢN LÝ KHÁCH HÀNG", 
             font=("Arial", 18, "bold"), 
             bg=bg_color, fg="#333").pack(pady=10)

    # --- Khung nhập liệu ---
    frm_input = tk.LabelFrame(parent_frame, text="Thông tin khách hàng", 
                                  padx=10, pady=10, bg=bg_color,
                                  font=("Arial", 11))
    frm_input.pack(padx=10, pady=5, fill="x")

    
    # Entry ẩn để chứa ma_kh khi chọn
    entry_ma = tk.Entry(frm_input)

    tk.Label(frm_input, text="Họ tên:", bg=bg_color, font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_ten = tk.Entry(frm_input, width=30, font=("Arial", 10))
    entry_ten.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frm_input, text="Số điện thoại:", bg=bg_color, font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_sdt = tk.Entry(frm_input, width=30, font=("Arial", 10))
    entry_sdt.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frm_input, text="Địa chỉ:", bg=bg_color, font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_diachi = tk.Entry(frm_input, width=60, font=("Arial", 10))
    entry_diachi.grid(row=2, column=1, padx=5, pady=5, columnspan=3, sticky="we")
    
    frm_input.grid_columnconfigure(1, weight=1)
    

    # --- Khung nút ở dưới cùng ---
    frame_btn_bottom = tk.Frame(parent_frame, bg=bg_color)
    frame_btn_bottom.pack(side="bottom", fill="x", padx=10, pady=10)

    # --- Khung Treeview ---
    frame_tree = tk.Frame(parent_frame)
    frame_tree.pack(padx=10, pady=10, fill="both", expand=True)
    # --- Treeview ---
    columns = ("ma_kh", "ho_ten", "sdt", "dia_chi")
    tree = ttk.Treeview(frame_tree, columns=columns, show="headings", height=10)
    # Định nghĩa cột
    tree.heading("ma_kh", text="Mã KH")
    tree.heading("ho_ten", text="Họ tên")
    tree.heading("sdt", text="Số điện thoại")
    tree.heading("dia_chi", text="Địa chỉ")
    # Định nghĩa độ rộng cột
    tree.column("ma_kh", width=80, anchor="center")
    tree.column("ho_ten", width=180, anchor="center") 
    tree.column("sdt", width=120, anchor="center")
    tree.column("dia_chi", width=250, anchor="center") 
    # Thêm thanh cuộn dọc
    scroll_y = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    # --- Các hàm xử lý ---
    def load_data():
        # Tải dữ liệu từ CSDL vào Treeview
        tree.delete(*tree.get_children())
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("SELECT ma_kh, ho_ten, sdt, dia_chi FROM khachhang ORDER BY ma_kh ASC")
            for row in cur.fetchall():
                tree.insert("", tk.END, values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}")

    def _clear_entries():
        # Xóa nội dung các trường nhập liệu
        entry_ma.delete(0, tk.END)
        entry_ten.delete(0, tk.END)
        entry_sdt.delete(0, tk.END)
        entry_diachi.delete(0, tk.END)
        
    def clear_form():
        # Xóa form và bỏ chọn trên Treeview
        _clear_entries()
        if tree.selection():
            tree.selection_remove(tree.selection())

    def get_form_data():
        #   Lấy và xác thực dữ liệu từ form
        ho_ten = entry_ten.get().strip()
        sdt = entry_sdt.get().strip()
        dia_chi = entry_diachi.get().strip()

        if not ho_ten or not sdt or not dia_chi:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
            return None
        return (ho_ten, sdt, dia_chi)

    def them():
        #   Thêm khách hàng mới
        data = get_form_data()
        if data is None:
            return

        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO khachhang (ho_ten, sdt, dia_chi)
                VALUES (%s, %s, %s)
            """, data)
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm khách hàng mới!")
            clear_form()
            load_data()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Lỗi", f"Không thể thêm dữ liệu: {e}")
        finally:
            conn.close()

    def xoa():
        # Xóa khách hàng (với xử lý lỗi Khóa ngoại)
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Chọn khách hàng để xóa!")
            return
        ma = tree.item(sel[0])["values"][0]
        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa khách hàng mã {ma}?"):
            return
            
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM khachhang WHERE ma_kh=%s", (ma,))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã xóa khách hàng!")
        except Exception as e:
            conn.rollback()
            # --- BẮT LỖI KHÓA NGOẠI ---
            if e.args and e.args[0] == 1451:
                messagebox.showerror(
                    "Không thể xóa", 
                    "Không thể xóa khách hàng này vì đã có lịch sử mua hàng (tồn tại trong hóa đơn).\n\n"
                    "Bạn chỉ có thể xóa khách hàng chưa từng mua hàng."
                )
            else:
                messagebox.showerror("Lỗi SQL", f"Không thể xóa: {e}")
           
        finally:
            conn.close()
            
        clear_form()
        load_data()

    
    def on_tree_select(event=None): 
        # Xử lý khi chọn một hàng trên Treeview
        sel = tree.selection()
        if not sel:
            if event is None: # Chỉ cảnh báo khi bấm nút "Sửa"
                messagebox.showwarning("Chưa chọn", "Vui lòng chọn khách hàng trên bảng!")
            return
        
        _clear_entries()
        
        vals = tree.item(sel[0])["values"]
        
        entry_ma.insert(0, vals[0])
        entry_ten.insert(0, vals[1])
        entry_sdt.insert(0, vals[2])
        entry_diachi.insert(0, vals[3])

    def luu(): 
        # Lưu thay đổi cho khách hàng đã chọn
        ma_kh = entry_ma.get().strip()
        if not ma_kh:
            messagebox.showwarning("Thiếu mã", "Hãy nhấn 'Sửa' (hoặc nhấp vào bảng) để chọn khách hàng trước!")
            return
        
        data = get_form_data()
        if data is None:
            return
            
        full_data = data + (ma_kh,) # (ho_ten, sdt, dia_chi, ma_kh)

        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE khachhang SET ho_ten=%s, sdt=%s, dia_chi=%s
                WHERE ma_kh=%s
            """, full_data)
            conn.commit()
            messagebox.showinfo("Thành công", "Đã lưu thay đổi!")
            clear_form()
            load_data()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Lỗi", f"Không thể cập nhật dữ liệu: {e}")
        finally:
            conn.close()
            
    # Gán sự kiện click vào Treeview
    tree.bind("<<TreeviewSelect>>", on_tree_select) 

    # --- Thêm nút vào frame_btn_bottom ---
    btn_them = tk.Button(frame_btn_bottom, text="Thêm", command=them, 
                         width=12, bg=btn_add_bg, fg=btn_fg_white, 
                         font=("Arial", 11, "bold"), height=2)
    btn_them.pack(side="left", padx=5)
    
    btn_sua = tk.Button(frame_btn_bottom, text="Sửa (Chọn)", command=lambda: on_tree_select(None), 
                         width=12, bg=btn_edit_bg, fg=btn_fg_white, 
                         font=("Arial", 11, "bold"), height=2)
    btn_sua.pack(side="left", padx=5)
    
    btn_luu = tk.Button(frame_btn_bottom, text="Lưu", command=luu, 
                         width=12, bg=btn_save_bg, fg=btn_fg_black, 
                         font=("Arial", 11, "bold"), height=2)
    btn_luu.pack(side="left", padx=5)
    
    btn_xoa = tk.Button(frame_btn_bottom, text="Xóa", command=xoa, 
                         width=12, bg=btn_del_bg, fg=btn_fg_white, 
                         font=("Arial", 11, "bold"), height=2)
    btn_xoa.pack(side="left", padx=5)
    
    btn_clear = tk.Button(frame_btn_bottom, text="Huỷ", command=clear_form, 
                          width=12, bg=btn_clear_bg, fg=btn_fg_white, 
                          font=("Arial", 11, "bold"), height=2)
    btn_clear.pack(side="left", padx=5)

    load_data()