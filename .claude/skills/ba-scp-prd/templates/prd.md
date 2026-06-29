# [Feature Name] — PRD

| Field | Value |
|-------|-------|
| Source | [đường dẫn file canonical / Master / user prompt — YYYY-MM-DD] |
| Domain | master-data \| demand \| supply-inventory \| drp-engine \| order-planning \| simulation \| daily-replan \| transport \| exception \| analytics \| shared-kernel \| integration \| admin |
| Canonical ref | [F0X-* hoặc P0X-* trong SCP-DRP-SPEC-SYSTEM-FINAL] |
| Status | draft \| review \| locked \| implemented |
| Priority | P0-Critical \| P1-High \| P2-Medium \| P3-Low |
| Customer scope | All \| UNIS \| TTC \| MDLZ \| [combo] |

---

## Overview

[Problem statement: pain point nào tồn tại? Feature này giải gì? Tại sao cần?]

**Module**: [domain dir]
**Complexity**: Simple \| Medium \| Complex
**Primary persona**: [persona name]

---

## Research Findings

> [Xóa section này nếu skip research]

### Competitor Benchmark

| Aspect | SAP IBP | Kinaxis | o9 | Smartlog SCP Decision |
|--------|---------|---------|----|-----------------------|
| ... | ... | ... | ... | ... |

### Key Insights
1. [Insight đã định hình approach]
2. [Insight khác]

---

## User Personas

### [Persona 1]
- **Role**: [mô tả ngắn]
- **Needs from this feature**: [họ cần gì]
- **Frequency**: [hàng ngày / hàng tuần / ad-hoc]

### [Persona 2]
- ...

---

## User Stories

> Group stories dưới sub-headings theo taxonomy phù hợp THIS feature (by persona, by workflow phase, by action, by screen, by domain concept). Apply MECE checklist (no overlap, no gap, same granularity, independently testable) trước khi finalize.
>
> **WRITING STYLE — US ≠ screen spec.**
> - `I want [goal]` = KẾT QUẢ user muốn (job-to-be-done), KHÔNG liệt kê field / entity / filter / status.
> - `So that [benefit]` = lợi ích nghề/business, KHÔNG lặp lại what.
> - Không tên entity kỹ thuật (`SOTOLifecycle` → "đơn hàng kế hoạch"; `DRPRun` → "phiên chạy phân phối").
> - Detail field / filter / layout → Wireframe / Data Model / AC.
> - Xem "Story-loose standard" trong `references/prd-format.md` section 3.

### Group A — [chosen label, vd "Planner — phân bổ hàng ngày"]

