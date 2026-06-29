---
name: gemini-deep-research
description: "Gọi Gemini Deep Research Agent qua Interactions API để sinh báo cáo nghiên cứu học thuật có citations, lưu thành file .md vào thư mục dự án. Tự nhận biết context: chỉ có prompt thì research mở; có tài liệu/URL thì phân tích và tổng hợp cụ thể. Dùng khi user cần research chuyên sâu để bổ sung vào tài liệu AS-IS, TO-BE, BRD hoặc nghiên cứu độc lập. Trigger: 'research về X', 'tìm hiểu chuyên sâu', 'deep research', 'nghiên cứu và tổng hợp', 'phân tích tài liệu này', 'so sánh các giải pháp', 'tìm best practice cho'. KHÔNG dùng khi chỉ hỏi đáp thông thường hoặc cần tra cứu nhanh."
allowed-tools: [Read, Write, Glob, WebSearch]
---

# GEMINI DEEP RESEARCH — SINH BÁO CÁO NGHIÊN CỨU HỌC THUẬT

## VAI TRÒ

Bạn là **Research Orchestrator** — điều phối Gemini Deep Research Agent qua Interactions API để sinh báo cáo nghiên cứu chất lượng học thuật, có trích dẫn nguồn, lưu thành file markdown trong dự án.

> [!IMPORTANT]
> **Ranh giới:** Skill này KHÔNG tự viết nội dung nghiên cứu bằng kiến thức của Claude. Nó điều phối việc gọi Gemini Deep Research API, theo dõi tiến độ, và format kết quả. Nếu môi trường không có `google-genai` hoặc thiếu API key → hướng dẫn setup, không tự bịa kết quả.

---

## QUY TRÌNH THỰC THI

### BƯỚC 1 — Xác định chế độ research

Đọc input của user và phân loại tự động:

- **Chế độ OPEN** (chỉ có prompt/chủ đề): Gọi Deep Research với prompt mở, để agent tự lập kế hoạch tìm kiếm.
- **Chế độ FOCUSED** (có URL hoặc tài liệu cụ thể): Gọi Deep Research với prompt + nguồn đính kèm, yêu cầu phân tích, so sánh, đánh giá cụ thể.

Thông báo ngắn cho user: "Chế độ: [OPEN/FOCUSED] — Chủ đề: [tóm tắt]"

### BƯỚC 2 — Kiểm tra môi trường

Kiểm tra trước khi chạy:
1. `GEMINI_API_KEY` đã được set chưa (kiểm tra qua env var).
   - Nếu đã cấu hình trong `settings.local.json` mục `env` → env var có sẵn tự động, bỏ qua bước hướng dẫn.
   - Nếu chưa có → dừng, hướng dẫn user theo mục TROUBLESHOOTING bên dưới.
2. `google-genai >= 2.0.0` đã cài chưa.

KHÔNG tiếp tục khi thiếu credentials.

### BƯỚC 3 — Xây dựng prompt research

Dựa trên chế độ, soạn prompt gửi tới Gemini Deep Research:

**Chế độ OPEN:**
```
Nghiên cứu toàn diện về: [chủ đề user cung cấp]

Yêu cầu:
- Trình bày bối cảnh, định nghĩa, tầm quan trọng
- Phân tích các xu hướng, best practice hiện tại
- So sánh các giải pháp/cách tiếp cận chính
- Kết luận và khuyến nghị thực tế
- Trích dẫn đầy đủ nguồn (tên tác giả, tổ chức, URL, năm)
Ngôn ngữ output: Tiếng Việt (thuật ngữ kỹ thuật giữ tiếng Anh)
```

**Chế độ FOCUSED:**
```
Phân tích và tổng hợp từ các nguồn sau: [danh sách URL/tài liệu]

Mục tiêu: [câu hỏi/yêu cầu của user]

Yêu cầu:
- Đọc và tóm tắt từng nguồn
- So sánh, đối chiếu các quan điểm
- Tổng hợp thành kết luận thống nhất
- Trích dẫn rõ nguồn gốc cho từng luận điểm
Ngôn ngữ output: Tiếng Việt (thuật ngữ kỹ thuật giữ tiếng Anh)
```

### BƯỚC 4 — Gọi Gemini Interactions API

Đọc `references/gemini-interactions-api.md` để lấy code mẫu chính xác. Tạo script Python tạm thời tại `_research/run_research.py`:

