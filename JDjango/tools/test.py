import subprocess

order = r'python3.7 /Users/jiyang/Desktop/jiyang/manage.py runserver 8868'

server = subprocess.Popen(order, shell=True)
print(server.poll())
# server.wait()
# server.kill()
print(server.poll())

