import tkinter as tk
from tkinter import ttk, messagebox
from db import connect_db

def create_view(parent_frame):
    
    # --- Màu sắc ---
    bg_color = "#f4f4f4" # Màu nền chính
    btn_add_bg = "#28a745"   # Màu nút Thêm
    btn_edit_bg = "#007bff"  # Màu nút Sửa
    btn_save_bg = "#ffc107"  # Màu nút Lưu
    btn_del_bg = "#dc3545"   # Màu nút Xóa
    btn_clear_bg = "#6c757d" # Màu nút Huỷ
    btn_fg_white = "white" # Màu chữ trắng
    btn_fg_black = "black"    # Màu chữ đen

    # --- Tiêu đề ---
    tk.Label(parent_frame, text="QUẢN LÝ TIVI TRƯNG BÀY", 
             font=("Arial", 18, "bold"), 
             bg=bg_color, fg="#333").pack(pady=10)

    # --- Khung nhập dữ liệu ---
    frm_input = tk.LabelFrame(parent_frame, text="Thông tin Tivi", 
                                  padx=10, pady=10, bg=bg_color, 
                                  font=("Arial", 11))
    frm_input.pack(padx=10, pady=5, fill="x")
    # Entry ẩn để chứa ma_tivi khi chọn
    tk.Label(frm_input, text="Tên Tivi:", bg=bg_color, font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_ten = tk.Entry(frm_input, width=30, font=("Arial", 10))
    entry_ten.grid(row=0, column=1, padx=5, pady=5)
     
    tk.Label(frm_input, text="Hãng SX:", bg=bg_color, font=("Arial", 10)).grid(row=0, column=2, padx=5, pady=5, sticky="w")
    combo_hang = ttk.Combobox(frm_input, width=28, state="readonly", font=("Arial", 10))
    combo_hang['values'] = ("Samsung", "LG", "Sony", "TCL", "Panasonic", "Sharp", "Asanzo")
    combo_hang.current(0)
    combo_hang.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(frm_input, text="Kích thước:", bg=bg_color, font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_kichthuoc = tk.Entry(frm_input, width=30, font=("Arial", 10))
    entry_kichthuoc.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frm_input, text="Giá (VNĐ):", bg=bg_color, font=("Arial", 10)).grid(row=1, column=2, padx=5, pady=5, sticky="w")
    entry_gia = tk.Entry(frm_input, width=30, font=("Arial", 10))
    entry_gia.grid(row=1, column=3, padx=5, pady=5)

    tk.Label(frm_input, text="Số lượng:", bg=bg_color, font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_sl = tk.Entry(frm_input, width=30, font=("Arial", 10))
    entry_sl.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frm_input, text="Bảo hành:", bg=bg_color, font=("Arial", 10)).grid(row=2, column=2, padx=5, pady=5, sticky="w")
    entry_bh = tk.Entry(frm_input, width=30, font=("Arial", 10))
    entry_bh.grid(row=2, column=3, padx=5, pady=5)
    
    # Căn chỉnh 2 cột trong grid
    frm_input.grid_columnconfigure(1, weight=1)
    frm_input.grid_columnconfigure(3, weight=1)

    # --- Khung nút bấm ---
    frame_btn_bottom = tk.Frame(parent_frame, bg=bg_color)
    frame_btn_bottom.pack(side="bottom", fill="x", padx=10, pady=10)

    # --- Khung Treeview ---
    frame_tree = tk.Frame(parent_frame)
    frame_tree.pack(padx=10, pady=10, fill="both", expand=True)
    
    # --- Treeview ---
    cols = ("ma_tivi", "ten_tivi", "hang_sx", "kich_thuoc", "gia", "so_luong", "bao_hanh")
    tree = ttk.Treeview(frame_tree, columns=cols, show="headings", height=10)

    # Định nghĩa tiêu đề và độ rộng cột
    tree.heading("ma_tivi", text="ID")
    tree.heading("ten_tivi", text="Tên Tivi")
    tree.heading("hang_sx", text="Hãng SX")
    tree.heading("kich_thuoc", text="Kích Thước")
    tree.heading("gia", text="Giá (VNĐ)")
    tree.heading("so_luong", text="Số Lượng")
    tree.heading("bao_hanh", text="Bảo Hành")
    # Định nghĩa độ rộng cột
    tree.column("ma_tivi", width=50, stretch=tk.NO, anchor="center")
    tree.column("ten_tivi", width=250,anchor="center") 
    tree.column("hang_sx", width=100, anchor="center")
    tree.column("kich_thuoc", width=100, anchor="center")
    tree.column("gia", width=120, anchor="center") 
    tree.column("so_luong", width=80, anchor="center")
    tree.column("bao_hanh", width=100, anchor="center")
    # --- Thanh cuộn dọc ---
    scroll_y = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    # --- Các hàm xử lý ---
    def load_data():
        # Tải dữ liệu từ CSDL lên Treeview
        tree.delete(*tree.get_children())
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("""
                SELECT ma_tivi, ten_tivi, hang_sx, kich_thuoc, gia, so_luong, bao_hanh 
                FROM tivi 
                ORDER BY ma_tivi ASC
            """)
            for row in cur.fetchall():
                # Định dạng số tiền và số lượng
                formatted_row = (
                    row[0], row[1], row[2], row[3],
                    f"{row[4]:,.0f}",  # Định dạng tiền tệ
                    f"{row[5]:,}",     # Định dạng số lượng
                    row[6]
                )
                tree.insert("", tk.END, values=formatted_row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}")

    
    def _clear_entries():
        # Xóa nội dung các trường nhập liệu
        entry_ten.delete(0, tk.END)
        entry_kichthuoc.delete(0, tk.END)
        entry_gia.delete(0, tk.END)
        entry_sl.delete(0, tk.END)
        entry_bh.delete(0, tk.END)
        combo_hang.current(0)

    def clear_form():
        # Xóa form và bỏ chọn trên Treeview
        _clear_entries()
        if tree.selection():
            tree.selection_remove(tree.selection())

    def on_tree_select(event=None):
        """Hàm "Chọn": được gọi khi click vào Treeview hoặc nút Sửa"""
        sel = tree.selection()
        if not sel:
            if event is None: 
                messagebox.showwarning("Chưa chọn", "Vui lòng chọn Tivi trên bảng!")
            return 
        
        _clear_entries() 
        # Lấy dữ liệu Tivi đã chọn
        item = tree.item(sel[0])
        values = item["values"]
        
        # Điền dữ liệu vào form
        entry_ten.insert(0, values[1])
        combo_hang.set(values[2])
        entry_kichthuoc.insert(0, values[3])
        # Xóa dấu phẩy khi điền lại form
        entry_gia.insert(0, str(values[4]).replace(",", "")) 
        entry_sl.insert(0, str(values[5]).replace(",", ""))
        entry_bh.insert(0, values[6])

    def sua():
        # Gọi hàm chọn khi nhấn nút Sửa
        on_tree_select(event=None)
    

    def get_form_data():
        # Lấy và xác thực dữ liệu từ form
        ten_tivi = entry_ten.get().strip()
        hang_sx = combo_hang.get().strip()
        kich_thuoc = entry_kichthuoc.get().strip()
        # Xử lý số có dấu phẩy
        gia_str = entry_gia.get().strip().replace(",", "")
        so_luong_str = entry_sl.get().strip().replace(",", "")
        bao_hanh = entry_bh.get().strip()

        if not ten_tivi or not hang_sx or not kich_thuoc or not gia_str or not so_luong_str:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin (trừ Bảo hành)!")
            return None
        try:
            gia = float(gia_str)
            so_luong = int(so_luong_str)
            if gia < 0 or so_luong < 0:
                raise ValueError("Giá và số lượng phải là số không âm")
        except ValueError as e:
            messagebox.showerror("Lỗi dữ liệu", f"Giá và Số lượng phải là số hợp lệ! \n{e}")
            return None
        
        return (ten_tivi, hang_sx, kich_thuoc, gia, so_luong, bao_hanh)

    def them():
        # Thêm Tivi mới
        data = get_form_data()
        if data is None:
            return

        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO tivi (ten_tivi, hang_sx, kich_thuoc, gia, so_luong, bao_hanh)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, data)
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm Tivi mới!")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Lỗi SQL", str(e))
        finally:
            conn.close()
        load_data()
        clear_form() 

    def luu(): 
        # Lưu thay đổi cho Tivi đã chọn
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn Tivi để sửa!")
            return

        ma_tivi_can_sua = tree.item(sel[0])["values"][0]
        data = get_form_data()
        if data is None:
            return

        full_data = data + (ma_tivi_can_sua,) # Thêm mã Tivi vào cuối tuple
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE tivi 
                SET ten_tivi=%s, hang_sx=%s, kich_thuoc=%s, gia=%s, so_luong=%s, bao_hanh=%s
                WHERE ma_tivi=%s
            """, full_data)
            conn.commit()
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin Tivi!")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Lỗi SQL", str(e))
        finally:
            conn.close()
        load_data()
        clear_form() 

    def xoa():
        # Xóa Tivi đã chọn (với xử lý lỗi Khóa ngoại)
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn Tivi để xóa!")
            return

        ma = tree.item(sel[0])["values"][0] 
        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa Tivi (ID: {ma})?"):
            return

        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM tivi WHERE ma_tivi=%s", (ma,))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã xóa Tivi!")
            
        except Exception as e:
            conn.rollback()
            # --- BẮT LỖI KHÓA NGOẠI ---
            if e.args and e.args[0] == 1451: 
                messagebox.showerror(
                    "Không thể xóa", 
                    "Không thể xóa Tivi này vì đã có lịch sử bán hàng (tồn tại trong hóa đơn).\n\n"
                    "Bạn chỉ có thể xóa các Tivi chưa từng được bán."
                )
            else:
                # Báo các lỗi SQL khác
                messagebox.showerror("Lỗi SQL", f"Không thể xóa: {e}")
            # --- KẾT THÚC THAY ĐỔI ---
        finally:
            if conn:
                conn.close()
                
        load_data()
        clear_form() 

    # Gán sự kiện click vào Treeview
    tree.bind("<<TreeviewSelect>>", on_tree_select)
    
    
    # --- Các nút bấm  ---
    btn_them = tk.Button(frame_btn_bottom, text="Thêm", command=them, 
                         width=12, bg=btn_add_bg, fg=btn_fg_white, 
                         font=("Arial", 11, "bold"), height=2)
    btn_them.pack(side="left", padx=5)
    
    btn_sua = tk.Button(frame_btn_bottom, text="Sửa (Chọn)", command=sua, 
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
    
    # Tải dữ liệu ban đầu
    load_data()
    clear_form()