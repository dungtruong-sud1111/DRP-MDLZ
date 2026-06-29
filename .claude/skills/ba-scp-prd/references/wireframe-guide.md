# Wireframe Design Guide

## When to Create Wireframes

**Create when ANY of these match:**
- New screen, page, or dialog
- Form with 4+ fields
- Multi-step workflow or wizard
- Multi-step full-page form (3+ sections with side progress panel)
- Complex layout (dashboard, split-panel, master-detail)
- Data table with filters, sorting, or bulk actions
- Conditional UI logic (show/hide based on state)
- User explicitly mentions: "UI", "giao diện", "màn hình", "form", "wireframe"

**Skip when:**
- API-only or background job with no UI
- Simple toggle or single-button action
- Pure business rule change with no visual impact

## ASCII Wireframe Method

Use box-drawing characters to create clean wireframes:

```
┌──┐  └──┘  ├──┤  ┬  ┴  ┼  │  ─
```

### Component Notation

| Symbol | Meaning |
|--------|---------|
| `[Button Text]` | Button |
| `[▼ Dropdown______]` | Dropdown/Select |
| `[_______________]` | Text input |
| `[📅 Date________]` | Date picker |
| `[🔍 Search______]` | Search input |
| `(○) Option` | Radio button (unselected) |
| `(●) Option` | Radio button (selected) |
| `[ ] Option` | Checkbox (unchecked) |
| `[✓] Option` | Checkbox (checked) |
| `[Tab 1] [Tab 2]` | Tab navigation |
| `≡` | Menu/hamburger icon |
| `✕` | Close/clear button |
| `←` | Back navigation |
| `⋮` | More actions menu |

## Container Pattern Decision

Before drawing any wireframe, determine the container pattern for each screen or action.

### Decision Table

| Criteria | Dialog | Drawer | Detail View |
|----------|--------|--------|-------------|
| Number of fields | ≤6 | 7–15 | Unlimited |
| Must keep list context visible | Yes | Yes | No |
| Needs its own URL (share/bookmark) | No | No | **Yes** |
| Estimated time on screen | <1 min | 1–3 min | >3 min |
| Blocking — user must act before continuing | **Yes** | No | No |
| Has tabs or sub-navigation | No | Max 2–3 small tabs | **Yes** |
| Entity has lifecycle, sub-data, activity log | No | No | **Yes** |

### Create and Edit Must Use the Same Pattern

User builds one mental model per entity. Mixing patterns across Create and Edit breaks that model and creates friction.

```
Create → Drawer   ⟹   Edit must → Drawer
Create → Dialog   ⟹   Edit must → Dialog
Create → Full-page ⟹  Edit must → Full-page
```

**Exception — when Edit is actually entity management:**

If the entity generates significant sub-data after creation (documents, milestones, activity log, related records), Edit is no longer "change a few fields" — it is full entity management. In this case:

```
Create  →  Drawer (simple form, just the initial fields)
View/Edit → Detail View (full entity management with tabs and sub-data)
```

On the Detail View, the Edit button must open **inline edit or an edit mode within the same page** — not re-open the Drawer. Returning to the Drawer for editing breaks consistency and loses sub-data context.

### Anti-Patterns to Avoid

| Wrong | Correct |
|-------|---------|
| Popup/dialog with 15 fields requiring scroll | Drawer or full-page |
| Navigate to detail view just for a 3-field action | Dialog |
| Drawer opened from inside another drawer | Separate dialog or inline section |
| Create → Drawer, Edit → Detail View (without inline edit on detail) | Create → Drawer, View/Edit → Detail View with inline edit |
| Dialog with no URL when user needs to bookmark or share | Detail View |

## Layout Patterns

### Pattern 1: List Screen (most common for logistics)

Standard layout for any entity list (shipments, bookings, orders, containers):

```
┌────────────────────────────────────────────────────────────────────┐
│  [Module Name] > [Feature Name]                                    │
│                                                                    │
│  ┌──────────────────────────────┐    [Tìm kiếm (F3)]  [+ Thêm]   │
│  │ 🔍 Quick search...           │                                  │
│  └──────────────────────────────┘                                  │
│                                                                    │
│  ┌─── Search Panel (collapsed by default, toggle via F3) ───────┐ │
│  │  Field 1: [___________]   Field 2: [▼__________]             │ │
│  │  Field 3: [📅 From____]   Field 4: [📅 To______]             │ │
│  │                                     [Tìm kiếm]  [Xoá bộ lọc]│ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ □ │ Code     │ Status   │ Origin   │ Dest    │ ETA    │ ⋮   │ │
│  │───┼──────────┼──────────┼──────────┼─────────┼────────┼─────│ │
│  │ □ │ SHP-001  │ ● Active │ VNHPH    │ USLAX   │ 15/04  │ ⋮   │ │
│  │ □ │ SHP-002  │ ○ Draft  │ VNSGN    │ JPOSA   │ 20/04  │ ⋮   │ │
│  │ □ │ SHP-003  │ ● Active │ VNHPH    │ KRPUS   │ 22/04  │ ⋮   │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  Showing 1-20 of 156              [< Prev] [1] [2] [3] [Next >]  │
└────────────────────────────────────────────────────────────────────┘
```

