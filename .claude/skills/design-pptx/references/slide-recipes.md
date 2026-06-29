# Thư viện Mẫu Slide PowerPoint — Slide Recipes (V5.1 Standard)

Tài liệu này cung cấp mã nguồn Python mẫu (`python-pptx`) chuẩn kỹ thuật cho 9 loại slide phổ biến nhất. Các đoạn mã đã được tích hợp đầy đủ hệ thống bóng đổ Neumorphic (`add_shadow`), inline bolding (`add_rich_text`) và bullet 2 màu (`add_bullet`).

---

## Mẫu A: Cover Slide (Trang bìa - Layout A)

```python
def make_cover_slide(prs, eyebrow_text, title_text, subtitle_text, author_role, author_name, date_text):
    slide_layout = prs.slide_layouts[6] # Blank slide
    slide = prs.slides.add_slide(slide_layout)
    
    # 1. Eyebrow
    tx_eyebrow = slide.shapes.add_textbox(MARGIN_L, Inches(0.80), CONTENT_W, Inches(0.40))
    tf = tx_eyebrow.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = Inches(0)
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = eyebrow_text.upper()
    r.font.name = FONT; r.font.size = Pt(14); r.font.bold = True; r.font.color.rgb = ORANGE
    
    # 2. Main Title (split colors if needed or solid PRIMARY)
    tx_title = slide.shapes.add_textbox(MARGIN_L, Inches(1.30), CONTENT_W, Inches(1.80))
    tf_t = tx_title.text_frame; tf_t.word_wrap = True; tf_t.margin_left = tf_t.margin_top = Inches(0)
    p_t = tf_t.paragraphs[0]; p_t.line_spacing = 1.05
    r_t = p_t.add_run(); r_t.text = title_text.upper()
    r_t.font.name = FONT; r_t.font.size = Pt(42); r_t.font.bold = True; r_t.font.color.rgb = PRIMARY
    
    # 3. Subtitle
    tx_sub = slide.shapes.add_textbox(MARGIN_L, Inches(3.40), CONTENT_W, Inches(0.80))
    tf_s = tx_sub.text_frame; tf_s.word_wrap = True; tf_s.margin_left = tf_s.margin_top = Inches(0)
    p_s = tf_s.paragraphs[0]
    add_rich_text(p_s, subtitle_text, size=20, color=TEXT)
    
    # 4. Author Block
    tx_auth = slide.shapes.add_textbox(MARGIN_L, Inches(4.50), CONTENT_W, Inches(1.00))
    tf_a = tx_auth.text_frame; tf_a.word_wrap = True; tf_a.margin_left = tf_a.margin_top = Inches(0)
    p_a = tf_a.paragraphs[0]
    r_k = p_a.add_run(); r_k.text = author_role.upper() + "\n"
    r_k.font.name = FONT; r_k.font.size = Pt(12); r_k.font.bold = True; r_k.font.color.rgb = ORANGE
    p_name = tf_a.add_paragraph()
    r_n = p_name.add_run(); r_n.text = author_name
    r_n.font.name = FONT; r_n.font.size = Pt(20); r_n.font.bold = True; r_n.font.color.rgb = PRIMARY
    
    # 5. Date Pill
    make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, MARGIN_L, Inches(5.80), Inches(2.20), Inches(0.45), fill=PALE_BLUE, radius=0.20)
    tx_d = slide.shapes.add_textbox(MARGIN_L, Inches(5.80), Inches(2.20), Inches(0.45))
    tf_d = tx_d.text_frame; tf_d.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_d = tf_d.paragraphs[0]; p_d.alignment = PP_ALIGN.CENTER
    r_d = p_d.add_run(); r_d.text = date_text
    r_d.font.name = FONT; r_d.font.size = Pt(11); r_d.font.bold = True; r_d.font.color.rgb = PRIMARY
    
    # 6. Staggered Accent Bars (Right aligned decorative)
    deco_colors = [PRIMARY, ACCENT, LIGHT_BLUE, PALE_BLUE]
    deco_widths = [Inches(3.2), Inches(2.8), Inches(2.4), Inches(2.0)]
    right_edge = SLIDE_W - Inches(0.6)
    for i, color in enumerate(deco_colors):
        w = deco_widths[i]; x = right_edge - w
        make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(3.0 + i*0.7), w, Inches(0.55), fill=color, line=None, radius=0.10)
```

---

## Mẫu B: Agenda Slide (Trang chương trình nghị sự - Layout B)

```python
def make_agenda_slide(prs, list_items, page_tagline):
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    slide_header(slide, "AGENDA", "CHƯƠNG TRÌNH NGHỊ SỰ")
    
    start_y = Inches(1.80)
    row_h = Inches(0.85)
    gap = Inches(0.15)
    
    for idx, item in enumerate(list_items):
        y = start_y + idx * (row_h + gap)
        title, subtitle = item
        
        # Shadow + Rounded card
        add_shadow(slide, MARGIN_L, y, CONTENT_W, row_h, radius=0.06)
        make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, MARGIN_L, y, CONTENT_W, row_h, fill=PALE_BLUE, radius=0.06)
        
        # Number indicator (ORANGE)
        tx_num = slide.shapes.add_textbox(MARGIN_L + Inches(0.15), y + Inches(0.15), Inches(0.50), Inches(0.55))
        tf_num = tx_num.text_frame; tf_num.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_num = tf_num.paragraphs[0]; p_num.alignment = PP_ALIGN.CENTER
        r_num = p_num.add_run(); r_num.text = f"{idx + 1:02d}"
        r_num.font.name = FONT; r_num.font.size = Pt(20); r_num.font.bold = True; r_num.font.color.rgb = ORANGE
        
        # Text Block (Title & Subtitle)
        tx_text = slide.shapes.add_textbox(MARGIN_L + Inches(0.85), y + Inches(0.08), CONTENT_W - Inches(1.00), Inches(0.70))
        tf_text = tx_text.text_frame; tf_text.word_wrap = True
        
        # Title (PRIMARY)
        p_t = tf_text.paragraphs[0]
        r_t = p_t.add_run(); r_t.text = title.upper()
        r_t.font.name = FONT; r_t.font.size = Pt(14); r_t.font.bold = True; r_t.font.color.rgb = PRIMARY
        
        # Subtitle (TEXT)
        p_s = tf_text.add_paragraph()
        r_s = p_s.add_run(); r_s.text = subtitle
        r_s.font.name = FONT; r_s.font.size = Pt(10.5); r_s.font.color.rgb = TEXT
        
    add_footer(slide, 2, page_tagline)
```

---

## Mẫu C: Section Divider Slide (Trang ngăn cách phân đoạn - Layout C)

