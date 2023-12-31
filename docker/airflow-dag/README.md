# Building custom docker images :: Airflow-dag

When you want to run Airflow locally, you might want to use an extended image, containing some additional dependencies - for example you might add new python packages, or upgrade airflow providers to a later version. This can be done very easily by specifying build: . in your docker-compose.yaml and placing a custom Dockerfile alongside your docker-compose.yaml. Then you can use docker compose build command to build your image (you need to do it only once). You can also add the --build flag to your docker compose commands to rebuild the images on-the-fly when you run other docker compose commands.

Examples of how you can extend the image with custom providers, python packages, apt packages and more can be found in [Building the image](https://airflow.apache.org/docs/docker-stack/build.html)

## Build the Airflow image

```bash
docker build -t airflow-dag:latest-python3.8 .
```
