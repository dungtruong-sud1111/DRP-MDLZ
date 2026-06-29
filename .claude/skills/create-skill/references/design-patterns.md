# 🎨 5 DESIGN PATTERNS THIẾT KẾ SKILL NÂNG CAO

Khi thiết kế Skill cho người dùng, bạn cần nhận diện mục đích sử dụng để tư vấn và áp dụng 1 trong 5 Pattern thiết kế chuẩn Anthropic dưới đây nhằm tối ưu hóa hiệu năng và trải nghiệm tương tác:

---

## 1. SEQUENTIAL WORKFLOW ORCHESTRATION (Quy trình cố định từng bước)
- **Định nghĩa**: Áp dụng khi luồng công việc cần thực hiện theo các bước cố định, bước sau kế thừa kết quả của bước trước.
- **Khi nào áp dụng**: Onboarding nhân viên mới, tạo deal bán hàng trên CRM, phê duyệt đơn nghỉ phép, hoặc xử lý khiếu nại khách hàng theo phân cấp.
- **Mẫu tư duy thiết kế**:
  - Chia nhỏ quy trình thành các bước tuyến tính rõ ràng: Bước 1 -> Bước 2 -> Bước 3.
  - Yêu cầu AI hoàn thành và kiểm tra kỹ từng bước trước khi chuyển sang bước tiếp theo.
  - Ví dụ: `onboard-nhan-vien` gồm (1) Tạo tài khoản -> (2) Phân quyền -> (3) Gửi thư chào mừng.

---

## 2. MULTI-MCP COORDINATION (Điều phối đa dịch vụ)
- **Định nghĩa**: Áp dụng khi luồng công việc yêu cầu tương tác với nhiều dịch vụ, công cụ hoặc nguồn dữ liệu khác nhau thông qua Model Context Protocol (MCP).
- **Khi nào áp dụng**: Bàn giao từ Thiết kế sang Lập trình (Figma + Jira + GitHub), Dashboard điều hành lấy dữ liệu từ nhiều nguồn (Slack + Notion + Google Drive).
- **Mẫu tư duy thiết kế**:
  - Hướng dẫn AI cách phối hợp gọi các công cụ MCP khác nhau một cách nhịp nhàng.
  - Định nghĩa rõ dữ liệu từ công cụ A sẽ được biến đổi và truyền vào công cụ B như thế nào.

---

## 3. ITERATIVE REFINEMENT (Tối ưu hóa lặp lại/Kiểm duyệt)
- **Định nghĩa**: Áp dụng khi chất lượng sản phẩm đầu ra tăng lên rõ rệt qua mỗi vòng lặp đánh giá, kiểm thử hoặc tối ưu.
- **Khi nào áp dụng**: Tạo báo cáo phân tích sâu, viết content marketing qua nhiều vòng kiểm duyệt, hoặc sinh mã nguồn có kèm vòng lặp chạy test & fix lỗi.
- **Mẫu tư duy thiết kế**:
  - Tạo cấu trúc gồm 3 phần: Sinh nội dung -> Đánh giá đối chiếu -> Tinh chỉnh tối ưu.
  - Yêu cầu AI tự động đóng vai trò là bên phản biện (Validator) để tự chấm điểm và sửa đổi kết quả cho đến khi đạt barem chất lượng đề ra.

---

## 4. CONTEXT-AWARE TOOL SELECTION (Lựa chọn công cụ theo ngữ cảnh)
- **Định nghĩa**: Áp dụng khi có cùng một mục tiêu đầu ra, nhưng các công cụ hoặc phương pháp thực hiện sẽ thay đổi linh hoạt tùy thuộc vào dữ liệu đầu vào hoặc bối cảnh cụ thể.
- **Khi nào áp dụng**: Lưu trữ file thông minh (tự động phân loại file PDF/Word/Excel để gọi tool đọc tương ứng), chọn framework tối ưu hóa quảng cáo dựa trên ngân sách chiến dịch.
- **Mẫu tư duy thiết kế**:
  - Dạy AI cách nhận diện các nhánh điều kiện (If-Else) dựa trên input của người dùng.
  - Cung cấp tiêu chí phân loại rõ ràng để AI tự quyết định phương án hành động phù hợp nhất.

---

## 5. DOMAIN-SPECIFIC INTELLIGENCE (Tích hợp tri thức chuyên ngành)
- **Định nghĩa**: Áp dụng khi Skill cần nhúng sẵn các tri thức chuyên môn sâu vượt trội hơn khả năng suy luận thông thường của AI để giải quyết bài toán nghiệp vụ phức tạp.
- **Khi nào áp dụng**: Kiểm tra tuân thủ điều khoản tài chính quốc tế, đánh giá CV ứng viên dựa trên luật lao động bản địa, hoặc tư vấn kỹ thuật theo chuẩn ISO.
- **Mẫu tư duy thiết kế**:
  - Tách tri thức chuyên ngành hoặc bộ quy chuẩn dày đặc ra thư mục `references/`.
  - Hướng dẫn AI bắt buộc phải tra cứu tri thức này trước khi ra quyết định hoặc phản hồi người dùng.

---

## 📊 MA TRẬN CHỌN PATTERN NHANH
| Nhu cầu của người dùng | Pattern tối ưu nên đề xuất |
| :--- | :--- |
| Quy trình cố định, bước nối tiếp bước | **Pattern 1: Sequential** |
| Tương tác/kết nối đa công cụ (Notion, Drive, Slack...) | **Pattern 2: Multi-MCP** |
| Sản phẩm đầu ra cần tinh chỉnh, sinh code hoặc audit tự động | **Pattern 3: Iterative Refinement** |
| Nhận diện kiểu dữ liệu đầu vào để chọn cách xử lý tương ứng | **Pattern 4: Context-Aware** |
| Cần nhúng sâu tri thức chuyên môn (Luật, Tài chính, Y tế...) | **Pattern 5: Domain-Specific** |