```python
def make_section_divider_slide(prs, part_num, category_text, title_text, tagline_text, page_tagline, page_num):
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    # 1. Dark background
    make_shape(slide, MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H, fill=PRIMARY)
    
    # 2. Orange accent bar
    make_shape(slide, MSO_SHAPE.RECTANGLE, MARGIN_L, Inches(2.40), Inches(0.80), Inches(0.08), fill=ORANGE)
    
    # 3. Category label
    tx_cat = slide.shapes.add_textbox(MARGIN_L, Inches(2.55), Inches(8), Inches(0.35))
    tf_c = tx_cat.text_frame; tf_c.margin_left = tf_c.margin_top = Inches(0)
    p_c = tf_c.paragraphs[0]
    r_c = p_c.add_run(); r_c.text = f"PHẦN {part_num:02d} · {category_text.upper()}"
    r_c.font.name = FONT; r_c.font.size = Pt(14); r_c.font.bold = True; r_c.font.color.rgb = PALE_BLUE
    
    # 4. Big number
    tx_num = slide.shapes.add_textbox(MARGIN_L, Inches(3.00), Inches(8), Inches(0.80))
    tf_n = tx_num.text_frame; tf_n.margin_left = tf_n.margin_top = Inches(0)
    p_n = tf_n.paragraphs[0]
    r_n = p_n.add_run(); r_n.text = f"{part_num:02d}"
    r_n.font.name = FONT; r_n.font.size = Pt(38); r_n.font.bold = True; r_n.font.color.rgb = ORANGE
    
    # 5. Main Title (Dynamic Y placement)
    title_upper = title_text.upper()
    lines_count = 2 if len(title_upper) > 28 else 1
    title_y = Inches(3.80)
    estimated_title_h = lines_count * Inches(0.75)
    tagline_y = title_y + estimated_title_h + Inches(0.20)
    
    tx_title = slide.shapes.add_textbox(MARGIN_L, title_y, Inches(10), estimated_title_h + Inches(0.1))
    tf_t = tx_title.text_frame; tf_t.word_wrap = True; tf_t.margin_left = tf_t.margin_top = Inches(0)
    p_t = tf_t.paragraphs[0]
    r_t = p_t.add_run(); r_t.text = title_upper
    r_t.font.name = FONT; r_t.font.size = Pt(44); r_t.font.bold = True; r_t.font.color.rgb = WHITE
    
    # 6. Tagline
    tx_tag = slide.shapes.add_textbox(MARGIN_L, tagline_y, Inches(10), Inches(0.55))
    tf_tg = tx_tag.text_frame; tf_tg.word_wrap = True; tf_tg.margin_left = tf_tg.margin_top = Inches(0)
    p_tg = tf_tg.paragraphs[0]
    r_tg = p_tg.add_run(); r_tg.text = tagline_text
    r_tg.font.name = FONT; r_tg.font.size = Pt(18); r_tg.font.color.rgb = PALE_BLUE
    
    # 7. Right Staggered Accent Bars (Variant colors)
    deco_colors = [ACCENT, LIGHT_BLUE, PALE_BLUE, ORANGE]
    deco_widths = [Inches(3.2), Inches(2.8), Inches(2.4), Inches(2.0)]
    right_edge = SLIDE_W - Inches(0.6)
    for i, color in enumerate(deco_colors):
        w = deco_widths[i]; x = right_edge - w
        make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(3.0 + i*0.7), w, Inches(0.55), fill=color, line=None, radius=0.10)
        
    # Dark background footer (using PALE_BLUE color)
    add_footer(slide, page_num, page_tagline)
    # Ghi đè màu chữ ở footer của trang divider thành PALE_BLUE
    for shape in slide.shapes:
        if shape.has_text_frame and ("Page" in shape.text_frame.text or page_tagline in shape.text_frame.text):
            for p in shape.text_frame.paragraphs:
                for run in p.runs:
                    run.font.color.rgb = PALE_BLUE
```

---

## Mẫu D: Two-Column Content Cards (Slide hai cột - Layout D)

```python
def make_two_col_cards_slide(prs, eyebrow, title, lede_text, card1_data, card2_data, conclusion_text, page_tagline, page_num):
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    slide_header(slide, eyebrow, title)
    
    # 1. Lede
    tx_lede = slide.shapes.add_textbox(MARGIN_L, LEDE_Y, CONTENT_W, LEDE_H)
    tf_l = tx_lede.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_top = Inches(0)
    p_l = tf_l.paragraphs[0]; p_l.font.italic = True
    add_rich_text(p_l, lede_text, size=13, color=TEXT, italic=True)
    
    # 2. Cards Dimensions
    card_w = Inches(5.96)
    card_h = Inches(3.40)
    gap = Inches(0.20)
    card_y = Inches(2.00)
    
    # Card 1
    c1_title, c1_bullets, c1_icon = card1_data
    # Shadow
    add_shadow(slide, MARGIN_L, card_y, card_w, card_h, radius=0.06)
    # Container
    make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, MARGIN_L, card_y, card_w, card_h, fill=PALE_BLUE, radius=0.06)
    # Header band
    make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, MARGIN_L, card_y, card_w, Inches(0.60), fill=PRIMARY, radius=0.06)
    # Che phủ cạnh dưới bo góc của header để tạo liên kết khối phẳng
    make_shape(slide, MSO_SHAPE.RECTANGLE, MARGIN_L, card_y + Inches(0.30), card_w, Inches(0.30), fill=PRIMARY)
    
    # Header Text
    tx_h1 = slide.shapes.add_textbox(MARGIN_L + Inches(0.15), card_y, card_w - Inches(0.60), Inches(0.60))
    tf_h1 = tx_h1.text_frame; tf_h1.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_h1 = tf_h1.paragraphs[0]
    r_h1 = p_h1.add_run(); r_h1.text = c1_title.upper()
    r_h1.font.name = FONT; r_h1.font.size = Pt(12); r_h1.font.bold = True; r_h1.font.color.rgb = WHITE
    
    # Overlapping Header Icon
    if c1_icon:
        icon_size = Inches(0.38)
        cx = MARGIN_L + card_w - Inches(0.38)
        cy = card_y + Inches(0.30)
        make_shape(slide, MSO_SHAPE.OVAL, cx - icon_size/2, cy - icon_size/2, icon_size, icon_size, fill=ORANGE, line=None)
        inner_size = icon_size * 0.55
        make_shape(slide, c1_icon, cx - inner_size/2, cy - inner_size/2, inner_size, inner_size, fill=WHITE, line=None)
        
    # Bullets Body
    tx_b1 = slide.shapes.add_textbox(MARGIN_L + Inches(0.15), card_y + Inches(0.72), card_w - Inches(0.30), card_h - Inches(0.85))
    tf_b1 = tx_b1.text_frame; tf_b1.word_wrap = True
    for bullet in c1_bullets:
        add_bullet(tf_b1, bullet, size=12.5)
        
    # Card 2
    c2_title, c2_bullets, c2_icon = card2_data
    c2_x = MARGIN_L + card_w + gap
    # Shadow
    add_shadow(slide, c2_x, card_y, card_w, card_h, radius=0.06)
    # Container
    make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, c2_x, card_y, card_w, card_h, fill=PALE_BLUE, radius=0.06)
    # Header band
    make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, c2_x, card_y, card_w, Inches(0.60), fill=PRIMARY, radius=0.06)
    make_shape(slide, MSO_SHAPE.RECTANGLE, c2_x, card_y + Inches(0.30), card_w, Inches(0.30), fill=PRIMARY)
    
    tx_h2 = slide.shapes.add_textbox(c2_x + Inches(0.15), card_y, card_w - Inches(0.60), Inches(0.60))
    tf_h2 = tx_h2.text_frame; tf_h2.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_h2 = tf_h2.paragraphs[0]
    r_h2 = p_h2.add_run(); r_h2.text = c2_title.upper()
    r_h2.font.name = FONT; r_h2.font.size = Pt(12); r_h2.font.bold = True; r_h2.font.color.rgb = WHITE
    
    if c2_icon:
        icon_size = Inches(0.38)
        cx = c2_x + card_w - Inches(0.38)
        cy = card_y + Inches(0.30)
        make_shape(slide, MSO_SHAPE.OVAL, cx - icon_size/2, cy - icon_size/2, icon_size, icon_size, fill=ORANGE, line=None)
        inner_size = icon_size * 0.55
        make_shape(slide, c2_icon, cx - inner_size/2, cy - inner_size/2, inner_size, inner_size, fill=WHITE, line=None)
        
    tx_b2 = slide.shapes.add_textbox(c2_x + Inches(0.15), card_y + Inches(0.72), card_w - Inches(0.30), card_h - Inches(0.85))
    tf_b2 = tx_b2.text_frame; tf_b2.word_wrap = True
    for bullet in c2_bullets:
        add_bullet(tf_b2, bullet, size=12.5)
        
    # 3. Orange Conclusion Bar
    if conclusion_text:
        conclusion(slide, Inches(6.55), conclusion_text)
        
    add_footer(slide, page_num, page_tagline)
```

---

## Mẫu G: Metric Cards Slide (Slide số liệu - Layout G)

