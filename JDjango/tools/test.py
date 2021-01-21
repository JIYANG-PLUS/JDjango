import subprocess

server = subprocess.Popen('python -m http.server 3000', shell=True)
server.wait()

