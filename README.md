# pithon-k8s-sensehat-monitor
Pi Python Monitor using pixels on the unicornhathd

Kubectl must be configured on the pi in question.
Currently supports up to 16 nodes (because there are only 16 columns on the unicornhat)
If the number of pods on a node >15, the excess is ignored.

pods in the kube-system namespace are purple
workload pods in the default namespace are green.

Node status is green (ready) or red (not ready)

TODO:
  Yellow node status for unschedulable nodes
  different intensity colors for pod lifecycle statuses
