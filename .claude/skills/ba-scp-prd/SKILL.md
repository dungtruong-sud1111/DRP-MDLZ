---
name: ba-scp-prd
description: BA PRD writer + maintainer cho dự án SCP/DRP (Supply Chain Planning / Distribution Requirements Planning) của Smartlog. Skill này GỘP 3 chế độ làm việc trên cùng một bộ artifact — (1) **Author**: viết PRD/User Story/Wireframe cho feature mới trong SCP; (2) **Breakdown**: đọc Master PRD canonical (`docs/prd/SCP-DRP-SPEC-SYSTEM-FINAL/`) hoặc PRD lớn (`PRD_v4_1_x_*.md`) và tách thành nhiều PRD nhỏ theo 13 domain SCP (master-data, demand, supply-inventory, drp-engine, order-planning, simulation, daily-replan, transport, exception, analytics + 3 cross-cutting hub) kèm BR catalog và US catalog; (3) **Analyze & Update**: phân tích PRD/US đã có, cập nhật business rules, acceptance criteria, validation rules, version history khi có change request. Trigger bất cứ khi nào user nói "PRD", "user story", "BR", "break down master", "tách PRD", "phân tích PRD SCP", "viết PRD cho module X", "cập nhật US", "wireframe SCP", "phân tích nghiệp vụ chuỗi cung ứng", "DRP", "S&OP", "demand planning", "supply planning", "MRP", "safety stock", "replenishment", "allocation", "lot sizing", "daily replan", "scenario approval", hoặc khi user mô tả flow Master Data → Demand → Supply → DRP → Order Planning → Transport mà chưa nói rõ "PRD". Cũng trigger khi user reference các file `SCP-DRP-Strategic-PRD.md`, `M01..M10` modules, hoặc đề cập đến UNIS/TTC/MDLZ customer overlays. KHÔNG dùng cho code, ERD vật lý/migration (đã có `db-architect`), API contract chi tiết (thuộc dev), hay logistics ngoài SCP (TMS/WMS execution thì dùng `ba-prd` / `scm-business-analyst`).
---

# SCP/DRP — BA PRD Writer & Maintainer

Skill này phục vụ một mục tiêu duy nhất: giữ cho PRD layer của hệ SCP/DRP luôn đồng bộ với Master canonical, đúng convention versioning, và developer-ready ở mức "đọc xong là code/test được". Skill này KHÔNG sinh schema DB, KHÔNG viết API contract chi tiết, KHÔNG quyết định kỹ thuật — đó là việc của `db-architect` và downstream dev skills.

## Skill này phục vụ ai

Business Analyst làm dự án Smartlog SCP/DRP. BA đã hiểu domain Supply Chain Planning (S&OP, MRP, DRP, Safety Stock, Replenishment, Allocation), biết đọc Master PRD `SCP-DRP-SPEC-SYSTEM-FINAL`, và cần một quy trình thống nhất để (a) viết PRD feature mới, (b) tách Master PRD thành PRD by module, (c) cập nhật PRD đã có theo change request — đều theo cùng một bộ format và versioning.

## 3 chế độ làm việc

Trước khi bắt đầu, **xác định ngay user đang ở mode nào** — vì input/output/quy trình khác nhau. Nếu không rõ, hỏi user 1 câu rồi mới làm.

| Mode | Khi nào dùng | Input chính | Output chính |
|---|---|---|---|
| **Author** | User mô tả feature mới chưa có PRD trong `docs/prd/by-module/` | User prompt + Master PRD context | 1 cặp PRD + WF mới |
| **Breakdown** | User đưa Master PRD/PRD lớn và nói "tách ra theo module" hoặc "break down" | File Master (`SCP-DRP-Strategic-PRD.md`, `PRD_v4_1_2_SSoT_FINAL.md`, hoặc spec dài) | N cặp PRD by domain + BR-catalog + US-catalog + traceability map |
| **Analyze & Update** | User chỉ vào PRD/US đang có và yêu cầu sửa, thêm BR, đổi flow, bump version | PRD hiện tại + change request | PRD đã cập nhật + entry trong Version History |

