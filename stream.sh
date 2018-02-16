IP=$1
FILE=$2

if [ -z $1 ]
then
    echo "Please specify an IP!"
    exit
fi

if [ -z $2 ]
then
    gst-launch-1.0 alsasrc device=hw:1 ! udpsink host=$1 port=9001
else
    gst-launch-1.0 -v filesrc location=$FILE ! wavparse ! udpsink host=$IP port=9001
fi

