# HƯỚNG DẪN VIẾT `_DANH-SACH-MAN-HINH.md`

File này mô tả từng màn hình để bạn đưa cho công cụ thiết kế (vd skill design) dựng mockup, rồi chèn ảnh vào TO-BE theo ID.

## NGUYÊN TẮC KHỚP ID 1-1
- Trong `_TOBE-BLUEPRINT.md`, mỗi chỗ cần ảnh đặt placeholder: `[[MH-<số mục>: <Tên màn hình>]]`
  - Ví dụ: `[[MH-3.1: Danh sách Lệnh châm hàng]]`
- Trong `_DANH-SACH-MAN-HINH.md`, mỗi màn hình một khối có **đúng ID đó**. Self-audit kiểm tra mọi placeholder đều có khối mô tả và ngược lại.

## QUY ƯỚC ĐẶT ID
- `MH-<mã mục cha>.<thứ tự>`: vd nghiệp vụ Châm hàng (mục 3) → `MH-3.1`, `MH-3.2`...
- ID là duy nhất toàn tài liệu.

## KHUÔN MỘT KHỐI MÔ TẢ MÀN HÌNH
```
### [[MH-3.1: Danh sách Lệnh châm hàng]]
- **Hệ thống / nền tảng:** WMS Web | Mobile App (handheld)
- **Mục đích màn hình:** (1 câu)
- **Bố cục tổng thể:** (header/toolbar, vùng bộ lọc, bảng danh sách, vùng chi tiết, nút hành động...)
- **Thành phần & trường chính:** (liệt kê — tên trường, loại: text/droplist/nút/checkbox/bảng)
  - VD: Thanh tìm kiếm; bộ lọc Ngày tạo lệnh (droplist); bảng danh sách (cột: Mã lệnh, Trạng thái, Kho, Ngày); nút Tạo, nút In.
- **Trạng thái / biến thể:** (rỗng/loading/lỗi; trạng thái đơn nếu có)
- **Gợi ý thiết kế / lưu ý thương hiệu:** (màu chủ đạo theo brand khách — mặc định #176bb4, font, mật độ thông tin...)
- **Tham chiếu nghiệp vụ:** (mục/usecase liên quan trong blueprint)
```

## LƯU Ý
- Mô tả ĐỦ để dựng mockup trung thực (đừng quá sơ sài), nhưng KHÔNG bịa trường không có cơ sở từ AS-IS/sản phẩm — chỗ chưa rõ ghi `[CẦN XÁC NHẬN: ...]`.
- Nếu nhiều màn hình giống nhau (vd list + detail), tách thành các MH riêng để dễ chèn ảnh.
- Giữ thứ tự khối theo thứ tự xuất hiện trong blueprint cho dễ đối chiếu.
- **[Planning — khối ⑥ bố cục 6 khối] Walkthrough thao tác:** một nghiệp vụ Planning có thể có NHIỀU placeholder màn hình, MỖI BƯỚC THAO TÁC một ID (`MH-x.y` tăng dần: xem danh sách → soi chi tiết → chỉnh sửa → gửi review → duyệt…). Mỗi ID vẫn có một khối mô tả tương ứng ở file này. Đây là cách thể hiện "quy trình thao tác nhiều ảnh" giống TTC.
