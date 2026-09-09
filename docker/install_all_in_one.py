import os
import time
from subprocess import Popen, PIPE
import subprocess


class bc:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    TEAL = '\033[96m'
    BLACK = '\033[97m'
    GRAY = '\033[90m'
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    lightred = '\033[91m'
    lightgreen = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    lightcyan = '\033[96m'


def cstr(i) -> str:
    return '\033[' + str(i) + 'm'


def make_timestamp() -> str:

    hh = time.localtime().tm_hour.__str__()
    mm = time.localtime().tm_min.__str__()
    ss = time.localtime().tm_sec.__str__()
    dd = time.localtime().tm_mday.__str__()
    MM = time.localtime().tm_mon.__str__()
    YY = time.localtime().tm_year.__str__()

    ts = hh+":"+mm+":"+ss+"__"+dd+"_"+MM+"_"+YY

    return ts


def log_error(pout: list, cmd):
    try:
        if os.path.exists("../logs"):
            t = make_timestamp()
            with open("../logs/" + t, "w") as file:
                file.writelines([str(cmd)] + pout)
            file.close()
            print('\033[93m logged to: \033[0m ../logs/' + t)
    except:
        print('\033[35m Couldn\'t save error output to ./../logs \033[0m')


class AKInstallation():

    def __init__(self):
        print("installation obj called...")

    @classmethod
    def print_array_line(cls, args):
        try:
            loop = 0
            color1 = bc.green
            end1 = bc.ENDC
            color2 = bc.blue
            if type(args) == str:
                color1 = bc.lightgreen + bc.BOLD
                end1 = bc.ENDC + bc.ENDC
                args = args.split(" ")
            odd = True
            for cmd in args:
                if loop == 0:
                    print(color1 + cmd + end1, end=' ')
                else:
                    if odd == True:
                        odd = not odd
                        color2 = bc.pink
                    else:
                        color2 = bc.lightblue
                    print(color2 + cmd + end1, end=' ')
                if len(args) == loop + 1:
                    print("")
                loop += 1
        except:
            print(cstr(31) + "PRINT ARRAYLINE FAILURE: " + cstr(0) + cstr(95))
            print(args)
            print(cstr(0))

    @classmethod
    def execute(cls, cmd, installation_phase):
        """
        runs a terminal command and waits for completion to then print all output at once.

        :param cmd: the full terminal command
        :param installation_phase: the current command number (1,2,3,4,...x)
        :return: void
        """
        args = cmd
        cls.print_array_line(args)
        print(args)
        proc = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = proc.communicate("")
        term_reply = output.decode('utf-8')
        term_errors = err.decode('utf-8')
        print(cstr(104) + cstr(37) + term_reply + cstr(0) + cstr(0))
        try:
            if len(term_errors) > 1 and args[0] != 'rm':
                print(cstr(107) + cstr(91) + term_errors + cstr(0) + cstr(0))
                os.system("say 'Warning, " + args[0] + " error.'")
        except:
            print(cstr(31) + "CAUSE OF EXEC FAILURE: " + cstr(0) + cstr(35))
            print(cmd)
            print(cstr(0))

    @classmethod
    def execute_realtime_out(cls, cmd: list, installation_phase):
        """
        runs a terminal command and gets all output in realtime.

        :param cmd: the full terminal command
        :param installation_phase: the current command number (1,2,3,4,...x)
        :return: void
        """
        print(cstr(91) + "╔══════════════════════════════════════════════════")
        print("║ ", end=cstr(0))
        for c in cmd:
            if c == "docker":
                print(bc.green, end="")
            elif c == "exec":
                print(bc.blue, end="")
            elif c == "-it":
                print(bc.yellow, end="")
            elif c == "-p":
                print(bc.cyan, end="")
            elif c[0:8] == "armprime":
                print(bc.red, end="")
            else:
                print(bc.purple, end="")
            print(c, end=" ")
            print(bc.ENDC, end="")
        print(cstr(91) + "\n╠══════════════════════════════════════════════════", end=cstr(0))
        try:
            args = cmd
            with Popen(args, stdout=PIPE) as p:
                log_buffer = []
                print(cstr(91) + "\n║ ", end=cstr(0))
                for line in p.stdout:
                    if installation_phase > 99:
                        print(".", end="")
                    else:
                        outstr1 = line.decode("utf-8").replace("\n", "\n")
                        outstr2 = outstr1.replace(" : RUN ", cstr(91) + " : RUN " + cstr(0))
                        print(cstr(92) + '<◈═══◘▸' + cstr(0), end=cstr(33) + outstr2)
                    log_buffer.append(line.decode("utf-8"))
                p.communicate("", 100)
                exitcode = p.returncode
                if exitcode != 0:
                    print("\033[41mUnexpected Error\033[0m", end="")
                    print("\033[5m\033[0m")
            #inp = input("press \033[35m[ENTER]\033[0m to skip.")
        except:
            print(cstr(91) + "║ " + cstr(0) + cstr(31) + "CAUSE OF THE TERMINAL CMD FAILURE: " + cstr(0))
            print(cmd)
        print(cstr(91) + "╚══════════════════════════════════════════════════" + cstr(0))

    @classmethod
    def destroy_docker(cls):
        """
        Completely wipe out all docker containers running on this machine.
        """
        cmd = ('sh KILL_ALL_.sh')
        os.system(cmd)


