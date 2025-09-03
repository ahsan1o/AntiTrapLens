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
            print(f"Page {i+1}: {page.get('url', 'N/A')}")
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
            print()
