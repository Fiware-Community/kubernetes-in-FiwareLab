# Openstack Heat:
Heat provides an AWS CloudFormation implementation for OpenStack that orchestrates an AWS CloudFormation template describing a cloud application by executing appropriate OpenStack API calls to generate running cloud applications.
The software integrates other core components of OpenStack into a one-file template system. The templates allow creation of most OpenStack resource types (such as instances, floating IPs, volumes, security groups and users), as well as some more advanced functionality such as instance high availability, instance autoscaling, and nested stacks. By providing very tight integration with other OpenStack core projects.
# Openstack Heat Architecture:

 
## heat
The heat tool is a CLI which communicates with the heat-api to execute AWS CloudFormation APIs. End developers could also use the heat REST API directly.


## heat-api
The heat-api component provides an OpenStack-native REST API that processes API requests by sending them to the heat-engine over RPC.

## heat-api-cfn
The heat-api-cfn component provides an AWS Query API that is compatible with AWS CloudFormation and processes API requests by sending them to the heat-engine over RPC.

## heat-engine
The heat-engine’s main responsibility is to orchestrate the launching of templates and provide events back to the API consumer.

# Template structure
HOT templates are defined in YAML and follow the structure outlined below.

###### heat_template_version: 2016-10-14
description:
   a description of the template
###### parameter_groups:
   a declaration of input parameter groups and order
###### parameters:
  declaration of input parameters
###### resources:
   declaration of template resources
###### outputs:
   declaration of output parameters
###### conditions:
declaration of conditions
  
##  heat_template_version
This key with value 2013-05-23 (or a later date) indicates that the YAML document is a HOT template of the specified version.
description
This optional key allows for giving a description of the template, or the workload that can be deployed using the template.
## parameter_groups
This section allows for specifying how the input parameters should be grouped and the order to provide the parameters in. This section is optional and can be omitted when necessary.
## parameters
This section allows for specifying input parameters that have to be provided when instantiating the template. The section is optional and can be omitted when no input is required.
## resources
This section contains the declaration of the single resources of the template. This section with at least one resource should be defined in any HOT template, or the template would not really do anything when being instantiated.
## outputs
This section allows for specifying output parameters available to users once the template has been instantiated. This section is optional and can be omitted when no output values are required.
## conditions
This optional section includes statements which can be used to restrict when a resource is created or when a property is defined. They can be associated with resources and resource properties in the resources section, also can be associated with outputs in the outputs sections of a template.

#  what is stack?
 a stack is the collection of objects—or resources—that will be created by Heat. This might include instances (VMs), networks, subnets, routers, ports, router interfaces, security groups, security group rules, auto-scaling rules, etc.
stack can be created in two ways. One is from CLI, another one is from GUI(Dashboard)

## creating stack from CLI:
To create a stack, or template, from an example template file, run the following command:

 eg: $ openstack stack create --template server_console.yaml \
  --parameter "image=cirros" MYSTACK
The --parameter values that you specify depend on the parameters that are defined in the template. If a website hosts the template file, you can also specify the URL with the --template parameter.

The command returns the following output:

eg:
+---------------------+----------------------------------------------------------------+
| Field               | Value                                                          |
+---------------------+----------------------------------------------------------------+
| id                  | 70b9feca-8f99-418e-b2f1-cc38d61b3ffb                           |
| stack_name          | MYSTACK                                                        |
| description         | The heat template is used to demo the 'console_urls' attribute |
|                     | of OS::Nova::Server.                                           |
|                     |                                                                |
| creation_time       | 2016-06-08T09:54:15                                            |
| updated_time        | None                                                           |
| stack_status        | CREATE_IN_PROGRESS                                             |
| stack_status_reason |                                                                |
+---------------------+----------------------------------------------------------------+
You can also use the --dry-run option with the openstack stack create command to validate a template file without creating a stack from it.
## creating stack from GUI(Dashboard):
1.Log in to the dashboard.
2.Select the appropriate project from the drop down menu at the top left.
3.On the Project tab, open the Orchestration tab and click Stacks category.
4.Click Launch Stack.

5.In the Select Template dialog box, specify the following values:

Template Source: Choose the source of the template from the list.
Template URL/File/Data: Depending on the source that you select, enter the URL, browse to the file location, or directly include the template.
Environment Source:	Choose the source of the environment from the list. The environment files contain additional settings for the stack.
Environment File/Data: Depending on the source that you select, browse to the file location, directly include the environment
6.Click Next.

7.In the Launch Stack dialog box, specify the following values:

Stack Name: Enter a name to identify the stack.
Creation Timeout (minutes): Specify the number of minutes that can elapse before the launch of the stack times out.
Rollback On Failure: Select this check box if you want the service to roll back changes if the stack fails to launch.
Password for user “demo”:  Specify the password that the default user uses when the stack is created.
DBUsername: Specify the name of the database user.
LinuxDistribution: Specify the Linux distribution that is used in the stack.
DBRootPassword: Specify the root password for the database.
KeyName:	Specify the name of the key pair to use to log in to the stack.
DBName: Specify the name of the database.
DBPassword: Specify the password of the database.
InstanceType: Specify the flavor for the instance.
8.Click Launch to create a stack. The Stacks tab shows the stack.


#  Creating Server from heat template:
Use the OS::Nova::Server resource to create a Compute instance. The flavor property is the only mandatory one, but you need to define a boot source using one of the image or block_device_mapping properties.

You also need to define the networks property to indicate to which networks your instance must connect if multiple networks are available in your tenant.

The following example creates a simple instance, booted from an image, and connecting to the private network:

**[The server creation template:](docs/Heat-Template/server.yml)**

#  Quota management template :
An administrator would like to have the ability to specify a project's nova quota and a project user's nova quota in a HOT template. This blueprint proposes to create a new heat resource type for nova quotas.
 
**[The quota management template](quota.yml)**

                                                                                     
#  Create and associate a floating IP to an instance:
You can use two sets of resources to create and associate floating IPs to instances.
OS::Nova resources:
Use the OS::Nova::FloatingIP resource to create a floating IP, and the OS::Nova::FloatingIPAssociation resource to associate the floating IP to an instance.

**[The floating IP template](docs/Heat-Template/floatingIP.yml)**
                                                                     


