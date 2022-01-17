# K8s UI

Step 1: Install Git using

    yum install git -y


step 2: Set ssh host key checking to "no"

     Add the following options to ssh configuration file /etc/ssh/ssh_config :

        StrictHostKeyChecking no

     Now reload your ssh service.


Step 3: Git clone the repo using

     git clone <>



step 4: Run prerequisite.sh for installing prerequisite envirment setup.

     cd UI/K8s/
     chmod +x prerequisite.sh
     ./prerequisite.sh

step 5: Follow prerequisite.sh output or do the below things.

      1.Make changes in cloud-config.yaml
      2.Source your openstack creds file to the terminal.
      3.And run "ansible-playbook site.yaml"
