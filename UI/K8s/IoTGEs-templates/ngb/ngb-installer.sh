######### NGB Installation Script #########
### Java8 installation:
echo "Installing Java..."
sudo add-apt-repository -y ppa:webupd8team/java
sudo apt-get -y update
echo "oracle-java8-installer shared/accepted-oracle-license-v1-1 select true" | debconf-set-selections
echo "oracle-java8-installer shared/accepted-oracle-license-v1-1 seen true" | debconf-set-selections
sudo apt-get -y install oracle-java8-installer
sudo echo 'JAVA_HOME="/usr/lib/jvm/java-8-oracle"' >> /etc/environment
source /etc/environment
sudo echo $JAVA_HOME
echo "Java Home Variable set..."

### Postgres installation:
echo "Installing Postgres..."
sudo apt install -y postgresql-10 postgresql-client-10 postgresql-server-dev-10
sudo apt install -y postgresql-10-postgis-2.4 postgresql-10-postgis-scripts
cd /usr/local/src/
git clone https://github.com/arkhipov/temporal_tables
cd temporal_tables/
apt install make
apt-get install -y build-essential
make
make install
echo "Creating ngb user and ngb databse..."
su postgres <<EOSU
psql -c "create user ngb superuser createdb password 'ngb'";
psql -c "create database ngb owner = ngb";
EOSU

mkdir /tmp/ngbroker
cd /tmp/ngbroker
### kafka installation:
echo "Downloading Kafka..."
sudo wget "http://www-eu.apache.org/dist/kafka/1.0.1/kafka_2.12-1.0.1.tgz"
sudo tar -xvf kafka_2.12-1.0.1.tgz
sudo mv kafka_2.12-1.0.1 kafka
cd kafka
echo "Starting Zookeeper..."
sudo ./bin/zookeeper-server-start.sh -daemon config/zookeeper.properties
echo "Starting KafkaServer..."
sudo ./bin/kafka-server-start.sh -daemon config/server.properties
cd /tmp/ngbroker
echo "Starting jars..."
cd BinariesForTesting
chmod +x run.sh
`/bin/bash ./run.sh > ../run-logs.txt`
echo "Started jars..."

rm -f ../kafka_2.12-1.0.1.tgz
rm -rvf ../kafka_2.12-1.0.1 kafka

echo "Checking if NG broker is up.."
DATA=""
RETRY=40
while [ $RETRY -gt 0 ]
do
    DATA=$(netstat -tnlp | grep 8761)
    if [ $? -eq 0 ]
    then
        break
    else
        #echo "Retrying..."
        sleep 5
    fi
    echo "Retrying..."
done

echo "Listening at port 8761..."

echo "Complete!"
