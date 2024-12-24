import shutil
import pyfiglet
import os
from .constants import check_for_updates

# Phiên bản hiện tại
current_version = check_for_updates()

# Mã ANSI để tạo màu sắc
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
MAGENTA = "\033[35m"
BLUE = "\033[34m"
WHITE = "\033[37m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_title():
    """ Hiển thị tiêu đề chương trình giống như bpytop """
    clear_screen()
    terminal_width = shutil.get_terminal_size().columns

    # Tạo tiêu đề với pyfiglet
    title_text = "E-COMMERCE PACKING"
    ascii_title = pyfiglet.figlet_format(title_text, "slant")
    ascii_lines = ascii_title.splitlines()

    # Hiển thị khung viền và tiêu đề
    print(f"{CYAN}{'=' * terminal_width}{RESET}")
    for line in ascii_lines:
        print(f"{CYAN}{line.center(terminal_width)}{RESET}")
    print(f"{CYAN}{'=' * terminal_width}{RESET}")

    # Thêm thông tin phụ
    print(f"{GREEN} Version: {current_version} | Design by: Justin Nguyen {RESET}")
    print(f"{YELLOW} Telegram: @Justin_Nguyen_97 {RESET}")
    print(f"{RED} Whatsapp: 0982579098 {RESET}")
    print(f"{CYAN}{'=' * terminal_width}{RESET}")

def display_menu():
    """ Hiển thị menu chính với màu sắc và bố cục như bpytop """
    try:
        print_title()

        # Tạo khung menu
        print(f"{BOLD}{GREEN}Chọn một công cụ:{RESET}")
        print(f"{MAGENTA} [1] {WHITE}Đóng hàng{RESET}")
        print(f"{MAGENTA} [2] {WHITE}Tìm mã vận đơn{RESET}")
        print(f"{MAGENTA} [3] {WHITE}Xóa đơn quá 30 ngày{RESET}")
        print(f"{MAGENTA} [4] {WHITE}Đơn quét được trong ngày{RESET}")
        # print(f"{MAGENTA} [5] {WHITE}Làm sạch màn hình{RESET}")
        print(f"{MAGENTA} [5] {WHITE}Thoát chương trình{RESET}")

        print(f"\n{CYAN}{'-' * shutil.get_terminal_size().columns}{RESET}")
        choice = input(f"{YELLOW}Nhập lựa chọn của bạn (1-5): {RESET}").strip()
        return choice
    except KeyboardInterrupt:
        print(f"\n{RED}Dừng chương trình.{RESET}")
        return '5'
