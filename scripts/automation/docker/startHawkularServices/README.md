# How to use?

!!!Use under root user!!!

See also [CloudForms Middleware Quickstart Guide]( https://docs.engineering.redhat.com/display/JP/CloudForms+Middleware+-+Quickstart+Guide)

Note that scripts are importing ../common/common.sh


## To start containers...


```bash
start.sh [path/to/source/setDefaultEnv.sh]
```

- Start Cassandra+HS without EAP7 running:
```bash
start.sh
```
or
```bash
start.sh setDefaultEnv.sh
```

- Start Cassandra+HS with EAP7 running in standalone mode:
```bash
start.sh setDefaultStandaloneEnv.sh
```

- Start Cassandra+HS with EAP7 running in domain mode:
```bash
start.sh setDefaultDomainEnv.sh
```

- or set use env variable with path to source file
```bash
export CF_UI_HS_ENV_SOURCE=path/to/source/setDefaultEnv.sh
```

## Note that scripts are importing ../common/common.sh

# Bash into container
```bash
docker exec -it $(docker ps | grep eap7domain | awk '{print $1}') bash
docker exec -it $(docker ps | grep eap7standalone | awk '{print $1}') bash
docker exec -it $(docker ps | grep hawkular-services | awk '{print $1}') bash
docker exec -it $(docker ps | grep cassandra | awk '{print $1}') bash
```


# Tail logs into container
```bash
docker exec -it $(docker ps | grep eap7domain | awk '{print $1}') tailf /opt/eap/domain/log/host-controller.log
docker exec -it $(docker ps | grep eap7standalone | awk '{print $1}') tailf /opt/eap/standalone/log/server.log
docker exec -it $(docker ps | grep hawkular-services | awk '{print $1}') tailf /opt/data/log/server.log
docker exec -it $(docker ps | grep cassandra | awk '{print $1}') tailf /opt/apache-cassandra/logs/system.log
```

## U can also keep docker ps running
```bash
while true ; do clear; docker ps; sleep 1; done
```

## Known issues

- Getting

```
docker: Error response from daemon: Conflict.
The name "/hawkular-cassandra" is already in use by container <containerId>.
You have to remove (or rename) that container to be able to reuse that name..
```

Remove old container by its id with ```docker rmi -f <containerId>```


- When at http://<host>:9080/ link "Administration Console" redirects to http://<host>:9990/console shows "404 - Not Found" , it is probably because docker redirects EAP7 mgmt port 9990 to 10990
