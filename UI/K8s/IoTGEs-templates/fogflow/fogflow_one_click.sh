echo "Creating rabbitmq service..."
kubectl create -f rabbitmq-service.yaml

echo "Creating postgis service..."
kubectl create -f postgis-service.yaml

echo "Creating discovery service..."
kubectl create -f discovery-service.yaml

echo "Creating broker service..."
kubectl create -f broker-service.yaml

echo "Creating designer service..."
kubectl create -f designer-service.yaml

echo "Creating master service..."
kubectl create -f master-service.yaml

echo "________________________________"

echo "Creating ConfigMaps..."
./config-map.sh

echo "________________________________"

mkdir /tmp/fog

echo "Deploying rabbitmq..."
kubectl create -f rabbitmq-deployment.yaml
./retry-script.sh "rabbitmq" > /tmp/fog/rabbit.txt

echo "Deploying postgis..."
kubectl create -f postgis-deployment.yaml
./retry-script.sh "postgis" > /tmp/fog/postgis.txt

echo "Deploying discovery..."
kubectl create -f discovery-deployment.yaml
./retry-script.sh "discovery" > /tmp/fog/discovery.txt

echo "Deploying broker..."
kubectl create -f broker-deployment.yaml
./retry-script.sh "broker" > /tmp/fog/broker.txt

echo "Deploying designer..."
kubectl create -f designer-deployment.yaml
./retry-script.sh "designer" > /tmp/fog/designer.txt

echo "Deploying master..."
kubectl create -f master-deployment.yaml
./retry-script.sh "master" > /tmp/fog/master.txt

echo "Deploying worker..."
kubectl create -f cloud-worker-deployment.yaml
./retry-script.sh "cloud-worker" > /tmp/fog/cloud-worker.txt


echo "Complete!"
