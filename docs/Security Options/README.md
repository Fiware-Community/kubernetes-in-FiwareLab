User can use various security options provided by Kubernetes, such as:

1. **Set the security context for a Pod:**

   To specify security settings for a Pod, include the securityContext field in the Pod specification. The securityContext field is a PodSecurityContext object. The security settings that you specify for a Pod apply to all Containers in the Pod.

2. **Pod Security Policies:**

    PodSecurityPolicy is deprecated as of Kubernetes v1.21, and will be removed in v1.25. It didn't worked in v1.21.3

3. **Use Network Policies to segment and limit container and pod communication:**

    - **Use a network plugin that supports network policies:**
  
      Calico, cillium, Antrea and flannel are configured.
    
    - **“Isolate” your pods:**
   
      - pods are “isolated” if at least one network policy applies to them; if no policies apply, they are “non-isolated”.
    
      - Since network policies are namespaced resources, you will need to create this policy for each namespace. 
    
    - **Explicitly allow internet access for pods that need it:**
  
      For most applications to work, you will need to allow some pods to receive traffic from outside sources. One convenient way to permit this setup would be to designate labels that are applied to those pods to which you want to allow access from the internet and to create network policies that target those labels i.e., networking/allow-internet-access=true
    
    - **communication within a namespace:**
  
      To allow all pods in the same namespace to talk to each other and explicitly allow communication across namespaces, since that is usually more rare.
	
4. **Limiting resource usage on a cluster:**

    Resource quota limits the number or capacity of resources granted to a namespace. This is most often used to limit the amount of CPU, memory, or persistent disk a namespace can allocate, but can also control how many pods, services, or volumes exist in each namespace.
