# Client Portal URLs

Quick reference for all client portal links.

*Last Updated: April 4, 2026*

---

## Portal Structure SOP

**Every client gets separate portals per service — never combine:**

| Portal Type | Slug Pattern | Purpose |
|-------------|-------------|---------|
| SEO / Retainer | `[slug]/` | Monthly deliverables, GBP metrics, reports, press releases |
| AI OS Program | `[slug]-aios/` | Program progress, Brain access, session log, automations |

A client can have one or both. All South has both (retainer + AIOS program).

---

## Active Portals

| Client | Service | Portal URL | Status |
|--------|---------|------------|--------|
| Fox Valley Plumbing & Backflow | SEO Retainer | [View Portal](https://nichefinder1.github.io/client-portals/fox-valley-plumbing/) | Active |
| All South Lightning Protection | SEO Retainer | [View Portal](https://nichefinder1.github.io/client-portals/all-south-lightning/) | Active |
| All South Lightning Protection | AI OS Program | [View Portal](https://nichefinder1.github.io/client-portals/all-south-lightning-aios/) | Active |

---

## Fox Valley Plumbing & Backflow

**SEO Retainer Portal:** https://nichefinder1.github.io/client-portals/fox-valley-plumbing/

### Dashboard
| Page | URL |
|------|-----|
| Main Dashboard | https://nichefinder1.github.io/client-portals/fox-valley-plumbing/ |

### One-Time Reports
| Report | URL |
|--------|-----|
| GBP Audit | https://nichefinder1.github.io/client-portals/fox-valley-plumbing/GBP_Audit.html |
| GBP Optimization Checklist | https://nichefinder1.github.io/client-portals/fox-valley-plumbing/GBP_Optimization_Checklist.html |
| Website Optimization Roadmap | https://nichefinder1.github.io/client-portals/fox-valley-plumbing/Website_Optimization_Roadmap.html |
| LLM Visibility Analysis | https://nichefinder1.github.io/client-portals/fox-valley-plumbing/LLM_Visibility_Analysis.html |
| Local Dominator Rankings | https://nichefinder1.github.io/client-portals/fox-valley-plumbing/LOCAL_DOMINATOR_BASELINE_JAN_2026.html |
| Service FAQs | https://nichefinder1.github.io/client-portals/fox-valley-plumbing/Service_FAQs.html |
| Press Release Intake | https://nichefinder1.github.io/client-portals/fox-valley-plumbing/Press_Release_Intake.html |

### Monthly Reports
| Month | URL |
|-------|-----|
| February 2026 | https://nichefinder1.github.io/client-portals/fox-valley-plumbing/2026-02/Monthly_Progress_Report_Feb_2026.html |
| March 2026 | https://nichefinder1.github.io/client-portals/fox-valley-plumbing/2026-03/Monthly_Progress_Report_Mar_2026.html |

**Total pages:** 10

---

## All South Lightning Protection — SEO Retainer

**Portal:** https://nichefinder1.github.io/client-portals/all-south-lightning/
**Data file:** `all-south-lightning/reports.json`

### Dashboard
| Page | URL |
|------|-----|
| Main Dashboard | https://nichefinder1.github.io/client-portals/all-south-lightning/ |

### One-Time Reports
| Report | URL |
|--------|-----|
| GBP Audit (Multi-Location) | https://nichefinder1.github.io/client-portals/all-south-lightning/GBP_Audit.html |
| Local SEO Roadmap | https://nichefinder1.github.io/client-portals/all-south-lightning/Local_SEO_Roadmap.html |
| LLM Visibility Analysis | https://nichefinder1.github.io/client-portals/all-south-lightning/LLM_Visibility_Analysis.html |
| Tampa Keywords | https://nichefinder1.github.io/client-portals/all-south-lightning/Tampa_Keywords.html |
| GBP Copy Kit v2.0 | https://nichefinder1.github.io/client-portals/all-south-lightning/GBP_UPDATE_CONTENT_AGENCY.html |
| Press Release Intake | https://nichefinder1.github.io/client-portals/all-south-lightning/Press_Release_Intake.html |

### Monthly Reports
| Month | URL |
|-------|-----|
| February 2026 Deliverables | https://nichefinder1.github.io/client-portals/all-south-lightning/February_2026_Deliverables.html |
| March 2026 | Due March 31 (not yet built) |

**Total pages:** 9

---

## All South Lightning Protection — AI OS Partner Program

**Portal:** https://nichefinder1.github.io/client-portals/all-south-lightning-aios/
**Data file:** `all-south-lightning-aios/program.json`

### Pages
| Page | URL |
|------|-----|
| Program Dashboard | https://nichefinder1.github.io/client-portals/all-south-lightning-aios/ |
| Week 2 Session Agenda | https://nichefinder1.github.io/client-portals/all-south-lightning-aios/AIOS_Week2_Agenda.html |

**Total pages:** 2 (grows as sessions complete)

---

## URL Pattern

```
SEO/Retainer:   https://nichefinder1.github.io/client-portals/[client-slug]/
AI OS Program:  https://nichefinder1.github.io/client-portals/[client-slug]-aios/
```

## Adding New Clients

**SEO Retainer portal:**
1. Create `company/client-portals/[slug]/`
2. Add `index.html` + `reports.json`
3. Add entry to this file under both Active Portals table and its own section
4. Push to `Nichefinder1/client-portals`

**AI OS Program portal:**
1. Copy `_AIOS-PARTNER-TEMPLATE/` to `[slug]-aios/`
2. Customize `program.json` — client name, slug, program type
3. Add entry to this file
4. Push to `Nichefinder1/client-portals`

## Data-Driven Architecture

- **SEO portals:** `index.html` fetches `reports.json` at page load — edit JSON → push → dashboard updates
- **AIOS portals:** `index.html` fetches `program.json` at page load — edit JSON → push → dashboard updates
- Monthly reports go in `YYYY-MM/` subfolders
- Update tool: `python3 portal-update.py` (from SEO portal directory)
