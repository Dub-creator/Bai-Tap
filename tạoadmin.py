import os
import pickle
import uuid

# Bạn cần đảm bảo rằng 2 lớp này đã được định nghĩa (hoặc import) trước khi dùng
# from your_module import InputValidator, Admin

class InputValidator:
    @staticmethod
    def validate_username(username):
        # 4–20 ký tự, chỉ chữ/số/_
        return bool(__import__('re').fullmatch(r'^[a-zA-Z0-9_]{4,20}$', username))

class Admin:
    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = 'admin'

    def login(self, username, password):
        return self.username == username and self.password == password

    def logout(self):
        print(f"Admin {self.username} đã đăng xuất.")


def create_admin_account(file_path='users.pkl'):
    # Tải hoặc khởi tạo danh sách users
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            users = pickle.load(f)
    else:
        users = []

    print("=== TẠO TÀI KHOẢN ADMIN MỚI ===")

    # Nhập tên đăng nhập
    while True:
        username = input("Nhập tên đăng nhập (4-20 ký tự, chữ/số/_): ")
        if not InputValidator.validate_username(username):
            print("Tên đăng nhập không hợp lệ! (4–20 ký tự, chỉ chữ/số/_)")
            continue
        if any(u.username == username for u in users):
            print("Tên đăng nhập đã tồn tại!")
            continue
        break

    # Nhập mật khẩu (bạn có thể thêm validate mật khẩu nếu cần)
    password = input("Nhập mật khẩu: ")

    # Tạo admin mới
    user_id = str(uuid.uuid4())
    new_admin = Admin(user_id, username, password)
    users.append(new_admin)

    # Lưu lại file
    with open(file_path, 'wb') as f:
        pickle.dump(users, f)

    print(f"Tạo tài khoản admin '{username}' thành công! ID: {user_id}")


if __name__ == "__main__":
    create_admin_account()

