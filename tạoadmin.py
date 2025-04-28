import pickle
import os

# Phải định nghĩa class giống hệt bên chương trình chính
class NguoiDung:
    def __init__(self, ten_dang_nhap, mat_khau, is_admin=False):
        self.__ten_dang_nhap = ten_dang_nhap
        self.__mat_khau = mat_khau
        self.__is_admin = is_admin  # Thêm flag phân biệt Admin hay User

    def get_ten_dang_nhap(self):
        return self.__ten_dang_nhap

    def get_mat_khau(self):
        return self.__mat_khau

    def is_admin(self):
        return self.__is_admin

def tai_nguoi_dung(filename="users.pkl"):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    else:
        return []

def luu_nguoi_dung(danh_sach_nguoi_dung, filename="users.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(danh_sach_nguoi_dung, f)

def tao_admin():
    danh_sach = tai_nguoi_dung()

    # Kiểm tra xem đã có admin chưa
    for nguoi in danh_sach:
        if nguoi.get_ten_dang_nhap() == "admin":
            print("Admin đã tồn tại.")
            return

    # Nhập tên đăng nhập và mật khẩu cho admin
    ten_admin = input("Nhập tên đăng nhập cho admin: ")
    mat_khau_admin = input("Nhập mật khẩu cho admin: ")

    # Kiểm tra tên đăng nhập và mật khẩu (có thể thêm các điều kiện kiểm tra nếu cần)
    if len(mat_khau_admin) < 6:
        print("Mật khẩu quá ngắn, phải có ít nhất 6 ký tự.")
        return

    # Tạo tài khoản admin mới
    admin = NguoiDung(ten_admin, mat_khau_admin, is_admin=True)
    danh_sach.append(admin)
    luu_nguoi_dung(danh_sach)
    print(f"Tạo tài khoản admin {ten_admin} thành công!")

if __name__ == "__main__":
    tao_admin()
