# Workflow — 3 chế độ chi tiết

Skill `ba-scp-prd` gộp 3 chế độ trên cùng artifact. Đây là quy trình chi tiết cho từng mode.

## Mode 1 — Author (viết PRD mới)

### Khi nào dùng
- User mô tả feature mới chưa có folder trong `docs/prd/by-module/`.
- User reference Master canonical và yêu cầu "viết PRD cho [feature X]".
- User nói "tạo PRD cho [feature]", "spec [feature]", "phân tích yêu cầu [feature]".

### Quy trình

1. **Hiểu request** — feature gì, persona ai, domain SCP nào.
2. **Xác định domain + numbering** — match vào 1 trong 13 domain, scan `docs/prd/by-module/{domain}/` lấy NNN tiếp theo.
3. **Load canonical context (BẮT BUỘC)**:
   - `SCP-DRP-Strategic-PRD.md` — WHY/WHAT/KPI/phasing.
   - `domains/{domain-folder}/F0X-*.md` — spec canonical domain.
   - `cross-cutting/P01-SCP-SharedKernel-spec.md` — canonical ERD.
   - `cross-cutting/P07-SCP-Glossary-spec.md` — terminology.
   - Customer overlay nếu feature có scope per customer.
4. **Hỏi research** — competitor (SAP IBP / Kinaxis / o9 / Blue Yonder) cần thiết không?
5. **Entity Registry detection** — scan `docs/prd/by-module/*/` + canonical `F01a` để build registry. Cross-reference rule (xem SKILL.md §"Bước 5").
6. **Viết PRD** từ `templates/prd.md`, follow `references/prd-format.md`.
7. **Viết Wireframes** nếu cần (auto-detect rule trong SKILL.md §"Bước 7").
8. **Self-review** theo "Developer-Ready Checklist" (xem cuối file).
9. **Output ending signals**.

### Validation gates

Trước khi tuyên bố "ready_for_dev = true":

- [ ] Mọi BR/AC/VR đầy đủ Subject + Action + Constraint (spec-tight).
- [ ] Mọi US là job-to-be-done (story-loose, không liệt kê field).
- [ ] MECE checklist passed cho cả BR và US.
- [ ] Mọi entity referenced có path PRD (✅) hoặc flag ⚠️ blocking.
- [ ] State machine vẽ rõ nếu entity có lifecycle.
- [ ] Permission matrix align canonical `P05`.
- [ ] Configurable Parameters đối chiếu canonical `P06` Config Registry.
- [ ] Customer Variants section nếu feature có overlay impact.
- [ ] Version History entry `1.0` đã ghi.

---

## Mode 2 — Breakdown (tách Master ra)

Mode phức tạp nhất. Đọc kỹ [master-prd-breakdown.md](master-prd-breakdown.md) để biết quy trình tách chi tiết.

### Khi nào dùng
- User đưa file Master và nói "tách ra", "break down", "chia nhỏ".
- User cần convert `PRD_v4_1_2_SSoT_FINAL.md` thành nhiều PRD by-module.
- User cần convert `SCP-DRP-Strategic-PRD.md` thành PRD chi tiết per domain.

### Quy trình tóm tắt

1. **Read Master end-to-end** — không skim. Note inline mọi entity, BR, US, state machine bắt gặp.
2. **Build domain map** — phân loại từng section/BR/US vào 1 trong 13 domain. Section nào cross-domain → ghi nhận, sẽ split sau.
3. **Create folder structure** — với mỗi domain có ≥ 1 item, tạo `docs/prd/by-module/{domain}/{NNN}-{feature-slug}/`.
4. **Extract per-domain content**:
   - PRD chính: overview + personas + US + BR + state machine + data model + ...
   - BR Catalog (nếu domain có ≥ 30 BR).
   - US Catalog (nếu domain có ≥ 20 US).
   - Wireframes nếu Master có spec UI cho domain đó.
5. **Cross-reference cleanup**:
   - Entity dùng cross-domain → reference PRD của domain owner, không re-define.
   - BR depend BR khác domain → ghi rõ "Depends on BR-XX-NNN" trong dependency section.
6. **Traceability map** — bảng map mỗi PRD-by-module ID ← Master section ID. Ghi vào `## Traceability` của PRD và tổng hợp ở root traceability file nếu user yêu cầu.
7. **Customer variant split**:
   - Behavior chung → đưa vào PRD chính.
   - Behavior per-customer → reference `customer-variants/{X}-Overlay.md`, không copy.
8. **Self-review** từng PRD theo "Developer-Ready Checklist".
9. **Output summary table** — list tất cả file đã tạo + thống kê (số BR, US per domain).

### Output cho mỗi domain

