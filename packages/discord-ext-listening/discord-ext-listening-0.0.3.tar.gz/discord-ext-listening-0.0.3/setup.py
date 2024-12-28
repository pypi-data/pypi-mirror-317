from setuptools import setup
import re
import subprocess

# Read requirements from requirements.txt
requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Extract version from __init__.py
version = ''
with open('discord/ext/listening/__init__.py') as f:
    version_match = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE)
    if version_match:
        version = version_match.group(1)

if not version:
    raise RuntimeError('Version is not set')

# Append version info for pre-releases
if version.endswith(('a', 'b', 'rc')):
    try:
        commit_count = subprocess.check_output(['git', 'rev-list', '--count', 'HEAD']).decode('utf-8').strip()
        commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('utf-8').strip()
        version += f'{commit_count}+g{commit_hash}'
    except Exception:
        pass

# Read the README file
readme = ''
with open('README.md') as f:
    readme = f.read()

# Define the package setup
setup(
    name="discord-ext-listening",
    author="Sheppsu",
    url="https://github.com/sheppsu/discord-ext-listening",
    version=version,
    packages=["discord.ext.listening"],
    license="MIT",
    description="Voice receive extension for discord.py built on multiprocessing and designed to be flexible.",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.8.0",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: Capture/Recording"
    ],
)
