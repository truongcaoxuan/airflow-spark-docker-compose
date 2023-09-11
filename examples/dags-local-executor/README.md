# Running Airflow in Docker with `Local` Executor

Link ref: <https://github.com/maxcotec/Apache-Airflow/tree/main/airflow-minimal/docker-localExecutor-mysql>

```bash
docker compose up -d
```

![dag-localExecutor-docker-up](../../images/dag-localExecutor-docker-up.png)

![dag-localExecutor-docker-desktop](../../images/dag-localExecutor-docker-desktop.png)

Accessing the web interface
Once the cluster has started up, you can log in to the web interface and begin experimenting with DAGs.

The webserver is available at: <http://localhost:8080>. The default account has the login `admin` and the password `airflow`

DAG Graph

![Alt text](../../images/dag-local-graph.png)

DAG Gantt

![Alt text](../../images/dag-localExecutor-grantt-chart.png)

## Cleaning-up the environment

The best way to do this is to:

- Run command in the directory you downloaded the docker-compose.yaml file

```bash
 docker compose down --volumes --remove-orphans 
```

- Remove the entire directory where you downloaded the docker-compose.yaml file

```bash
rm -rf '<DIRECTORY>'
```

- Run through this guide from the very beginning, starting by re-downloading the docker-compose.yaml file