| File | Mandatory? | Nội dung |
|------|-----------|----------|
| `PRD-{PFX}-{NNN}-{slug}.md` | Yes | Overview, personas, US, BR, state machine, data model, AC, … |
| `WF-{PFX}-{NNN}-{slug}.md` | If UI present | ASCII wireframes |
| `BR-CATALOG-{PFX}-{NNN}.md` | If BR ≥ 30 | Bảng tổng hợp BR, group, dependency, customer matrix |
| `US-CATALOG-{PFX}-{NNN}.md` | If US ≥ 20 | Bảng tổng hợp US, persona × phase coverage matrix |

---

## Mode 3 — Analyze & Update (cập nhật PRD đã có)

### Khi nào dùng
- User chỉ vào PRD cụ thể và nói "sửa BR-XX", "thêm AC", "đổi flow".
- User đưa change request và yêu cầu áp dụng vào PRD by-module hiện có.
- User feedback từ review (ai cũng được — dev, QA, PO) và cần phản ánh vào PRD.

### Quy trình

1. **Read PRD hiện tại** — toàn bộ, không skim. Note `## Version History` để biết version hiện tại.
2. **Parse change request** — phân loại từng request:
   - **Minor**: sửa wording BR, thêm 1-2 AC, cập nhật WF layout, thêm 1 validation rule.
   - **Major**: thêm/bỏ US, đổi state machine, đổi data model cấu trúc, đổi permission matrix scope.
3. **Đối chiếu canonical** — nếu request mâu thuẫn `SCP-DRP-SPEC-SYSTEM-FINAL`, **dừng và flag** Open Question. Không silent-override canonical.
4. **Đối chiếu entity registry** — nếu request thêm field/entity, scan cross-domain xem đã có chưa.
5. **Apply changes** — chỉ touch section relevant, không rewrite phần không liên quan (surgical).
6. **Track impacted IDs** — liệt kê BR-xx, AC-xx, US-xx, WF-xx, VR-xx đã thay đổi.
7. **Determine version bump**:
   - Chỉ minor changes → bump minor (1.1 → 1.2).
   - Có major change → bump major (1.x → 2.0).
8. **Append Version History entry** — KHÔNG mỗi edit thêm 1 entry. Cuối phiên thêm 1 entry duy nhất tóm tắt mọi thay đổi.
9. **Re-validate** — chạy lại MECE + Developer-Ready Checklist trên PRD đã sửa.
10. **Output diff summary** — liệt kê section thay đổi, version bump, IDs impacted.

### Cẩn trọng

- **Không xóa BR/US legacy mà không có Open Question đi kèm** — luôn đợi user confirm trước khi delete.
- **Không reset version** — chỉ bump theo lịch sử thực tế.
- **State machine change = major bump** kể cả khi chỉ thêm 1 transition (có downstream impact lớn).
- **Permission matrix change** = check canonical `P05` RBAC matrix trước. Nếu drift, flag OQ.

### Detect existing version

Khi update file:
1. Read PRD.
2. Check `## Version History` section.
3. Có → đọc version mới nhất → bump theo rule.
4. Không có (legacy file) → thêm section ở cuối, version khởi đầu `1.1` (vì file đã có content trước), không phải `1.0`.

---

## Developer-Ready Checklist (chung cho cả 3 mode)

Trước khi tuyên bố PRD "READY_FOR_DEV = true":

### Structure
- [ ] Có đủ section bắt buộc: Overview, Personas, US, BR, AC, Data Model, Permission Matrix, Version History.
- [ ] Section conditional có/không theo applicability (State Machine, WF, Notifications, Config, Customer Variants).
- [ ] H1 + metadata table đầu file.

### Content quality
- [ ] BR spec-tight: mỗi rule là câu đầy đủ, không label-only.
- [ ] US story-loose: voice của user, không liệt kê field.
- [ ] MECE: BR và US group hợp lý, không trùng, không gap, same granularity.
- [ ] Mọi BR map ≥ 1 AC; mọi US map ≥ 1 AC.
- [ ] Validation rule có user-facing error message tiếng Việt có dấu.
- [ ] Cross-entity ref đúng quy tắc (Ref → Entity (PRD-XX-NNN) hoặc ⚠️ flag).

### Canonical alignment
- [ ] PRD reference canonical file (F0X / P0X) trong metadata.
- [ ] BR không mâu thuẫn canonical — nếu có, ghi Open Question.
- [ ] Terminology đồng nhất với `P07 Glossary`.
- [ ] Customer variant reference đúng overlay file.

### Traceability
- [ ] Có `## Traceability` table nếu PRD breakdown từ canonical.
- [ ] Mọi Open Question có owner.
- [ ] Dependency table phân ✅ ready vs ⚠️ blocking.

### Version
- [ ] `## Version History` là section cuối, có ≥ 1 entry.
- [ ] Version đúng quy tắc bump (minor/major).
