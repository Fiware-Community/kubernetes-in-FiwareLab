************************************
UI support to create and manage Kubernetes cluster for FIWARE Lab user
************************************

Fiware Lab user will be able to create and manage kubernetes cluster through UI. User can also deploy Fiware GEs over kubernetes cluster by selecting the GEs from the catalogue provided in GUI.

User can redirect himself to kubernetes GUI from FIWARE Lab dashboard afte clicking on kubernetes button.

After successful login to FIWARE Lab a button will appear in overview section of Project from where the user will be redirected to kubernetes GUI where user will get options to create and manage kubernetes cluster and deploy Fiware GEs.

Pages in the FIWARE Lab GUI:
---------------------------------------------
**Login Page:** User have to login with their credentials to access FIWARE Lab dashboard.

.. figure:: source/figures/login-page.png
   :align: center
   :width: 100px
   :height: 100px
   :scale: 50 %

**Instances:** User have to create two instances in instances tab of FIWARE Lab dashboard with minimum configuration flavor medium(2VCPUS).

.. figure:: source/figures/instances-page.png
   :align: center
   :width: 100px
   :height: 100px
   :scale: 50 %

**Overview Page:** User have to click on kubernetes button to redirect to Kubernetes support UI for cluser deployment.

.. figure:: source/figures/overview-page.png
   :align: center
   :width: 100px
   :height: 100px
   :scale: 50 %

Pages in the Kubernetes support UI:
---------------------------------------------

**Dashboard:** After clicking on button, the default screen will be Dashboard which will list all the clusters created from the user account. User can click on the ID to check and modify the cluster details.

.. figure:: source/figures/dashboard.png
   :align: center
   :width: 100px
   :height: 100px
   :scale: 50 %   

**Create Cluster:** User will get option to create his own cluster in "Create Cluster" tab. User needs to fill the details which will be used for creating cluster.

.. figure:: source/figures/create-cluster.png
   :align: center
   :width: 100px
   :height: 100px
   :scale: 50 %

**Components details:** User will get option to View and edit components. For this first user needs to select the Cluster name from the Cluster List and after that user can view/edit its components.

.. figure:: source/figures/component.png
   :align: center
   :width: 100px
   :height: 100px
   :scale: 50 %

**Add Node:** User can add node details in "Add Node" option after clicking on the ID shown in the Dashboard. User need to provide details such as VM username (centos/ubuntu), VM IP (internal IP), pem file to access the VM and after submitting the information, VM details will be added to the cluster.

.. figure:: source/figures/id-add-node.png
   :align: center
   :width: 100px
   :height: 100px
   :scale: 50 %

.. figure:: source/figures/add-node.png
   :align: center
   :width: 100px
   :height: 100px
   :scale: 50 %

**Add Components:** User can add Fiware GEs to the cluster by using "Add Components" option after clicking on the ID  shown in the Dashboard. User can select the components which he needs in the cluster by selecting the Enable option. User can also select the version of the Fiware GEs and its database version from the dropdown. After submitting the details, Fiware GEs will be added to the cluster.

.. figure:: source/figures/id-add-component.png
   :align: center
   :width: 100px
   :height: 100px
   :scale: 50 %

.. figure:: source/figures/add-component.png
   :align: center
   :width: 100px
   :height: 100px
   :scale: 50 %

**Deployment logs:** User will get the option to check the deployment logs based on the cluster and deployment under "Deployment Logs" tab. For this, user need to select Cluster name from the "Cluster List" and deployment from "Deployment List" and then the logs will appear on the screen.

.. figure:: source/figures/cluster-deployment-log.png
   :align: center
   :width: 100px
   :height: 100px
   :scale: 50 %

**Delete Cluster:** User will get the option to delete the cluster in GUI. After clicking on icon it will ask to confirm if you want to delete the cluster.

.. figure:: source/figures/delete-cluster.png
   :align: center
   :width: 100px
   :height: 100px
   :scale: 50 %

**Advantages:**

1. Easier to create and manage kubernetes cluster through GUI.

2. User will be provided with option to deploy Fiware GEs through GUI.

3. User can select Fiware GEs from the catalogue and those GEs will be deployed.
