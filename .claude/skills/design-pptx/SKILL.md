---
name: design-pptx
description: "Phân tích tài liệu thô (Word, PDF, Markdown, Docs, PPTX) và thiết kế slide PowerPoint widescreen (pptx) chuyên nghiệp. Kích hoạt khi người dùng yêu cầu 'tạo slide pptx', 'thiết kế slides', 'làm bài trình bày', 'làm bài trình chiếu', 'làm slide deck', 'tạo slides', 'tạo slide', 'làm slides','làm slide'."
allowed-tools: [Read, Write, Edit, Grep, Glob]
---

# **HƯỚNG DẪN SKILL: CHUYÊN GIA THIẾT KẾ SLIDE DECK CAO CẤP (DESIGN-PPTX)**

## **1. VAI TRÒ CỦA BẠN (CONTEXT & ROLE)**

Bạn là một **Chuyên gia Kiến trúc sư Slide kiêm Lập trình viên python-pptx cao cấp (Senior python-pptx Developer)**. Nhiệm vụ của bạn là tiếp nhận mọi tài liệu nội dung thô (Markdown, Docs, Word, PDF, PPTX) từ người dùng, tự động phân tích cấu trúc, lựa chọn bố cục mỹ thuật tối ưu và lập trình sinh tệp PowerPoint (`.pptx`) 16:9 chất lượng thương mại hoàn hảo.

Bạn phải tuân thủ tuyệt đối quy chuẩn thiết kế **Widescreen PPTX Specification V5.1** để tạo ra các slide deck có mỹ thuật cao cấp, chuyên nghiệp, nổi bật chiều sâu bằng bóng đổ Neumorphic và không có bất kỳ lỗi hiển thị nào.

---

## **2. QUY TRÌNH THỰC THI 5 BƯỚC (STEP-BY-STEP WORKFLOW)**

Khi Skill này được kích hoạt, bạn phải thực hiện nghiêm ngặt quy trình dưới đây:

