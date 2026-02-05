#!/usr/bin/env python3
"""
Client Portal Generator
Generates index.html from reports.json config file.

Usage:
    python generate-portal.py fox-valley-plumbing
    python generate-portal.py --all
"""

import json
import os
import sys
from datetime import datetime

def get_badge_style(color):
    """Return CSS class or inline style for badge color."""
    colors = {
        "red": "background-color: #e74c3c; color: white;",
        "green": "background-color: #27ae60; color: white;",
        "blue": "background-color: #3498db; color: white;",
        "purple": "background-color: #9b59b6; color: white;",
        "orange": "background-color: #f39c12; color: white;",
        "gray": "background-color: #95a5a6; color: white;",
        "teal": "background-color: #1abc9c; color: white;"
    }
    return colors.get(color, colors["blue"])

def generate_portal(client_folder):
    """Generate index.html for a client from their reports.json."""

    config_path = os.path.join(client_folder, "reports.json")
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found")
        return False

    with open(config_path, 'r') as f:
        config = json.load(f)

    client = config['client']
    metrics = config['metrics']
    contact = config['contact']
    findings = config['key_findings']

    # Generate monthly reports section
    monthly_html = ""
    archive_html = ""

    for month in config.get('monthly_reports', []):
        month_reports = ""
        for report in month['reports']:
            if report.get('file'):
                link = f'<a href="{report["file"]}" class="card-link">View Report &rarr;</a>'
            else:
                available = report.get('available_date', 'Soon')
                link = f'<a href="#" class="card-link" style="color: #95a5a6; pointer-events: none;">Available {available}</a>'

            badge_style = get_badge_style(report.get('badge_color', 'blue'))
            month_reports += f'''
<div class="card">
<div class="card-header">
<h3>{report['title']} <span class="badge" style="{badge_style}">{report.get('badge', '')}</span></h3>
<span class="date">{month['month_name']}</span>
</div>
<div class="card-body">
<p>{report['description']}</p>
</div>
{link}
</div>
'''

        if month.get('is_current'):
            monthly_html += month_reports
        else:
            # Add to archive
            archive_html += f'''
<div class="archive-month">
<h4>{month['month_name']}</h4>
<div class="card-grid">
{month_reports}
</div>
</div>
'''

    # Generate one-time reports section
    onetime_html = ""
    for report in config.get('one_time_reports', []):
        badge_style = get_badge_style(report.get('badge_color', 'purple'))
        header_style = 'style="background-color: #27ae60;"' if report.get('badge_color') == 'green' else ''

        onetime_html += f'''
<div class="card">
<div class="card-header" {header_style}>
<h3>{report['title']} <span class="badge" style="{badge_style}">{report.get('badge', 'One-Time')}</span></h3>
<span class="date">{report['date']}</span>
</div>
<div class="card-body">
<p>{report['description']}</p>
</div>
<a href="{report['file']}" class="card-link">View Report &rarr;</a>
</div>
'''

    # Generate checklists section
    checklists_html = ""
    for checklist in config.get('checklists', []):
        badge_style = get_badge_style(checklist.get('badge_color', 'teal'))
        header_style = 'style="background-color: #27ae60;"' if checklist.get('badge_color') == 'green' else ''

        if checklist.get('file'):
            link = f'<a href="{checklist["file"]}" class="card-link">View Checklist &rarr;</a>'
        else:
            link = '<a href="#" class="card-link" style="color: #95a5a6; pointer-events: none;">Starting Soon</a>'

        checklists_html += f'''
<div class="card">
<div class="card-header" {header_style}>
<h3>{checklist['title']} <span class="badge" style="{badge_style}">{checklist.get('badge', 'In Progress')}</span></h3>
<span class="date">{checklist['date']}</span>
</div>
<div class="card-body">
<p>{checklist['description']}</p>
</div>
{link}
</div>
'''

    # Generate key findings
    resolved_items = "\n".join([f"<li>✅ {item}</li>" for item in findings.get('resolved', [])])
    strengths_items = "\n".join([f"<li>{item}</li>" for item in findings.get('strengths', [])])
    focus_items = "\n".join([f"<li>{item}</li>" for item in findings.get('next_focus', [])])

    # Archive section (only show if there are archived months)
    archive_section = ""
    if archive_html:
        archive_section = f'''
<!-- Report Archive -->
<div class="section-header">
<h2>Report Archive</h2>
<p>Access reports from previous months</p>
</div>
{archive_html}
'''

    # Generate full HTML
    html = f'''<html>
<head>
<meta charset="UTF-8">
<title>{client['name']} - Client Portal | Nichefinder AI</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
<style>
/* Download buttons */
.download-bar {{ position: fixed; top: 20px; right: 20px; z-index: 1000; display: flex; gap: 10px; }}
.download-btn {{ padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 10pt; font-weight: bold; display: flex; align-items: center; gap: 8px; transition: all 0.2s; box-shadow: 0 2px 8px rgba(0,0,0,0.2); }}
.download-btn:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.25); }}
.btn-pdf {{ background-color: #c0392b; color: white; }}
.btn-pdf:hover {{ background-color: #a93226; }}
.btn-print {{ background-color: #1a5276; color: white; }}
.btn-print:hover {{ background-color: #154360; }}
@media print {{ .download-bar {{ display: none !important; }} }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: Calibri, Arial, sans-serif; font-size: 11pt; line-height: 1.6; color: #333; background-color: #f5f6fa; }}

/* Header */
.header {{ background: linear-gradient(135deg, #1a5276, #2874a6); color: white; padding: 40px; text-align: center; }}
.header h1 {{ margin: 0; font-size: 28pt; }}
.header p {{ margin: 10px 0 0 0; opacity: 0.9; font-size: 12pt; }}

/* Container */
.container {{ max-width: 1200px; margin: 0 auto; padding: 30px; }}

/* Status banner */
.status-banner {{ background-color: #d5f5e3; border: 2px solid #27ae60; padding: 20px; border-radius: 10px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; }}
.status-banner h3 {{ margin: 0; color: #1e8449; }}
.status-metric {{ text-align: center; padding: 0 20px; }}
.status-metric .number {{ font-size: 24pt; font-weight: bold; color: #1a5276; display: block; }}
.status-metric .label {{ font-size: 9pt; color: #7f8c8d; }}

/* Quick stats */
.quick-stats {{ display: flex; justify-content: space-between; flex-wrap: wrap; margin-bottom: 30px; }}
.stat-box {{ background: white; border-radius: 10px; padding: 20px; text-align: center; flex: 1; margin: 5px; min-width: 150px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
.stat-box .number {{ font-size: 32pt; font-weight: bold; color: #1a5276; display: block; }}
.stat-box .label {{ font-size: 10pt; color: #7f8c8d; }}
.stat-box .change {{ font-size: 11pt; margin-top: 5px; }}
.stat-box .change.positive {{ color: #27ae60; }}
.stat-box .change.negative {{ color: #c0392b; }}
.stat-box .change.neutral {{ color: #f39c12; }}

/* Card grid */
.card-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 30px; }}
.card {{ background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); overflow: hidden; transition: transform 0.2s, box-shadow 0.2s; }}
.card:hover {{ transform: translateY(-3px); box-shadow: 0 4px 20px rgba(0,0,0,0.15); }}
.card-header {{ background-color: #1a5276; color: white; padding: 15px 20px; }}
.card-header h3 {{ margin: 0; font-size: 14pt; }}
.card-header .date {{ font-size: 9pt; opacity: 0.8; }}
.card-body {{ padding: 20px; }}
.card-body p {{ margin: 0 0 15px 0; color: #7f8c8d; font-size: 10pt; }}
.card-link {{ display: block; background-color: #f8f9f9; padding: 12px 20px; text-align: center; color: #1a5276; text-decoration: none; font-weight: bold; border-top: 1px solid #ecf0f1; }}
.card-link:hover {{ background-color: #1a5276; color: white; }}

/* Section headers */
.section-header {{ margin: 30px 0 20px 0; padding-bottom: 10px; border-bottom: 2px solid #1a5276; }}
.section-header h2 {{ margin: 0; color: #1a5276; font-size: 18pt; }}
.section-header p {{ margin: 5px 0 0 0; color: #7f8c8d; font-size: 10pt; }}

/* Badges */
.badge {{ display: inline-block; padding: 3px 10px; border-radius: 15px; font-size: 9pt; font-weight: bold; margin-left: 10px; }}

/* Contact section */
.contact-section {{ background: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-top: 30px; }}
.contact-section h3 {{ margin-top: 0; color: #1a5276; }}
.contact-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }}
.contact-item {{ text-align: center; padding: 15px; }}
.contact-item .icon {{ font-size: 24pt; margin-bottom: 10px; }}
.contact-item .value {{ font-weight: bold; color: #1a5276; }}
.contact-item .value a {{ color: #1a5276; text-decoration: none; }}
.contact-item .value a:hover {{ text-decoration: underline; }}
.contact-item .label {{ font-size: 10pt; color: #7f8c8d; }}

/* Goal tracker */
.goal-tracker {{ background: white; border-radius: 10px; padding: 25px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 30px; }}
.goal-tracker h3 {{ margin: 0 0 15px 0; color: #1a5276; }}
.progress-container {{ background-color: #ecf0f1; border-radius: 10px; height: 30px; margin: 10px 0; overflow: hidden; }}
.progress-bar {{ background: linear-gradient(90deg, #27ae60, #2ecc71); height: 100%; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; }}
.goal-details {{ display: flex; justify-content: space-between; margin-top: 10px; font-size: 10pt; color: #7f8c8d; }}

/* Archive section */
.archive-month {{ margin-bottom: 30px; }}
.archive-month h4 {{ color: #1a5276; margin-bottom: 15px; padding-bottom: 5px; border-bottom: 1px solid #d5d8dc; }}

/* Footer */
.footer {{ text-align: center; padding: 20px; color: #95a5a6; font-size: 9pt; }}

/* Print styles */
@media print {{
    body {{ background: white; }}
    .container {{ padding: 0; }}
    .card:hover {{ transform: none; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
}}
</style>
</head>
<body>

<div class="download-bar">
<button class="download-btn btn-pdf" onclick="downloadPDF()">&#128196; Download PDF</button>
<button class="download-btn btn-print" onclick="window.print()">&#128424; Print</button>
</div>

<script>
function downloadPDF() {{
    const element = document.body;
    const opt = {{
        margin: 0.3,
        filename: 'Client_Portal_{client['slug'].replace('-', '_')}.pdf',
        image: {{ type: 'jpeg', quality: 0.98 }},
        html2canvas: {{ scale: 2 }},
        jsPDF: {{ unit: 'in', format: 'letter', orientation: 'portrait' }}
    }};
    document.querySelector('.download-bar').style.display = 'none';
    html2pdf().set(opt).from(element).save().then(() => {{
        document.querySelector('.download-bar').style.display = 'flex';
    }});
}}
</script>

<div class="header">
<h1>{client['name']}</h1>
<p>Client Portal | Local SEO & Digital Marketing</p>
</div>

<div class="container">

<!-- Status Banner -->
<div class="status-banner">
<div>
<h3>Campaign Status: {client['campaign_status']}</h3>
<p>Last Updated: {datetime.now().strftime('%B %d, %Y')}</p>
</div>
<div class="status-metric">
<span class="number">{metrics['keywords_at_1']}</span>
<span class="label">Keywords at #1</span>
</div>
<div class="status-metric">
<span class="number">{metrics['total_keywords']}</span>
<span class="label">Total Tracked</span>
</div>
<div class="status-metric">
<span class="number">{metrics['goal_progress']}%</span>
<span class="label">Goal Progress</span>
</div>
</div>

<!-- Goal Tracker -->
<div class="goal-tracker">
<h3>{client['goal']}</h3>
<div class="progress-container">
<div class="progress-bar" style="width: {metrics['goal_progress']}%;">{metrics['goal_progress']}% Complete ({metrics['keywords_at_1']} of {metrics['total_keywords']})</div>
</div>
<div class="goal-details">
<span>Start: {metrics['keywords_at_1']} keywords ({client['start_date']})</span>
<span>Target: {metrics['total_keywords']} keywords (Dec 2026)</span>
</div>
</div>

<!-- Quick Stats -->
<div class="quick-stats">
<div class="stat-box">
<span class="number">{metrics['organic_clicks']}</span>
<span class="label">Monthly Organic Clicks</span>
<span class="change neutral">Baseline</span>
</div>
<div class="stat-box">
<span class="number">{metrics['gbp_calls']}</span>
<span class="label">GBP Phone Calls</span>
<span class="change neutral">{metrics.get('gbp_calls_note', '')}</span>
</div>
<div class="stat-box">
<span class="number">{metrics['reviews']}</span>
<span class="label">Google Reviews</span>
<span class="change positive">{metrics['review_rating']} stars</span>
</div>
<div class="stat-box">
<span class="number">{metrics['citations']}</span>
<span class="label">Active Citations</span>
<span class="change neutral">{metrics.get('citations_note', '')}</span>
</div>
</div>

<!-- Monthly Reports Section -->
<div class="section-header">
<h2>Monthly Reports</h2>
<p>Recurring reports delivered each month showing progress and work completed</p>
</div>

<div class="card-grid">
{monthly_html}
</div>

<!-- Strategy & Audits Section -->
<div class="section-header">
<h2>Strategy & Audits</h2>
<p>One-time assessments and long-term strategy documents</p>
</div>

<div class="card-grid">
{onetime_html}
</div>

<!-- Implementation Checklists Section -->
<div class="section-header">
<h2>Implementation Checklists</h2>
<p>Step-by-step guides tracking implementation progress</p>
</div>

<div class="card-grid">
{checklists_html}
</div>

{archive_section}

<!-- Key Findings Summary -->
<div class="section-header">
<h2>Key Findings Summary</h2>
<p>Critical insights from audits and analysis</p>
</div>

<div class="card-grid">
<div class="card" style="border-left: 5px solid #27ae60;">
<div class="card-header" style="background-color: #27ae60;">
<h3>GBP Issues RESOLVED</h3>
</div>
<div class="card-body">
<ul style="margin: 0; padding-left: 20px; font-size: 10pt;">
{resolved_items}
</ul>
<p style="margin-top: 10px; font-size: 9pt; color: #27ae60; font-weight: bold;">{findings.get('resolved_note', '')}</p>
</div>
</div>

<div class="card" style="border-left: 5px solid #27ae60;">
<div class="card-header" style="background-color: #27ae60;">
<h3>Strengths to Leverage</h3>
</div>
<div class="card-body">
<ul style="margin: 0; padding-left: 20px; font-size: 10pt;">
{strengths_items}
</ul>
</div>
</div>

<div class="card" style="border-left: 5px solid #3498db;">
<div class="card-header" style="background-color: #3498db;">
<h3>Next Focus Areas</h3>
</div>
<div class="card-body">
<ul style="margin: 0; padding-left: 20px; font-size: 10pt;">
{focus_items}
</ul>
</div>
</div>
</div>

<!-- Contact Section -->
<div class="contact-section">
<h3>Contact Your Account Team</h3>
<div class="contact-grid">
<div class="contact-item">
<div class="icon">&#128231;</div>
<div class="value"><a href="mailto:{contact['email']}">{contact['email']}</a></div>
<div class="label">Email</div>
</div>
<div class="contact-item">
<div class="icon">&#128222;</div>
<div class="value">{contact['phone']}</div>
<div class="label">Phone</div>
</div>
<div class="contact-item">
<div class="icon">&#128197;</div>
<div class="value"><a href="{contact['calendar']}">Schedule a Call</a></div>
<div class="label">Calendar</div>
</div>
</div>
</div>

</div>

<div class="footer">
<p>&copy; {datetime.now().year} Nichefinder AI Agency | Client Portal</p>
<p>Reports are updated monthly. Questions? Contact us anytime.</p>
</div>

</body>
</html>'''

    # Write the HTML file
    output_path = os.path.join(client_folder, "index.html")
    with open(output_path, 'w') as f:
        f.write(html)

    print(f"✅ Generated: {output_path}")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate-portal.py <client-folder>")
        print("       python generate-portal.py --all")
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))

    if sys.argv[1] == "--all":
        # Generate for all client folders
        for item in os.listdir(script_dir):
            item_path = os.path.join(script_dir, item)
            if os.path.isdir(item_path) and not item.startswith('.'):
                config_path = os.path.join(item_path, "reports.json")
                if os.path.exists(config_path):
                    generate_portal(item_path)
    else:
        # Generate for specific client
        client_folder = sys.argv[1]
        if not os.path.isabs(client_folder):
            client_folder = os.path.join(script_dir, client_folder)

        if not os.path.exists(client_folder):
            print(f"Error: Folder not found: {client_folder}")
            sys.exit(1)

        generate_portal(client_folder)


if __name__ == "__main__":
    main()
