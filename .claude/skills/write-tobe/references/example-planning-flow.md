# FEW-SHOT: MỘT NGHIỆP VỤ PLANNING ĐẠT CHUẨN GIAO KHÁCH

> **Khi nào đọc:** đang viết nghiệp vụ domain **Planning** theo 6 khối → dùng file này làm KHUÔN về *cấu trúc, giọng văn, mức chi tiết, định dạng công thức*. Bắt chước **KIỂU**, KHÔNG copy nội dung (số liệu/công thức/tên màn hình bên dưới là của ví dụ In-In BKD — dữ liệu riêng, không hardcode sang khách khác).
> **Lưu ý chống lỗi:** khối `.6` dưới đây đã **dọn sạch mã kỹ thuật** (không GAP/DOI/TF/Sum Transfer) — đúng writing-style #6; đừng học theo bản còn jargon.

---

## 4.1. In-In BKD — Điều chuyển nội bộ phục vụ bán (BKD2/BKD3 → BKD1)

### 4.1.1. Bảng tổng hợp
Bảng dưới tóm tắt các thông tin nền của nghiệp vụ (ai làm, trên hệ thống nào, tần suất, phương thức):

| Hạng mục | Nội dung |
|---|---|
| Mục đích | Tự động xác định sản lượng cần điều chuyển từ BKD2/BKD3 về BKD1 mỗi chu kỳ để BKD1 đủ hàng bán mà vẫn trong năng lực điều chuyển |
| Nhân sự chịu trách nhiệm | Warehouse Planner (chủ trì, duyệt); hệ thống tính & đề xuất tự động |
| Hệ thống thao tác | SMARTLOG Supply Chain Planning |
| Tần suất | Hằng ngày — chu kỳ D+1, chốt số liệu 16h00 ngày D |
| Phương thức | Hệ thống tự đề xuất → Planner review & xác nhận |

### 4.1.2. Mục đích
Hiện nay mỗi ngày Warehouse Planner phải mở nhiều sheet Excel, tự đối chiếu tồn rồi tính tay lượng cần kéo hàng từ kho nhập xưởng về kho bán — phụ thuộc kinh nghiệm, dễ sai, khó bàn giao. Nghiệp vụ này số hóa toàn bộ chuỗi đó: hệ thống tự đề xuất *chuyển bao nhiêu, lấy từ kho nào*, để planner chỉ còn rà soát và xác nhận.

### 4.1.3. Danh sách tính năng
Hệ thống cung cấp các tính năng sau để thực hiện nghiệp vụ:

| STT | Tên tính năng | Mô tả |
|---|---|---|
| 1 | Kiểm tra tồn kho & phát hiện chênh lệch | Đọc tồn từ 2 nguồn (hệ thống ERP & hệ thống kho thực tế), so sánh để phát hiện phần chênh lệch chưa ghi nhận kịp |
| 2 | Tính lượng bù tồn an toàn | So số ngày còn đủ hàng với mức dự trữ tối thiểu để ra lượng cần kéo thêm |
| 3 | Tính lượng bù cho kế hoạch bán | So tồn kho với đơn hàng ngày mai (GT + MT); thiếu thì tính lượng cần bù, làm tròn theo pallet |
| 4 | Chốt & phân nguồn điều chuyển | Giới hạn theo tồn nguồn, ưu tiên BKD2 trước BKD3, kiểm năng lực 500 pallet/ngày |
| 5 | Duyệt & xác nhận | Planner điều chỉnh nếu cần, xác nhận → khóa số liệu & phát sinh lệnh |

### 4.1.4. Mô tả dữ liệu đầu ra
Đầu ra là Bảng đề xuất điều chuyển theo từng mặt hàng: cần chuyển bao nhiêu về BKD1, lấy từ kho nào, quy ra pallet.

**Lưu đồ quy trình:**

```mermaid
# src: in-in-bkd
flowchart TD
    Start([Bắt đầu]) --> S1[B1. Lấy nhu cầu bán/ngày]
    ... (giữ mermaid làm nguồn logic; bản giao khách dùng PNG swimlane)
```

**Diễn giải từng bước:**

