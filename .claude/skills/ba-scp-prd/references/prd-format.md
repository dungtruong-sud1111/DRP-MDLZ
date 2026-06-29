# PRD Format Guide

This document defines the structure of a Product Requirements Document for Smartlog SCP/DRP. Each section has a purpose — include it when relevant, skip it when it adds no value (but note which sections you skipped and why).

> **SCP context**: PRD này áp dụng cho 13 domain SCP (master-data, demand, supply-inventory, drp-engine, order-planning, simulation, daily-replan, transport, exception, analytics, shared-kernel, integration, admin). Mọi PRD by-module phải align với canonical `docs/prd/SCP-DRP-SPEC-SYSTEM-FINAL/` — drift → Open Question, không silent-diverge.

---

## Writing Quality Standard

PRD items follow **two distinct standards** — do not mix them:

| Standard | Áp dụng cho | Quy chiếu |
|---|---|---|
| **Spec-tight** (below) | Business Rules, Acceptance Criteria, Validation Rules | This section |
| **Story-loose** | User Stories | Section 3 — "User Story Writing Style" |

The Spec-tight standard below applies to **BR / AC / VR only**. Applying it to User Stories turns stories into mini-specs (field lists, entity names, UI mechanics) and destroys their job-to-be-done framing. See section 3 for the US-specific standard and Before/After examples.

### Each BR / AC / VR is a complete, self-contained sentence

A reader new to the feature must be able to read a single row and understand the rule **without** scanning the surrounding section. Each item must contain:

1. **Subject** — who or what the rule applies to (persona, entity, list, dialog, system component)
2. **Action / condition** — what the system enforces, what the user does, or the precondition that triggers the rule
3. **Constraint / outcome** — the specific boundary, threshold, allowed values, or expected result. **Quantify whenever possible** (state numbers, dates, state names, role codes)
4. **Reason** — include the *why* whenever the constraint is not self-evident

### Anti-patterns — must be rewritten

- **Label-only rule**: writing a topic name in place of an actual rule. Examples observed in real PRDs: "Phân trang", "Sắp xếp mặc định", "Bộ lọc mặc định khi mở màn hình", "Empty state", "Validation". These are headlines, not rules. The Description column must hold the full rule statement, not the topic.
- **Missing subject**: "Chỉ thấy chuyến của nhà thầu được phân quyền" — who is the subject of "thấy"? Which user role? Visible where (list, search, count, API)?
- **Missing constraint / outcome**: "Cột Xe/Tài xế lấy từ Trip liên kết" — what shows when Trip is unassigned? When Trip is deleted? Display format?
- **Pronouns without antecedent**: "Họ chỉ xem được của mình", "Cái này áp dụng cho mọi trường hợp".
- **Vague qualifiers**: "phù hợp", "hợp lý", "đầy đủ", "tối ưu", "thân thiện" — replace with measurable criteria, lists of allowed values, or specific thresholds.
- **Single-noun fragments**: "Phân trang.", "Bulk action toolbar." — even when these appear alongside a name column, the Description must be a sentence.

### Before / After — using real examples observed in PRDs

