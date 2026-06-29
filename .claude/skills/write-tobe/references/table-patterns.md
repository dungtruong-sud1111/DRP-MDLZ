# MẪU MARKDOWN CHO MỌI LOẠI BẢNG

Dùng pipe-table markdown. Script `md_to_docx.py` sẽ tô header bảng màu #176bb4 (mặc định, đổi theo brand khách) chữ trắng. Hàng tiêu đề LUÔN là dòng đầu của bảng.

---

## A. BẢNG BOILERPLATE

### Trang ký (lặp cho Đơn vị triển khai và cho Khách hàng)
```
**TRANG KÝ ĐƠN VỊ TRIỂN KHAI**

| Vai trò | Tên và chức vụ | Chữ ký | Ngày | Ghi chú |
|---|---|---|---|---|
| Solution Owner | [Tên] | | | |
| PM – Project Manager | [Tên] | | | |
| PD – Project Director | [Tên] | | | |

**TRANG KÝ [KHÁCH HÀNG]**

| Vai trò | Tên người duyệt | Chữ ký | Ngày ký | Ghi chú |
|---|---|---|---|---|
| Người dùng chính | [Tên] | | | |
| Trưởng Ban QLDA | [Tên] | | | |
```

### Quản lý thay đổi
```
| Ngày thay đổi | Mục, bảng, sơ đồ được thay đổi | Mô tả thay đổi | Phiên bản |
|---|---|---|---|
| [dd/mm/yyyy] | Toàn bộ | Tạo mới tài liệu | 1.0 |
```

### Thuật ngữ & viết tắt
```
| Viết tắt | Diễn giải |
|---|---|
| WMS | Hệ thống quản lý kho (Warehouse Management System) |
```

### Legend ký hiệu lưu đồ
```
| Ký hiệu | Mô tả |
|---|---|
| Hình bo tròn (stadium) | Bắt đầu / Kết thúc |
| Hình chữ nhật | Bước thực hiện thủ công (User) |
| Hình chữ nhật (đậm/khác màu) | Bước hệ thống tự động (System) |
| Hình thoi | Ra quyết định / Phân nhánh trường hợp |
| Hình bình hành | Báo cáo / Chứng từ / Dữ liệu |
| Mũi tên | Hướng đi của luồng |
```

---

## B. BẢNG BƯỚC QUY TRÌNH (chọn 1 biến thể đã chốt)

### V1 — User/System (mặc định WMS/Integration/Planning)
```
| Bước thực hiện | Đối tượng thực hiện | Mô tả |
|---|---|---|
| 1.1 Tạo PO | User (Mua hàng) | Người dùng tạo PO trên SAP (NCC, hàng hóa, số lượng, ngày giao…). |
| 1.2 Kiểm tra dữ liệu | System (POMS) | Hệ thống kiểm tra mã NCC, mã hàng, đơn vị tính, kho nhận, mapping. |
| 1.3.1 Tạo PO trên WMS (nhánh đúng) | System (WMS-WEB) | Dữ liệu hợp lệ → tự động tạo PO tương ứng. |
| 1.3.2 Báo lỗi (nhánh sai) | System | Dữ liệu sai → báo lỗi, quy trình tạm dừng. |
```
> Đánh số bước KHỚP với node trong lưu đồ. Nhánh đúng/sai đánh `x.y.1` / `x.y.2`.

### V2 — As-is/To-be
```
| Bước | Phòng ban | Quy trình | As-is | To-be | Hiệu quả |
|---|---|---|---|---|---|
| 1 | Kho | Nhận hàng | Ghi sổ tay, đối chiếu thủ công | Quét QR nhận hàng trên app | Giảm sai sót, nhanh hơn |
```
> Cột **As-is** lấy nguyên văn từ `_TONG-HOP-HIEN-TRANG.md`.

### V3 — Đầy đủ ràng buộc (TMS phức tạp)
```
| Bước | Nội dung thực hiện | Ràng buộc đầu vào | Logic & Nguyên tắc | Kết quả đầu ra | Tài liệu viện dẫn | PIC | Tool |
|---|---|---|---|---|---|---|---|
```

### V4 — Actor đơn giản
```
| Bước | Đối tượng | Mô tả công việc |
|---|---|---|
```

---

## C. ĐẶC TẢ CHỨC NĂNG (domain vận hành)

### Bảng "Các thuộc tính & nghiệp vụ" (theo từng màn hình)
```
| Thuộc tính | Loại | Mô tả | Trường dữ liệu bắt buộc |
|---|---|---|---|
| Danh sách công việc | Văn bản | Tên màn hình | N/A |
| Tìm kiếm | Trường nhập dữ liệu | Dùng để tìm kiếm lệnh | N/A |
| Ngày tạo lệnh | Droplist | Tiêu chí bộ lọc thời gian | N/A |
| Nút Lưu | Nút bấm | Lưu bản ghi | N/A |
```
(Loại thường gặp: Văn bản, Trường nhập dữ liệu, Droplist, Nút bấm, Checkbox, Bảng, Tab.)

