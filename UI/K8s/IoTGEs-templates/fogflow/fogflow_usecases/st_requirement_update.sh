echo ">> Update request for Requirement for topology TemperatureCheck <<"

read -a VAR1 -p "master-ip: "

read -a VAR2 -p "entity_id for type Requirement:"

read -a VAR3 -p "Center Latitude (-90 to 90): "

read -a VAR4 -p "Center Longitude (-180 to 180): "

read -a VAR5 -p "Radius (in meters): "

curl -iX POST 'http://'$VAR1':8082/ngsi10/updateContext' -H 'Content-Type: application/json' -d '{"contextElements": [{"entityId": {"id": "'$VAR2'", "type": "Requirement", "isPattern": false}, "attributes": [{"name": "output", "type": "string", "contextValue": "TemperatureAlarm"},{"name": "scheduler", "type": "string", "contextValue": "default"}, {"name": "restriction", "type": "object", "contextValue": {"scopes": [{"scopeType": "circle", "scopeValue": {"centerLatitude": '$VAR3', "centerLongitude": '$VAR4', "radius": '$VAR5'}}]}}], "domainMetadata": [{"name": "topology", "type": "string", "value":"Topology.TemperatureCheck"}]}], "updateAction": "UPDATE"}'
