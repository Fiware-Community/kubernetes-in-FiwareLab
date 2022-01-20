# SSH into the Kubernetes master and run the following command
mkdir -p /opt/data
chmod 777 /opt/data
echo "/opt/data *(rw,sync,no_root_squash,no_all_squash)"  >> /etc/exports
mkdir -p /opt/data/vol/0
mkdir -p /opt/data/vol/1
mkdir -p /opt/data/vol/2
mkdir -p /opt/data/vol/3
mkdir -p /opt/data/vol/4
mkdir -p /opt/data/content