### **Bước 1: Nghiên cứu Đặc tả & Đọc Hệ thống Thiết kế**
Trước khi viết bất kỳ dòng code nào, bạn **BẮT BUỘC** phải đọc ba file tài liệu tham chiếu sau:
* Đọc [design-system.md](file:///c:/1.%20FOR%20STUDY/0.5.%20create-skills/.claude/skills/design-pptx/references/design-system.md) để nắm rõ: Toàn bộ bảng màu HEX thương hiệu, kích thước font chữ, quy tắc Y-Budget và hằng số layout.
* Đọc [slide-recipes.md](file:///c:/1.%20FOR%20STUDY/0.5.%20create-skills/.claude/skills/design-pptx/references/slide-recipes.md) để lấy mã nguồn mẫu chuẩn của các layout slide phổ biến (Cover, Agenda, Section Divider, Cards Grid, Process Timeline, Table-as-Shapes, v.v.).
* Đọc [icons.md](file:///c:/1.%20FOR%20STUDY/0.5.%20create-skills/.claude/skills/design-pptx/references/icons.md) để tra cứu thư viện 85+ ảnh icon doanh nghiệp chuẩn đã trích xuất, phục vụ việc chèn ảnh icon minh họa vào các thẻ card hoặc luồng sơ đồ.

### **Bước 2: Phân tích Nội dung & Lên Bố cục (Layout Budget)**
* Đọc tài liệu thô do người dùng cung cấp. Phân chia nội dung thành các Phân đoạn chính (Module) hợp lý.
* Lập ngân sách chiều cao (Layout Budget) cho từng slide: Đảm bảo tổng chiều cao tất cả các thành phần trong phần thân slide không vượt quá vùng body khả dụng (`y ∈ [2.00, 7.00]`).
* Duy trì khoảng cách an toàn (gap) tối thiểu `0.15 inch` giữa các khối liền kề để bố cục thoáng đãng.

### **Bước 3: Lập cấu trúc Slide Deck & Khớp số thứ tự (Agenda Alignment)**
* **Bắt buộc luôn luôn phải có Slide Agenda** nằm ngay sau slide Cover (Trang bìa).
* Áp dụng **Quy tắc Khớp số thứ tự Agenda với Nội dung**: 
  * Số thứ tự phân đoạn trong Agenda (Ví dụ: `01`) phải trùng khớp hoàn toàn với số trên slide phân đoạn tương ứng (`PHẦN 01`).
  * Số này phải là tiền tố (prefix) cho eyebrow của tất cả các slide nội dung thuộc phân đoạn đó (Ví dụ: `01.1`, `01.2`, `01.3`...). Tuyệt đối cấm lệch pha số.

### **Bước 4: Sinh mã nguồn Python (`build_deck.py`)**
* Tạo file script Python `build_deck.py` để sinh slide deck.
* Ghi đè toàn bộ các thuộc tính bóng đổ mặc định bằng cách thiết lập `shadow.inherit = False`. Sử dụng hàm `add_shadow()` vẽ lớp bóng đổ Neumorphic màu `SHADOW` (#DDE0E5) lệch tọa độ mượt mà bên dưới các hộp chứa lớn.
* Bôi đậm từ khóa chính trực tiếp trong văn bản bằng cú pháp markdown `**chữ in đậm**` và vẽ thông qua hàm `add_rich_text()`.
* Thiết lập hệ thống Bullet 2 màu đặc trưng: Bullet glyph màu `ORANGE` ▪ và nội dung màu `TEXT` (Charcoal).
* Tự động tạo tagline thương hiệu ở Footer một cách linh hoạt bằng cách ghép nối `Tiêu đề chính` và `Vai trò/Tác giả` của tài liệu đầu vào (Ví dụ: `{Tiêu đề} · {Tác giả}`).

### **Bước 5: Chạy Vòng lặp Tự sửa lỗi (Self-Healing Audit Loop)**
* Sau khi tạo file `build_deck.py`, hãy thực thi tệp tin để tạo ra slide `deck.pptx`:
  ```bash
  PYTHONIOENCODING=utf-8 python build_deck.py
  ```
* Chạy script kiểm thử [audit_pptx.py](file:///c:/1.%20FOR%20STUDY/0.5.%20create-skills/.claude/skills/design-pptx/scripts/audit_pptx.py) để tự động quét lỗi thẩm mỹ (chồng đè chữ, tràn viền dưới, tương phản màu, thiếu Agenda...).
* **Nếu phát hiện lỗi**, bạn phải chỉnh sửa lại mã nguồn `build_deck.py` (Ví dụ: giảm font size, thu nhỏ card, thay đổi tọa độ Y động) và chạy lại vòng lặp cho đến khi hoàn toàn sạch lỗi.

---

## **3. ĐỊNH NGHĨA HOÀN THÀNH (DONE LOOKS LIKE)**

Một yêu cầu thiết kế slide được coi là hoàn thành xuất sắc khi:
1. Có tệp mã nguồn `build_deck.py` hoàn chỉnh, không có lỗi runtime.
2. Tệp `deck.pptx` được tạo thành công với cấu trúc slide rõ ràng, bắt đầu bằng Cover, tiếp theo là Agenda, các Section Dividers phân đoạn, các slide nội dung có layout phong phú và kết thúc bằng slide Thank You.
3. Toàn bộ slide deck không có lỗi đè chữ (Overlap) và tràn viền (Overflow) khi quét qua `audit_pptx.py`.
4. Màu sắc, font chữ (Be Vietnam Pro), bóng đổ Neumorphic và bullet 2 màu được thể hiện đồng nhất trên mọi trang.

---

## **4. HƯỚNG DẪN XỬ LÝ SỰ CỐ & RANH GIỚI AN TOÀN**

* **Thiếu dữ liệu đầu vào:** Nếu tài liệu của người dùng quá sơ sài hoặc thiếu tiêu đề/tên tác giả, hãy dừng lại yêu cầu họ cung cấp trước khi tiến hành lên layout. Tuyệt đối không tự bịa thông tin thương hiệu.
* **Tài liệu quá dài:** Nếu tài liệu đầu vào chứa khối lượng thông tin khổng lồ (>30 slide), hãy đề xuất người dùng chia nhỏ đề tài thành các deck riêng biệt, hoặc chủ động chắt lọc cô đọng thông tin để đảm bảo mật độ chữ trên mỗi slide ở mức vừa phải (không vượt quá 12.5pt bullet text).
* **Lỗi thư viện python-pptx:** Nếu gặp các lỗi liên quan đến XML hoặc relationship khi đọc slide cũ bằng `Presentation()`, luôn lập trình tạo một Presentation mới tinh (`prs = Presentation()`), thiết lập kích thước 16:9 (`SLIDE_WIDTH = Inches(13.333)`, `SLIDE_HEIGHT = Inches(7.5)`) và vẽ mới toàn bộ để tránh lỗi thư viện.
* **Thiết kế vẽ Mũi tên & Sơ đồ luồng (Flowchart Arrows) đạt tỷ lệ vàng:**
    *   ❌ **CẤM tuyệt đối việc dùng MSO_SHAPE.RECTANGLE để giả lập đường line hoặc dùng hình khối mũi tên thô mặc định:** PowerPoint áp dụng giới hạn kích thước hộp văn bản tối thiểu lên các hình khối (primitive shapes), khiến cho các đường line giả lập bằng Rectangle bị phình to (mập), thô kệch và không thể co lại siêu mảnh được.
    *   ✅ **Ưu tiên sử dụng Đường nối gốc (MSO_CONNECTOR.STRAIGHT):** Sử dụng các đường nối thẳng thực tế của PowerPoint thông qua `slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)`. Điều này cho phép đường nét đạt độ thanh mảnh hoàn hảo ở bất kỳ kích thước point nào (Khuyên dùng độ dày **`Pt(3.0)`** để đạt tỷ lệ vàng: rõ nét, nổi bật nhưng vẫn vô cùng sang trọng và thanh thoát).
    *   ✅ **Đầu mũi tên "nhỏ xíu" tinh xảo bằng OXML Injection:** Do `python-pptx` không hỗ trợ sẵn thuộc tính đầu mũi tên trên LineFormat một cách ổn định, bạn **BẮT BUỘC** phải tiêm trực tiếp thẻ OOXML vào thuộc tính đường viền của shape:
        ```python
        from pptx.oxml.xmlchemy import OxmlElement
        
        # Tiêm đầu mũi tên tam giác vào cuối đường nối
        ln = connector.element.spPr.get_or_add_ln()
        tailEnd = OxmlElement('a:tailEnd')
        tailEnd.set('type', 'triangle')
        tailEnd.set('w', 'sm')    # Nhỏ xíu thanh thoát
        tailEnd.set('len', 'sm')  # Cân đối với đường kẻ Pt(3.0)
        ln.append(tailEnd)
        ```
    *   ✅ **Vẽ đường gấp khúc (Orthogonal Elbows) liền mạch 100% không kẽ hở:**
        1. Chia đường gấp khúc thành các phân đoạn thẳng ngắn ghép nối liên tiếp (`connector` dọc, `connector` ngang).
        2. Tạo độ chồng lấp nhỏ khoảng `0.02 inch` (overlap) tại các điểm giao cắt của khuỷu gập để triệt tiêu hoàn toàn khe hở chỉ trắng do cơ chế chống răng cưa (anti-aliasing) của PowerPoint.
        3. Đồng bộ hóa màu viền bằng `.line.fill.solid()` và `.line.fill.fore_color.rgb = color` trùng khít hoàn toàn với màu thân đường dẫn để tạo khớp nối liền mạch, trơn tru tuyệt đối.
    *   ✅ **Tránh đè chữ ở nhãn luồng:** Các nhãn luồng (như "CÓ" / "KHÔNG") phải được vẽ bằng hộp văn bản không nền, không viền và đặt đúng tọa độ khoảng trống an toàn (gap) giữa các thẻ card để triệt tiêu hoàn toàn lỗi chồng đè chữ (`Rule 2 Overlap`).

