# KHUNG TÀI LIỆU TO-BE & BOILERPLATE CHUẨN

Thứ tự các phần của một TO-BE Blueprint. Phần BẤT BIẾN áp dụng mọi domain; phần thân lấy skeleton theo domain trong `domain-playbooks.md`.

## A. TRANG BÌA & BOILERPLATE (bất biến)

Theo đúng thứ tự:

1. **Trang bìa:** Tên tài liệu (vd "TÀI LIỆU THIẾT KẾ HỆ THỐNG <TÊN HỆ THỐNG>"), tên khách hàng, "KHÁCH HÀNG – ĐƠN VỊ TRIỂN KHAI", "ngày … tháng … năm …".
2. **Trang ký** — 2 bảng: TRANG KÝ ĐƠN VỊ TRIỂN KHAI và TRANG KÝ <KHÁCH HÀNG>. (tài liệu dạng đề xuất có thể bỏ.)
3. **Quản lý thay đổi** — bảng change log.
4. **Mục lục** (tự sinh khi mở Word; trong .md để heading là đủ).
5. **A. TỔNG QUAN:**
   - Định nghĩa Golive & phạm vi dự án.
   - Thuật ngữ & viết tắt (bảng).
   - Ý nghĩa hình vẽ / Legend ký hiệu lưu đồ (bảng).
6. **Thiết lập hệ thống / Master data** (nếu domain cần): danh mục kho, chủ hàng, khách hàng...

> Mẫu markdown cho các bảng boilerplate (trang ký, quản lý thay đổi, thuật ngữ, legend): xem `table-patterns.md` mục "Bảng boilerplate".

## B. THÂN TÀI LIỆU (theo domain)
Lấy skeleton từ `domain-playbooks.md`. Quy ước chung cho domain VẬN HÀNH (WMS/TMS/SOM): mỗi nghiệp vụ gồm 2 lớp
- **Quy trình nghiệp vụ:** Lưu đồ quy trình + Chi tiết quy trình (bảng bước).
- **Đặc tả yêu cầu chức năng:** mỗi màn hình → Màn hình (placeholder ảnh) + Các thuộc tính & nghiệp vụ (bảng) + Usecase & luồng (bảng).

## C. ĐÁNH SỐ MỤC
- **MẶC ĐỊNH: số thuần `1. → 1.1. → 1.1.1.`** cho toàn tài liệu (kể cả mục lớn). Đây là kiểu chuẩn đang dùng — KHÔNG dùng chữ cái A/B/C cho mục lớn nữa (trừ khi khách yêu cầu rõ).
- **Map cấp heading ↔ độ sâu số:** `# 1.` → Heading1 · `## 1.1.` → Heading2 · `### 1.1.1.` → Heading3. (6 khối Planning của nghiệp vụ `x.y` nằm ở `x.y.1 … x.y.6` = Heading3.)
- **Tự viết số vào tiêu đề markdown** (vd `# 1. TỔNG QUAN`, `## 2.1. Danh mục kho`, `### 4.1.4. Mô tả dữ liệu đầu ra`). Script convert giữ nguyên text tiêu đề, chỉ map cấp `#`→Heading.
- KHÔNG dùng ký tự ① ② ③ làm heading (chỉ để mô tả nội bộ).

## C2. MỤC "CÂU HỎI CÒN MỞ" (cuối tài liệu)
Khi gặp điểm chưa chốt với khách: **thiết kế theo phương án đề xuất của BA ngay tại chỗ** (không để trống, KHÔNG chèn blockquote `[CẦN XÁC NHẬN]` chặn ngang thân) → rồi **gom toàn bộ điểm chờ xác nhận vào MỘT mục cuối tài liệu**:
```
# N. CÂU HỎI CÒN MỞ (Open Questions — cần [KHÁCH] xác nhận)
> Các điểm thiết kế dưới đây do BA đề xuất dựa trên phân tích tài liệu. [KHÁCH] cần xác nhận trước khi chốt/nghiệm thu.

| Mã | Nội dung câu hỏi | Đề xuất của BA | Ảnh hưởng tới mục | Người trả lời |
|---|---|---|---|---|
| OQ-01 | … | … | … | … |
```
> Marker `[CẦN XÁC NHẬN]` chỉ dùng **nội bộ lúc draft**; trước khi giao khách → chuyển hết vào mục Câu hỏi còn mở (self-audit Bước 9 kiểm việc này).

## D. GOLIVE & PHẠM VI — văn mẫu (chỉnh theo dự án)
> Dự án triển khai hệ thống <TÊN HỆ THỐNG> được xác nhận Golive/nghiệm thu giữa hai bên khi:
> + Một là, dữ liệu <kho/đơn/...> của <KHÁCH HÀNG> được đưa lên quản lý trên nền tảng <...>, ký xác nhận bằng biên bản golive.
> + Hai là, hệ thống đáp ứng đủ các tính năng theo mô tả trong tài liệu này. Tính năng mới phát sinh được ghi nhận, đồng ý 2 bên (ngoài phạm vi sẽ tính thêm phí).
> + Ba là, nội dung đặc tả thể hiện trên logic các Quy trình; đến UAT tiếp tục hoàn thiện. Tài liệu hoàn chỉnh được ký bởi các bên.

## E. BỘ THUẬT NGỮ CHUẨN NGÀNH (điền sẵn, bổ sung theo dự án)
| Viết tắt | Diễn giải |
|---|---|
| <ĐVTK> | Tên đơn vị triển khai (điền theo dự án) |
| WMS | Hệ thống quản lý kho (Warehouse Management System) |
| TMS | Hệ thống quản lý vận tải (Transport Management System) |
| SOM | Hệ thống/Mobile app quản lý đặt hàng (Sales Order Management) |
| LPN | License Plate Number — mã định danh pallet trên WMS |
| PO | Purchase Order — đơn/lệnh mua hàng |
| ASN | Advanced Shipping Note — đơn nhập hàng |
| SO | Sales Order — đơn/lệnh xuất bán |
| TO | Transfer Order — đơn chuyển kho |
| POD | Proof of Delivery — chứng từ giao hàng |
| OTIF | On-Time In-Full — giao đúng hạn & đủ |
| FEFO/FIFO | First Expired/In First Out — nguyên tắc xuất hàng |
| RTM | Route to Market — phương án chọn kho theo khách (Planning) |
| S&OP / AOP | Sales & Operations Planning / Annual Operating Plan |

(Giữ + bổ sung thuật ngữ riêng của khách lấy từ AS-IS.)
