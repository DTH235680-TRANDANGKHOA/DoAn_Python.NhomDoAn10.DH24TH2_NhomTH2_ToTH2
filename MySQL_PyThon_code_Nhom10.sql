CREATE DATABASE ql_cuahangtv_nk CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ql_cuahangtv_nk;

CREATE TABLE tivi (
    ma_tivi INT PRIMARY KEY AUTO_INCREMENT,
    ten_tivi VARCHAR(100),
    hang_sx VARCHAR(50),
    kich_thuoc VARCHAR(20),
    gia DECIMAL(15,2),
    so_luong INT, 
    bao_hanh VARCHAR(50)
);


CREATE TABLE nhanvien (
    ma_nv INT PRIMARY KEY AUTO_INCREMENT,
    ho_ten VARCHAR(100),
    chuc_vu VARCHAR(50),
    luong DECIMAL(15,2),
    
    /* ---  CHỨC NĂNG ĐĂNG NHẬP --- */
    username VARCHAR(50) UNIQUE,
    password VARCHAR(100)
);


CREATE TABLE khachhang (
    ma_kh INT PRIMARY KEY AUTO_INCREMENT,
    ho_ten VARCHAR(100),
    sdt VARCHAR(15),
    dia_chi VARCHAR(150)
);


CREATE TABLE hoadon (
    ma_hd INT PRIMARY KEY AUTO_INCREMENT,
    ma_nv INT, 
    ma_kh INT, 
    ngay_lap DATE,
    tong_tien DECIMAL(15,2),
    
    FOREIGN KEY (ma_nv) REFERENCES nhanvien(ma_nv) ON DELETE SET NULL,
    FOREIGN KEY (ma_kh) REFERENCES khachhang(ma_kh) ON DELETE SET NULL
);

/* Bảng Chitiet_Hoadon (Liên kết Hoadon và Tivi) */
CREATE TABLE chitiet_hoadon (
    ma_cthd INT PRIMARY KEY AUTO_INCREMENT,
    ma_hd INT, 
    ma_tivi INT, 
    so_luong_mua INT,
    don_gia DECIMAL(15,2), 
    
    /* 
        Nếu xóa Hoadon -> tự động xóa các Chitiet_hoadon (CASCADE)
        Cấm xóa Tivi nếu nó đã có trong 1 chi tiết hóa đơn (RESTRICT - Mặc định)
    */
    FOREIGN KEY (ma_hd) REFERENCES hoadon(ma_hd) ON DELETE CASCADE,
    FOREIGN KEY (ma_tivi) REFERENCES tivi(ma_tivi) ON DELETE RESTRICT
);


CREATE TABLE tonkho (
    ma_ton INT AUTO_INCREMENT PRIMARY KEY,
    ma_tivi INT, 
    ngay_cap_nhat DATE,
    so_luong_ton INT, 
    ghi_chu VARCHAR(255),
    
    FOREIGN KEY (ma_tivi) REFERENCES tivi(ma_tivi) ON DELETE CASCADE
); 


INSERT INTO tivi (ten_tivi, hang_sx, kich_thuoc, gia, so_luong, bao_hanh) 
VALUES 
('Smart Tivi QLED 4K 65 inch Samsung', 'Samsung', '65 inch', 25000000, 50, '24 tháng'),
('Smart Tivi NanoCell 4K 55 inch LG', 'LG', '55 inch', 18500000, 30, '24 tháng'),
('Android Tivi 4K 50 inch Sony', 'Sony', '50 inch', 15000000, 40, '24 tháng');


INSERT INTO nhanvien (ho_ten, chuc_vu, luong, username, password) 
VALUES 
('Thái Vĩnh Nghi', 'Quản lý', 30000000, 'admin', 'nghi123'),
('Trần Đăng Khoa', 'Bán hàng', 12000000, 'nhanvien1', 'khoa123');


INSERT INTO khachhang (ho_ten, sdt, dia_chi) 
VALUES 
('Tôn Anh Quân', '0909123456', '12 Đường Mỹ Bình, Quận Bình Long 1, TP. Long Xuyên'),
('Tạ Hồng Quân', '0987654321', '56 Đường Mỹ Long, Quận Hoà An, Châu Đốc'),
('Phó Bảo Phong', '0954654331', '90 Đường Mỹ Hoà Hưng, Quận An Phú, Tịnh Biên'),
('Tống Nhựt Nam', '0967453982', '64 Đường Mỹ Thới, Quận Gia Lai, Đắc Lắc'),
('Huỳnh Minh Thuận', '0932578954', '78 Đường Mỹ Phước, Quận An Biên, Cần Thơ');

INSERT INTO tonkho (ma_tivi, ngay_cap_nhat, so_luong_ton, ghi_chu)
VALUES
(1, CURDATE(), 50, 'Nhập kho lần đầu'),
(2, CURDATE(), 30, 'Nhập kho lần đầu'),
(3, CURDATE(), 40, 'Nhập kho lần đầu');


--  Tạo Hóa đơn --
INSERT INTO hoadon (ma_nv, ma_kh, ngay_lap, tong_tien)
VALUES
(2, 1, '2025-11-10', 37000000); 

-- Thêm Chi tiết Hóa đơn --
INSERT INTO chitiet_hoadon (ma_hd, ma_tivi, so_luong_mua, don_gia)
VALUES
(1, 2, 2, 18500000);

--  Cập nhật lại số lượng trong kho Tivi --
UPDATE tivi SET so_luong = 28 WHERE ma_tivi = 2;

-- Thêm Log Xuất Kho --
INSERT INTO tonkho (ma_tivi, ngay_cap_nhat, so_luong_ton, ghi_chu)
VALUES
(2, '2025-11-10', -2, 'Bán theo Hóa đơn ID 1');