| ❌ BAD (label / cụt lủn) | ✅ GOOD (complete sentence with subject + action + constraint) |
|---|---|
| "Phân trang" | "Danh sách Tendered Trip phân trang server-side, mặc định 25 dòng/trang. Hỗ trợ đổi page size sang 10/50/100. Hiển thị 'Showing X of Y' trong đó Y là tổng dòng match filter hiện tại." |
| "Sắp xếp mặc định" | "Khi mở màn hình lần đầu, list sort mặc định theo `tenderedAt DESC` (chuyến vừa được nhà thầu nhận gần nhất ở trên). User có thể đổi sort; lựa chọn này không persist giữa các session." |
| "Bộ lọc mặc định khi mở màn hình" | "Lần đầu Vendor mở màn hình, các filter mặc định được áp: `status = Tendered` và `tenderedAt ∈ [today − 7 ngày, today]`. User có thể clear hoặc đổi giá trị filter; thay đổi này không persist." |
| "Chỉ thấy chuyến của nhà thầu được phân quyền" | "User có role `Vendor` chỉ truy vấn được Trip có `assignedVendorId` = Vendor mà user đại diện. Trip của Vendor khác không xuất hiện trong list, search, count, hoặc bất kỳ aggregation nào trên màn hình. Quy tắc này áp dụng cả khi gọi API trực tiếp (data scope ở backend, không chỉ ẩn ở UI)." |
| "Cột Xe/Tài xế lấy từ Trip liên kết" | "Cột 'Xe' và 'Tài xế' trong list Tendered Trip hiển thị giá trị từ Trip cha (`Trip.vehicleCode`, `Trip.driverName`). Khi Trip cha chưa gán Xe hoặc Tài xế, cell hiển thị '—'. Khi Trip cha bị xóa, dòng Tendered Trip cũng được ẩn (xem BR-XX về cascade)." |
| "Checkbox chọn nhiều và điều kiện được chọn" | "List có cột checkbox đầu mỗi dòng để chọn nhiều TenderedTrip. Chỉ TenderedTrip ở `status = Tendered` mới được chọn; các status khác checkbox bị disable kèm tooltip lý do. Header có checkbox 'Select all' chỉ chọn các dòng đang ở trang hiện tại và đang ở status hợp lệ." |
| "Bulk action toolbar — điều kiện hiển thị và nội dung" | "Bulk action toolbar xuất hiện ở chân list khi user chọn ≥ 1 TenderedTrip. Toolbar hiển thị 'Đã chọn N chuyến', nút 'Accept' (chỉ enable khi mọi dòng chọn ở status Tendered), nút 'Reject' (cùng điều kiện), và nút 'Clear selection'. Toolbar tự ẩn khi không còn dòng nào được chọn." |
| "Thứ tự ưu tiên empty state" | "Khi list trả về 0 dòng, hệ thống hiển thị empty state theo thứ tự ưu tiên: (1) Nếu Vendor user chưa được gán Trip nào → '[Vendor name] chưa có chuyến tender'; (2) Nếu có filter đang áp → 'Không tìm thấy chuyến match filter — Clear filter để xem tất cả'; (3) Mặc định → 'Chưa có Tendered Trip'. Mỗi empty state có 1 CTA tương ứng." |

### Self-check before finalizing each row

For each BR / US / AC, ask:

1. Can someone read this row alone, without context, and understand it? If no → rewrite.
2. Are subject + action + constraint all present? Each missing element = rewrite.
3. Are there numbers, states, or thresholds I should have quantified? If yes → quantify.
4. Did I write a topic name instead of a rule (e.g., "Phân trang", "Validation")? → expand into a full sentence.
5. Could two reasonable readers interpret this row differently? If yes → tighten the wording.

If a BR/AC/VR row is shorter than ~12 words and contains no number, persona, state name, entity reference, or specific verb, it almost certainly fails this standard.

> **This length/quantification rule applies to BR / AC / VR only — NOT to User Stories.** A US can (and often should) be short, free of state names, and free of entity references. See section 3 for the US-specific standard.

---

## Mandatory Sections

### 1. Overview

Set the context in 3–5 sentences:
- **Problem**: What pain point or gap exists today?
- **Solution**: What does this feature do at a high level?
- **Target users**: Which personas benefit?
- **Goals**: What measurable outcome do we expect?

Also include metadata:

```markdown
**Module**: [module name]
**Complexity**: Simple | Medium | Complex
**Primary persona**: [persona name]
```

### 2. User Personas

For each persona involved, describe:
- Role name and brief description
- What they need from this feature
- How often they interact with it (daily/weekly/ad-hoc)

Only list personas relevant to THIS feature — don't repeat the full persona catalog.

### 3. User Stories

Format:
```
**US-{nn}**: As a [persona], I want [goal], So that [benefit].
```

Each story should be **INVEST**:
- **Independent**: Can be delivered on its own
- **Valuable**: Delivers user-visible benefit
- **Testable**: Has clear acceptance criteria

#### User Story Writing Style (story-loose — KHÁC với BR/AC/VR)

User Story là **câu chuyện về nhu cầu**, không phải mô tả màn hình. Standard "complete sentence with subject + action + constraint + quantify" ở phần "Writing Quality Standard" trên cùng **KHÔNG áp dụng cho US**. Một US có thể (và thường nên) ngắn, không có state name, không có entity reference, không có field list.

**Anatomy của một US tốt:**

| Phần | Là gì | KHÔNG phải là gì |
|---|---|---|
| `As a [persona]` | Vai trò + bối cảnh nghề nghiệp (ví dụ "Vendor Dispatcher đang quản 5 nhà xe") | "User", "System user", role code |
| `I want [goal]` | KẾT QUẢ user muốn đạt được (job-to-be-done) | Field list, entity name kỹ thuật, UI mechanism, filter combo |
| `So that [benefit]` | Lợi ích nghề / business — trả lời "vì sao điều này quan trọng với job của tôi" | Lặp lại nội dung "I want" bằng từ khác |

