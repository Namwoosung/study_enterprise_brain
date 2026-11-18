"""Build the current learning course locally or from a standalone Sites checkout."""
from pathlib import Path
import os, shutil, subprocess, sys

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parent
SOURCE=HERE/'source-materials-v2'
ASSETS=HERE/'course-reader'
if (PROJECT/'learning-v2/manifest.json').exists():
    shutil.copytree(PROJECT/'learning-v2',SOURCE,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    ASSETS.mkdir(exist_ok=True)
    for name in ['build.py','reader.css','reader.js','panels.py']:
        src=PROJECT/'rebuild/reader'/name
        if src.exists():shutil.copy2(src,ASSETS/name)
    for original,target in [('build.py','comparison_builder.py'),('reading.css','comparison.css'),('reading.js','comparison.js')]:
        shutil.copy2(PROJECT/'rebuild/prototypes'/original,ASSETS/target)
if not (SOURCE/'manifest.json').exists():
    raise SystemExit('Missing course source snapshot')
legacy=HERE/'legacy-v1'
if not legacy.exists() and (HERE/'dist/content.js').exists():
    shutil.copytree(HERE/'dist',legacy,ignore=shutil.ignore_patterns('legacy'))
env=os.environ.copy()
env.update(COURSE_PROJECT_ROOT=str(HERE),COURSE_SOURCE=str(SOURCE),COURSE_OUTPUT=str(HERE/'dist'))
subprocess.run([sys.executable,str(ASSETS/'build.py')],env=env,check=True)
if legacy.exists():shutil.copytree(legacy,HERE/'dist/legacy',dirs_exist_ok=True)
