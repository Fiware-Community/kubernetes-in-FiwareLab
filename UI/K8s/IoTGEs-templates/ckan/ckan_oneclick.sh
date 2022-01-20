echo "starting ckan installation"
echo "/opt/ckan *(rw,sync,no_root_squash,no_all_squash)"  >> /etc/exports
echo "/opt/solr *(rw,sync,no_root_squash,no_all_squash)"  >> /etc/exports
echo "/opt/redis *(rw,sync,no_root_squash,no_all_squash)"  >> /etc/exports
mkdir -p /opt/ckan/postgres/postgres-pv01
#cp -rf /tmp/IotGEs//ckan/postgress/perm-data /opt/ckan/postgres/
mkdir -p /opt/ckan/postgres-replica/postgres-replica-pv01
mkdir  -p /opt/solr/vol/{0..2}
mkdir -p  /opt/redis/vol/{0..5}
#mkdir -p  /opt/ckan/ckanconfig
mkdir -p  /opt/ckan/ckandata
chmod 777 -R /opt/redis
chmod 777 -R /opt/solr
chmod 777 -R /opt/ckan
#cp -rf ./ckan/ckanconfig/* /opt/ckan/ckanconfig/
systemctl reload nfs-server
echo "postgres deployment started"
kubectl create configmap postgres  --from-file=postgress/config/postgres.conf --from-file=postgress/config/master.conf --from-file=postgress/config/replica.conf --from-file=postgress/config/pg_hba.conf --from-file=postgress/config/create-replica-user.sh
kubectl create -f ./postgress/postgres_vol/pg_replica_vol.yaml
sleep 4
kubectl create -f ./postgress/postgres_vol/pg_master_vol.yaml
sleep 4
kubectl create -f ./postgress/postgres_vol/pg_master_perm_data_vol.yaml
sleep 7
kubectl create -f ./postgress/service/service.yaml
kubectl create -f ./postgress/secret/secret.yml
kubectl create -f ./postgress/statefulset/statefulset-master.yaml
sleep 60
kubectl create -f ./postgress/statefulset/postgres-replica.yaml
sleep 80
kubectl exec -it postgres-0 bash /opt/data/00_create_datastore.sh
kubectl exec -it postgres-0 bash  /opt/data/perm1.sh
echo "datapusher deployment started"
kubectl create -f ./datapusher/datapusher.yaml
#kubectl create configmap postgres  --from-file=
#solr/configmap/solr-cluster-config.properties
echo "solr deployment started"
kubectl create -f ./solr/service/service-solr-cluster.yml
kubectl create -f ./solr/solr_vol/solr-vol1
sleep 4
kubectl create -f ./solr/solr_vol/solr-vol2
sleep 4
kubectl create -f ./solr/solr_vol/solr-vol3
sleep 10
kubectl create -f ./solr/statfulset/statefulset-solr-cluster.yml
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
echo 'yes'| kubectl exec -it redis-cluster-0 -- redis-cli --cluster create --cluster-replicas 1 $(kubectl get pods -l app=redis-cluster -o jsonpath='{range.items[*]}{.status.podIP}:6379 ')
sleep 10
echo "main comp ckan deployment started"
kubectl create -f ./ckan/ckan-vol.yaml
sleep 4
kubectl create -f ./ckan/ckan-vol-data.yaml
sleep 4
kubectl create -f ./ckan/ckan-service.yaml
kubectl create -f ./ckan/ckan-deployment.yaml
sleep 180
echo "ckan deployment completed"