Rules:
- Quick search always visible at top
- Advanced search panel (F3 toggle) collapsed by default
- Create button ("+ Thêm") always top-right
- Table has checkbox column for bulk actions
- Row actions via "⋮" menu (not inline buttons)
- Pagination at bottom

### Pattern 2: Form Dialog

**Use when:** ≤6 fields, blocking action (user must act before continuing), no URL needed, action completes in <1 minute. Both Create and Edit use this pattern together.

```
┌─────────────────────────────────────────────────────┐
│  [Dialog Title]                                   ✕  │
│─────────────────────────────────────────────────────│
│                                                      │
│  Field 1 *                                           │
│  [________________________________]                  │
│                                                      │
│  Field 2 *                    Field 3                │
│  [▼______________]            [_______________]      │
│                                                      │
│  Field 4                                             │
│  [________________________________]                  │
│  (i) Helper text explaining the field                │
│                                                      │
│─────────────────────────────────────────────────────│
│                                [Huỷ]    [Lưu]       │
└─────────────────────────────────────────────────────┘
```

Rules:
- Dialog title describes the action (e.g., "Tạo Booking mới")
- Required fields marked with *
- 2-column layout for related short fields, 1-column for long fields
- Helper text with (i) icon for fields that need explanation
- Action buttons at bottom-right: Cancel (secondary) + Save (primary)

### Pattern 2b: Drawer / Side Sheet

**Use when:** 7–15 fields, user needs list context while filling the form, action takes 1–3 minutes, no URL needed. Also used for quick-view preview when clicking a row without navigating away. Both Create and Edit use this pattern together.

```
┌──────────────────────┬─────────────────────────────────────────┐
│  [Module] > [Feature]│  Tạo [Entity] mới                    ✕  │
│                      │─────────────────────────────────────────│
│  ┌────────────────┐  │                                          │
│  │ 🔍 Quick search│  │  Section (optional grouping)             │
│  └────────────────┘  │                                          │
│                      │  Field 1 *          Field 2              │
│  ┌────────────────┐  │  [▼______________]  [_______________]    │
│  │ □ Code  │ ⋮   │  │                                          │
│  │ SHP-001 │ ⋮   │  │  Field 3 *                               │
│  │ SHP-002 │ ⋮   │  │  [________________________________]       │
│  │ SHP-003 │ ⋮   │  │                                          │
│  └────────────────┘  │  Field 4            Field 5              │
│                      │  [📅 Date________]  [▼______________]    │
│  1-20 of 156         │                                          │
│  [< 1 2 3 >]         │  Field 6                                 │
│                      │  [________________________________]       │
│                      │  (i) Helper text                         │
│                      │                                          │
│                      │─────────────────────────────────────────│
│                      │                       [Huỷ]    [Lưu]    │
└──────────────────────┴─────────────────────────────────────────┘
```

Rules:
- Drawer slides in from the right, list remains visible and scrollable on the left
- Drawer width: ~480px fixed (desktop), full-screen on mobile
- Title describes the action; ✕ closes without saving
- Section headings optional — use when fields group into logical clusters
- Action buttons pinned to drawer footer
- Do not open a second drawer from within a drawer — use a dialog instead

### Pattern 3: Detail View (Master-Detail)

**Use when:** Entity has a URL (share/bookmark), entity has lifecycle with tabs or sub-data (documents, milestones, costs, activity log), user spends >3 minutes on screen, or sub-actions navigate to further screens. Edit is done via inline edit mode within this same page — not by reopening a Drawer or Dialog.

