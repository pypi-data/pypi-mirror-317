import os
import subprocess

def search_tracking_id(data_directory):
    while True:
        tracking_id = input("\nNhập mã vận đơn (gõ 'exit' hoặc 'ex' để thoát): ").strip()
        
        # Kiểm tra nếu người dùng nhập 'exit' hoặc 'ex'
        if tracking_id.lower() in ['exit', 'ex']:
            # print("\nĐã thoát khỏi chương trình.")
            break

        # Kiểm tra nếu người dùng không nhập gì
        if not tracking_id:
            print("\nVui lòng nhập mã vận đơn.")
            continue

        tracking_dir = os.path.join(data_directory, tracking_id)
        if os.path.exists(tracking_dir):
            print(f"Mở thư mục: {tracking_dir}")
            if os.name == 'nt':  # Windows
                os.startfile(tracking_dir)
            elif os.name == 'posix':  # MacOS, Linux
                subprocess.call(['open', tracking_dir] if os.uname().sysname == 'Darwin' else ['xdg-open', tracking_dir])
        else:
            print("\nKhông tìm thấy mã đơn hàng.")
