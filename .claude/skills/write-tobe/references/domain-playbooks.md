# PLAYBOOK THEO DOMAIN — skeleton + "phương ngữ" bảng

Mỗi domain có: (1) skeleton mục để đưa vào MỤC LỤC KẾ HOẠCH, (2) biến thể bảng bước mặc định, (3) lưu ý đặc thù. Mẫu chi tiết các bảng nằm ở `table-patterns.md`.

## Biến thể BẢNG BƯỚC (chọn ở Bước 3, xác nhận với người dùng)
- **V1 — User/System** (mặc định WMS/Integration/Planning): `Bước thực hiện | Đối tượng thực hiện (User/System) | Mô tả`
- **V2 — As-is/To-be** (mặc định khi muốn nhấn giá trị thay đổi, hay dùng GGG/TTC/SOM): `Bước | Phòng ban | Quy trình | As-is | To-be | Hiệu quả`
- **V3 — Đầy đủ ràng buộc** (TMS phức tạp kiểu Hương Thủy): `Bước | Nội dung thực hiện | Ràng buộc đầu vào | Logic & Nguyên tắc | Kết quả đầu ra | Tài liệu viện dẫn | PIC | Tool`
- **V4 — Actor đơn giản** (đề xuất/tham khảo): `Bước | Đối tượng | Mô tả công việc`

---

## 1. WMS — quản lý kho
**Biến thể mặc định:** V1 (hoặc V2 nếu khách muốn nhấn As-is/To-be).
**Skeleton:**
- Thiết lập hệ thống: Danh mục kho, Danh mục chủ hàng.
- Quy trình nhập hàng (mỗi loại đơn: NCC, nội bộ, hàng bán trả lại, khác).
- Quy trình xuất hàng (xuất bán, ký gửi, trả NCC, khác) — kèm Soạn/Châm/Chỉ định/Đóng/Xuất.
- Quy trình chuyển kho (1 bước / 2 bước).
- Quản lý tồn kho (kiểm kê, di chuyển, đổi trạng thái/lô/mã, đối chiếu).
- Báo cáo.
**Mỗi nghiệp vụ:** Lưu đồ + bảng bước → Đặc tả (Màn hình + thuộc tính + usecase). Phân biệt thao tác **Web** vs **App (handheld)**.

## 2. TMS — quản lý vận tải
**Biến thể mặc định:** V2 hoặc V3 (TMS nhiều ràng buộc).
**Skeleton:**
- Phạm vi & mô hình chuỗi vận hành; lưu đồ End-to-End.
- Quản lý đơn (SO/TO/PO; nội địa, xuất/nhập khẩu, từ sản xuất).
- Điều phối (thủ công + tự động/auto-planning). Nếu có auto-planning: nêu **mô hình VRP, mục tiêu & ràng buộc** (tải trọng, time window, MOQ, giờ hoạt động, điểm cố định, 3D loading), tiêu chí Golive/nghiệm thu, giả định.
- Vận hành chuyến; Đăng tài (gate); Giám sát đa cấp (điều vận/NVT/sales/khách).
- POD (chứng từ giao hàng); thu hồi.
- KPI (OTIF, DIFOT, scorecard NVT); Quản lý nhà vận tải (rate card, lead time); Đối chiếu cước/billing; Tính CO2.
- Báo cáo; Phân quyền.

## 3. SOM — mobile app đặt hàng
**Biến thể mặc định:** V2.
**Skeleton:**
- Tổng quan + cài đặt app + các thay đổi chính so với hiện tại.
- Luồng tạo đơn xuất bán (theo bước: thông tin đơn → kiểm tồn/chỉ định kho/tính cước → giữ tồn → duyệt giá → kiểm công nợ).
- Luồng chỉnh sửa đơn; trả hàng; ký gửi; hủy đơn; xuất mẫu.
- Bảng trạng thái đơn hàng (state enum).
**Đặc thù:** nặng về **màn hình app** + luồng người dùng; mỗi luồng kèm placeholder màn hình.

