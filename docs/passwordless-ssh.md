1. Login to Ansible Host VM and switch to root user using command:
	$ sudo -i
2. Generate a pair of public keys using the following command:
	# ssh-keygen -t rsa
3. Press enter key in "Enter file in which to save the key", "Enter passphrase" and "Enter same passphrase again"
4. Use SSH from Ansible Host to connect node (master or worker) using centos (or ubuntu) as a user and create .ssh directory under it, using the following command:
	# ssh -i <key.pem> centos@<ip> mkdir -p .ssh
5. Use SSH from Ansible Host and upload a new generated public key (id_rsa.pub) on server node (master or worker) under centos‘s .ssh directory as a file name authorized_keys:
	# cat .ssh/id_rsa.pub | ssh -i <key.pem> centos@<ip> 'cat >> .ssh/authorized_keys'
6. Set permissions on .ssh directory and authorized_keys file:
	# ssh -i <key.pem> centos@<ip> "chmod 700 .ssh; chmod 640 .ssh/authorized_keys"
7. ssh centos@<ip>
