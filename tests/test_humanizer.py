"""Tests for the li-human scripts. Run with: python -m unittest discover tests"""

import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HUMAN = os.path.join(ROOT, "skills", "li-human")
sys.path.insert(0, HUMAN)

import detect  # noqa: E402
import humanize  # noqa: E402

LEX = humanize.load_lexicon()

SLOPPY = (
    "In today’s fast-paced world, leveraging AI is crucial.​\n\n"
    "It’s not just a tool, it’s a revolution. Moreover, it empowers teams.\n\n"
    "We must delve into this — let that sink in.\n\n"
    "See https://example.com/robust-leverage for more…\n\n"
    "Thoughts?"
)

HUMAN_TEXT = (
    "I spent $4,200 and 6 weeks on a proposal tool in March. It saved us 5 hours per bid.\n"
    "We won 3 of the next 4.\n"
    "Honestly? I didn't expect that. Sarah, our ops lead, called it a fluke at first. "
    "She doesn't anymore.\n"
    "What I'd do differently: start with the pricing page, not the cover letter.\n"
)


class TestData(unittest.TestCase):
    def test_json_files_parse(self):
        for rel in [
            "skills/li-human/slop.json",
            "skills/li-post/hooks.json",
            "skills/li-profile/rubric.json",
            ".claude-plugin/plugin.json",
            ".claude-plugin/marketplace.json",
        ]:
            with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
                json.load(fh)

    def test_hooks_and_rubric_totals(self):
        with open(os.path.join(ROOT, "skills/li-post/hooks.json"), encoding="utf-8") as fh:
            self.assertEqual(len(json.load(fh)["hooks"]), 21)
        with open(os.path.join(ROOT, "skills/li-profile/rubric.json"), encoding="utf-8") as fh:
            self.assertEqual(sum(i["points"] for i in json.load(fh)["items"]), 100)

    def test_skill_names_match_folders(self):
        skills = os.path.join(ROOT, "skills")
        for name in os.listdir(skills):
            with open(os.path.join(skills, name, "SKILL.md"), encoding="utf-8") as fh:
                self.assertIn("\nname: {}\n".format(name), fh.read())


class TestHumanize(unittest.TestCase):
    def setUp(self):
        self.clean, self.report = humanize.humanize(SLOPPY, LEX)

    def test_removes_fingerprint(self):
        for ch in "​—’…":
            self.assertNotIn(ch, self.clean)

    def test_swaps_stock_words(self):
        for word in ["leveraging", "crucial", "Moreover", "delve", "let that sink in"]:
            self.assertNotIn(word.lower(), self.clean.lower())

    def test_leaves_urls_alone(self):
        self.assertIn("https://example.com/robust-leverage", self.clean)

    def test_flags_structures(self):
        ids = {f["id"] for f in self.report["structures"]}
        self.assertIn("not-just", ids)
        self.assertIn("bait", ids)

    def test_idempotent(self):
        again, _ = humanize.humanize(self.clean, LEX)
        self.assertEqual(again, self.clean)


class TestDetect(unittest.TestCase):
    def test_sloppy_is_flagged(self):
        self.assertEqual(detect.score(SLOPPY, LEX)["verdict"], "FLAGGED")

    def test_human_text_passes(self):
        self.assertEqual(detect.score(HUMAN_TEXT, LEX)["verdict"], "PASS")


class TestGate(unittest.TestCase):
    def run_gate(self, text):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "draft.txt")
            out = os.path.join(tmp, "clean.txt")
            with open(src, "w", encoding="utf-8") as fh:
                fh.write(text)
            proc = subprocess.run(
                [sys.executable, os.path.join(HUMAN, "gate.py"), src, "-o", out],
                capture_output=True, text=True, encoding="utf-8",
            )
            with open(out, encoding="utf-8") as fh:
                return proc, fh.read()

    def test_passing_pieces(self):
        proc, clean = self.run_gate(HUMAN_TEXT + "---\nThanks Lee.\n")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("humanized: 2 pieces", proc.stdout)
        self.assertEqual(clean.count("\n---\n"), 1)

    def test_failing_piece_exits_nonzero(self):
        proc, clean = self.run_gate("Great point — this is crucial.\n---\nThanks Lee.\n")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("NOT ALL PASSING", proc.stdout)
        self.assertNotIn("—", clean)


if __name__ == "__main__":
    unittest.main()