**5 nguyên tắc bắt buộc cho US:**

1. **Voice của user, không phải voice của developer.** Viết như user đang nói với đồng nghiệp, không phải spec gửi dev.
2. **Một US = một nhu cầu.** Nếu phải dùng dấu phẩy liệt kê field / filter / status thì US đang ôm nhiều việc — tách thành nhiều US, hoặc đẩy detail xuống AC / Wireframe.
3. **Không tên entity kỹ thuật trong US** — dùng từ nghiệp vụ tự nhiên.
   - ❌ "TenderedTrip" → ✅ "chuyến nhà thầu nhận"
   - ❌ "OrderLine" → ✅ "dòng hàng trong đơn"
   - ❌ "BusinessPartner" → ✅ "khách hàng" / "nhà cung cấp" / "đối tác"
4. **Không liệt kê field, status name, filter list** trong "I want". Field thuộc Data Model; status name thuộc State Machine; filter list thuộc Wireframe + AC.
5. **Benefit phải nói về business outcome**, không lặp what.
   - ❌ "So that tôi xem được danh sách" (lặp what)
   - ✅ "So that tôi biết hôm nay có bao nhiêu việc và sắp xếp tài/xe kịp giờ"

#### Before / After — US screen-spec → US user-voice

Tất cả ví dụ "BAD" dưới đây xuất phát từ PRD thực tế của dự án — đây là dạng drift cần tránh.

| ❌ BAD — screen spec disguised as story | ✅ GOOD — user voice |
|---|---|
| As a Vendor Dispatcher, I want xem danh sách tất cả **TenderedTrip** đã được giao cho công ty tôi, kèm thông tin **ETD/ETA, số đơn, tổng tải trọng, và trạng thái**, So that tôi nắm được toàn bộ khối lượng công việc cần xử lý và ưu tiên phân bổ nguồn lực. | As a Vendor Dispatcher, I want thấy hết chuyến mà khách giao cho bên tôi xử lý hôm nay, So that tôi biết phải sắp xếp bao nhiêu tài/xe và bắt đầu công việc đúng giờ. |
| As a Vendor Dispatcher, I want xem thống kê tổng số chuyến theo từng trạng thái (**Tổng / Chờ xử lý / Đã tạo chuyến**) ngay trên đầu danh sách, So that tôi có cái nhìn tổng quan về tình trạng vận hành. | As a Vendor Dispatcher, I want biết ngay còn bao nhiêu chuyến chưa xử lý, So that tôi không bỏ sót chuyến nào tới sát deadline mới phát hiện. |
| As a Vendor Dispatcher, I want lọc danh sách theo **trạng thái, khoảng thời gian ETD, khoảng thời gian ETA, Sold To, điểm lấy hàng, và điểm giao hàng**, So that tôi nhanh chóng tìm được các chuyến cần xử lý ngay. | As a Vendor Dispatcher, I want lọc nhanh các chuyến cần xử lý ngay, So that tôi không phải lướt qua các chuyến chưa tới lượt khi đầu ca có hàng chục chuyến cùng đổ về. |
| As a Vendor Dispatcher, I want tìm kiếm chuyến **theo mã chuyến**, So that tôi tra cứu nhanh một chuyến cụ thể. | As a Vendor Dispatcher, I want tra cứu nhanh một chuyến khi khách hoặc tài xế gọi hỏi về nó, So that tôi trả lời được trong vài giây thay vì để họ phải chờ. |
| As an Operator, I want tạo Order với các field **customerCode, pickupAddress, deliveryAddress, weight (kg), volume (m³), pickupDate, deliveryDate**, So that hệ thống lưu được đơn. | As an Operator, I want nhập đơn hàng mới từ yêu cầu của khách, So that bộ phận điều phối có thể bắt đầu lên kế hoạch xe ngay trong ngày. |

**Pattern dấu hiệu** — nếu US có ≥1 dấu hiệu sau, gần chắc nó là screen-spec chứ không phải story:

