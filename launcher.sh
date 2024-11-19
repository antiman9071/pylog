#! /bin/bash

SCRIPT_LOG_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )""/log.db"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

if [[ "$1" == "help" ]];
    then
        echo "PyLog [-w] [-g]"
        echo ""
        echo "PyLog runs a terminal based python script the two options are lited below"
        echo ""
        echo "all options are interchangeable this is just the order I put them in the code"
        echo ""
        echo "-w launches the program as a web based application(needs to be sudo)"
        echo ""
        echo "-g launches the program as a gui based application"
        exit 0;
    else
        while getopts ":w :g" opt; do
            case $opt in
            w) 
                sudo python3 $SCRIPT_DIR/webLog.py $SCRIPT_LOG_DIR
                exit 0;
                ;;
            g) 
                python3 $SCRIPT_DIR/guiLog.py $SCRIPT_LOG_DIR
                exit 0;
                ;;
            esac
        done
    fi
python3 $SCRIPT_DIR/terminalLog.py $SCRIPT_LOG_DIR

