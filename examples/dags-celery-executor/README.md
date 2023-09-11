# Running Airflow in Docker with `Celery` Executor

Link ref: <https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html>

```bash
docker compose --profile flower up -d
```

![dag-celeryExecutor-docker-up](../../images/dag-celeryExecutor-docker-up.png)

![dag-celeryExecutor-docker-desktop](../../images/dag-celeryExecutor-docker-desktop.png)

Accessing the web interface
Once the cluster has started up, you can log in to the web interface and begin experimenting with DAGs.

The webserver is available at: <http://localhost:8080>. The default account has the login `airflow` and the password `airflow`

DAG Graph

![DAG Graph](../../images/dag-celery-graph.png)

DAG Gantt
![DAG Gantt](../../images/dag-celeryExecutor-grantt-chart.png)

Flower is available at: <http://localhost:5555>

![dag-celeryExecutor-flower-info](../../images/dag-celeryExecutor-flower-info.png)

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
