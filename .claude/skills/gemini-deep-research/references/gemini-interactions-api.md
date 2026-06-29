# GEMINI INTERACTIONS API — TECHNICAL REFERENCE

Nguồn chính thức: [ai.google.dev/gemini-api/docs/interactions/deep-research](https://ai.google.dev/gemini-api/docs/interactions/deep-research)

---

## SETUP

### Cài đặt SDK

```bash
pip install -U google-genai
# Yêu cầu >= 2.0.0 — SDK cũ google-generativeai đã deprecated
```

### API Key

```powershell
# PowerShell (Windows)
$env:GEMINI_API_KEY = "your-api-key-here"
```

```bash
# bash/zsh (macOS/Linux)
export GEMINI_API_KEY="your-api-key-here"
```

Lấy key tại: [aistudio.google.com](https://aistudio.google.com)

---

## CÁC MODEL DEEP RESEARCH (2026)

| Model ID | Đặc điểm | Thời gian |
|---|---|---|
| `deep-research-preview-04-2026` | Nhanh, hiệu quả | 5–10 phút |
| `deep-research-max-preview-04-2026` | Toàn diện tối đa, nhiều vòng lặp tìm kiếm | 10–20 phút |

**Lưu ý:** Các model này chỉ dùng qua Interactions API (`client.interactions.create()`), KHÔNG qua `client.models.generate_content()`.

---

## CODE MẪU ĐẦY ĐỦ (Python)

```python
import os
import time
from google import genai

# Khởi tạo client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

PROMPT = """
Nghiên cứu toàn diện về: [chủ đề]
...
"""

MODEL = "deep-research-preview-04-2026"  # hoặc deep-research-max-preview-04-2026

# Bước 1: Khởi chạy tác vụ (PHẢI dùng background=True — sync sẽ timeout)
interaction = client.interactions.create(
    model=MODEL,
    prompt=PROMPT,
    config={"background": True}
)

interaction_id = interaction.id
print(f"Interaction ID: {interaction_id}")

# Bước 2: Polling cho đến khi hoàn thành
while True:
    result = client.interactions.get(interaction_id)
    status = result.status
    print(f"Trạng thái: {status}")
    
    if status == "completed":
        break
    elif status == "failed":
        print(f"Lỗi: {result}")
        exit(1)
    
    time.sleep(30)  # Chờ 30 giây giữa mỗi lần poll

# Bước 3: Lấy nội dung (schema mới từ tháng 5/2026 — dùng steps, không dùng outputs)
report_parts = []
for step in result.steps:
    if hasattr(step, "content") and step.content:
        report_parts.append(step.content)

full_report = "\n\n".join(report_parts)
print(full_report)
```

---

## TÍCH HỢP MCP SERVER (tùy chọn nâng cao)

Cho phép Deep Research truy cập trực tiếp file system hoặc codebase của IDE:

```python
# Kết nối với MCP Server đang chạy local
interaction = client.interactions.create(
    model="deep-research-preview-04-2026",
    prompt=PROMPT,
    config={
        "background": True,
        "tools": [
            {
                "mcp_server": {
                    "url": "http://localhost:8080"  # URL MCP server của bạn
                }
            }
        ]
    }
)
```

**Lưu ý khi dùng MCP:**
- MCP Server phải đang chạy TRƯỚC khi gọi API.
- Hỗ trợ từ bản cập nhật ngày 21/04/2026 (Gemini 3.1 Pro).
- Chỉ dùng khi cần truy cập file local; không cần cho research web thông thường.

---

## SCHEMA RESPONSE (quan trọng — thay đổi tháng 5/2026)

| Trường | Giá trị |
|---|---|
| `interaction.id` | ID để dùng polling |
| `result.status` | `"running"` / `"completed"` / `"failed"` |
| `result.steps` | **Mảng các bước** (thay thế `outputs` từ 08/06/2026) |
| `step.content` | Nội dung text của từng bước |

> [!CAUTION]
> `result.outputs` và `response_mime_type` đã bị loại bỏ từ ngày 08/06/2026. Luôn dùng `result.steps`.

---

## REST API (không dùng Python SDK)

```bash
# Tạo interaction
curl -X POST \
  "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Api-Revision: 2026-05-20" \
  -H "Content-Type: application/json" \
  -d '{"input": "...", "agent": "deep-research-preview-04-2026", "background": true}'

# Polling kết quả
curl "https://generativelanguage.googleapis.com/v1beta/interactions/INTERACTION_ID" \
  -H "x-goog-api-key: $GEMINI_API_KEY"
```
