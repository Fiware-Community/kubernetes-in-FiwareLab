# kubernetes-in-FiwareLab
This repository has set of ansible playbooks created to setup a kubernetes cluster fully automated with one master and multiple worker nodes. This will work on Fiware-Lab VMs. This has been tested and verified on Centos 7.9 64 bit operating systems with Kernel 5.12.10-1.el7.elrepo.x86_64 and Ubuntu 16.04 64 bit operating systems with Kernel Linux 4.4.0-210-generic. 

# Prerequisites
1.	At least three VMs are required for K8s deployment.
2.	Servers required:

    a. Ansible Host
    
    b. Master Node
    
    c. Worker Nodes
    
3.	Ansible should be installed on Ansible Host. For installation steps, follow [install-ansible.md](https://github.com/Fiware-Community/kubernetes-in-FiwareLab/blob/main/docs/install-ansible.md).

# How to use this (Setup Instructions)
1.	Make servers ready (Ansible Host, one master node and multiple worker nodes) by creating new VMs on Fiware-Lab.
2.	Update the Kernel if it is lower than 5.x (for CentOS). Steps are added in [update-kernel.md](https://github.com/Fiware-Community/kubernetes-in-FiwareLab/blob/main/docs/update-kernel.md).
3.	Install firewall (if not installed). Steps are added in [setup-firewalld.md](https://github.com/Fiware-Community/kubernetes-in-FiwareLab/blob/main/docs/setup-firewalld.md).
4.	Make an entry of each hosts in /etc/hosts file for name resolution in Master and Worker VM as:

    On Master: 127.0.0.1   <master-vm-name>.novalocal
    
    On Worker: 127.0.0.1   <worker-vm-name>.novalocal
    
5.	Make sure kubernetes master node and other worker nodes are reachable between each other.
6.	Internet connection must be enabled in all nodes, required packages will be downloaded from kubernetes official yum repository. 
7.	Copy the script and ansible playbooks on Ansible Host VM.
8.	There is a file ```hosts``` in this folder, make entries of all kubernetes nodes.
9.	Provide server details in ```playbooks/env_variables```.
10.	Deploy the ssh key from Ansible Host to nodes for password less authentication. Steps are added in [passwordless-ssh.md](https://github.com/Fiware-Community/kubernetes-in-FiwareLab/blob/main/docs/passwordless-ssh.md).
11.	Provide root level privilege to centos or ubuntu user. Steps are added in [root-access.md](https://github.com/Fiware-Community/kubernetes-in-FiwareLab/blob/main/docs/root-access.md).
12.	Run ```settingup_kubernetes_cluster.yml``` playbook to setup all nodes and kubernetes master configuration.
    
    ```ansible-playbook settingup_kubernetes_cluster.yml```

13.	Run ```join_kubernetes_workers_nodes.yml``` playbook to join the worker nodes with kubernetes master node once ```settingup_kubernetes_cluster.yml``` playbook tasks are completed.
    
    ```ansible-playbook join_kubernetes_workers_nodes.yml```

14.	Verify the configuration from master node:
    
    ```
    kubectl get nodes
    kubectl get pods --all-namespaces
    ```
    
# Troubleshooting
In case settingup_kubernetes_cluster playbook fails due to some system errors. Then reset the cluster otherwise it will show different errors like **PORT IN USE** and **CERTIFICATES ALREADY EXIST**
To fix these errors run below commands on master node:
    
    kubeadm reset
    iptables -F && iptables -t nat -F && iptables -t mangle -F && iptables -X
 
# Files in this repository
1.	**ansible.cfg** - Ansible configuration file created locally.
2.	**hosts** - Ansible Inventory File
3.	**env_variables** - Main environment variable file where we have to specify based on our environment.
4.	**settingup_kubernetes_cluster.yml** - Ansible Playbook to perform prerequisites ready, setting up nodes, configure master node.
5.	**configure_worker_nodes.yml** - Ansible Playbook to join worker nodes with master node.
6.	**clear_k8s_setup.yml** - Ansible Playbook helps to delete entire configurations from all nodes.
7.	**playbooks** – It’s a directory holds all playbooks.

# Deploy Fiware GEs using HELM
1.	To make use of the charts, you may add the repository:
    
    helm repo add fiware https://fiware.github.io/helm-charts
2.	After the repo is added all charts can be installed via:
    
    ```helm install <RELEASE_NAME> fiware/<CHART_NAME>```

# Limitations
1.	Ansible script would deploy bare minimum K8s. User can configure K8s like persistent storage etc.
2. At least three VMs are required for K8s deployment. 
