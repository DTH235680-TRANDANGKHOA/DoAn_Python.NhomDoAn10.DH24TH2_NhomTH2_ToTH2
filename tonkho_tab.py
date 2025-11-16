import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # Cần cài đặt: pip install tkcalendar
from db import connect_db
import datetime

# Biến toàn cục để lưu danh sách Tivi (ma_tivi, ten_tivi, hang_sx)
tivi_list = []

def create_view(parent_frame):
    global tivi_list

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
    tk.Label(parent_frame, text="QUẢN LÝ TỒN KHO", 
             font=("Arial", 18, "bold"), 
             bg=bg_color, fg="#333").pack(pady=10)
    
    # --- Khung lọc ---
    frm_filter = tk.Frame(parent_frame, bg=bg_color)
    frm_filter.pack(padx=10, pady=5, fill="x")
    # --- Lọc theo hãng ---
    tk.Label(frm_filter, text="Lọc theo hãng:", bg=bg_color, font=("Arial", 10, "bold")).pack(side="left", padx=(0, 5))
    combo_filter = ttk.Combobox(
        frm_filter, state="readonly", font=("Arial", 10),
        values=["Tất cả", "Samsung", "LG", "Sony", "TCL", "Panasonic", "Sharp", "Asanzo"],
        width=20
    )
    combo_filter.current(0)
    combo_filter.pack(side="left", padx=5)

    # --- Khung nhập liệu ---
    frm_input = tk.LabelFrame(parent_frame, text="Thông tin cập nhật tồn kho", 
                                  padx=10, pady=10, bg=bg_color,
                                  font=("Arial", 11))
    frm_input.pack(padx=10, pady=5, fill="x")

   
    tk.Label(frm_input, text="Chọn Tivi:", bg=bg_color, font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
    combo_tivi = ttk.Combobox(frm_input, state="readonly", width=40, font=("Arial", 10))
    combo_tivi.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frm_input, text="Ngày cập nhật:", bg=bg_color, font=("Arial", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
    entry_ngay = DateEntry(frm_input, width=23, font=("Arial", 10), background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
    entry_ngay.grid(row=0, column=3, padx=5, pady=5)

   
    
    tk.Label(frm_input, text="Số lượng:", bg=bg_color, font=("Arial", 10)).grid(row=2, column=0, sticky="w", padx=5, pady=5)
    entry_soluong = tk.Entry(frm_input, width=42, font=("Arial", 10))
    entry_soluong.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    


    tk.Label(frm_input, text="Ghi chú:", bg=bg_color, font=("Arial", 10)).grid(row=3, column=0, sticky="w", padx=5, pady=5)
    entry_note = tk.Entry(frm_input, font=("Arial", 10))
    entry_note.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky="we")
    
    frm_input.grid_columnconfigure(1, weight=1)
    frm_input.grid_columnconfigure(3, weight=1)

    # --- Khung nút ở dưới cùng ---
    frame_btn_bottom = tk.Frame(parent_frame, bg=bg_color)
    frame_btn_bottom.pack(side="bottom", fill="x", padx=10, pady=10)

    # --- Khung Treeview ---
    frame_tree = tk.Frame(parent_frame)
    frame_tree.pack(padx=10, pady=10, fill="both", expand=True)

    # --- Cập nhật cột Treeview ---
    columns = ( "ma_ton", "ma_tivi", "ten_tivi", "hang_sx", "ngay_cap_nhat", "so_luong_ton", "ghi_chu")
    tree = ttk.Treeview(frame_tree, columns=columns, show="headings", height=12)
    
    # Định nghĩa cột
    tree.heading("ma_ton", text="ID Log") 
    tree.heading("ma_tivi", text="Mã TV")
    tree.heading("ten_tivi", text="Tên Tivi")
    tree.heading("hang_sx", text="Hãng SX")
    tree.heading("ngay_cap_nhat", text="Ngày Cập Nhật")
    tree.heading("so_luong_ton", text="Số Lượng")
    tree.heading("ghi_chu", text="Ghi Chú")

    #   Định nghĩa độ rộng cột
    tree.column("ma_ton", width=50, anchor="center") 
    tree.column("ma_tivi", width=50, anchor="center")
    tree.column("ten_tivi", width=200, anchor="center")
    tree.column("hang_sx", width=100, anchor="center")
    tree.column("ngay_cap_nhat", width=100, anchor="center")
    tree.column("so_luong_ton", width=80, anchor="center")
    tree.column("ghi_chu", width=250, anchor="center")
    
    # Ẩn 2 cột ID
    tree.column("ma_ton", width=0, stretch=tk.NO) 
    tree.column("ma_tivi", width=0, stretch=tk.NO)
    # Thêm thanh cuộn dọc
    scroll_y = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    # --- Các hàm xử lý  ---
    
    def load_tivi_combobox():
        # Tải danh sách Tivi từ CSDL vào Combobox
        global tivi_list
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("SELECT ma_tivi, ten_tivi, hang_sx FROM tivi ORDER BY ten_tivi")
            tivi_list = cur.fetchall()
            
            combo_tivi['values'] = [f"{row[1]} (Hãng: {row[2]}, ID: {row[0]})" for row in tivi_list]
            if tivi_list:
                combo_tivi.current(0)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách Tivi: {e}")
        finally:
            if conn:
                conn.close()

    def load_data(event=None): 
        # Tải dữ liệu từ CSDL vào Treeview
        tree.delete(*tree.get_children())
        try:
            conn = connect_db()
            cur = conn.cursor()
            hang = combo_filter.get()
            
           
            base_query = """
                SELECT tk.ma_ton, tk.ma_tivi, tv.ten_tivi, tv.hang_sx, 
                       tk.ngay_cap_nhat, tk.so_luong_ton, tk.ghi_chu 
                FROM tonkho tk
                JOIN tivi tv ON tk.ma_tivi = tv.ma_tivi
            """
            
            if hang == "Tất cả":
                cur.execute(base_query + " ORDER BY tk.ngay_cap_nhat DESC, tk.ma_ton DESC")
            else:
                cur.execute(base_query + " WHERE tv.hang_sx=%s ORDER BY tk.ngay_cap_nhat DESC, tk.ma_ton DESC", (hang,))
            
            for row in cur.fetchall():
                
                so_luong_formatted = f"+{row[5]}" if row[5] > 0 else str(row[5])
                formatted_row = (row[0], row[1], row[2], row[3], row[4], so_luong_formatted, row[6])
                tree.insert("", tk.END, values=formatted_row)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}")
        finally:
            if conn:
                conn.close()

    
    def _clear_entries():
        # Xóa nội dung các trường nhập liệu
        if tivi_list:
            combo_tivi.current(0)
        entry_soluong.delete(0, tk.END)
        entry_note.delete(0, tk.END)
        entry_ngay.set_date(datetime.date.today())

    def clear_form():
        # Xóa form và bỏ chọn trên Treeview
        _clear_entries() 
        if tree.selection():
            tree.selection_remove(tree.selection())

    
    def get_form_data():
        #   Lấy và xác thực dữ liệu từ form
        try:
           
            selected_index = combo_tivi.current()
            if selected_index < 0:
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng chọn Tivi")
                return None
            ma_tivi = tivi_list[selected_index][0]
        except IndexError:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng chọn Tivi")
            return None
            
        ngay = entry_ngay.get()
        so_luong_str = entry_soluong.get().strip()
        note = entry_note.get().strip()

        if not so_luong_str:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập Số lượng")
            return None
        try:
            so_luong = int(so_luong_str)
            if so_luong == 0:
                raise ValueError("Số lượng phải khác 0")
        except ValueError as e:
            messagebox.showerror("Lỗi dữ liệu", f"Số lượng phải là số nguyên khác 0!\n{e}")
            return None
        
        return (ma_tivi, ngay, so_luong, note)

    def them():
        #   Thêm bản ghi tồn kho mới
        data = get_form_data()
        if data is None:
            return
        
        # data = (ma_tivi, ngay, so_luong, note)
        
        conn = connect_db()
        cur = conn.cursor()
        try:
            
            cur.execute("INSERT INTO tonkho (ma_tivi, ngay_cap_nhat, so_luong_ton, ghi_chu) VALUES (%s,%s,%s,%s)",
                        (data[0], data[1], data[2], data[3]))
            
            # --- Tự động cập nhật bảng tivi ---
            
            cur.execute("UPDATE tivi SET so_luong = so_luong + %s WHERE ma_tivi = %s", (data[2], data[0]))
            
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã thêm bản ghi tồn kho VÀ cập nhật số lượng Tivi ID: {data[0]}!")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()
        load_data()
        clear_form()

    def xoa():
        #   Xóa bản ghi tồn kho (và hoàn tác số lượng trong kho Tivi)
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Chọn bản ghi cần xóa!")
            return
            
        values = tree.item(sel[0])["values"]
        ma_ton = values[0]
        ma_tivi = values[1]
        
        
        try:
            so_luong_log = int(str(values[5]).replace("+", ""))
        except:
            so_luong_log = 0

        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa bản ghi log {ma_ton}?\n\nCẢNH BÁO: Thao tác này sẽ HOÀN TÁC thay đổi tồn kho (trừ lại {so_luong_log} cái cho Tivi ID {ma_tivi})."):
            return
            
        conn = connect_db()
        cur = conn.cursor()
        try:
            
            cur.execute("DELETE FROM tonkho WHERE ma_ton=%s", (ma_ton,))
            
           
            cur.execute("UPDATE tivi SET so_luong = so_luong - %s WHERE ma_tivi = %s", (so_luong_log, ma_tivi))
            
            conn.commit()
            messagebox.showinfo("Thành công", "Đã xóa bản ghi log VÀ hoàn tác số lượng trong kho Tivi!")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Lỗi", f"Không thể xóa: {e}")
        finally:
            conn.close()
            
        clear_form()
        load_data()

    def on_tree_select(event=None): 
        # Xử lý khi chọn một hàng trên Treeview
        sel = tree.selection()
        if not sel:
            if event is None:
                messagebox.showwarning("Chưa chọn", "Vui lòng chọn bản ghi trên bảng!")
            return
        
        _clear_entries()
        
        vals = tree.item(sel[0])["values"]
        
        
        ma_tivi_can_chon = vals[1]
        
        
        for i, tivi in enumerate(tivi_list):
            if tivi[0] == ma_tivi_can_chon:
                combo_tivi.current(i)
                break
        
        try:
            entry_ngay.set_date(vals[4])
        except:
            entry_ngay.set_date(None)
            
        so_luong_str = str(vals[5]).replace("+", "")
        entry_soluong.insert(0, so_luong_str)
        entry_note.insert(0, vals[6])

    def luu(): 
        #   Lưu thay đổi cho khách hàng đã chọn
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Hãy nhấn 'Sửa' để chọn bản ghi cần lưu!")
            return
        
        
        old_vals = tree.item(sel[0])["values"]
        ma_ton = old_vals[0]
        old_ma_tivi = old_vals[1]
        try:
            old_so_luong = int(str(old_vals[5]).replace("+", ""))
        except:
            old_so_luong = 0

       
        new_data = get_form_data()
        if new_data is None:
            return
        # new_data = (new_ma_tivi, new_ngay, new_so_luong, new_note)
        new_ma_tivi = new_data[0]
        new_ngay = new_data[1]
        new_so_luong = new_data[2]
        new_note = new_data[3]

        if not messagebox.askyesno("Xác nhận Cực kỳ Cẩn trọng!", 
            "Bạn đang sửa một bản ghi LOG. Việc này sẽ:\n"
            "1. Hoàn tác số lượng CŨ (trừ {-old_so_luong} cho Tivi ID {old_ma_tivi})\n"
            "2. Cập nhật số lượng MỚI (cộng {new_so_luong} cho Tivi ID {new_ma_tivi})\n"
            "Bạn có chắc muốn tiếp tục?"):
            return

        conn = connect_db()
        cur = conn.cursor()
        try:
           
            
            #  Hoàn tác số lượng CŨ
            cur.execute("UPDATE tivi SET so_luong = so_luong - %s WHERE ma_tivi = %s", (old_so_luong, old_ma_tivi))
            
            #  Cập nhật bản ghi log
            cur.execute("""UPDATE tonkho 
                           SET ma_tivi=%s, ngay_cap_nhat=%s, so_luong_ton=%s, ghi_chu=%s
                           WHERE ma_ton=%s""",
                        (new_ma_tivi, new_ngay, new_so_luong, new_note, ma_ton))
                        
            #  Cập nhật số lượng MỚI
            cur.execute("UPDATE tivi SET so_luong = so_luong + %s WHERE ma_tivi = %s", (new_so_luong, new_ma_tivi))

            conn.commit()
            messagebox.showinfo("Thành công", "Đã lưu thay đổi VÀ cập nhật cả hai kho Tivi!")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()
            
        load_data()
        clear_form()

    # Kết nối sự kiện
    tree.bind("<<TreeviewSelect>>", on_tree_select)
    combo_filter.bind("<<ComboboxSelected>>", load_data) 

    #--- Nút chức năng ở dưới cùng ---
    btn_them = tk.Button(frame_btn_bottom, text="Thêm (Nhập/Xuất)", command=them, 
                         width=15, bg=btn_add_bg, fg=btn_fg_white, 
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
    
    btn_xoa = tk.Button(frame_btn_bottom, text="Xóa (Hoàn tác)", command=xoa, 
                         width=15, bg=btn_del_bg, fg=btn_fg_white, 
                         font=("Arial", 11, "bold"), height=2)
    btn_xoa.pack(side="left", padx=5)
    
    btn_clear = tk.Button(frame_btn_bottom, text="Huỷ", command=clear_form, 
                          width=12, bg=btn_clear_bg, fg=btn_fg_white, 
                          font=("Arial", 11, "bold"), height=2)
    btn_clear.pack(side="left", padx=5)

    # Tải dữ liệu ban đầu
    load_tivi_combobox() # Tải danh sách Tivi vào Combobox
    load_data()          # Tải Log kho
    clear_form()