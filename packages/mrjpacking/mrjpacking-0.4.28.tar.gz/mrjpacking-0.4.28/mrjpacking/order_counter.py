import os
from datetime import datetime
from .constants import display_all_orders


def count_orders_today(data_directory):
    """Đếm tổng số đơn quét được trong ngày, phân loại theo trước và sau 2 giờ chiều, và hiển thị mã vận đơn theo bưu cục."""
    today = datetime.now().date()
    count = 0
    orders_info = []  # Danh sách lưu mã vận đơn và thời gian quét
    before_2pm = []   # Danh sách đơn trước 2 giờ chiều
    after_2pm = []    # Danh sách đơn sau 2 giờ chiều
    cutoff_time = datetime(today.year, today.month, today.day, 14, 0, 0)  # 2 giờ chiều hôm nay

    for folder_name in os.listdir(data_directory):
        folder_path = os.path.join(data_directory, folder_name)
        if os.path.isdir(folder_path):
            # Lấy thời gian tạo của thư mục
            creation_time = os.path.getctime(folder_path)
            creation_datetime = datetime.fromtimestamp(creation_time)

            # Kiểm tra xem thư mục có được tạo trong ngày hôm nay không
            if creation_datetime.date() == today:
                count += 1
                orders_info.append((folder_name, creation_datetime))

                # Phân loại đơn hàng theo thời gian quét
                if creation_datetime < cutoff_time:
                    before_2pm.append((folder_name, creation_datetime))
                else:
                    after_2pm.append((folder_name, creation_datetime))

    orders_info_sorted = sorted(orders_info, key=lambda x: x[1])  # Sắp xếp theo thời gian

    # Hiển thị thông tin mã vận đơn theo bưu cục
    if orders_info_sorted:
        display_all_orders(orders_info_sorted)

    # Hiển thị số lượng đơn trước và sau 2 giờ chiều
    print(f"\nĐơn quét trước 14 giờ: {len(before_2pm)}")
    print(f"Đơn quét sau 14 giờ: {len(after_2pm)}")

    return count

