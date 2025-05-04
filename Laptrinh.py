import pickle
import os
import re
from enum import Enum
from datetime import datetime

# ========================
# Enum và các lớp cơ bản
# ========================
class BookStatus(Enum):
    AVAILABLE = "Có sẵn"
    BORROWED = "Đã mượn"
    LOST = "Đã mất"

class InputValidator:
    @staticmethod
    def validate_author(name):
        return bool(re.fullmatch(r"[A-Za-zÀ-ỹ ]+", name))

    @staticmethod
    def validate_year(year):
        return year.isdigit() and len(year) == 4 and 1000 <= int(year) <= datetime.now().year

    @staticmethod
    def validate_rating(rating):
        return rating.isdigit() and 0 <= int(rating) <= 5

    @staticmethod
    def validate_username(username):
        return bool(re.fullmatch(r"^[a-zA-Z0-9_]{4,20}$", username))

# ========================
# Lớp Book (Sách)
# ========================
class Book:
    def __init__(self, book_id, title, author, publish_year, category=None, status=BookStatus.AVAILABLE, rating=0):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.publish_year = publish_year
        self.category = category
        self.status = status
        self.rating = rating
        self.added_date = datetime.now().date()
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def display_info(self):
        print(f"[{self.book_id}] {self.title} - Tác giả: {self.author}")
        print(f"Năm XB: {self.publish_year} | Thể loại: {self.category}")
        print(f"Trạng thái: {self.status.value} | Đánh giá: {'★' * self.rating}")
        print(f"Ngày thêm: {self.added_date}\n")

# ========================
# Lớp User (Người dùng)
# ========================
class User:
    def __init__(self, user_id, username, password, role):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role
    
    def login(self, username, password):
        return self.username == username and self.password == password
    
    def logout(self):
        print(f"Người dùng {self.username} đã đăng xuất.")

