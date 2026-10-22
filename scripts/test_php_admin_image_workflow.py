#!/usr/bin/env python3
"""Offline regression checks for the admin image source-policy workflow."""

from pathlib import Path
import re
import unittest


WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/php-admin-image-security.yml"


class WorkflowTests(unittest.TestCase):
    def test_source_policy_ci(self):
        workflow = WORKFLOW.read_text()
        self.assertRegex(workflow, r"(?m)^on:\n  pull_request:\n  push:\n    branches:\n      - main$")
        self.assertRegex(workflow, r"(?m)^permissions:\n  contents: read\n(?:\n)?jobs:")
        self.assertRegex(workflow, r"(?m)^    runs-on: ubuntu-24\.04$")
        self.assertRegex(workflow, r"(?m)^      - uses: actions/checkout@v7$")
        for command in (
            "python3 -B scripts/test_php_admin_images.py",
            "python3 -B scripts/check_php_admin_images.py",
            "git diff --check",
        ):
            with self.subTest(command=command):
                self.assertRegex(workflow, rf"(?m)^      - run: {re.escape(command)}$")


if __name__ == "__main__":
    unittest.main(verbosity=2)
