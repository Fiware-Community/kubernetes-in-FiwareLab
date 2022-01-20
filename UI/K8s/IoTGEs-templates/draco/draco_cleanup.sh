echo "++++++++++draco cleanup start+++++++++++"
kubectl delete  -f ./kube_sql_svc.yaml
kubectl delete -f ./kube_svc_draco.yaml
kubectl delete -f ./kube_draco_etc.yaml
kubectl delete -f ./sql-statefulset.yaml
kubectl delete -f ./kube_draco_deployment.yaml
kubectl delete  pvc mysql-datadir-galera-ss-0 mysql-datadir-galera-ss-1 mysql-datadir-galera-ss-2 
kubectl delete pv datadir-galera-0 datadir-galera-1 datadir-galera-2
rm -rvf /data/pods/*
rm -rvf /var/lib/mysql
echo "++++++++++draco cleanup done+++++++++++"
