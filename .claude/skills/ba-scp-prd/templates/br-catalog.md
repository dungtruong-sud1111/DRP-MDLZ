# BR Catalog — [Domain Name] [{PREFIX}-{NNN}]

> Catalog tổng hợp Business Rules cho domain `[domain dir]` (feature `[NNN]-{slug}`). Dùng khi domain có ≥ 30 BR, hoặc khi cần trace từ Master canonical xuống các PRD by-module.
>
> Mục đích: 1 nơi duy nhất để search BR theo ID, theo entity, theo lifecycle phase — không phải scroll PRD dài hàng nghìn dòng.

| Field | Value |
|-------|-------|
| Domain | [master-data \| demand \| ... ] |
| Canonical refs | [F01a, F01b, P01, ...] |
| PRDs covered | [PRD-MD-001-..., PRD-MD-002-...] |
| Total BR | [N] |
| Last sync với canonical | [YYYY-MM-DD] |

---

## Group A — [Group label, vd "Entity identity & uniqueness"]

| # | Rule | Description | Maps to PRD | Maps to canonical | AC |
|---|------|-------------|--------------|---------------------|-----|
| BR-MD-001 | [Rule name] | [Câu đầy đủ Subject + Action + Constraint + Why] | PRD-MD-001 §BR group X | F01a §BR-XX | AC-MD-001 |
| BR-MD-002 | ... | ... | ... | ... | ... |

## Group B — [Group label, vd "Data Quality gates"]

| # | Rule | Description | Maps to PRD | Maps to canonical | AC |
|---|------|-------------|--------------|---------------------|-----|
| BR-MD-101 | ... | ... | ... | ... | ... |

## Group C — [...]

---

## Cross-domain Dependencies

> BR phụ thuộc rule ở domain khác — flag rõ để khi update không miss impact.

| BR | Depends on | Type | Notes |
|----|-----------|------|-------|
| BR-MD-001 | BR-SK-005 (Shared Kernel — base columns) | inherits | Phải align audit fields |
| BR-DM-012 | BR-MD-050 (Master Data — Product status) | data scope | Chỉ Product status = Active mới được forecast |

---

## Cross-customer Notes

> BR có behavior khác giữa UNIS / TTC / MDLZ — link đến overlay.

| BR | All | UNIS | TTC | MDLZ |
|----|-----|------|-----|------|
| BR-DM-005 | Default 1-tier SS | ✓ Override → 2-tier (UNIS-Overlay §X) | — | — |

---

## Open Items

| BR | Status | Action needed | Owner |
|----|--------|----------------|-------|
| BR-XX-... | Draft | Needs canonical alignment with F0X §Y | PO |

---

## Version History

| Version | Ngày | Thay đổi | Lý do |
|---------|------|----------|-------|
| 1.0 | [YYYY-MM-DD] | Khởi tạo catalog | Breakdown từ canonical F0X |
