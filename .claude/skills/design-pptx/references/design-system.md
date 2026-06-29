# Design PPTX Specification — V5.1 (Comprehensive Widescreen Reference with Soft Shadow Upgrade)

> **Nguồn gốc:** Kế thừa toàn bộ cấu trúc chi tiết từ V3 & V5 (layout constants, palette, 4-tier hierarchy, bullet system, 12 component types, anti-patterns, build workflow, audit script, slide recipes, self-healing audit loop). Tích hợp **chuẩn kích thước chữ Widescreen** từ bản Final — phóng lớn tối đa khả năng đọc trên màn hình trình chiếu. Bổ sung: cơ chế inline bolding (`add_rich_text`), staggered accent bars, overlapping header icons, safety weight badges, process card dividers và **nâng cấp hệ thống bóng đổ Neumorphic cao cấp chống hiệu ứng 3D mặc định**.

---

## 1. Canvas & Layout Constants

```python
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

SLIDE_W, SLIDE_H = Inches(13.333), Inches(7.5)   # 16:9
MARGIN_L = MARGIN_R = Inches(0.6)
CONTENT_W = SLIDE_W - MARGIN_L - MARGIN_R        # 12.133 inch

# Vertical regions — TUYỆT ĐỐI KHÔNG ĐỔI
TITLE_Y        = Inches(0.30)    # textbox top
TITLE_H        = Inches(1.15)    # vừa 2 dòng @ 35pt Bold ls=1.05
DIVIDER_Y      = Inches(1.50)    # đường kẻ mảnh ngay sát title
LEDE_Y         = Inches(1.55)
LEDE_H         = Inches(0.40)
BODY_Y         = Inches(2.00)    # body bắt đầu khi có lede
BODY_Y_NOLEDE  = Inches(1.60)    # body khi KHÔNG có lede
FOOTER_BAR_Y   = Inches(6.55)    # orange callout bar top
FOOTER_BAR_H   = Inches(0.50)    # orange callout bar height
FOOTER_Y       = Inches(7.15)    # branding + page number text
BODY_MAX_Y     = Inches(7.00)    # content phải kết thúc trước đây
SLIDE_BOTTOM   = Inches(7.50)    # edge tuyệt đối
```

**Vùng body khả dụng:** `y ∈ [2.00, 6.55]` = **4.55 inch** (bên trên footer bar).  
Khi không có orange footer bar: `y ∈ [2.00, 7.00]` = **5.00 inch**.

---

## 2. Palette (HEX) — KHÔNG đổi giữa slides

| Token          | HEX       | Alias       | Dùng cho                                                    |
|----------------|-----------|-------------|-------------------------------------------------------------|
| `PRIMARY`      | `#2933D9` | Brand Blue  | Title text, card header band, section divider bg, H1       |
| `ACCENT`       | `#3543F6` | Mid Blue    | Metric card bg (intentionally lighter để số trắng nổi)      |
| `LIGHT_BLUE`   | `#7594FF` | Soft Blue   | L3 tier label, rare accent; card tier hierarchy             |
| `PALE_BLUE`    | `#ECF3FF` | Near-White  | Card body bg (dominant fill), quote bar                    |
| `ORANGE`       | `#DD5320` | Accent CTA  | Eyebrow number, bullet ▪ glyph, footer bar, number badges  |
| `TEXT`         | `#40444C` | Charcoal    | Body text, bullet content, footer branding                  |
| `DIVIDER`      | `#EDEEF1` | Light Gray  | Horizontal rule dưới title                                  |
| `WHITE`        | `#FFFFFF` | White       | Chữ trên nền đậm, số metric cards                          |
| `SHADOW`       | `#DDE0E5` | Soft Gray   | Lớp hình khối nằm dưới (lệch tọa độ) để tạo bóng đổ mềm     |

```python
PRIMARY = RGBColor(0x29, 0x33, 0xD9)
ACCENT = RGBColor(0x35, 0x43, 0xF6)
LIGHT_BLUE = RGBColor(0x75, 0x94, 0xFF)
PALE_BLUE = RGBColor(0xEC, 0xF3, 0xFF)
ORANGE = RGBColor(0xDD, 0x53, 0x20)
TEXT = RGBColor(0x40, 0x44, 0x4C)
DIVIDER = RGBColor(0xED, 0xEE, 0xF1)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SHADOW = RGBColor(0xDD, 0xE0, 0xE5)
FONT = "Be Vietnam Pro"
```

### 4-Tier Color Hierarchy (KPI / Org Levels)
* **L1 (Strategic / root node):** `PRIMARY` (`#2933D9`)
* **L2 (Operational):** `ACCENT` (`#3543F6`)
* **L3 (Tactical):** `LIGHT_BLUE` (`#7594FF`)
* **L4 (Execution / leaf node):** `PALE_BLUE` (`#ECF3FF`)

---

## 3. Typography Scale — Widescreen Standard (Kích thước lớn)

