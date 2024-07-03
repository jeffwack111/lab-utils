import subprocess

if __name__ == "__main__":
    devnull = subprocess.DEVNULL
    subprocess.Popen(['nohup', 'pyro5-ns', '-n', '192.168.50.179'], stdout=devnull, stderr=devnull)
    print("nameserver started")