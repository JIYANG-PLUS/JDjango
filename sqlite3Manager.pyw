#!/usr/bin/env python
import os

PPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'JDjango')
os.chdir(PPATH)
from JDjango.apps import startSQLiteApp


if __name__ == "__main__":
    startSQLiteApp()

