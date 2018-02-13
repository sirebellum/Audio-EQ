IP=$1
SLEEP=$2

if [ -z $1 ]
then
    echo "Please specify an IP!"
    exit
fi

if [ $SLEEP = 'y' ]
then sleep 2
fi

gst-launch-1.0 alsasrc device=hw:1 ! udpsink host=$1 port=9001
