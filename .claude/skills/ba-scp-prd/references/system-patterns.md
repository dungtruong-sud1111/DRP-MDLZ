# Smartlog SCP — System Infrastructure Patterns for BA

> Use this reference when a PRD describes system-triggered behavior such as "sau X phút hệ thống tự...", "mỗi N giờ hệ thống chạy...", "khi vượt ngưỡng → cảnh báo", "schedule notification at time Y". BA must pick the **correct pattern** so the technical plan does not fall back to anti-patterns like 60-second polling.

---

## When to read this file

Trigger this reference whenever the PRD contains any of:

- "Hệ thống tự sinh / phát hiện / cảnh báo sau X (phút | giờ | ngày)"
- "Hệ thống tự gửi email / notification / reminder khi..."
- "Hệ thống tự escalate / auto-resolve khi quá ngưỡng"
- "Mỗi ngày / mỗi giờ / mỗi tuần hệ thống chạy..."
- "Báo cáo định kỳ", "cleanup định kỳ", "sync định kỳ"
- "Real-time monitoring" with threshold-based detection
- Any "system action triggered by time" requirement

---

## Two background job patterns

The codebase ships **two scheduler service abstractions**. Every "system-triggered-by-time" requirement maps to exactly one of them. BA does **not** need to spell out the API — only describe the rule using the correct semantic (event-driven vs cron) so the dev team knows which service to wire up.

| Pattern | Service | When to use | Cron? |
|---|---|---|---|
| **Fire-and-forget** | `SmartlogFireAndForgetJobService` | Run **once** at a specific moment computed from a business event (`event_time + threshold`) | No |
| **Recurring** | `SmartlogRecurringJobService` | Run **repeatedly** on a calendar schedule (every N min/hour/day/week) | Yes |

Both services are production-ready in `backend/src/Smartlog.Core.Infrastructure/Schedulers/` and already used in AutoPlanning + other modules.

---

## Pattern 1 — Fire-and-forget (event-driven)

### Semantics

Schedule one job that fires exactly once at `runAt = event_time + threshold`. Job state lives externally in the Scheduler Service (restart-safe, tenant-scoped). Re-scheduling with the same `jobId` replaces the old job atomically.

### When to use

- "Sau X phút từ event Y, hệ thống kiểm tra điều kiện Z và sinh alert nếu vi phạm"
- "Sau 24 giờ chưa duyệt, hệ thống gửi reminder cho approver"
- "Sau N ngày kể từ tạo đơn, hệ thống tự đánh dấu hết hạn"
- "Sau 60 phút alert chưa Resolved, hệ thống tự escalate"
- Any business rule that says "do X at a specific future moment determined by an event"

### How BA writes the rule

```
BR-XX-YY: Schedule [job-name] khi [trigger event]
Description: Khi [business event] xảy ra (vd: Trip → Dispatched), hệ thống schedule
1 fire-and-forget job với runAt = [event_field] + [threshold cấu hình]. Khi job fire,
handler re-verify điều kiện hiện tại trước khi thực hiện action (tránh race
condition khi event source đã thay đổi). Re-schedule với cùng jobId khi
event_field update — không cancel job cũ. Self-noop khi điều kiện đã hết hiệu lực
(idempotent).
```

### Mandatory companion rules

For every fire-and-forget detection BR, the spec MUST also write:

| Companion rule | Purpose |
|---|---|
| **Re-schedule rule** | "Khi field X update → re-schedule cùng `jobId` với `runAt` mới" |
| **Cancel / self-noop rule** | "Khi event không còn áp dụng → handler self-noop khi fire (idempotent), KHÔNG cần explicit cancel (Scheduler Service hiện không expose cancel)" |
| **Idempotency rule** | "Khi job fire, handler re-verify mọi điều kiện (state hiện tại, threshold, đã có alert chưa) → exit nếu bất kỳ điều kiện nào không thỏa" |

Without these companion rules, the spec leaves race conditions and duplicates to dev guesswork.

### Past usage examples

- **TMS-003-004 Late Alerts**: `late-etd-{tripId}` scheduled when Trip → Dispatched, runAt = ETD + threshold. Re-scheduled on ETD update. Self-noop on Driver Start Trip. Escalation uses sibling job `escalate-alert-{alertId}` scheduled at `triggered_at + escalation_threshold`.
- **AutoPlanning VRP polling**: `poll-vrp-{runId}` scheduled to poll VRP solver status after submission.

---

## Pattern 2 — Recurring (cron-based)

### Semantics

Job runs on a recurring cron schedule (every N minutes/hours/days). Each tenant has its own per-tenant cron registration. `RunOnceOnStartup` flag controls whether to fire immediately when the schedule is registered (not just at next cron tick).

### When to use

- "Mỗi ngày 0:00 hệ thống tổng hợp báo cáo bán hàng"
- "Mỗi 15 phút sync master data từ ERP"
- "Mỗi tuần Chủ nhật 23:00 cleanup soft-deleted records cũ > 90 ngày"
- "Mỗi giờ recalculate inventory snapshot"
- Any business rule that says "run X on a calendar schedule" — NOT triggered by a specific event

### How BA writes the rule

```
BR-XX-YY: Recurring [job-name]
Description: Hệ thống chạy [tên job] theo lịch [cron expression hoặc mô tả tần
suất, vd: mỗi ngày 0:00 ICT, mỗi 15 phút]. Job [mô tả action - vd: tổng hợp số
liệu 24h trước vào bảng X, gửi email kết quả cho Y]. Khi job fail → retry [N lần
| skip + log]. Stop job khi tenant inactive.
```

### Mandatory companion rules

