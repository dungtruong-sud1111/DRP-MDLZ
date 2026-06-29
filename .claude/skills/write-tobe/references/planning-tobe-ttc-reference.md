# REFERENCE: CẤU TRÚC TO-BE BÀI PLANNING ROLLING (mẫu TTC AgriS — CHỈ THAM KHẢO)

> ⚠️ **ĐÂY LÀ REFERENCE CỦA RIÊNG DỰ ÁN TTC AgriS (TMS Planning / S&OP-DRP rolling).**
> - **CHỈ để THAM KHẢO. Dự án Planning khác KHÔNG bắt buộc tuân theo.**
> - Mục tiêu: cho thấy **CẤU TRÚC một tài liệu TO-BE bài Planning rolling lớn trông như thế nào** — học **bộ xương & cách tổ chức mục**, KHÔNG phải bê công thức/nguyên tắc.
> - **TTC thường PHỨC TẠP hơn đa số khách.** Nhiều nguyên tắc, output, master-data dưới đây khách khác KHÔNG dùng tới — đừng coi là chuẩn tối thiểu.
> - **Công thức / số liệu / tên kho / tên khách / nguyên tắc cụ thể** đặt trong khối "▸ Minh họa TTC" là **DIALECT TTC** — tuyệt đối KHÔNG hardcode sang khách khác.
> - Khi làm TO-BE cho dự án cụ thể: **đọc BRD/AS-IS của khách đó và tự đề xuất Input/Output/Nguyên tắc theo nhu cầu thật** — file này chỉ gợi ý menu cấu trúc.
> - Quy tắc chống áp dialect: `domain-playbooks.md` mục 5. Few-shot 1 nghiệp vụ đạt chuẩn: `example-planning-flow.md`.
> - **Khi nào đọc:** bài Planning quy mô lớn kiểu **S&OP/DRP rolling nhiều chân trời**. Bài đơn giản (vd replenishment theo trigger như MDLZ) **KHÔNG cần file này** — bám skeleton lõi mục 5.

---

## 0. Bài TTC thuộc LOẠI nào
S&OP/DRP **rolling đa chân trời** (Monthly/Weekly/Daily): cân đối Supply↔Demand theo nhiều ràng buộc, đề xuất chuyển kho (TO) & xuất bán (SO) + gợi ý sản xuất bổ sung. Bài khách KHÁC loại này → chỉ tham khảo rời.

## 1. MACRO-SKELETON A→G (phần ĐÁNG HỌC NHẤT — cấu trúc, KHÔNG phải công thức)
Một bài Planning rolling lớn có thể kể mạch lạc theo 7 khối. Đây là MENU cấu trúc, lấy/bỏ theo bài:

- **A. Tổng quan giải pháp** — lưu đồ tổng quan end-to-end; phạm vi & mục tiêu; **cấu trúc giải pháp theo các tầng rolling**; quy trình vận hành theo từng tầng.
- **B. Master Data & cấu hình chung** — danh mục nền cần khai báo trước (menu ở mục 4).
- **C. Input (Demand & Supply)** — nguồn cầu + nguồn cung theo từng chân trời (+ tùy chọn Constraint/Unconstraint).
- **D. Nguyên tắc & ràng buộc xử lý** — tập quy tắc logic của bài (mục 3). *Không phải khách nào cũng nhiều như TTC.*
- **E. Output kế hoạch** — các màn hình kết quả (mục 6); đề xuất theo nhu cầu khách.
- **F. Exceptional cases** — gom tình huống ngoại lệ + cách xử lý.
- **G. Luồng tích hợp** — ở skill ta đẩy sang file `_TOBE-TICH-HOP.md` (playbook Integration).

> **So với skeleton lõi Planning** (Setup→Input→Logic→Output→Exception→Integration ở `domain-playbooks.md` mục 5): A→G là **một hiện thực cụ thể**, có **bổ sung Khối A "Tổng quan/Cấu trúc giải pháp"** ở đầu. Bài đủ lớn nên mở đầu bằng khối Tổng quan như vậy; bài nhỏ thì bỏ.

### 1b. Cascade chân trời rolling (cấu trúc tư duy — số tầng tùy khách)
| Chân trời | Nguồn Demand | Nguồn Supply | Đầu ra chính |
|---|---|---|---|
| Dài hạn (Monthly) | dự báo năm | KHSX dài hạn | Dự trù nguồn lực, alert capacity |
| Trung hạn (Weekly) | forecast tuần + đơn pending | KHSX tuần | Projection tồn, đề xuất bổ sung |
| Ngắn hạn (Daily) | đơn pending + thực tế | cung thực tế | Kế hoạch chuyển kho/xuất bán theo ngày |
*Cascade này tái dùng được; khách có thể chỉ chạy 1–2 tầng. Nguồn dữ liệu cụ thể của TTC là dialect TTC.*

## 2. QUẢN LÝ VERSION (pattern hay cần)
- **Quản lý version + chọn version nào để chạy** kế hoạch: hay cần, nên gợi ý cho bài Planning có nhiều phương án. Mỗi version có ID/thời gian/người tạo.
- **Compare nhiều version (OPTIONAL):** không phải khách nào cũng chạy & so sánh — chỉ thêm khi khách thật sự cần.
- Chi tiết (giới hạn số version, khóa kịch bản đã duyệt…) là dialect TTC.

