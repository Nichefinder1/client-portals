# Monthly Portal Update Workflow

## Quick Reference (2 minutes per client)

```bash
# 1. Add new month folder with reports
mkdir fox-valley-plumbing/2026-03

# 2. Copy report template and fill in data
cp templates/Monthly_Progress_Report.html fox-valley-plumbing/2026-03/Monthly_Progress_Report_Mar_2026.html

# 3. Edit reports.json (add new month, update metrics)
# 4. Regenerate portal
./update-portal.sh fox-valley-plumbing

# 5. Deploy
git add . && git commit -m "March 2026 reports" && git push
```

---

## Detailed Monthly Steps

### Step 1: Create New Month Folder

```bash
cd /Users/nichefinder/Desktop/Nichefinder\ AI\ Agency/company/client-portals
mkdir fox-valley-plumbing/2026-03
```

### Step 2: Add Report Files

Copy and customize report templates:
- Monthly_Progress_Report_[Month]_2026.html
- Ranking_Movement_Report_[Month]_2026.html (if applicable)

### Step 3: Update reports.json

Open `fox-valley-plumbing/reports.json` and:

**A. Update metrics at top:**
```json
"metrics": {
    "keywords_at_1": 15,        // ← Update from LocalDominator
    "goal_progress": 26,        // ← Recalculate: (15/58)*100
    "organic_clicks": "1,847",  // ← Update from Search Console
    "reviews": 128              // ← Update from GBP
}
```

**B. Move current month to archive (change is_current to false):**
```json
{
    "month": "2026-02",
    "month_name": "February 2026",
    "is_current": false,         // ← Change to false
    "reports": [...]
}
```

**C. Add new month at TOP of monthly_reports array:**
```json
"monthly_reports": [
    {
        "month": "2026-03",
        "month_name": "March 2026",
        "is_current": true,
        "reports": [
            {
                "title": "Monthly Progress Report",
                "file": "2026-03/Monthly_Progress_Report_Mar_2026.html",
                "description": "Complete overview of work completed, metrics, and next steps.",
                "badge": "NEW",
                "badge_color": "red"
            }
        ]
    },
    // ... previous months stay below
]
```

### Step 4: Regenerate Portal

```bash
./update-portal.sh fox-valley-plumbing
```

Or for all clients:
```bash
./update-portal.sh
```

### Step 5: Deploy to GitHub Pages

```bash
git add .
git commit -m "Add March 2026 reports for Fox Valley Plumbing"
git push
```

Site updates automatically within 1-2 minutes.

---

## Monthly Checklist

- [ ] Create month folder (e.g., `2026-03/`)
- [ ] Add Monthly Progress Report
- [ ] Add Ranking Movement Report (if applicable)
- [ ] Update metrics in reports.json
- [ ] Mark previous month as `is_current: false`
- [ ] Add new month with `is_current: true`
- [ ] Run `./update-portal.sh [client]`
- [ ] Commit and push to GitHub
- [ ] Verify live site updated

---

## Badge Colors Reference

| Color | Use For |
|-------|---------|
| `red` | NEW reports |
| `green` | UPDATED, Complete, Success |
| `blue` | Coming Soon, In Progress |
| `purple` | One-Time, Strategy, Baseline |
| `orange` | Warning, Attention needed |
| `gray` | Pending, Not started |
| `teal` | Checklists |

---

## File Structure

```
client-portals/
├── generate-portal.py      # Main generator script
├── update-portal.sh        # Quick update wrapper
├── MONTHLY_WORKFLOW.md     # This file
├── README.md               # General docs
│
├── fox-valley-plumbing/
│   ├── reports.json        # ← Edit this monthly
│   ├── index.html          # ← Auto-generated
│   ├── GBP_Audit.html
│   ├── [other reports...]
│   ├── 2026-01/
│   ├── 2026-02/
│   │   └── Monthly_Progress_Report_Feb_2026.html
│   └── 2026-03/            # ← Add each month
│       └── Monthly_Progress_Report_Mar_2026.html
│
└── [other-clients]/
    └── [same structure]
```

---

## Adding a New Client

1. Create client folder with URL-friendly name:
   ```bash
   mkdir new-client-name
   ```

2. Copy reports.json template:
   ```bash
   cp fox-valley-plumbing/reports.json new-client-name/
   ```

3. Edit reports.json with client details

4. Add report HTML files

5. Generate portal:
   ```bash
   ./update-portal.sh new-client-name
   ```

6. Add client card to main index.html (root level)

7. Commit and push
