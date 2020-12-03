import os

# os.chdir(os.path.join(os.getcwd(), 'wxpython', 'projectDjango'))
os.chdir(os.path.join(os.getcwd(), 'projectDjango'))

from projectDjango.apps import main

if __name__ == "__main__":
    main()
