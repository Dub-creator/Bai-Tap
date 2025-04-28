import pickle
import os
import re

# ========================
# Định nghĩa lớp Sách
# ========================
class Sach:
    def __init__(self, ma_sach, ten_sach, tac_gia, nam_xuat_ban):
        self.__ma_sach = ma_sach
        self.__ten_sach = ten_sach
        self.__tac_gia = tac_gia
        self.__nam_xuat_ban = nam_xuat_ban

    def get_ma_sach(self): return self.__ma_sach
    def get_ten_sach(self): return self.__ten_sach
    def get_tac_gia(self): return self.__tac_gia
    def get_nam_xuat_ban(self): return self.__nam_xuat_ban

    def hien_thi_thong_tin(self):
        print(f"[{self.__ma_sach}] {self.__ten_sach} - Tác giả: {self.__tac_gia} - Năm XB: {self.__nam_xuat_ban}")

# ========================
# Định nghĩa lớp Người dùng
# ========================
class NguoiDung:
    def __init__(self, ten_dang_nhap, mat_khau, is_admin=False):
        self.__ten_dang_nhap = ten_dang_nhap
        self.__mat_khau = mat_khau
        self.__is_admin = is_admin
        self.__saved_books = []  # danh sách muốn đọc

    def get_ten_dang_nhap(self): return self.__ten_dang_nhap
    def get_mat_khau(self): return self.__mat_khau
    def is_admin(self): return self.__is_admin

    # Lưu sách muốn đọc
    def save_book(self, sach):
        self.__saved_books.append(sach)
        print(f"Đã lưu sách '[{sach.get_ma_sach()}] {sach.get_ten_sach()}' vào danh sách muốn đọc.")

    # Xem sách đã lưu
    def view_saved_books(self):
        if not self.__saved_books:
            print("Danh sách muốn đọc trống.")
        else:
            for s in self.__saved_books:
                s.hien_thi_thong_tin()

    # Xóa sách đã lưu
    def remove_saved_book(self, ma_sach):
        for s in self.__saved_books:
            if s.get_ma_sach() == ma_sach:
                self.__saved_books.remove(s)
                print(f"Đã xóa sách '{ma_sach}' khỏi danh sách muốn đọc.")
                return
        print(f"Không tìm thấy sách '{ma_sach}' trong danh sách muốn đọc.")

# ========================
# Định nghĩa lớp Quản lý Sách
# ========================
class QuanLySach:
    def __init__(self):
        self.danh_sach_sach = []

    def them_sach(self, sach):
        self.danh_sach_sach.append(sach)
        print("Thêm sách thành công vào thư viện.")

    def hien_thi_tat_ca_sach(self):
        if not self.danh_sach_sach:
            print("Chưa có sách nào trong thư viện.")
        else:
            for sach in self.danh_sach_sach:
                sach.hien_thi_thong_tin()

    def tim_sach_theo_ten(self, ten):
        return [s for s in self.danh_sach_sach if ten.lower() in s.get_ten_sach().lower()]

# ========================
# Lưu/tải dữ liệu người dùng
# ========================

def luu_nguoi_dung(ds, filename="users.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(ds, f)

def tai_nguoi_dung(filename="users.pkl"):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return []

# ========================
# Đăng nhập/Đăng ký chung
# ========================

def dang_nhap(ds):
    ten = input("Tên đăng nhập: ")
    mat_khau = input("Mật khẩu: ")
    for u in ds:
        if u.get_ten_dang_nhap() == ten and u.get_mat_khau() == mat_khau:
            print("Đăng nhập thành công!")
            return u
    print("Đăng nhập thất bại!")
    return None

# ========================
# Tạo admin lần đầu
# ========================
def tao_admin():
    ds = tai_nguoi_dung()
    for u in ds:
        if u.get_ten_dang_nhap() == 'admin' and u.is_admin():
            return
    admin = NguoiDung('admin', 'admin123', is_admin=True)
    ds.append(admin)
    luu_nguoi_dung(ds)
    print("Admin mặc định đã được tạo (admin/admin123)")

# ========================
# Kiểm tra input
# ========================

def valid_author(name):
    return bool(re.fullmatch(r"[A-Za-zÀ-ỹ ]+", name))

def valid_year(y):
    return y.isdigit() and len(y) == 4

# ========================
# Menu chính
# ========================

def main():
    lib = QuanLySach()
    users = tai_nguoi_dung()

    while True:
        print("\n========== MENU ==========")
        print("1. Đăng nhập admin")
        print("2. Đăng nhập người dùng")
        print("3. Đăng ký người dùng")
        print("0. Thoát")
        ch = input("Chọn chức năng: ")

        if ch == '1':
            user = dang_nhap(users)
            if user and user.is_admin():
                while True:
                    print("\n--- Admin Menu ---")
                    print("1. Thêm sách")
                    print("2. Xem tất cả sách")
                    print("3. Tìm sách")
                    print("0. Đăng xuất")
                    c = input("Chọn: ")
                    if c == '1':
                        ma = input("Mã sách: ")
                        ten = input("Tên sách: ")
                        while not valid_author((tg := input("Tác giả: "))):
                            print("Tên tác giả không hợp lệ.")
                        while not valid_year((ny := input("Năm xuất bản (YYYY): "))):
                            print("Năm xuất bản không hợp lệ.")
                        lib.them_sach(Sach(ma, ten, tg, ny))
                    elif c == '2': lib.hien_thi_tat_ca_sach()
                    elif c == '3':
                        kw = input("Từ khóa tìm: ")
                        rs = lib.tim_sach_theo_ten(kw)
                        if rs: [s.hien_thi_thong_tin() for s in rs]
                        else: print("Không tìm thấy.")
                    elif c == '0': break
                    else: print("Lựa chọn không hợp lệ.")

        elif ch == '2':
            user = dang_nhap(users)
            if user and not user.is_admin():
                while True:
                    print("\n--- User Menu ---")
                    print("1. Xem tất cả sách")
                    print("2. Tìm sách")
                    print("3. Lưu sách muốn đọc")
                    print("4. Xem sách đã lưu")
                    print("5. Xóa sách đã lưu")
                    print("0. Đăng xuất")
                    c = input("Chọn: ")
                    if c == '1':
                        lib.hien_thi_tat_ca_sach()
                    elif c == '2':
                        kw = input("Từ khóa tìm: ")
                        rs = lib.tim_sach_theo_ten(kw)
                        if rs: [s.hien_thi_thong_tin() for s in rs]
                        else: print("Không tìm thấy.")
                    elif c == '3':
                        ma = input("Mã sách muốn lưu: ")
                        target = next((s for s in lib.danh_sach_sach if s.get_ma_sach()==ma), None)
                        if target: user.save_book(target)
                        else: print("Không tìm thấy sách.")
                    elif c == '4': user.view_saved_books()
                    elif c == '5': user.remove_saved_book(input("Mã sách xóa: "))
                    elif c == '0': break
                    else: print("Lựa chọn không hợp lệ.")

        elif ch == '3':
            un = input("Tên đăng nhập mới: ")
            if any(u.get_ten_dang_nhap()==un for u in users):
                print("Tên đã tồn tại.")
            else:
                pw = input("Mật khẩu: ")
                users.append(NguoiDung(un, pw, False))
                luu_nguoi_dung(users)
                print("Đăng ký thành công.")

        elif ch == '0':
            print("Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    if not os.path.exists('users.pkl'):
        tao_admin()
    main()
