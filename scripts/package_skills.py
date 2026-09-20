"""Export independent skills; never install globally or overwrite an existing skill."""
import argparse
from pathlib import Path
import shutil
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--feature-name', choices=('demo-features', 'feature-walkthrough'),
                        default='demo-features', help='Name for the exported feature skill only')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    out = args.out.resolve()
    if out == root or root in out.parents:
        parser.error('Choose an output directory outside this checkout')
    feature, pitch = out / args.feature_name, out / 'demo-pitch'
    for target in (feature, pitch):
        if target.exists():
            parser.error(f'Refusing to overwrite existing skill: {target}')
    out.mkdir(parents=True, exist_ok=True)
    # Finish copying both skills before making either destination visible.
    with tempfile.TemporaryDirectory(prefix='.skill-export-', dir=out) as temporary:
        stage = Path(temporary)
        staged_feature, staged_pitch = stage / args.feature_name, stage / 'demo-pitch'
        staged_feature.mkdir()
        source_skill = (root / 'SKILL.md').read_text(encoding='utf-8')
        source_skill = source_skill.replace('name: feature-walkthrough', 'name: ' + args.feature_name, 1)
        source_skill = source_skill.replace('/feature-walkthrough', '/' + args.feature_name)
        (staged_feature / 'SKILL.md').write_text(source_skill, encoding='utf-8')
        shutil.copy2(root / 'LICENSE', staged_feature / 'LICENSE')
        for name in ('reference', 'template', 'example'):
            shutil.copytree(root / name, staged_feature / name)
        shutil.copytree(root / 'demo-pitch', staged_pitch, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        for target in (feature, pitch):
            if target.exists():
                parser.error(f'Destination appeared during export: {target}')
        staged_feature.rename(feature)
        staged_pitch.rename(pitch)
    for target in (feature, pitch):
        print(target)


if __name__ == '__main__':
    main()
