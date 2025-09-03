"""
JSON reporter for AntiTrapLens.
"""

import json
from pathlib import Path
from typing import Dict, Any
from ...core.types import ScanResult
from ..base import BaseReporter
from ..common import DataConverter

class JSONReporter(BaseReporter):
    """JSON-based report generator."""

    def __init__(self, config=None):
        super().__init__(config)

    def generate(self, scan_result: ScanResult, output_path: str = None) -> str:
        """Generate JSON report."""
        if output_path is None:
            output_path = "antitraplens_report.json"

        # Convert scan result to dictionary
        report_data = self._scan_result_to_dict(scan_result)

        # Write to file with pretty printing
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False, default=str)

        return f"JSON report saved to {output_path}"

    def _scan_result_to_dict(self, scan_result: ScanResult) -> Dict[str, Any]:
        """Convert ScanResult to dictionary with project info and enhanced pattern descriptions."""
        # Get the enhanced scan result from DataConverter
        enhanced_data = DataConverter.scan_result_to_dict(scan_result)
        
        return {
            "project": {
                "name": "AntiTrapLens",
                "description": "Privacy & Dark Pattern Detection Tool",
                "author": "Ahsan Malik",
                "github": "https://github.com/ahsan1o/AntiTrapLens",
                "version": "1.0.0"
            },
            "metadata": enhanced_data["metadata"],
            "scan_info": enhanced_data["scan_info"],
            "pages": enhanced_data["pages"],
            "summary": {
                "dark_patterns": DataConverter.get_dark_pattern_summary(scan_result.pages),
                "cookie_tracking": DataConverter.get_cookie_summary(scan_result.pages),
                "severity_breakdown": {
                    "dark_patterns": DataConverter.get_dark_pattern_severity_counts(scan_result.pages),
                    "cookie_tracking": DataConverter.get_cookie_severity_counts(scan_result.pages)
                }
            },
            "pattern_descriptions": DataConverter.DARK_PATTERN_DESCRIPTIONS
        }

    def get_format(self) -> str:
        """Get report format."""
        return "json"