Tín hiệu nhận diện:
- "Viết PRD cho [feature]", "tạo spec [feature]" → **Author**
- "Tách Master ra", "break down [file]", "chia M01 ra thành các PRD nhỏ", "đọc Strategic PRD và tạo PRD by module" → **Breakdown**
- "Sửa BR-XX", "thêm AC", "update PRD theo feedback", "bump version", "cập nhật US-XX cho rule mới" → **Analyze & Update**

Quy trình chi tiết từng mode xem `references/workflow-modes.md`. Đặc biệt với mode **Breakdown** (phức tạp nhất), đọc kỹ `references/master-prd-breakdown.md` trước khi bắt đầu.

## Output: 3 loại artifact, tổ chức theo 13 domain

Mỗi feature/sub-feature sản sinh 1 folder con dưới `docs/prd/by-module/{domain}/`. Folder chứa tối thiểu 2 file (PRD + WF), tối đa 4 file (thêm BR-catalog và US-catalog khi feature lớn).

| Artifact | Path | Khi nào tạo |
|---|---|---|
| PRD | `docs/prd/by-module/{domain}/{NNN}-{feature-slug}/PRD-{PREFIX}-{NNN}-{title-slug}.md` | Mọi feature |
| Wireframes | `docs/prd/by-module/{domain}/{NNN}-{feature-slug}/WF-{PREFIX}-{NNN}-{title-slug}.md` | Có UI mới — quy tắc trong [references/wireframe-guide.md](references/wireframe-guide.md) |
| BR Catalog | `docs/prd/by-module/{domain}/{NNN}-{feature-slug}/BR-CATALOG-{PREFIX}-{NNN}.md` | Mode Breakdown khi domain có ≥ 30 BR; hoặc khi user yêu cầu rõ |
| US Catalog | `docs/prd/by-module/{domain}/{NNN}-{feature-slug}/US-CATALOG-{PREFIX}-{NNN}.md` | Mode Breakdown khi domain có ≥ 20 US; hoặc khi user yêu cầu rõ |

### 13 Domain dirs (theo canonical `SCP-DRP-SPEC-SYSTEM-FINAL`)

| Domain dir | Prefix | Covers | Canonical spec ref |
|---|---|---|---|
| `master-data` | `MD` | Entity Registry (18 entities), Data Quality, CRUD lifecycle | `F01a`, `F01b` |
| `demand` | `DM` | AOP, S&OP, PO Pending, Phasing, Forecast | `F02` |
| `supply-inventory` | `SI` | 6 Buckets (canonical), Safety Stock, Pipeline | `F03` |
| `drp-engine` | `DE` | Allocation Engine, 2-Phase 6-Layer, Lot Sizing, DRP Run | `F04a`, `F04b` |
| `order-planning` | `OP` | SO/TO Lifecycle, ProC Workflow, Cross-ORG | `F05a`, `F05b` |
| `simulation` | `SM` | Plan Registry, Compare, Publish | `F06` |
| `daily-replan` | `DR` | Revision, Delta, ACK/NACK, Bitemporal | `F07` |
| `transport` | `TP` | Vehicle Frame, 3 Rules, Multi-Drop | `F08` |
| `exception` | `EX` | 20 exception types, War Room, SLA | `F09` |
| `analytics` | `AN` | 17 KPIs, Dashboards, Forecast Accuracy | `F10` |
| `shared-kernel` | `SK` | Canonical ERD, base columns, policy platform | `P01`, `P02` |
| `integration` | `IG` | ERP/WMS/TMS connectors, DLQ | `P03` |
| `admin` | `AM` | Config Registry, RBAC, SSO, NFR | `P04`, `P05`, `P06` |

**Nếu feature không khớp 13 domain trên**: dừng, hỏi user `"Feature này không thuộc 13 domain SCP. Bạn muốn đặt vào domain nào, hoặc cần định nghĩa domain mới?"`. Không tự tạo domain mới — flag thành Open Question và chờ user/PO confirm.

