# Portal Update Log

**Purpose:** Running record of every change pushed to any client-facing portal.
**Rule:** Every deliverable ships → portal updated → this log entry added. No exceptions.
**Format:** Date | Portal | What Changed | Pushed to GitHub (Y/N)

---

## How Portals Work

| Client | Portal Type | Source File | Live URL |
|---|---|---|---|
| All South SEO | GitHub Pages | `all-south-lightning/reports.json` | https://nichefinder1.github.io/client-portals/all-south-lightning/ |
| All South AIOS | GitHub Pages | `all-south-lightning-aios/program.json` | https://nichefinder1.github.io/client-portals/all-south-lightning-aios/ |
| Fox Valley | GitHub Pages | `fox-valley-plumbing/reports.json` | https://nichefinder1.github.io/client-portals/fox-valley-plumbing/ |
| iCare Foundation | Netlify (iCare's account) | `icare-foundation/program.json` | https://icaregives.org (separate) |

**Portal update = edit JSON → git commit → git push → GitHub Pages live within 1–2 min.**

---

## Update Log

### 2026-04-26
| Portal | What Changed | Pushed |
|---|---|---|
| All South AIOS | `program.json` — Week 5 session added (trade show video + triage demo), current_week updated to 5, phase description updated to reflect IT admin consent complete | ✅ Yes |
| Fox Valley SEO | `reports.json` — content_execution block corrected: blog_posts 0→12, social_posts 0→84, press_releases 0→1, backlinks 0→30. last_updated → 2026-04-26. JSON now matches Q1 reality. | ✅ Yes — ef8a482 |

### 2026-04-23
| Portal | What Changed | Pushed |
|---|---|---|
| All South AIOS | `program.json` — Trade show commercial video status → "live", deployed_date: 2026-04-23. Week 5 session added. last_updated: 2026-04-23 | ✅ Yes |
| Fox Valley | `DELIVERY_SCORECARD.md` — Microsoft Clarity installed (all 246 pages), Netlify deploy incident resolved | Local only |

### 2026-04-13
| Portal | What Changed | Pushed |
|---|---|---|
| All South SEO | GBP Posts — Sunrise + JAX (14 posts) added to completed deliverables. Citation Build Plan added. Local Dominator keywords added. | Local only — needs push |

### 2026-04-12
| Portal | What Changed | Pushed |
|---|---|---|
| Fox Valley | Monthly Progress Report — Mar 2026 added to portal. Press release (BBB A+) published on EINPresswire. | ✅ Yes |

### 2026-04-10
| Portal | What Changed | Pushed |
|---|---|---|
| All South AIOS | `program.json` — Week 2 session details added. Business process mapping documented. Automation pick confirmed: email triage #1. | ✅ Yes |

### 2026-04-01
| Portal | What Changed | Pushed |
|---|---|---|
| All South SEO | `reports.json` — ZooTampa press release added to completed deliverables + distribution URL. press_releases_published → 1. | ✅ Yes |

### 2026-03-26
| Portal | What Changed | Pushed |
|---|---|---|
| All South AIOS | `program.json` — Week 1 session added. Program status set to active. | ✅ Yes |

### 2026-03-21
| Portal | What Changed | Pushed |
|---|---|---|
| All South AIOS | Portal live. `program.json` seeded with initial program data, all 6 quick wins, key discoveries. | ✅ Yes |

### 2026-03-11
| Portal | What Changed | Pushed |
|---|---|---|
| All South SEO | `reports.json` — Local SEO Roadmap, LLM Visibility Analysis, Tampa Keywords published. GBP Audit resolved. 17/22 keyword scan results added. GBP Setup Checklist Phase 1 marked complete. | ✅ Yes |
| Fox Valley | `reports.json` — LLM Visibility Analysis updated, Local Dominator Rankings updated (26 keywords improved). | ✅ Yes |

### 2026-03-10
| Portal | What Changed | Pushed |
|---|---|---|
| Fox Valley | Portal live (8 pages). `reports.json` seeded. GBP Audit, GBP Checklist, LLM Analysis, Local Dominator published. | ✅ Yes |

### 2026-02-13
| Portal | What Changed | Pushed |
|---|---|---|
| Fox Valley | BBB A+ Accreditation earned — added to key findings. GBP score updated D+ → A-. | ✅ Yes |

### 2026-02-04
| Portal | What Changed | Pushed |
|---|---|---|
| All South SEO | GBP Audit published. Tampa GBP score 42/100 documented. Revenue gap identified ($150K–$400K/yr). | ✅ Yes |
| Fox Valley | GBP Audit published. Score 37/70 (D+) documented. All critical issues resolved. | ✅ Yes |

---

## Pending Portal Updates (Not Yet Pushed)

| Portal | What Needs Updating | Priority |
|---|---|---|
| Fox Valley SEO | `reports.json` — blog_posts_published → 12, social_posts_published → 84, backlinks_built → 30+, press_releases_published → 1. Data is stale showing 0 across all Q1 metrics. | HIGH |
| All South SEO | `reports.json` — last_updated → 2026-04-26. GBP Posts Sunrise + JAX status → "Ready to publish". Citation build in progress. | HIGH |
| All South AIOS | `program.json` — upcoming_session date → TBD (Week 6). Email triage status note updated: IT admin consent complete, Chuck OAuth is only remaining step. | MEDIUM |
| All South AIOS | After Week 6 call: current_week → 6, session log Week 6 added, email triage status → "live", upcoming_session → Week 7 | Week 6 call |

---

## Portal Update Checklist (Every Deliverable)

After any deliverable ships, complete in order:
- [ ] Edit source JSON file (reports.json or program.json)
- [ ] Update `last_updated` field to today's date
- [ ] Add entry to this log (PORTAL_UPDATE_LOG.md)
- [ ] Git commit with message: `portal: [client] — [what changed]`
- [ ] Git push → GitHub Pages live
- [ ] Update DELIVERY_SCORECARD.md "Portal Updated" column → ✅ Yes