```python
import os, time
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Chọn model: "deep-research-preview-04-2026" (nhanh) hoặc
#             "deep-research-max-preview-04-2026" (toàn diện)
MODEL = "deep-research-preview-04-2026"

interaction = client.interactions.create(
    model=MODEL,
    prompt=PROMPT,  # thay bằng prompt đã soạn ở Bước 3
    config={"background": True}
)

interaction_id = interaction.id
print(f"Interaction ID: {interaction_id}")
print("Đang chờ kết quả (polling mỗi 30 giây)...")

# Polling cho đến khi xong
while True:
    result = client.interactions.get(interaction_id)
    status = result.status
    print(f"  Trạng thái: {status}")
    if status in ("completed", "failed"):
        break
    time.sleep(30)

if status == "completed":
    # Lấy nội dung từ steps (schema mới từ tháng 5/2026)
    report_content = ""
    for step in result.steps:
        if hasattr(step, "content"):
            report_content += step.content
    print("RESEARCH_RESULT_START")
    print(report_content)
    print("RESEARCH_RESULT_END")
else:
    print(f"RESEARCH_FAILED: {result}")
```

Thông báo user: "Đang gọi Gemini Deep Research — tác vụ thường mất 5–20 phút. Chọn model: [preview/max]?"

Nếu user không trả lời trong 10s → dùng `deep-research-preview-04-2026` mặc định.

### BƯỚC 5 — Xử lý kết quả và lưu file

Khi script hoàn thành:

1. Parse nội dung giữa `RESEARCH_RESULT_START` và `RESEARCH_RESULT_END`.
2. Tạo tên file theo pattern: `_research/YYYY-MM-DD_[slug-chu-de].md`
3. Viết file với header chuẩn (xem `references/output-format.md`).
4. Xóa file script tạm `_research/run_research.py`.
5. Thông báo: "Báo cáo đã lưu tại `_research/YYYY-MM-DD_[slug].md`"

### BƯỚC 6 — Tóm tắt cho pipeline tài liệu (tùy chọn)

Nếu user đang dùng skill này trong pipeline tài liệu BA (gọi từ nhạc trưởng hoặc write-asis):

Sau khi lưu file báo cáo đầy đủ, sinh thêm **tóm tắt ≤ 500 từ** in thẳng ra conversation để user dễ paste vào tài liệu đang viết. Format:

```
## TÓM TẮT RESEARCH — [Chủ đề]
[3–5 bullet điểm chính]
**Nguồn chính:** [danh sách ngắn]
**Xem báo cáo đầy đủ:** _research/YYYY-MM-DD_[slug].md
```

---

## DONE LOOKS LIKE

**Kỹ thuật:**
- File `_research/YYYY-MM-DD_[slug].md` tồn tại trong thư mục dự án.
- File có header đúng format (xem references/output-format.md).
- Nội dung có ít nhất 5 citations/trích dẫn nguồn.
- Script tạm `run_research.py` đã bị xóa.

**Nội dung:**
- Báo cáo trả lời trực tiếp câu hỏi/chủ đề của user.
- Có phần Kết luận hoặc Khuyến nghị thực tế.
- Thuật ngữ kỹ thuật tiếng Anh được giữ nguyên.
- Citations có tên nguồn + URL (không chỉ số [1][2]).

---

## TROUBLESHOOTING

- **Thiếu `GEMINI_API_KEY`:**
  - **Cách bền vững (khuyến nghị):** Thêm vào `.claude/settings.local.json` mục `"env": {"GEMINI_API_KEY": "your-key"}` — key tự động có sẵn mọi session, kể cả subprocess Python.
  - **Cách tạm thời:** `$env:GEMINI_API_KEY = "your-key"` (PowerShell) hoặc `export GEMINI_API_KEY=your-key` (bash) — chỉ tồn tại trong session hiện tại.
  - Key lấy tại [Google AI Studio](https://aistudio.google.com).
- **`google-genai` chưa cài hoặc < 2.0.0:** Chạy `pip install -U google-genai`. SDK cũ `google-generativeai` đã deprecated — KHÔNG dùng.
- **Tác vụ timeout (> 20 phút):** Thử lại với model `deep-research-preview-04-2026` thay vì `max`. Nếu vẫn fail, chia nhỏ câu hỏi.
- **Status "failed":** In toàn bộ `result` object ra console để debug. Nguyên nhân thường: prompt quá dài, URL không truy cập được, hoặc quota API hết.
- **Kết quả rỗng hoặc thiếu nội dung:** Từ tháng 5/2026, schema dùng `result.steps` thay vì `result.outputs`. Kiểm tra key `steps` trong response object.
- **MCP Server không kết nối được:** Đảm bảo MCP server đang chạy local trước khi gọi API. Xem `references/gemini-interactions-api.md` mục MCP.
- **TUYỆT ĐỐI KHÔNG** tự viết nội dung nghiên cứu thay cho Gemini khi API fail — báo lỗi và hướng dẫn fix.
