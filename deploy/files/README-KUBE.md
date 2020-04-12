# Steps to configure project with Kubernetes

This file presents how to setup and run project architecture using Kubernetes. This project runs on Windows Host.

## Prerequisite

* [Kubernetes](https://kubernetes.io/docs/tasks/tools/install-kubectl/) - Version 1.17.0 used
* [Minikube](https://medium.com/faun/minikube-installation-on-windows-10-9908d17cfad9) - Version 1.6.2 used
* [Docker](https://docs.docker.com/docker-for-windows/install/) - Version 19.03.05 used (Docker Desktop v2.1.0.5)
* [Helm](https://helm.sh/docs/intro/install/) - Version 3.1.2 used

## Starting application
First, you have to run cmd as admin and navigate to the root of project.
### Starting kubernetes cluster

First command starts the cluster. Without additional parameters (--) cluster did not start correctly. Type *minikube status* to check 
whether everything is alright. Command *minikube stop* stops the cluster and *minikube delete* deletes cluster and VM from computer.

```
minikube start --vm-driver=hyperv --registry-mirror=https://registry.docker-cn.com --image-mirror-country=cn --image-repository=registry.cn-hangzhou.aliyuncs.com/google_containers
```

### Deploying applications
We will position to the root file where DockerFile is located. Deploying files are located under **/deploy/kubernetes/** folder. 
With command kubectl **apply -f (PATH_FILE | DIRECTORY_FILE(For multiple files))**. 

First apply objects for database and cache service. To do so type these 2 commands:

```
kubectl apply -f deploy/kubernetes/postgres/
kubectl apply -f deploy/kubernetes/redis/
``` 

Then, we will create deploying objects for Django application.
Since the docker image is not yet in the registry we will need to build image with docker command. Fot this purpose we will need to access to internal Docker daemon inside kubernetes. Instructin below does this.
On Windows host machine you have to execute 4 additional commands that are listed after **minikube docker-env** to set things up.
```
minikube docker-env
```
Before building docker image ensure you create migrations file.
Keep in mind when building image that .yaml files which depends on this image are set under the name:
**lukajvnv/uxhub_django_minikube**. After creating image you can approach deploying django application with known command.

```
docker build -t lukajvnv/uxhub_django:latest .
kubectl apply -f deploy/kubernetes/django/
```
After this command deployment, migration-job and service object are created in the cluster. You have to provide all unimplemented migrations file **(to do so python manage.py makemigrations uxhub --settings uks.settings_mini_kube)** before the command above. The job object *django-migrations* migrates all migrations to the database.

**Note 1:** If the postgres pod is not in consistent state, new migrations will not be implemented.
**Note 2:** To open django app in browser press **minikube service django**. If you notice homepage then django deployment is configured correctly. To check whether other services that django uses are set add /health_check in the url.

Prometheus is used to collect metrics and logs and Grafana to visualize gathering data. We will use helm package manager to deploy many kubernetes objects. Type this two commands one by another. First argument after install is chart name and second is path to the files.
Having in mind that grafana datasource url to the prometheus database pod contains chart name(here it is **prometheus**).
```
helm install prometheus ./deploy/kubernetes/prometheus/
helm install grafana ./deploy/kubernetes/grafana/
``` 
For advanced metrics we will fetch and install kube-state-metrics.
```
helm install kube-state-metrics ./deploy/kubernetes/kube-state-metrics/
```

At the end, apply prometheus, grafana and kube-state-metrics to the cluster. Now you can access to the running pods and services.
```
kubectl prometheus -f deploy/kubernetes/prometheus/
kubectl grafana -f deploy/kubernetes/grafana/
kubectl kube-state-metrics -f deploy/kubernetes/kube-state-metrics/

# get services and access to them in browser
kubectl get svc
minikube service SERVICE_NAME
``` 

### NOTES
To view prometheus dashboard use command below.
```
kubectl --namespace default port-forward prometheus-server-NODE_ID 9090
```
To view grafana dashboard access to grafana service with **minikube service NAME** since it is typed to be exposed.
```
minikube service grafana
# username: admin, password: strongpassword
# to import dashboards upload .json files freom deploy/files
```
If you want to execute Django commands in running pod and container you can use **kubectl exec**. For instance, to create superuser use:  
```
# gets running pods
kubectl get pod

# exec cmd
kubectl exec DJANGO_POD_ID -it -- python manage.py createsuperuser --settings uks.settings_mini_kube
```
Flag *--settings* is used to override default settings.py configuration file. File use.settings_mini_kube has kubernetes configuration data. 