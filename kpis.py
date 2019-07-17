#!/usr/bin/python
from kubernetes import client, config
import unicornhathd

unicornhathd.clear()
unicornhathd.rotation(180)
config.load_kube_config()
nameCount = {}
v1 = client.CoreV1Api()
#print("begin")
try:
#  print("begin try")
  while True:
#    print("begin while true")
    ret1 = v1.list_node(watch=False)
    ret2 = v1.list_pod_for_all_namespaces(watch=False)
    j = 0
    for i in ret1.items:
#      print("begin parse nodes - %s" % i.metadata.name)
#      print("  - Status - %s" % i.status.conditions[3].status)
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
    for i in ret2.items:
      if nameCount.has_key(i.status.host_ip):
        nameCount[i.status.host_ip][0] = nameCount[i.status.host_ip][0] + 1
        if nameCount[i.status.host_ip][0] > 15:
          nameCount[i.status.host_ip][0] = 15
        if i.metadata.namespace == "default":
          unicornhathd.set_pixel(nameCount[i.status.host_ip][1],nameCount[i.status.host_ip][0],0,0,128)
        elif i.metadata.namespace == "kube-system":
          unicornhathd.set_pixel(nameCount[i.status.host_ip][1],nameCount[i.status.host_ip][0],32,0,32)
        else:
          unicornhathd.set_pixel(nameCount[i.status.host_ip][1],nameCount[i.status.host_ip][0],16,16,16)
      else:
#        print("Not in nameCount: %s" % i.status.host_ip)
#        print("Name of pod: %s" % i.metadata.name)
        nameCount[i.status.host_ip] = [1,15]
    unicornhathd.show()
except KeyboardInterrupt:
  unicornhathd.off()
