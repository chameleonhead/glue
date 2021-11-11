from pyspark import SparkContext
from awsglue.context import GlueContext

glueContext = GlueContext(SparkContext.getOrCreate()) 
inputDF = glueContext.create_dynamic_frame_from_options(connection_type = "s3", connection_options = {"paths": ["s3://firststep-glue-nagano-20211105/s3s3in/1_cvlog.csv"]}, format = "csv")
inputDF.toDF().show()
