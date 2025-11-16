import tkinter as tk
from tkinter import ttk, messagebox
from db import connect_db
from datetime import date


current_cart = [] # (ma_tivi, ten_tivi, so_luong, don_gia, thanh_tien) # Giỏ hàng hiện tại
tivi_list = [] # (ma_tivi, ten_tivi, don_gia, so_luong_ton) # Danh sách Tivi còn hàng
customer_list = [] # (ma_kh, ho_ten) # Danh sách Khách hàng
staff_list = [] # (ma_nv, ho_ten) # Danh sách Nhân viên

def create_view(parent_frame):
    global current_cart, tivi_list, customer_list, staff_list
    # Reset giỏ hàng mỗi khi vào tab
    current_cart = []
    # Tạo khung chính
    frame = tk.Frame(parent_frame, bg="#f4f4f4")
    frame.pack(fill="both", expand=True)
    #--- Tiêu đề ---
    tk.Label(frame, text="BÁN HÀNG -  HÓA ĐƠN", font=("Arial", 20, "bold"), bg="#f4f4f4").pack(pady=20) 

    # --- Khung chính chứa 2 cột ---
    main_container = tk.Frame(frame, bg="#f4f4f4")
    main_container.pack(fill="both", expand=True, padx=20, pady=10)

    # --- CỘT TRÁI: Thông tin chọn Khách hàng, Nhân viên, Tivi ---
    info_frame = tk.Frame(main_container, bg="#f4f4f4")
    info_frame.pack(side="left", fill="y", padx=(0, 10))

    #  Chọn Khách hàng và Nhân viên
    customer_frame = tk.LabelFrame(info_frame, text="Thông tin Hóa đơn", padx=10, pady=10)
    customer_frame.pack(fill="x", pady=5)

    # -- Combobox Khách hàng và Nhân viên ---
    tk.Label(customer_frame, text="Chọn Khách hàng:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    customer_combo = ttk.Combobox(customer_frame, width=30, state="readonly")
    customer_combo.grid(row=0, column=1, sticky="w", padx=5, pady=5)
    
    tk.Label(customer_frame, text="Chọn Nhân viên:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    staff_combo = ttk.Combobox(customer_frame, width=30, state="readonly")
    staff_combo.grid(row=1, column=1, sticky="w", padx=5, pady=5)

    #  Chọn Tivi và Số lượng
    product_frame = tk.LabelFrame(info_frame, text="Thêm Tivi vào giỏ", padx=10, pady=10)
    product_frame.pack(fill="x", pady=10)
    #-- Combobox Tivi và nhập số lượng ---
    tk.Label(product_frame, text="Chọn Tivi:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    tivi_combo = ttk.Combobox(product_frame, width=50, state="readonly")
    tivi_combo.grid(row=0, column=1, columnspan=3, sticky="w", padx=5, pady=5)
    #-- Nhãn hiển thị số lượng tồn và đơn giá ---
    tk.Label(product_frame, text="Số lượng tồn:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    ton_kho_label = tk.Label(product_frame, text="...", fg="blue")
    ton_kho_label.grid(row=1, column=1, sticky="w", padx=5, pady=5)
    
    tk.Label(product_frame, text="Đơn giá:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
    don_gia_label = tk.Label(product_frame, text="...", fg="blue")
    don_gia_label.grid(row=1, column=3, sticky="w", padx=5, pady=5)
    #-- Nhập số lượng mua ---
    tk.Label(product_frame, text="Nhập Số lượng mua:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    so_luong_entry = tk.Entry(product_frame, width=10)
    so_luong_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
    # -- Nút Thêm vào giỏ ---
    add_to_cart_btn = tk.Button(product_frame, text="Thêm vào giỏ", command=lambda: add_to_cart(tivi_combo, so_luong_entry, ton_kho_label, don_gia_label))
    add_to_cart_btn.grid(row=2, column=2, columnspan=2, sticky="ew", padx=5, pady=10)

    # --- CỘT PHẢI: Giỏ hàng và Thanh toán ---
    cart_frame_container = tk.Frame(main_container, bg="#f4f4f4")
    cart_frame_container.pack(side="right", fill="both", expand=True, padx=(10, 0))
    # Giỏ hàng
    cart_frame = tk.LabelFrame(cart_frame_container, text="Giỏ hàng hiện tại", padx=10, pady=10)
    cart_frame.pack(fill="both", expand=True)
    #-- TreeView Giỏ hàng ---
    cart_cols = ('ma_tivi', 'ten_tivi', 'so_luong', 'don_gia', 'thanh_tien')
    cart_tree = ttk.Treeview(cart_frame, columns=cart_cols, show='headings', height=10)
    # Định nghĩa cột
    cart_tree.heading('ma_tivi', text='Mã TV')
    cart_tree.heading('ten_tivi', text='Tên Tivi')
    cart_tree.heading('so_luong', text='SL')
    cart_tree.heading('don_gia', text='Đơn giá')
    cart_tree.heading('thanh_tien', text='Thành tiền')
    # Định nghĩa kích thước cột
    cart_tree.column('ma_tivi', width=50, anchor="center")
    cart_tree.column('ten_tivi', width=200,anchor="center")
    cart_tree.column('so_luong', width=50, anchor="center")
    cart_tree.column('don_gia', width=100, anchor="center")
    cart_tree.column('thanh_tien', width=100, anchor="center")
    # Đặt TreeView vào frame
    cart_tree.pack(fill="both", expand=True, side="top")
    #  Nút Xóa khỏi giỏ
    remove_item_btn = tk.Button(cart_frame_container, text="Xóa Tivi khỏi giỏ", command=lambda: remove_from_cart(cart_tree))
    remove_item_btn.pack(pady=5, side="top")

    # Thanh toán
    total_frame = tk.Frame(cart_frame_container, bg="#f4f4f4")
    total_frame.pack(fill="x", side="bottom", pady=10)

    #-- Nhãn Tổng tiền và Nút Thanh toán ---
    tk.Label(total_frame, text="TỔNG TIỀN:", font=("Arial", 14, "bold"), bg="#f4f4f4").grid(row=0, column=0, sticky="w", padx=10)
    total_label = tk.Label(total_frame, text="0 VNĐ", font=("Arial", 14, "bold"), fg="red", bg="#f4f4f4")
    total_label.grid(row=0, column=1, sticky="e", padx=10)
    
    checkout_btn = tk.Button(total_frame, text="THANH TOÁN (LƯU HÓA ĐƠN)", font=("Arial", 12, "bold"), bg="#28a745", fg="white", 
                             command=lambda: checkout(customer_combo, staff_combo, cart_tree, total_label))
    checkout_btn.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10, ipady=10)


    # --- CÁC HÀM XỬ LÝ ---
    def load_combobox_data():
        # Load dữ liệu cho các Combobox
        global tivi_list, customer_list, staff_list
        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Load Khach hàng
            cursor.execute("SELECT ma_kh, ho_ten FROM khachhang ORDER BY ho_ten")
            customer_list = cursor.fetchall()
            customer_combo['values'] = [f"{kh[1]} (ID: {kh[0]})" for kh in customer_list]

            # Load Nhân viên
            cursor.execute("SELECT ma_nv, ho_ten FROM nhanvien ORDER BY ho_ten")
            staff_list = cursor.fetchall()
            staff_combo['values'] = [f"{nv[1]} (ID: {nv[0]})" for nv in staff_list]

            # Load Tivi (chỉ Tivi còn hàng)
            cursor.execute("SELECT ma_tivi, ten_tivi, gia, so_luong FROM tivi WHERE so_luong > 0 ORDER BY ten_tivi")
            tivi_list = cursor.fetchall()
            tivi_combo['values'] = [f"{tv[1]} (Giá: {tv[2]:,.0f})" for tv in tivi_list]
            
            if customer_combo['values']: customer_combo.current(0)
            if staff_combo['values']: staff_combo.current(0)
            if tivi_combo['values']: tivi_combo.current(0)
    
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải dữ liệu: {e}")
        finally:
            if conn: conn.close()
    
    def on_tivi_select(event):
        # Cập nhật nhãn tồn kho và đơn giá khi chọn Tivi
        selected_index = tivi_combo.current()
        if selected_index < 0: return
        
        selected_tivi = tivi_list[selected_index]
        so_luong_ton = selected_tivi[3]
        don_gia = selected_tivi[2]
        
        ton_kho_label.config(text=f"{so_luong_ton} cái")
        don_gia_label.config(text=f"{don_gia:,.0f} VNĐ")

    def update_cart_tree(cart_tree, total_label):
        # Cập nhật TreeView giỏ hàng và tổng tiền
        # Xóa tất cả item cũ
        for item in cart_tree.get_children():
            cart_tree.delete(item)
        
        tong_tien = 0
        for item in current_cart:
            # (ma_tivi, ten_tivi, so_luong, don_gia, thanh_tien)
            formatted_item = (item[0], item[1], item[2], f"{item[3]:,.0f}", f"{item[4]:,.0f}")
            cart_tree.insert('', 'end', values=formatted_item)
            tong_tien += item[4]
            
        total_label.config(text=f"{tong_tien:,.0f} VNĐ")

    def add_to_cart(tivi_combo, so_luong_entry, ton_kho_label, don_gia_label):
        # Thêm Tivi đã chọn vào giỏ hàng
        selected_index = tivi_combo.current()
        if selected_index < 0:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một Tivi")
            return
            
        try:
            so_luong_mua = int(so_luong_entry.get())
            if so_luong_mua <= 0:
                raise ValueError("Số lượng phải lớn hơn 0")
        except ValueError:
            messagebox.showwarning("Sai số lượng", "Vui lòng nhập số lượng mua hợp lệ")
            return

        selected_tivi = tivi_list[selected_index]
        ma_tivi = selected_tivi[0]
        ten_tivi = selected_tivi[1]
        don_gia = selected_tivi[2]
        so_luong_ton = selected_tivi[3]

        if so_luong_mua > so_luong_ton:
            messagebox.showwarning("Hết hàng", f"Số lượng tồn kho không đủ (Chỉ còn {so_luong_ton} cái)")
            return
            
        # Kiểm tra xem Tivi đã có trong giỏ chưa
        found = False
        for i, item in enumerate(current_cart):
            if item[0] == ma_tivi:
                # Cập nhật số lượng
                new_sl = item[2] + so_luong_mua
                if new_sl > so_luong_ton:
                    messagebox.showwarning("Hết hàng", f"Tổng số lượng mua ({new_sl}) vượt quá tồn kho ({so_luong_ton})")
                    return
                thanh_tien = new_sl * don_gia
                current_cart[i] = (ma_tivi, ten_tivi, new_sl, don_gia, thanh_tien)
                found = True
                break
        
        if not found:
            # Thêm mới vào giỏ
            thanh_tien = so_luong_mua * don_gia
            current_cart.append((ma_tivi, ten_tivi, so_luong_mua, don_gia, thanh_tien))

        update_cart_tree(cart_tree, total_label)
        # Reset
        so_luong_entry.delete(0, 'end')

    def remove_from_cart(cart_tree):
        # Xóa Tivi đã chọn khỏi giỏ hàng
        selected_item = cart_tree.focus()
        if not selected_item:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn Tivi cần xóa khỏi giỏ")
            return
        
        values = cart_tree.item(selected_item, 'values')
        ma_tivi = values[0]
        
        for i, item in enumerate(current_cart):
            if item[0] == ma_tivi:
                del current_cart[i]
                break
        
        update_cart_tree(cart_tree, total_label)

    def checkout(customer_combo, staff_combo, cart_tree, total_label):
        # Thanh toán và lưu hóa đơn
        if not current_cart:
            messagebox.showwarning("Giỏ hàng rỗng", "Vui lòng thêm sản phẩm vào giỏ")
            return
        
        try:
            # Lấy ma_kh và ma_nv từ combobox
            ma_kh = customer_list[customer_combo.current()][0]
            ma_nv = staff_list[staff_combo.current()][0]
        except IndexError:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn khách hàng và nhân viên")
            return

        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thanh toán và lưu hóa đơn này?"):
            return

        conn = None
        try:
            conn = connect_db()
            cursor = conn.cursor()
            
            # --- Bắt đầu Transaction ---
            conn.start_transaction()

            #  Tính tổng tiền từ giỏ hàng 
            tong_tien = sum(item[4] for item in current_cart)
            
            #  Tạo Hóa đơn (hoadon)
            ngay_lap = date.today()
            sql_hoadon = "INSERT INTO hoadon (ma_nv, ma_kh, ngay_lap, tong_tien) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_hoadon, (ma_nv, ma_kh, ngay_lap, tong_tien))
            
            # Lấy ID của hóa đơn vừa tạo
            ma_hd_moi = cursor.lastrowid

            #  Thêm các Chi tiết Hóa đơn (chitiet_hoadon)
            sql_chitiet = "INSERT INTO chitiet_hoadon (ma_hd, ma_tivi, so_luong_mua, don_gia) VALUES (%s, %s, %s, %s)"
            sql_update_tivi = "UPDATE tivi SET so_luong = so_luong - %s WHERE ma_tivi = %s"
            
            for item in current_cart:
                # item = (ma_tivi, ten_tivi, so_luong, don_gia, thanh_tien)
                ma_tivi = item[0]
                so_luong_mua = item[2]
                don_gia = item[3]
                
                # Thêm vào chitiet_hoadon
                cursor.execute(sql_chitiet, (ma_hd_moi, ma_tivi, so_luong_mua, don_gia))
                
                # Cập nhật số lượng Tivi (tivi)
                cursor.execute(sql_update_tivi, (so_luong_mua, ma_tivi))

            # --- Kết thúc Transaction (lưu) ---
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã lưu hóa đơn (Mã HĐ: {ma_hd_moi}) thành công!")
            
            # Reset giỏ hàng và giao diện
            current_cart.clear()
            update_cart_tree(cart_tree, total_label)
            load_combobox_data() 

        except Exception as e:
            
            if conn:
                conn.rollback()
            messagebox.showerror("Lỗi Giao dịch", f"Không thể lưu hóa đơn: {e}")
        finally:
            if conn:
                conn.close()

    # --- Gán sự kiện và Tải dữ liệu ---
    tivi_combo.bind('<<ComboboxSelected>>', on_tivi_select)
    load_combobox_data()
    # Kích hoạt sự kiện lần đầu
    on_tivi_select(None)