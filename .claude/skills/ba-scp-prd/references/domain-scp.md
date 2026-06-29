# Smartlog SCP/DRP — Domain Knowledge (project-specific)

Reference này chứa kiến thức nghiệp vụ ĐẶC THÙ cho dự án Smartlog SCP/DRP. Đọc file này sau `domain-supply-chain.md` (tổng quan) và `domain-supply-demand.md` (lý thuyết S&D Planning), nhưng TRƯỚC khi viết bất kỳ PRD nào — vì nó phản ánh các quyết định canonical đã chốt trong `SCP-DRP-SPEC-SYSTEM-FINAL`.

## Table of Contents
1. [13 Domains — boundaries & ownership](#13-domains)
2. [Master entities (Entity Registry)](#master-entities)
3. [6 Buckets — canonical inventory model](#6-buckets)
4. [Allocation Engine — 2-Phase 6-Layer](#allocation-engine)
5. [SO/TO Lifecycle](#soto-lifecycle)
6. [Daily Replan & Bitemporal](#daily-replan)
7. [Customer overlays — UNIS, TTC, MDLZ](#customer-overlays)
8. [17 canonical KPIs](#17-kpis)
9. [Common terminology VN↔EN](#terminology)

---

## 13 Domains — boundaries & ownership

| Domain | Prefix | Owns | Does NOT own |
|---|---|---|---|
| `master-data` | MD | 18 entities (Product, SKU, Location, BP, UoM, Tax, Currency, Vehicle Type, Delivery Zone, …) + Data Quality gates (16) | Transactional data (Order, Plan, Run) |
| `demand` | DM | AOP, S&OP cycle, PO Pending, Phasing, Forecast versioning, Forecast accuracy | Statistical method library (ML model) |
| `supply-inventory` | SI | 6 Buckets canonical, Safety Stock, Inventory Pipeline, On-hand/On-order/Reserved/Available calc | Physical movement (đó là WMS) |
| `drp-engine` | DE | Allocation Engine (2-phase 6-layer), Lot Sizing, DRP Run orchestration, Saga | Solver implementation (đó là dev) |
| `order-planning` | OP | SO/TO Lifecycle (Plan/con/exec), ProC Workflow, Cross-ORG handover, SO Plan → SO con derivation | OMS execution post-confirm (handover to OMS module) |
| `simulation` | SM | Plan Registry, scenario compare, what-if simulation, Publish flow | Forecast generation (đó là DM) |
| `daily-replan` | DR | Revision tracking, Delta computation, ACK/NACK protocol, Bitemporal model | Initial plan creation (đó là DE) |
| `transport` | TP | Vehicle Frame, 3 transport rules, Multi-Drop optimization | Actual dispatch & track (đó là TMS) |
| `exception` | EX | 20 canonical exception types, War Room workflow, SLA escalation | Alert delivery channel (đó là Integration) |
| `analytics` | AN | 17 KPIs, dashboard layout, Forecast Accuracy report | BI tool integration (đó là Integration) |
| `shared-kernel` | SK | Canonical ERD, base columns (audit fields, soft-delete, tenant), Policy Platform (39 policy types) | Domain-specific entity |
| `integration` | IG | ERP/WMS/TMS/Carrier connectors, DLQ, event bus contract | Internal API contract |
| `admin` | AM | Config Registry, RBAC (6×18), SSO, Chaos/Pentest config, NFR enforcement | User-facing settings UI |

**Boundary rule**: nếu feature nằm trên ranh giới 2 domain — flag rõ trong PRD `## Dependencies`, **không** ghi cùng 1 BR cho cả 2 domain.

---

## Master entities (Entity Registry)

Theo canonical `F01a-SCP-EntityRegistry-spec.md`, 18 entities chính:

### Master Data — sản phẩm & tổ chức
1. **Product** — sản phẩm cấp gốc (parent SKU)
2. **SKU** — mã quản lý kho (variant của Product, có size/pack/UoM)
3. **Product Hierarchy** — phân cấp cây (Category → Sub-category → Product)
4. **UoM** — đơn vị tính + conversion table
5. **Business Partner** — Customer / Supplier / Carrier / 3PL
6. **Location** — kho/DC/branch/store + hierarchy (Zone → Aisle → Rack → Level → Bin)
7. **Delivery Zone** — vùng giao hàng (per Customer)
8. **Vehicle Type** — loại xe + capacity

### Master Data — finance & compliance
9. **Currency** + exchange rate
10. **Tax** — thuế suất per region/product
11. **Calendar** — working day, holiday per region

### Master Data — planning config
12. **Safety Stock Config** — per SKU-Location
13. **Reorder Config** — ROP, ROQ, MOQ, order multiple
14. **Lead Time** — per SKU × Source (Supplier / Internal transfer)
15. **Lot Sizing Policy** — FOQ / EOQ / Lot-for-Lot / Period order
16. **Cost** — standard cost, last purchase cost (per SKU)

### Master Data — quality
17. **Quality Group** — phân nhóm BR validation
18. **Data Quality Gate** — 16 DQ gates với threshold

**Cross-reference rule**: mọi domain ngoài `master-data` **MUST** dùng `Ref → {Entity} (PRD-MD-NNN)` — không re-define field.

---

## 6 Buckets — canonical inventory model

Theo canonical `F03-SCP-SupplyInventory-spec.md`, mọi tính toán supply MUST dùng 6 bucket sau (không invent bucket mới):

| # | Bucket | Định nghĩa | Khi nào tăng/giảm |
|---|--------|------------|---------------------|
| 1 | **On-hand** | Tồn vật lý tại Location | +inbound receipt, −outbound ship, ±adjustment |
| 2 | **On-order** | Đã PO/MO chưa nhận | +PO confirmed, −PO received/cancelled |
| 3 | **In-transit** | Đang vận chuyển (giữa Location) | +Transfer Order ship, −Transfer Order received |
| 4 | **Reserved** | Đã allocate cho SO/Plan | +SO confirmed, −SO shipped/cancelled |
| 5 | **Damaged / Quarantine** | Tách ra khỏi available pool | +QC fail/damage report, −scrap/release |
| 6 | **Available** | Pool có thể allocate | = On-hand − Reserved − Damaged |

**Anti-pattern**: định nghĩa `Net Inventory = On-hand + In-transit − Reserved` ở chỗ khác. Mọi PRD MUST tham chiếu `F03 §Buckets` thay vì re-derive công thức.

---

## Allocation Engine — 2-Phase 6-Layer

Canonical `F04a-SCP-AllocationEngine-spec.md` định nghĩa engine phân bổ supply → demand theo cấu trúc 2-Phase × 6-Layer.

### Phase 1 — Hard constraints (must satisfy)
Loại bỏ allocation vi phạm hard constraint. Order theo layer:

| Layer | Constraint | Reject when |
|-------|------------|-------------|
| L1 | Product status | Product = Inactive/Discontinued |
| L2 | Location eligibility | Location không phục vụ Customer |
| L3 | Quality group | Demand group ≠ Supply group |
| L4 | Available qty | Available < demand qty (no oversell) |
| L5 | Lead time feasibility | Required date < earliest possible ship date |
| L6 | Capacity constraint | Supplier/Production capacity exhausted |

### Phase 2 — Soft optimization (prefer best)
Trong các allocation hợp lệ, chọn optimal theo priority:

| Layer | Optimization | Goal |
|-------|--------------|------|
| L1 | Cost | Minimize total landed cost |
| L2 | Lead time | Minimize lead time |
| L3 | Order priority | Honor customer priority tier |
| L4 | FIFO / FEFO | Older lot first / earlier expiry first |
| L5 | Capacity utilization | Balance load across DC/supplier |
| L6 | Container fill | Maximize FCL utilization |

**Dispatch & Saga**: kết quả allocation engine ghi vào `AllocationResult`, sau đó saga dispatch sang OP (tạo SO con) + IG (tạo PO/Transfer Order). Rollback nếu saga step fail.

---

## SO/TO Lifecycle

Theo canonical `F05a-SCP-SOTOLifecycle-spec.md`:

```
SO Plan (kế hoạch)          ──derive──→     SO con (concrete, dispatchable)
TO Plan (kế hoạch transfer) ──derive──→     TO con (concrete, dispatchable)
```

- **SO/TO Plan** = abstract level, output của Allocation Engine. Editable, simulation-friendly.
- **SO/TO con** = concrete order ready cho OMS/WMS execution. Một SO con = 1 demand line được satisfied.
- **Inheritance rule**: SO con kế thừa Customer/Location/Product/Qty từ SO Plan parent, **nhưng** có thể bị adjust khi daily-replan (xem §Daily Replan).

### State machine

```
Draft → Planned → Allocated → SO con generated → Confirmed → Released to OMS
                                  ↓                              ↓
                            Cancelled                       Cancelled (compensation)
```

---

## Daily Replan & Bitemporal

Canonical `F07-SCP-DailyReplan-spec.md` áp dụng bitemporal model (valid_time + transaction_time) để track revision:

- **Revision**: phiên replan trong ngày — không overwrite plan cũ, mà tạo revision mới với link đến revision trước.
- **Delta**: thay đổi giữa 2 revision liên tiếp (add/remove/modify SO con).
- **ACK/NACK protocol**: downstream system (OMS/WMS) ACK delta nó accept; NACK kèm lý do → exception flow.
- **Bitemporal**: query "plan as of yesterday" vs "plan as of today, valid for tomorrow" đều phải trả về kết quả nhất quán.

Anti-pattern: replan bằng cách DELETE old plan + INSERT new — mất history, không thể audit.

---

## Customer overlays — UNIS, TTC, MDLZ

3 customer triển khai, mỗi customer có overlay file trong `customer-variants/`:

| Customer | Key differences | Overlay file |
|---|---|---|
| **UNIS** | 2-Tier Safety Stock; LCNB (Local Container No-Bother); CN approve cycle; Force-release | `UNIS-Overlay.md` |
| **TTC** | 1-Tier Safety Stock; NM nội bộ (internal mfg); Peak Season config; Multi-BU | `TTC-Overlay.md` |
| **MDLZ** | LCNB last; Phase 2 stub (chưa active) | `MDLZ-Overlay.md` |

**Rule**: PRD by-module **không copy** logic overlay — chỉ reference file overlay trong section `## Customer Variants`. Lý do: overlay thay đổi theo customer contract, copy = drift risk.

---

## 17 canonical KPIs

Theo canonical `F10-SCP-Analytics-spec.md`:

| # | KPI | Đo lường |
|---|-----|----------|
| 1 | Forecast Accuracy (MAPE) | |Actual − Forecast| / Actual |
| 2 | Forecast Bias | (Forecast − Actual) / Actual (dương = over-forecast) |
| 3 | Service Level | Số order ship đúng hạn / Total |
| 4 | Fill Rate | Qty shipped / Qty ordered |
| 5 | Inventory Turnover | COGS / avg inventory |
| 6 | Days of Supply (DOS) | On-hand / avg daily demand |
| 7 | Stockout Rate | Số ngày stockout / Total ngày |
| 8 | Excess Stock Rate | Số SKU có DOS > max threshold / Total |
| 9 | Plan Adherence | SO confirmed = SO planned (delta < tolerance) |
| 10 | Replan Frequency | Số revision per day per plan |
| 11 | ACK Latency | Time from delta sent → downstream ACK |
| 12 | Exception MTTR | Mean time to resolve exception |
| 13 | Capacity Utilization | Used / total capacity (per DC, per supplier) |
| 14 | Cost-to-Serve | Total cost / order delivered |
| 15 | Perfect Order Rate | % order: on-time + complete + no exception |
| 16 | Allocation Confidence | % demand satisfied at L1-L4 Phase 1 (no degradation) |
| 17 | DRP Run Duration | Time from Run start → result published |

PRD by-module reference KPI canonical ID, không re-define công thức.

---

## Common terminology VN↔EN

Theo canonical `P07-SCP-Glossary-spec.md` (28 thuật ngữ). Trích những từ quan trọng:

| EN | VN | Notes |
|----|----|----|
| SKU (Stock Keeping Unit) | Mã quản lý kho | Variant của Product |
| AOP (Annual Operating Plan) | Kế hoạch hoạt động năm | Top-level demand plan |
| S&OP | Lập kế hoạch cung cầu | Monthly cycle |
| MRP | Hoạch định nhu cầu vật tư | Material Requirements Planning |
| DRP | Hoạch định nhu cầu phân phối | Distribution Requirements Planning |
| Safety Stock | Tồn kho an toàn | Buffer chống stockout |
| ROP (Reorder Point) | Điểm đặt hàng lại | When projected_inv < ROP → trigger reorder |
| MOQ | Số lượng đặt tối thiểu | Min Order Qty |
| Lot Sizing | Định cỡ lô | FOQ/EOQ/LfL/POQ |
| Allocation | Phân bổ | Match supply → demand |
| Replan | Lập lại kế hoạch | Daily revision |
| Cross-dock | Trung chuyển trực tiếp | No storage step |
| FIFO | Vào trước ra trước | First-In First-Out |
| FEFO | Hạn sớm ra trước | First-Expiry First-Out |
| LCNB | Không bận tâm container nội địa | UNIS-specific |
| ProC | Production Confirm | Order-planning workflow step |
| War Room | Phòng xử lý sự cố | Exception escalation channel |
| Bitemporal | Hai trục thời gian | Valid time + Transaction time |

PRD MUST giữ thuật ngữ canonical — không tự dịch/đổi nghĩa.
