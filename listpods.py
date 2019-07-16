#!/usr/bin/python
from kubernetes import client, config
import unicornhathd

#bright_red = (255,0,0)
#bright_green = (0,255,0)
#bright_blue = (0,0,255)
#system_pod_healthy = (64,0,64)
#workload_pod_healthy = (0,0,64)

unicornhathd.clear()
unicornhathd.rotation(270)
config.load_kube_config()
nameCount = {}
v1 = client.CoreV1Api()
#get nodes with status
ret1 = v1.list_node(watch=False)
ret2 = v1.list_pod_for_all_namespaces(watch=False)
j = 0
for i in ret1.items:
#    print("%s\t%s\t%s\t%s" % (i.status.conditions[3].type,i.status.conditions[3].status, i.metadata.name, i.status.addresses[0].address))
    if i.status.conditions[3].status == "True":
        unicornhathd.set_pixel(j,0,0,255,0)
    elif i.status.conditions[3].status == "Unknown":
        unicornhathd.set_pixel(j,0,255,0,0)
    else:
        unicornhathd.set_pixel(j,0,128,128,0)
    nameCount[i.status.addresses[0].address] = [0,j]
    j = j + 1


#print("Listing pods with their Node Names:")
for i in ret2.items:
#    print("%s\t%s\t%s" % (i.status.host_ip, i.metadata.namespace, i.metadata.name))
    if nameCount.has_key(i.status.host_ip):
      nameCount[i.status.host_ip][0] = nameCount[i.status.host_ip][0] + 1
      if nameCount[i.status.host_ip][0] > 15:
        nameCount[i.status.host_ip][0] = 15
      if i.metadata.namespace == "default":
        unicornhathd.set_pixel(nameCount[i.status.host_ip][1],nameCount[i.status.host_ip][0],0,0,128)
#        print("Set blue...(%s,%s)" % (nameCount[i.status.host_ip][1],nameCount[i.status.host_ip][0]))
      elif i.metadata.namespace == "kube-system":
        unicornhathd.set_pixel(nameCount[i.status.host_ip][1],nameCount[i.status.host_ip][0],64,0,64)
#        print("Set purple...(%s,%s)" % (nameCount[i.status.host_ip][1],nameCount[i.status.host_ip][0]))
      else:
        unicornhathd.set_pixel(nameCount[i.status.host_ip][1],nameCount[i.status.host_ip][0],16,16,16)
#        print("Set grey...(%s,%s)" % (nameCount[i.status.host_ip][1],nameCount[i.status.host_ip][0]))
    else:
      nameCount[i.status.host_ip] = (1,15)

unicornhathd.show()
