sudo yum install epel-release -y
sudo yum install ansible -y
sudo yum install python-pip -y
#sudo pip install -U ansible
sudo pip install shade
sudo pip install -U  ansible
sudo pip install python-openstackclient
sudo pip install boto #install boto for aws
sudo pip install boto3
sudo pip install botocore
sudo echo "+++++++++++++++please source your openstack auth/rc file here+++++++++++++"
sudo sed -i '/host_key_checking = False/s/^#//g' /etc/ansible/ansible.cfg
sudo sed -i '/pipelining = False/s/^#//g' /etc/ansible/ansible.cfg
sudo sed -i 's/pipelining = False/pipelining = True/g' /etc/ansible/ansible.cfg
sudo sed -i '/forks=5/s/^#//g' /etc/ansible/ansible.cfg
sudo sed -i 's/forks=5/forks=100/g' /etc/ansible/ansible.cfg
sudo echo "+++++++++++++ we are done with prerequisite ++++++++++++"
sudo echo "++++++++ please edit cloud-config.yaml file for inputs and run this command    'ansible-playbook site.yaml'     ++++++++++ "

