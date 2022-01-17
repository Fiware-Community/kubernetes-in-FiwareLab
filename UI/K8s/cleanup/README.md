# sandbox

Step 1: To clean the GEs from exiting VM, provide the input parameters in cleanup-config.yaml file.


Step 2: To clean the required VMs whose master_ip is given in cleanup-config.yaml, run the following command in this directory:

ansible-playbook site.yaml