```
┌──────────────────────────────────────────────────────────────────┐
│  ← Back to list    Shipment SHP-001             [Edit] [⋮ More] │
│  Status: ● In Transit                                            │
│──────────────────────────────────────────────────────────────────│
│  [Overview] [Documents] [Milestones] [Costs] [Activity Log]     │
│──────────────────────────────────────────────────────────────────│
│                                                                  │
│  ┌─ General Information ──────────────────────────────────────┐  │
│  │  Origin: VNHPH          Destination: USLAX                │  │
│  │  Carrier: MAERSK        Vessel: MAERSK ELBA               │  │
│  │  ETD: 01/04/2026        ETA: 22/04/2026                   │  │
│  │  Container: MSKU1234567 (40HC)                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌─ Milestones ──────────────────────────────────────────────┐  │
│  │  ✓ Booking Confirmed     01/04 09:00                      │  │
│  │  ✓ Container Picked Up   03/04 14:30                      │  │
│  │  ✓ Gate In (POL)         04/04 08:00                      │  │
│  │  ● Vessel Departed       05/04 16:00                      │  │
│  │  ○ Vessel Arrived        — (ETA: 20/04)                   │  │
│  │  ○ Customs Cleared       —                                │  │
│  │  ○ Delivered             —                                │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

Rules:
- Back link + entity title + status badge at top
- Tab navigation for different aspects of the entity
- Read-only sections by default, Edit button switches the page to inline edit mode
- Timeline/milestone visualization for entities with lifecycle
- URL changes when navigating to this view (enables share/bookmark)

### Pattern 4: Multi-Step Wizard

For complex creation flows (e.g., creating a booking with multiple legs):

```
┌───────────────────────────────────────────────────────────────────┐
│  Tạo Booking mới                                              ✕   │
│───────────────────────────────────────────────────────────────────│
│                                                                   │
│  Step 1          Step 2          Step 3          Step 4           │
│  ● Thông tin     ○ Hàng hoá     ○ Vận chuyển    ○ Xác nhận      │
│  ─────●─────────────○──────────────○──────────────○──────        │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  [Step content goes here]                                   │ │
│  │                                                             │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│───────────────────────────────────────────────────────────────────│
│  [Quay lại]                                       [Tiếp theo]    │
└───────────────────────────────────────────────────────────────────┘
```

Rules:
- Step indicator at top with current step highlighted
- Back/Next buttons at bottom
- Final step has "Xác nhận" (Confirm) instead of "Tiếp theo"
- Allow jumping to completed steps by clicking the step indicator

### Pattern 5: Full-Page Multi-Step Form with Side Progress Panel

For complex creation flows where all sections need to be visible simultaneously
(e.g., creating an order with cross-referencing fields across sections):

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  [Module] > [Feature] > Create [Entity]             [Cancel]  [Create Order]│
│─────────────────────────────────────────────────────────────────────────────│
│                                                                              │
│  ┌──────────────────────────────────────────┐  ┌─────────────────────────┐  │
│  │                                          │  │  Order Progress         │  │
│  │  1  Section Title              * required│  │  ─────────────────────  │  │
│  │  ┌──────────────────────────────────────┐│  │  ● 1  Section One       │  │
│  │  │ Field A *       Field B              ││  │     field a, b, c       │  │
│  │  │ [▼ Select____]  [▼ Normal_______]    ││  │                         │  │
│  │  │ Field C         Field D              ││  │  ○ 2  Section Two       │  │
│  │  │ [___________]   [_______________]    ││  │     field x, y          │  │
│  │  └──────────────────────────────────────┘│  │                         │  │
│  │                                          │  │  ○ 3  Section Three     │  │
│  │  2  Section Title              * required│  │     field p, q          │  │
│  │  ┌──────────────────────────────────────┐│  │                         │  │
│  │  │ Field X *       Field Y (Optional)   ││  │  ○ 4  Section Four      │  │
│  │  │ [▼ Select____]  [_______________]    ││  │     notes               │  │
│  │  └──────────────────────────────────────┘│  └─────────────────────────┘  │
│  └──────────────────────────────────────────┘                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

Rules:
- Full-page layout (not a dialog/modal)
- Two-column: scrollable form sections (left) + fixed progress panel (right)
- Sections numbered sequentially (1, 2, 3...) and scroll continuously — no step-by-step navigation
- Progress panel is sticky; shows all sections with short field descriptions
- Step indicator: ● = current/active section, ○ = pending
- Primary action buttons (Cancel + Submit) at top-right of page header
- Use over Pattern 4 (dialog wizard) when: form has 10+ fields, sections need cross-referencing, or all data must be reviewable before submit

## Wireframe File Structure

Each wireframe file should follow this structure:

```markdown
# [Feature Name] — Wireframes

## WF-01: [Screen Name]

**Context**: [Who sees this, how they get here, what precondition]

\`\`\`
[ASCII wireframe]
\`\`\`

**Annotations:**
- **A1**: [Explanation of a specific element]
- **A2**: [Explanation of another element]

---

## WF-02: [Next Screen]
...

---

## State Variations

### When [condition]
[How the wireframe changes]

---

## Interaction Notes

| # | Interaction | Behavior |
|---|-------------|----------|
| I-01 | [Trigger] | [What happens] |
```

## Important UX Rules

1. **Create button always top-right** — next to search/filter controls
2. **No custom empty states** unless the user specifies one
3. **No Export button** unless explicitly requested
4. **Search panel collapsed by default** — toggle via button or F3 shortcut
5. **Row actions via ⋮ menu** — don't clutter the table with inline action buttons
6. **Status badges**: Use ● (filled circle) for active states, ○ (empty circle) for inactive/pending
7. **Responsive consideration**: Design for desktop-first (1280px+), note mobile adaptations only if the feature has mobile scope