**US-01**: As a [persona], I want [goal in user's own words — describe NEED, not the screen], So that [business/job outcome].
**US-02**: As a [persona], I want [goal], So that [benefit].

### Group B — [chosen label, vd "Manager — review & approve plan"]

**US-03**: As a [persona], I want [goal], So that [benefit].

> Thêm/bớt group theo feature. Xóa hint block này trước khi publish.

---

## Business Rules

> Group rules dưới sub-headings theo taxonomy phù hợp THIS feature (by domain concept, by entity, by lifecycle phase, by rule kind, by scenario). Apply MECE checklist trước khi finalize.
>
> **Nếu BR có "system tự X sau Y" hoặc "định kỳ chạy"** → đọc `references/system-patterns.md` để chọn đúng fire-and-forget vs recurring, kèm companion rules (re-schedule / cancel / idempotency).

### Group A — [chosen label, vd "DRP run identity & lifecycle"]

| # | Rule | Description |
|---|------|-------------|
| BR-01 | [Rule name] | [Câu đầy đủ: Subject + Action/Condition + Constraint + Why] |
| BR-02 | [Rule name] | [Câu đầy đủ] |

### Group B — [chosen label, vd "Allocation logic"]

| # | Rule | Description |
|---|------|-------------|
| BR-03 | [Rule name] | [Câu đầy đủ] |

> Thêm/bớt group theo feature. Xóa hint block này trước khi publish.

---

## State Machine

> [Xóa nếu entity không có lifecycle]

### [Entity Name] Lifecycle

```
[State A] → [State B] → [State C]
                       ↘ [State D] (exception path)
```

| From | To | Trigger | Who can trigger | Notes |
|------|----|---------|-----------------|-------|
| ... | ... | ... | ... | ... |

---

## Acceptance Criteria

| AC | Given | When | Then | Maps to |
|----|-------|------|------|---------|
| AC-01 | [precondition] | [action] | [expected result] | US-01, BR-01 |
| AC-02 | ... | ... | ... | US-02 |

---

## Data Model & Validation

> [Xóa nếu feature không introduce/modify entity]

### Data Model

#### [Entity Name]

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| code | Text | Yes | [Unique identifier] |
| name | Text | Yes | [Display name] |
| status | Enum: Draft, Active, Inactive | Yes | [Lifecycle status] |
| productRef | Ref → Product (PRD-MD-001) | Yes | Tham chiếu master Product |
| ... | ... | ... | ... |

> **Quy tắc cross-reference**:
> - Entity đã có PRD → `Ref → {Entity} (PRD-XX-NNN)` — không redefine field.
> - Entity chưa có PRD → `Ref → {Entity} (⚠️ chưa có PRD — cần tạo PRD tại docs/prd/by-module/{domain}/{slug}/)`.
> - Reference enum/status từ source PRD, không re-list.

### Validation Rules

| # | Field(s) | Rule | Error message (user-facing tiếng Việt) |
|---|----------|------|-----------------------------------------|
| VR-01 | code | Unique trong tenant. Pattern: ^[A-Z0-9_-]+$, max 20 chars | "Mã {entity} đã tồn tại" |
| VR-02 | ... | ... | ... |

### Entity Relationships

> [Xóa nếu chỉ 1 entity]

| From | To | Relationship | Description |
|------|----|--------------|-------------|
| ... | ... | 1:N | ... |

### Module Consumers

> [Bắt buộc cho domain `master-data` và `shared-kernel`. Xóa nếu domain khác]

| Entity | Consuming Domain | Feature/Use Case | Notes |
|--------|------------------|-------------------|-------|
| ... | demand | ... | ... |
| ... | drp-engine | ... | ... |

---

## Permission Matrix

> [Đối chiếu canonical `P05-SCP-RBAC-spec.md` 6×18 matrix. Xóa nếu feature không có user-facing operation]

| Operation | Persona | Data Scope | Notes |
|-----------|---------|------------|-------|
| View list | [Persona] | [own / branch / all] | |
| View detail | [Persona] | [scope] | |
| Create | [Persona] | [scope] | |
| Update | [Persona] | [scope] | |
| Delete | [Persona] | [scope] | [Soft delete? Confirm required?] |
| Export | [Persona] | [scope] | |
| Approve | [Persona] | [scope] | [State transition trigger] |

---

## Wireframes

> Xem [WF-{PREFIX}-{NNN}-{title-slug}.md](./WF-{PREFIX}-{NNN}-{title-slug}.md) cho detail screen design.
> Hoặc: "Wireframes skipped — feature là API-only, không có UI screen mới."

---

## UI/UX Notes

[Behavioral notes cho FE — search/filter behavior, empty state, loading state, error handling từ góc user]

> **KHÔNG đặt ở đây**: data invariant, validation logic, state transition rule, permission/scope rule. Đó là BR — đặt ở section trên.

### i18n

| Key | EN | VI |
|-----|----|----|
| ... | ... | ... |

---

## Notifications

> [Xóa nếu feature không trigger notification]

| Event | Channel | Recipient | Message summary |
|-------|---------|-----------|-----------------|
| ... | ... | ... | ... |

---

## Configurable Parameters

> [Đối chiếu canonical `P06-SCP-Admin-spec.md` Config Registry. Xóa nếu nothing configurable]

| Parameter | Default | Why configurable | Tenant override? |
|-----------|---------|-------------------|-------------------|
| ... | ... | ... | Yes/No |

---

## Customer Variants

> [Xóa nếu feature không có customer overlay. Reference file overlay — không copy logic]

| Customer | Overlay reference | Key differences |
|----------|--------------------|------------------|
| UNIS | `customer-variants/UNIS-Overlay.md` | [2-Tier SS, LCNB, CN approve, ...] |
| TTC | `customer-variants/TTC-Overlay.md` | [1-Tier SS, NM nội bộ, ...] |
| MDLZ | `customer-variants/MDLZ-Overlay.md` | [LCNB last, Phase 2 stub] |

---

## Non-functional Requirements

> [Đối chiếu canonical `P04-SCP-NFR-spec.md`. Xóa nếu không relevant]

- Data volume ước tính: [vd ~50K SKU-Location combo per tenant per DRP run]
- Concurrency: [vd nhiều planner có thể edit cùng plan, optimistic locking]
- Latency target: [vd allocation engine < 5 min for 10K SKU]
- Antifragility: [retry / DLQ / chaos rules nếu có]

---

## Dependencies

### Entity Dependencies

| Entity | PRD Status | Path | Blocking? |
|--------|-----------|------|-----------|
| ... | ✅ PRD exists | `docs/prd/by-module/master-data/001-entity-registry/PRD-MD-001-*.md` | No |
| ... | ⚠️ No PRD yet | — | Yes — cần tạo PRD trước dev |

### Other Dependencies
- Modules/features khác beyond entity references
- External integration (ERP/WMS/TMS connectors)
- Data must be seeded

---

## Out of Scope

- [Điều PRD này KHÔNG cover]
- [Sub-feature scheduled cho phase sau]

---

## Open Questions

| # | Question | Impact | Owner | Status |
|---|----------|--------|-------|--------|
| OQ-01 | [Unresolved decision] | [Ảnh hưởng feature thế nào] | [Ai decide] | Open / Resolved |

---

## Traceability

> [Đối chiếu canonical `traceability/RTM.md`]

| Canonical FR | Canonical BR | This PRD ID | Test scenario |
|--------------|--------------|--------------|----------------|
| FR-XXX | BR-XXX | US-01, BR-01 | TC-XXX |

---

## Version History

| Version | Ngày | Thay đổi | Lý do |
|---------|------|----------|-------|
| 1.0 | [YYYY-MM-DD] | Khởi tạo PRD | [Yêu cầu từ PM / Tách từ Master M0X / Breakdown từ F0X canonical] |
