# 🚀 HƯỚNG DẪN THIẾT KẾ CÁC PATTERN NÂNG CAO CHO AGENT SKILLS

Khi người dùng yêu cầu thiết kế các Skill phức tạp, có tính logic cao, sinh code/file hoặc chạy các luồng tự động hóa, bạn hãy chủ động tư vấn và áp dụng 6 thiết kế nâng cao dưới đây:

---

## 1. VÒNG LẶP TỰ SỬA LỖI (SELF-HEALING AUDIT LOOP)
- **Khi nào áp dụng**: Các tác vụ sinh code, tạo file, cấu hình hệ thống hoặc chạy script tự động.
- **Cách thiết kế**: Yêu cầu AI không chỉ chạy tạo file mà phải chạy kèm một script kiểm thử độc lập (ví dụ: `audit.py`, `validator.sh`) hoặc thực hiện một quy trình tự kiểm tra.
- **Mẫu chỉ dẫn**:
  > *"Sau khi chạy tạo file [Tên File], bạn BẮT BUỘC phải thực thi script kiểm tra `python scripts/audit.py`. Nếu có lỗi trả về, hãy đọc log lỗi, phân tích nguyên nhân và tự động cập nhật/sửa đổi file cho đến khi script trả về kết quả 0 lỗi (thành công)."*

---

## 2. RANH GIỚI CẤM (NEGATIVE CONSTRAINTS)
- **Khi nào áp dụng**: Khi cần kiểm soát chặt chẽ chất lượng đầu ra, hạn chế các lỗi suy diễn hoặc phong cách viết sáo rỗng của AI.
- **Cách thiết kế**: Tập trung mô tả rõ ràng những gì AI "TUYỆT ĐỐI KHÔNG" được làm thay vì chỉ mô tả cái đúng.
- **Mẫu chỉ dẫn**:
  > *"**Ranh giới cấm nghiêm ngặt (Negative Constraints):**
  > - TUYỆT ĐỐI KHÔNG sử dụng các tính từ sáo rỗng (như 'elegant', 'robust', 'cutting-edge').
  > - KHÔNG dùng tiêu đề dạng cụm danh từ chung chung, phải sử dụng động từ hành động rõ ràng.
  > - KHÔNG tự ý suy đoán hoặc bịa đặt thông tin nếu dữ liệu đầu vào bị thiếu."*

---

## 3. TUYÊN BỐ CÔ LẬP & KẾ THỪA (COMPOSABILITY BOUNDARIES)
- **Khi nào áp dụng**: Khi dự án có nhiều Skill hoạt động song song hoặc các tác vụ dễ bị nhầm lẫn ngữ cảnh.
- **Cách thiết kế**: Tuyên bố rõ ràng ranh giới phạm vi dữ liệu và quy trình mà Skill được phép kế thừa hoặc phải cô lập hoàn toàn.
- **Mẫu chỉ dẫn**:
  > *"**Ranh giới phạm vi (Composability Boundaries):**
  > - Skill này KHÔNG kế thừa quy trình viết từ Skill [Tên Skill Khác], CHỈ kế thừa cấu trúc dữ liệu từ file [Đường Dẫn File].
  > - Mọi thao tác ghi đè chỉ được áp dụng trong thư mục `src/` và không ảnh hưởng đến các thư mục khác."*

---

## 4. XỬ LÝ BUG THƯ VIỆN NGAY TRONG TROUBLESHOOTING (KNOWN-BUGS WORKAROUND)
- **Khi nào áp dụng**: Tác vụ sử dụng các công cụ, thư viện bên thứ ba có lỗi đã biết (Known bugs).
- **Cách thiết kế**: Cung cấp sẵn đoạn code workaround hoặc giải pháp thay thế ngay trong phần Troubleshooting của `SKILL.md` để AI áp dụng thay vì tự mò lỗi và thất bại.
- **Mẫu chỉ dẫn**:
  > *"**Known-Bugs Workaround:**
  > - Lỗi lệch layout khi dùng thư viện python-pptx để vẽ hình: Đảm bảo thiết lập tham số margin cụ thể thông qua hàm `set_slide_margins()` như mẫu code dưới đây thay vì dùng giá trị mặc định:
  >   ```python
  >   slide.width = Inches(13.33)
  >   slide.height = Inches(7.5)
  >   ```"*

---

## 5. ĐỊNH NGHĨA HOÀN THÀNH (DONE LOOKS LIKE) ĐA CHIỀU
- **Khi nào áp dụng**: Mọi Skill chuẩn hóa.
- **Cách thiết kế**: Chia tiêu chí hoàn thành (Done Looks Like) thành các khía cạnh rõ ràng để AI dễ tự đánh giá.
- **Mẫu chỉ dẫn**:
  > *"**DONE LOOKS LIKE ĐA CHIỀU:**
  > - **Khía cạnh Kỹ thuật (Technical):**
  >   - File được tạo đúng đường dẫn tương đối.
  >   - Code không có lỗi cú pháp hoặc cảnh báo linter.
  > - **Khía cạnh Nội dung (Content):**
  >   - Đầy đủ thông tin phản hồi từ người dùng.
  >   - Ngôn từ ngắn gọn, súc tích và đúng tone giọng thương hiệu."*

---

## 6. SKILL LÀ THỰC THỂ SỐNG (LIVING DOCUMENT)
- **Khi nào áp dụng**: Quá trình bảo trì và nâng cấp Skill.
- **Cách thiết kế**: Dẫn dắt người dùng liên tục cập nhật thêm các quy tắc rút ra từ thực tế (Learned Lessons) vào `SKILL.md` dựa trên các lỗi AI thường xuyên mắc phải trong quá trình vận hành thực tế.
