from .datetypes import DatabendDataType
import re


class QueryResult(object):
    """
    Stores query result from multiple response data.
    """

    def __init__(
        self, data_generator, first_data, with_column_types=False, null_to_none=False
    ):
        self.data_generator = data_generator
        self.with_column_types = with_column_types
        self.first_data = first_data
        self.column_data_dict_list = []
        self.columns_with_types = []
        self.column_type_dic = {}
        self.type_convert = DatabendDataType.type_convert_fn
        self.null_to_none = null_to_none

        super(QueryResult, self).__init__()

    def store_data(self, raw_data: dict):
        fields = raw_data.get("schema")
        column_name_ls = []
        datas = raw_data.get("data")
        for field in fields:
            column_name_ls.append(field["name"])

        for data in datas:
            self.column_data_dict_list.append(dict(zip(column_name_ls, data)))

    def store_columns(self, raw_data: dict):
        fields = raw_data.get("schema")
        for field in fields:
            inner_type = self.extract_type(field["type"])
            column_type = (field["name"], inner_type)
            self.column_type_dic[field["name"]] = inner_type
            self.columns_with_types.append(column_type)

    def get_result(self):
        """
        :return: stored query result.
        """
        data = []
        self.store_data(self.first_data)
        self.store_columns(self.first_data)
        for d in self.data_generator:
            self.store_data(d)

        for read_data in self.column_data_dict_list:
            tmp_list = []
            for c, d in read_data.items():
                if d == "NULL":
                    if self.null_to_none:
                        tmp_list.append(None)
                    else:
                        tmp_list.append(d)
                else:
                    tmp_list.append(self.type_convert(self.column_type_dic[c])(d))
            data.append(tuple(tmp_list))

        if self.with_column_types:
            return self.columns_with_types, data
        else:
            return [], data

    @staticmethod
    def extract_type(schema_type):
        if "nullable" in schema_type.lower():
            return re.findall(r"[(](.*?)[)]", schema_type)[0]
        elif "(" in schema_type:
            return schema_type.split("(")[0]
        else:
            return schema_type
