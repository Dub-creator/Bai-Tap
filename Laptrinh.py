import pickle
import os

# ========================
# Định nghĩa lớp Sách
# ========================
class Sach:
    def __init__(self, ma_sach, ten_sach, tac_gia, nam_xuat_ban):
        self.__ma_sach = ma_sach
        self.__ten_sach = ten_sach
        self.__tac_gia = tac_gia
        self.__nam_xuat_ban = nam_xuat_ban

    def get_ma_sach(self):
        return self.__ma_sach

    def set_ma_sach(self, ma_sach):
        self.__ma_sach = ma_sach

    def get_ten_sach(self):
        return self.__ten_sach

    def set_ten_sach(self, ten_sach):
        self.__ten_sach = ten_sach

    def get_tac_gia(self):
        return self.__tac_gia

    def set_tac_gia(self, tac_gia):
        self.__tac_gia = tac_gia

    def get_nam_xuat_ban(self):
        return self.__nam_xuat_ban

    def set_nam_xuat_ban(self, nam_xuat_ban):
        self.__nam_xuat_ban = nam_xuat_ban

    def hien_thi_thong_tin(self):
        print(f"Mã sách: {self.__ma_sach}, Tên sách: {self.__ten_sach}, Tác giả: {self.__tac_gia}, Năm xuất bản: {self.__nam_xuat_ban}")

# ========================
# Định nghĩa lớp Người dùng
# ========================
class NguoiDung:
    def __init__(self, ten_dang_nhap, mat_khau):
        self.__ten_dang_nhap = ten_dang_nhap
        self.__mat_khau = mat_khau

    def get_ten_dang_nhap(self):
        return self.__ten_dang_nhap

    def get_mat_khau(self):
        return self.__mat_khau

# ========================
# Định nghĩa lớp Quản lý Sách
# ========================
class QuanLySach:
    def __init__(self):
        self.danh_sach_sach = []

    def them_sach(self, sach):
        self.danh_sach_sach.append(sach)

    def hien_thi_tat_ca_sach(self):
        if not self.danh_sach_sach:
            print("Chưa có sách nào trong thư viện.")
        else:
            for sach in self.danh_sach_sach:
                sach.hien_thi_thong_tin()

    def tim_sach_theo_ten(self, ten):
        ket_qua = []
        for sach in self.danh_sach_sach:
            if ten.lower() in sach.get_ten_sach().lower():
                ket_qua.append(sach)
        return ket_qua

# ========================
# Các hàm lưu và tải dữ liệu
# ========================

def luu_nguoi_dung(danh_sach_nguoi_dung, filename="users.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(danh_sach_nguoi_dung, f)

def tai_nguoi_dung(filename="users.pkl"):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    else:
        return []

# ========================
# Các chức năng chính
# ========================

def dang_nhap_admin():
    admin_ten = "admin"
    admin_mat_khau = "admin123"
    ten = input("Nhập tên đăng nhập: ")
    mat_khau = input("Nhập mật khẩu: ")
    if ten == admin_ten and mat_khau == admin_mat_khau:
        print("Đăng nhập quản trị viên thành công!")
        return True
    else:
        print("Đăng nhập thất bại!")
        return False

def dang_nhap_user(danh_sach_nguoi_dung):
    ten = input("Nhập tên đăng nhập: ")
    mat_khau = input("Nhập mật khẩu: ")
    for user in danh_sach_nguoi_dung:
        if user.get_ten_dang_nhap() == ten and user.get_mat_khau() == mat_khau:
            print("Đăng nhập người dùng thành công!")
            return True
    print("Đăng nhập thất bại!")
    return False

def dang_ky_user(danh_sach_nguoi_dung):
    ten = input("Nhập tên đăng nhập mới: ")
    for user in danh_sach_nguoi_dung:
        if user.get_ten_dang_nhap() == ten:
            print("Tên đăng nhập đã tồn tại!")
            return
    mat_khau = input("Nhập mật khẩu: ")
    danh_sach_nguoi_dung.append(NguoiDung(ten, mat_khau))
    luu_nguoi_dung(danh_sach_nguoi_dung)
    print("Đăng ký tài khoản thành công!")

# ========================
# Chương trình chính
# ========================

def main():
    quan_ly = QuanLySach()
    danh_sach_nguoi_dung = tai_nguoi_dung()

    while True:
        print("\n========== MENU ==========")
        print("1. Đăng nhập Quản trị viên")
        print("2. Đăng nhập Người dùng")
        print("3. Đăng ký tài khoản Người dùng")
        print("0. Thoát")
        lua_chon = input("Chọn chức năng: ")

        if lua_chon == "1":
            if dang_nhap_admin():
                while True:
                    print("\n----- QUẢN TRỊ VIÊN -----")
                    print("1. Thêm sách")
                    print("2. Hiển thị tất cả sách")
                    print("3. Tìm sách theo tên")
                    print("0. Đăng xuất")
                    chon = input("Chọn chức năng: ")

                    if chon == "1":
                        ma_sach = input("Nhập mã sách: ")
                        ten_sach = input("Nhập tên sách: ")
                        tac_gia = input("Nhập tên tác giả: ")
                        nam_xuat_ban = input("Nhập năm xuất bản: ")
                        sach = Sach(ma_sach, ten_sach, tac_gia, nam_xuat_ban)
                        quan_ly.them_sach(sach)
                        print("Thêm sách thành công!")
                    elif chon == "2":
                        quan_ly.hien_thi_tat_ca_sach()
                    elif chon == "3":
                        ten = input("Nhập tên sách cần tìm: ")
                        ket_qua = quan_ly.tim_sach_theo_ten(ten)
                        if ket_qua:
                            for s in ket_qua:
                                s.hien_thi_thong_tin()
                        else:
                            print("Không tìm thấy sách.")
                    elif chon == "0":
                        break
                    else:
                        print("Lựa chọn không hợp lệ!")

        elif lua_chon == "2":
            if dang_nhap_user(danh_sach_nguoi_dung):
                while True:
                    print("\n----- NGƯỜI DÙNG -----")
                    print("1. Xem tất cả sách")
                    print("2. Tìm sách theo tên")
                    print("0. Đăng xuất")
                    chon = input("Chọn chức năng: ")

                    if chon == "1":
                        quan_ly.hien_thi_tat_ca_sach()
                    elif chon == "2":
                        ten = input("Nhập tên sách cần tìm: ")
                        ket_qua = quan_ly.tim_sach_theo_ten(ten)
                        if ket_qua:
                            for s in ket_qua:
                                s.hien_thi_thong_tin()
                        else:
                            print("Không tìm thấy sách.")
                    elif chon == "0":
                        break
                    else:
                        print("Lựa chọn không hợp lệ!")

        elif lua_chon == "3":
            dang_ky_user(danh_sach_nguoi_dung)

        elif lua_chon == "0":
            print("Tạm biệt!")
            break

        else:
            print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
