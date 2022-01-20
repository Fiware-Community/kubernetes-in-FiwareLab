kubectl create  -f ./kube_svc_cygnus_ckan.yaml
kubectl create -f ./kube_cygnus_ckan_deployment.yaml
echo "+++++++++++++++++ waiting for cygnus-ckan to come up ++++++++++++++++++++++++"
sleep 25
echo "+++++++++++++++++++  cygnus-ckan deployed ++++++++++++++++++++++++++++++++"
