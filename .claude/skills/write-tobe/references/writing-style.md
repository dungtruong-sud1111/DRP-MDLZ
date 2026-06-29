# VĂN PHONG & DIỄN GIẢI TÀI LIỆU TO-BE (cho khách hàng nghiệp vụ)

TO-BE là deliverable đọc bởi **NGƯỜI NGHIỆP VỤ** của khách (vận hành, kế hoạch, quản lý) — KHÔNG phải dev. Viết để họ hiểu **"làm gì, vì sao, được gì"**, không sa vào ngôn ngữ kỹ thuật. Đúng cấu trúc chưa phải xong — tài liệu phải **đọc được**.

## 1. WHY trước WHAT — mở đầu bằng "Mục đích"
Mỗi mục/nghiệp vụ mở đầu bằng 1–3 câu **Mục đích** bằng NGÔN NGỮ NGHIỆP VỤ: mục này giải quyết bài toán gì, phục vụ ai, cho ra giá trị gì.
> ✅ "Mục đích: Thiết lập lead time giao hàng nhằm tính được ngày dự kiến xuất hàng cho từng khách, làm căn cứ để hệ thống tự đề xuất kế hoạch chuyển kho đúng hạn."
> ❌ "Bảng cấu hình lead_time gồm các trường site_code, region, lead_days, transport_mode."

**Công thức câu Mục đích hiệu quả nhất — nêu PAIN hiện trạng → giá trị TO-BE:** mô tả cách làm thủ công đang đau ở đâu, rồi nghiệp vụ này số hóa/giải quyết ra sao.
> ✅ "Hiện nay mỗi ngày planner phải mở nhiều sheet Excel, tự đối chiếu tồn rồi tính tay lượng cần kéo về — phụ thuộc kinh nghiệm, dễ sai, khó bàn giao. Nghiệp vụ này số hóa toàn bộ chuỗi đó: hệ thống tự đề xuất chuyển bao nhiêu, lấy từ kho nào, để planner chỉ còn rà soát và xác nhận."

## 2. Bảng cần câu dẫn; lưu đồ quy trình chuẩn thì KHÔNG
- **BẢNG dữ liệu:** trước MỖI bảng → 1–2 câu dẫn giải (bảng thể hiện gì, đọc theo hướng nào, điểm cần chú ý). KHÔNG để bảng "trần".
- **LƯU ĐỒ quy trình chuẩn (swimlane / flowchart):** chỉ cần **nhãn ngắn** ("Lưu đồ quy trình:"); phần **"Diễn giải từng bước" theo sau** đã đóng vai trò giải nghĩa → **KHÔNG thêm câu "Lưu đồ thể hiện…"** (người nghiệp vụ đọc lưu đồ quen ký hiệu rồi, câu dẫn thừa gây loãng).
> ✅ Bảng: "Bảng dưới tóm tắt các thông tin nền của nghiệp vụ để người đọc nắm nhanh bối cảnh:"
> ✅ Lưu đồ: chỉ ghi "**Lưu đồ quy trình:**" rồi tới sơ đồ, sau đó là "**Diễn giải từng bước:**".

## 3. Logic phức tạp PHẢI có ví dụ mô phỏng
Mọi nguyên tắc phân bổ, công thức tính, ngưỡng, quy tắc xét chọn → kèm **"Ví dụ mô phỏng…"** với SỐ LIỆU CỤ THỂ (mã hàng, số lượng, ngày, kết quả từng bước), diễn giải từng bước đi tới kết quả. Đây là cách hiệu quả nhất để khách "thấy" logic chạy.
> Mẫu: nêu Input (đơn/nhu cầu) → chạy qua từng tiêu chí/bước → ra kết quả, mỗi bước 1 dòng.
> Số liệu ví dụ là MINH HỌA — đặt số hợp lý, không cần (và không nên giả định) là dữ liệu thật của khách.

