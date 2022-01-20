# SSH into the Kubernetes master and run the following command
mkdir -p /opt/sth-mongo
chmod 777 /opt/sth-mongo
echo "/opt/sth-mongo *(rw,sync,no_root_squash,no_all_squash)"  >> /etc/exports
mkdir -p /opt/sth-mongo/vol/0
mkdir -p /opt/sth-mongo/vol/1
mkdir -p /opt/sth-mongo/vol/2
mkdir -p /opt/sth-mongo/content