# ========================
# Lớp Admin (Quản trị viên)
# ========================
class Admin(User):
    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password, "admin")
    
    def add_book(self, book_list, book):
        book_list.add_book(book)
        print("Thêm sách thành công!")
    
    def edit_book(self, book_list, book_id, **new_data):
        book = book_list.find_book_by_id(book_id)
        if book:
            book.update(**new_data)
            print("Cập nhật sách thành công!")
        else:
            print("Không tìm thấy sách!")
    
    def delete_book(self, book_list, book_id):
        if book_list.remove_book(book_id):
            print("Xóa sách thành công!")
        else:
            print("Không tìm thấy sách!")

    def run_menu(self, book_list, user_manager):
        while True:
            print("\n--- MENU QUẢN TRỊ ---")
            print("1. Thêm sách mới")
            print("2. Chỉnh sửa thông tin sách")
            print("3. Xóa sách")
            print("4. Xem tất cả sách")
            print("5. Tìm kiếm sách")
            print("6. Lọc sách theo thể loại")
            print("7. Lọc sách theo trạng thái")
            print("8. Lọc sách theo ngày thêm")
            print("0. Đăng xuất")
            
            choice = input("Chọn chức năng: ")
            
            if choice == '1':
                self._handle_add_book(book_list)
            
            elif choice == '2':
                self._handle_edit_book(book_list)
            
            elif choice == '3':
                self._handle_delete_book(book_list)
            
            elif choice == '4':
                book_list.display_all_books()
            
            elif choice == '5':
                self._handle_search_book(book_list)
            
            elif choice == '6':
                self._handle_filter_by_category(book_list)
            
            elif choice == '7':
                self._handle_filter_by_status(book_list)
            
            elif choice == '8':
                self._handle_filter_by_date(book_list)
            
            elif choice == '0':
                self.logout()
                break
            
            else:
                print("Lựa chọn không hợp lệ!")

    def _handle_add_book(self, book_list):
        print("\n--- THÊM SÁCH MỚI ---")
        book_id = input("Mã sách: ")
        title = input("Tên sách: ")
        
        while not InputValidator.validate_author((author := input("Tác giả: "))):
            print("Tên tác giả không hợp lệ!")
        
        while not InputValidator.validate_year((year := input("Năm xuất bản (YYYY): "))):
            print("Năm xuất bản không hợp lệ!")
        
        category = input("Thể loại (Enter để bỏ qua): ") or None
        
        status = BookStatus.AVAILABLE
        status_input = input("Trạng thái (1. Có sẵn, 2. Đã mượn, 3. Đã mất): ")
        if status_input == '2':
            status = BookStatus.BORROWED
        elif status_input == '3':
            status = BookStatus.LOST
        
        rating = 0
        rating_input = input("Đánh giá (0-5, Enter để bỏ qua): ")
        if rating_input:
            while not InputValidator.validate_rating(rating_input):
                print("Đánh giá phải từ 0-5!")
                rating_input = input("Đánh giá: ")
            rating = int(rating_input)
        
        new_book = Book(book_id, title, author, year, category, status, rating)
        self.add_book(book_list, new_book)
        BookManager.save_to_file(book_list)

    def _handle_edit_book(self, book_list):
        book_id = input("Nhập mã sách cần chỉnh sửa: ")
        book = book_list.find_book_by_id(book_id)
        if book:
            print("\nThông tin hiện tại:")
            book.display_info()
            
            updates = {}
            if (title := input("Tên mới (Enter để giữ nguyên): ")):
                updates['title'] = title
            
            if (author := input("Tác giả mới (Enter để giữ nguyên): ")):
                while not InputValidator.validate_author(author):
                    print("Tên tác giả không hợp lệ!")
                    author = input("Tác giả mới: ")
                updates['author'] = author
            
            if (year := input("Năm XB mới (Enter để giữ nguyên): ")):
                while not InputValidator.validate_year(year):
                    print("Năm xuất bản không hợp lệ!")
                    year = input("Năm XB mới: ")
                updates['publish_year'] = year
            
            if (category := input("Thể loại mới (Enter để giữ nguyên, 'none' để xóa): ")):
                updates['category'] = None if category.lower() == 'none' else category
            
            if (status := input("Trạng thái mới (1. Có sẵn, 2. Đã mượn, 3. Đã mất, Enter để giữ nguyên): ")):
                if status == '1': updates['status'] = BookStatus.AVAILABLE
                elif status == '2': updates['status'] = BookStatus.BORROWED
                elif status == '3': updates['status'] = BookStatus.LOST
            
            if (rating := input("Đánh giá mới (0-5, Enter để giữ nguyên): ")):
                while not InputValidator.validate_rating(rating):
                    print("Đánh giá phải từ 0-5!")
                    rating = input("Đánh giá mới: ")
                updates['rating'] = int(rating)
            
            if updates:
                self.edit_book(book_list, book_id, **updates)
                BookManager.save_to_file(book_list)
            else:
                print("Không có thay đổi nào được thực hiện.")
        else:
            print("Không tìm thấy sách!")

    def _handle_delete_book(self, book_list):
        book_id = input("Nhập mã sách cần xóa: ")
        self.delete_book(book_list, book_id)
        BookManager.save_to_file(book_list)

    def _handle_search_book(self, book_list):
        keyword = input("Nhập từ khóa tìm kiếm: ")
        results = book_list.search_books(keyword)
        if results:
            print(f"\nTìm thấy {len(results)} kết quả:")
            for book in results:
                book.display_info()
        else:
            print("Không tìm thấy sách phù hợp.")

    def _handle_filter_by_category(self, book_list):
        category = input("Nhập thể loại cần lọc: ")
        results = book_list.filter_by_category(category)
        if results:
            print(f"\nTìm thấy {len(results)} sách thuộc thể loại '{category}':")
            for book in results:
                book.display_info()
        else:
            print(f"Không có sách nào thuộc thể loại '{category}'.")

    def _handle_filter_by_status(self, book_list):
        print("Chọn trạng thái:")
        print("1. Có sẵn")
        print("2. Đã mượn")
        print("3. Đã mất")
        status_choice = input("Lựa chọn: ")
        
        if status_choice in ['1', '2', '3']:
            status = BookStatus.AVAILABLE if status_choice == '1' else (
                BookStatus.BORROWED if status_choice == '2' else BookStatus.LOST)
            results = book_list.filter_by_status(status)
            
            if results:
                print(f"\nTìm thấy {len(results)} sách có trạng thái '{status.value}':")
                for book in results:
                    book.display_info()
            else:
                print(f"Không có sách nào có trạng thái '{status.value}'.")
        else:
            print("Lựa chọn không hợp lệ!")

    def _handle_filter_by_date(self, book_list):
        try:
            start = input("Ngày bắt đầu (YYYY-MM-DD): ")
            end = input("Ngày kết thúc (YYYY-MM-DD): ")
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            end_date = datetime.strptime(end, "%Y-%m-%d").date()
            
            results = book_list.filter_by_date(start_date, end_date)
            if results:
                print(f"\nTìm thấy {len(results)} sách được thêm từ {start} đến {end}:")
                for book in results:
                    book.display_info()
            else:
                print(f"Không có sách nào được thêm từ {start} đến {end}.")
        except ValueError:
            print("Định dạng ngày không hợp lệ! Sử dụng YYYY-MM-DD.")

