def show_pd_df(self):
    from IPython.display import display, HTML
    style = """
    <style scoped>
        .dataframe-div {
          max-height: 300px;
          overflow: auto;
          position: relative;
        }
        .dataframe {
            border-collapse: collapse;
            font-size: 0.8em;
            font-family: sans-serif;
            min-width: 400px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
        }

        .dataframe thead tr {
            background-color: #009879;
            color: #ffffff;
            text-align: left;
        }

        .dataframe tbody tr {
            border-bottom: 1px solid #dddddd;
        }

        .dataframe tbody tr:nth-of-type(even) {
            background-color: #f3f3f3;
        }

        .dataframe tbody tr:last-of-type {
            border-bottom: 2px solid #009879;
        }

        .dataframe tbody tr.active-row {
            font-weight: bold;
            color: #009879;
        }
    </style>
    """
    df_html = self.to_html()
    df_html = style + '<div class="dataframe-div">' + df_html + "\n</div>"

    return display(HTML(df_html))


def show_spark_df(self, limit=10):
    import os
    import jinja2
    import humanize
    from spark_dataframe_tools.utils import BASE_DIR

    from IPython.display import display, HTML

    def collect_to_dict(df_collect):
        dict_result = [v.asDict() for v in df_collect]
        return dict_result

    _columns = [c for c in self.columns]
    if limit is None:
        limit = 10

    data_select = self.select(_columns).limit(limit)
    data = collect_to_dict(data_select.toLocalIterator())

    template_dir = os.path.join(BASE_DIR, "utils", "templates")
    template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)
    template = template_env.get_template("table.html")

    dtypes = [(i[0], i[1],) for i, j in zip(data_select.dtypes, data_select.schema)]

    total_rows = self.cache().count()
    limit = min(limit, total_rows)

    total_rows = humanize.intword(total_rows)
    total_cols = len(_columns)
    total_partitions = data_select.rdd.getNumPartitions()

    output = template.render(cols=dtypes, data=data, limit=limit,
                             total_rows=total_rows, total_cols=total_cols,
                             partitions=total_partitions)
    return display(HTML(output))


def show_size_df(self):
    from pyspark.serializers import PickleSerializer, AutoBatchedSerializer
    from sizebytes_tools import convert_bytes
    from pyspark.sql import SparkSession

    def _to_java_object_rdd(rdd):
        rdd = rdd._reserialize(AutoBatchedSerializer(PickleSerializer()))
        return rdd.ctx._jvm.org.apache.spark.mllib.api.python.SerDe.pythonToJava(rdd._jrdd, True)

    JavaObj = _to_java_object_rdd(self.rdd)
    spark = SparkSession.getActiveSession()
    sc = spark.sparkContext
    data_memory = sc._jvm.org.apache.spark.util.SizeEstimator.estimate(JavaObj)
    data_memory = convert_bytes(data_memory)
    print(f'The memory of the dataframe is: {data_memory}')
