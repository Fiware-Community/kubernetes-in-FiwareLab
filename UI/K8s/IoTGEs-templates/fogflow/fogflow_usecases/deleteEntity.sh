echo ">> Delete request for an entity based on id and type <<"

read -a VAR1 -p "master-ip: "

read -a VAR2 -p "entity_id to be deleted:"

read -a VAR3 -p "entity_type:"


curl -iX POST 'http://'$VAR1':8082/ngsi10/updateContext' -H 'Content-Type: application/json' -d '{"contextElements": [{"entityId": {"id": "'$VAR2'", "type": "'$VAR3'", "isPattern": false}}], "updateAction": "DELETE"}'
