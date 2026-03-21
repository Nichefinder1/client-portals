# NicheFinders AI OS Partner Program Portal — Template

The client-facing dashboard for every AI OS Partner Program engagement.
Data-driven: edit `program.json` only — the HTML never needs to touch.

---

## Setup for a New Client

1. Copy this entire folder to `company/client-portals/[client-slug]/`
2. Rename `program.json` entries — replace all `[CLIENT NAME]`, `[Industry Type]`, `[client-slug]`
3. Set `program_type` to `"founding"` (6 months) or `"standard"` (3 months)
4. Set `total_weeks` to `24` or `12` accordingly
5. Push the folder to `Nichefinder1/client-portals` repo under `/[client-slug]/`
6. Share the GitHub Pages URL with the client: `https://nichefinder1.github.io/client-portals/[client-slug]/`

---

## Weekly Update Workflow (After Every Session)

Edit `program.json` only:

1. **Increment** `current_week`
2. **Update** `overview.current_phase` and `phase_description`
3. **Update** `overview.overall_progress_pct` (0–100)
4. **Update** pillar `status` and `progress_pct` for each of the three pillars
5. **Update** individual item `status` values: `not_started` → `in_progress` → `complete`
6. **Add** a new entry to the `sessions` array (see schema below)
7. **Update** `upcoming_session` with next week's details
8. **Update** `client.last_updated` to today's date
9. Push to GitHub — portal updates live immediately

---

## Session Array Schema

```json
{
  "week": 1,
  "label": "Week 1: Kickoff",
  "date": "March 25, 2026",
  "topics": ["Business walkthrough", "Team introductions", "Pain point mapping"],
  "decisions": "Top priority: lead intake automation. Brain install scheduled Week 3.",
  "next_steps": "Corey: SOP gap analysis. Client: send org chart and current process docs."
}
```

---

## Pillar Item Status Values

| Value         | Meaning                        | Display         |
|---------------|--------------------------------|-----------------|
| `not_started` | Not yet touched                | Empty circle    |
| `in_progress` | Currently being mapped/built   | Clock icon      |
| `complete`    | Fully mapped or built          | Check icon      |

## Quick Win Status Values

| Value         | Meaning                        |
|---------------|--------------------------------|
| `pending`     | Not yet identified or started  |
| `in_progress` | Being built                    |
| `live`        | Deployed and running           |

---

## All South Lightning (Client #1)

- Slug: `all-south-lightning-blueprint`
- Program type: `founding` (6 months, $2,500/mo)
- Start date: TBD — portal ready, kickoff scheduling in progress