### Numbering & file naming

- `{NNN}` = 3 chữ số, scope per domain, tự động dò: scan `docs/prd/by-module/{domain}/` lấy `{NNN}` lớn nhất + 1. Nếu chưa có folder nào → `001`.
- `{feature-slug}` = lowercase kebab-case 2–4 từ. **Không** prefix domain (đã trong path). Ví dụ `001-entity-registry`, không phải `001-md-entity-registry`.
- `{title-slug}` (trong tên file) = lowercase kebab-case 2–4 từ rút từ H1 của PRD. Loại stop-word ("management", "module", "feature") nếu bỏ không mất nghĩa.
- Một folder có thể chứa nhiều PRD (sub-feature) — mỗi file có `{title-slug}` riêng biệt.

Ví dụ:
- `docs/prd/by-module/master-data/001-entity-registry/PRD-MD-001-entity-registry.md`
- `docs/prd/by-module/drp-engine/001-allocation-engine/PRD-DE-001-allocation-engine.md`
- `docs/prd/by-module/drp-engine/001-allocation-engine/PRD-DE-001-lot-sizing.md` (sub-feature trong cùng folder)
- `docs/prd/by-module/demand/002-sop-cycle/WF-DM-002-sop-cycle.md`

## Core principles (apply cho cả 3 mode)

### Canonical override

Mỗi khi BR / state / persona / KPI / threshold trong PRD by-module mâu thuẫn với `docs/prd/SCP-DRP-SPEC-SYSTEM-FINAL/`, **canonical thắng**. Không silent-diverge — flag thành Open Question và đợi confirm. Lý do: folder `SCP-DRP-SPEC-SYSTEM-FINAL` đã pass audit 96/100 và là single source of truth của dự án; mọi drift gây ra rework downstream (RTM, test plan, dev migration).

### Business-first, tech-later

PRD mô tả từ góc nhìn user: vấn đề gì? cho ai? user thấy/làm gì? business rule nào? Decisions kỹ thuật (DB schema, API shape, auth) là việc của `db-architect` + dev skills. Tuy vậy PRD **được phép** chứa permission matrix mức persona (ai view/create/edit/delete) — để dev có authorization intent từ đầu.

### Phân biệt BR vs UX (litmus test)

Một BR mô tả **WHAT** hệ thống enforce và **WHY**. Một UX note mô tả **HOW** user trải nghiệm một screen cụ thể. Trộn 2 thứ này khiến BR section đầy screen behavior và UX section che mất domain rule.

Litmus test — với mỗi câu sắp viết, hỏi:
1. Nếu dev hit rule này qua API/import/batch (không qua UI), rule có còn áp dụng không? — **Yes → BR**, No → UX
2. Nếu redesign screen hoàn toàn ngày mai, rule có còn đúng không? — **Yes → BR**, No → UX
3. Vi phạm rule có rủi ro data integrity / money / legal / business correctness, hay chỉ là awkward? — **Risk → BR**, Awkward → UX

Khi do dự → BR. UX note KHÔNG được chứa data invariant, validation logic, state transition, hay permission/data-scope rule. Side-by-side ví dụ + common mistakes xem [references/prd-format.md](references/prd-format.md) section 4.

### Writing quality — 2 standard tách biệt

| Standard | Áp dụng cho | Mục tiêu |
|---|---|---|
| **Spec-tight** | BR / AC / VR | Một câu đầy đủ Subject + Action + Constraint, testable độc lập |
| **Story-loose** | US | Giọng user, mô tả NHU CẦU (job-to-be-done), không liệt kê field/entity/UI |

KHÔNG trộn 2 standard. Áp spec-tight vào US → US biến thành mini-spec; áp story-loose vào BR → rule không testable. Chi tiết Before/After + self-check list xem [references/prd-format.md](references/prd-format.md) sections 3 & "Writing Quality Standard".