class InstallationRuntime:

    def __init__(self):
        self.install_all_in_one = True
        WORK_DIR = os.getcwd()
        PARENT_DIRPATH = os.path.abspath(os.path.join(WORK_DIR, os.pardir))
        installer = AKInstallation()

        print(bc.lightblue + "WORKING IN " + bc.ENDC + bc.pink + WORK_DIR + bc.ENDC)

        DOCKER_SQL_NAME = "armprime-postgres"
        SQL_USER = "jawn"
        SQL_PASS = "xzxzf87d93a3f32551927489028495710693217ffb64bed152ae124d2e79xzxz"
        SQL_PUBLIC_PORT = "8091"
        SQL_PRIVATE_PORT = "5432"
        SQL_ARGS = "-e POSTGRES_USER=" + \
                   SQL_USER + " -d -p " + \
                   "POSTGRES_PASSWORD=" + SQL_PASS + \
                   SQL_PUBLIC_PORT + ":" + \
                   SQL_PRIVATE_PORT + " " + \
                   DOCKER_SQL_NAME

        ORDERED_COMMANDS = []

        cmd_n01 = ['docker', 'build', '-t', 'mattjawn/armprime', './app/']
        cmd_n02 = ['docker',
                   'run',
                   '--name',
                   'armprime-postgres',
                   '-e',
                   'POSTGRES_USER=jawn',
                   '-e',
                   'POSTGRES_PASSWORD=xzxzf87d93a3f32551927489028495710693217ffb64bed152ae124d2e79xzxz',
                   '-d',
                   '-p',
                   '8091:5432',
                   'postgres']

        cmd_n03 = ['docker', 'run', '-d', '-p', '7070:6379', '--name=armprime-redis', 'redis']
        pp = PARENT_DIRPATH + ':/usr/src/app/'
        cmd_n04 = ['docker', 'run', '-d', '--expose=443', '-p', '80:80', '-p', '443:443', '-v', pp, '--link', 'armprime-postgres:postgres', '--link',
                   'armprime-redis:redis', '--name=armprime', 'mattjawn/armprime']
        cmd_n05 = ['docker', 'exec', 'armprime-redis', 'redis-cli', 'config', 'set', 'notify-keyspace-events', 'KEA']
        cmd_n06 = ['docker', 'exec', '-it', 'armprime-postgres', 'useradd', '-p', '$(openssl passwd -1 123123)', 'jawn']
        cmd_n07 = ['sh', 'create_psql_extensions.sh']

        cmd_n08 = ['rm', '-R', '"../krogoth_gantry/migrations"']
        cmd_n09 = ['rm', '-R', '"../krogoth_chat/migrations"']
        cmd_n10 = ['rm', '-R', '"../krogoth_3rdparty_api/migrations"']
        cmd_n11 = ['rm', '-R', '"../krogoth_examples/migrations"']
        cmd_n12 = ['rm', '-R', '"../krogoth_admin/migrations"']
        cmd_n13 = ['rm', '-R', '"../krogoth_apps/migrations"']
        cmd_n14 = ['rm', '-R', '"../krogoth_social/migrations"']
        cmd_n15 = ['rm', '-R', '"../moho_extractor/migrations"']
        cmd_n16 = ['rm', '-R', '"../kbot_lab/migrations"']

        MIGRATIONS = ['krogoth_gantry']
        cmd_n18 = ['docker', 'exec', '-it', 'armprime', './manage.py', 'makemigrations'] + MIGRATIONS
        cmd_n18_1 = ['docker', 'exec', '-it', 'armprime', './manage.py', 'makemigrations']
        cmd_n19 = ['docker', 'exec', '-it', 'armprime', './manage.py', 'migrate']
        cmd_n21 = ['docker', 'exec', '-it', 'armprime', './manage.py', 'installdjangular']
        ak_install = ['docker', 'exec', '-it', 'armprime', './manage.py', 'collectdvc']
        static_col = ['docker', 'exec', '-it', 'armprime', './manage.py', 'collectstatic']

        get_pyink = ['docker','exec','-it','armprime',"pip","install","git+https://github.com/MattAndrzejczuk/pyink.git"]

        # ORDERED_COMMANDS.append(cmd_n01)
        # ORDERED_COMMANDS.append(cmd_n02)
        # ORDERED_COMMANDS.append(cmd_n03)
        # ORDERED_COMMANDS.append(cmd_n04)
        # ORDERED_COMMANDS.append(cmd_n05)
        # ORDERED_COMMANDS.append(cmd_n06)
        # ORDERED_COMMANDS.append(cmd_n07)
        # ORDERED_COMMANDS.append(cmd_n08)
        # ORDERED_COMMANDS.append(cmd_n09)
        # ORDERED_COMMANDS.append(cmd_n10)
        # ORDERED_COMMANDS.append(cmd_n11)
        # ORDERED_COMMANDS.append(cmd_n12)
        # ORDERED_COMMANDS.append(cmd_n13)
        # ORDERED_COMMANDS.append(cmd_n14)
        # ORDERED_COMMANDS.append(cmd_n15)
        # ORDERED_COMMANDS.append(cmd_n16)
        # ORDERED_COMMANDS.append(cmd_n18)
        # ORDERED_COMMANDS.append(cmd_n18_1)
        # ORDERED_COMMANDS.append(cmd_n19)
        # ORDERED_COMMANDS.append(cmd_n21)


        # wait = input('ready?')
        
        dexec = ['docker', 'exec', '-it', 'armprime', 'pip3', 'install', '-r', 'requirements.txt']
        
        dexec2 = ['docker', 'exec', '-it', 'armprime', 'pip3', 'install', 'psycopg2-binary']
        dexec3 = ['docker', 'exec', '-it', 'armprime', 'pip3', 'install', 'requests-oauthlib']

        installer.destroy_docker()
        AKInstallation.execute_realtime_out(cmd_n01, 1)
        AKInstallation.execute_realtime_out(cmd_n02, 2)
        AKInstallation.execute_realtime_out(cmd_n03, 3)
        AKInstallation.execute_realtime_out(cmd_n04, 4)
        AKInstallation.execute_realtime_out(cmd_n05, 5)
        AKInstallation.execute_realtime_out(cmd_n06, 6)
        AKInstallation.execute_realtime_out(cmd_n08, 8)
        AKInstallation.execute_realtime_out(cmd_n07, 7)
        ### ---====== remove previous migrations ======---
        AKInstallation.execute_realtime_out(get_pyink, 8)
        # AKInstallation.execute_realtime_out(cmd_n08, -1)
        # AKInstallation.execute_realtime_out(cmd_n09, -1)
        # AKInstallation.execute_realtime_out(cmd_n10, -1)
        # AKInstallation.execute_realtime_out(cmd_n11, -1)
        # AKInstallation.execute_realtime_out(cmd_n12, -1)
        # AKInstallation.execute_realtime_out(cmd_n13, -1)
        # AKInstallation.execute_realtime_out(cmd_n14, -1)
        # AKInstallation.execute_realtime_out(cmd_n15, -1)
        # AKInstallation.execute_realtime_out(cmd_n16, -1)
        AKInstallation.execute_realtime_out(dexec, 16)
        AKInstallation.execute_realtime_out(dexec2, 17)
        AKInstallation.execute_realtime_out(dexec3, 18)
        ### ---====== make new migrations ======---
        AKInstallation.execute_realtime_out(cmd_n18, 19)
        AKInstallation.execute_realtime_out(cmd_n19, 20)
        ### ---====== install krogoth gantry units ======---
        AKInstallation.execute_realtime_out(cmd_n21, 21)
        AKInstallation.execute_realtime_out(ak_install, 100)
        AKInstallation.execute_realtime_out(static_col, 101)


        ### ---====== install global fuse units ======---

        ### ---====== fin ======---
        os.system('docker exec -it armprime ./manage.py createsuperuser')


InstallationRuntime()
