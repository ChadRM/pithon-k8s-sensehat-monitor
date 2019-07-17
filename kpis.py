#!/usr/bin/python
from kubernetes import client, config
import unicornhathd

unicornhathd.clear()
unicornhathd.rotation(180)
config.load_kube_config()
nameCount = {}
v1 = client.CoreV1Api()

ret1 = v1.list_node(watch=False)
ret2 = v1.list_pod_for_all_namespaces(watch=False)
j = 0
for i in ret1.items:
#    print("%s\t%s\t%s\t%s" % (i.status.conditions[3].type,i.status.conditions[3].status, i.metadata.name, i.status.addresses[0].address))
#    print("%s" % (i.spec.unschedulable))
    if i.status.conditions[3].status == "True":
        unicornhathd.set_pixel(j,0,0,255,0)
    elif i.status.conditions[3].status == "Unknown":
        unicornhathd.set_pixel(j,0,255,0,0)
    else:
        unicornhathd.set_pixel(j,0,128,128,0)
    if i.spec.unschedulable:
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

#banner

#unicornhathd.set_pixel(0,15,128,128,128) #k
#unicornhathd.set_pixel(0,14,128,128,128)
#unicornhathd.set_pixel(0,13,128,128,128)
#unicornhathd.set_pixel(0,12,128,128,128)
#unicornhathd.set_pixel(0,11,128,128,128)
#unicornhathd.set_pixel(1,13,128,128,128)
#unicornhathd.set_pixel(2,15,128,128,128)
#unicornhathd.set_pixel(2,14,128,128,128)
#unicornhathd.set_pixel(2,12,128,128,128)
#unicornhathd.set_pixel(2,11,128,128,128)

#unicornhathd.set_pixel(5,15,128,128,128) #pi
#unicornhathd.set_pixel(5,14,128,128,128)
#unicornhathd.set_pixel(5,13,128,128,128)
#unicornhathd.set_pixel(5,12,128,128,128)
#unicornhathd.set_pixel(5,11,128,128,128)
#unicornhathd.set_pixel(6,15,128,128,128)
#unicornhathd.set_pixel(7,15,128,128,128)
#unicornhathd.set_pixel(7,14,128,128,128)
#unicornhathd.set_pixel(7,13,128,128,128)
#unicornhathd.set_pixel(7,12,128,128,128)
#unicornhathd.set_pixel(7,11,100,100,100)
#unicornhathd.set_pixel(4,15,128,128,128)
#unicornhathd.set_pixel(8,15,128,128,128)

#unicornhathd.set_pixel(10,14,128,128,128) #s
#unicornhathd.set_pixel(10,11,128,128,128)
#unicornhathd.set_pixel(11,15,128,128,128)
#unicornhathd.set_pixel(11,13,128,128,128)
#unicornhathd.set_pixel(11,11,128,128,128)
#unicornhathd.set_pixel(12,15,128,128,128)
#unicornhathd.set_pixel(12,12,128,128,128)

unicornhathd.show()
