# [Feature Name] — Wireframes

| Field | Value |
|-------|-------|
| Source | [PRD-{PREFIX}-{NNN}-{title-slug}.md] |
| Domain | [domain dir] |
| Status | draft \| review \| locked |

---

## Container Pattern Decision

> Ghi quyết định container pattern cho TỪNG action (Create / Edit / View / Bulk). Áp dụng decision table trong `references/wireframe-guide.md` — Container Pattern Decision.

| Action | Pattern | Lý do |
|--------|---------|-------|
| Create | Dialog \| Drawer \| Detail View \| Wizard \| Full-page | [field count, time on screen, có cần URL không, list context cần thiết không] |
| Edit | Dialog \| Drawer \| Detail View | [same pattern as Create unless entity có sub-data] |
| View detail | Drawer \| Detail View | [có lifecycle/sub-data không] |

---

## WF-01: [Screen Name]

**Context**: [Ai thấy screen này, navigate từ đâu, precondition gì]

**Maps to**: US-XX, BR-XX

```
[ASCII wireframe ở đây]
```

**Annotations:**
- **A1**: [Giải thích UI element cụ thể — vd "Drawer 480px, slide từ phải, giữ list context"]
- **A2**: [Element khác]

---

## WF-02: [Screen Name]

**Context**: [...]

**Maps to**: US-XX

```
[ASCII wireframe]
```

**Annotations:**
- **A1**: [...]

---

## State Variations

### Khi [condition A — vd "User là role Vendor"]
[Wireframe thay đổi thế nào — element nào hide/show, button state khác nhau]

### Khi [condition B — vd "Plan status = Approved"]
[...]

### Empty states
[Khi list trả về 0 dòng — thứ tự ưu tiên empty state nếu có nhiều scenario]

---

## Interaction Notes

| # | Interaction | Behavior | Maps to |
|---|-------------|----------|---------|
| I-01 | [User action / trigger] | [Hệ thống phản ứng thế nào] | US-XX, AC-XX |
| I-02 | [...] | [...] | [...] |

---

## Responsive / Mobile Notes

> [Xóa nếu feature desktop-only. SCP thường desktop-heavy, nhưng có module mobile (vd Driver app handover)]

| Breakpoint | Layout adjustment |
|------------|-------------------|
| Desktop ≥1280px | [Pattern A] |
| Tablet 768–1279px | [Adjustment] |
| Mobile <768px | [Adjustment hoặc "not supported"] |

---

## Version History

| Version | Ngày | Thay đổi | Lý do |
|---------|------|----------|-------|
| 1.0 | [YYYY-MM-DD] | Khởi tạo wireframes | [Yêu cầu từ PM / Tách từ Master / Breakdown từ canonical] |
