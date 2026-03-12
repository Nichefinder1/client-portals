#!/usr/bin/env python3
"""
All South Lightning Protection — Portal Update Script
======================================================
Run this script at the end of every work session or monthly update.
It asks structured questions, updates reports.json, then commits and pushes.

Since index.html is now data-driven, updating reports.json is ALL you need
to do to refresh: status banner, goal tracker, quick stats, metrics table
(current month), location cards, completed wins, and next focus areas.

Usage:
  python3 portal-update.py

Requirements: git must be configured and authenticated in this directory.
"""

import json
import subprocess
import sys
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_FILE = os.path.join(SCRIPT_DIR, 'reports.json')

GREEN  = '\033[92m'
YELLOW = '\033[93m'
BLUE   = '\033[94m'
BOLD   = '\033[1m'
RESET  = '\033[0m'

def banner(text):
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}  {text}{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")

def ask(prompt, current=None, allow_blank=True):
    """Ask a question. Press Enter to keep current value."""
    if current is not None:
        display = str(current)
        full_prompt = f"  {prompt}\n  {YELLOW}Current: {display}{RESET}\n  New value (Enter to keep): "
    else:
        full_prompt = f"  {prompt}: "
    try:
        val = input(full_prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{YELLOW}Update cancelled.{RESET}")
        sys.exit(0)
    if val == '' and current is not None:
        return current
    if val == '' and not allow_blank:
        return current
    return val

def ask_int(prompt, current=None):
    while True:
        val = ask(prompt, current)
        try:
            return int(val)
        except (ValueError, TypeError):
            if val == current:
                return current
            print(f"  Please enter a number.")

def ask_float(prompt, current=None):
    while True:
        val = ask(prompt, current)
        try:
            return float(val)
        except (ValueError, TypeError):
            if val == current:
                return current
            print(f"  Please enter a number (e.g. 4.7).")

def ask_list(prompt, current=None):
    """For lists: show current, then ask to add/edit/keep."""
    print(f"\n  {BOLD}{prompt}{RESET}")
    if current:
        print(f"  {YELLOW}Current items:{RESET}")
        for i, item in enumerate(current, 1):
            # Strip HTML for display
            clean = item.replace('<strong>', '').replace('</strong>', '')
            print(f"    {i}. {clean}")
    print(f"  Options: [K]eep as-is · [R]eplace all · [A]dd items")
    choice = input("  Choice (K/R/A): ").strip().upper()
    if choice == 'K' or choice == '':
        return current
    elif choice == 'R':
        print(f"  Enter new items one per line. Empty line when done:")
        items = []
        while True:
            line = input(f"  Item {len(items)+1}: ").strip()
            if not line:
                break
            items.append(line)
        return items if items else current
    elif choice == 'A':
        items = list(current) if current else []
        print(f"  Enter items to add. Empty line when done:")
        while True:
            line = input(f"  Add: ").strip()
            if not line:
                break
            items.append(line)
        return items
    return current

def git_commit_push(commit_msg):
    """Stage all changes, commit, and push."""
    portal_root = os.path.dirname(SCRIPT_DIR)  # company/client-portals/
    try:
        subprocess.run(['git', 'add', REPORTS_FILE], cwd=portal_root, check=True)
        subprocess.run(['git', 'commit', '-m', commit_msg], cwd=portal_root, check=True)
        subprocess.run(['git', 'push'], cwd=portal_root, check=True)
        print(f"\n{GREEN}✅ Changes committed and pushed to GitHub Pages.{RESET}")
        print(f"   Live in ~60 seconds: https://nichefinder1.github.io/client-portals/all-south-lightning/")
    except subprocess.CalledProcessError as e:
        print(f"\n{YELLOW}⚠️  Git error: {e}{RESET}")
        print(f"   reports.json was saved. Commit manually when ready.")

def main():
    banner("All South Lightning — Portal Update")
    print(f"  This script updates reports.json, which drives the live dashboard.")
    print(f"  Press Enter on any field to keep the current value.\n")

    # Load current data
    with open(REPORTS_FILE, 'r') as f:
        data = json.load(f)

    m  = data.get('metrics', {})
    db = data.get('dashboard', {})
    kf = data.get('key_findings', {})
    cl = data.get('client', {})
    cm = db.get('current_metrics', {})
    locs = db.get('location_cards', [])

    today = datetime.now().strftime('%B %-d, %Y')  # e.g. March 12, 2026

    # ── Section 1: Campaign Status ──────────────────────────────────
    banner("1 of 6 — Campaign Status")
    cl['last_updated'] = ask("Last updated date", cl.get('last_updated', today))
    db['campaign_phase'] = ask("Campaign phase", db.get('campaign_phase'))
    db['goal_pct'] = ask_int("Goal tracker % (0–100)", db.get('goal_pct'))
    db['goal_label'] = ask("Goal bar label text", db.get('goal_label'))

    # ── Section 2: Key Metrics ───────────────────────────────────────
    banner("2 of 6 — Key Metrics")
    m['reviews'] = ask_int("Tampa Google Reviews", m.get('reviews'))
    m['review_rating'] = ask_float("Tampa Star Rating", m.get('review_rating'))
    m['citations'] = ask("Active Citations count", m.get('citations'))
    db['keywords_rank'] = ask("Keywords ranking #1-2 (e.g. 17/22)", db.get('keywords_rank'))
    db['keywords_rank_sub'] = ask("Keywords sub-label (e.g. Apr 2026 Scan ✅)", db.get('keywords_rank_sub'))

    # ── Section 3: Current Month Metrics Table ───────────────────────
    banner("3 of 6 — Current Month Metrics Table")
    db['current_month_col'] = ask("Current month column header (e.g. Apr 2026)", db.get('current_month_col'))
    print(f"\n  {YELLOW}For each metric, enter the value to show in the current month column.{RESET}")
    print(f"  Trend: 'up' (green), 'down' (red), 'flat' (orange)\n")

    metric_prompts = {
        'gbp_listings':       'GBP Listings (of 3)',
        'tampa_gbp_score':    'Tampa GBP Score',
        'tampa_map_pack':     'Tampa Map Pack Rank (Median)',
        'tampa_reviews':      'Tampa Reviews',
        'tampa_rating':       'Tampa Star Rating',
        'sunrise_gbp':        'Sunrise GBP status',
        'jacksonville_gbp':   'Jacksonville GBP status',
        'organic_clicks':     'Organic Clicks (GSC)',
        'gbp_website_clicks': 'GBP Website Clicks',
        'citations':          'Active Citations',
        'gbp_posts':          'Tampa GBP Posts',
        'blog_posts':         'Blog Posts Published',
        'social_posts':       'Social Posts (LinkedIn/FB/IG)',
    }
    for key, label in metric_prompts.items():
        current_entry = cm.get(key, {})
        val   = ask(f"{label} — value", current_entry.get('value'))
        trend = ask(f"{label} — trend (up/flat/down)", current_entry.get('trend', 'flat'))
        cm[key] = {'value': val, 'trend': trend}

    # ── Section 4: Status Tiles ──────────────────────────────────────
    banner("4 of 6 — Status Banner Tiles (top of dashboard)")
    tiles = db.get('status_tiles', [
        {"value": "", "label": "", "color": "#27ae60", "small": False},
        {"value": "", "label": "", "color": "#27ae60", "small": True},
        {"value": "", "label": "", "color": "#27ae60", "small": False},
        {"value": "", "label": "", "color": "#1a5276", "small": False},
    ])
    for i, tile in enumerate(tiles, 1):
        print(f"\n  Tile {i}:")
        tile['value'] = ask(f"  Value", tile.get('value'))
        tile['label'] = ask(f"  Label", tile.get('label'))
    db['status_tiles'] = tiles

    # ── Section 5: Location Cards ────────────────────────────────────
    banner("5 of 6 — Location Cards")
    print(f"  Update each location's GBP status card.\n")
    for loc in locs:
        print(f"\n  {BOLD}{loc['name']}{RESET}")
        loc['status']       = ask("  Status text", loc.get('status'))
        loc['status_class'] = ask("  Status class (good/bad)", loc.get('status_class'))
        loc['line1']        = ask("  Line 1 (reviews/date)", loc.get('line1'))
        loc['line2']        = ask("  Line 2 (services/status)", loc.get('line2'))

    # ── Section 6: Completed Wins & Next Focus ───────────────────────
    banner("6 of 6 — Completed Wins & Next Focus")
    kf['completed_wins'] = ask_list("Completed Wins", kf.get('completed_wins', []))
    kf['next_focus']     = ask_list("Next Focus Areas", kf.get('next_focus', []))

    # ── Write back ───────────────────────────────────────────────────
    data['client']   = cl
    data['metrics']  = m
    data['dashboard'] = {**db, 'current_metrics': cm, 'location_cards': locs, 'status_tiles': tiles}
    data['key_findings'] = kf

    with open(REPORTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\n{GREEN}✅ reports.json saved.{RESET}")

    # ── Commit & Push ────────────────────────────────────────────────
    commit = input(f"\n  Commit message (Enter for default): ").strip()
    if not commit:
        phase = db.get('campaign_phase', 'update')
        commit = f"All South Lightning: portal update — {cl.get('last_updated', today)} ({phase})\n\nCo-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
    else:
        commit += "\n\nCo-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"

    push = input(f"  Push to GitHub Pages now? (Y/n): ").strip().lower()
    if push != 'n':
        git_commit_push(commit)
    else:
        print(f"\n  {YELLOW}Skipped push. Run: cd company/client-portals && git add . && git commit -m '...' && git push{RESET}")

    print(f"\n{BOLD}{GREEN}Portal update complete! Dashboard will reflect changes within 60 seconds of push.{RESET}\n")

if __name__ == '__main__':
    main()
