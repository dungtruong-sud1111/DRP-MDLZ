# Field Validation Patterns — Smartlog SCP

Reference này định nghĩa standard constraints per field type. Khi Data Model có common field type (Name, Code, Email, Phone, Date, Amount, …), copy constraints từ đây vào bảng Validation Rules — để mọi PRD by-module cùng convention.

## Code fields

| Pattern | Constraint | Error message (VN) |
|---|---|---|
| Generic code | Pattern: `^[A-Z0-9_-]+$`, length 3–20 | "Mã {entity} chỉ chứa chữ HOA, số, gạch dưới hoặc gạch ngang, dài 3–20 ký tự" |
| Product / SKU code | Pattern: `^[A-Z0-9_-]+$`, length 3–50 | "Mã SKU/Product không đúng định dạng" |
| BP code | Pattern: `^[A-Z0-9_-]+$`, length 3–20, unique per partner type | "Mã đối tác đã tồn tại trong cùng loại" |
| Location code | Pattern: `^[A-Z0-9_-]+$`, length 3–30, unique trong tenant | "Mã địa điểm đã tồn tại" |
| Order code | Auto-gen `{PREFIX}-{YYYYMMDD}-{SEQ}` hoặc user-entered theo pattern | "Mã đơn không đúng định dạng" |

## Name fields

| Pattern | Constraint | Error message (VN) |
|---|---|---|
| Display name | Length 1–255, trim whitespace, không cho phép chuỗi rỗng | "Tên {entity} không được để trống và không quá 255 ký tự" |
| Short name / Alias | Length 1–100 | "Tên ngắn không quá 100 ký tự" |
| Long description | Length 0–1000, optional | "Mô tả không quá 1000 ký tự" |

## Contact fields

| Pattern | Constraint | Error message (VN) |
|---|---|---|
| Email | RFC 5322 format, max 200 chars, lowercase normalize | "Email không đúng định dạng" |
| Phone (VN) | Pattern: `^(0\|\\+84)([0-9]{9,10})$`, normalize bỏ space/dash | "Số điện thoại Việt Nam không đúng định dạng" |
| Phone (international) | Pattern: `^\\+?[0-9 \\-()]{7,20}$` | "Số điện thoại không đúng định dạng" |
| Tax code (VN) | Pattern: `^[0-9]{10}(-[0-9]{3})?$` (10 hoặc 13 số) | "Mã số thuế Việt Nam phải có 10 hoặc 13 chữ số" |

## Quantitative fields (SCP-critical)

| Pattern | Constraint | Error message (VN) |
|---|---|---|
| Quantity | Decimal(18,4), ≥ 0 (trừ adjustment), không chứa dấu phẩy | "Số lượng phải ≥ 0" |
| Adjustment qty | Decimal(18,4), có thể âm | "Số lượng điều chỉnh không đúng định dạng" |
| UoM-bound qty | Phải có UoM ref kèm; conversion về base UoM trước khi compare | "Phải chọn đơn vị tính trước khi nhập số lượng" |
| Lead time (days) | Integer ≥ 0, ≤ 365 | "Lead time phải từ 0 đến 365 ngày" |
| Safety days | Integer ≥ 0, ≤ 180 | "Số ngày an toàn từ 0 đến 180" |
| Service level | Decimal 0.50 ≤ x ≤ 0.9999, default 0.95 | "Mức dịch vụ phải trong [50%, 99.99%]" |
| Service level Z-score | Decimal 0.00 ≤ x ≤ 5.00 (95% = 1.65, 99% = 2.33) | "Z-score không đúng phạm vi" |
| MAPE / Bias | Decimal, MAPE ≥ 0, Bias có thể âm/dương | — |

## Financial fields

| Pattern | Constraint | Error message (VN) |
|---|---|---|
| Amount (currency) | Decimal(18,4), ≥ 0, kèm currency ref | "Số tiền phải ≥ 0" |
| Cost (unit) | Decimal(18,4), ≥ 0 | "Giá đơn vị phải ≥ 0" |
| Exchange rate | Decimal(18,8), > 0 | "Tỷ giá phải > 0" |
| Tax rate | Decimal 0.00 ≤ x ≤ 1.00 (vd 0.10 = 10%) | "Thuế suất phải trong [0%, 100%]" |
| Rounding rule | Enum: ROUND_HALF_UP / ROUND_HALF_EVEN / FLOOR / CEILING | — |

## Date / time fields

| Pattern | Constraint | Error message (VN) |
|---|---|---|
| Date | ISO 8601 YYYY-MM-DD | "Ngày không đúng định dạng" |
| DateTime | ISO 8601 với timezone | "Thời gian không đúng định dạng" |
| Future date only | Date > today | "Ngày phải lớn hơn hôm nay" |
| Past date only | Date < today | "Ngày phải nhỏ hơn hôm nay" |
| Period (year-month) | Format `YYYY-MM`, range 2000-01 đến 2099-12 | "Kỳ phải theo định dạng YYYY-MM" |

## Cross-field validation (SCP common)

| Rule | Description |
|------|-------------|
| Date range | `from_date <= to_date` cho mọi cặp date filter / period |
| Lifecycle constraint | Date follow state machine: `confirmed_at >= created_at >= updated_at` (logically) |
| Required by state | `Confirmed` requires all mandatory fields filled; `Draft` allows partial |
| Quantity ≤ available | SO con qty ≤ Available bucket (xem `domain-scp.md` §6 Buckets) |
| UoM consistency | Khi line items so sánh / sum → convert về base UoM trước |
| MOQ constraint | PO qty >= MOQ và là bội số của order_multiple |
| Lead time feasibility | `Required date >= Order date + Lead time + Buffer` |

## Enum / Reference fields

| Pattern | Constraint |
|---|---|
| Status enum | Reference state machine của entity. Không hardcode trong VR — point đến `State Machine` section |
| BP type | Enum: Customer / Supplier / Carrier / 3PL. Source: Business Partner PRD |
| Currency | Ref → Currency master. Default = tenant default currency |
| UoM | Ref → UoM master. Required nếu field là qty |
| Customer scope | Enum: All / UNIS / TTC / MDLZ |

## File / attachment

| Pattern | Constraint |
|---|---|
| Single file | Max 10 MB, allowed types per PRD scope |
| File array | Max 5 files × 10 MB each |
| Image | Max 5 MB, types: png/jpg/webp, optional dimensions constraint |

## Compound rules

### Multi-tenancy (luôn áp dụng)

- BR-MT-01: Mọi entity có `tenantId` (xem [CLAUDE.md](../../../CLAUDE.md) — DB column convention)
- BR-MT-02: Mọi query filter `tenantId`
- BR-MT-03: Unique constraint luôn include `tenantId`
- BR-MT-04: Không có API trả về data cross-tenant

### Document lifecycle (xem `domain-supply-chain.md` §Cross-domain Patterns)

- Draft → Confirmed → InProgress → Completed → Cancelled (cancelled từ Draft/Confirmed only)
- Completed = immutable
- Cancelled = soft delete, giữ history
- Status transition phải validate (không nhảy cóc)

### Audit trail

- Mọi thay đổi quan trọng: who, when, what, from, to
- Đặc biệt cho: status change, qty adjustment, price change, plan revision
