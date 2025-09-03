"""
Reporter module for generating reports from AntiTrapLens findings.
"""

from typing import Dict, Any, List
import json
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        pass

    def generate_json_report(self, data: Dict[str, Any], filename: str):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    def generate_markdown_report(self, data: Dict[str, Any], filename: str):
        scan_info = data.get('scan_info', {})
        pages = data.get('pages', [])

        md = f"# AntiTrapLens Report\n\n"
        md += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md += f"**Start URL:** {scan_info.get('start_url', 'N/A')}\n"
        md += f"**Depth:** {scan_info.get('depth', 'N/A')}\n"
        md += f"**Pages Scanned:** {scan_info.get('pages_scanned', 0)}\n"
        md += f"**Total Findings:** {scan_info.get('total_findings', 0)}\n\n"

        for i, page in enumerate(pages):
            md += f"## Page {i+1}: {page.get('url', 'N/A')}\n\n"
            md += f"**Title:** {page.get('title', 'N/A')}\n"
            md += f"**Findings:** {len(page.get('dark_patterns', {}).get('findings', []))}\n\n"

            findings = page.get('dark_patterns', {}).get('findings', [])
            if findings:
                md += "### Dark Patterns Detected\n\n"
                for finding in findings:
                    md += f"- **{finding['pattern']}** ({finding['severity']}): {finding['description']}\n"
                md += "\n"

            score = page.get('dark_patterns', {}).get('score', {})
            if score:
                md += f"**Score:** {score.get('total_score', 0)}/100 ({score.get('grade', 'N/A')})\n"
                md += f"**Breakdown:** High: {score['breakdown']['high']}, Medium: {score['breakdown']['medium']}, Low: {score['breakdown']['low']}\n\n"

        md += f"## Summary\n\n"
        total_high = sum(len([f for f in page.get('dark_patterns', {}).get('findings', []) if f['severity'] == 'high']) for page in pages)
        total_medium = sum(len([f for f in page.get('dark_patterns', {}).get('findings', []) if f['severity'] == 'medium']) for page in pages)
        total_low = sum(len([f for f in page.get('dark_patterns', {}).get('findings', []) if f['severity'] == 'low']) for page in pages)
        md += f"- **High Severity:** {total_high}\n"
        md += f"- **Medium Severity:** {total_medium}\n"
        md += f"- **Low Severity:** {total_low}\n\n"

        if scan_info.get('total_findings', 0) == 0:
            md += "✅ **No dark patterns found!** The site appears clean.\n\n"
        else:
            md += f"⚠️ **{scan_info.get('total_findings', 0)} dark patterns found.** Review the details below.\n\n"

        with open(filename, 'w') as f:
            f.write(md)

    def generate_console_report(self, data: Dict[str, Any]):
        scan_info = data.get('scan_info', {})
        print("=== AntiTrapLens Report ===")
        print(f"Start URL: {scan_info.get('start_url', 'N/A')}")
        print(f"Pages Scanned: {scan_info.get('pages_scanned', 0)}")
        print(f"Total Findings: {scan_info.get('total_findings', 0)}")
        print()

        for i, page in enumerate(data.get('pages', [])):
            category = page.get('category', 'General')
            print(f"Page {i+1}: {page.get('url', 'N/A')} ({category})")
            findings = page.get('dark_patterns', {}).get('findings', [])
            if findings:
                print(f"  Findings: {len(findings)}")
                for finding in findings[:3]:  # Show top 3
                    print(f"    - {finding['pattern']} ({finding['severity']}): {finding['description']}")
                if len(findings) > 3:
                    print(f"    ... and {len(findings) - 3} more")
            else:
                print("  No dark patterns found")
            score = page.get('dark_patterns', {}).get('score', {})
            if score:
                print(f"  Score: {score.get('total_score', 0)}/100 ({score.get('grade', 'N/A')})")
            
            # Display cookie information
            cookies = page.get('cookies', [])
            if cookies:
                print(f"  Cookies: {len(cookies)} total")
                third_party = [c for c in cookies if c.get('is_third_party')]
                if third_party:
                    print(f"    Third-party: {len(third_party)}")
                
                cookie_analysis = page.get('cookie_access_analysis', {})
                if cookie_analysis.get('data_collection'):
                    print(f"    Data Collection: {', '.join(cookie_analysis['data_collection'][:2])}")
                if cookie_analysis.get('privacy_concerns'):
                    print(f"    Privacy Issues: {len(cookie_analysis['privacy_concerns'])}")
            print()

    def generate_html_report(self, data: Dict[str, Any], filename: str):
        scan_info = data.get('scan_info', {})
        pages = data.get('pages', [])

        # Calculate totals
        total_high = sum(len([f for f in page.get('dark_patterns', {}).get('findings', []) if f['severity'] == 'high']) for page in pages)
        total_medium = sum(len([f for f in page.get('dark_patterns', {}).get('findings', []) if f['severity'] == 'medium']) for page in pages)
        total_low = sum(len([f for f in page.get('dark_patterns', {}).get('findings', []) if f['severity'] == 'low']) for page in pages)

        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AntiTrapLens - Dark Pattern Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            background: #ffffff;
            color: #000000;
            line-height: 1.6;
        }}
        .hero {{
            background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
            padding: 100px 20px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        .hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="rgba(0,0,0,0.05)"/></svg>') repeat;
            opacity: 0.1;
        }}
        .hero h1 {{
            font-size: 4em;
            font-weight: 300;
            color: #000000;
            position: relative;
            z-index: 1;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }}
        .hero p {{
            font-size: 1.5em;
            color: #333333;
            margin-top: 20px;
            position: relative;
            z-index: 1;
        }}
        .summary {{
            padding: 80px 20px;
            background: #ffffff;
            text-align: center;
        }}
        .summary h2 {{
            font-size: 3em;
            font-weight: 200;
            color: #000000;
            margin-bottom: 40px;
        }}
        .stats {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 40px;
        }}
        .stat {{
            background: #f8f8f8;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            min-width: 200px;
            height: 150px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        .stat h3 {{
            font-size: 2.5em;
            color: #000000;
        }}
        .stat p {{
            font-size: 1.2em;
            color: #666666;
        }}
        .pages {{
            padding: 60px 20px;
            background: #f9f9f9;
        }}
        .page-card {{
            background: #ffffff;
            margin: 40px auto;
            max-width: 800px;
            border-radius: 15px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            overflow: hidden;
            position: relative;
        }}
        .page-header {{
            background: linear-gradient(135deg, #000000 0%, #333333 100%);
            color: #ffffff;
            padding: 30px;
            cursor: pointer;
        }}
        .page-header h3 {{
            font-size: 1.8em;
            font-weight: 300;
        }}
        .page-content {{
            padding: 30px;
            display: none;
        }}
        .finding {{
            background: #f0f0f0;
            margin: 15px 0;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #000000;
        }}
        .score {{
            font-size: 2em;
            font-weight: 300;
            color: #000000;
            text-align: center;
            margin: 20px 0;
        }}
        .footer {{
            background: #000000;
            color: #ffffff;
            padding: 40px 20px;
            text-align: center;
        }}
        .footer a {{
            color: #ffffff;
            text-decoration: none;
            font-weight: 300;
        }}
        .logo {{
            font-size: 2em;
            font-weight: 300;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }}
    </style>
    <script>
        function togglePage(id) {{
            var content = document.getElementById('content-' + id);
            content.style.display = content.style.display === 'block' ? 'none' : 'block';
        }}
    </script>
</head>
<body>
    <div class="hero">
        <h1>AntiTrapLens</h1>
        <p>Dark Pattern Detection Report</p>
        <p style="font-size: 1em; margin-top: 10px;">Developed by Ahsan Malik | <a href="https://github.com/ahsan1o" style="color: #000000;">GitHub: ahsan1o</a></p>
    </div>

    <div class="summary">
        <h2>Scan Overview</h2>
        <div class="stats">
            <div class="stat">
                <h3>{scan_info.get('pages_scanned', 0)}</h3>
                <p>Pages Scanned</p>
            </div>
            <div class="stat">
                <h3>{scan_info.get('total_findings', 0)}</h3>
                <p>Dark Patterns Found</p>
            </div>
            <div class="stat">
                <h3>{total_high + total_medium + total_low}</h3>
                <p>Total Issues</p>
            </div>
        </div>
    </div>

    <div class="pages">
"""

        for i, page in enumerate(pages):
            category = page.get('category', 'General')
            html += f"""
        <div class="page-card">
            <div class="page-header" onclick="togglePage({i})">
                <h3>Page {i+1}: {page.get('url', 'N/A')}</h3>
                <p>Category: {category} | Title: {page.get('title', 'N/A')}</p>
            </div>
            <div id="content-{i}" class="page-content">
"""

            findings = page.get('dark_patterns', {}).get('findings', [])
            if findings:
                for finding in findings:
                    html += f"""
                <div class="finding">
                    <strong>{finding['pattern']}</strong> ({finding['severity']}): {finding['description']}
                </div>
"""
            else:
                html += "<p>No dark patterns found.</p>"

            score = page.get('dark_patterns', {}).get('score', {})
            if score:
                html += f"""
                <div class="score">Score: {score.get('total_score', 0)}/100 ({score.get('grade', 'N/A')})</div>
"""

            # Add cookie information
            cookies = page.get('cookies', [])
            if cookies:
                html += f"""
                <div class="finding">
                    <strong>Cookies Detected:</strong> {len(cookies)} total cookies
                </div>
"""
                third_party = [c for c in cookies if c.get('is_third_party')]
                if third_party:
                    html += f"""
                <div class="finding">
                    <strong>Third-party Cookies:</strong> {len(third_party)} from domains like {', '.join([c.get('domain', '') for c in third_party[:3]])}
                </div>
"""
                
                cookie_analysis = page.get('cookie_access_analysis', {})
                if cookie_analysis.get('data_collection'):
                    html += f"""
                <div class="finding">
                    <strong>Data Collection:</strong> {', '.join(cookie_analysis['data_collection'][:3])}
                </div>
"""
                if cookie_analysis.get('tracking_capabilities'):
                    html += f"""
                <div class="finding">
                    <strong>Tracking Systems:</strong> {len(cookie_analysis['tracking_capabilities'])} detected
                </div>
"""
                if cookie_analysis.get('privacy_concerns'):
                    html += f"""
                <div class="finding">
                    <strong>Privacy Concerns:</strong> {', '.join(cookie_analysis['privacy_concerns'][:2])}
                </div>
"""

            html += "</div></div>"

        html += """
    </div>

    <div class="footer">
        <div class="logo">AntiTrapLens</div>
        <p>Privacy Advocate's Scanner | <a href="https://github.com/ahsan1o/AntiTrapLens">View Source</a></p>
    </div>
</body>
</html>
"""

        with open(filename, 'w') as f:
            f.write(html)
