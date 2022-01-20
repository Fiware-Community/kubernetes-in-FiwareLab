#!/bin/bash
sleep 10
cfg="{
    _id: 'rs0',
    members: [
        {_id: 0, host: 'mongo2-0.mongo2.default.svc.cluster.local:27017'},{_id: 1, host: 'mongo2-1.mongo2.default.svc.cluster.local:27017'},{_id: 2, host: 'mongo2-2.mongo2.default.svc.cluster.local:27017'}
    ]
}"
echo $cfg > /usr/share/check3
mongo  --eval "rs.initiate($cfg)"  | tee -a /usr/share/check3
echo "---"
