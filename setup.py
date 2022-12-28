"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['startscreen.py']
DATA_FILES = ['project.py', 'timerecord.py', 'timetracker.py', 'application.py','mainscreen.py', 'stringbuilder.py','icon.jpeg']
OPTIONS = {}

setup(
    name="Projekt Manager",
    version="1.0",
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
