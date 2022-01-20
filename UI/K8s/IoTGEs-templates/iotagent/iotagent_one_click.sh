echo "++++++++++iotagent cleanup done+++++++++++"
kubectl create -f ./kube_svc_iotagent-json.yaml
sleep 5
kubectl create -f ./kube_iotagent-json_deployment.yaml
sleep 30
echo "++++++++++iotagent oneclick soln completed+++++++++++"