### Bảng Usecase & luồng nghiệp vụ
```
| Tổng quan | | |
|---|---|---|
| Tên usecase | [Tên] | |
| Tên tác nhân | [Vai trò] | |
| Mô tả | [Mô tả ngắn] | |
| Điều kiện cần có | [Tiền điều kiện] | |
| Điều kiện hoàn thành | [Hậu điều kiện] | |
| Luồng chính | [Các bước luồng chính] | |
| Luồng phụ / ngoại lệ | [Các nhánh phụ] | |
```

---

## D. BẢNG TÍCH HỢP (file `_TOBE-TICH-HOP.md`)

### Tổng luồng tích hợp
```
| Quy trình | STT | Luồng tích hợp | Từ | Đến | Thao tác |
|---|---|---|---|---|---|
| WMS-SAP 01 | 1 | Master Data SKU (Item) | SAP | WMS | GET |
| WMS-SAP 03 | 4 | Purchase Order | WMS | WMS | POST |
```

### Field mapping (mỗi luồng)
```
| Field | Description | Data Type | Sample | Required |
|---|---|---|---|---|
| sku | Mã hàng | Varchar(32) | 20100101 | Y |
| description | Tên hàng | Varchar(255) | Gạch men 60x60 | Y |
```

---

## E. BẢNG CẤU HÌNH PLANNING (bảng dọc 6 dòng)
```
| Mục đích | [Mục đích thiết lập] | |
|---|---|---|
| Nhân sự chịu trách nhiệm | [Bộ phận] | |
| Hệ thống thao tác | [Hệ thống] | |
| Hệ thống tích hợp | [Hệ thống / Không] | |
| Tần suất | [Lần đầu / Hằng ngày / …] | |
| Phương thức | [Nhập tay / Upload Excel / Tự động] | |
```
> Field spec cấu hình Planning: `Tên trường | Mô tả | Bắt buộc | Ví dụ`.

---

## G. BẢNG TRƯỜNG DỮ LIỆU ĐẦU RA — bản giao khách [CHỈ Planning, khối .4]
Dùng **3 cột** ngôn ngữ nghiệp vụ; KHÔNG để cột "Bắt buộc/Kiểu dữ liệu" (đó là tầng SPEC). Cột "Ý nghĩa" giải nghĩa *trường nói lên điều gì về nghiệp vụ*, KHÔNG viết công thức/nguồn kỹ thuật.
```
| Tên trường | Ý nghĩa | Ví dụ |
|---|---|---|
| Mặt hàng | Tên và mã sản phẩm | Cosy Marie 100g |
| Nhu cầu bán mỗi ngày | Lượng hàng cần xuất bán trung bình mỗi ngày, tính từ dự báo tháng | 200 thùng/ngày |
| Chênh lệch tồn kho | Tồn thực tế trừ tồn hệ thống — phản ánh hàng chưa được ghi nhận kịp | +50 thùng |
| Số ngày còn đủ hàng | Kho còn đủ bán bao nhiêu ngày nữa nếu không nhập thêm | 9 ngày |
| Sản lượng điều chuyển đề xuất | Lượng thực tế sẽ chuyển (không vượt tồn nguồn) | 1.600 thùng |
| Trạng thái | Hệ thống đề xuất / Đã duyệt / Đã điều chỉnh | Đề xuất |
```
> Tên trường tránh mã trần (GAP→"chênh lệch tồn kho", DOI→"số ngày còn đủ hàng" — writing-style #6).

## H. BẢNG VÍ DỤ MÔ PHỎNG — khối .5 [CHỈ Planning]
1 câu nêu thông số áp dụng → bảng **3 cột** chạy từng bước có số → **1 đoạn kết luận văn xuôi** chốt ý nghĩa.
```
Minh họa cho mặt hàng [X]; thông số: [quy cách], [mức dự trữ], [nhu cầu/ngày].

| Nội dung tính | Cách tính | Kết quả |
|---|---|---|
| Tồn kho thực tế | Đọc từ hệ thống kho | 1.800 thùng |
| Số ngày còn đủ hàng | 1.800 ÷ 200 | 9 ngày — thiếu so với mức tối thiểu 14 ngày |
| Lượng bù tồn an toàn | (14 − 9) × 200 | 1.000 thùng |
| … | … | … |
| Quy đổi sang pallet | 1.600 ÷ 60 = 26,67 → làm tròn lên | 27 pallet — trong giới hạn cho phép |
```
> Sau bảng: 1 đoạn văn xuôi tổng kết ("Mặt hàng này vừa thiếu… nên hệ thống đề xuất kéo … , lấy từ … trước, phần còn lại …").