| pt    | Role                              | Bold? | Color(s)                        |
|-------|-----------------------------------|-------|---------------------------------|
| 52    | Closing slide title               | Yes   | `WHITE`                         |
| 44    | Section divider chapter title     | Yes   | `WHITE` on PRIMARY bg           |
| 42    | Cover main title                  | Yes   | `PRIMARY`                       |
| 38    | Chapter number (section divider)  | Yes   | `ORANGE`                        |
| 35    | H1 slide title (Module 01)        | Yes   | `PRIMARY` (inline `ORANGE` eyebrow) |
| 32–30 | H1 slide title (Module 02–05)     | Yes   | `PRIMARY` (denser sections)     |
| 28    | Large KPI metric number           | Yes   | `WHITE` on ACCENT card          |
| 22    | Numbered step label in process    | Yes   | `ORANGE`                        |
| 20    | Cover subtitle                    | No    | `TEXT`                          |
| 18    | Section divider tagline           | No    | `PALE_BLUE`                     |
| 14    | Agenda section label              | Yes   | `PRIMARY`                       |
| 13    | Lede text (dẫn nhập slide)        | Italic| `TEXT` (hỗ trợ bold highlights) |
| 12.5  | Bullet content (2–3 col cards)    | No    | `TEXT` (▪ `ORANGE`)             |
| 12.5  | Quote / Callout text              | Italic| `PALE_BLUE` trên nền PRIMARY   |
| 12    | Card header band text             | Yes   | `WHITE`                         |
| 12    | Table header cell                 | Yes   | `WHITE` on PRIMARY              |
| 12    | Conclusion bar text               | Yes   | `WHITE` on ORANGE               |
| 11    | Process chain body bullets        | No    | `TEXT` (▪ `ORANGE`)             |
| 11    | Table data cell                   | No    | `TEXT` (hỗ trợ markdown bullet) |
| 11    | Weight badge text                 | Yes   | `WHITE` on ORANGE pill          |
| 10.5  | Metric card note line             | No    | `PALE_BLUE`                     |
| 10    | Metric card label, footer text    | Yes/No| `PALE_BLUE` / `TEXT`            |

**Font:** `Be Vietnam Pro` (fallback: Arial, Segoe UI).  
**Line spacing:** `1.05` title, `1.15` bảng/trích dẫn, `1.3` body bullets.

---

## 4. Inline Bold Engine (`add_rich_text`)

**Tính năng bôi đậm từ khóa chính trực tiếp trong nội dung bằng cú pháp markdown `**từ khóa**`:**

```python
def add_rich_text(p, text, size=11, color=TEXT, default_bold=False, italic=False):
    if not text:
        return
    if "**" in text:
        parts = text.split("**")
        for idx, part in enumerate(parts):
            if idx % 2 == 1:
                r = p.add_run(); r.text = part
                r.font.name = FONT; r.font.size = Pt(size)
                r.font.bold = True; r.font.italic = italic
                r.font.color.rgb = color
            else:
                if part:
                    r = p.add_run(); r.text = part
                    r.font.name = FONT; r.font.size = Pt(size)
                    r.font.bold = default_bold; r.font.italic = italic
                    r.font.color.rgb = color
    else:
        r = p.add_run(); r.text = text
        r.font.name = FONT; r.font.size = Pt(size)
        r.font.bold = default_bold; r.font.italic = italic
        r.font.color.rgb = color
```

---

## 5. Title + Eyebrow — 1 TextBox, 2 Runs

```python
def slide_header(slide, eyebrow, title_text):
    tb = slide.shapes.add_textbox(MARGIN_L, TITLE_Y, CONTENT_W, TITLE_H)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = tf.margin_right = Inches(0.02)
    tf.margin_top = tf.margin_bottom = Inches(0.0)
    p = tf.paragraphs[0]; p.line_spacing = 1.05
    
    r1 = p.add_run(); r1.text = eyebrow.upper() + "   "
    r1.font.name = FONT; r1.font.size = Pt(35); r1.font.bold = True
    r1.font.color.rgb = ORANGE
    
    r2 = p.add_run(); r2.text = title_text.upper()
    r2.font.name = FONT; r2.font.size = Pt(35); r2.font.bold = True
    r2.font.color.rgb = PRIMARY
    
    # Divider line under title
    hline(slide, MARGIN_L, DIVIDER_Y, SLIDE_W - MARGIN_R, color=DIVIDER, width=0.75)

def hline(slide, x1, y, x2, color=DIVIDER, width=0.75):
    # Dùng shape chữ nhật rất mỏng để làm đường kẻ chính xác
    h = Inches(0.01) * width
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x1, y - h/2, x2 - x1, h)
    s.shadow.inherit = False
    s.fill.solid(); s.fill.fore_color.rgb = color
    s.line.fill.background()
```

---

## 6. Shape Primitives & Neumorphic Soft Shadow

