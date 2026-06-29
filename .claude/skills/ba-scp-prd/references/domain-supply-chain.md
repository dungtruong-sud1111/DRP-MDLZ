# Supply Chain Management — Domain Knowledge (Tổng quan)

Đây là reference file nền tảng. Đọc file này trước mọi PRD trong hệ sinh thái SCM.

## Table of Contents
1. [Core Concepts](#core-concepts)
2. [Common Entities](#common-entities)
3. [Cross-domain Patterns](#cross-domain-patterns)
4. [Master Data](#master-data)
5. [Common Business Rules](#common-business-rules)
6. [Integration Points](#integration-points)
7. [KPIs & Metrics](#kpis--metrics)

---

## Core Concepts

### Supply Chain Flow
```
Supplier → Purchase Order → Inbound → Warehouse → Outbound → Transport → Customer
    ↑                                                                        |
    └──────────── Return / Reverse Logistics ────────────────────────────────┘
```

### Planning Hierarchy
```
Strategic Planning (1-5 years)
  └── S&OP / Demand Planning (3-18 months)
       └── Master Production Schedule (1-3 months)
            └── MRP / DRP (weekly/daily)
                 └── Execution (WMS/TMS/OMS real-time)
```

### Key Domains & Boundaries

| Domain | Scope | Key Entities |
|--------|-------|-------------|
| **WMS** | Quản lý hàng hóa trong kho | Location, Inventory, Inbound/Outbound Order, Pick Task |
| **TMS** | Vận chuyển từ điểm A → B | Shipment, Route, Carrier, Vehicle, Trip |
| **OMS** | Quản lý đơn hàng end-to-end | Sales Order, Purchase Order, Return Order |
| **Supply-Demand** | Lập kế hoạch cung-cầu | Forecast, Plan, Safety Stock, Replenishment |
| **Logistics** | Điều phối tổng thể + 3PL | Logistics Order, 3PL Integration, Cross-dock |

---

## Common Entities

Các entity xuất hiện xuyên suốt mọi domain:

### Product / SKU (Stock Keeping Unit)
- `sku_code` — mã sản phẩm unique
- `barcode` — mã vạch (EAN-13, Code128...)
- `name`, `description`
- `category_id` → Product Category
- `uom_id` → Unit of Measure (đơn vị tính)
- `weight`, `volume`, `dimensions` (L x W x H)
- `shelf_life_days` — hạn sử dụng (cho hàng FMCG)
- `is_lot_controlled` — có quản lý theo lô?
- `is_serial_controlled` — có quản lý serial number?
- `status` — ACTIVE / INACTIVE / DISCONTINUED

### Partner (Customer / Supplier / Carrier)
- `partner_code`, `partner_type` (CUSTOMER / SUPPLIER / CARRIER / 3PL)
- `name`, `tax_code`, `address`, `contact_info`
- `payment_terms`, `credit_limit`
- `lead_time_days` — thời gian giao hàng tiêu chuẩn

### Warehouse / Location
- `warehouse_code`, `name`, `address`
- `type` — WAREHOUSE / DISTRIBUTION_CENTER / CROSS_DOCK / STORE
- Location hierarchy: Zone → Aisle → Rack → Level → Bin

### Unit of Measure (UoM)
- Base UoM (piece, kg, liter...)
- Conversion: 1 carton = 12 pieces, 1 pallet = 48 cartons
- Quan trọng: mọi tính toán phải convert về cùng UoM trước khi so sánh

---

## Cross-domain Patterns

### Document Number Format
Convention phổ biến: `{PREFIX}-{YYYYMMDD}-{SEQUENCE}`
- PO-20260416-0001 (Purchase Order)
- SO-20260416-0001 (Sales Order)
- GRN-20260416-0001 (Goods Receipt Note)
- DN-20260416-0001 (Delivery Note)

Sequence reset: theo ngày hoặc không reset (tùy business).

### Status Lifecycle Pattern
Hầu hết documents đều có lifecycle:
```
DRAFT → CONFIRMED → IN_PROGRESS → COMPLETED
                  → CANCELLED
```
Rules:
- Chỉ DRAFT có thể edit
- CONFIRMED → không sửa header, chỉ sửa lines trong giới hạn
- COMPLETED → immutable (chỉ tạo adjustment/return)
- CANCELLED → soft delete, giữ history

### Line Item Pattern
Mọi document có header + lines:
```
Order (header)
  ├── OrderLine 1: SKU-A × 100 pcs
  ├── OrderLine 2: SKU-B × 50 cartons
  └── OrderLine 3: SKU-C × 200 kg
```
Line items luôn có: `line_number`, `sku_id`, `quantity`, `uom_id`, `unit_price` (nếu có)

### Quantity Tracking Pattern
Cho mỗi line item, track nhiều loại quantity:
- `ordered_qty` — số lượng đặt
- `received_qty` — số lượng đã nhận
- `shipped_qty` — số lượng đã giao
- `remaining_qty` = ordered - received (hoặc ordered - shipped)

### Audit Trail
Mọi thay đổi quan trọng cần log:
- Who (user), When (timestamp), What (field changed), From (old value), To (new value)
- Đặc biệt quan trọng cho: status changes, quantity adjustments, price changes

---

## Master Data

Master data là foundation. Luôn thiết kế master data trước transaction data.

### Hierarchy
```
Company
  └── Warehouse / Distribution Center
       └── Zone (Dry / Cold / Hazardous)
            └── Location (Aisle-Rack-Level-Bin)

Product Category (tree structure)
  └── Sub-category
       └── SKU

Partner Group
  └── Partner (Customer/Supplier)
       └── Partner Address (shipping/billing)
```

### Common Master Data Entities
1. **Product / SKU** — core
2. **Product Category** — phân loại tree
3. **Partner** — customer, supplier, carrier
4. **Warehouse** — kho/DC
5. **Location** — vị trí trong kho
6. **UoM** — đơn vị tính + conversion
7. **Currency** + exchange rate
8. **Tax** — thuế suất
9. **Delivery Zone** — vùng giao hàng
10. **Vehicle Type** — loại xe

---

## Common Business Rules

### Multi-tenancy (BẮT BUỘC)
- BR-MT-01: Mọi entity có `tenant_id`
- BR-MT-02: Mọi query filter `tenant_id`
- BR-MT-03: Unique constraint luôn include `tenant_id`
- BR-MT-04: Không có API nào trả về data cross-tenant

### Số lượng & Tính toán
- BR-QTY-01: Quantity luôn >= 0 (trừ adjustment)
- BR-QTY-02: Mọi phép tính dùng decimal-safe math (tránh floating point)
- BR-QTY-03: UoM phải thống nhất trước khi tính toán
- BR-QTY-04: Rounding rule cần define rõ (ROUND_HALF_UP, 2 decimal places)

### Document Lifecycle
- BR-DOC-01: Document đã COMPLETED không thể sửa/xóa
- BR-DOC-02: Document CANCELLED giữ lại, không hard delete
- BR-DOC-03: Chỉ DRAFT/CONFIRMED mới có thể cancel
- BR-DOC-04: Status transition phải validate (không nhảy cóc)

### Inventory
- BR-INV-01: Tồn kho không âm (trừ khi business cho phép oversell)
- BR-INV-02: Xuất kho trừ vào available_qty, không phải on_hand_qty
- BR-INV-03: Available = On-hand - Reserved - Damaged
- BR-INV-04: Lot/Serial tracking nếu SKU yêu cầu

---

## Integration Points

### Giữa các domain
```
OMS ──(Sales Order)──→ WMS (Outbound Order) ──→ TMS (Shipment)
OMS ──(Purchase Order)──→ WMS (Inbound Order) ←── Supplier
Supply-Demand ──(Replenishment)──→ OMS (Purchase Order)
Supply-Demand ──(Forecast)──→ WMS (Capacity Planning)
```

### Với hệ thống bên ngoài
- **ERP** — master data sync, financial posting
- **3PL** — order push/pull, inventory sync, event tracking
- **Carrier API** — booking, tracking, POD (Proof of Delivery)
- **E-commerce** — order import, inventory publish
- **IoT/Barcode** — scan events cho WMS tasks

### Integration Patterns
- **Sync** (real-time): REST API call
- **Async** (near real-time): Message queue (Kafka, RabbitMQ)
- **Batch** (periodic): File exchange (CSV, EDI, XML)

---

## KPIs & Metrics

### WMS
- Inventory Accuracy (%)
- Order Fulfillment Rate (%)
- Pick Accuracy (%)
- Warehouse Utilization (%)
- Cycle Time (receipt-to-putaway, order-to-ship)

### TMS
- On-time Delivery Rate (%)
- Cost per Km / Cost per Delivery
- Vehicle Utilization (%)
- Average Transit Time

### OMS
- Order Accuracy (%)
- Order Cycle Time (order-to-delivery)
- Return Rate (%)
- Perfect Order Rate (%)

### Supply-Demand
- Forecast Accuracy (MAPE, Bias)
- Inventory Turnover
- Stockout Rate (%)
- Days of Supply (DOS)
- Fill Rate (%)
