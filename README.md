<center><img src="https://github.com/kubegems/.github/blob/master/static/image/kubegem-logo.jpg?raw=true" width="30%" height="30%"></center>

Installer Operator powered by [Ansible-Operator(OperatorSDK)](https://sdk.operatorframework.io/docs/overview/), it contains all the manifests needed to deploy kubegems.

## Quick start

```
kubectl apply -f deploy/centrol.yaml
kubectl apply -f deploy/centrol.installer.yaml
```
## Custom plugins

change file `deploy/centrol.installer.yaml` and re-apply the CustomResources.

example:

- Set private docker registry

```
apiVersion: plugins.kubegems.io/v1beta1
kind: Installer
metadata:
  name: kubegems-plugins
spec:
  global:
    # Container repository on kubegems installer running.
    # default vvariable used to "docker.io/kubegems" if not set.
    # available container repositories "docker.io/kubegem" is default, other reigstry incoude <ghcr.io/kubegems> and <registry.cn-beijing.aliyuncs.com/kubegems>.
    # If you are using a private repository, you can configure a policy to replicat image locallly from any of the srouce registry listed above.
    repository: registry.cn-beijing.aliyuncs.com/kubegems
```

- Set global StorageClass or ImagePullSecrets

```
apiVersion: plugins.kubegems.io/v1beta1
kind: Installer
metadata:
  name: kubegems-plugins
  namespace: kubegems-installer
spec:
  global:
    # imagepullsecret: kubegems
  
    # Kubegems uses the built-in local-path-provisioner by defaults.
    # If you need to set a personalised storage class for the component, please configure it in the field "<component>.operator.persisten.storageclass".
    # storageclass: local-path
```

- enable istio

```
apiVersion: plugins.kubegems.io/v1beta1
kind: Installer
metadata:
  name: kubegems-plugins
spec:
  global:
    istio:
      details:
        catalog: 服务网格
        description: KubeGems平台服务治理套件.
        version: v1.11.0
      #enabled: false 
      enabled: true
      namespace: istio-system
      operator:
        eastwestgateway:
          enabled: true
        dnsproxy:
          enabled: true
        istio-cni:
          enabled: true
        tracing:
          enabled: true
          param: 50
          address: "jaeger-collector.observability.svc.cluster.local:9411"
        kiali:
          enabled: true
          prometheus_urls: "http://prometheus.gemcloud-monitoring-system.svc.cluster.local:9090"
          trace_urls: "http://jaeger-query.observability.svc.cluster.local:16685/jaeger"
          grafana_urls: "http://grafana-service.gemcloud-monitoring-system.svc.cluster.local:3000"
      status:
        deployment:
        - istiod
```

## Local Debuging

### Installing the Kubernetes Collection for Ansible 

To install the Kubernetes Collection, one must first install Ansible 2.9+. For example, on Fedora/Centos:

```
sudo dnf install ansible
```

In addition to Ansible, a user must install the OpenShift Restclient Python package:

```
pip3 install openshift
```

Finally, install the Kubernetes Collection from ansible-galaxy:

```
ansible-galaxy collection install kubernetes.core
```

Alternatively, if you’ve already initialized your operator, you may have a requirements.yml file at the top level of your project. This file specifies Ansible dependencies that need to be installed for your operator to function. By default it will install the kubernetes.core collection as well as the operator_sdk.util collection, which provides modules and plugins for operator-specific operations.

To install the dependent modules from this file, run:

```
ansible-galaxy collection install -r requirements.yml
```

### Testing the Kubernetes Collection locally 

```
ansible-playbook test.yaml
```

> tips: Export your environments `RUNNINT_MODE` and `LOCATION`  before you run ansible playbook.

### Custom Ansible-Self environments

The environments of ansbile-playbook runtime at `roles/installer/defaults/main.yaml`, you can modity it after some task changed.

> tips: Do not include this file in .dockerignore.


for more information, see https://sdk.operatorframework.io/docs/building-operators/ansible/development-tips/ 