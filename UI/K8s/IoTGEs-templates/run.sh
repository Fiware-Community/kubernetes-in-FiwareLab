load_jar ()
{
	nohup java -jar "$1" >/dev/null 2>&1 &	
	echo -e ""$2" has been started.\n"
}	

#declare -a arr=("eureka-server-0.0.1-SNAPSHOT" "gateway-0.0.1-SNAPSHOT" "EntityManager-0.0.1-SNAPSHOT" "QueryManager-0.0.1-SNAPSHOT")

declare -a arr=(`ls -l *.jar | awk '{ print $9}'`)

## now loop through the above array
for i in "${arr[@]}"
do
  b=$(echo $i | awk -F"-" '{print $1}')
  if [ -z "`ps -ef | grep "$i"| grep -v grep`" ];
  then
      load_jar $i $b
  else
       echo  -e ""$b" seems already running.\nRestarting again....."
       PID=`ps -ef | grep "$i" | grep -v 'grep' | awk '{ printf $2 }'`
       kill -9 $PID
       load_jar $i $b
  fi
done
