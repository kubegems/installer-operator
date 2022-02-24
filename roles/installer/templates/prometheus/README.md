# 简介

[Prometheus Operator API 文档](https://github.com/prometheus-operator/prometheus-operator/blob/master/Documentation/api.md)

- operator 版本: 0.46.0
- prometheus 版本：2.25.0
- node-exporter 版本: 1.1.1
- kube-state-metrics 版本: 1.9.8
- ssl-exporter 版本：0.6.0

> 无 alertmanager 组件

**服务发现包含如下服务**

- kubernetes apiserver
- kubernetes proxy
- kubernetes state metrics
- kubelet
- coredns
- cadvisor
- node-exporter
- prometheus-opertor
- prometheus
- ssl

## 部署说明

按照如下流程部署 prometheus-operator

1.kubectl 提交所有 crd 目录下的文件

2.kubectl 提交 psp 文件

3.kubectl 提交 rbac 文件

4.kubectl 提交 service 文件

5.kubectl 提交 node-exporter 文件

6.kubectl 提交 kube-state-metrics 文件

7.kubectl 提交 operator 文件

8.kubectl 提交 prometheus 文件

8.kubectl 提交 servicemonitor 文件

## 额外说明

1. 通过 opertor 创建的 prometheus 实例如果需要外挂 pvc，需要在 prometheus 里面添加如下内容

   ```yaml
   apiVersion: monitoring.coreos.com/v1
   kind: Prometheus
   metadata:
     name: kube-promethe-prometheus
   spec:
     storage:
       volumeClaimTemplate:
         spec:
           storageClassName: storageClass Name
           resources:
             requests:
               storage: 40Gi
   ```

2. 更新 prometheus-additional.yaml 后的操作

执行下列命令更新对应的 secret

```yaml
kubectl create secret generic additional-scrape-configs -n gemcloud-monitoring-system --from-file=prometheus-additional.yaml --dry-run -oyaml > additional-scrape-configs.yaml
```

在创建 prometheus 的 crd 文件中添加下列部分

```yaml
spec:
  additionalScrapeConfigs:
    name: additional-scrape-configs
    key: prometheus-additional.yaml
```
