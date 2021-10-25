We can create persistent Storage i.e., Persistent Volume (PV) and Persistent Volume Claim (PVC) in the kubernetes cluster created.

Example for the PV, PVC and Pod is provided with the following options:

## PersistentVolume:
**Capacity:** PV will have a specific storage capacity.

**Volume Mode:** Filesystem and Block

**Access Modes:** ReadWriteOnce(RWO), ReadOnlyMany(ROX), ReadWriteMany(RWX), ReadWriteOncePod(RWOP)

**Class:** storageClassName: A PV of a particular class can only be bound to PVCs requesting that class. 

**Reclaim Policy:** Retain, Recycle, Delete

**Mount Options:** Not all Persistent Volume types support mount options.

**Node Affinity:** A PV can specify node affinity to define constraints that limit what nodes this volume can be accessed from.

**Phase:** Available, Bound, Released, Failed

 
## PersistentVolumeClaim:
**Access Modes:** Claims use the same conventions as volumes when requesting storage with specific access modes.

**Volume Modes:** Claims use the same convention as volumes to indicate the consumption of the volume as either a filesystem or block device.

**Resources:** Claims, like Pods, can request specific quantities of a resource.

**Selector:** Claims can specify a label selector to further filter the set of volumes. Only the volumes whose labels match the selector can be bound to the claim. The selector can consist of two fields: matchLabels, matchExpressions

**Class:** A claim can request a particular class by specifying the name of a StorageClass using the attribute storageClassName. Only PVs of the requested class, ones with the same storageClassName as the PVC, can be bound to the PVC.
