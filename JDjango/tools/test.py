import subprocess


order = r'C:\Users\PC\Desktop\venv\Scripts\python C:\Users\PC\Desktop\djangoProject\HELLOWORD\manage.py runserver 8868'

server = subprocess.Popen(order, shell = True)
print(server.poll())
server.wait()
# server.kill()
print(server.poll())

