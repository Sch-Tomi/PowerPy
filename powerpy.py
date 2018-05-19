import sys
import subprocess 
from time import sleep

from deamon import daemon
from stopper import Stopper

class PowerPy(daemon):

    def __init__(self, pidfile):

        super().__init__(pidfile)

        self.observedPorts = ["80", "22", "443"]
        self.observationInterval = 5
        self.observationState = 1
        self.inactiveTime = 300
        self.haltCommand = "echo VEGE"

        self.debug = 1

        self.stopper = Stopper()

    def run(self):
        while self.observationState:
            if self.debug:
                self.__printDebug()
            
            isConnectionActive = self.__examinePorts(self.__getActivePorts())

            if isConnectionActive:
                self.stopper.reset()
            else:
                self.stopper.progress()
                if self.stopper.timeSpent > self.inactiveTime:
                    break
        
            sleep(self.observationInterval)
        self.__runCommand(self.haltCommand)

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
        ports = []
        for line in str(output).splitlines():
            connection = line.split()
            ip = connection[3]
            ports.append(ip.split(":")[1])
        return ports

    def __examinePorts(self, activePorts):
        for port in activePorts:
            if port in self.observedPorts:
                if self.debug:
                    print("Active port: {}".format(port))
                return True
        return False

    def __printDebug(self):
        print("Observed ports: {}".format(self.observedPorts))
        print("Active ports: {}".format(self.__getActivePorts()))
        print("Matched ports: {}".format(self.__examinePorts(self.__getActivePorts())))
        print("Stopper time: {}".format(self.stopper.timeSpent))
        print("\n\n ------------------------ \n\n")

if __name__ == "__main__":
    daemon = PowerPy('/tmp/powerpy.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart".format(sys.argv[0]))
        sys.exit(2)
    