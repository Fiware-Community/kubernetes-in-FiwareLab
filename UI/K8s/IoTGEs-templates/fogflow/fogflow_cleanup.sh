echo "Removing worker..."
kubectl delete -f cloud-worker-deployment.yaml

echo "Removing master..."
kubectl delete -f master-deployment.yaml

echo "Removing designer..."
kubectl delete -f designer-deployment.yaml

echo "Removing broker..."
kubectl delete -f broker-deployment.yaml

echo "Removing discovery..."
kubectl delete -f discovery-deployment.yaml

echo "Removing postgis..."
kubectl delete -f postgis-deployment.yaml

echo "Removing rabbitmq..."
kubectl delete -f rabbitmq-deployment.yaml

echo "____________________"

echo "Deleting master service..."
kubectl delete -f master-service.yaml

echo "Deleting designer service..."
kubectl delete -f designer-service.yaml

echo "Deleting broker service..."
kubectl delete -f broker-service.yaml

echo "Deleting discovery service..."
kubectl delete -f discovery-service.yaml

echo "Deleting postgis service..."
kubectl delete -f postgis-service.yaml

echo "Deleting rabbitmq service..."
kubectl delete -f rabbitmq-service.yaml

echo "____________________"

echo "ConfigMaps..."
kubectl delete configmap discovery-configmap
kubectl delete configmap broker-configmap
kubectl delete configmap designer-configmap
kubectl delete configmap master-configmap
kubectl delete configmap cloud-worker-configmap

echo "Complete!"
