#!/bin/bash
PID=/tmp/weatherlink-service-bot.pid
LOG=/tmp/weatherlink-service-bot.log
ERROR=/tmp/weatherlink-service-bot-error.log

CMD="poetry run python3 src/weatherlink.py"
DIR="/home/pi/weatherlink-data-logger"

kill_cmd() {
  SIGNAL=""; MSG="Killing..."
  while true
  do
    LIST=`ps -ef | grep -v grep | grep $CMD | grep -w $USR | awk '{print $2}'`
    if [ "$LIST" ]
    then
      echo; echo "$MSG $LIST"; echo
      echo $LIST | xargs kill $SIGNAL
      sleep 2
      SIGNAL="-9" ; MSG="Killing $SIGNAL"
      if [ -f $PID ]
      then
        /bin/rm $PID
      fi
    else
      echo; echo "All killed..."; echo
      break
    fi
  done
}

start() {
  if [ -f $PID ]
  then
    echo
    echo "Application already started. PID: $( cat $PID )"
  else
    echo "==== Start"
    touch $PID
    if nohup $CMD >>$LOG 2>&1 &
    then echo $! >$PID
         cd $DIR
         echo "$(date '+%Y-%m-%d %X'): START" >>$LOG
    else echo "Error..."
         /bin/rm $PID
    fi
  fi
}

stop() {
  echo "==== Stop"
  if [ -f $PID ]
  then
    if kill $( cat $PID )
    then
      echo "$(date '+%Y-%m-%d %X'): STOP" >>$LOG
    fi
    /bin/rm $PID
    kill_cmd
  else
    echo "No pid file."
  fi
}

case "$1" in
  'start')
         start
         ;;
  'stop')
         stop
         ;;
  '')
         echo
         echo "Usage: $0 { start | stop }"
         echo
         exit 1
         ;;
esac

exit 0

