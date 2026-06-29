# Master PRD Breakdown — Quy trình tách Master ra PRD by-module

Mode **Breakdown** là phức tạp nhất trong skill này. Reference này đi sâu vào quy trình: đọc Master PRD lớn → tách thành nhiều PRD nhỏ theo 13 domain SCP, đảm bảo traceability ngược về canonical, không miss content, không duplicate.

## Khi nào cần Breakdown

- Master spec ≥ 500 dòng, dev đọc thẳng thì lạc.
- Master spec mix nhiều domain — dev của 1 team không cần đọc hết.
- Master spec cần versioning per-feature, nhưng đang ở 1 file tổng → mỗi sửa 1 chỗ phải bump version cả file.
- User reference `PRD_v4_1_2_SSoT_FINAL.md` hoặc `SCP-DRP-Strategic-PRD.md` và muốn convert sang granular per-domain.

## Input có thể gặp

| Input file | Mức độ Master | Approach |
|---|---|---|
| `SCP-DRP-Strategic-PRD.md` (943 dòng) | Strategic — WHY/WHAT/KPI/phasing | Breakdown → high-level PRD per domain, mỗi domain 1-3 PRD |
| `domains/{X}/F0X-*-spec.md` (200-1100 dòng) | Detailed domain spec | Breakdown → 1 PRD per major feature trong domain |
| `PRD_v4_1_2_SSoT_FINAL.md` (~9000 dòng) | All-in-one legacy | Breakdown nghiêm túc — có thể tạo 30-50 PRD by-module |
| `v4_1_2_modules/M0X_*.md` (M01-M10) | Module-level legacy | Map M0X → tương ứng 1-2 domain mới, breakdown thành sub-PRD |

## Quy trình chi tiết — 9 bước

### Bước 1 — Read Master end-to-end (không skim)

Đây là bước tốn thời gian nhất, **không bỏ qua**. Skim làm miss BR hidden trong middle of section. Đọc xong, có notes:

- **Entity list** — mọi entity nhắc trong Master.
- **BR list** — mọi rule (đánh số nếu chưa, theo thứ tự xuất hiện).
- **US list** — mọi user story (đánh số nếu chưa).
- **State machine** — mọi entity có lifecycle.
- **KPI list** — mọi metric Master định nghĩa hoặc reference.
- **Persona list** — mọi role/actor Master đề cập.
- **Open Question** — câu hỏi Master còn ghi `[TBD]` hoặc tương tự.

### Bước 2 — Build domain map

Phân loại từng item (entity, BR, US, state machine) vào **đúng 1** trong 13 domain. Nếu item cross-domain (thuộc 2+ domain), ghi nhận → resolve ở Bước 4.

**Quy tắc map**:

| Item | Map vào |
|------|---------|
| Entity master (Product, BP, Location, UoM, …) | `master-data` |
| Demand forecast / S&OP / AOP | `demand` |
| 6 Buckets / Safety Stock / Reorder | `supply-inventory` |
| Allocation logic / DRP run / Lot Sizing | `drp-engine` |
| SO Plan / TO Plan / ProC | `order-planning` |
| Simulation / Plan compare / Publish | `simulation` |
| Revision / Delta / ACK / Bitemporal | `daily-replan` |
| Vehicle frame / Multi-drop | `transport` |
| Exception types / War Room / Escalation | `exception` |
| KPI / Dashboard / Forecast accuracy report | `analytics` |
| Canonical ERD / base columns / Policy Platform | `shared-kernel` |
| ERP/WMS/TMS connector / DLQ | `integration` |
| Config Registry / RBAC / NFR / SSO | `admin` |

Output Bước 2: bảng `Item → Domain` covering 100% Master content.

### Bước 3 — Determine feature granularity per domain

Trong mỗi domain, decide tách thành bao nhiêu PRD. Default rule:

| Domain content size | Granularity |
|---|---|
| ≤ 10 BR + ≤ 5 US | 1 PRD duy nhất cho domain |
| 10-30 BR / 5-20 US | 1 PRD chính + (optional) BR Catalog |
| ≥ 30 BR / ≥ 20 US | Tách 2-3 sub-feature PRD trong cùng folder, có BR Catalog + US Catalog |

