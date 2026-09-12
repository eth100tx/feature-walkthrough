"""Exercise untrusted storyboard content and required evidence boundaries."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('storyboard', ROOT / 'demo-pitch/scripts/render_storyboard.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class StoryboardTest(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'demo-pitch/assets/storyboard.example.json').read_text())

    def test_untrusted_markup_is_never_executable(self):
        self.data['title'] = '<script>alert(1)</script>'
        self.data['beats'][0]['visual'] = '<img src=x onerror=alert(1)>'
        result = MODULE.render(self.data)
        self.assertNotIn('<script>', result)
        self.assertNotIn('<img', result)
        self.assertIn('&lt;script&gt;', result)

    def test_evidence_type_cannot_be_omitted(self):
        del self.data['beats'][0]['evidence_type']
        with self.assertRaises(ValueError):
            MODULE.render(self.data)

    def test_unknown_evidence_type_rejected(self):
        self.data['beats'][0]['evidence_type'] = 'proven by AI'
        with self.assertRaises(ValueError):
            MODULE.render(self.data)

    def test_duplicate_scene_identity_rejected(self):
        self.data['beats'][1]['id'] = self.data['beats'][0]['id']
        with self.assertRaises(ValueError):
            MODULE.render(self.data)

    def test_source_required(self):
        self.data['beats'][0]['source'] = ' '
        with self.assertRaises(ValueError):
            MODULE.render(self.data)

    def test_output_labels_planning_scope(self):
        self.assertIn('No audio or product interaction', MODULE.render(self.data))
        self.assertIn('Duration has not been recorded or measured', MODULE.render(self.data))

    def test_non_object_scene_rejected_cleanly(self):
        self.data['beats'][0] = 'invalid'
        with self.assertRaises(ValueError):
            MODULE.render(self.data)

    def test_data_origin_required_separately(self):
        del self.data['beats'][0]['data_provenance']
        with self.assertRaises(ValueError):
            MODULE.render(self.data)

    def test_word_counts_separate_optional_content(self):
        self.data['beats'][1]['section'] = 'optional'
        result = MODULE.render(self.data)
        self.assertIn('core:', result)
        self.assertIn('optional:', result)


if __name__ == '__main__':
    unittest.main()
