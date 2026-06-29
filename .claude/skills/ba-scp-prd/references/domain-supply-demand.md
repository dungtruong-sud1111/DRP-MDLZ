# Supply & Demand Planning — Domain Knowledge

## Table of Contents
1. [Core Processes](#core-processes)
2. [Key Entities](#key-entities)
3. [Demand Planning](#demand-planning)
4. [Supply Planning](#supply-planning)
5. [Inventory Planning](#inventory-planning)
6. [DRP (Distribution Requirements Planning)](#drp)
7. [S&OP Process](#sop-process)
8. [Business Rules](#business-rules)
9. [Common Screens](#common-screens)

---

## Core Processes

```
DEMAND SIDE                 BALANCING                   SUPPLY SIDE
───────────                 ─────────                   ───────────
Historical Sales       →    S&OP Review            ←    Supplier Capacity
Market Intelligence    →    Consensus Forecast     ←    Production Capacity
Promotions Calendar    →    Gap Analysis           ←    Lead Times
Seasonal Patterns      →    What-if Scenarios      ←    MOQ / Order Constraints
Customer Forecast      →    Approved Plan          ←    Budget / Capital

                            ↓

EXECUTION PLANNING
──────────────────
Safety Stock Calculation
Reorder Point / Reorder Qty
MRP / DRP Explosion
Purchase Order Suggestions
Transfer Order Suggestions
```

---

## Key Entities

### Forecast & Plan
| Entity | Mô tả | Key Fields |
|--------|--------|-----------|
| **DemandForecast** | Dự báo nhu cầu | forecast_id, sku_id, location_id, period (YYYY-MM), forecast_qty, confidence_level, method, version |
| **ForecastVersion** | Phiên bản dự báo | version_id, name, type (STATISTICAL/MANUAL/CONSENSUS), created_date, status (DRAFT/APPROVED) |
| **SupplyPlan** | Kế hoạch cung ứng | plan_id, sku_id, location_id, period, planned_receipt_qty, source (PO/PRODUCTION/TRANSFER) |
| **ConsensusRecord** | Kết quả S&OP | period, sku_group_id, demand_plan_qty, supply_plan_qty, gap, decision, notes |

### Inventory Planning
| Entity | Mô tả | Key Fields |
|--------|--------|-----------|
| **SafetyStockConfig** | Cấu hình tồn kho an toàn | sku_id, location_id, method (FIXED/DYNAMIC/SERVICE_LEVEL), safety_stock_qty, service_level_target |
| **ReorderConfig** | Cấu hình đặt hàng lại | sku_id, location_id, reorder_point, reorder_qty, min_order_qty (MOQ), order_multiple |
| **InventoryPolicy** | Chính sách tồn kho | sku_group_id, location_id, min_dos, max_dos, target_dos, review_cycle_days |
| **ReplenishmentSuggestion** | Đề xuất bổ sung | sku_id, source_location_id, dest_location_id, suggested_qty, required_date, type (PO/TRANSFER), status (PENDING/APPROVED/CONVERTED) |

### DRP
| Entity | Mô tả | Key Fields |
|--------|--------|-----------|
| **DRPPlan** | Kế hoạch phân phối | plan_id, period_start, period_end, status |
| **DRPRecord** | Chi tiết DRP per SKU per location | sku_id, location_id, period, beginning_inv, demand_forecast, planned_receipts, ending_inv, net_requirement, planned_order |
| **DistributionNetwork** | Mạng lưới phân phối | source_id (DC), dest_id (store/sub-DC), transit_time_days, cost_per_unit |

---

## Demand Planning

### Forecasting Methods
| Method | Mô tả | Khi dùng |
|--------|--------|---------|
| **Moving Average** | Trung bình X kỳ gần nhất | Demand ổn định, ít biến động |
| **Exponential Smoothing** | Weighted average, gần hơn nặng hơn | Demand có trend nhẹ |
| **Holt-Winters** | Triple exponential (level + trend + seasonality) | Demand có mùa vụ rõ |
| **Linear Regression** | Fit đường thẳng trên historical | Demand có trend dài hạn |
| **Manual Override** | Người dùng nhập tay | Sản phẩm mới, events đặc biệt |
| **Consensus** | Kết hợp statistical + market intel + manual | S&OP approved plan |

### Forecast Accuracy Metrics
```
MAPE = Σ|Actual - Forecast| / Σ Actual × 100%
Bias = Σ(Forecast - Actual) / Σ Actual × 100%  (dương = over-forecast)
WMAPE = Σ|Actual - Forecast| / Σ Actual × 100%  (weighted by volume)
```

### Forecast Granularity
- **Time:** weekly / monthly / quarterly
- **Product:** SKU / SKU Group / Category
- **Location:** Store / DC / Region / National
- **Channel:** B2B / B2C / Marketplace

Nguyên tắc: Forecast ở mức aggregate chính xác hơn. Disaggregate xuống SKU-Location dùng proportional allocation.

---

## Supply Planning

### MRP Logic (Material Requirements Planning)
```
Gross Requirement = Demand Forecast + Safety Stock target
Net Requirement = Gross Requirement - On-hand - Scheduled Receipts
If Net Requirement > 0 → Planned Order
Planned Order Qty = max(Net Requirement, MOQ), rounded up to order multiple
Planned Order Date = Required Date - Lead Time
```

### Supply Sources (priority order)
1. **Internal Transfer** — từ DC/kho có surplus
2. **Production** — nếu có nhà máy
3. **Purchase Order** — từ supplier
4. **Emergency** — spot buy, air freight (costly)

### Constraints
- Supplier MOQ (Minimum Order Quantity)
- Order multiples (phải đặt theo bội số, vd: 1 pallet = 48 cartons)
- Supplier capacity per period
- Budget allocation per category
- Container optimization (FCL vs LCL for import)

---

## Inventory Planning

### Safety Stock Formulas

**Fixed Safety Stock:**
```
SS = fixed_qty (set manually per SKU)
```

**Based on Days of Supply:**
```
SS = avg_daily_demand × safety_days
```

**Service Level based (Z-score):**
```
SS = Z × σ_demand × √(lead_time + review_period)
Z = service level factor (95% → Z=1.65, 99% → Z=2.33)
σ_demand = standard deviation of demand
```

### Reorder Point (ROP)
```
ROP = (avg_daily_demand × lead_time_days) + safety_stock
```

### Inventory Classification (ABC-XYZ)
| | X (Low variability) | Y (Medium) | Z (High variability) |
|---|---|---|---|
| **A** (High value) | AX: Tight control, frequent review | AY: Moderate buffer | AZ: High buffer, close monitoring |
| **B** (Medium) | BX: Standard | BY: Standard | BZ: Moderate buffer |
| **C** (Low value) | CX: Min effort | CY: Min effort | CZ: Consider discontinue |

### Days of Supply (DOS)
```
DOS = Current Inventory / Avg Daily Demand
Target DOS = Lead Time + Safety Days + Review Period / 2
```

---

## DRP (Distribution Requirements Planning)

### DRP Table Structure
Cho mỗi SKU tại mỗi location, tính theo period (tuần/tháng):

| Period | P1 | P2 | P3 | P4 | ... |
|--------|----|----|----|----|-----|
| Beginning Inventory | 100 | 60 | 80 | 50 | |
| Demand Forecast | 50 | 40 | 60 | 45 | |
| Scheduled Receipts | 0 | 60 | 0 | 0 | |
| Ending Inventory | 50 | 80 | 20 | 5 | |
| Net Requirement | 0 | 0 | 0 | 25 | |
| Planned Order Receipt | 0 | 0 | 0 | 60 | |
| Planned Order Release | 0 | 0 | 60* | 0 | |

*Planned Order Release = Planned Order Receipt offset by lead time

### DRP Network Explosion
```
Store demand → aggregated at Regional DC → aggregated at Central DC → Purchase Order to Supplier

Central DC
  ├── Regional DC North
  │     ├── Store Hanoi 1
  │     └── Store Hanoi 2
  └── Regional DC South
        ├── Store HCMC 1
        └── Store HCMC 2
```

Net requirements cascade up the network. Each level adds its own lead time offset.

---

## S&OP Process

### Monthly Cycle
```
Week 1: Data Preparation
  - Collect actual sales, inventory snapshots
  - Run statistical forecast
  - Sales team input market intelligence

Week 2: Demand Review
  - Compare statistical vs last consensus
  - Adjust for promotions, new launches, discontinuations
  - Agree on unconstrained demand plan

Week 3: Supply Review
  - Check supply capacity vs demand plan
  - Identify gaps, propose alternatives
  - Run scenarios (what-if)

Week 4: Executive S&OP Meeting
  - Review demand/supply balance
  - Approve consensus plan
  - Decisions on budget, investments, risk
```

### What-if Scenarios
| Scenario | Parameters | Giải đáp |
|----------|-----------|---------|
| Demand spike | +20% demand Q4 | Đủ capacity không? Cần tăng PO? |
| Supplier delay | Lead time +2 weeks | Safety stock đủ cover? |
| New product launch | X units/month forecast | Kho nào, khi nào stock, promotion? |
| Price increase | +10% cost | Impact on margin? Pass to customer? |

---

## Business Rules

### Forecast
- BR-SD-FC-01: Forecast phải có version control (không overwrite)
- BR-SD-FC-02: Statistical forecast chạy auto hàng tháng
- BR-SD-FC-03: Manual override ghi lý do (promotion, event, market intel)
- BR-SD-FC-04: Approved forecast = input cho MRP/DRP
- BR-SD-FC-05: New SKU (< 6 months data) dùng analog/manual forecast

### Safety Stock
- BR-SD-SS-01: Review safety stock monthly (hoặc khi demand pattern thay đổi)
- BR-SD-SS-02: Service level A-items ≥ 95%, B ≥ 90%, C ≥ 85%
- BR-SD-SS-03: Safety stock != 0 cho active SKUs (trừ made-to-order)
- BR-SD-SS-04: Excess stock (DOS > max_dos) → flag for review

### Replenishment
- BR-SD-REP-01: Auto-generate suggestion khi projected_inv < reorder_point
- BR-SD-REP-02: Suggestion qty = max(net_requirement, MOQ), round up to order_multiple
- BR-SD-REP-03: Prioritize transfer trước PO (nếu network có surplus)
- BR-SD-REP-04: Approved suggestion → auto-create PO hoặc Transfer Order
- BR-SD-REP-05: Expired suggestions (> 7 days unapproved) → auto-cancel + regenerate

---

## Common Screens

### Demand Planning
1. **Forecast Workbench** — grid view: SKU × Period, editable cells, version comparison
2. **Forecast Accuracy Dashboard** — MAPE, Bias by category/SKU (charts + heatmap)
3. **Demand Review** — side-by-side: statistical vs manual vs consensus
4. **Promotion Calendar** — timeline view, impact overlay on forecast

### Supply Planning
1. **MRP/DRP Dashboard** — supply vs demand balance chart per SKU
2. **Replenishment Suggestions** — list with approve/reject/edit actions
3. **Supplier Capacity View** — utilization % per supplier per period
4. **What-if Simulator** — adjust parameters, see projected inventory impact

### Inventory Planning
1. **Safety Stock Review** — ABC classification, current SS vs recommended
2. **Inventory Health** — DOS distribution, overstock/understock alerts
3. **Reorder Configuration** — mass edit ROP/ROQ per SKU group
4. **Stock Coverage Report** — projected DOS for next X weeks (color-coded)

### S&OP
1. **S&OP Dashboard** — demand/supply/inventory summary by category
2. **Gap Analysis** — demand vs supply capacity, shortfall highlighted
3. **Scenario Comparison** — table + chart comparing 2-3 scenarios
4. **Meeting Minutes** — decisions, action items, risk register
