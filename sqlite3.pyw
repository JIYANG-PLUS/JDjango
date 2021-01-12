#!/usr/bin/env python
import os

os.chdir(os.path.join(os.getcwd(), 'JDjango'))

from JDjango.apps import startSQLiteApp

if __name__ == "__main__":
    startSQLiteApp()
