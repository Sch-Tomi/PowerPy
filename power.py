import sys
import subprocess 
import configparser
from time import sleep

from deamon import daemon
from stopper import Stopper

class PowerPy(daemon):

    def __init__(self, pidfile):

        super().__init__(pidfile)

        self.observedPorts = {"TCP": [], "UDP": []}
        self.observationInterval = None
        self.inactiveTime = None
        self.haltCommand = None
        self.debug = None

        self.__readConf()

        self.stopper = Stopper()

    def run(self):
        while True:
            if self.debug:
                self.__printDebug()
            
            isConnectionActive = self.__examinePorts(self.__getActivePorts())

            if isConnectionActive:
                self.stopper.reset()
            else:
                self.stopper.progress()
                if self.stopper.timeSpent > self.inactiveTime:
                    self.__runCommand(self.haltCommand)
                    self.stopper.reset()
        
            sleep(self.observationInterval)
        

    def __readConf(self):
        config = configparser.ConfigParser()
        config.read("config.ini")

        self.inactiveTime = config["BASIC"].getint("inactiveTime")
        self.observationInterval = config["BASIC"].getint("checkInterval")
        self.debug = config["BASIC"].getint("debug")
        self.haltCommand = config["BASIC"]["haltCommand"]

        for protocol in ["TCP", "UDP"]:
            if protocol in config:
                self.observedPorts[protocol] = [val for key, val in config[protocol].items()]

        if "TCP/UDP" in config:
            for key, val in config['TCP/UDP'].items():
                if val not in self.observedPorts["TCP"]:
                    self.observedPorts["TCP"].append(val)
                if val not in self.observedPorts["UDP"]:
                    self.observedPorts["UDP"].append(val)


    def __getActivePorts(self):
        output = self.__runCommand("netstat -antu | grep ESTABLISHED").decode('UTF-8')
        return self.__processOutputPorts(output)

    def __runCommand(self, command):
        #out = subprocess.check_output(command.split())
        #print(out)
        ps = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        out = ps.communicate()[0]
        return out
    
    def __processOutputPorts(self, output):
        """
        Connection Indexes:
        0 - tcp/udp
        1 - Recv-Q
        2 - Send-Q
        3 - Local Address (IP:PORT)
        4 - Foreign Address
        5 - State (LISTEN / ESTABLISHED / TIME_WAIT / CLOSE_WAIT)
        """
        ports = {"TCP":[], "UDP":[]}
        for line in str(output).splitlines():
            connection = line.split()
            ip = connection[3]

            ports[str(connection[0]).upper()].append(ip.split(":")[1])
        return ports

    def __examinePorts(self, activePorts):
        for protocol in activePorts.keys():
            for port in activePorts[protocol]:
                if port in self.observedPorts[protocol]:
                    if self.debug:
                        sys.stdout.write("Active port: {}".format(port))
                    return True
        return False

    def __printDebug(self):
        sys.stdout.write("Observed ports: {}".format(self.observedPorts))
        sys.stdout.write("Active ports: {}".format(self.__getActivePorts()))
        sys.stdout.write("Matched ports: {}".format(self.__examinePorts(self.__getActivePorts())))
        sys.stdout.write("Stopper time: {}".format(self.stopper.timeSpent))
        sys.stdout.write("\n\n ------------------------ \n\n")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        daemon = PowerPy(sys.argv[2])
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            sys.stdout.write("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        sys.stdout.write("usage: {} start|stop|restart".format(sys.argv[0]))
        sys.exit(2)
    