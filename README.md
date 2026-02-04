# Nichefinder AI - Client Portals

This repository hosts client-facing reports and dashboards for Nichefinder AI Agency clients.

## Live Site

**URL:** https://nichefinder1.github.io/client-portals/

## Structure

```
client-portals/
├── index.html                    # Main portal listing all clients
├── fox-valley-plumbing/          # Fox Valley Plumbing & Backflow
│   ├── index.html                # Client dashboard
│   ├── GBP_Audit.html
│   ├── GBP_Optimization_Checklist.html
│   ├── LLM_Visibility_Analysis.html
│   ├── Website_Optimization_Roadmap.html
│   ├── LOCAL_DOMINATOR_BASELINE_JAN_2026.html
│   └── 2026-02/
│       └── Monthly_Progress_Report_Feb_2026.html
└── [future-client]/              # Additional clients
```

## Adding New Clients

1. Create a new folder with URL-friendly client name (lowercase, hyphens)
2. Copy `index.html` template and customize
3. Add client card to main `index.html`
4. Commit and push

## Updating Reports

1. Add new HTML files to client folder
2. Update client's `index.html` with new links
3. Commit and push

## GitHub Pages Setup

This site is hosted via GitHub Pages from the `main` branch.

**Settings:** Repository Settings → Pages → Source: Deploy from branch (main)

---

*Maintained by Nichefinder AI Agency*
