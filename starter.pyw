#!/usr/bin/env python
import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'JDjango'))
from JDjango.apps import main

if __name__ == "__main__":
    main()
