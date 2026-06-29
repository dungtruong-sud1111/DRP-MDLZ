# CHUẨN FORMAT FILE BÁO CÁO RESEARCH

## TÊN FILE

Pattern: `_research/YYYY-MM-DD_[slug-chu-de].md`

Ví dụ:
- `_research/2026-06-16_wms-best-practice.md`
- `_research/2026-06-16_so-sanh-tms-solutions.md`

Quy tắc slug: chữ thường, dấu gạch ngang, không dấu tiếng Việt, tối đa 40 ký tự.

---

## HEADER BẮT BUỘC

```markdown
# [Tiêu đề báo cáo — rõ ràng, mô tả chủ đề]

**Ngày research:** DD/MM/YYYY  
**Model:** deep-research-preview-04-2026 | deep-research-max-preview-04-2026  
**Chế độ:** OPEN | FOCUSED  
**Thời gian xử lý:** ~X phút  

---
```

---

## CẤU TRÚC NỘI DUNG (Chế độ OPEN)

```markdown
## 1. Tổng quan
[Định nghĩa, bối cảnh, tầm quan trọng]

## 2. Phân tích chuyên sâu
[Các khía cạnh chính, xu hướng, số liệu]

## 3. So sánh các giải pháp / cách tiếp cận
[Bảng hoặc danh sách so sánh]

## 4. Kết luận & Khuyến nghị
[Tổng kết + hành động đề xuất cụ thể]

## Nguồn trích dẫn
- [Tên nguồn 1](URL) — Tổ chức, Năm
- [Tên nguồn 2](URL) — Tổ chức, Năm
```

---

## CẤU TRÚC NỘI DUNG (Chế độ FOCUSED)

```markdown
## 1. Tóm tắt từng nguồn
### [Tên nguồn 1]
[Tóm tắt 3–5 câu, luận điểm chính]

### [Tên nguồn 2]
...

## 2. Phân tích so sánh
[Điểm tương đồng, khác biệt, mâu thuẫn]

## 3. Tổng hợp & Kết luận
[Luận điểm thống nhất rút ra từ nhiều nguồn]

## Nguồn trích dẫn
- [Tên nguồn 1](URL)
- [Tên nguồn 2](URL)
```

---

## YÊU CẦU CITATIONS

- Mỗi luận điểm quan trọng PHẢI có nguồn dẫn kèm.
- Format: `[Tên tổ chức/tác giả, Năm](URL)`
- Tối thiểu 5 citations trong toàn báo cáo.
- KHÔNG dùng format `[1][2][3]` — dùng tên nguồn rõ ràng.

---

## TÓM TẮT (chỉ khi gọi từ pipeline BA)

Sau file báo cáo, in thêm khối tóm tắt ngắn vào conversation:

```
---
## TÓM TẮT RESEARCH — [Chủ đề]

- [Điểm chính 1]
- [Điểm chính 2]
- [Điểm chính 3]
- [Khuyến nghị chính]

**Nguồn chính:** [2–3 nguồn quan trọng nhất]  
**Báo cáo đầy đủ:** `_research/YYYY-MM-DD_[slug].md`
---
```