Tóm tắt nguyên tắc US:
1. Voice của user, không phải dev.
2. 1 US = 1 nhu cầu — dấu phẩy liệt kê = đang ôm nhiều việc, tách ra.
3. Không tên entity kỹ thuật trong US (❌ `TenderedTrip` → ✅ "chuyến nhà thầu nhận"; ❌ `SOTOLifecycle` → ✅ "đơn hàng kế hoạch").
4. Không liệt kê field/status/filter trong "I want" — field thuộc Data Model, status thuộc State Machine, filter thuộc Wireframe + AC.
5. Benefit nói business outcome, không lặp what.

### MECE cho BR & US

Mỗi PRD MUST tổ chức BR và US theo MECE (Mutually Exclusive, Collectively Exhaustive) và present dưới **logical groups**:

- **Mutually Exclusive**: không 2 BR/US restate cùng một thứ ở góc khác. Trùng → merge hoặc tách overlap thành item thứ 3.
- **Collectively Exhaustive**: union của tất cả BR/US cover toàn bộ scope feature — mọi CRUD action, mọi state transition, mọi persona interaction, mọi constraint đã nêu phải map vào ≥ 1 BR hoặc US.
- **Logical grouping**: chọn taxonomy phù hợp feature, KHÔNG fix cứng:
  - CRUD-heavy → group theo action (Create / View / Update / Delete / Import-Export)
  - Workflow → group theo phase (Submission → Review → Approval → Execution)
  - Multi-persona → group theo persona
  - Domain-rich → group theo concept (Pricing / Capacity / Routing / Allocation)
- **MECE checklist** trước finalize:
  1. Pair-wise no overlap?
  2. Pair-wise no gap (mỗi persona × phase có ≥ 1 US; mỗi constraint có ≥ 1 BR)?
  3. Same granularity trong cùng group?
  4. Mỗi item map được ≥ 1 AC?

**Format ưu tiên cho BR**: bảng `| # | Rule | Description |` — mỗi rule scannable độc lập, dễ reference theo ID. Prose / bullet chỉ chấp nhận khi BR set rất nhỏ (≤ 3).

### Versioning (chung cho cả 3 mode)

Mọi PRD/WF/Catalog MUST có `## Version History` là section cuối file. Format:

```markdown
## Version History

| Version | Ngày | Thay đổi | Lý do |
|---------|------|----------|-------|
| 1.0 | 2026-05-14 | Khởi tạo PRD | Tách từ Master M04 (Breakdown mode) |
| 1.1 | 2026-05-20 | Sửa BR-03, thêm AC-07, cập nhật WF-02 layout | Review feedback từ backend-pro |
| 2.0 | 2026-06-01 | Thay state machine: bỏ Draft, thêm US-06 | Quyết định từ stakeholder meeting |
```

Quy tắc bump version:

| Thay đổi | Bump | Ví dụ |
|---|---|---|
| Tạo mới | `1.0` | Khởi tạo PRD |
| Nhỏ (sửa BR, thêm AC, layout WF) | minor `1.1`, `1.2`... | Sửa BR-03, thêm AC-07 |
| Lớn (thêm/bỏ US, đổi state machine, đổi data model cấu trúc) | major `2.0`, `3.0`... | Bỏ state Draft |

**Khi nào ghi version entry**:
- Tạo mới file: ghi `1.0` ngay, date = hôm nay, change = "Khởi tạo PRD", reason = nguồn yêu cầu.
- Update file đã có: **KHÔNG bump version sau mỗi edit nhỏ trong cùng phiên**. Thay vào đó:
  1. Sửa nội dung như bình thường.
  2. Chỉ thêm **1 entry duy nhất** ở cuối phiên (khi user nói "xong", "finalize", "ship", hoặc khi mọi thay đổi rõ ràng đã kết thúc).
  3. Entry tóm tắt MỌI thay đổi trong phiên, liệt kê ID bị ảnh hưởng (BR-xx, AC-xx, US-xx, WF-xx).
  4. Cột "Lý do" capture nguồn: user request / review feedback (từ reviewer nào) / stakeholder decision / breakdown từ Master.

