from __future__ import annotations

import pendulum

from airflow.decorators import dag
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

@dag(
    dag_id="mlops_project_training_pipeline",
    schedule=None,  # This DAG will only be triggered manually for now
    start_date=pendulum.datetime(2025, 1, 1, tz="Europe/Berlin"),
    catchup=False,
    doc_md="""
    ## MLOps Project Training Pipeline
    This DAG retrains the insurance prediction model. It uses the DockerOperator
    to run the entire training process inside a container.
    """,
    tags=["mlops", "training"],
)
def training_pipeline():
    """Defines the training pipeline DAG."""

    retrain_model_task = DockerOperator(
        task_id="run_training_script",
        image="my_fastapi",  # The name of the Docker image you built
        command="python main.py",
        docker_url="unix://var/run/docker.sock",
        mount_tmp_dir=False,
        # Mounts your project folder so the container can access the code
        # and so the mlruns/ and models/ folders are updated on your host machine.
        mounts=[
            Mount(
                source="C:/Users/malte/Desktop/Coding/mlops-project",
                target="/app",
                type="bind"
            )
        ],
        working_dir="/app"
    )

training_pipeline()