- Liệt kê field bằng dấu phẩy hoặc dấu gạch nghiêng (`/`)
- Có tên entity viết hoa kiểu PascalCase (TenderedTrip, OrderLine, BusinessPartner)
- Mô tả vị trí UI ("trên đầu danh sách", "ở sidebar", "trong dialog")
- Liệt kê tên status / trạng thái cụ thể
- "So that…" chỉ lặp lại "I want…" bằng từ khác
- Câu dài >40 từ trong phần "I want"

**Tự kiểm tra trước khi finalize từng US:**

1. Đọc US cho một BA mới (không biết feature) — họ hiểu user đang muốn **giải quyết vấn đề gì** không? Không phải "user muốn thấy gì trên màn hình".
2. Câu "So that…" có nói về **nghề / business outcome** không, hay chỉ lặp what?
3. Có tên entity kỹ thuật, field, status, hoặc filter list trong US không? → Có = sai chỗ. Đẩy detail vào Wireframe / Data Model / AC.
4. Nếu xóa US này, có một US khác trong cùng group bị mất nhu cầu không? → Không = US trùng, cần merge.
5. Một dev đọc US có viết được Given/When/Then AC không? (Không cần "code được ngay" — chỉ cần viết AC.) AC mới là nơi chứa detail.

#### Phân công nội dung — US vs Wireframe vs Data Model vs AC

Khi viết PRD, mỗi loại thông tin có chỗ riêng. Không nhồi mọi thứ vào US:

| Nội dung | Thuộc về |
|---|---|
| Nhu cầu của user, lý do nghề nghiệp | **US** |
| Field nào hiển thị, vị trí trên màn hình, layout | **Wireframe** |
| Tên field chính xác + type + required | **Data Model (section 10)** |
| Status name, state transitions | **State Machine (section 8)** |
| Filter combinations cụ thể, sort default, page size | **UI/UX Notes (section 12)** + **AC (section 5)** |
| Điều kiện testable Given/When/Then | **AC (section 5)** |
| Quy tắc hệ thống enforce (uniqueness, format, scope) | **BR (section 4)** |

#### Grouping (mandatory) — MECE

Stories MUST be presented under sub-headings that group related items together. The grouping taxonomy is **chosen for THIS feature** — there is no fixed list of groups. Pick the dimension that makes the structure clearest:

- by **persona** (Operator stories / Manager stories / Admin stories) when multiple roles use the feature
- by **workflow phase** (Submission → Review → Approval → Execution) when the feature is a process
- by **action** (Create / Search / Update / Delete / Import-Export) when the feature is CRUD-heavy
- by **screen / sub-feature** (Login screen / Home screen / Trip detail screen) when the feature is a multi-screen app
- by **domain concept** (Pricing stories / Capacity stories / Routing stories) for domain-rich features

Example structure:

```markdown
## User Stories

### Group A — [chosen group label, e.g. "Operator — Daily order entry"]
**US-01**: As an Operator, I want ...
**US-02**: As an Operator, I want ...

### Group B — [chosen group label, e.g. "Manager — Oversight"]
**US-03**: As a Manager, I want ...
```

#### MECE checklist (apply before finalizing User Stories)

1. **No overlap** — for each pair within the same group, can you state a clear difference? If not, merge.
2. **No gap** — for each persona × workflow phase listed in the Personas section, is there at least one US? Missing combinations must be marked "out of scope" in section 15.
3. **Same granularity** — items inside one group are at the same level of detail. Don't put a fine-grained "filter by date" story next to an umbrella "manage all orders" story.
4. **Independently testable** — each US has at least one AC; if you cannot write an AC, the US is too vague or bundles multiple stories.

### 4. Business Rules

Numbered rules that govern the feature's behavior:

```markdown
| # | Rule | Description |
|---|------|-------------|
| BR-01 | Rule name | What the system must enforce and why |
```

Business rules are things like:
- "A shipment cannot be marked as Delivered without a POD (Proof of Delivery) document"
- "Customs declaration must be submitted at least 24 hours before vessel arrival"
- "Container demurrage charges start accruing after 5 free days"

Avoid encoding technical implementation in business rules — focus on the **what** and **why**.

#### What belongs here vs in UI/UX Notes

Business Rules and UI/UX Notes are routinely confused. The split is:

- **BR = WHAT the system enforces, regardless of UI.** Survives a UI redesign. Enforced even when the rule is hit via API / import / batch job. Violation risks data integrity, money, legal/audit, or business correctness.
- **UX = HOW the user experiences a specific screen.** Disappears or changes if the screen is rebuilt. Violation just feels awkward, not damaging.