**Detect version hiện tại khi update**:
1. Read file trước.
2. Check `## Version History` section.
3. Có → đọc version mới nhất → bump theo rule trên → append row mới.
4. Không có (legacy file) → thêm section ở cuối, version khởi đầu = `1.1` (vì file đã có content trước), không phải `1.0`.

## Quy trình thực hiện

### Bước 0 — Xác định mode

Đọc user prompt. Phân loại:
- Feature mới chưa có PRD → **Author** → đi tiếp Bước 1.
- File Master / spec lớn cần tách → **Breakdown** → đọc [references/master-prd-breakdown.md](references/master-prd-breakdown.md) rồi áp dụng.
- PRD/US đã có cần sửa → **Analyze & Update** → đọc [references/workflow-modes.md](references/workflow-modes.md) section "Update Mode".

### Bước 1 — Hiểu request

Identify:
- Feature/capability nào được yêu cầu.
- Thuộc domain SCP nào (xem [references/domain-supply-chain.md](references/domain-supply-chain.md) + [references/domain-supply-demand.md](references/domain-supply-demand.md) + [references/domain-scp.md](references/domain-scp.md)).
- Primary persona là ai.

### Bước 2 — Xác định domain + numbering

Match feature vào 1 trong 13 domain. Không khớp → hỏi user. Scan `docs/prd/by-module/{domain}/` lấy `{NNN}` tiếp theo.

### Bước 3 — Load Master + Canonical context (BẮT BUỘC)

Đọc **trước** khi viết:

1. `docs/prd/SCP-DRP-SPEC-SYSTEM-FINAL/SCP-DRP-Strategic-PRD.md` — WHY/WHAT/KPI/phasing.
2. `docs/prd/SCP-DRP-SPEC-SYSTEM-FINAL/domains/{domain-folder}/F0X-*.md` — spec canonical cho domain đang làm.
3. `docs/prd/SCP-DRP-SPEC-SYSTEM-FINAL/cross-cutting/P01-SCP-SharedKernel-spec.md` — canonical ERD + base columns.
4. `docs/prd/SCP-DRP-SPEC-SYSTEM-FINAL/cross-cutting/P07-SCP-Glossary-spec.md` — terminology canonical (28 terms VN↔EN).
5. Nếu feature có customer overlay impact: `docs/prd/SCP-DRP-SPEC-SYSTEM-FINAL/customer-variants/{UNIS|TTC|MDLZ}-Overlay.md`.

**Consistency rule**: mọi PRD by-module phải align canonical. Drift → Open Question, không silent-diverge.

### Bước 4 — Hỏi research khi cần

Hỏi user: "Feature này có cần research competitor / best practice trước khi viết PRD không?"
- Yes → `WebSearch` 2–3 platform SCP/DRP (SAP IBP, Kinaxis RapidResponse, o9 Solutions, Anaplan, Blue Yonder) → đúc kết vào section `## Research Findings`.
- No → skip.

### Bước 5 — Entity Registry detection (cross-PRD scan)

Trước khi viết Data Model, scan TẤT CẢ PRD trong `docs/prd/by-module/*/` + canonical `F01a-SCP-EntityRegistry-spec.md` để build entity registry. Quy tắc:

1. **MUST reference, not redefine**: nếu entity đã có PRD (Business Partner, Location, SKU, UoM…), dùng `Ref → {Entity}` trong data model — KHÔNG redefine field.
2. **Flag unknown references**: entity cần dùng nhưng chưa có PRD → `Ref → {Entity} (⚠️ chưa có PRD — cần tạo PRD tại docs/prd/by-module/{domain}/{slug}/)`.
3. **Detect duplicates**: field/concept mới overlap với entity đã có → Open Question.
4. **Dependencies section** liệt kê tất cả entity referenced kèm path PRD, phân ✅ ready vs ⚠️ blocking.
5. **Enum/Status reuse**: dùng giá trị từ source PRD (vd `partnerType: Customer|Carrier` từ Business Partner), không re-list.
6. **SharedData consumer mapping**: khi PRD thuộc `master-data` hoặc `shared-kernel`, MUST có bảng "Module Consumers" liệt kê các domain sẽ reference entity và mục đích — giúp dev đánh giá blast radius.

