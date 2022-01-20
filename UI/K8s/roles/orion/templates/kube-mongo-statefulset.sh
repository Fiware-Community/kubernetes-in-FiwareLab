#!/bin/bash
sleep 10
cfg="{
    _id: 'rs0',
    members: [
        {_id: 0, host: 'mongo-0.mongo.{{ k8s_namespace }}.svc.cluster.local:27017'},{_id: 1, host: 'mongo-1.mongo.{{ k8s_namespace }}.svc.cluster.local:27017'},{_id: 2, host: 'mongo-2.mongo.{{ k8s_namespace }}.svc.cluster.local:27017'},{_id: 3, host: 'mongo-3.mongo.{{ k8s_namespace }}.svc.cluster.local:27017'},{_id: 4, host: 'mongo-4.mongo.{{ k8s_namespace }}.svc.cluster.local:27017'}
    ]
}"
echo $cfg > /usr/share/check2
mongo  --eval "rs.initiate($cfg)"  | tee -a /usr/share/check1
echo "---"

