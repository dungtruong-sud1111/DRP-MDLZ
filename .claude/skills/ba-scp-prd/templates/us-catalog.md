# US Catalog — [Domain Name] [{PREFIX}-{NNN}]

> Catalog tổng hợp User Stories cho domain `[domain dir]` (feature `[NNN]-{slug}`). Dùng khi domain có ≥ 20 US.
>
> Mục đích: trace nhu cầu user theo persona × workflow phase, đảm bảo MECE coverage, hỗ trợ sprint planning.

| Field | Value |
|-------|-------|
| Domain | [master-data \| demand \| ... ] |
| Canonical refs | [F01a, F01b, ...] |
| PRDs covered | [PRD-MD-001-..., PRD-MD-002-...] |
| Total US | [N] |
| Personas | [list các persona xuất hiện] |

---

## Coverage Matrix — Persona × Workflow Phase

> Apply MECE: mỗi cell phải có ≥ 1 US, hoặc explicit "n/a" / "out of scope".

| | Phase 1 (vd Submission) | Phase 2 (Review) | Phase 3 (Approval) | Phase 4 (Execution) |
|---|-------------------------|------------------|---------------------|----------------------|
| Persona A (Planner) | US-01, US-02 | US-03 | n/a | US-04 |
| Persona B (Manager) | n/a | US-05 | US-06 | out of scope |
| Persona C (System) | US-07 | US-08 | — | US-09 |

---

## Group A — [Group label, vd "Planner — Daily allocation"]

| # | Story | Persona | Maps to PRD | AC | Notes |
|---|-------|---------|--------------|-----|-------|
| US-DM-001 | As a Planner, I want [need in user voice], So that [business outcome] | Planner | PRD-DM-002 §US-01 | AC-DM-001..003 | |
| US-DM-002 | ... | ... | ... | ... | ... |

## Group B — [Group label, vd "Manager — Plan review & approve"]

| # | Story | Persona | Maps to PRD | AC | Notes |
|---|-------|---------|--------------|-----|-------|
| US-DM-010 | ... | Manager | ... | ... | ... |

## Group C — [...]

---

## Cross-domain Dependencies

> US đòi hỏi capability từ domain khác — flag để sequencing dev đúng.

| US | Depends on | Type | Notes |
|----|-----------|------|-------|
| US-DM-005 | Master Data Entity Registry ready | blocking | Phải có Product/SKU PRD trước |

---

## Customer Variant Notes

> US có behavior/wording khác per customer — link overlay.

| US | All | UNIS | TTC | MDLZ |
|----|-----|------|-----|------|
| US-DM-008 | Standard 1-tier review | ✓ Override → 2-tier review (UNIS §X) | — | — |

---

## Open Items

| US | Status | Action needed | Owner |
|----|--------|----------------|-------|
| US-XX-... | Draft | Persona chưa confirm | PO |

---

## Version History

| Version | Ngày | Thay đổi | Lý do |
|---------|------|----------|-------|
| 1.0 | [YYYY-MM-DD] | Khởi tạo US catalog | Breakdown từ canonical |
