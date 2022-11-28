# kubernetes-in-FiwareLab
This repository has set of ansible playbooks created to setup a kubernetes cluster fully automated with one master and multiple worker nodes. This will work on Fiware-Lab VMs. This has been tested and verified on Centos 7.9 64 bit operating systems with Kernel 5.12.10-1.el7.elrepo.x86_64 and Ubuntu 16.04 64 bit operating systems with Kernel Linux 4.4.0-210-generic.

[quick_start_guide](https://github.com/Fiware-Community/kubernetes-in-FiwareLab/blob/main/docs/quick_start_guide.md) provide the steps which needs to be followed sor the setup using this repository.
 
# Files in this repository under centos and ubuntu folders
1.	**ansible.cfg** - Ansible configuration file created locally.
2.	**hosts** - Ansible Inventory File
3.	**env_variables** - Main environment variable file where we have to specify based on our environment.
4.	**settingup_kubernetes_cluster.yml** - Ansible Playbook to perform prerequisites ready, setting up nodes, configure master node.
5.	**configure_worker_nodes.yml** - Ansible Playbook to join worker nodes with master node.
6.	**clear_k8s_setup.yml** - Ansible Playbook helps to delete entire configurations from all nodes.
7.	**playbooks** – It’s a directory holds all playbooks.

# Limitations
1. Ansible script would deploy bare minimum K8s. User can configure K8s like persistent storage etc.
2. At least two FIWARE Lab VMs are required for K8s deployment. 
