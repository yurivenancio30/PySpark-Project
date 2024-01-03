FROM bitnami/spark
USER root
COPY ./jars/mysql-connector-j-8.0.33.jar /opt/bitnami/spark/jars/
COPY ./jars/postgresql-42.6.0.jar /opt/bitnami/spark/jars/
WORKDIR /opt/bitnami/spark/python/
COPY pyspark_project.py ./
RUN chmod +x pyspark_project.py
RUN pip install pyspark
RUN pip install 'pandas < 2'
RUN pip install pyarrow
ENV PYSPARK_PYTHON=/opt/bitnami/python/bin/python3
ENV PYSPARK_DRIVER_PYTHON=/opt/bitnami/python/bin/python3
#USER 1001
WORKDIR /opt/bitnami/spark