## 4. Giọng văn tư vấn, khách-hàng-thân-thiện
- Câu **đủ chủ–vị**, ưu tiên thể **chủ động** ("Hệ thống tự đề xuất…", không "được đề xuất bởi…").
- **Thuật ngữ/viết tắt lần đầu phải giải nghĩa** (mở ngoặc tiếng Việt), sau đó mới dùng tắt.
- **Tránh jargon kỹ thuật/dev trong phần diễn giải**: enum, nullable, primary/foreign key, join, API payload… → để dành cho tài liệu SPEC. Với khách, nói nghiệp vụ: "trạng thái (gồm các giá trị…)", "trường bắt buộc", "khóa định danh".
- Tránh liệt kê khô khốc không có câu nối; tránh dịch máy / câu cụt.
- Nhất quán xưng hô đối tượng (Hệ thống / Người dùng / vai trò cụ thể).

## 5. Bảng vs văn xuôi — bổ trợ, không loại trừ
Bảng để chứa **DỮ LIỆU** (trường, bước, ma trận); văn xuôi để giải nghĩa **Ý NGHĨA, LÝ DO, VÍ DỤ**. Một mục tốt = **câu Mục đích → (văn dẫn) → bảng/lưu đồ → (văn chốt + ví dụ nếu là logic)**.

## 6. KHỬ MÃ KỸ THUẬT — dịch sang ngôn ngữ nghiệp vụ (áp MỌI tiểu mục)
Phần **nghiệp vụ** — Mục đích, tên & mô tả tính năng, tên & ý nghĩa cột bảng, **diễn giải từng bước**, và **CẢ khối "Quy trình thao tác trên hệ thống" (walkthrough màn hình)** — **KHÔNG để mã kỹ thuật/viết tắt nội bộ trần**. Phải dịch sang ngôn ngữ người nghiệp vụ hiểu được mà không cần tra glossary.

Mã kỹ thuật/tên hệ thống CHỈ được xuất hiện ở: phần **công thức** (khi cần chính xác), **bảng thuật ngữ/field**, hoặc **mở ngoặc giải nghĩa lần đầu** — vd "hệ thống quản lý kho thực tế (SWM)".

**Ví dụ quy đổi (minh họa — không hardcode, mỗi domain tự có bộ riêng):**
| Mã trần ❌ | Ngôn ngữ nghiệp vụ ✅ |
|---|---|
| GAP | chênh lệch tồn kho (thực tế vs hệ thống) |
| DOI | số ngày còn đủ hàng |
| TF for Safety | lượng bù tồn an toàn |
| TF for Sale | lượng bù cho kế hoạch bán |
| Sloc | vị trí lưu kho |
| SWM | hệ thống quản lý kho thực tế |
| CSE/PL | quy cách (số thùng/pallet) |
| Sum Transfer / Plan đáp ứng | sản lượng điều chuyển / lượng còn lại để bán |

> ⚠️ Lỗi hay gặp: dọn jargon ở phần công thức/field nhưng **QUÊN khối walkthrough ⑥** → vẫn còn "GAP/TF/DOI/Sum Transfer" ở đó. Phải rà cả ⑥.

### 6b. ĐỪNG OVER-TRANSLATE — giữ thuật ngữ chuẩn ngành khách đang dùng
Bảng trên là **mã NỘI BỘ khó hiểu** (chỉ người trong dự án/cấu hình hệ thống mới hiểu: GAP, DOI, TF, Sum Transfer, Sloc, CSE/PL, receipt type, order key…) → **phải dịch**. NHƯNG **thuật ngữ & hệ thống CHUẨN NGÀNH mà khách dùng hằng ngày thì GIỮ NGUYÊN** (giải nghĩa NGẮN một lần ở lần đầu là đủ, sau đó dùng thẳng): **WMS, ERP/SAP, EDI, API, DRP, In-In / In-Ex, FEFO / LEFO, put-away, pallet, OTIF / DIFOT…**

