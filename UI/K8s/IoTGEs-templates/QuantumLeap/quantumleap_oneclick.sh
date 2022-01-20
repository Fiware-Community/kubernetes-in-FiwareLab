echo "starting quantumleap installation"
echo "/opt/cratedb *(rw,sync,no_root_squash,no_all_squash)"  >> /etc/exports
echo "/opt/quantumleap *(rw,sync,no_root_squash,no_all_squash)"  >> /etc/exports
echo "/opt/grafana *(rw,sync,no_root_squash,no_all_squash)"  >> /etc/exports
echo "/opt/qp/redis *(rw,sync,no_root_squash,no_all_squash)"  >> /etc/exports
mkdir  -p /opt/cratedb/vol/{0..2}
mkdir -p  /opt/cratedb/data
mkdir -p  /opt/quantumleap
mkdir -p  /opt/grafana
mkdir -p  /opt/qp/redis/vol/{0..5}
chmod 777 -R /opt/cratedb
chmod 777 -R /opt/quantumleap
chmod 777 -R /opt/grafana
chmod 777 -R /opt/qp/redis
systemctl reload nfs-server
echo "cratedb deployment started"
kubectl create -f ./crate/vol1.yaml
kubectl create -f ./crate/vol2.yaml
kubectl create -f ./crate/vol3.yaml
sleep 4
kubectl create -f ./crate/crate-internal-service.yaml
kubectl create -f ./crate/crate-external-service.yaml
kubectl create -f ./crate/crate-controller.yaml
sleep 60
echo "redis deployment started"
kubectl create -f ./redis/redis-svc.yaml
kubectl create -f ./redis/redis-vol/redis-vol1.yaml
sleep 4
kubectl create -f ./redis/redis-vol/redis-vol2.yaml
sleep 4
kubectl create -f ./redis/redis-vol/redis-vol3.yaml
sleep 4
kubectl create -f ./redis/redis-vol/redis-vol4.yaml
sleep 4
kubectl create -f ./redis/redis-vol/redis-vol5.yaml
sleep 4
kubectl create -f ./redis/redis-vol/redis-vol6.yaml
sleep 4
kubectl create -f ./redis/redis-sts.yaml
sleep 70
echo 'yes'| kubectl exec -it redis-cluster2-0 -- redis-cli --cluster create --cluster-replicas 1 $(kubectl get pods -l app=redis-cluster2 -o jsonpath='{range.items[*]}{.status.podIP}:6379 ')
sleep 10

echo "quantumleap deployment started"
kubectl create -f ./quantumleap/quantumleap-service.yaml
kubectl create -f ./quantumleap/quantumleap-deployment.yaml
sleep 60
echo "grafana deployment started"
kubectl create -f ./grafana/grafana-service.yaml
kubectl create -f ./grafana/grafana-deployment.yaml
sleep 80
echo "quantumleap deployment completed"