**TUYỆT ĐỐI CẤM sử dụng hiệu ứng đổ bóng 3D hoặc bóng thô mặc định của PowerPoint.**
Để tạo độ nổi trực quan cao cấp, hãy vẽ lớp hình nền màu xám nhạt (`SHADOW` token `#DDE0E5`) lệch tọa độ an toàn bên dưới card:

```python
def make_shape(slide, kind, x, y, w, h, fill=None, line=None, line_w=0.75, radius=None):
    s = slide.shapes.add_shape(kind, x, y, w, h)
    s.shadow.inherit = False
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid(); s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line; s.line.width = Pt(line_w)
    if radius is not None and kind == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    tf = s.text_frame
    tf.margin_left = tf.margin_right = Inches(0.12)
    tf.margin_top = tf.margin_bottom = Inches(0.08)
    tf.word_wrap = True
    return s

def add_shadow(slide, x, y, w, h, radius=0.06, offset=0.06):
    """Bóng đổ Neumorphic mềm mại, vẽ TRƯỚC KHI vẽ card chứa chính."""
    return make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 
                      x + Inches(offset), y + Inches(offset), w, h, 
                      fill=SHADOW, line=None, radius=radius)
```

---

## 7. Bullet System — 2-Color (Chữ ký design số 2)

Bullets dùng **2 run riêng biệt trong cùng 1 paragraph**:

```python
def add_bullet(tf, text, size=12.5):
    p = tf.add_paragraph() if tf.paragraphs and tf.paragraphs[0].text else tf.paragraphs[0]
    p.line_spacing = 1.3
    # Run 1 — bullet glyph màu ORANGE
    r_bullet = p.add_run(); r_bullet.text = "▪ "
    r_bullet.font.name = FONT; r_bullet.font.size = Pt(size)
    r_bullet.font.bold = True; r_bullet.font.color.rgb = ORANGE
    # Run 2 — nội dung màu TEXT (hỗ trợ add_rich_text cho inline bold)
    add_rich_text(p, text, size=size, color=TEXT)
```

---

## 8. Orange Footer Bar — Editorial Voice

```python
def conclusion(slide, y, text, color=ORANGE, size=12):
    # Shadow lót dưới
    add_shadow(slide, MARGIN_L, y, CONTENT_W, Inches(0.50), radius=0.25, offset=0.04)
    # Card chính
    s = make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE,
        MARGIN_L, y, CONTENT_W, Inches(0.50), radius=0.25, fill=color)
    tf = s.text_frame
    tf.margin_left = tf.margin_right = Inches(0.15)
    tf.margin_top = tf.margin_bottom = Inches(0.08)
    tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    add_rich_text(p, text, size=size, color=WHITE, default_bold=True)
```

---

## 9. Footer (Branding + Page Number)

```python
def add_footer(slide, page_num, tagline_text):
    # Left — tagline branding động
    tx = slide.shapes.add_textbox(MARGIN_L, Inches(7.15), Inches(10), Inches(0.3))
    tf = tx.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = Inches(0)
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = tagline_text
    r.font.name = FONT; r.font.size = Pt(10); r.font.color.rgb = TEXT
    
    # Right — page number
    tx2 = slide.shapes.add_textbox(SLIDE_W - Inches(1.5), Inches(7.15), Inches(1.0), Inches(0.3))
    tf2 = tx2.text_frame; tf2.word_wrap = True; tf2.margin_right = tf2.margin_top = Inches(0)
    p2 = tf2.paragraphs[0]; p2.alignment = PP_ALIGN.RIGHT
    r2 = p2.add_run(); r2.text = f"Page {page_num}"
    r2.font.name = FONT; r2.font.size = Pt(10); r2.font.color.rgb = TEXT
```

---

## 10. Anti-Patterns — Các lỗi cấm kỵ

* ❌ **Đè chữ (Overlap):** Tọa độ Y cứng khiến text box trên đè lên text box dưới. Khắc phục: tính toán Y động.
* ❌ **Tràn viền dưới:** Để các hình khối vượt quá Y = 7.12. Khắc phục: giảm font size, giảm khoảng cách dòng, hoặc rút ngắn bullets.
* ❌ **Dùng bóng đổ 3D mặc định:** Gây bẩn slide và khó đọc. Khắc phục: Tắt shadow mặc định (`s.shadow.inherit=False`) và dùng hàm `add_shadow()`.
* ❌ **Bullet thô sơ:** Dùng chấm tròn đen mặc định. Khắc phục: Dùng bullet 2 màu (▪ cam và chữ xám).
* ❌ **Table PowerPoint mặc định:** Khó căn chỉnh padding và màu sắc. Khắc phục: Dùng Table-as-shapes (tạo bảng bằng các mảnh ghép Rectangle).
* ❌ **Chữ chìm mờ nền (Watermark):** Gây rối mắt và giảm độ tương phản. Khắc phục: Cấm tuyệt đối.