**Litmus test** — apply per sentence before deciding which section to put it in:

1. If a developer triggers this rule via API/import/automation (not the UI), does the rule still apply? — **Yes → BR**, No → UX.
2. If the screen is fully redesigned tomorrow, does this still hold? — **Yes → BR**, No → UX.
3. Does breaking it risk data integrity / money / legal / business correctness, or just feel awkward? — **Risk → BR**, Awkward → UX.

**Side-by-side examples:**

| Topic | ✅ Business Rule (section 4) | ✅ UI/UX Note (section 12) |
|-------|------------------------------|----------------------------|
| Uniqueness | "Order code must be unique within the tenant" | "Inline error displayed under the input as the user types a duplicate" |
| Default value | "On create, Order.status defaults to Draft" (domain invariant) | "Pre-fill 'Delivery date' with today + 1" (input convenience only) |
| Required field | "Customer is mandatory before confirming an Order" | "Show red `*` next to the label" |
| Date constraint | "deliveryDate must be after pickupDate" | Error wording "Ngày giao phải sau ngày lấy hàng" |
| State immutability | "Cancelled Order is read-only" | "Hide the Edit button when status = Cancelled (or disable + tooltip)" |
| Soft delete | "Delete is soft delete; sets `deletedAt`" | "Confirm dialog 'Bạn có chắc...' before deleting" |
| Sort order | "Trips are processed FIFO by creation date" (if it is a real domain rule) | "Default list sort = Updated date desc" (presentation default only) |
| Pagination | (Not a BR) | "Default page size 25, options 10/25/50/100" |
| Permission | "Operator can only see Orders of their own branch" (data scope — backend-enforced) | "Hide the 'Manage all branches' menu for Operator" (UI expression of the BR) |
| Validation message | (Not a BR) | "Show toast 'Đã lưu' on successful save" |

**Common mistakes — these are UX, NOT BR:**

- ❌ "Save button is disabled until the form is valid" — UX. The BRs are the individual validation rules.
- ❌ "On clicking Confirm, show a confirmation dialog" — UX. The BR is what Confirm does to data.
- ❌ "Search results paginate at 25 per page" — UX, place under UI/UX Notes.
- ❌ "Use a drawer instead of a navigate to detail page" — UX, never a BR.

**Gray-zone handling:**

