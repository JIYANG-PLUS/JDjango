#!/usr/bin/env python
import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'JDjango'))

if __name__ == "__main__":
    from JDjango.apps import startRecognitionApp
    startRecognitionApp()