```python
def make_metric_row_slide(prs, eyebrow, title, lede_text, list_metrics, page_tagline, page_num):
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    slide_header(slide, eyebrow, title)
    
    # Lede
    tx_lede = slide.shapes.add_textbox(MARGIN_L, LEDE_Y, CONTENT_W, LEDE_H)
    tf_l = tx_lede.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_top = Inches(0)
    p_l = tf_l.paragraphs[0]; p_l.font.italic = True
    add_rich_text(p_l, lede_text, size=13, color=TEXT, italic=True)
    
    card_w = Inches(2.88)
    card_h = Inches(1.85)
    gap = Inches(0.20)
    card_y = Inches(2.20)
    
    for idx, metric in enumerate(list_metrics[:4]): # Max 4 cards/row
        label, number, note, icon = metric
        cx = MARGIN_L + idx * (card_w + gap)
        
        # Shadow
        add_shadow(slide, cx, card_y, card_w, card_h, radius=0.06)
        # Card Container (ACCENT)
        make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, cx, card_y, card_w, card_h, fill=ACCENT, radius=0.06)
        
        # Text positioning
        tx = slide.shapes.add_textbox(cx + Inches(0.12), card_y + Inches(0.10), card_w - Inches(0.24), card_h - Inches(0.20))
        tf = tx.text_frame; tf.word_wrap = True
        
        # Label (L3 tier)
        p_l = tf.paragraphs[0]
        r_l = p_l.add_run(); r_l.text = label.upper()
        r_l.font.name = FONT; r_l.font.size = Pt(10); r_l.font.bold = True; r_l.font.color.rgb = PALE_BLUE
        
        # Big Number (WHITE)
        p_n = tf.add_paragraph()
        p_n.line_spacing = 1.05
        r_n = p_n.add_run(); r_n.text = number
        r_n.font.name = FONT; r_n.font.size = Pt(28); r_n.font.bold = True; r_n.font.color.rgb = WHITE
        
        # Note
        p_nt = tf.add_paragraph()
        r_nt = p_nt.add_run(); r_nt.text = note
        r_nt.font.name = FONT; r_nt.font.size = Pt(10.5); r_nt.font.color.rgb = PALE_BLUE
        
        # Icon (LIGHT_BLUE)
        if icon:
            icon_size = Inches(0.32)
            ix = cx + card_w - Inches(0.44)
            iy = card_y + Inches(0.12)
            make_shape(slide, icon, ix, iy, icon_size, icon_size, fill=LIGHT_BLUE, line=None)
            
    add_footer(slide, page_num, page_tagline)
```

---

## Mẫu H: Process Subway Flow (Slide tiến trình liên hoàn - Layout H)

```python
def make_process_flow_slide(prs, eyebrow, title, lede_text, steps, conclusion_text, page_tagline, page_num):
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    slide_header(slide, eyebrow, title)
    
    # Lede
    tx_lede = slide.shapes.add_textbox(MARGIN_L, LEDE_Y, CONTENT_W, LEDE_H)
    tf_l = tx_lede.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_top = Inches(0)
    p_l = tf_l.paragraphs[0]; p_l.font.italic = True
    add_rich_text(p_l, lede_text, size=13, color=TEXT, italic=True)
    
    # Dimensions for 4 steps
    n_steps = len(steps)
    step_w = Inches(2.88)
    step_h = Inches(3.20)
    gap = Inches(0.20)
    
    track_y = Inches(2.20)
    card_y = Inches(2.40)
    
    # 1. Subway Track Line (DIVIDER)
    hline(slide, MARGIN_L + Inches(0.40), track_y, MARGIN_L + CONTENT_W - Inches(0.40), color=DIVIDER, width=4)
    
    for idx, step in enumerate(steps[:4]):
        num_str, cat_title, bullets = step
        cx = MARGIN_L + idx * (step_w + gap)
        
        # 2. Subway Oval Dot Nodes
        dot_r = Inches(0.30)
        dot_cx = cx + step_w / 2
        make_shape(slide, MSO_SHAPE.OVAL, dot_cx - dot_r/2, track_y - dot_r/2, dot_r, dot_r, fill=ORANGE, line=None)
        inner_r = Inches(0.16)
        make_shape(slide, MSO_SHAPE.OVAL, dot_cx - inner_r/2, track_y - inner_r/2, inner_r, inner_r, fill=WHITE, line=None)
        
        # 3. Shadow
        add_shadow(slide, cx, card_y, step_w, step_h, radius=0.06)
        # 4. Step Box Container (PALE_BLUE)
        make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, cx, card_y, step_w, step_h, radius=0.06, fill=PALE_BLUE)
        
        # Number Label
        tx_num = slide.shapes.add_textbox(cx + Inches(0.12), card_y + Inches(0.10), step_w - Inches(0.24), Inches(0.40))
        tf_num = tx_num.text_frame; tf_num.margin_left = tf_num.margin_top = Inches(0)
        p_num = tf_num.paragraphs[0]; p_num.alignment = PP_ALIGN.CENTER
        r_num = p_num.add_run(); r_num.text = num_str.upper()
        r_num.font.name = FONT; r_num.font.size = Pt(22); r_num.font.bold = True; r_num.font.color.rgb = ORANGE
        
        # Category Title
        tx_cat = slide.shapes.add_textbox(cx + Inches(0.12), card_y + Inches(0.50), step_w - Inches(0.24), Inches(0.38))
        tf_cat = tx_cat.text_frame; tf_cat.word_wrap = True; tf_cat.margin_left = tf_cat.margin_top = Inches(0)
        p_cat = tf_cat.paragraphs[0]; p_cat.alignment = PP_ALIGN.CENTER
        r_cat = p_cat.add_run(); r_cat.text = cat_title.upper()
        r_cat.font.name = FONT; r_cat.font.size = Pt(11.5); r_cat.font.bold = True; r_cat.font.color.rgb = PRIMARY
        
        # Process Card Divider Line
        make_shape(slide, MSO_SHAPE.RECTANGLE, cx + Inches(0.12), card_y + Inches(0.92), step_w - Inches(0.24), Inches(0.01), fill=DIVIDER, line=None)
        
        # Bullets content
        tx_bullets = slide.shapes.add_textbox(cx + Inches(0.12), card_y + Inches(1.00), step_w - Inches(0.24), step_h - Inches(1.10))
        tf_bullets = tx_bullets.text_frame; tf_bullets.word_wrap = True
        for b in bullets:
            add_bullet(tf_bullets, b, size=11)
            
    # 5. Conclusion
    if conclusion_text:
        conclusion(slide, Inches(6.55), conclusion_text)
        
    add_footer(slide, page_num, page_tagline)
```

---

## Mẫu I: Comparison Table (Slide bảng so sánh - Layout I)

