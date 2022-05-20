************************************
Fiware VM's K8s user Support through command line (Phase-1)
************************************

The process of deploying Kubernetes and creating K8s cluster for Fiware GEs will be automated by using automated script files and Helm charts. Fiware Lab users can deploy Kubernetes and create K8s cluster with the script files with minimal configuration changes. It would save the effort to deploy the K8s cluster over provided VM’s to the users.

* User needs to create 3 new VM
* User needs to setup ansible on 1 VM (Ansible server)
* User will get Ansible Playbooks (for centos and ubuntu) to install Kubernetes on master and worker nodes.
* User can deploy Fiware GEs using helm charts and create cluster.
* User can manage GEs using Kubernetes API

**Limitation of K8s Support through command**

1. Helm charts is available for only limited Fiware GEs for creating cluster. However, user can create the files to run his application.
2. User needs to have at least 3 VMs i.e., 1 Ansible Server, 1 master node and 1 worker node.
3. User must be aware of networking between VMs.
4. User need to have knowledge about Ansible script to create setup K8s and create cluster.

