echo ">> Update request for pollutant concentration of City <<"

read -a VAR1 -p "master-ip: "

read -a VAR2 -p "entity_id for type City:"

read -a VAR3 -p "PM10 Concentration (Integer value): "

read -a VAR4 -p "PM25 Concentration (Integer value): "

read -a VAR5 -p "latitude (-90 to 90): "

read -a VAR6 -p "longitude (-180 to 180): "


curl -iX POST 'http://'$VAR1':8082/ngsi10/updateContext' -H 'Content-Type: application/json' -d '{"contextElements": [{"entityId": {"id": "'$VAR2'", "type": "City", "isPattern": false}, "attributes": [{"name": "PM10", "type": "integer", "contextValue": '$VAR3'},{"name": "PM25", "type": "integer", "contextValue": '$VAR4'}], "domainMetadata": [{"name": "location", "type": "point", "value": {"latitude": '$VAR5', "longitude": '$VAR6'}}]}],"updateAction": "UPDATE"}'