```python
def make_table_slide(prs, eyebrow, title, lede_text, col_widths, row_heights, data, conclusion_text, page_tagline, page_num):
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    slide_header(slide, eyebrow, title)
    
    # Lede
    tx_lede = slide.shapes.add_textbox(MARGIN_L, LEDE_Y, CONTENT_W, LEDE_H)
    tf_l = tx_lede.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_top = Inches(0)
    p_l = tf_l.paragraphs[0]; p_l.font.italic = True
    add_rich_text(p_l, lede_text, size=13, color=TEXT, italic=True)
    
    # Table start coordinate
    table_x = MARGIN_L
    table_y = Inches(2.10)
    
    # Render table as individual Shapes with Neumorphic Shadows lót dưới toàn khối
    simple_table(slide, table_x, table_y, col_widths, row_heights, data, header_rows=1)
    
    # Conclusion
    if conclusion_text:
        conclusion(slide, Inches(6.55), conclusion_text)
        
    add_footer(slide, page_num, page_tagline)

def simple_table(slide, x, y, col_widths, row_heights, data, header_rows=1):
    total_w = sum(col_widths)
    total_h = sum(row_heights)
    
    # Tạo bóng đổ Neumorphic mượt mà nguyên khối cho cả Table
    add_shadow(slide, x, y, Inches(total_w), Inches(total_h), radius=0.06)
    
    cy = y
    for r_idx, row in enumerate(data):
        cx = x
        is_header = r_idx < header_rows
        fill = PRIMARY if is_header else PALE_BLUE
        text_color = WHITE if is_header else TEXT
        pt_size = 12 if is_header else 11
        
        for c_idx, cell_text in enumerate(row):
            w = col_widths[c_idx]
            h = row_heights[r_idx]
            
            # Check for Safety Weight Badge: chỉ tạo pill cam khi text cực ngắn dạng số %
            is_weight = (not is_header) and cell_text.strip().endswith("%") and len(cell_text.strip()) <= 5
            
            s = make_shape(slide, MSO_SHAPE.RECTANGLE, cx, cy, Inches(w), Inches(h), fill=fill, line=WHITE, line_w=1.0)
            
            if is_weight:
                # Orange pill badge
                badge_w, badge_h = Inches(0.80), Inches(0.35)
                bx = cx + (Inches(w) - badge_w) / 2
                by = cy + (Inches(h) - badge_h) / 2
                badge = make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, badge_w, badge_h, fill=ORANGE, line=None, radius=0.25)
                tf_b = badge.text_frame; tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
                p_b = tf_b.paragraphs[0]; p_b.alignment = PP_ALIGN.CENTER
                add_rich_text(p_b, cell_text.strip(), size=11, color=WHITE, default_bold=True)
            else:
                tf = s.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
                tf.margin_left = tf.margin_right = Inches(0.10)
                tf.word_wrap = True
                
                # Hỗ trợ ngắt dòng và markdown bullets inside cell
                lines = cell_text.split('\n')
                for l_idx, line in enumerate(lines):
                    p = tf.add_paragraph() if l_idx > 0 else tf.paragraphs[0]
                    p.alignment = PP_ALIGN.LEFT; p.line_spacing = 1.15
                    
                    if line.strip().startswith('* '):
                        r_bullet = p.add_run(); r_bullet.text = "▪ "
                        r_bullet.font.name = FONT; r_bullet.font.size = Pt(pt_size)
                        r_bullet.font.bold = True; r_bullet.font.color.rgb = ORANGE
                        add_rich_text(p, line.strip()[2:], size=pt_size, color=text_color, default_bold=is_header)
                    else:
                        add_rich_text(p, line, size=pt_size, color=text_color, default_bold=is_header)
                        
            cx += Inches(w)
        cy += Inches(row_heights[r_idx])
```

---

## PHẦN BỔ SUNG: Các Visual Pattern trích xuất trực tiếp từ Slide mẫu thực tế

> **Nguồn gốc:** Phân tích XML cấu trúc từ 6 file PPTX mẫu thực tế (FINAL LEAP PROPOSAL, Hà Hằng Đức WMS, Senko WMS, Thaco Agri, Phúc Khải STM, VOPAK WMS) tổng cộng **602 slides**, **7485 rect shapes**, **1141 roundRect shapes**, **410 ellipse shapes**, **95 chevron shapes**, **838 group shapes**, **1605 hình ảnh** và **256 shadow effects**.

---

## Mẫu J: Chevron Process Bar (Thanh quy trình mũi tên xếp tầng)

**Đặc trưng visual thực tế:** Các slide mẫu sử dụng một hàng chevron (homePlate + chevron shapes) nối tiếp nhau ở phần trên, mỗi chevron đại diện cho một bước trong quy trình nghiệp vụ. Bước đang active được tô màu đậm (PRIMARY/dk1), các bước khác nhạt hơn (accent2). Thường gặp ở các slide "To-Be High Level Flow", "Order Structure & Status Flow".

```python
def make_chevron_process_bar(slide, steps, active_index, y=Inches(1.20)):
    """Vẽ thanh Chevron Process Bar xếp tầng nằm ngang.
    
    Args:
        steps: list of str - Tên các bước ("Order", "Dispatch", "Mobile App", ...)
        active_index: int - Index (0-based) của bước đang active (tô đậm)
        y: starting Y position
    """
    n = len(steps)
    bar_h = Inches(0.71)
    # Bước đầu tiên dùng homePlate (có đầu nhọn bên phải), các bước sau dùng chevron
    total_w = CONTENT_W
    step_w = total_w / n
    
    for i, step_text in enumerate(steps):
        x = MARGIN_L + i * step_w
        shape_type = MSO_SHAPE.HOME_PLATE if i == 0 else MSO_SHAPE.CHEVRON
        
        # Active step = PRIMARY/dk1, inactive = PALE_BLUE hoặc accent2
        is_active = (i == active_index)
        fill_color = PRIMARY if is_active else PALE_BLUE
        text_color = WHITE if is_active else PRIMARY
        
        s = make_shape(slide, shape_type, x, y, step_w, bar_h, fill=fill_color, line=None)
        tf = s.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_right = Inches(0.08)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = step_text
        r.font.name = FONT; r.font.size = Pt(16)
        r.font.bold = True; r.font.color.rgb = text_color
```

---

## Mẫu K: Problem-Solution-Value Table (Bảng Vấn đề-Giải pháp-Giá trị)

