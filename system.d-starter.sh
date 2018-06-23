#!/bin/sh
### BEGIN INIT INFO
# Provides:                      PowerPy
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO

dir="/home/tomi/PowerPy"
cmd="python3 power.py"
user=""

name=`basename $0`
pid_file="/var/run/$name.pid"
stdout_log="/var/log/$name.log"
stderr_log="/var/log/$name.err"

get_pid() {
    cat "$pid_file"
}

is_running() {
    [ -f "$pid_file" ] && [ $(ps -u root | grep $(get_pid) | wc -l) -eq 1 ]
}

case "$1" in
    start)
    if is_running; then
        echo "Already started"
    else
        echo "Starting $name"
        cd "$dir"
        sudo $cmd "start" $pid_file >> "$stdout_log" 2>> "$stderr_log" &
        sleep 1

        if ! is_running; then
            echo "Unable to start, see $stdout_log and $stderr_log"
            exit 1
                else
                        echo "Started:" `get_pid`
        fi
    fi
    ;;
    stop)
    if is_running; then
        echo -n "Stopping $name.."
        cd "$dir"
        sudo $cmd "stop" $pid_file >> "$stdout_log" 2>> "$stderr_log" & 
        for i in 1 2 3 4 5 6 7 8 9 10
        # for i in `seq 10`
        do
            if ! is_running; then
                break
            fi

            echo -n "."
            sleep 1
        done
        echo

        if is_running; then
            echo "Not stopped; may still be shutting down or shutdown may have failed"
            exit 1
        else
            echo "Stopped"
            if [ -f "$pid_file" ]; then
                rm "$pid_file"
            fi
        fi
    else
        echo "Not running"
    fi
    ;;
    restart)
    cd "$dir"
    sudo $cmd "restart" $pid_file >> "$stdout_log" 2>> "$stderr_log" &
    sleep 1
    $0 status
    ;;
    status)
    if is_running; then
        echo "Running" `get_pid`
    else
        echo "Stopped"
        exit 1
    fi
    ;;
    *)
    echo "Usage: $0 {start|stop|restart|status}"
    exit 1
    ;;
esac

exit 0