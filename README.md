# PowerPy
> Power manegment script

![support](https://img.shields.io/badge/support-Debian%209-red.svg) ![license](https://img.shields.io/github/license/mashape/apistatus.svg)



This is a small powermanagment script. It's usefull for small home servers to reduce the running cost. The script can watch the established ports, and if no connections for a given time, the script will run a custom command  e.g. ``pm-suspend``

## Installation

### Pre-requirements

- netstat (part of ``net-tools``)
- suspend/hybernate script (e.g. pm-suspend from ``pm-utils``)
- root priviliges

#### Installation from sources

```
git pull https://github.com/Sch-Tomi/PowerPy.git
cd PowerPy
[vim/nano/micro] config.ini
[vim/nano/micro] init.d-starter.sh
sudo cp init.d-starter.sh /etc/init.d/powerpy
sudo chmod +x /etc/init.d/powerpy
sudo update-rc.d powerpy defaults 100
```

## Configuration

### sytem.d starter
In the installation process you have to edit the starter script. The only thing you have to do is edit the dir variable to your path.

### config.ini
#### BASIC
- checkInterval: INT
    Time passed between two netstat check in seconds

- inactiveTime: INT
    Inactive counter to run ``haltCommand``

- haltCommand: <SCRIPT>
    Default is pm-suspend, but you can change to any other.

- debug: 1
    0 - turn debug off
    1 - turn debug on

#### TCP,UDP,TCP/UDP
In each section you can add ports to check by the script. Syntax is simple:
```
<NAME>:<PORT>
```
The name is a fictive name, just to recognize your watched ports.

## Meta

[Sch-Tomi](https://github.com/Sch-Tomi)

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/Sch-Tomi/PowerPy](https://github.com/Sch-Tomi/PowerPy)