## 4. CONTROL TOWER — giám sát/BI
**Không phải blueprint vận hành.** Không có lưu đồ quy trình; trọng tâm là **dashboard & KPI**.
**Skeleton:**
- Tổng quan Control Tower; kiến trúc phân loại báo cáo; chiến lược Real-time vs History.
- WMS Management (Inbound, Inventory, Outbound, Productivity).
- TMS Management (Transportation, KPI, Analysis).
- Revenue & Cost (WMS cost + TMS cost).
**Bảng đặc thù:** mỗi báo cáo/dashboard = `Loại báo cáo | Dữ liệu nguồn | Chỉ số/KPI | Người dùng | Tần suất`. KPI điển hình: OTIF, DIFOT, utilization %, aging, cost/đơn vị.

## 5. PLANNING — hoạch định cung-cầu (TMS/SC Planning)
**Cấu trúc KHÁC HẲN vận hành** — kể theo **pipeline** (không theo màn hình vận hành).

**Skeleton LÕI (chung MỌI bài Planning — BẤT BIẾN):** kể theo pipeline
**Setup (Master data & cấu hình) → Input (Demand & Supply) → Logic (nguyên tắc/công thức tính) → Output (kế hoạch đề xuất) → Exception → Integration.**
Áp cho mọi bài Planning (Warehouse Replenishment/DRP/S&OP/Allocation…). Mỗi nghiệp vụ trong pipeline trình bày theo **bố cục 6 khối** ở dưới.

> **Các mục dưới đây là THAM CHIẾU theo LOẠI bài Planning — CHỈ thêm khi bài toán của khách thực sự cần, KHÔNG mặc định bắt buộc, KHÔNG dùng làm checklist chấm điểm:**
> - *(Tham chiếu — mẫu TTC AgriS, bài S&OP/DRP rolling):* chân trời **Monthly/Weekly/Daily rolling**; **Inventory Projection** có cấu trúc; **RTM** (Route to Market); **phasing forecast** (tháng→tuần); **stock policy**; **substitution list**; quy đổi khung xe; phân bổ tỉ lệ NVT.
> - Bài Planning khác (vd **Warehouse Replenishment theo trigger** thiếu hàng/safety/capacity như MDLZ) → các mục TTC trên **KHÔNG áp dụng**; bám skeleton lõi + nhu cầu thật của khách.
> ⚠️ **KHÔNG áp phương ngữ của một khách mẫu (TTC) lên khách khác.**
>
> 📎 Bài Planning lớn kiểu **S&OP/DRP rolling nhiều chân trời** (như TTC) → tham khảo CẤU TRÚC TO-BE vĩ mô A→G ở `references/planning-tobe-ttc-reference.md` (CHỈ tham khảo cấu trúc; nguyên tắc/output/master-data trong đó là dialect TTC, đa số khách đơn giản hơn — đề xuất theo BRD/AS-IS của khách).
**Bảng đặc thù:**
- Cấu hình master data — **bảng dọc 6 dòng:** `Mục đích | Nhân sự chịu trách nhiệm | Hệ thống thao tác | Hệ thống tích hợp | Tần suất | Phương thức`.
- Field spec: `Tên trường | Mô tả | Bắt buộc | Ví dụ`.

**Bố cục MỖI nghiệp vụ Planning — 6 khối (mẫu TTC; chỉ mượn LAYOUT, KHÔNG bê dialect TTC):**

