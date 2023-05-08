from setuptools import setup

from pathlib import Path
dir = Path(__file__).parent
desc = (dir / 'README.md').read_text()

setup(
    name="roboviz",
    version="0.1",
    description="Robot Swarm Visualization Tool",
    packages=["src"],
    author="Ben Chiddy, Hamza Amir, Jonathan Doyle",
    install_requires=["panda3d"],
    python_requires=">=3.5",
    entry_points={"console_scripts": ["roboviz = src.main:run"]},
    long_description=desc
)
