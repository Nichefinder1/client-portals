<original_task>
Complete iCare Foundation board portal document lifecycle — ensure all governance documents (bylaws, COI, NDA, board agreement) can be downloaded, signed, and re-uploaded. Replace placeholder docs with official versions. Deploy portal.
</original_task>

<work_completed>

## This Session — April 29, 2026 (Evening)

### 1. Official Documents Added to Portal
Received and placed 3 real documents into `docs/` directory:
- `ICARE_Conflict_of_Interest_Final.pdf` (2.7K) — official COI form aligned with bylaws, replaced generated placeholder
- `ICARE_Board_NDA.docx` (36.6K) — new addition, board member NDA
- `iCARE_Board_Member_Agreement.docx` (36.4K) — official version replacing generated placeholder

Previous session already added:
- `iCARE_Bylaws_Final.pdf` (53.5K) — real bylaws

Removed placeholder file: `iCARE_Conflict_of_Interest_Form.docx`

### 2. Portal HTML Updated (`index.html`)
- **COI download link** — changed from `docs/iCARE_Conflict_of_Interest_Form.docx` to `docs/ICARE_Conflict_of_Interest_Final.pdf`, updated meta text from "Word doc" to "PDF"
- **NDA row added** — new doc-row in Agreements folder with download link to `docs/ICARE_Board_NDA.docx`
- **Folder title** — changed from "Board Agreements & Conflict of Interest Forms" to "Board Agreements, COI & NDA"
- **Folder count** — changed from "2 documents" to "3 documents"
- **Upload dropdown** — added `<option value="nda">Board Member NDA</option>`
- **JS DOC_TYPE_LABELS** — added `'nda': 'Board Member NDA'`

### 3. Deployed to Production
- Switched Netlify auth from nichefindersai@gmail.com → icaregives@gmail.com (Rhonda Marie)
- Deployed: `netlify deploy --prod --dir=. --site=602a70e6-590b-43c8-bf85-6c822b237f39`
- Live at: **membersportal.icaregives.org**
- Deploy ID: `69f2ce1560f36bb671066954`

### 4. Git Backup Pushed
- Switched GitHub to iCareGives account
- Committed: "Add document lifecycle: download, sign, re-upload for all governance docs"
- Pushed to `main` on iCareGives/icare-foundation repo
- Switched back to Nichefinder1 GitHub account

### 5. Publix Grant Denial Processed
- **GRANT_PIPELINE.md** — Publix status changed to ❌ DENIED, reason: "Requires 4+ years of operation. iCARE incorporated ~1 year (IRS determination May 2025). Reapply 2029 at earliest."
- Food Security summary table updated with strikethrough
- Fixed 990-EZ → 990-N reference (line 156)
- Updated Last Updated date to 2026-04-29

### 6. Grant Writer Skill Hardened
- **Pre-flight step 3 added**: CHECK HARD ELIGIBILITY FIRST
  - Minimum years of operation
  - Minimum annual budget
  - Geographic restrictions
  - Organization type exclusions
  - Prior grant history requirements
  - If ANY fails → STOP immediately, don't draft

### 7. Error Pattern Logged
- Added entry to `context/error-patterns.md`: Grant eligibility not checked before drafting Publix application

</work_completed>

<work_remaining>

## Netlify Account
1. **Switch Netlify CLI back to agency account** — run `netlify switch` and select nichefindersai@gmail.com. CLI crashed on interactive prompt during session; user needs to do manually: `! netlify switch`

## This Week
2. **Florida Annual Report** — Due May 1. File at sunbiz.org, $61.25. Rhonda files.
3. **Update DELIVERY_SCORECARD.md** — Stale. Needs:
   - Change "990-EZ Prep Document" to "990-N Prep"
   - Update in-kind from "$5,599.99+" to "$14,419.70"
   - Add row: Publix Charities grant application (completed April 29 — DENIED)
   - Add row: Grant writer skill (completed April 29)
   - Add row: Board portal document lifecycle (completed April 29)
   - Remove "Sep–Dec bank records" blocker (resolved)
   - Remove "Collins paid or in-kind?" blocker (resolved — confirmed in-kind $200)
   - Remove "Regina's fans fair market value" blocker (resolved — fans removed, total $3,026.70)

## Before May 15
4. **File IRS Form 990-N** — irs.gov/charities, ~10 min. EIN 92-3071148, tax year Jan 1–Dec 31 2025. Check "Initial Return." Gross receipts ≤ $50K. Principal officer: Rhonda Reeder.
5. **Create GuideStar/Candid profile** — After 990-N filed. Free at candid.org. Unblocks grant credibility.

