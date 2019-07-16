#!/usr/bin/python
from kubernetes import client, config
from sense_hat import SenseHat

bright_red = (255,0,0)
bright_green = (0,255,0)
bright_blue = (0,0,255)
system_pod_healthy = (64,0,64)
workload_pod_healthy = (0,0,64)

sense = SenseHat()
sense.clear(0,0,0)
sense.set_rotation(180)
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
        sense.set_pixel(j,0,bright_green)
    elif i.status.conditions[3].status == "Unknown":
        sense.set_pixel(j,0,bright_red)
    else:
        sense.set_pixel(j,0,255,255,0)
    nameCount[i.status.addresses[0].address] = [0,j]
    j = j + 1


#print("Listing pods with their Node Names:")
for i in ret2.items:
#    print("%s\t%s\t%s" % (i.status.host_ip, i.metadata.namespace, i.metadata.name))
    if nameCount.has_key(i.status.host_ip):
      nameCount[i.status.host_ip][0] = nameCount[i.status.host_ip][0] + 1
#      if nameCount[i.status.host_ip][0] > 7:
#        nameCount[i.status.host_ip][0] = 7
      if i.metadata.namespace == "default":
        sense.set_pixel(nameCount[i.status.host_ip][1],nameCount[i.status.host_ip][0],workload_pod_healthy)
#        print("Set blue...(%s,%s)" % (nameCount[i.status.host_ip][1],nameCount[i.status.host_ip][0]))
      elif i.metadata.namespace == "kube-system":
        sense.set_pixel(nameCount[i.status.host_ip][1],nameCount[i.status.host_ip][0],system_pod_healthy)
#        print("Set purple...(%s,%s)" % (nameCount[i.status.host_ip][1],nameCount[i.status.host_ip][0]))
      else:
        sense.set_pixel(nameCount[i.status.host_ip][1],nameCount[i.status.host_ip][0],16,16,16)
#        print("Set grey...(%s,%s)" % (nameCount[i.status.host_ip][1],nameCount[i.status.host_ip][0]))
    else:
      nameCount[i.status.host_ip] = (1,7)

