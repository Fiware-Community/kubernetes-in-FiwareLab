echo "++++++++++draco oneclick soln started+++++++++++"
mkdir -p  /opt/draco/galera-0/datadir
mkdir -p  /opt/draco/galera-1/datadir
mkdir -p  /opt/draco/galera-2/datadir
chmod 777 -R /opt/draco
echo "/opt/draco *(rw,sync,no_root_squash,no_all_squash)"  >> /etc/exports
systemctl reload nfs-server
kubectl create  -f ./kube_sql_etc.yaml
kubectl create  -f ./Volume1.yaml
kubectl create  -f ./Volume2.yaml
kubectl create  -f ./Volume3.yaml
sleep 10
#kubectl create  -f ./kube_sql_svc.yaml
kubectl create -f ./sql-statefulset.yaml
echo "======waiting 360 sec for statefulset to deploy===="
sleep 40
kubectl create -f ./kube_svc_draco.yaml
echo "setting up mysql completed in HA"
kubectl create -f ./kube_draco_deployment.yaml
echo "======waiting 240 sec for draco to deploy===="
sleep 120

echo "++++++++++draco oneclick soln completed+++++++++++"
