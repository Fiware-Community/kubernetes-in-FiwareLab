************************************
Setup guide
************************************

**Steps to Setup UI dashboard in Ubuntu 16_04:**

1. Update:

.. code-block:: console

    sudo apt update
    sudo apt upgrade

2. Install git: 

.. code-block:: console
    
    sudo apt-get install git

3. Install mysql: 

.. code-block:: console

    sudo apt-get install mysql-server

4. Clone git repository: 

.. code-block:: console
    
    git clone https://github.com/Fiware-Community/kubernetes-in-FiwareLab

5. Move to the directory: 

.. code-block:: console

    cd kubernetes-in-FiwareLab/UI/K8s/K8s_ui/microblog2/

6. Install pip: 

.. code-block:: console

    sudo apt install python-pip

7. Install requirements: 

.. code-block:: console

    pip install -r requirements.txt

8. Update pass mysql password: (change the password to Abc@1234)

.. code-block:: console

    mysql_secure_installation

9. Check if database “db” exists. Otherwise create a new database: 

.. code-block:: console

    sudo mysql -u root –p
    mysql > SHOW DATABASES;
    mysql> CREATE DATABASE db;
    mysql> exit;

10. Update flash database:

.. code-block:: console   

    flask db upgrade

11. Run application: 

.. code-block:: console

    flask run --host=0.0.0.0

12. Open browser to check dashboard: 

.. code-block:: console

    www.<public_ip_address>:5000

