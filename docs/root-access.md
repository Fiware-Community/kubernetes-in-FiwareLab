1. Edit visudo file to grant user(centos/ubuntu) all permission by executing below command:
	# visudo 
2. Add below lines after "root ALL=(ALL) ALL":
	centos ALL=(ALL) ALL
3. Save and exit file by below command:
	:wq
4. Add user to wheel group:
	# usermod -aG wheel centos