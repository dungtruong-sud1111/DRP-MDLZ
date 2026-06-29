# Thư viện Icon Doanh nghiệp chuẩn mã nguồn — Enterprise Icons (V5.1 Standard)

Tài liệu này danh mục hóa toàn bộ **85+ icon Logistics & Chuỗi cung ứng cao cấp** đã được trích xuất trực tiếp từ PowerPoint Template chuẩn 2025 của doanh nghiệp. 

Các tệp ảnh icon nằm tại thư mục:  
`c:\1. FOR STUDY\0.5. create-skills\.claude\skills\design-pptx\assets\icons\`

---

## 1. Danh mục Icon theo Nhóm Nghiệp vụ

### Nhóm A: Nghiệp vụ & Vận hành (Operations & Flow)
* **`booking.png`**: Nghiệp vụ đặt chỗ, lên lịch gửi hàng (Booking).
* **`tracking.png`**: Theo dõi hành trình, giám sát vận tải (Tracking).
* **`matching.png`**: Khớp nối thông tin, ghép xe, ghép chuyến (Matching).
* **`execution.png`**: Thực thi vận hành, triển khai tác vụ (Execution).
* **`reconciliation.png`**: Đối soát tài chính, kiểm toán, đối chiếu (Reconciliation).
* **`reverse.png`**: Logistics ngược, thu hồi, đổi trả (Reverse Logistics).

### Nhóm B: Địa điểm & Thực thể (Supply Chain Nodes)
* **`cang.png` / `cang_1.png`**: Cảng biển, cảng xếp hàng (Loading Port).
* **`cang_ich.png`**: Cảng đích, cảng dỡ hàng (Destination Port).
* **`depot.png`**: Cảng cạn, bãi container (Depot / Container Yard).
* **`nha_may.png`**: Nhà máy, cơ sở sản xuất (Factory / Plant).
* **`kho_bai.png` / `kho_hang.png` / `kho_hang_1.png` / `kho_hang_2.png`**: Kho hàng, trung tâm phân phối (Warehouse / DC).
* **`chinh_phu.png`**: Cơ quan hải quan, thuế quan, chính phủ (Customs / Government).
* **`xnk.png`**: Khu vực xuất nhập khẩu, thương mại quốc tế (Import / Export).
* **`depot.png`**: Trạm trung chuyển, bãi đỗ (Depot).

### Nhóm C: Phương thức Vận tải (Transport Modes)
* **`van_tai.png` / `van_tai_1.png` / `van_tai_2.png` / `van_tai_3.png`**: Xe tải, vận tải đường bộ (Truck / Road Transport).
* **`van_tai_bien.png`**: Tàu container, vận tải đường biển (Container Vessel / Ocean Freight).
* **`xa_lan.png`**: Xà lan, vận tải đường thủy nội địa (Barge).
* **`a_phuong_thuc.png`**: Vận tải đa phương thức, kết hợp bộ-biển-sắt (Multimodal).

### Nhóm D: Công nghệ & Giải pháp (Technology & Systems)
* **`control_tower.png`**: Trung tâm điều hành thông minh, tháp điều khiển (Control Tower).
* **`port_optimization.png`**: Hệ thống tối ưu hóa cảng, xếp dỡ (Port Optimization).
* **`4pl_5pl_services.png`**: Dịch vụ tích hợp logistics bên thứ 4/thứ 5 (4PL / 5PL Services).
* **`digital_win.png`**: Chuyển đổi số, giải pháp công nghệ số (Digital Transformation / Win).

---

## 2. Hướng dẫn lập trình Chèn Icon trong `build_deck.py`

Khi sinh mã Python, bạn chèn icon vào các thẻ card hoặc đầu đề slide bằng phương thức `add_picture`.

### Nguyên tắc căn lề & kích thước chuẩn:
* **Icon lồng trong Shape tròn (Circular Highlight Badge):** Kích thước tròn `0.38 inch`, kích thước icon bên trong `0.21 inch` (tỷ lệ 55% để đảm bảo padding đẹp mắt).
* **Icon tiêu đề slide:** Kích thước `0.45 x 0.45 inch`, đặt ở góc trái trước tiêu đề.

### Đoạn mã ví dụ chèn Icon vào Slide:

```python
import os
from pptx.util import Inches

# Đường dẫn gốc tới thư mục chứa assets của Skill
ICON_DIR = r"C:\1. FOR STUDY\0.5. create-skills\.claude\skills\design-pptx\assets\icons"

def add_icon_badge(slide, icon_filename, cx, cy):
    """
    Vẽ một badge tròn màu Orange cao cấp và lồng icon màu trắng vào giữa.
    cx, cy: tọa độ tâm của badge tròn.
    """
    icon_path = os.path.join(ICON_DIR, icon_filename)
    if not os.path.exists(icon_path):
        # Tránh lỗi crash nếu thiếu file ảnh
        return
        
    badge_size = Inches(0.38)
    icon_size = Inches(0.21)
    
    # 1. Vẽ hình tròn nền màu Orange
    badge = make_shape(slide, MSO_SHAPE.OVAL, 
                       cx - badge_size/2, cy - badge_size/2, 
                       badge_size, badge_size, 
                       fill=ORANGE, line=None)
                       
    # 2. Chèn đè icon ảnh lên trên hình tròn
    slide.shapes.add_picture(icon_path, 
                             cx - icon_size/2, cy - icon_size/2, 
                             icon_size, icon_size)
```

---

## 3. Cách Sử dụng Đóng khung / Highlight Icon (Từ Slide 17 của Mẫu)

Theo hướng dẫn sử dụng PPT Template 2025:
* **Ưu tiên không đóng khung** khi icon đứng độc lập làm hình họa minh họa chung.
* **Đóng khung tròn khi cần highlight** (ví dụ: làm mốc quy trình, làm đầu mục tính năng chính):
  * **Phương án A (Nền sáng):** Nền hình tròn màu `PALE_BLUE` (`#ECF3FF`) + Icon vẽ đè lên.
  * **Phương án B (Nền đậm):** Nền hình tròn màu `PRIMARY` (`#2933D9`) hoặc `ACCENT` (`#3543F6`) + Icon âm bản (màu trắng).
