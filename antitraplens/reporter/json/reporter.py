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
        report_data = DataConverter.scan_result_to_dict(scan_result)

        # Write to file with pretty printing
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False, default=str)

        return f"JSON report saved to {output_path}"

    def get_format(self) -> str:
        """Get report format."""
        return "json"