Cách tách sub-feature trong cùng domain:
- Theo **major use case** (vd `master-data` tách thành `entity-registry`, `data-quality`).
- Theo **persona track** (vd `demand` tách thành `planner-workflow`, `manager-review`).
- Theo **lifecycle phase** (vd `drp-engine` tách thành `allocation`, `lot-sizing`, `run-orchestration`).

**Đừng tách quá nhỏ** — PRD chỉ có 3 BR đọc không có giá trị, dev phải open nhiều file. Threshold tham khảo: PRD ≥ 100 dòng / ≥ 10 BR mới đáng đứng riêng.

### Bước 4 — Create folder structure

Tạo folder per (domain, feature):
```
docs/prd/by-module/{domain}/{NNN}-{feature-slug}/
```

Numbering scan `docs/prd/by-module/{domain}/` lấy max + 1. Nếu Breakdown lần đầu cho domain → start `001`.

### Bước 5 — Extract per-feature content

Với mỗi (domain, feature), trích từ Master:

| Section | Trích từ | Lưu ý |
|---------|----------|-------|
| Overview | Master intro + domain-specific paragraph | Viết lại ngắn gọn, không copy nguyên đoạn |
| Personas | Master personas filter theo feature | Chỉ list persona liên quan, không full catalog |
| User Stories | Master US filter theo feature | Áp story-loose standard (xem prd-format.md) |
| Business Rules | Master BR filter theo feature | Áp spec-tight standard, MECE check |
| State Machine | Master state machine entity thuộc feature | Vẽ lại với từ Master, đảm bảo đầy đủ transition |
| Acceptance Criteria | Master AC + tự sinh thêm theo BR/US mới | Mỗi BR/US map ≥ 1 AC |
| Data Model | Master data model filter theo entity thuộc feature | Cross-ref entity domain khác (không re-define) |
| Permission Matrix | Master perm matrix filter theo entity feature | Đối chiếu canonical `P05` |
| UI/UX Notes | Master UI notes filter theo screen feature | KHÔNG chứa BR/VR |
| Configurable Parameters | Master config filter theo feature | Đối chiếu canonical `P06` Config Registry |
| Customer Variants | Master customer overlay filter | Reference overlay file, không copy |
| Dependencies | Compute từ entity ref + tham chiếu Master | Phân ✅/⚠️ |
| Out of Scope | Master out-of-scope filter | Rõ ràng feature này KHÔNG cover |
| Open Questions | Master OQ filter | Carry forward, không tự resolve |
| Traceability | Map từ Master section ID | Bảng `Canonical FR/BR ↔ This PRD ID` |
| Version History | Khởi `1.0` với reason "Breakdown từ Master {file}" | Date = ngày breakdown |

### Bước 6 — Cross-reference cleanup

Sau khi tách, check inter-PRD references:

1. **Entity references**: PRD A reference entity owned by domain B → ghi `Ref → Entity (PRD-B-NNN)`. Nếu PRD-B-NNN chưa được tạo → flag ⚠️.
2. **BR depends BR khác domain**: ghi rõ trong `## Dependencies` của PRD: `Depends on BR-DM-005 (Demand — Forecast versioning)`.
3. **State machine cross-domain**: nếu state transition cần trigger ở domain khác (vd allocation engine generate SO con → notify OMS), ghi rõ trong section Notifications/Integration.

### Bước 7 — Customer variant split

Master có thể chứa lẫn lộn behavior chung + behavior per-customer. Khi tách:

- **Behavior chung** → đưa vào PRD chính.
- **Behavior per-customer** → KHÔNG copy vào PRD chính. Thay vào đó:
  - Trong PRD section `## Customer Variants` → bảng reference đến `customer-variants/{X}-Overlay.md`.
  - Trong canonical overlay file → giữ nguyên detail (không phải việc của Breakdown mode).

Ví dụ: Master ghi "UNIS dùng 2-tier safety stock, các customer khác 1-tier". Trong PRD by-module `supply-inventory/00X-safety-stock/`:

