echo ">> Update request for Temperature of a floor <<"

read -a VAR1 -p "master-ip: "

read -a VAR2 -p "entity_id for type Temperature (must be of format "Stream.Temperaturexxxxx"):"

read -a VAR3 -p "Current Temperature (Integer value): "

read -a VAR4 -p "Device_id: "

read -a VAR5 -p "Floor_id: "

read -a VAR6 -p "latitude (-90 to 90): "

read -a VAR7 -p "longitude (-180 to 180): "


curl -iX POST 'http://'$VAR1':8082/ngsi10/updateContext' -H 'Content-Type: application/json' -d '{"contextElements": [{"entityId": {"id": "'$VAR2'", "type": "Temperature", "isPattern": false}, "attributes": [{"name": "currentTemperature", "type": "float", "contextValue": '$VAR3'}, {"name": "deviceId", "type": "string", "contextValue": "'$VAR4'"}], "domainMetadata": [{"name": "floor", "type": "string", "value": "'$VAR5'"}, {"name": "location", "type": "point", "value": {"latitude": '$VAR6', "longitude": '$VAR7'}}]}], "updateAction": "UPDATE"}'
