1. To check current kernel version on CentOS, open a command-line interface and enter following command:

	```# uname -msr```

2. To update CentOS software repositories, use the command:

	```# sudo yum -y update```

3. To install the new kernel version, a new repository (ELRepo repository) needs to be enabled, type:

	```# sudo rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org```

4. Next, install the ELRepo repository by executing the following command:

	```# sudo rpm -Uvh https://www.elrepo.org/elrepo-release-7.0-3.el7.elrepo.noarch.rpm```

5. Allow the system to finish performing the operation.
6. To list available kernels, enter:

	```# yum list available --disablerepo='*' --enablerepo=elrepo-kernel```

7. To install the latest mainline kernel:

	```# sudo yum --enablerepo=elrepo-kernel install kernel-ml```

8. Reboot your system by running the command:

	```# reboot```

9. In case VM is not accessible after this step then soft reboot from Fiware-Lab GUI.
10. To set Default Kernel Version type the following in the terminal:

	```# sudo vim /etc/default/grub```

11. Once the file opens, look for the line that says ```GRUB_DEFAULT=X```, and change it to ```GRUB_DEFAULT=0```
12. Save the file, and then type the following command in the terminal to recreate the kernel configuration:

	```# sudo grub2-mkconfig -o /boot/grub2/grub.cfg```

13. Reboot once more:

	```# reboot```

14. In case VM is not accessible after this step then soft reboot from Fiware-Lab GUI.