```markdown
## Customer Variants

| Customer | Overlay reference | Key differences |
|----------|--------------------|------------------|
| Default | — | 1-tier safety stock (Z × σ × √(lead_time + review_period)) |
| UNIS | `customer-variants/UNIS-Overlay.md` §2-Tier SS | 2-tier: tier 1 at DC, tier 2 at store |
```

### Bước 8 — Self-review per PRD

Chạy Developer-Ready Checklist (xem `workflow-modes.md`) cho **mỗi** PRD. Đặc biệt:

- MECE check trong context PRD nhỏ — có thể có BR Master nằm cross-domain mà BA tách nhầm → fix.
- Coverage: tổng số BR/US/Entity sau Breakdown = tổng Master? Nếu thiếu, có item nào miss?
- Cross-ref: mọi `Ref →` có target tồn tại hoặc flag ⚠️?

### Bước 9 — Output summary

Khi xong Breakdown, trả về user:

```
BREAKDOWN_SUMMARY:
Master file: docs/prd/PRD_v4_1_2_SSoT_FINAL.md
Total PRDs created: N
Total BRs migrated: X
Total USs migrated: Y
Total entities mapped: Z

Per domain:
- master-data: 3 PRDs (45 BR, 12 US)
- demand: 2 PRDs (28 BR, 15 US)
- supply-inventory: 1 PRD (18 BR, 6 US)
- drp-engine: 4 PRDs (62 BR, 22 US) — has BR Catalog + US Catalog
- order-planning: 2 PRDs (35 BR, 18 US) — has BR Catalog
- ...

Files created: <list>
Open Questions: N (need PO review)
Cross-domain dependencies flagged: M

CANONICAL_ALIGNMENT: OK | DRIFT (list)
TRACEABILITY: complete | partial (list missing)
```

## Anti-patterns

### Anti-pattern 1 — Copy nguyên section từ Master sang PRD nhỏ
**Hậu quả**: PRD nhỏ chứa text dài lê thê, dev phải đọc cả những phần không relevant.
**Fix**: trích lọc theo feature scope, viết lại ngắn gọn.

### Anti-pattern 2 — Tách quá granular
**Hậu quả**: 1 domain có 15 PRD, mỗi PRD 5 BR. Dev phải open hàng chục file, cross-ref hỗn loạn.
**Fix**: gộp lại theo major use case, threshold ≥ 100 dòng / ≥ 10 BR / 1 PRD.

### Anti-pattern 3 — Bỏ Open Question khi tách
**Hậu quả**: Master có OQ chưa resolve, BA "đoán" answer khi viết PRD nhỏ. Khi resolve khác đoán → rework.
**Fix**: carry forward mọi OQ, kèm owner. Không tự resolve.

### Anti-pattern 4 — Quên customer overlay
**Hậu quả**: PRD nhỏ chứa logic UNIS-specific như default rule, dev implement nhầm cho mọi customer.
**Fix**: section `## Customer Variants` đầy đủ, reference overlay file.

### Anti-pattern 5 — Mismatch numbering
**Hậu quả**: Tạo `001-foo` trong khi domain đã có `001-bar` từ trước → conflict.
**Fix**: ALWAYS scan `docs/prd/by-module/{domain}/` trước khi assign NNN.

### Anti-pattern 6 — Drift canonical
**Hậu quả**: Master có BR nói "X", PRD nhỏ tự viết "X nâng cao" mà không flag.
**Fix**: align nguyên văn (hoặc rút gọn), drift → Open Question.

## Checklist trước khi mark Breakdown DONE

- [ ] 100% Master content đã map vào ≥ 1 PRD by-module.
- [ ] Mỗi PRD pass Developer-Ready Checklist độc lập.
- [ ] Mọi cross-domain reference đúng (PRD path tồn tại hoặc ⚠️ flagged).
- [ ] Customer overlay không leak vào PRD chính.
- [ ] Mọi PRD có `## Version History` entry `1.0` ghi rõ "Breakdown từ {Master file}".
- [ ] Summary output rõ ràng, user dễ verify.