> **Đánh số 6 khối:** dùng số con của nghiệp vụ — nếu nghiệp vụ là `4.1` thì 6 khối là `4.1.1 … 4.1.6` (heading cấp 3). **TUYỆT ĐỐI không dùng ký tự ① ② ③ làm heading** (chỉ dùng để mô tả trong tài liệu này). Mỗi khối kèm câu dẫn nếu là bảng (xem writing-style #2).

- **(.1) Bảng tổng hợp** — câu dẫn ngắn + bảng 6 dòng dọc: `Mục đích | Nhân sự chịu trách nhiệm | Hệ thống thao tác | Hệ thống tích hợp | Tần suất | Phương thức`.
- **(.2) Mục đích** — 1–3 câu WHY theo công thức *pain hiện trạng → giá trị TO-BE* (writing-style #1).
- **(.3) Danh sách tính năng** — câu dẫn + bảng `STT | Tên tính năng | Mô tả` (tên & mô tả bằng **ngôn ngữ nghiệp vụ**, không mã trần — writing-style #6).
- **(.4) Mô tả dữ liệu đầu ra** — trình bày theo **THỨ TỰ** (quy trình trước, dữ liệu sau):
   1. 1 câu mô tả output là gì.
   2. **Lưu đồ quy trình** (chỉ nhãn "Lưu đồ quy trình:" — KHÔNG câu "Lưu đồ thể hiện…"; ưu tiên **swimlane PNG**, xem `swimlane-guide.md`).
   3. **Diễn giải từng bước** dạng **VĂN XUÔI** (không bảng): mỗi bước `**Bước N — <tên>**` rồi nội dung **thụt lề 1 cấp** (dùng blockquote `>` — script tự render thụt lề). Công thức nhúng ngay trong bước theo định dạng `Công thức:/Trong đó:/Ví dụ` (writing-style #7).
   4. **Bảng trường dữ liệu đầu ra** — bản giao khách dùng **3 cột `Tên trường | Ý nghĩa | Ví dụ`** (xem `table-patterns.md` mục G), tên & ý nghĩa bằng ngôn ngữ nghiệp vụ.
- **(.5) Ví dụ mô phỏng** — 1 câu nêu thông số áp dụng + **bảng 3 cột `Nội dung tính | Cách tính | Kết quả`** (mỗi dòng 1 bước có số) + **1 đoạn kết luận văn xuôi** chốt ý nghĩa kết quả (xem `table-patterns.md` mục H).
- **(.6) Quy trình thao tác trên hệ thống** — đường dẫn truy cập (vd "Module X → Chức năng Y") + walkthrough THEO BƯỚC THAO TÁC: mỗi bước = 1 placeholder `[[MH-x.y: …]]` + dòng `_[Chèn ảnh: …]_` + 1–2 câu mô tả. **Mô tả thao tác cũng phải dùng ngôn ngữ nghiệp vụ — KHÔNG để mã trần GAP/DOI/TF/Sum Transfer ở đây** (writing-style #6).
> Lưu đồ (logic) ở khối (.4) và khối (.6) (thao tác UI) là HAI thứ BỔ TRỢ — KHÔNG bỏ (.6) chỉ vì đã có lưu đồ. Nghiệp vụ thuần tính-toán-tự-động vẫn cần (.6) cho phần người dùng review/confirm.

**Liều lượng viết (Planning) — vừa phải, KHÔNG lan man (chuẩn TTC):** dồn độ sâu vào diễn giải CHỖ KHÓ + CÔNG THỨC (vd cap đa tầng = MIN lồng nhau, quy tắc ưu tiên, tách Allocated/Available) + ví dụ số — phần này KHÔNG rút gọn. Cắt giới thiệu dài; KHÔNG để "Diễn giải/Nguồn/Lưu ý" ở MỌI bảng (chỉ chỗ cần); mục dùng-chung (phân quyền/ngoại lệ/vòng đời/truy vết) gói gọn + trỏ tài liệu gốc thay vì nhân bản; field đầu ra rút gọn theo nhóm + trỏ bảng đầy đủ nếu là bản tách/trích.

> Lưu ý: bộ tài liệu Planning tham khảo còn hạn chế (mới 1 mẫu TTC AgriS). Khi gặp tình huống ngoài skeleton → hỏi người dùng, đừng bịa. *(Nguyên tắc chống áp dialect TTC đã nêu ở phần skeleton lõi trên.)*

## 6. INTEGRATION — tích hợp (TÁCH FILE RIÊNG `_TOBE-TICH-HOP.md`)
**Biến thể bảng bước:** V1 (User/System).
**Skeleton:**
- Tổng quan: thuật ngữ; legend; mô hình tích hợp (A ↔ Middleware ↔ B); quy ước (GET/POST/Webhook, xử lý lỗi/retry).
- Bảng tổng **luồng tích hợp:** `Quy trình | STT | Luồng tích hợp | Từ | Đến | Thao tác`.
- (Tùy chọn) Bảng mapping kho/đơn vị: `Tên kho | Mã (WMS) | Owner | Plant | Sloc | Mô tả`.
- Mỗi luồng: Lưu đồ + Diễn giải (bảng bước) + **Field mapping** `Field | Description | Data Type | Sample | Required`.
- Update Result: cách kiểm tra phản hồi tích hợp + ví dụ lỗi & hướng xử lý.