# ========================
# Lớp NormalUser (Người dùng thường)
# ========================
class NormalUser(User):
    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password, "user")
        self.saved_books = []
    
    def save_book(self, book):
        if book not in self.saved_books:
            self.saved_books.append(book)
            print(f"Đã lưu sách '{book.title}' vào danh sách yêu thích.")
        else:
            print("Sách đã có trong danh sách yêu thích.")
    
    def remove_saved_book(self, book_id):
        for book in self.saved_books:
            if book.book_id == book_id:
                self.saved_books.remove(book)
                print("Đã xóa sách khỏi danh sách yêu thích.")
                return
        print("Không tìm thấy sách trong danh sách yêu thích.")
    
    def view_saved_books(self):
        if not self.saved_books:
            print("Danh sách yêu thích trống.")
        else:
            print("\n--- SÁCH YÊU THÍCH ---")
            for book in self.saved_books:
                book.display_info()

    def run_menu(self, book_list, user_manager):
        while True:
            print("\n--- MENU NGƯỜI DÙNG ---")
            print("1. Xem tất cả sách")
            print("2. Tìm kiếm sách")
            print("3. Lưu sách vào danh sách yêu thích")
            print("4. Xem sách yêu thích")
            print("5. Xóa sách khỏi danh sách yêu thích")
            print("0. Đăng xuất")
            
            choice = input("Chọn chức năng: ")
            
            if choice == '1':
                book_list.display_all_books()
            
            elif choice == '2':
                self._handle_search_book(book_list)
            
            elif choice == '3':
                self._handle_save_book(book_list)
            
            elif choice == '4':
                self.view_saved_books()
            
            elif choice == '5':
                self._handle_remove_saved_book()
            
            elif choice == '0':
                self.logout()
                break
            
            else:
                print("Lựa chọn không hợp lệ!")

    def _handle_search_book(self, book_list):
        keyword = input("Nhập từ khóa tìm kiếm: ")
        results = book_list.search_books(keyword)
        if results:
            print(f"\nTìm thấy {len(results)} kết quả:")
            for book in results:
                book.display_info()
        else:
            print("Không tìm thấy sách phù hợp.")

    def _handle_save_book(self, book_list):
        book_id = input("Nhập mã sách muốn lưu: ")
        book = book_list.find_book_by_id(book_id)
        if book:
            self.save_book(book)
        else:
            print("Không tìm thấy sách!")

    def _handle_remove_saved_book(self):
        book_id = input("Nhập mã sách muốn xóa khỏi danh sách yêu thích: ")
        self.remove_saved_book(book_id)