**Đặc trưng visual thực tế:** Slide mẫu "CÁC VẤN ĐỀ KHÓ KHĂN VÀ GIẢI PHÁP ĐỀ XUẤT" (Hà Hằng Đức WMS, slide 12 — 66 shapes) dùng cấu trúc 4 cột: Label hàng bên trái (nền đen, chữ trắng), cột Vấn đề (tag đỏ #DC2626), cột Giải pháp (tag xanh #3543F6), cột Giá trị (tag xanh lá #16A34A). Mỗi hàng có đường kẻ ngang #3543F6 phân tách. Cột Label bên trái kèm icon hình ảnh nhỏ.

```python
def make_problem_solution_slide(prs, eyebrow, title, rows_data, page_tagline, page_num):
    """Slide bảng Vấn đề - Giải pháp - Giá trị theo cột màu.
    
    rows_data: list of dicts, each: {
        'label': str,           # e.g. "HÀNG HÓA / LOT BATCH"
        'problem': str,         # Nội dung vấn đề
        'solution': str,        # Nội dung giải pháp
        'value': list[str],     # Danh sách giá trị mang lại
    }
    """
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Title bar (full width, PRIMARY background)
    make_shape(slide, MSO_SHAPE.RECTANGLE, MARGIN_L, Inches(0.37), 
               Inches(14.89), Inches(0.83), fill=ACCENT)
    tx_title = slide.shapes.add_textbox(MARGIN_L + Inches(0.15), Inches(0.37), 
                                         Inches(14), Inches(0.83))
    tf_t = tx_title.text_frame; tf_t.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_t = tf_t.paragraphs[0]
    add_rich_text(p_t, title.upper(), size=34, color=WHITE, default_bold=True)
    
    # Column headers - divider line
    header_y = Inches(1.91)
    make_shape(slide, MSO_SHAPE.RECTANGLE, MARGIN_L, header_y, CONTENT_W, Inches(0.03), fill=ACCENT)
    
    # Column header labels
    col_headers = ["Loại", "Khó khăn hiện tại", "Giải pháp đề xuất", "Giá trị mang lại"]
    col_xs = [MARGIN_L + Inches(0.3), MARGIN_L + Inches(3.8), MARGIN_L + Inches(9.5), MARGIN_L + Inches(15.0)]
    col_ws = [Inches(2.74), Inches(4.80), Inches(5.25), Inches(4.03)]
    
    TAG_RED = RGBColor(0xDC, 0x26, 0x26)
    TAG_GREEN = RGBColor(0x16, 0xA3, 0x4A)
    VALUE_GREEN = RGBColor(0x15, 0x80, 0x3D)
    
    for i, header in enumerate(col_headers):
        tx = slide.shapes.add_textbox(col_xs[i], Inches(2.12), col_ws[i], Inches(0.58))
        tf = tx.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        r = p.add_run(); r.text = header
        r.font.name = FONT; r.font.size = Pt(25); r.font.bold = True; r.font.color.rgb = ACCENT
    
    # Data rows
    row_y = Inches(3.12)
    row_h = Inches(1.57)
    gap = Inches(0.20)
    
    for idx, row in enumerate(rows_data[:4]):  # Max 4 rows
        cy = row_y + idx * (row_h + gap)
        
        # Divider line between rows
        if idx > 0:
            make_shape(slide, MSO_SHAPE.RECTANGLE, MARGIN_L, cy - Inches(0.10), 
                       CONTENT_W, Inches(0.03), fill=ACCENT)
        
        # Col 1: Category Label (dark bg, white text)
        make_shape(slide, MSO_SHAPE.RECTANGLE, col_xs[0], cy, col_ws[0], row_h, 
                   fill=RGBColor(0, 0, 0))
        tx_label = slide.shapes.add_textbox(col_xs[0] + Inches(0.08), cy, 
                                             col_ws[0] - Inches(0.16), row_h)
        tf_l = tx_label.text_frame; tf_l.word_wrap = True; tf_l.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_l = tf_l.paragraphs[0]
        r_l = p_l.add_run(); r_l.text = row['label'].upper()
        r_l.font.name = FONT; r_l.font.size = Pt(20); r_l.font.bold = True; r_l.font.color.rgb = WHITE
        
        # Col 2: Problem (white bg with red "Vấn đề" tag)
        make_shape(slide, MSO_SHAPE.RECTANGLE, col_xs[1], cy, col_ws[1], row_h, fill=WHITE)
        # Red tag
        tx_tag = slide.shapes.add_textbox(col_xs[1] + Inches(0.12), cy + Inches(0.08), 
                                           Inches(1.5), Inches(0.26))
        tf_tag = tx_tag.text_frame
        p_tag = tf_tag.paragraphs[0]
        r_tag = p_tag.add_run(); r_tag.text = "Vấn đề"
        r_tag.font.name = FONT; r_tag.font.size = Pt(18); r_tag.font.bold = True
        r_tag.font.color.rgb = TAG_RED
        # Problem text
        tx_prob = slide.shapes.add_textbox(col_xs[1] + Inches(0.12), cy + Inches(0.40), 
                                            col_ws[1] - Inches(0.24), row_h - Inches(0.48))
        tf_prob = tx_prob.text_frame; tf_prob.word_wrap = True
        p_prob = tf_prob.paragraphs[0]
        add_rich_text(p_prob, row['problem'], size=18, color=TEXT)
        
        # Col 3: Solution (white bg with blue "Giải pháp" tag)
        make_shape(slide, MSO_SHAPE.RECTANGLE, col_xs[2], cy, col_ws[2], row_h, fill=WHITE)
        tx_stag = slide.shapes.add_textbox(col_xs[2] + Inches(0.12), cy + Inches(0.08), 
                                            Inches(2.0), Inches(0.26))
        tf_stag = tx_stag.text_frame
        p_stag = tf_stag.paragraphs[0]
        r_stag = p_stag.add_run(); r_stag.text = "Giải pháp"
        r_stag.font.name = FONT; r_stag.font.size = Pt(18); r_stag.font.bold = True
        r_stag.font.color.rgb = ACCENT
        tx_sol = slide.shapes.add_textbox(col_xs[2] + Inches(0.12), cy + Inches(0.40), 
                                           col_ws[2] - Inches(0.24), row_h - Inches(0.48))
        tf_sol = tx_sol.text_frame; tf_sol.word_wrap = True
        p_sol = tf_sol.paragraphs[0]
        add_rich_text(p_sol, row['solution'], size=18, color=TEXT)
        
        # Col 4: Value (green tags)
        make_shape(slide, MSO_SHAPE.RECTANGLE, col_xs[3], cy, col_ws[3], row_h, fill=WHITE)
        tx_vtag = slide.shapes.add_textbox(col_xs[3] + Inches(0.12), cy + Inches(0.08), 
                                            Inches(2.0), Inches(0.26))
        tf_vtag = tx_vtag.text_frame
        p_vtag = tf_vtag.paragraphs[0]
        r_vtag = p_vtag.add_run(); r_vtag.text = "Giá trị"
        r_vtag.font.name = FONT; r_vtag.font.size = Pt(18); r_vtag.font.bold = True
        r_vtag.font.color.rgb = TAG_GREEN
        tx_val = slide.shapes.add_textbox(col_xs[3] + Inches(0.12), cy + Inches(0.40), 
                                           col_ws[3] - Inches(0.24), row_h - Inches(0.48))
        tf_val = tx_val.text_frame; tf_val.word_wrap = True
        for vi, v_text in enumerate(row.get('value', [])):
            p_v = tf_val.add_paragraph() if vi > 0 else tf_val.paragraphs[0]
            add_rich_text(p_v, v_text, size=18, color=VALUE_GREEN)
    
    add_footer(slide, page_num, page_tagline)
```

---

## Mẫu L: Process Flow with Triangle Arrows (Quy trình hộp nối mũi tên tam giác)

**Đặc trưng visual thực tế:** Slide mẫu "QUY TRÌNH NHẬP HÀNG" (Hà Hằng Đức WMS, slides 14-16 — 20+ shapes mỗi slide) dùng các roundRect (fill=ACCENT #3543F6, text WHITE) cho từng bước, nối với nhau bằng hình tam giác nhỏ (#E94949 đỏ, kích thước 0.47x0.35 inch) thay vì mũi tên. Phía dưới mỗi bước có hộp chi tiết (accent1, text lt1). Dòng cuối cùng có thanh ghi chú LIGHT_BLUE (#7594FF) trải rộng toàn bộ.

```python
def make_triangle_flow_slide(prs, eyebrow, title, steps_data, note_text, page_tagline, page_num):
    """Slide quy trình nối bằng tam giác đỏ giữa các hộp tròn.
    
    steps_data: list of dicts: {
        'title': str,       # Tên bước (e.g. "Nhận hàng")
        'details': list[str] # Chi tiết (e.g. ["Scan PALLET ID", "Ghi nhận Batch"])
    }
    note_text: str - Ghi chú cuối slide (thanh LIGHT_BLUE)
    """
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide_header(slide, eyebrow, title)
    
    n = len(steps_data)
    step_w = Inches(2.59)
    step_h = Inches(1.47)
    tri_w = Inches(0.47)
    tri_h = Inches(0.35)
    gap = Inches(0.30)
    
    # Calculate total width and starting X
    total_needed = n * step_w + (n - 1) * (tri_w + gap * 2)
    start_x = MARGIN_L + (CONTENT_W - total_needed) / 2
    
    step_y = Inches(2.20)  # Main step row Y
    detail_y = Inches(4.20)  # Detail boxes Y
    
    for i, step in enumerate(steps_data):
        cx = start_x + i * (step_w + tri_w + gap * 2)
        
        # Main step box (roundRect, ACCENT fill)
        s = make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, cx, step_y, step_w, step_h, 
                       fill=ACCENT, radius=0.10)
        tf = s.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_right = Inches(0.10)
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = step['title']
        r.font.name = FONT; r.font.size = Pt(18); r.font.bold = True; r.font.color.rgb = WHITE
        
        # Triangle arrow between steps (red #E94949)
        if i < n - 1:
            tri_x = cx + step_w + gap
            tri_y_pos = step_y + (step_h - tri_h) / 2
            tri = make_shape(slide, MSO_SHAPE.RIGHT_TRIANGLE, tri_x, tri_y_pos, tri_w, tri_h, 
                            fill=RGBColor(0xE9, 0x49, 0x49))
        
        # Detail box below (accent1 fill, showing sub-steps)
        if step.get('details'):
            detail_h = Inches(1.24)
            d = make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, cx - Inches(0.20), detail_y, 
                          step_w + Inches(0.40), detail_h, fill=PRIMARY, radius=0.08)
            tf_d = d.text_frame; tf_d.word_wrap = True
            tf_d.margin_left = tf_d.margin_right = Inches(0.10)
            tf_d.margin_top = Inches(0.08)
            for di, detail in enumerate(step['details']):
                p_d = tf_d.add_paragraph() if di > 0 else tf_d.paragraphs[0]
                p_d.line_spacing = 1.15
                add_rich_text(p_d, detail, size=18, color=WHITE, default_bold=True)
    
    # Bottom note bar (LIGHT_BLUE #7594FF full width)
    if note_text:
        note_y = Inches(6.00)
        note_bar = make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, MARGIN_L, note_y, 
                              CONTENT_W, Inches(1.00), fill=LIGHT_BLUE, radius=0.08)
        tf_note = note_bar.text_frame; tf_note.word_wrap = True
        tf_note.margin_left = tf_note.margin_right = Inches(0.15)
        tf_note.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_note = tf_note.paragraphs[0]
        add_rich_text(p_note, note_text, size=18, color=WHITE, default_bold=True)
    
    add_footer(slide, page_num, page_tagline)
```

---

## Mẫu M: Module Architecture Diagram (Sơ đồ kiến trúc module hệ thống)

**Đặc trưng visual thực tế:** Slide mẫu "PROPOSED MODULE FOR TRANSPORTATION MANAGEMENT" (LEAP, slide 14 — 27 shapes) và "LEAP'S SUPPLY CHAIN" (slide 13 — 69 shapes) dùng cấu trúc grid lớn gồm nhiều rect blocks xếp cạnh nhau theo ma trận, mỗi block là một module (fill=dk1/PRIMARY, text WHITE). Đặc biệt sử dụng **numbered ellipse badges** (fill=accent1, text lt1, size 21-27pt bold) đánh số thứ tự module. Phía dưới có thanh phân loại nhỏ (e.g. "Core modules" vs "Advanced modules"). Các thanh ngang màu #7594FF liệt kê tính năng con bên trong khu vực module lớn.

```python
def make_module_architecture_slide(prs, eyebrow, title, modules_data, features_data, page_tagline, page_num):
    """Slide sơ đồ kiến trúc hệ thống module.
    
    modules_data: list of dicts: {
        'num': str,           # Số thứ tự ("1", "2a", "2b", ...)
        'name': str,          # Tên module ("Order", "Dispatch", ...)
        'x': float,           # Tọa độ X (inches)
        'y': float,           # Tọa độ Y (inches)
        'w': float,           # Width (inches)
        'h': float,           # Height (inches)
    }
    features_data: list of dicts: {
        'text': str,          # Tên tính năng
        'x': float, 'y': float, 'w': float,  # Vị trí
    }
    """
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide_header(slide, eyebrow, title)
    
    # Container background (accent2/PALE_BLUE)
    make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, MARGIN_L + Inches(1.0), Inches(1.82), 
               Inches(17.83), Inches(6.10), fill=PALE_BLUE, radius=0.06)
    
    for mod in modules_data:
        mx = Inches(mod['x'])
        my = Inches(mod['y'])
        mw = Inches(mod['w'])
        mh = Inches(mod['h'])
        
        # Module block (PRIMARY/dk1 fill, WHITE text)
        s = make_shape(slide, MSO_SHAPE.RECTANGLE, mx, my, mw, mh, fill=PRIMARY)
        tf = s.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_right = Inches(0.08)
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = mod['name']
        r.font.name = FONT; r.font.size = Pt(19); r.font.color.rgb = WHITE
        
        # Numbered ellipse badge (accent1, positioned above-left of module)
        badge_size = Inches(0.53)
        bx = mx + (mw - badge_size) / 2
        by = my - badge_size - Inches(0.05)
        badge = make_shape(slide, MSO_SHAPE.OVAL, bx, by, badge_size, badge_size, 
                          fill=ACCENT, line=None)
        tf_b = badge.text_frame; tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_b = tf_b.paragraphs[0]; p_b.alignment = PP_ALIGN.CENTER
        r_b = p_b.add_run(); r_b.text = mod['num']
        r_b.font.name = FONT; r_b.font.size = Pt(21)
        r_b.font.bold = True; r_b.font.color.rgb = WHITE
    
    # Feature bars (#7594FF, horizontal bars inside container)
    for feat in features_data:
        fx = Inches(feat['x'])
        fy = Inches(feat['y'])
        fw = Inches(feat['w'])
        fh = Inches(0.38)
        
        fs = make_shape(slide, MSO_SHAPE.RECTANGLE, fx, fy, fw, fh, fill=LIGHT_BLUE)
        tf_f = fs.text_frame; tf_f.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf_f.margin_left = Inches(0.10)
        p_f = tf_f.paragraphs[0]
        r_f = p_f.add_run(); r_f.text = feat['text']
        r_f.font.name = FONT; r_f.font.size = Pt(16)
        r_f.font.color.rgb = WHITE
    
    add_footer(slide, page_num, page_tagline)
```

---

## Mẫu N: Screenshot + Callout Panel (Slide ảnh chụp màn hình kèm khung mô tả)

**Đặc trưng visual thực tế:** Rất nhiều slide trong các file mẫu (đặc biệt VOPAK WMS — 154 slides) dùng layout: ảnh chụp màn hình lớn chiếm 60-70% diện tích slide, kèm một hoặc nhiều callout boxes nhỏ bo tròn ở bên cạnh hoặc bên dưới (fill=dk1/accent4, text=WHITE/accent4, size 22pt). Callout box thường chứa nhãn đỏ (#E94949) và mô tả ngắn.

```python
def make_screenshot_callout_slide(prs, eyebrow, title, screenshot_path, callouts, page_tagline, page_num):
    """Slide ảnh chụp màn hình kèm các callout boxes.
    
    screenshot_path: str - Đường dẫn tuyệt đối tới ảnh chụp
    callouts: list of dicts: {
        'label': str,         # Nhãn callout (e.g. "Báo cáo tồn theo thời gian thực")
        'description': str,   # Mô tả chi tiết
        'position': str,      # "left", "right", "bottom"
    }
    """
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide_header(slide, eyebrow, title)
    
    # Screenshot image area
    img_x = MARGIN_L + Inches(3.0)
    img_y = Inches(1.60)
    img_w = Inches(9.50)
    img_h = Inches(5.40)
    
    if screenshot_path:
        slide.shapes.add_picture(screenshot_path, img_x, img_y, img_w, img_h)
    
    # Callout boxes (positioned based on 'position')
    for ci, callout in enumerate(callouts):
        pos = callout.get('position', 'left')
        
        if pos == 'left':
            cx = MARGIN_L
            cy = Inches(2.00) + ci * Inches(1.50)
            cw = Inches(2.88)
            ch = Inches(1.20)
        elif pos == 'right':
            cx = SLIDE_W - MARGIN_R - Inches(2.88)
            cy = Inches(2.00) + ci * Inches(1.50)
            cw = Inches(2.88)
            ch = Inches(1.20)
        else:  # bottom
            cx = MARGIN_L
            cy = Inches(7.00) - Inches(1.20)
            cw = CONTENT_W
            ch = Inches(0.80)
        
        # Callout background (red accent for label)
        add_shadow(slide, cx, cy, cw, ch, radius=0.08)
        c_shape = make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, cw, ch, 
                            fill=RGBColor(0xE9, 0x49, 0x49), radius=0.08)
        tf_c = c_shape.text_frame; tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = Inches(0.12)
        tf_c.margin_top = Inches(0.08)
        
        p_label = tf_c.paragraphs[0]
        r_label = p_label.add_run(); r_label.text = callout['label']
        r_label.font.name = FONT; r_label.font.size = Pt(22)
        r_label.font.bold = True; r_label.font.color.rgb = WHITE
        
        if callout.get('description'):
            p_desc = tf_c.add_paragraph()
            add_rich_text(p_desc, callout['description'], size=16, color=WHITE)
    
    add_footer(slide, page_num, page_tagline)
```

---

## Mẫu O: Thank You / Closing Slide (Slide kết thúc)

**Đặc trưng visual thực tế:** Các slide kết thúc của file mẫu dùng layout đơn giản: nền đậm toàn slide với title lớn ở giữa, kèm thông tin liên hệ và logo. Tương tự Section Divider nhưng thêm subtitle liên hệ.

```python
def make_thank_you_slide(prs, title_text, subtitle_text, contact_text, page_tagline, page_num):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Full dark background
    make_shape(slide, MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H, fill=PRIMARY)
    
    # Main title (52pt WHITE, center)
    tx_title = slide.shapes.add_textbox(MARGIN_L, Inches(2.50), CONTENT_W, Inches(1.50))
    tf_t = tx_title.text_frame; tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = Inches(0)
    p_t = tf_t.paragraphs[0]; p_t.alignment = PP_ALIGN.CENTER
    r_t = p_t.add_run(); r_t.text = title_text.upper()
    r_t.font.name = FONT; r_t.font.size = Pt(52); r_t.font.bold = True; r_t.font.color.rgb = WHITE
    
    # Subtitle
    tx_sub = slide.shapes.add_textbox(MARGIN_L, Inches(4.20), CONTENT_W, Inches(0.80))
    tf_s = tx_sub.text_frame; tf_s.word_wrap = True
    p_s = tf_s.paragraphs[0]; p_s.alignment = PP_ALIGN.CENTER
    add_rich_text(p_s, subtitle_text, size=20, color=PALE_BLUE)
    
    # Contact info
    if contact_text:
        tx_contact = slide.shapes.add_textbox(MARGIN_L, Inches(5.30), CONTENT_W, Inches(1.00))
        tf_c = tx_contact.text_frame; tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]; p_c.alignment = PP_ALIGN.CENTER
        add_rich_text(p_c, contact_text, size=14, color=PALE_BLUE)
    
    # Staggered Accent Bars (same as Section Divider variant)
    deco_colors = [ACCENT, LIGHT_BLUE, PALE_BLUE, ORANGE]
    deco_widths = [Inches(3.2), Inches(2.8), Inches(2.4), Inches(2.0)]
    right_edge = SLIDE_W - Inches(0.6)
    for i, color in enumerate(deco_colors):
        w = deco_widths[i]; x = right_edge - w
        make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(3.0 + i*0.7), 
                   w, Inches(0.55), fill=color, line=None, radius=0.10)
    
    # Footer (PALE_BLUE text on dark bg)
    add_footer(slide, page_num, page_tagline)
    for shape in slide.shapes:
        if shape.has_text_frame and ("Page" in shape.text_frame.text or page_tagline in shape.text_frame.text):
            for p in shape.text_frame.paragraphs:
                for run in p.runs:
                    run.font.color.rgb = PALE_BLUE
```

---

## Mẫu P: Kanban Board (Bảng Kanban quản trị trạng thái)

**Đặc trưng visual thực tế:** Phân chia slide thành 3 hoặc 4 cột dọc dạng bảng Kanban (như phân chia module chức năng hoặc luồng công việc). Mỗi cột có một thanh tiêu đề màu nổi bật (PRIMARY, ACCENT, hoặc ORANGE), bên dưới là các thẻ công việc (white background, Neumorphic shadow) xếp chồng đứng theo chiều dọc. Phù hợp cho slide phân chia trách nhiệm phần mềm, phân nhóm chức năng "To-Be scope", hoặc Kanban quản lý dự án.

```python
def make_kanban_board_slide(prs, eyebrow, title, lede_text, columns_data, page_tagline, page_num):
    """Slide dạng bảng Kanban gồm nhiều cột dọc, mỗi cột chứa danh sách các thẻ công việc (cards).
    
    columns_data: list of dicts: {
        'title': str,          # Tên cột (e.g., "STM", "SWM", "INTEGRATION")
        'color': RGBColor,     # Màu header cột (e.g. PRIMARY, ACCENT, ORANGE)
        'tasks': list of dicts: [
            {'title': str, 'desc': str, 'badge': str}, # badge là nhãn phụ e.g., "Core", "Optional"
            ...
        ]
    }
    """
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    slide_header(slide, eyebrow, title)
    
    # Lede
    tx_lede = slide.shapes.add_textbox(MARGIN_L, LEDE_Y, CONTENT_W, LEDE_H)
    tf_l = tx_lede.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_top = Inches(0)
    p_l = tf_l.paragraphs[0]; p_l.font.italic = True
    add_rich_text(p_l, lede_text, size=13, color=TEXT, italic=True)
    
    n_cols = len(columns_data)
    gap = Inches(0.20)
    col_w = (CONTENT_W - (n_cols - 1) * gap) / n_cols
    start_y = Inches(2.20)
    col_h = Inches(4.20)
    
    for i, col in enumerate(columns_data[:4]): # Tối đa 4 cột để đảm bảo khoảng cách hiển thị
        cx = MARGIN_L + i * (col_w + gap)
        
        # 1. Vẽ Container nền cho cả cột (PALE_BLUE nhạt)
        make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, cx, start_y, col_w, col_h, fill=PALE_BLUE, line=None, radius=0.04)
        
        # 2. Tiêu đề cột (Màu chỉ định, chữ trắng in đậm)
        header_h = Inches(0.45)
        col_color = col.get('color', PRIMARY)
        make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, cx, start_y, col_w, header_h, fill=col_color, line=None, radius=0.04)
        make_shape(slide, MSO_SHAPE.RECTANGLE, cx, start_y + Inches(0.25), col_w, Inches(0.20), fill=col_color) # làm phẳng cạnh dưới header
        
        tx_h = slide.shapes.add_textbox(cx, start_y, col_w, header_h)
        tf_h = tx_h.text_frame; tf_h.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_h = tf_h.paragraphs[0]; p_h.alignment = PP_ALIGN.CENTER
        r_h = p_h.add_run(); r_h.text = col['title'].upper()
        r_h.font.name = FONT; r_h.font.size = Pt(11); r_h.font.bold = True; r_h.font.color.rgb = WHITE
        
        # 3. Vẽ các Task Card xếp chồng đứng
        card_start_y = start_y + header_h + Inches(0.15)
        card_h = Inches(1.05)
        card_gap = Inches(0.12)
        
        for ti, task in enumerate(col.get('tasks', [])[:3]): # Tối đa 3 card mỗi cột để tránh tràn viền dưới (Y-Budget)
            cy = card_start_y + ti * (card_h + card_gap)
            
            # Bóng đổ Neumorphic lót dưới card trắng
            add_shadow(slide, cx + Inches(0.08), cy, col_w - Inches(0.16), card_h, radius=0.04, offset=0.04)
            # Card trắng chứa thông tin công việc
            make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, cx + Inches(0.08), cy, col_w - Inches(0.16), card_h, fill=WHITE, line=DIVIDER, line_w=1.0, radius=0.04)
            
            # Hộp chữ nhiệm vụ
            tx_card = slide.shapes.add_textbox(cx + Inches(0.15), cy + Inches(0.06), col_w - Inches(0.30), card_h - Inches(0.12))
            tf_card = tx_card.text_frame; tf_card.word_wrap = True
            tf_card.margin_left = tf_card.margin_right = tf_card.margin_top = tf_card.margin_bottom = Inches(0)
            
            # Tiêu đề nhiệm vụ (Chữ xám đậm, bôi đậm từ khóa)
            p_title = tf_card.paragraphs[0]
            add_rich_text(p_title, task['title'], size=11, color=TEXT, default_bold=True)
            
            # Mô tả chi tiết (Chữ nhỏ hơn)
            if task.get('desc'):
                p_desc = tf_card.add_paragraph()
                p_desc.space_before = Pt(3)
                add_rich_text(p_desc, task['desc'], size=9.5, color=TEXT)
                
            # Badge phân loại góc dưới bên phải card
            if task.get('badge'):
                badge_w = Inches(0.80)
                badge_h = Inches(0.24)
                bx = cx + col_w - badge_w - Inches(0.15)
                by = cy + card_h - badge_h - Inches(0.08)
                badge = make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, badge_w, badge_h, fill=ORANGE, line=None, radius=0.25)
                tf_b = badge.text_frame; tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
                tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = Inches(0)
                p_b = tf_b.paragraphs[0]; p_b.alignment = PP_ALIGN.CENTER
                r_b = p_b.add_run(); r_b.text = task['badge']
                r_b.font.name = FONT; r_b.font.size = Pt(8.5); r_b.font.bold = True; r_b.font.color.rgb = WHITE
                
    add_footer(slide, page_num, page_tagline)
```

---

## Mẫu Q: Alternating Milestone Timeline (Trình tự thời gian xen kẽ)

**Đặc trưng visual thực tế:** Khi mô tả một lộ trình triển khai (Roadmap) hoặc các trạng thái chuyển dịch của hệ thống, một sơ đồ Timeline nằm ngang là tối ưu nhất. Để **tránh chồng lấn chữ** và tối đa hóa mật độ thông tin, mẫu này sử dụng đường trục chính nằm ngang ở giữa slide, với các hộp thông tin được xếp **xen kẽ TRÊN và DƯỚI** trục chính, kết nối với trục bằng các đường line chỉ hướng mảnh. 

```python
def make_alternating_timeline_slide(prs, eyebrow, title, lede_text, milestones, page_tagline, page_num):
    """Slide tiến trình lộ trình / timeline với các thẻ thông tin xếp xen kẽ trên dưới trục ngang.
    
    milestones: list of dicts: {
        'date': str,         # Mốc thời gian / Tên mốc (e.g. "Q1/2026", "Tháng 05")
        'title': str,        # Tiêu đề cột mốc (e.g. "Kick-off", "Go-Live")
        'bullets': list[str] # Các đầu mục công việc cụ thể tại mốc này
    }
    """
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    slide_header(slide, eyebrow, title)
    
    # Lede
    tx_lede = slide.shapes.add_textbox(MARGIN_L, LEDE_Y, CONTENT_W, LEDE_H)
    tf_l = tx_lede.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_top = Inches(0)
    p_l = tf_l.paragraphs[0]; p_l.font.italic = True
    add_rich_text(p_l, lede_text, size=13, color=TEXT, italic=True)
    
    # 1. Trục chính Timeline nằm ngang ở giữa slide (Y = 3.90)
    axis_y = Inches(3.90)
    hline(slide, MARGIN_L + Inches(0.50), axis_y, SLIDE_W - MARGIN_R - Inches(0.50), color=PRIMARY, width=4)
    
    n_steps = len(milestones)
    timeline_w = CONTENT_W - Inches(1.00)
    step_w = timeline_w / n_steps
    
    for i, ms in enumerate(milestones[:5]): # Giới hạn tối đa 5 bước để đảm bảo chiều ngang thông thoáng
        # Tọa độ X tâm của nút tiến trình
        cx = MARGIN_L + Inches(0.50) + i * step_w + step_w / 2
        
        # 2. Vẽ nút tròn (Node) trên trục chính
        dot_r = Inches(0.24)
        make_shape(slide, MSO_SHAPE.OVAL, cx - dot_r/2, axis_y - dot_r/2, dot_r, dot_r, fill=ORANGE, line=None)
        inner_r = Inches(0.12)
        make_shape(slide, MSO_SHAPE.OVAL, cx - inner_r/2, axis_y - inner_r/2, inner_r, inner_r, fill=WHITE, line=None)
        
        # 3. Tính toán vị trí xen kẽ (Chẵn: TRÊN trục, Lẻ: DƯỚI trục)
        card_w = step_w - Inches(0.30)
        card_h = Inches(1.80)
        card_x = cx - card_w / 2
        
        if i % 2 == 0:
            # Ở TRÊN trục chính
            card_y = axis_y - card_h - Inches(0.40)
            # Đường chỉ hướng đi xuống nút tròn
            hline(slide, cx, card_y + card_h, cx, color=DIVIDER, width=1.5)
            # Dịch chuyển vị trí vẽ đường kẻ chỉ hướng (dùng hline dạng dọc)
            make_shape(slide, MSO_SHAPE.RECTANGLE, cx - Inches(0.005), card_y + card_h, Inches(0.01), Inches(0.40), fill=DIVIDER, line=None)
        else:
            # Ở DƯỚI trục chính
            card_y = axis_y + Inches(0.40)
            # Đường chỉ hướng đi lên nút tròn
            make_shape(slide, MSO_SHAPE.RECTANGLE, cx - Inches(0.005), axis_y + Inches(0.12), Inches(0.01), Inches(0.28), fill=DIVIDER, line=None)
            
        # 4. Vẽ card thông tin mốc tiến độ (Nền PALE_BLUE nhạt, header PRIMARY đậm)
        add_shadow(slide, card_x, card_y, card_w, card_h, radius=0.06, offset=0.04)
        make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, card_x, card_y, card_w, card_h, fill=PALE_BLUE, line=None, radius=0.06)
        
        # Header của Card chứa Mốc thời gian
        make_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, card_x, card_y, card_w, Inches(0.42), fill=PRIMARY, radius=0.06)
        make_shape(slide, MSO_SHAPE.RECTANGLE, card_x, card_y + Inches(0.20), card_w, Inches(0.22), fill=PRIMARY) # làm phẳng
        
        tx_h = slide.shapes.add_textbox(card_x, card_y, card_w, Inches(0.42))
        tf_h = tx_h.text_frame; tf_h.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_h = tf_h.paragraphs[0]; p_h.alignment = PP_ALIGN.CENTER
        r_h = p_h.add_run(); r_h.text = ms['date'].upper()
        r_h.font.name = FONT; r_h.font.size = Pt(11); r_h.font.bold = True; r_h.font.color.rgb = WHITE
        
        # Nội dung công việc (Tiêu đề in đậm + Bullet)
        tx_b = slide.shapes.add_textbox(card_x + Inches(0.08), card_y + Inches(0.48), card_w - Inches(0.16), card_h - Inches(0.55))
        tf_b = tx_b.text_frame; tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = Inches(0)
        
        # Tiêu đề mốc công việc (Ví dụ: "Kick-off dự án")
        p_title = tf_b.paragraphs[0]
        p_title.alignment = PP_ALIGN.CENTER
        add_rich_text(p_title, ms['title'], size=10.5, color=PRIMARY, default_bold=True)
        
        # Vẽ các bullet con mô tả nhiệm vụ
        for bullet in ms.get('bullets', [])[:3]: # Tối đa 3 đầu dòng
            add_bullet(tf_b, bullet, size=9.5)
            
    add_footer(slide, page_num, page_tagline)
```

---

## Tổng kết Thống kê Visual trích xuất từ 6 File Mẫu (602 slides)

| Đặc tính | Giá trị thực tế |
|-----------|-----------------|
| **Hình chữ nhật (rect)** | 7,485 lần sử dụng — thành phần visual chủ đạo |
| **Hình bo tròn (roundRect)** | 1,141 lần — dùng cho cards, step boxes, badges |
| **Hình tròn (ellipse)** | 410 lần — dùng cho numbered badges, icons |
| **Chevron** | 95 lần — thanh quy trình nối tiếp |
| **Mũi tên phải (rightArrow)** | 41 lần — flow connectors |
| **Tam giác (triangle)** | 38 lần — kết nối giữa các bước quy trình |
| **Nhóm hình (groups)** | 838 lần — ghép nối nhiều shape thành block |
| **Hình ảnh** | 1,605 lần — screenshots, logos, diagrams |
| **Bóng đổ (outerShdw)** | 256 lần — hiệu ứng nổi cho card |
| **Font chính: Be Vietnam Pro** | 2,701 lần (chiếm ưu thế tuyệt đối) |
| **Font phụ: Mulish** | 941 lần (dùng cho một số file cũ) |
| **Cỡ chữ phổ biến nhất** | 18pt (1,004 lần), 16pt (479), 22pt (470), 21pt (450) |
| **Màu fill phổ biến nhất** | `#FFFFFF` (782), `#2933D9` PRIMARY (617), `#E94949` Red (466), `#40444C` TEXT (460) |
| **Màu chữ phổ biến nhất** | `#FFFFFF` (710), `#40444C` TEXT (329), `#2933D9` PRIMARY (237) |