Dịch những từ này thành "hệ thống quản lý kho / kết nối tự động / chuyển nội bộ / đưa lên kệ" ở MỌI chỗ là **over-translate** → tài liệu rườm rà, khách am hiểu logistics thấy bị "nói xuống".
- **Tên hệ thống:** giữ tên + giải nghĩa ngắn một lần (vd "hệ thống quản lý kho (**WMS**)"), KHÔNG bung "hệ thống quản lý kho thực tế" ở mọi câu.
- **Test ranh giới:** "khách có nói từ này trong cuộc họp không?" → Có (WMS, DRP, In-In, FEFO, pallet, OTIF) thì giữ; chỉ có trong file cấu hình/khảo sát nội bộ (Sloc 0012, CSE/PL, GAP) thì dịch. Không chắc → giữ + giải nghĩa ngắn một lần.

> 📌 Bài học thực tế (BRD MDLZ): bản giao khách dịch hết "WMS qua API" → "hệ thống quản lý kho qua kết nối tự động", người dùng đã chủ động sửa lại về **WMS / API / In-In / DRP / put-away** vì khách dùng đúng các từ đó.

## 7. ĐỊNH DẠNG CÔNG THỨC (áp mọi domain khi có công thức)
- Mỗi công thức: tiền tố **`Công thức:`** + **in đậm cả dòng** công thức. KHÔNG bọc blockquote-kiểu-trích-dẫn, KHÔNG để dấu `_` gạch chân quanh ví dụ.
- Ngay sau là **`Trong đó:`** + bullet giải nghĩa **TỪNG biến**, mỗi biến nêu đủ: **(i)** là gì (nghiệp vụ) → **(ii)** ai cấp / lấy từ đâu → **(iii)** thiết lập/nạp tại **màn hình ⟨tên⟩ của module ⟨tên⟩ (mục ⟨số + tên mục⟩)**.
- Biến trung gian tự nó là đại lượng tính được (vd "nhu cầu bán/ngày") → phải có **công thức con + nguồn** ở bước tương ứng.
- Công thức phức / có ngưỡng / làm tròn → kèm **"Ví dụ: …"** số cụ thể ngay sau, chạy ra kết quả.
> ✅ "**Công thức: Nhu cầu bán/ngày = Dự báo tháng × % Phân bổ kho trong ÷ Số ngày bán hàng trong tháng**" → "Trong đó: • Dự báo tháng: … nạp tại màn hình *Tiếp nhận Forecast IBP* của module *Hoạch định nhu cầu* (mục 3.1…)." → "Ví dụ: 500.000 × 70% ÷ 26 = 13.462 thùng/ngày."

## 8. THAM CHIẾU CHÉO & TRUY VẾT
- **Tham chiếu mục: luôn kèm TÊN mục**, không để số trơ. ✅ "xem mục **2.4. Tham số planning động**" ❌ "xem mục 2.4".
- **Tham chiếu màn hình/module:** nêu **tên màn hình + tên module bằng CHỮ** (vd "màn hình *Thiết lập số ngày bán hàng* của module *Thiết lập tham số Planning động*"). **KHÔNG dùng placeholder ảnh `[[MH-…]]`** cho mục đích cross-reference (placeholder ảnh chỉ dùng ở khối walkthrough ⑥).
- **Truy vết nội bộ (BR/PP/OBJ/BRULE…):** viết dưới dạng annotation **`_(Truy vết …)_`** hoặc `_(Ghi chú …)_`. Giữ trong markdown để truy vết; **script `md_to_docx.py` tự BỎ khi convert .docx** (bản giao khách không lộ mã truy vết). Bảng bước bản giao khách KHÔNG để cột "BRULE/Quy tắc" riêng — gộp logic vào diễn giải.

> Lưu ý: file này mã hóa QUY TẮC viết, không phải nội dung của một khách cụ thể. Các ví dụ ở trên chỉ minh họa CÁCH viết.