# ========================
# Lớp BookList (Quản lý sách)
# ========================
class BookList:
    def __init__(self):
        self.books = []
    
    def add_book(self, book):
        self.books.append(book)
    
    def remove_book(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                self.books.remove(book)
                return True
        return False
    
    def find_book_by_id(self, book_id):
        return next((book for book in self.books if book.book_id == book_id), None)
    
    def search_books(self, keyword):
        keyword = keyword.lower()
        return [book for book in self.books 
                if (keyword in book.title.lower() or 
                    keyword in book.author.lower() or 
                    (book.category and keyword in book.category.lower()))]
    
    def filter_by_category(self, category):
        return [book for book in self.books if book.category and book.category.lower() == category.lower()]
    
    def filter_by_status(self, status):
        return [book for book in self.books if book.status == status]
    
    def filter_by_date(self, start_date, end_date):
        return [book for book in self.books if start_date <= book.added_date <= end_date]
    
    def display_all_books(self):
        if not self.books:
            print("Thư viện chưa có sách nào.")
        else:
            print("\n--- DANH SÁCH SÁCH ---")
            for book in self.books:
                book.display_info()

# ========================
# Lớp BookManager (Quản lý file)
# ========================
class BookManager:
    @staticmethod
    def save_to_file(book_list, filename="books.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(book_list.books, f)
    
    @staticmethod
    def load_from_file(filename="books.pkl"):
        book_list = BookList()
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                book_list.books = pickle.load(f)
        return book_list

# ========================
# Lớp UserManager (Quản lý người dùng)
# ========================
class UserManager:
    @staticmethod
    def save_to_file(users, filename="users.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(users, f)
    
    @staticmethod
    def load_from_file(filename="users.pkl"):
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                return pickle.load(f)
        return []

    @classmethod
    def login(cls, users):
        username = input("Tên đăng nhập: ")
        password = input("Mật khẩu: ")
        for user in users:
            if user.login(username, password):
                print(f"Đăng nhập thành công! Chào mừng {user.username}.")
                return user
        print("Tên đăng nhập hoặc mật khẩu không đúng!")
        return None

    @classmethod
    def register(cls, users):
        username = input("Tên đăng nhập mới: ")
        if any(user.username == username for user in users):
            print("Tên đăng nhập đã tồn tại!")
            return None
        
        while not InputValidator.validate_username(username):
            print("Tên đăng nhập phải từ 4-20 ký tự, chỉ chứa chữ cái, số và dấu gạch dưới!")
            username = input("Tên đăng nhập mới: ")
        
        password = input("Mật khẩu: ")
        while len(password) < 6:
            print("Mật khẩu phải có ít nhất 6 ký tự!")
            password = input("Mật khẩu: ")
        
        user_id = str(max(int(u.user_id) for u in users) + 1) if users else "1"
        new_user = NormalUser(user_id, username, password)
        users.append(new_user)
        cls.save_to_file(users)
        print("Đăng ký thành công!")
        return new_user

# ========================
# Lớp Application (Chương trình chính)
# ========================
class Application:
    def __init__(self):
        self.book_list = BookManager.load_from_file()
        self.users = UserManager.load_from_file()
        self._initialize_default_admin()

    def _initialize_default_admin(self):
        if not any(user.role == "admin" for user in self.users):
            self.users.append(Admin("1", "admin", "admin123"))
            UserManager.save_to_file(self.users)

    def run(self):
        while True:
            print("\n===== HỆ THỐNG QUẢN LÝ THƯ VIỆN =====")
            print("1. Đăng nhập quản trị")
            print("2. Đăng nhập người dùng")
            print("3. Đăng ký người dùng mới")
            print("0. Thoát chương trình")
            
            choice = input("Chọn chức năng: ")
            
            if choice == '1':
                self._handle_admin_login()
            
            elif choice == '2':
                self._handle_user_login()
            
            elif choice == '3':
                UserManager.register(self.users)
            
            elif choice == '0':
                print("Cảm ơn đã sử dụng hệ thống!")
                break
            
            else:
                print("Lựa chọn không hợp lệ!")

    def _handle_admin_login(self):
        user = UserManager.login(self.users)
        if user and isinstance(user, Admin):
            user.run_menu(self.book_list, self.users)

    def _handle_user_login(self):
        user = UserManager.login(self.users)
        if user and isinstance(user, NormalUser):
            user.run_menu(self.book_list, self.users)

# ========================
# Chạy chương trình
# ========================
if __name__ == "__main__":
    app = Application()
    app.run()

if __name__ == "__main__":
    main()