## Overdue
6. **Process April 11 board meeting transcript** — Corey needs to share Gemini transcript. Parse → decisions, motions, action items → update portal program.json → deploy. See `clients/iCare Foundation/notes/gemini-transcript-workflow.md`
7. **Cedrick & Joseph portal invites** — Check if expired, resend from Netlify Identity dashboard
8. **Send portal URL to all board members** — After all 5 confirmed: membersportal.icaregives.org

## Next Grants (APPLY HARD ELIGIBILITY CHECK FIRST)
9. **Wawa Foundation** — Quarterly, $2,500+. Research next open window. CHECK: years-of-operation requirement
10. **Bank of America Empowering Communities RFP** — Opens May 18. CHECK: eligibility before drafting
11. **Community Foundation Tampa Bay** — Cycle opens Dec 1. Start relationship NOW. CHECK: eligibility
12. **Register SAM.gov** — Unlocks all federal grants. Free, annual renewal.

## Longer Term
13. **52-week email calendar** — After board meeting processed
14. **Upgrade Resend to Pro** ($20/mo) when subscriber list approaches 750
15. **Obsidian vault update** — Not done this session. Update iCare project note.

</work_remaining>

<attempted_approaches>

### Netlify Account Switching
- `netlify switch` — crashes with "Detected unsettled top-level await" error on interactive prompt. Known CLI bug. Workaround: `netlify logout` then `netlify login` and authenticate via browser.
- `netlify link --id 602a70e6...` — fails with "Project id not found" when logged in as nichefindersai@gmail.com (agency account can't see iCare's site)
- Successful approach: `netlify logout` → `netlify login` → open auth URL in Chrome incognito (where icaregives@gmail.com was logged in) → authorize → deploy works

### Chrome Auth Caching
- Default Chrome browser cached nichefindersai@gmail.com Netlify session
- User had icaregives@gmail.com in incognito
- Solution: `open -na "Google Chrome" --args --incognito "<auth-url>"` to force incognito window

</attempted_approaches>

<critical_context>

### iCare Eligibility Reality
- **IRS Determination Date: May 15, 2025** — iCARE is approximately 1 year old
- Many funders require 2–4+ years of operation
- ALL future grant applications MUST check org-age eligibility before drafting
- Earliest Publix reapply: 2029
- Grant writer skill pre-flight now enforces this check

### iCare Infrastructure
- ALL infra is CLIENT-OWNED (iCareGives GitHub, icaregives@gmail.com Netlify, iCare's Airtable)
- Deploy: `netlify deploy --prod --dir=. --site=602a70e6-590b-43c8-bf85-6c822b237f39`
- Must switch to iCare accounts before deploy/push, switch back after
- GitHub: `gh auth switch --user iCareGives` → work → `gh auth switch --user Nichefinder1`
- Portal URL: membersportal.icaregives.org
- NEVER reference 990-EZ — iCare files 990-N only
- Corporate turkey donor = always "Corporate donor"

### Netlify CLI State
- Currently logged in as **icaregives@gmail.com** (Rhonda Marie) — needs to be switched back to nichefindersai@gmail.com
- `netlify switch` command crashes — use logout/login flow instead

### Document Lifecycle (Complete)
- 4 docs in `docs/`: Bylaws (PDF), Board Agreement (Word), COI (PDF), NDA (Word)
- Upload: Netlify Forms, 8MB limit, PDF/JPG/PNG/Word accepted
- localStorage persists upload metadata (per-device limitation)
- Netlify Function `list-uploads.js` built for future server-side listing (needs NETLIFY_API_TOKEN env var on iCare's Netlify account)

</critical_context>

<current_state>

| Item | Status |
|------|--------|
| Portal document lifecycle (download/upload) | ✅ Complete + deployed |
| All 4 official docs in place | ✅ Complete (no placeholders) |
| Portal deployed to production | ✅ Live at membersportal.icaregives.org |
| Git backup pushed | ✅ On iCareGives/icare-foundation main |
| GitHub switched back to Nichefinder1 | ✅ Done |
| Netlify switched back to agency account | ⬜ NOT DONE — still on icaregives@gmail.com |
| Publix grant pipeline updated (denied) | ✅ Done |
| Grant writer skill hardened | ✅ Eligibility check added |
| Error pattern logged | ✅ Done |
| DELIVERY_SCORECARD.md | ⬜ Stale — needs multiple fixes |
| Obsidian vault update | ⬜ Not done this session |

**Next action:** Switch Netlify back to agency account (`! netlify switch` or logout/login). Then pick up DELIVERY_SCORECARD updates and board meeting transcript processing.

</current_state>

<resume>
Say: **"Continuing iCare. Last session: portal document lifecycle deployed (4 real docs), Publix grant denied (4-year requirement — grant skill hardened to prevent). Netlify CLI still on icaregives account — switch back first. Next: update DELIVERY_SCORECARD, process board meeting transcript, file 990-N by May 15."**
</resume>
