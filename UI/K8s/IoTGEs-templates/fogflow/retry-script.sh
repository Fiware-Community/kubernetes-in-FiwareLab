echo "Checking if $1 pod is up.."
DATA=""
RETRY=40
while [ $RETRY -gt 0 ]
do
    DATA=$(kubectl get pods | grep "Running" | grep $1 )
    if [ $? -eq 0 ]
    then
        break
    else
        sleep 5
    fi
    (( RETRY-- ))
    echo "Retrying... $RETRY"

done
echo "$1 is now running..."
