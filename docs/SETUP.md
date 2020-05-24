# Local Development

1. Clone this repo.

```
$ git clone https://github.com/[GH_USER]/[GH_REPO].git
$ cd [GH_REPO]
```

2. Install Docker (skip if already installed)

3. Setup Airflow variables

**config/airflow-vars.json** contains airflow variables that you would need in
order to  upload the output csv files to Google Sheet, AWS S3 and/or Snowflake.
These are optional. Recommended if you have your own storage. Make sure to look at
`dags/notebook_dags.py` on how to use it. 
```
$ cp config/airflow-vars-sample.json config/airflow-vars.json
[edit airflow-vars.json]
```

4. Start Airflow container (SequentialExecitor)
```
$ scripts/airflow.sh start
```

5. View Airflow container logs (optional)
```
$ scripts/airflow.sh logs
```

6. List Airflow DAGs (testing) 
```
$ scripts/airflow.sh list_dags

-------------------------------------------------------------------
DAGS
-------------------------------------------------------------------
...
github_poll_trigger
...

```
5. Test a DAG task
```
$ scripts/airflow.sh test github_poll_trigger check_commits_hello_world 2020-03-28
```

6. Start coding
```
$ jupyter-lab
```

# Integration Test

1. Start Airflow container (SequentialExecitor)
```
$ scripts/airflow.sh start
```

2. Unpause dags 
```
$ scripts/airflow.sh unpause github_poll_trigger
$ scripts/airflow.sh unpause hello_world
```

3. Trigger dag 
```
$ scripts/airflow.sh trigger_dag -e 2020-03-28 github_poll_trigger
```

# Production Deployment

1. For LocalExecutor:
```
docker-compose -f docker-compose-LocalExecutor.yml up -d
```

2. For CeleryExecutor:
```
docker-compose -f docker-compose-CeleryExecutor.yml up -d
```

3. For Astronomer:

```
$ astro dev init
$ astro dev start
$ astro deploy
```

# Customizing Docker Image

You may want to rebuild the docker image when changes have been made to the
following files:
- requirements.txt
- scripts/docker-entrypoint.sh
- config/airflow.cfg
- Dockerfile

1.  Build image
```
$ docker build --rm -t altcoder/docker-airflow .
```

