************************************
Hardware & Software Requirement
************************************

**Hardware Requirement:**
1. 2 GB or more of RAM per machine
2. 2 CPUs or more.
3. Full network connectivity between all machines in the cluster i.e., master node and other worker nodes are reachable between each other.

**Software Requirement:**
1. A compatible Linux host. The Kubernetes project provides generic instructions for Linux distributions based on Debian and Red Hat, and those distributions without a package manager.
2. Unique hostname, MAC address, and product_uuid for every node.
3. Open ports
    * For master Node: 6443, 2379-2380, 10250, 10251, 10252
    * For Worker Node: 10250, 30000-32767
4. Swap disabled.
