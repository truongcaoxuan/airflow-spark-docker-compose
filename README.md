# Apache Airflow and Spark Data Pipelines with Docker Compose

This repository offers a comprehensive guide and practical examples for setting up `Apache Airflow` and `Apache Spark` data pipelines using `Docker Compose`. It covers three different Apache Airflow executors: `Sequential` Executor, `Local` Executor, and `Celery` Executor, enabling you to select the executor that best suits your specific workflow.

## Table of Contents

### 1. Introduction

### 2. Prerequisites

- Install Docker

- Install Docker Compose

- Install Docker Desktop on Windows

### 3. Getting Started

- Running Docker Build for Custom Images

### 4. Repository Structure

### 5. Examples

- Sequential Executor

- Local Executor

- Celery Executor

### 6. Usage

### 7. Contributing

### 8. License

## Introduction

Apache Airflow and Apache Spark are powerful tools for orchestrating and processing data workflows. This repository provides a straightforward way to set up Airflow and Spark using Docker Compose, making it easy to begin working with different executor configurations.

## Prerequisites

Before you can effectively use this repository, you need to set up Docker and Docker Compose on your system.

### Install Docker

Docker is a containerization platform that allows you to package and distribute applications as containers. Follow the installation guide for your operating system:
[Install Docker on Windows](https://docs.docker.com/desktop/install/windows-install/)

### Install Docker Compose

Docker Compose is a tool for defining and running multi-container Docker applications. Install Docker Compose by following the official guide:
[Install Docker Compose](https://docs.docker.com/compose/install/)

### Install Docker Desktop on Windows

If you are using Windows, it's recommended to use Docker Desktop, which provides an integrated environment for Docker on Windows. Follow the instructions to install [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/).

## Getting Started

To begin using this repository and set up Apache Airflow and Apache Spark with various executors, follow these steps:

### 1. Clone this repository to your local machine

```bash
git clone https://github.com/truongcaoxuan/airflow-spark-docker-compose.git
```

### 2. Navigate to the repository directory

```bash
cd airflow-spark-docker-compose
```

Explore the examples and usage instructions in the respective sections below to configure and run Apache Airflow with your preferred executor.

### Running Docker Build for Custom Images

So we need to create custom Docker images for Airflow, Spark, or MongoDB and add dependencies via a requirements.txt file, follow these steps:

Navigate to the respective directory for the custom image you want to build (e.g., airflow-custom-image, spark-custom-image, or mongodb-custom-image).

Build the custom image using Docker:

```bash
docker build -t custom-image-name .
```

Ensure that the custom image is added to your docker-compose.yml file.

Run Docker Compose to set up your environment as per the examples provided.

### 1. Build the Spark image

```bash
cd docker/spark-cluster
docker build -t spark-cluster:3.4.1 .
```

### 2. Build the Airflow image

```bash
cd docker/airflow-dag
docker build -t airflow-dag:latest-python3.8 .
```

### 3. Build the Mongodb image

```bash
cd docker/mongodb
docker build -t mongodb:latest .
```

## Repository Structure

The repository is organized as follows:

- docker/: Contains Dockerfile to build docker images: airflow-dag, spark-cluster, mongodb
- examples/: Contains subdirectories with examples for each executor type.
  - docker-compose.yml: The Docker Compose configuration file for setting up Airflow, Spark, and related services.
  - airflow/dags/: Directory to store your Apache Airflow DAGs (workflow definitions).

- README.md: This README file with instructions and descriptions.

## Examples

This repository provides examples for three different Apache Airflow executors: Sequential Executor, Local Executor, and Celery Executor.

### 1. Sequential Executor

The Sequential Executor runs tasks sequentially within a single process. It's suitable for development and testing when parallelism is not required.

Example DAG and configuration files: `examples/dags-sequential-executor/`

### 2. Local Executor

The Local Executor runs tasks in parallel on the same machine, making it suitable for small to medium workloads.

Example DAG and configuration files: `examples/dags-local-executor/`

### 3. Celery Executor

The Celery Executor uses Celery, a distributed task queue, to execute tasks in parallel across a cluster of worker nodes. It's suitable for scaling to handle large workloads.

Example DAG and configuration files: `examples/dags-celery-executor/`

## Usage

Detailed usage instructions for each executor type and examples can be found in their respective subdirectories within the examples directory.

## Contributing

If you'd like to contribute to this repository, please follow the standard GitHub workflow:

- Fork the repository.
- Create a new branch for your feature or bug fix: git checkout -b feature-name
- Make your changes and commit them with clear messages.
- Push your changes to your fork: git push origin feature-name
- Create a Pull Request (PR) from your fork to the main repository.
- Please ensure your code adheres to best practices and includes appropriate documentation.

## License

This repository is licensed under the MIT License. See the LICENSE file for details.

---
By following this guide and using the provided examples, you can set up Apache Airflow and Apache Spark data pipelines with different executors using Docker Compose. Whether you need a simple sequential executor for development or a scalable Celery executor for production, this repository offers a flexible solution. Enjoy building your data pipelines!
