kubectl create configmap discovery-configmap --from-file=/tmp/IotGEs/fogflow/config/discovery/config.json
kubectl create configmap broker-configmap --from-file=/tmp/IotGEs/fogflow/config/broker/config.json
kubectl create configmap designer-configmap --from-file=/tmp/IotGEs/fogflow/config/designer/config.json
kubectl create configmap master-configmap --from-file=/tmp/IotGEs/fogflow/config/master/config.json
kubectl create configmap cloud-worker-configmap --from-file=/tmp/IotGEs/fogflow/config/cloud-worker/config.json