**Bước 1 — Xác định nhu cầu bán trung bình mỗi ngày**
> Hệ thống lấy nhu cầu bán/ngày cho từng mặt hàng làm nền tính toán.
>
> **Công thức: Nhu cầu bán/ngày = Dự báo tháng × % Phân bổ kho trong ÷ Số ngày bán hàng trong tháng**
>
> Trong đó:
> - **Dự báo tháng**: do Demand Planning cấp từ IBP; nạp tại màn hình *Tiếp nhận Forecast IBP* của module *Hoạch định nhu cầu* (mục 3.1).
> - **% Phân bổ kho trong**: tỷ lệ phân bổ về kho BKD, theo loại hàng & kênh; thiết lập tại màn hình *Thiết lập tỷ lệ phân bổ* của module *Thiết lập tham số Planning động* (mục 2.4).
> - **Số ngày bán hàng/tháng**: hiện 26 ngày; thiết lập tại màn hình *Thiết lập số ngày bán hàng* (mục 2.4).
>
> Ví dụ: 500.000 thùng × 70% ÷ 26 ngày = **13.462 thùng/ngày**.

*(… Bước 2–9 cùng kiểu: mỗi bước = tiêu đề + nội dung thụt lề + Công thức/Trong đó/Ví dụ khi có …)*

**Bảng trường dữ liệu đầu ra** (3 cột — xem `table-patterns.md` mục G):

| Tên trường | Ý nghĩa | Ví dụ |
|---|---|---|
| Mặt hàng | Tên và mã sản phẩm | Cosy Marie 100g |
| Chênh lệch tồn kho | Tồn thực tế trừ tồn hệ thống | +50 thùng |
| Số ngày còn đủ hàng | Còn đủ bán bao nhiêu ngày nếu không nhập thêm | 9 ngày |
| Sản lượng điều chuyển đề xuất | Lượng thực tế sẽ chuyển | 1.600 thùng |

### 4.1.5. Ví dụ mô phỏng
Minh họa cho Cosy Marie 100g; quy cách 60 thùng/pallet, mức dự trữ tối thiểu 14 ngày, nhu cầu 200 thùng/ngày.

| Nội dung tính | Cách tính | Kết quả |
|---|---|---|
| Số ngày còn đủ hàng | 1.800 ÷ 200 | 9 ngày — thiếu so với 14 ngày |
| Lượng bù tồn an toàn | (14 − 9) × 200 | 1.000 thùng |
| Quy đổi pallet | 1.600 ÷ 60 → làm tròn lên | 27 pallet |

Mặt hàng này vừa thiếu hàng dự trữ vừa thiếu cho kế hoạch bán, nên hệ thống đề xuất kéo 1.600 thùng = 27 pallet, lấy từ BKD2 trước, phần còn lại từ BKD3 — trong giới hạn cho phép.

### 4.1.6. Quy trình thao tác trên hệ thống
**Đường dẫn:** Module Điều chuyển → chức năng In-In BKD → chọn ngày chu kỳ.

**Bước 1 — Mở chu kỳ điều chuyển.** Planner chọn ngày và phạm vi kho; hệ thống hiển thị dữ liệu đầu vào đã sẵn sàng hay chưa.

[[MH-D.1.1: Màn hình tổng quan chu kỳ điều chuyển]]
_[Chèn ảnh: chọn ngày + checklist dữ liệu đầu vào]_

**Bước 2 — Xem tồn kho & chênh lệch.** Hệ thống hiển thị tồn từ hai nguồn và phần chênh lệch của từng kho theo mặt hàng để planner soi nhanh. *(dùng "chênh lệch tồn kho", KHÔNG ghi "GAP")*

[[MH-D.1.2: Màn hình tồn kho & chênh lệch]]
_[Chèn ảnh: bảng tồn 2 nguồn + cột chênh lệch tô màu]_

**Bước 3 — Xem kết quả tính nhu cầu.** Hệ thống trình lượng bù tồn an toàn và lượng bù cho kế hoạch bán theo mặt hàng, kèm số ngày còn đủ hàng để planner hiểu vì sao phát sinh nhu cầu. *(KHÔNG ghi "TF for Safety/Sale", "DOI")*

[[MH-D.1.3: Màn hình kết quả tính nhu cầu]]
_[Chèn ảnh: bảng nhu cầu theo mặt hàng]_

**Bước 4 — Rà soát đề xuất.** Hệ thống trình sản lượng điều chuyển đã phân nguồn và quy ra pallet; cảnh báo nếu vượt năng lực. Planner điều chỉnh nếu cần.

[[MH-D.1.4: Màn hình đề xuất điều chuyển]]
_[Chèn ảnh: bảng đề xuất + phân nguồn + cảnh báo]_

**Bước 5 — Xác nhận & chốt.** Planner duyệt; hệ thống khóa số liệu chu kỳ và phát sinh lệnh điều chuyển.

[[MH-D.1.5: Màn hình xác nhận & chốt lệnh]]
_[Chèn ảnh: xác nhận + trạng thái khóa + danh sách lệnh]_
