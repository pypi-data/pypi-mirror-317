import os
import time
import shutil
from .menu import print_title
from tkinter import Tk
from tkinter.filedialog import askdirectory
from .constants import MAX_FOLDER_AGE_SECONDS
from shutil import get_terminal_size

MAX_FOLDER_AGE_SECONDS = 30 * 24 * 3600  # 30 ngày

def clear_console():
    """Xóa màn hình console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def list_old_folders(data_directory):
    """Liệt kê các thư mục đã được tạo quá 30 ngày."""
    current_time = time.time()
    old_folders = []

    for folder_name in os.listdir(data_directory):
        folder_path = os.path.join(data_directory, folder_name)
        if os.path.isdir(folder_path):
            folder_creation_time = os.path.getctime(folder_path)
            folder_age = current_time - folder_creation_time

            if folder_age >= MAX_FOLDER_AGE_SECONDS:
                old_folders.append(folder_name)

    return old_folders

def print_table(folders):
    """In tên các thư mục theo dạng bảng ngang, tự động xuống dòng khi đạt giới hạn chiều rộng terminal."""
    if not folders:
        print("Không có thư mục nào quá 30 ngày.")
        return

    terminal_width = get_terminal_size((80, 20)).columns
    column_width = max([len(folder) for folder in folders]) + 4
    columns_per_row = max(1, terminal_width // column_width)

    rows = [folders[i:i + columns_per_row] for i in range(0, len(folders), columns_per_row)]

    for row in rows:
        print(" | ".join(f"{folder:<{column_width}}" for folder in row))  # Thêm dấu "|"


def delete_old_folders(data_directory):
    current_time = time.time()
    folder_count_del = 0
    for folder_name in os.listdir(data_directory):
        folder_path = os.path.join(data_directory, folder_name)
        if os.path.isdir(folder_path):
            folder_creation_time = os.path.getctime(folder_path)
            folder_age = current_time - folder_creation_time
            if folder_age >= MAX_FOLDER_AGE_SECONDS:
                shutil.rmtree(folder_path)
                folder_count_del += 1
                # print(f"\nĐã xóa thư mục: {folder_name} vì đã đủ 30 ngày.")
    print(f"\nĐã xóa {folder_count_del} thư mục quá 30 ngày.")

def ask_to_delete_old_folders(data_directory):
    old_folders = list_old_folders(data_directory)
    folder_count = len(old_folders)
    if old_folders:
        print("\nCác thư mục đã tạo quá 30 ngày:")
        print_table(old_folders)  # In theo dạng bảng
        
        while True:
            answer = input(f"Bạn có muốn xóa {folder_count} thư mục này không? (y/n): ").strip().lower()
            if answer == 'y':
                delete_old_folders(data_directory)
                break  # Thực thi xong và thoát khỏi vòng lặp
            elif answer == 'n':
                print("Quá trình xóa đã bị hủy.")
                break  # Thoát khỏi vòng lặp mà không làm gì
            else:
                print("Vui lòng nhập 'y' (có) hoặc 'n' (không).")  # Thông báo nếu nhập sai
    else:
        print("\nKhông có thư mục nào quá hạn để xóa.")


def select_data_directory():

    print_title()

    """Hàm này cho phép người dùng chọn thư mục lưu hoặc nhập đường dẫn."""
    print("\nChọn thư mục lưu trữ hoặc nhập đường dẫn trực tiếp:")
    selected_dir = input("Nhập đường dẫn lưu trữ (hoặc bấm Enter để mở thư mục chọn): ").strip()

    # Nếu người dùng không nhập, yêu cầu họ chọn thư mục
    if not selected_dir:
        try:
            import tkinter as tk
            from tkinter import filedialog

            root = tk.Tk()
            root.withdraw()  # Ẩn cửa sổ chính
            selected_dir = filedialog.askdirectory()  # Mở hộp thoại chọn thư mục
        except ImportError:
            print("Không thể sử dụng giao diện đồ họa. Vui lòng nhập đường dẫn thủ công.")
    
    # Kiểm tra nếu người dùng vẫn không chọn hoặc nhập, thoát chương trình
    if not selected_dir or not os.path.exists(selected_dir):
        print("Không chọn thư mục. Chương trình sẽ kết thúc.")
        exit()

    print(f"Thư mục lưu trữ đã chọn: {selected_dir}")
    return selected_dir

def create_tracking_directory(data_dir, tracking_id):
    """Tạo thư mục cho mã vận đơn mới."""
    tracking_dir = os.path.join(data_dir, tracking_id)
    os.makedirs(tracking_dir, exist_ok=True)
    return tracking_dir
