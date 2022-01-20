mkdir -p  /opt/sth-mongo/vol/{0..2}
kubectl create  configmap wrapper1 --from-file=./kube-mongo-statefulset.sh
kubectl create  -f ./volume1.yaml
kubectl create  -f ./volume2.yaml
kubectl create  -f ./volume3.yaml
kubectl create -f ./fiware-sth2-comet-service.yaml
sleep 10
kubectl create -f ./mongo-statefulset.yaml
echo "======waiting 120 sec for statefulset to deploy===="
sleep 120
echo "setting up mongodb in HA"
kubectl	exec  -it mongo2-0 /opt/kube-mongo-statefulset.sh
echo "waiting for HA to complete"
echo "waiting for HA to complete 15 sec"
sleep 15
kubectl create -f ./fiware-sth2-comet-deployment.yaml
sleep 30
echo "++++++++++sth-comet oneclick soln completed+++++++++++"