| Companion rule | Purpose |
|---|---|
| **Tenant scope rule** | "Job chạy per tenant (không cross-tenant), dùng `currentUser.TenantId` để scope query" |
| **Failure mode rule** | "Khi job fail → retry N lần với exponential backoff; sau N retry → log + alert dev (không block tenant next run)" |
| **Configurable frequency rule** | "Tần suất [cron] cấu hình tại PRD-SYS-001 (tenant settings); default = [value]" |

---

## Decision tree — which pattern?

Apply this in order; stop at the first YES.

```
1. Is the trigger a SPECIFIC business event (Trip dispatched, Order created, Alert triggered)?
   → Fire-and-forget. Job scheduled when event happens, runs once at event + threshold.

2. Is the trigger a CALENDAR rule (every N minutes, daily at HH:MM, weekly on Sunday)?
   → Recurring. Cron expression.

3. Is the trigger "scan every N seconds to check if anything has changed"?
   → STOP. This is the POLLING ANTI-PATTERN. Re-frame as event-driven:
     ask "what is the source event that I would be scanning for?" — then use Fire-and-forget
     triggered by that event.
```

---

## Anti-patterns to avoid

### Anti-pattern 1 — Polling job that scans the whole table

```
BR-XX-YY (WRONG): Hệ thống chạy job mỗi 60 giây quét toàn bộ Trip có status =
InTransit và estimated_arrival_time + threshold < now() → sinh alert nếu vi phạm.
```

**Why wrong**: DB load grows linearly with `(active trips × tenants)`. Wastes 99% of scans (no violation). Caused production-class incident in PRD-TMS-003-late-alerts v1.0..v1.6.

**Fix**: Re-frame as fire-and-forget:

```
BR-XX-YY (RIGHT): Khi Trip → InTransit (có ETA), hệ thống schedule 1 fire-and-forget
job late-eta-{tripId} với runAt = ETA + threshold. Khi job fire, handler re-verify
điều kiện hiện tại → sinh alert nếu vi phạm.
```

### Anti-pattern 2 — Mixing fire-and-forget with cron

```
BR-XX-YY (WRONG): Mỗi 60 giây hệ thống quét alert chưa Acknowledged trong > 60
phút → escalate.
```

**Why wrong**: Detection logic should fire at the exact moment `triggered_at + threshold`, not be discovered by a polling sweep. Latency is non-deterministic (0..60s lag) and DB cost is wasted.

**Fix**:

```
BR-XX-YY (RIGHT): Khi alert được tạo (Triggered), hệ thống schedule 1 fire-and-forget
job escalate-alert-{alertId} với runAt = triggered_at + escalation_threshold. Khi
job fire, handler re-verify alert vẫn ∈ {Triggered, Acknowledged} → chuyển sang
Escalated.
```

### Anti-pattern 3 — Implicit assumption that "real-time" requires polling

BA writes "hệ thống cần phát hiện trễ trong vòng 1 phút" → dev infers "phải polling 60s".

**Fix**: Frame "detection latency" as the granularity of the Scheduler Service, not as polling interval. Fire-and-forget jobs fire within ±vài giây of `runAt`. NFR-style wording:

```
NFR: Alert sinh đúng tại ETD/ETA + threshold (± vài giây — tùy granularity Scheduler
Service, mục tiêu < 30s). Không có khái niệm "polling interval".
```

### Anti-pattern 4 — Recurring job that is really event-driven

```
BR-XX-YY (WRONG): Mỗi 1 phút hệ thống kiểm tra các Order tạo > 24h chưa duyệt
→ gửi reminder approver.
```

**Why wrong**: This is event-driven (event = Order created), not cron. Should be:

```
BR-XX-YY (RIGHT): Khi Order tạo (status = Submitted), hệ thống schedule 1 fire-and-
forget job reminder-order-{orderId} với runAt = created_at + 24h. Khi job fire, handler
re-verify Order vẫn Submitted → gửi reminder.
```

### Anti-pattern 5 — Recurring job without tenant scope / failure mode

```
BR-XX-YY (WRONG): Mỗi ngày 0:00 hệ thống tổng hợp báo cáo.
```

Missing: per-tenant scope, configurable frequency, failure mode.

**Fix**: Add companion rules per section "Mandatory companion rules" above.

---

## Wording checklist before merging PRD

For every BR that triggers system action by time, verify:

- [ ] Pattern explicitly named: "fire-and-forget job" or "recurring job"
- [ ] `jobId` naming convention specified (e.g., `late-etd-{tripId}`, `daily-report-{tenantId}`)
- [ ] `runAt` formula (fire-and-forget) or `cron expression` (recurring) is unambiguous
- [ ] Re-schedule rule present (fire-and-forget) — what events trigger re-schedule, with same jobId
- [ ] Cancel / self-noop rule present (fire-and-forget) — what events make the job a no-op
- [ ] Idempotency rule present — handler re-verify on fire
- [ ] No occurrence of "polling", "quét định kỳ N giây", "detection interval" anywhere in BR
- [ ] Detection latency NFR is "tại đúng thời điểm ± vài giây", NOT "trong vòng N giây"
- [ ] Configurable threshold/cron is documented in §Configurable Parameters

---

## Cross-references

- **Past incident**: PRD-TMS-003-late-alerts v1.0–v1.6 fell into Anti-pattern 1; rewritten to fire-and-forget in v1.7 (BR-MN-04-01..05, BR-MN-04-16..19). Technical companion: PRD-TMS-003-late-alerts-impl.md.
- **Codebase reference**: `backend/src/Smartlog.Core.Infrastructure/Schedulers/SmartlogFireAndForgetJobService.cs` and `SmartlogRecurringJobService.cs`. BA does not implement these — only references the pattern by name when writing BR.
- **Configurable params**: Both patterns expose threshold/cron values via `IAppConfigService` (PRD-SYS-001 tenant settings). BA documents the default + the tenant override capability.
