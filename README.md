version: '3'


services:
  postgres:
    image: postgres:14.0
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    logging:
      options:
        max-size: 10m
        max-file: "3"
    ports:
      - "5433:5433"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U airflow"]
      interval: 30s
      timeout: 30s
      retries: 3
    networks:
      - confluent

# apache/airflow:2.6.0-python3.9   airflow:0.0.1
  webserver:
    image: airflow:0.0.1
    command: webserver
    entrypoint: ['/opt/airflow/script/entrypoint.sh']
    depends_on:
      - postgres
    environment:
      LOAD_EX: 'n'
      EXECUTOR: SequentialExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres:5432/airflow
      AIRFLOW_WEBSERVER_SECRET_KEY: this_is_a_very_secured_key
    logging:
      options:
        max-size: 10m
        max-file: "3"
    volumes:
      - ./dags:/opt/airflow/dags
      - ./script/entrypoint.sh:/opt/airflow/script/entrypoint.sh
      #- ./requirements.txt:/opt/airflow/requirements.txt
    ports:
      - "8080:8080"
    healthcheck:
      test: ['CMD-SHELL', "[ -f /opt/airflow/airflow-webserver.pid ]"]
      interval: 30s
      timeout: 30s
      retries: 3
    networks:
      - confluent

  scheduler:
    image: apache/airflow:2.6.0-python3.9
    depends_on:
      postgres:
        condition: service_healthy
      webserver:
        condition: service_healthy
    volumes:
      - ./dags:/opt/airflow/dags
      - ./requirements.txt:/opt/airflow/requirements.txt
    environment:
      LOAD_EX: 'n'
      EXECUTOR: SequentialExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres:5432/airflow
      AIRFLOW_WEBSERVER_SECRET_KEY: this_is_a_very_secured_key
    command: bash -c "pip install -r ./requirements.txt && airflow db upgrade && airflow scheduler"
    networks:
      - confluent

networks:
  confluent:
    driver: bridge