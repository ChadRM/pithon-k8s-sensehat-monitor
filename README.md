# pithon-k8s-sensehat-monitor
Pi Python Monitor using pixels on the sensehat

Kubectl must be configured on the pi in question.
Currently supports up to 8 nodes (because there are only 8 columns on the sensehat)
If the number of pods on a node >7, the excess is ignored.

pods in the kube-system namespace are purple
workload pods in the default namespace are green.

Node status is green (ready) or red (not ready)

TODO:
  Yellow node status for unschedulable nodes
  different intensity colors for pod lifecycle statuses
