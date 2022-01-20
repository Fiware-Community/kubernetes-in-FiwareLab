cd orion
./orion_cleanup.sh

sleep 5

cd ../cepheus
./cepheus_cleanup.sh
sleep 5

cd ../sth-comet
./sth-comet_cleanup.sh

sleep 5

cd ../cygnus-sth
./cyhnus_sth_cleanup.sh

cd ../cygnus-ckan
./cyhnus_ckan_cleanup.sh

cd ../ckan
./ckan_cleanup.sh