## 3. NGUYÊN TẮC & RÀNG BUỘC XỬ LÝ (Khối D) — học CÁCH TỔ CHỨC, không bê nguyên tắc
Bài rolling thường có một lớp "nguyên tắc & ràng buộc" quyết định chọn nguồn cung nào, kho nào, phương thức nào. **Số lượng & độ phức tạp tùy khách — nhiều khách chỉ cần 1–2 ràng buộc, hoặc không có lớp này.** Cách tổ chức tốt: xếp ràng buộc thành các lớp ưu tiên + vòng lặp + cây quyết định khi không đủ.

> ▸ **Minh họa TTC (DIALECT — KHÔNG hardcode sang khách khác; TTC nhiều ràng buộc bất thường):** TTC dùng tới 4 nguyên tắc — (1) phân bổ theo lớp RTM direct/indirect + vòng lặp ưu tiên; (2) xét đủ tồn **đồng thời 4 tiêu chí** SKU+Spec+FEFO+Qty rồi loop kho kế; (3) ưu tiên theo nhóm khách; (4) rolling + trừ lùi leadtime đa phương thức + cây quyết định tồn→chuyển kho→sản xuất. Ví dụ loop RTM: Kho BHC (ưu tiên 1, fail FEFO/Qty) → Kho NHS (đạt). Trừ lùi: `Ngày dispatch = Ngày nhận − leadtime lớn nhất`.
>
> 👉 **Điều cần học:** *cách xếp ràng buộc thành lớp + vòng lặp + cây quyết định khi thiếu*, KHÔNG phải số/tên kho/số lớp của TTC. Đa số khách đơn giản hơn nhiều.

## 4. MENU MASTER DATA (gợi nhớ — KHÔNG phải khách nào cũng dùng hết)
Item · Danh mục điểm · Capacity WH/DC · Capacity vận chuyển/ngày · Spec chất lượng KH · Substitution list · RTM · Lead time · FEFO & %shelf-life · Stock Policy (Min/Target/Max) · Rule phasing tháng→tuần · Rule quy đổi khung xe · Phân bổ tỉ lệ NVT · Bảng giá vận chuyển.
*Đây là MENU đầy đủ của TTC. Mỗi khách lấy/bỏ tùy bài — đừng ép đủ hết. Mỗi master data nên tả theo bảng dọc 6 dòng (xem mục 5 playbook) + field spec.*

## 5. INPUT (Demand & Supply) — cấu trúc tổng quát
- **Demand:** nhu cầu theo (các) chân trời — dài hạn (dự báo năm), trung hạn (forecast tuần), ngắn hạn (đơn thực tế/pending). Tùy khách có disaggregate tháng→tuần, tích hợp actual để đo Forecast Accuracy.
- **Supply:** tồn khả dụng (= tồn onhand − giữ chỗ) + tồn đi đường (nếu có WMS); khả năng cung ứng theo horizon.
- **(Tùy chọn) Constraint/Unconstraint:** chọn version supply, có xét đơn pending không, khi thiếu cung → lost-sales hay đề xuất sản xuất bổ sung. *Tham khảo, không bắt buộc.*

## 6. OUTPUT — menu các màn hình kết quả (đề xuất theo nhu cầu khách)
> **Lưu ý quan trọng:** output KHÔNG phải lúc nào cũng nhiều như TTC. **Khi làm TO-BE dự án cụ thể: đọc BRD/AS-IS rồi tự đề xuất output theo nhu cầu khách.** Dưới đây là menu tham khảo:
- **Tổng quan kế hoạch** (service level, tổng điều chuyển, dashboard chi phí, map…).
- **Inventory Projection** — mô phỏng tồn theo kỳ; cảnh báo Min/Max; DOH; so plan-vs-actual.
- **Kế hoạch chuyển kho (TO)** vs **xuất bán (SO)** — có thể tách 2 màn hình; trừ lùi leadtime; duyệt → tích hợp vận hành.
- **Chỉ định tồn cho đơn trong ngày** — check tiêu chí tồn, fallback mã thay thế, gửi WMS/TMS.
- **Chia khung xe & phân bổ NVT** — vd 3 rule chọn NVT: theo tỷ lệ / giá thấp nhất / service level.

> ▸ **Minh họa TTC (DIALECT):** `Ending Inventory = Opening + Incoming + Replenishment − Demand`; Target cover ~4 tuần; cảnh báo màu theo Min/Max. *Công thức này của TTC.*

## 7. EXCEPTION & INTEGRATION
- **Exception:** gom 1 mục thống nhất cách xử lý (thiếu cung, thiếu leadtime, hết cả mã thay thế…).
- **Integration:** tách file `_TOBE-TICH-HOP.md` theo playbook Integration.

## 8. ĐỘ SÂU & VĂN PHONG
Mỗi nghiệp vụ trong B/C/D/E vẫn viết theo **bố cục 6 khối** của `domain-playbooks.md` mục 5; dồn độ sâu vào chỗ khó + ví dụ số; khử mã kỹ thuật (writing-style §6). File này chỉ thêm **lớp cấu trúc vĩ mô A→G** bao ngoài.
