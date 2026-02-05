# Nichefinder AI - Client Portals

Client-facing report portals hosted on GitHub Pages.

## Live Site

**URL:** https://nichefinder1.github.io/client-portals/

## Quick Commands

```bash
# Update a specific client portal
./update-portal.sh fox-valley-plumbing

# Update all client portals
./update-portal.sh

# Deploy changes
git add . && git commit -m "Update reports" && git push
```

## Monthly Updates

See **[MONTHLY_WORKFLOW.md](MONTHLY_WORKFLOW.md)** for detailed steps.

**Quick version (2 min per client):**
1. Add report files to new month folder
2. Edit `reports.json` (update metrics, add new month)
3. Run `./update-portal.sh [client]`
4. `git add . && git commit && git push`

## Structure

```
client-portals/
├── generate-portal.py      # Portal generator script
├── update-portal.sh        # Quick update wrapper
├── MONTHLY_WORKFLOW.md     # Monthly update guide
├── index.html              # Main portal (all clients)
│
└── fox-valley-plumbing/
    ├── reports.json        # Client config (edit monthly)
    ├── index.html          # Generated portal
    ├── [report files...]
    └── 2026-02/
        └── Monthly_Progress_Report_Feb_2026.html
```

## How It Works

1. **reports.json** - Contains all client data, metrics, and report links
2. **generate-portal.py** - Reads JSON, generates index.html
3. **GitHub Pages** - Hosts the static HTML files

## Features

- PDF download button on every report
- Print button on every report
- Archive section for historical reports
- Mobile responsive
- No backend required ($0 hosting)

---

*Maintained by Nichefinder AI Agency*