- **Permission- or state-driven UI behavior** is usually a UX **expression** of an underlying BR. Write the BR first ("Cancelled Order = read-only"); the UX note may reference it ("Hide Edit per BR-12").
- **Default value**: if it is a domain invariant ("status defaults to Draft on create") → BR. If it is just input convenience ("pre-fill date with tomorrow") → UX.
- **Validation**: the rule itself ("must be unique", "must be > 0") → BR (or VR in section 10b). The wording of the error message → UX (it's user-facing copy).
- **Search / filter / export capabilities** are **User Stories** (section 3), not BRs and not UX notes.

**When in doubt, put it in BR.** UI/UX Notes must never contain data invariants, validation logic, state transitions, or permission/data-scope rules.

#### Grouping (mandatory) — MECE

Business Rules MUST be presented under sub-headings that group related rules together. The grouping taxonomy is **chosen for THIS feature** — there is no fixed list of groups. Examples of groupings that may apply (use what makes sense for the feature):

- by **domain concept** (Identity & uniqueness / Pricing / Capacity / Routing / Approval)
- by **entity** (Order rules / Trip rules / Driver rules) when the feature spans multiple entities
- by **lifecycle phase** (Creation rules / Activation rules / Cancellation rules) when state transitions dominate
- by **rule kind** (Validation / Calculation / Authorization / Notification trigger) when the feature is rule-heavy
- by **scenario** (Domestic shipments / Cross-border shipments) when the same rule space splits along a clear axis

Each group becomes a sub-heading with its own table. Example structure:

```markdown
## Business Rules

### Group A — [chosen group label, e.g. "Order identity & uniqueness"]
| # | Rule | Description |
|---|------|-------------|
| BR-01 | Order code format | ... |
| BR-02 | Order code uniqueness | ... |

### Group B — [chosen group label, e.g. "Pricing & charges"]
| # | Rule | Description |
|---|------|-------------|
| BR-03 | Base freight calculation | ... |
| BR-04 | Surcharge application order | ... |
```

#### MECE checklist (apply before finalizing Business Rules)

1. **No overlap** — for each pair of BRs in the same group, can you state a clear difference? If two rules say the same thing under different words, merge them. If they restrict the same field from different angles, consider whether to consolidate or split into a third rule.
2. **No gap** — every business constraint mentioned in the Overview, Personas, or stakeholder discussion must map to at least one BR. Walk through each persona's main actions and check that each constraint they hit is covered.
3. **Same granularity** — items inside one group are at the same level of detail. Avoid mixing one fine-grained constraint ("max length 50") with a coarse umbrella rule ("all validations follow company standard") — the umbrella rule must be expanded.
4. **Independently testable** — each BR has at least one Acceptance Criterion. If you cannot write an AC for a BR, it is either too vague or it bundles multiple rules.
5. **Coverage map (optional but recommended for complex features)** — list the entities × actions (Create/Read/Update/Delete/State-transition) and confirm at least one BR covers each non-trivial cell, or mark explicitly "no rule needed".

### 5. Acceptance Criteria

Testable conditions using Given/When/Then:

```markdown
| AC | Given | When | Then |
|----|-------|------|------|
| AC-01 | [precondition] | [action] | [expected result] |
```

Every user story should have at least one acceptance criterion. Complex stories may have several.

### 6. Wireframes

Reference to the wireframes file:
```markdown
> See [wireframes.md](wireframes.md) for detailed screen designs.
```

If wireframes were skipped, state why:
```markdown
> Wireframes skipped — feature is API-only with no new UI screens.
```

---

## Conditional Sections (include when applicable)

### 7. Research Findings (when research was conducted)

Structure:
```markdown
### Competitor Benchmark

| Aspect | SAP IBP | Kinaxis | o9 | Smartlog SCP Decision |
|--------|---------|---------|----|-----------------------|
| ...    | ...     | ...     | ...| ...                   |

### Key Insights
1. Insight that changed our approach
2. Another insight
```

### 8. State Machine (when entities have lifecycle)

If the feature introduces or modifies an entity with distinct states (e.g., Booking: Draft → Confirmed → In Transit → Completed → Cancelled):

```markdown
## State Machine

### [Entity Name] Lifecycle

[State A] → [State B] → [State C]
              ↘ [State D] (exceptional path)

| From | To | Trigger | Who can trigger | Notes |
|------|----|---------|-----------------|-------|
| Draft | Confirmed | User submits | Operator | Validates required fields |
```

Include:
- Visual flow (text-based diagram)
- Transition table with triggers
- Who has permission to trigger each transition (persona level, not technical permission codes)

### 9. Notifications (when the feature triggers alerts)

```markdown
| Event | Channel | Recipient | Message summary |
|-------|---------|-----------|-----------------|
| Shipment delayed | Email + In-app | Shipper, Consignee | "Shipment {code} delayed. New ETA: {date}" |
```

### 10. Data Model & Validation (when the feature introduces or modifies entities)

Describe the business-level data structure and validation rules. This is NOT a database schema — it is a product-level description of what data the system manages, what constraints apply, and how entities relate to each other.

#### 10a. Data Model

List each entity this feature introduces or significantly modifies:

```markdown
### [Entity Name]

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| code | Text | Yes | Unique identifier, auto-generated or user-entered |
| name | Text | Yes | Display name |
| status | Enum | Yes | Draft, Active, Inactive |
| category | Ref → [Entity] | No | Link to parent category |
| weight | Number (kg) | Conditional | Required when vehicle type is "Truck" |
| attachments | File[] | No | Max 5 files, max 10MB each |
```

Guidelines:
- **Type** uses business language: Text, Number, Date, DateTime, Enum, Boolean, Ref → [Entity], File, File[], Coordinate (lat/lng), etc.
- **Required** can be: Yes, No, or Conditional (with condition described in Description)
- For Enum fields, list all valid values
- For Ref fields, specify which entity it references
- Include computed/derived fields if they are visible to the user (e.g., "Total Weight = sum of order line weights")
- Do NOT specify database column names, data types (varchar, int), or index strategies — those are dev decisions

**Cross-reference rules for Ref → [Entity]:**
- If the referenced entity already has a PRD in `docs/prd/`, write: `Ref → Business Partner` (no warning needed)
- If the referenced entity does NOT have a PRD yet, write: `Ref → Vehicle Type (⚠️ chưa có PRD — cần tạo tại docs/prd/{module}/{slug}/)`
- NEVER redefine fields that belong to an existing entity — use `Ref →` to reference it. For example, if you need customer info and Business Partner PRD already exists, use `Ref → Business Partner` instead of adding `customerName`, `customerPhone`, `customerAddress` fields
- When referencing an entity's enum/status values (e.g., partnerType: Customer|Carrier from Business Partner), cite the source: "Giá trị theo định nghĩa tại Business Partner PRD"

**Module Consumers (mandatory for `master-data` và `shared-kernel` domain):**

When this PRD belongs to the `master-data` or `shared-kernel` domain, include a consumer mapping table showing which other 13 SCP domains will use the entity:

```markdown
| Entity | Consuming Domain | Feature/Use Case | Notes |
|--------|------------------|-------------------|-------|
| Business Partner | demand | Forecast aggregation by Customer | Filter forecast theo customer tier |
| Business Partner | order-planning | SO Plan / SO con → customerRef | Required for order creation |
| Business Partner | drp-engine | Allocation priority by customer tier | Allocation L3 ordering |
| Business Partner | transport | Multi-drop → carrierRef | Required for dispatching |
```

This table answers: "If I change this master-data/shared-kernel entity, which SCP domains are affected?" — critical for impact analysis during development.

#### 10b. Validation Rules

**IMPORTANT**: Reference [field-validation-patterns.md](field-validation-patterns.md) (cùng skill) for standard constraints per field type. When the data model includes common field types (Name, Code, Email, Phone, Date, Amount, etc.), copy the applicable constraints from that file into the validation rules table. This ensures consistency across all PRDs.

List the validation rules that the system must enforce when creating or editing entities:

```markdown
| # | Field(s) | Rule | Error message (user-facing) |
|---|----------|------|-----------------------------|
| VR-01 | code | Must be unique within the system. Pattern: ^[A-Z0-9_-]+$, max 20 chars (per field-validation-patterns) | "Mã {entity} đã tồn tại" |
| VR-02 | weight | Must be > 0 when provided | "Trọng lượng phải lớn hơn 0" |
| VR-03 | pickupDate, deliveryDate | deliveryDate must be after pickupDate | "Ngày giao phải sau ngày lấy hàng" |
| VR-04 | email | Must be valid email format, max 200 chars (per field-validation-patterns) | "Email không đúng định dạng" |
```

Guidelines:
- For standard field types (Name, Code, Email, Phone, Date, Amount, etc.), include constraints from `field-validation-patterns.md` (max length, format pattern, normalization rules)
- Cross-field validations are important — list them explicitly (see section 10 "Cross-Field Validation Summary" in field-validation-patterns.md)
- Include the user-facing error message in Vietnamese (có dấu) — this helps both QA and frontend teams
- If validation differs by state (e.g., Draft allows partial data, Confirmed requires all fields), note which validations apply at which state

#### 10c. Entity Relationships (when there are 2+ entities)

Describe how entities relate to each other:

```markdown
| From | To | Relationship | Description |
|------|----|-------------|-------------|
| Order | OrderLine | 1:N | One order has many lines |
| Order | Customer | N:1 | Many orders belong to one customer |
| Trip | Order | N:N | One trip can carry multiple orders; one order can be split across trips |
```

Include a simple text diagram for complex relationships:

```
Customer (1) ──── (N) Order (1) ──── (N) OrderLine
                        │
                       (N:N)
                        │
                      Trip (N) ──── (1) Vehicle
                                    (1) Driver
```

### 10d. Permission Matrix (when the feature has user-facing operations)

Define who can perform what operations on the feature's entities. This is a business-level authorization table — use persona names (not technical permission codes) so stakeholders can review it.

**Include this section when:**
- The feature introduces CRUD operations on entities
- Different user roles should have different access levels
- Some operations should be restricted (e.g., only managers can delete)
- Data visibility differs by role (e.g., "see own records" vs "see all")

**Skip when:**
- Background/system-only feature with no user-facing operations
- All authenticated users have identical access

```markdown
### Permission Matrix

| Operation | Persona | Data Scope | Notes |
|-----------|---------|------------|-------|
| View list | Operator, Manager | Operator: own branch only. Manager: all branches | Default landing page for both |
| View detail | Operator, Manager | Same as list | |
| Create | Operator | Own branch | Auto-assigns to creator's branch |
| Update | Operator, Manager | Operator: own records. Manager: all in org | Manager can reassign between branches |
| Delete | Manager | All in org | Soft delete — requires confirmation dialog |
| Export | Manager | All in org | CSV/Excel export of filtered list |
| Import | Manager | Own org | Bulk import from Excel template |
| Approve | Manager | All in org | Only applicable when status = Pending Approval |
```

Guidelines:
- **Operation**: Use plain verbs — View list, View detail, Create, Update, Delete, Export, Import, Approve, Submit, Cancel, etc.
- **Persona**: Use persona names from the User Personas section (not role names or permission codes)
- **Data Scope**: Describe what subset of data this persona can see/act on — "all", "own branch", "own records", "assigned to me"
- **Notes**: Conditions, restrictions, or special behavior
- If an operation should trigger a state transition (e.g., Approve moves status from Pending → Active), cross-reference the State Machine section
- Do NOT write technical permission codes (`Feature__Action`) — that's for the downstream db-architect/dev team to define based on this business intent. Đối chiếu canonical `P05-SCP-RBAC-spec.md` (6×18 matrix) khi map persona ↔ operation

### 11. Configurable Parameters (when rules vary by client)

```markdown
| Parameter | Default | Why configurable |
|-----------|---------|-----------------|
| Free days before demurrage | 5 days | Varies by port/carrier agreement |
| Auto-close booking after | 30 days | Different clients have different SLAs |
```

Don't specify the config mechanism (DB config vs app config vs feature flag) — that's a technical decision for the dev team.

### 12. UI/UX Notes

Behavioral guidance for the frontend team:
- How search/filter should work
- What happens on empty states
- Loading states and error handling from user perspective
- i18n keys if applicable

**Do NOT put the following here — they belong in Business Rules (section 4) or Validation Rules (section 10b):**

- Data invariants and defaults that are domain-mandated (e.g., "status defaults to Draft on create")
- Validation logic ("must be unique", "must be > 0", "deliveryDate after pickupDate")
- State transitions and immutability rules ("Cancelled orders cannot be edited")
- Permission and data-scope rules ("Operator only sees own branch records")
- Calculations and derived values ("Total = sum of line amounts")

UI/UX Notes describe **how** the user experiences a screen — disable/hide patterns, dialog vs. page choice, confirm prompts, toast wording, default sort/page-size, focus order, empty-state visuals, loading indicators, error-message copy. If a sentence would still apply when the rule is hit via API/import (no UI involved), it is a Business Rule, not a UI/UX Note. See section 4 "What belongs here vs in UI/UX Notes" for the full litmus test and side-by-side examples.

When a UX behavior is the screen's **expression** of an underlying BR (e.g., hiding the Edit button because "Cancelled is read-only"), write the BR in section 4 first, then reference it here ("Hide Edit per BR-12") rather than restating the rule.

### 13. Non-functional Requirements (when relevant)

High-level expectations only — no performance tier tables or SLA numbers unless the user provides them:
- Expected data volume (e.g., "~10,000 shipments/month per tenant")
- Concurrency concerns (e.g., "Multiple operators may update the same booking simultaneously")
- Offline/degraded mode needs

### 14. Dependencies

What must exist before this feature can be built. Classify each dependency:

```markdown
### Entity Dependencies

| Entity | PRD Status | Path | Blocking? |
|--------|-----------|------|-----------|
| Business Partner | ✅ PRD exists | `docs/prd/by-module/master-data/00X-business-partner/PRD-MD-00X-*.md` | No |
| Vehicle Type | ⚠️ No PRD yet | — | Yes — need PRD before dev |
```

Also list:
- Other features or modules (beyond entity references)
- External integrations
- Data that must be seeded

### 15. Out of Scope

Explicitly list what this PRD does NOT cover. This prevents scope creep and sets expectations:
```markdown
- Mobile app support (Phase 2)
- Integration with SAP ERP (separate feature)
- Automated rate negotiation (future enhancement)
```

### 16. Open Questions

Unresolved decisions that need stakeholder input:

```markdown
| # | Question | Impact | Owner |
|---|----------|--------|-------|
| OQ-01 | Should we support partial delivery? | Affects state machine and UI | Product Owner |
```

---

## Writing Style

- Write in Vietnamese (có dấu) for descriptions, business rules, and UI copy
- Use English for technical terms that don't have good Vietnamese translations (e.g., "shipment", "ETA", "POD", "container")
- Be specific — "User can filter shipments by status, origin port, and date range" is better than "User can filter shipments"
- Each business rule should be testable — if you can't write an acceptance criterion for it, it's too vague
