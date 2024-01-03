from pyspark.sql import SparkSession, DataFrame
from pyspark.context import SparkContext
from pyspark.conf import SparkConf
import pyspark.pandas as pd
import json
import os
import pathlib
import sys


if __name__ == "__main__":
    SECRETS_DIR = pathlib.Path(os.environ["SECRETS_DIR"])
    DATA_DIR = pathlib.Path(os.environ["DATA_DIR"])

    conf = SparkConf()
    conf.set(
        "spark.jars",
        "/opt/bitnami/spark/jars/mysql-connector-j-8.0.33.jar",
    )
    conf.set(
        "spark.sql.shuffle.partitions",
        60,
    )
    # conf.set(
    #     "spark.tasks.cpus",
    #     9,
    # )
    conf.set(
        "spark.jars",
        "/opt/bitnami/spark/jars/postgresql-42.6.0.jar",
    )
    conf.set(
        "spark.driver.extraClassPath",
        "/opt/bitnami/spark/jars/mysql-connector-j-8.0.33.jar",
    )
    print(f"{conf.getAll()=}")
    print(f"{sys.argv=}")

    spark = (
        SparkSession.builder.appName("readsql")
        .master("k8s://http://localhost:63097")
        # .master("local[4]")
        .config(conf=conf)
        .getOrCreate()
    )
    print(f"{spark=}")
    print(f"{spark.sparkContext=}")

    uri_db = json.load((DATA_DIR / "db-metadados.json").open())

    # sql = json.load((DATA_DIR / "-config-map").open()).get("query", {})
    # sql = """
    # (select ps.id as id, ps.cpf, ps.cnpj, ps.quantity, ps.price, ps.saleDate from prod_icv_db.PreSale ps) as prevendas
    # """
    sql = """
    (SELECT p.id, p.name, p.age
    FROM spark.person p) as person
    """
    jdbc = "jdbc:{type}://{host_mysql}:{port}/{db}?".format_map(uri_db) + "&".join(
        f"{key}={value}"
        for key, value in dict(
            **json.load((SECRETS_DIR / "pyspark-project.json").open()),
            **uri_db.get("extra", {}),
        ).items()
    )
    # df = pd.read_sql(sql=sql, con=jdbc, numPartitions=3)
    df: DataFrame = (
        spark.read.format("jdbc")
        .options(
            url=jdbc,
            driver="com.mysql.jdbc.Driver",
            numPartitions="9",
            dbtable=sql,
            partitionColumn="id",
            upperBound="100000",
            lowerBound="0",
        )
        .load()
        .cache()
    )
    # df = df.repartition(9)
    # df = pd.read_sql(sql=sql, con=jdbc, numPartitions=3)
    # df = df.to_spark()
    # type(df)
    # df.info()
    # df.write.format("jdbc").\
    # .option("url","jdbc:postgres://localhost:5432/postgres")\
    # .option()
    # df2 = df.to_spark()
    type(df)
    host_postgres = uri_db.get("postgres_host", {})
    df.repartition(9).write.format("jdbc").options(
        url=f"jdbc:postgresql://{host_postgres}:5432/postgres?user=postgres&password=password",
        driver="org.postgresql.Driver",
        dbtable="sparkProject",
        # query="CREATE TABLE campanhasSpark AS select * from df2"
    ).saveAsTable(name="sparkProject", mode="overwrite")
    # print("--------")
    # df2 = df.to_pandas()
    # print(df2.infer_objects().dtypes)
    spark.stop()
