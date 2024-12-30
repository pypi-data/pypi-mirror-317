def extract_only_parenthesis(format):
    import re
    _number = re.findall(r'\(.*?\)', format)
    if len(_number) > 0:
        res = str(_number[0])
        res = res.replace("(", "").replace(")", "").strip()
    else:
        res = ""
    return res


def extract_only_column_text(columns):
    import re
    new_col = str(columns).lower()

    _text = re.findall(r'([a-zA-Z ]+)', new_col)
    if len(_text) > 0:
        res = _text[0]
    else:
        res = ""
    return res


def spark_reformat_dtype_data(columns, format, convert_string=False):
    from pyspark.sql import types

    _format = str(extract_only_column_text(format)).upper()
    _format_text = str(extract_only_column_text(format)).upper()
    if str(_format).upper() == "DATE":
        _mask = "yyyy-MM-dd"
        _format = format
        _format_spark = "date"
        _locale = "es_PE"
        _schema_type = "['date', 'null']"
        _type = types.StructField(columns, types.DateType())
        _type_string = types.StructField(columns, types.StringType())
        if convert_string:
            _mask = ""
            _format = "ALPHANUMERIC(10)"
            _locale = ""
            _schema_type = "['string', 'null']"
    elif str(_format).upper() == "TIMESTAMP":
        _mask = "yyyy-MM-dd HH:mm:ss.SSSSSS"
        _format = format
        _format_spark = "timestamp"
        _locale = "es_PE"
        _schema_type = "['timestamp', 'null']"
        _type = types.StructField(columns, types.TimestampType())
        _type_string = types.StructField(columns, types.StringType())
        if convert_string:
            _mask = ""
            _format = "ALPHANUMERIC(26)"
            _locale = ""
            _schema_type = "['string', 'null']"

    elif str(_format).upper() == "TIME":
        _mask = ""
        _format = "ALPHANUMERIC(8)"
        _format_spark = "string"
        _locale = ""
        _schema_type = "['string', 'null']"
        _type = types.StructField(columns, types.StringType())
        _type_string = types.StructField(columns, types.StringType())
    elif str(_format).upper() in ("NUMERIC SHORT", "INTEGER"):
        _mask = ""
        _format = format
        _format_spark = "integer"
        _locale = ""
        _schema_type = "['null', 'int32']"
        _type = types.StructField(columns, types.IntegerType())
        _type_string = types.StructField(columns, types.StringType())
        if convert_string:
            _mask = ""
            _format = "ALPHANUMERIC"
            _locale = ""
            _schema_type = "['string', 'null']"
    elif str(_format).upper() in ("NUMERIC BIG", "NUMERIC LARGE"):
        _mask = ""
        _format = format
        _format_spark = "long"
        _locale = ""
        _schema_type = "['null', 'int64']"
        _type = types.StructField(columns, types.IntegerType())
        _type_string = types.StructField(columns, types.StringType())
        if convert_string:
            _mask = ""
            _format = "ALPHANUMERIC"
            _locale = ""
            _schema_type = "['string', 'null']"
    elif str(_format).upper().startswith("DECIMAL"):
        _parentheses = extract_only_parenthesis(format)
        _parentheses_split = str(_parentheses).split(",")
        if len(_parentheses_split) <= 1:
            _decimal_left = int(_parentheses_split[0])
            _decimal_right = 0
        else:
            _decimal_left = int(_parentheses_split[0])
            _decimal_right = int(_parentheses_split[1])

        _mask = ""
        _format = format
        _format_spark = f"decimal({_decimal_left},{_decimal_right})"
        _locale = ""
        _schema_type = f"['null', '{format}']"
        _type = types.StructField(columns, types.DecimalType(precision=_decimal_left, scale=_decimal_right))
        _type_string = types.StructField(columns, types.StringType())
        if convert_string:
            _mask = ""
            _format = "ALPHANUMERIC"
            _locale = ""
            _schema_type = "['string', 'null']"

    else:
        _mask = ""
        _format = format
        _format_spark = "string"
        _locale = ""
        _schema_type = "['string', 'null']"
        _type = types.StructField(columns, types.StringType())
        _type_string = types.StructField(columns, types.StringType())
        _format_text = "STRING"

    result = dict()
    result["_format"] = _format
    result["_format_spark"] = _format_spark
    result["_mask"] = _mask
    result["_locale"] = _locale
    result["_type"] = _type
    result["_type_string"] = _type_string
    result["_schema_type"] = _schema_type
    result["_format_text"] = _format_text

    return result


def get_statistics_schema(schema=None, columns_all=False):
    import json
    from prettytable import PrettyTable
    from spark_dataframe_tools import spark_reformat_dtype_data

    artifactory_json = json.loads(schema.getRaw())

    t = PrettyTable()
    t.field_names = [f"Naming", "Type", "Obligatory"]
    for row in artifactory_json["fields"]:
        naming = str(row['name']).lower().strip()
        logical_format = row['logicalFormat']
        _type = row['type']
        _obligatory = True
        if isinstance(_type, list):
            _obligatory = False

        if columns_all:
            _reformat = spark_reformat_dtype_data(naming, logical_format, convert_string=False)
            _format = _reformat.get("_format")
            _format_spark = _reformat.get("_format_spark")
            t.add_row([naming, _format_spark, _obligatory])
        else:
            if naming not in ("cutoff_date", "gf_cutoff_date", "audtiminsert_date"):
                _reformat = spark_reformat_dtype_data(naming, logical_format, convert_string=False)
                _format = _reformat.get("_format")
                _format_spark = _reformat.get("_format_spark")
                t.add_row([naming, _format_spark, _obligatory])

    print(t)


def get_casting_dataframe(schema=None, df=None, columns_all=False):
    import json
    from pyspark.sql import functions as func
    from spark_dataframe_tools import spark_reformat_dtype_data

    artifactory_json = json.loads(schema.getRaw())

    struct_list = list()
    for row in artifactory_json["fields"]:
        naming = str(row.get("name", "").lower().strip())
        logical_format = str(row.get("logicalFormat", "").lower().strip())

        if columns_all:
            _reformat = spark_reformat_dtype_data(naming, logical_format, convert_string=False)
            _format_spark = _reformat.get("_format_spark")
            struct_list.append((naming, _format_spark))
        else:
            if naming not in ("cutoff_date", "gf_cutoff_date", "audtiminsert_date"):
                _reformat = spark_reformat_dtype_data(naming, logical_format, convert_string=False)
                _format_spark = _reformat.get("_format_spark")
                struct_list.append((naming, _format_spark))

    df = df.select(*[func.col(col[0]).cast(col[1]) for col in struct_list])

    return df
