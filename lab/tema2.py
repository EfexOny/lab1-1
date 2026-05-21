import subprocess

def main():
    # comanda = input("comanda:")
    comanda = "ip a | grep inet | wc -l"

    cmd = []
    for comenzi in comanda.split("|"):
        cmd.append(comenzi.split())

    intrare = None
    proces = None

    for arg in cmd:
        proces = subprocess.Popen(arg,stdin=intrare,stdout=subprocess.PIPE)
        intrare = proces.stdout


    rez = proces.communicate()

    if rez:
        print(rez[0])

if __name__ == "__main__":
    main()