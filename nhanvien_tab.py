import tkinter as tk
from tkinter import ttk, messagebox
from db import connect_db

def create_view(parent_frame):
    
    # --- Màu sắc ---
    bg_color = "#f4f4f4" # Màu nền
    btn_add_bg = "#28a745" # Màu nút Thêm
    btn_edit_bg = "#007bff" # Màu nút Sửa
    btn_save_bg = "#ffc107" # Màu nút Lưu
    btn_del_bg = "#dc3545" # Màu nút Xóa
    btn_clear_bg = "#6c757d" # Màu nút Huỷ
    btn_fg_white = "white" # Màu chữ trắng
    btn_fg_black = "black"  # Màu chữ đen

    # --- Tiêu đề ---
    tk.Label(parent_frame, text="QUẢN LÝ NHÂN VIÊN", 
             font=("Arial", 18, "bold"), 
             bg=bg_color, fg="#333").pack(pady=10)

    # --- Khung nhập liệu ---
    frm_input = tk.LabelFrame(parent_frame, text="Thông tin nhân viên", 
                                  padx=10, pady=10, bg=bg_color,
                                  font=("Arial", 11))
    frm_input.pack(padx=10, pady=5, fill="x")

    
    # Entry ẩn để chứa ma_nv khi chọn (dùng cho hàm luu())
    entry_ma = tk.Entry(frm_input)

    
    # --- Hàng 1 ---
    tk.Label(frm_input, text="Họ tên:", bg=bg_color, font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_ten = tk.Entry(frm_input, width=30, font=("Arial", 10))
    entry_ten.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frm_input, text="Chức vụ:", bg=bg_color, font=("Arial", 10)).grid(row=0, column=2, padx=5, pady=5, sticky="w")
    combo_chucvu = ttk.Combobox(frm_input, width=28, state="readonly", font=("Arial", 10),
        values=["Quản lý", "Thu ngân", "Bán hàng", "Kỹ thuật viên", "Bảo vệ", "Lễ tân", "Giao hàng"])
    combo_chucvu.grid(row=0, column=3, padx=5, pady=5)
    combo_chucvu.current(0)

    # --- Hàng 2 ---
    tk.Label(frm_input, text="Lương (VNĐ):", bg=bg_color, font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_luong = tk.Entry(frm_input, width=30, font=("Arial", 10))
    entry_luong.grid(row=1, column=1, padx=5, pady=5)
    
    frm_input.grid_columnconfigure(1, weight=1)
    frm_input.grid_columnconfigure(3, weight=1)

    # --- Khung nút ở dưới cùng ---
    frame_btn_bottom = tk.Frame(parent_frame, bg=bg_color)
    frame_btn_bottom.pack(side="bottom", fill="x", padx=10, pady=10)

    # --- Khung Treeview ---
    frame_tree = tk.Frame(parent_frame)
    frame_tree.pack(padx=10, pady=10, fill="both", expand=True)
    #-- Treeview và cột ---
    cols = ("ma_nv", "ho_ten", "chuc_vu", "luong")
    tree = ttk.Treeview(frame_tree, columns=cols, show="headings", height=12)
    #-- Định nghĩa tiêu đề cột ---
    tree.heading("ma_nv", text="Mã NV")
    tree.heading("ho_ten", text="Họ tên")
    tree.heading("chuc_vu", text="Chức vụ")
    tree.heading("luong", text="Lương (VNĐ)")
    #-- Định nghĩa độ rộng cột ---
    tree.column("ma_nv", width=80, anchor="center")
    tree.column("ho_ten", width=180,anchor="center") 
    tree.column("chuc_vu", width=150, anchor="center")
    tree.column("luong", width=120, anchor="center") 
    #-- Thêm thanh cuộn dọc ---
    scroll_y = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    # --- Các hàm xử lý ---
    def load_data():
        ## Tải dữ liệu từ CSDL vào Treeview
        tree.delete(*tree.get_children()) # Xóa dữ liệu cũ
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("SELECT ma_nv, ho_ten, chuc_vu, luong FROM nhanvien ORDER BY ma_nv ASC")
            for row in cur.fetchall():
                # Định dạng Lương (thêm , và VNĐ)
                formatted_row = (row[0], row[1], row[2], f"{row[3]:,.0f} VNĐ")
                tree.insert("", tk.END, values=formatted_row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}")

    
    def _clear_entries():
        # Xóa nội dung các trường nhập liệu
        entry_ma.delete(0, tk.END) 
        entry_ten.delete(0, tk.END)
        entry_luong.delete(0, tk.END)
        combo_chucvu.current(0)
        
    def clear_form():
        # Xóa form và bỏ chọn trên Treeview
        _clear_entries()
        if tree.selection():
            tree.selection_remove(tree.selection())

    def on_tree_select(event=None): 
        """Xử lý khi chọn một hàng trên Treeview"""
        selected = tree.selection()
        if not selected:
            if event is None: # Chỉ cảnh báo khi bấm nút "Sửa"
                messagebox.showwarning("Chưa chọn", "Vui lòng chọn nhân viên trên bảng!")
            return
        
        # Xóa form trước khi điền
        _clear_entries()
        
        vals = tree.item(selected[0])["values"]
        
        entry_ma.insert(0, vals[0])
        entry_ten.insert(0, vals[1])
        combo_chucvu.set(vals[2])
        
        # Bỏ định dạng "VNĐ" và "," khi điền vào form
        luong_str = str(vals[3]).replace(",", "").replace(" VNĐ", "")
        entry_luong.insert(0, luong_str)

    def get_form_data():
        # Lấy và xác thực dữ liệu từ form
        ho_ten = entry_ten.get().strip()
        chuc_vu = combo_chucvu.get().strip()
        luong_str = entry_luong.get().strip().replace(",", "") # Bỏ dấu phẩy nếu người dùng nhập

        if not ho_ten or not chuc_vu or not luong_str:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
            return None
        try:
            luong = float(luong_str)
            if luong < 0: raise ValueError("Lương phải là số không âm")
        except ValueError as e:
            messagebox.showerror("Lỗi dữ liệu", f"Lương phải là số hợp lệ! \n{e}")
            return None
        return (ho_ten, chuc_vu, luong)

    def them():
        # Thêm nhân viên mới
        data = get_form_data()
        if data is None:
            return

        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO nhanvien (ho_ten, chuc_vu, luong) VALUES (%s,%s,%s)",
                data
            )
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm nhân viên mới!")
            clear_form()
            load_data()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Lỗi", f"Không thể thêm dữ liệu: {e}")
        finally:
            conn.close()

    def xoa():
        # Xóa nhân viên (với xử lý lỗi Khóa ngoại)
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn nhân viên để xóa!")
            return
            
        ma_nv = tree.item(selected[0])["values"][0]
        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa nhân viên mã {ma_nv}?"):
            return
            
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM nhanvien WHERE ma_nv=%s", (ma_nv,))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã xóa nhân viên!")
        except Exception as e:
            conn.rollback()
            # --- BẮT LỖI KHÓA NGOẠI ---
            if e.args and e.args[0] == 1451:
                messagebox.showerror(
                    "Không thể xóa", 
                    "Không thể xóa nhân viên này vì đã có lịch sử bán hàng (tồn tại trong hóa đơn).\n\n"
                    "Bạn chỉ có thể xóa nhân viên chưa từng lập hóa đơn."
                )
            else:
                messagebox.showerror("Lỗi SQL", f"Không thể xóa: {e}")
          
        finally:
            conn.close()
        
        clear_form()
        load_data()

    def luu(): 
        # Lưu thay đổi cho nhân viên đã chọn
        ma_nv = entry_ma.get().strip() 
        if not ma_nv:
            messagebox.showwarning("Thiếu mã", "Hãy nhấn 'Sửa' (hoặc nhấp vào bảng) để chọn nhân viên trước!")
            return

        data = get_form_data()
        if data is None:
            return
            
        full_data = data + (ma_nv,) # (ho_ten, chuc_vu, luong, ma_nv)
        
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE nhanvien SET ho_ten=%s, chuc_vu=%s, luong=%s
                WHERE ma_nv=%s
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

    # --- Thêm nút vào frame_btn_bottom  ---
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