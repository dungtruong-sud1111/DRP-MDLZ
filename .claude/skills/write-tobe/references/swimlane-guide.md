# HƯỚNG DẪN SƠ ĐỒ SWIMLANE PHONG CÁCH SMARTLOG (canonical)

Sơ đồ swimlane là **lưu đồ giao khách** chuẩn Smartlog: chia **lane dọc theo VAI TRÒ** (người thao tác / hệ thống xử lý / phòng ban). Áp **mọi domain** có quy trình (WMS nhập/xuất, TMS điều phối, SOM tạo đơn, Planning…). Pipeline: **JSON → HTML/SVG → PNG (playwright) → chèn vào Word thay block mermaid**.

## 1. PHONG CÁCH SMARTLOG (học từ mẫu `Swimlane diagram mẫu/`)
- **Tiêu đề quy trình** ở đỉnh: dải nền `#176bb4`, chữ trắng đậm.
- **Lane dọc**, mỗi lane = 1 vai trò; tên lane ở header (nền nhạt, viền, chữ đậm); có đường phân chia lane.
- **Ký hiệu:** chữ nhật bo góc = bước xử lý; **hình thoi = điểm quyết định** (nhánh Có/Không); **oval = Bắt đầu/Kết thúc**; nhãn nhánh ("Có"/"Không"/"Duyệt"/"Điều chỉnh") đặt trên cạnh.
- **Ghi chú phụ** (nếu cần): chữ **màu đỏ** ở lề trái của bước.
- **Đánh số bước** B1, B2… (hoặc khớp số bước trong bảng bước/diễn giải).

## 2. QUY TẮC DỰNG (bắt buộc — tránh lỗi đã gặp)
1. **Bám ĐÚNG các bước trong TO-BE — KHÔNG tự thêm bước.** TO-BE mô tả 9 bước thì sơ đồ đúng 9 bước; KHÔNG bịa thêm bước (vd thêm "B10 thực thi" khi tài liệu không có).
2. **Lane trống thì BỎ.** Chỉ giữ lane có ít nhất 1 node. (Không để lane "Bộ phận kho" trống nếu tài liệu không có thao tác ở đó.)
3. **Mũi tên xuất phát/đi vào từ CẠNH/ĐỈNH/GÓC shape**, KHÔNG từ tâm: ra ở đáy (đi xuống), vào ở đỉnh; hình thoi rẽ ngang → ra ở **góc trái/phải**.
4. **Node đủ lớn** để chữ KHÔNG tràn (process ~180×52, hình thoi ~140×72, oval ~130×56). Lane đủ rộng (~400px) để tỷ lệ ngang/dọc cân với khổ A4 khi vào Word.
5. **Vòng lặp** (vd "Điều chỉnh" quay lại bước trước) vẽ **nét đứt**, có nhãn rõ; đi vòng bên phải, điểm đầu–cuối rõ ràng.
6. **Kết thúc phải nối vào node Kết thúc** — không để mũi tên lửng.

## 3. SCHEMA JSON (đầu vào `swimlane_generator.py`)
```json
{
  "title": "4.1. In-In BKD — Điều chuyển nội bộ (BKD2/BKD3 → BKD1)",
  "lanes": ["Hệ thống", "Warehouse Planner"],
  "nodes": [
    {"id": "start", "lane": 1, "row": 0,  "type": "start",    "label": "Bắt đầu\n(16h00 ngày D)"},
    {"id": "b1",    "lane": 0, "row": 1,  "type": "process",  "label": "B1. Lấy nhu cầu\nbán/ngày"},
    {"id": "d1",    "lane": 0, "row": 6,  "type": "decision", "label": "Tổng nhu\ncầu > 0?"},
    {"id": "end",   "lane": 1, "row": 15, "type": "end",      "label": "Kết thúc"}
  ],
  "edges": [
    {"from": "start", "to": "b1", "label": ""},
    {"from": "d1",    "to": "b6", "label": "Có"},
    {"from": "d3",    "to": "b8", "label": "Điều chỉnh"}
  ]
}
```
- `lane`: chỉ số lane (0-based). `row`: hàng dọc (số nguyên tăng dần — quyết định vị trí trên–dưới). `type`: `start|end|process|decision`. `\n` trong `label` để xuống dòng.
- Edge `label`: nhãn nhánh. Edge "ngược" (row đích ≤ row nguồn) tự vẽ nét đứt vòng phải (vòng lặp).

## 4. PIPELINE & LỆNH
```
# Sinh HTML + PNG từ JSON (có cache)
export PYTHONIOENCODING=utf-8 PYTHONUTF8=1
python scripts/swimlane_generator.py "luu-do/<ten>.json"
# → luu-do/<ten>.html  +  luu-do/<ten>.png
```
- Trong `_TOBE-BLUEPRINT.md`, block ```` ```mermaid ```` của nghiệp vụ đó thêm **dòng đầu `# src: <ten>`** để `md_to_docx.py` khớp đúng PNG khi convert.
- **CACHE:** `swimlane_generator.py` chỉ vẽ lại PNG khi HTML mới hơn PNG. Sơ đồ đã vẽ & không đổi → **dùng lại**, không tạo mới. Chỉ khi sửa JSON (→ HTML đổi) mới vẽ lại.

## 5. YÊU CẦU MÔI TRƯỜNG
- `pip install playwright` + `python -m playwright install chromium` (capture HTML→PNG headless).
- Nếu thiếu playwright: script báo lỗi rõ; `md_to_docx.py` fallback mermaid-cli/placeholder.

> Lưu đồ swimlane (giao khách) và **mermaid** (nguồn logic, fallback) bổ trợ nhau. Giữ `.mmd` để đối chiếu logic; bản .docx dùng PNG swimlane.
