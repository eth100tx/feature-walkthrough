"""Test installation boundaries and portable CLI behavior using isolated outputs."""
import json
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


class PackagingTest(unittest.TestCase):
    def run_package(self, out, *args):
        return subprocess.run([sys.executable, str(ROOT / 'scripts/package_skills.py'),
                               '--out', str(out), *args], cwd=out.parent,
                              capture_output=True, text=True)

    def test_default_exports_are_independent_and_source_unchanged(self):
        before = (ROOT / 'SKILL.md').read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'skills'
            result = self.run_package(out)
            self.assertEqual(result.returncode, 0, result.stderr)
            feature = out / 'demo-features'
            pitch = out / 'demo-pitch'
            self.assertIn('name: demo-features', (feature / 'SKILL.md').read_text())
            self.assertIn('/demo-features', (feature / 'SKILL.md').read_text())
            self.assertFalse((feature / 'agents/openai.yaml').exists())
            self.assertEqual((ROOT / 'template/walkthrough-template.html').read_bytes(),
                             (feature / 'template/walkthrough-template.html').read_bytes())
            for name in ['LICENSE', 'scripts/render_storyboard.py', 'examples/pitch-demo-brief.md',
                         'examples/supplylane-storyboard.json', 'references/narration.md']:
                self.assertTrue((pitch / name).is_file(), name)
            rendered = Path(tmp) / 'planning.html'
            result = subprocess.run([sys.executable, str(pitch / 'scripts/render_storyboard.py'),
                                     str(pitch / 'examples/supplylane-storyboard.json'), str(rendered)],
                                    cwd=tmp, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(rendered.is_file())
        self.assertEqual((ROOT / 'SKILL.md').read_bytes(), before)

    def test_legacy_export_name_remains_available(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'skills'
            result = self.run_package(out, '--feature-name', 'feature-walkthrough')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((out / 'feature-walkthrough/SKILL.md').read_bytes(), (ROOT / 'SKILL.md').read_bytes())

    def test_existing_pitch_prevents_partial_feature_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'skills'
            (out / 'demo-pitch').mkdir(parents=True)
            sentinel = out / 'demo-pitch/keep.txt'
            sentinel.write_text('existing work')
            result = self.run_package(out)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(sentinel.read_text(), 'existing work')
            self.assertFalse((out / 'demo-features').exists())

    def test_copied_source_cannot_contain_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / 'repo'
            (fixture / 'scripts').mkdir(parents=True)
            script = fixture / 'scripts/package_skills.py'
            shutil.copy2(ROOT / 'scripts/package_skills.py', script)
            for name in ('demo-pitch', 'reference', 'template', 'example', 'other-output'):
                with self.subTest(source=name):
                    out = fixture / name / 'must-not-be-created'
                    result = subprocess.run([sys.executable, str(script), '--out', str(out)],
                                            cwd=tmp, capture_output=True, text=True)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn('outside this checkout', result.stderr)
                    self.assertFalse(out.exists())

    def test_copy_failure_leaves_no_partial_skill(self):
        spec = importlib.util.spec_from_file_location('packaging_helper', ROOT / 'scripts/package_skills.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        copytree = module.shutil.copytree
        def fail_pitch(source, *args, **kwargs):
            if Path(source) == ROOT / 'demo-pitch':
                raise OSError('simulated copy failure')
            return copytree(source, *args, **kwargs)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'skills'
            with mock.patch.object(sys, 'argv', ['package_skills.py', '--out', str(out)]), \
                 mock.patch.object(module.shutil, 'copytree', side_effect=fail_pitch):
                with self.assertRaises(OSError):
                    module.main()
            self.assertEqual(list(out.iterdir()), [])

    def test_renderer_cli_accepts_bom_and_creates_parent(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'input.json'
            data = json.loads((ROOT / 'demo-pitch/examples/supplylane-storyboard.json').read_text(encoding='utf-8'))
            source.write_text(json.dumps(data), encoding='utf-8-sig')
            output = Path(tmp) / 'nested/output.html'
            result = subprocess.run([sys.executable, str(ROOT / 'demo-pitch/scripts/render_storyboard.py'),
                                     str(source), str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(output.is_file())

    def test_renderer_refuses_to_replace_its_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'input.json'
            original = (ROOT / 'demo-pitch/examples/supplylane-storyboard.json').read_bytes()
            source.write_bytes(original)
            result = subprocess.run([sys.executable, str(ROOT / 'demo-pitch/scripts/render_storyboard.py'),
                                     str(source), str(source)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(source.read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
