# spark_dataframe_tools

[![Github License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Updates](https://pyup.io/repos/github/woctezuma/google-colab-transfer/shield.svg)](pyup)
[![Python 3](https://pyup.io/repos/github/woctezuma/google-colab-transfer/python-3-shield.svg)](pyup)
[![Code coverage](https://codecov.io/gh/woctezuma/google-colab-transfer/branch/master/graph/badge.svg)](codecov)

spark_dataframe_tools is a Python library that implements styles in the Dataframe

## Installation

The code is packaged for PyPI, so that the installation consists in running:

```sh
pip install spark-dataframe-tools --user --upgrade
```

## Usage
```sh
import spark_dataframe_tools 
```

```sh
from pyspark.sql.types import StructType,StructField, StringType, IntegerType
data2 = [("James","","Smith","36636","M",3000),
    ("Michael","Rose","","40288","M",4000),
    ("Robert","","Williams","42114","M",4000),
    ("Maria","Anne","Jones","39192","F",4000),
    ("Jen","Mary","Brown","","F",-1)
  ]

schema = StructType([ \
    StructField("firstname",StringType(),True), \
    StructField("middlename",StringType(),True), \
    StructField("lastname",StringType(),True), \
    StructField("id", StringType(), True), \
    StructField("gender", StringType(), True), \
    StructField("salary", IntegerType(), True) \
  ])
 
df = spark.createDataFrame(data=data2, schema=schema)
```

## Pandas

```sh
df_pandas = df.toPandas()
df_pandas.show2()
```

## Spark

```sh
# Dataframe template table
df.show2()

# Dataframe memory usage
df.size()
```



## License

[Apache License 2.0](https://www.dropbox.com/s/8t6xtgk06o3ij61/LICENSE?dl=0).

## New features v1.0

## BugFix

- choco install visualcpp-build-tools

## Reference

- Jonathan Quiza [github](https://github.com/jonaqp).
- Jonathan Quiza [RumiMLSpark](http://rumi-ml.herokuapp.com/).