### Bước 6 — Viết PRD theo format

Follow [references/prd-format.md](references/prd-format.md). Bắt đầu từ [templates/prd.md](templates/prd.md). Sections chính:

- **Overview**: problem, target users, goals + Module/Complexity/Primary persona
- **User Personas**: chỉ list persona liên quan feature này, không lặp full catalog
- **User Stories**: format `As a / I want / So that` — group theo taxonomy phù hợp feature, áp story-loose standard
- **Business Rules**: bảng numbered theo group — áp spec-tight standard. **Nếu có rule "system tự X sau Y" / "mỗi N giờ chạy" / "tự cảnh báo khi quá ngưỡng" / "định kỳ"**, đọc [references/system-patterns.md](references/system-patterns.md) trước khi viết — chọn đúng fire-and-forget vs recurring + companion rules (re-schedule / cancel / idempotency) để tránh anti-pattern polling 60s
- **State Machine**: khi entity có lifecycle (Order: Draft → Confirmed → InProgress → Completed → Cancelled, DRP Run: Created → Running → Approved → Published…)
- **Acceptance Criteria**: bảng Given/When/Then, mỗi US/BR map ≥ 1 AC
- **Data Model & Validation**: business-level (Text / Number / Date / Enum / Ref → Entity), VR với user-facing error message tiếng Việt có dấu, entity relationships
- **Permission Matrix**: persona-level (không technical permission code), data scope (own/branch/all) — đối chiếu canonical `P05-SCP-RBAC-spec.md` 6×18 matrix
- **UI/UX Notes**: behavioral notes cho FE — search/filter behavior, empty state, loading state. KHÔNG chứa BR / VR / state transition / permission rule
- **Configurable Parameters**: gì có thể config per tenant — đối chiếu canonical `P06-SCP-Admin-spec.md` Config Registry
- **Customer Variants** (mục riêng cho SCP): nếu feature có overlay UNIS/TTC/MDLZ — reference customer-variant file, không copy logic
- **Non-functional Requirements**: data volume, concurrency, latency (đối chiếu `P04-SCP-NFR-spec.md`)
- **Dependencies**: entity dependencies với PRD status ✅/⚠️
- **Out of Scope**: rõ ràng feature này KHÔNG cover gì
- **Open Questions**: bảng unresolved decisions
- **Version History**: section cuối file

### Bước 7 — Wireframes (khi cần)

Auto-detect — tạo WF khi:
- Screen/page/dialog mới
- Form ≥ 4 field
- Multi-step workflow
- Table với filter/sort/bulk action
- Dashboard / split-panel / master-detail
- User mention "UI", "giao diện", "màn hình"

Skip khi: API-only, single-button action, pure BR change không impact UI.

Khi tạo WF: trước hết xác định container pattern (Dialog vs Drawer vs Detail View vs Wizard vs Full-page) theo [references/wireframe-guide.md](references/wireframe-guide.md) → Container Pattern Decision. Create + Edit dùng cùng pattern (trừ exception entity có sub-data). Annotation pattern lên WF đầu (vd: `A1: Dùng Drawer — 10 field, cần giữ list context`).

### Bước 8 — Output ending signals

Khi xong, output:

```
MODE: author | breakdown | analyze-update
PRD_PATH: docs/prd/by-module/{domain}/{NNN}-{feature-slug}/PRD-{PREFIX}-{NNN}-{title-slug}.md
WIREFRAME_PATH: <path> | skipped (lý do)
BR_CATALOG_PATH: <path> | n/a
US_CATALOG_PATH: <path> | n/a
DOMAIN: master-data | demand | supply-inventory | drp-engine | order-planning | simulation | daily-replan | transport | exception | analytics | shared-kernel | integration | admin
COMPLEXITY: Simple | Medium | Complex
RESEARCH: none | light | deep
CANONICAL_REF: <list các file canonical đã align>
OPEN_QUESTIONS: <số OQ chưa resolve>
READY_FOR_DEV: true | false
```

