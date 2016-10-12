# How to use?

!!!Use under root user!!!

Note that scripts are importing ../common/common.sh

See also [CloudForms Middleware Quickstart Guide]( https://docs.engineering.redhat.com/display/JP/CloudForms+Middleware+-+Quickstart+Guide)

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


# Bash into container
```bash
docker exec -it $(docker ps | grep cloudforms/cfme-middleware | awk '{print $1}') bash
```

# Tail logs into container
```bash
docker exec -it $(docker ps | grep cloudforms/cfme-middleware | awk '{print $1}') tailf /var/www/miq/vmdb/log/evm.log
```
