User can Select different networking options whichever best fit their requirement.

Here we have provided configuration for flannel by default. However user can use Callico, Antrea and Cilium by using the playbooks which has been tested in our environment. 
User just needs to replace configure_master_node.yml with the file provided in this directory.

For flannel and Cillium ```cidr_v``` in env_variables will be ```10.244.0.0/16```.
For Callico and Antrea ```cidr_v``` in env_variables will be ```192.168.0.0/16```.