## Read references by topic

| Topic | Read file |
|---|---|
| **Master PRD canonical (đọc đầu tiên)** | `docs/prd/SCP-DRP-SPEC-SYSTEM-FINAL/SCP-DRP-Strategic-PRD.md` |
| **Canonical domain spec** | `docs/prd/SCP-DRP-SPEC-SYSTEM-FINAL/domains/{domain}/F0X-*.md` |
| **Canonical shared kernel + ERD** | `docs/prd/SCP-DRP-SPEC-SYSTEM-FINAL/cross-cutting/P01-SCP-SharedKernel-spec.md` |
| **Canonical glossary VN↔EN** | `docs/prd/SCP-DRP-SPEC-SYSTEM-FINAL/cross-cutting/P07-SCP-Glossary-spec.md` |
| **Customer overlays** | `docs/prd/SCP-DRP-SPEC-SYSTEM-FINAL/customer-variants/{UNIS|TTC|MDLZ}-Overlay.md` |
| Workflow chi tiết cho 3 mode | [references/workflow-modes.md](references/workflow-modes.md) |
| **Master PRD breakdown** (mode Breakdown) | [references/master-prd-breakdown.md](references/master-prd-breakdown.md) |
| PRD structure & section guide | [references/prd-format.md](references/prd-format.md) |
| Supply Chain domain knowledge tổng quan | [references/domain-supply-chain.md](references/domain-supply-chain.md) |
| Supply & Demand Planning domain | [references/domain-supply-demand.md](references/domain-supply-demand.md) |
| SCP/DRP-specific concepts (allocation, lot sizing, daily replan) | [references/domain-scp.md](references/domain-scp.md) |
| Wireframe design patterns | [references/wireframe-guide.md](references/wireframe-guide.md) |
| Background job patterns (fire-and-forget vs recurring) | [references/system-patterns.md](references/system-patterns.md) |
| PRD template | [templates/prd.md](templates/prd.md) |
| Wireframe template | [templates/wireframe.md](templates/wireframe.md) |
| BR Catalog template (mode Breakdown) | [templates/br-catalog.md](templates/br-catalog.md) |
| US Catalog template (mode Breakdown) | [templates/us-catalog.md](templates/us-catalog.md) |

## Directory structure (target output)

```
docs/prd/
├── SCP-DRP-SPEC-SYSTEM-FINAL/         ← canonical (READ-ONLY cho skill này)
│   ├── SCP-DRP-Strategic-PRD.md
│   ├── domains/ ...
│   └── cross-cutting/ ...
└── by-module/                          ← skill này GHI vào đây
    ├── master-data/
    │   ├── 001-entity-registry/
    │   │   ├── PRD-MD-001-entity-registry.md
    │   │   ├── WF-MD-001-entity-registry.md
    │   │   ├── BR-CATALOG-MD-001.md     (optional)
    │   │   └── US-CATALOG-MD-001.md     (optional)
    │   └── 002-data-quality/
    │       ├── PRD-MD-002-data-quality.md
    │       └── WF-MD-002-data-quality.md
    ├── demand/
    │   └── 001-sop-cycle/
    ├── supply-inventory/
    │   └── 001-six-buckets/
    ├── drp-engine/
    │   ├── 001-allocation-engine/
    │   │   ├── PRD-DE-001-allocation-engine.md
    │   │   ├── PRD-DE-001-lot-sizing.md       (sub-feature cùng folder)
    │   │   └── WF-DE-001-allocation-engine.md
    │   └── 002-drp-run/
    ├── order-planning/
    ├── simulation/
    ├── daily-replan/
    ├── transport/
    ├── exception/
    ├── analytics/
    ├── shared-kernel/
    ├── integration/
    └── admin/
```
