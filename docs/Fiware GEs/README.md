User can make use of Helm charts to deploy Fiware at [helm-charts](https://github.com/FIWARE/helm-charts).

## MongoDB
To setup mongoDB required for Fiware GEs like ```orion``` and ```iot-agent``` below commands needs to be followed:
1. Copy [storage.yaml](https://github.com/Fiware-Community/kubernetes-in-FiwareLab/blob/main/docs/Fiware%20GEs/storage.yaml) and [values.yaml](https://github.com/Fiware-Community/kubernetes-in-FiwareLab/blob/main/docs/Fiware%20GEs/values.yaml) to the master node.
2. Add repo using command:

   ```helm repo add bitnami https://charts.bitnami.com/bitnami```
3. Create Persistent Volume from file using command:

   ```kubectl apply -f storage.yaml```
4. Install mongoDB using command:

   ```helm install --values values.yaml mongo bitnami/mongodb```

## Fiware GEs
User can follow any of the following two method to install Fiware GEs 
1. User can add the repository using command:

   ```helm repo add fiware https://fiware.github.io/helm-charts```

   and then install GEs by command:

   ```helm install <RELEASE_NAME> fiware/<CHART_NAME>```

2. User can clone the repository using command:

   ```git clone https://github.com/FIWARE/helm-charts.git```

   and then running the following command inside folder ```charts/<GE-name>```:

   ```helm install <GE-name> .```

For Fogflow setup using Helm user can follow steps provided at: https://github.com/smartfog/fogflow/blob/development/doc/en/source/k8sIntegration.rst
For Scorpio Broker setup user can follow steps at: https://github.com/ScorpioBroker/ScorpioBroker/blob/development/docs/en/source/kubernetesDeployment.rst
