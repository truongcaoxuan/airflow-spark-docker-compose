#FROM apache/airflow:2.6.2-python3.8
FROM apache/airflow:latest-python3.8
#FROM apache/airflow:2.7.0
# adding apt package (adds vim and java to the airflow image)
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim wget openjdk-11-jre-headless\
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
	
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Install MongoDB Shell
RUN wget https://downloads.mongodb.com/compass/mongodb-mongosh_1.10.6_amd64.deb && \
    apt install ./mongodb-mongosh*.deb && \
    rm -f mongodb-mongosh*.deb

# Install Mongodb database tools
RUN wget https://fastdl.mongodb.org/tools/db/mongodb-database-tools-debian11-x86_64-100.8.0.deb && \
    apt install ./mongodb-database-tools-*.deb && \
    rm -f mongodb-database-tools-*.deb
	
USER airflow

# adds python packages/ Airflow Provider package from requirements.txt from PyPI to the image
# adds apache-spark airflow-providers which requires both java and python package from PyPI.
COPY requirements.txt /
#RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
RUN pip install --upgrade pip
RUN pip install "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt