import os
from urllib.parse import quote

import taosws
import pandas as pd
from loguru import logger

try:
    from mydatatools.read_config import *
except Exception as e:
    logger.error(e)
    IB_TURBINE_TYPE, IB_TABLE, IB_USER, IB_PASSWORD, IB_HOST, IB_PORT, IB_DB = (
        None, None, None, None, None, None, None
    )


class PVDataTools(object):
    """
    明阳量云集控数据获取工具
    """
    def __init__(self, map_table_path=os.path.join(".", '光伏点表映射汇总表.csv'), username=IB_USER,
                 password=IB_PASSWORD, host=IB_HOST, port=IB_PORT, db=IB_DB,
                 **kwargs):
        self.db = db
        self.engine = taosws.connect(f"taosws://{username}:{quote(password)}@{host}:{port}")
        # 点表信息
        self.all_map_data = pd.read_csv(map_table_path)

        self.kwargs = kwargs

    def get_map_data(self) -> pd.DataFrame:
        return self.all_map_data

    def get_data(self, farm_code, turbine_code, turbine_type=IB_TURBINE_TYPE,  table_name=IB_TABLE,
                 col_names=None, start_date=None, end_date=None) -> pd.DataFrame:
        """
        Return DataFrame.

        Returns
        -------
        DataFrame

        Examples
        --------
        For Series

        >>> dt = PVDataTools("D:\project\GearingBoxOilFilterFDModel\光伏点表映射汇总表.csv",
        >>>              username="root",
        >>>              password="taosdata", host="172.16.0.14", port="6041", db=IB_DB)
        >>> df = dt.get_data(farm_code='95004', turbine_code='95004001', turbine_type="sun2000_125ktl_c1",
        >>>              col_names=['group_current1', 'group_voltage1', 'group_current2', 'group_voltage2'],
        >>>              table_name="sun2000_125ktl_c1", start_date='2024-10-24', end_date='2024-10-25')

                            turbine_code  ...  group_voltage2
        real_time                         ...
        2024-10-24 00:00:00     95004001  ...             0.0
        2024-10-24 00:00:01     95004001  ...             0.0
        ...
        2024-10-24 23:59:55     95004001  ...             0.0
        2024-10-24 23:59:56     95004001  ...             0.0
        """
        # 根据col_names 映射为实际的点表tags
        tag_maps_all = self.all_map_data[(self.all_map_data["TYPE"] == turbine_type) &
                                         (self.all_map_data["GENERAL_NAME_EN"].notnull())]
        if col_names is None:
            tags_lis = tag_maps_all["GENERAL_NAME_EN"].tolist()
        else:
            if not isinstance(col_names, list):
                col_names = [col_names]
            tags_lis = [c for c in col_names if c in tag_maps_all["GENERAL_NAME_EN"].tolist()]
            if len(tags_lis) < len(col_names):
                logger.warning('warring 部分给定的字段名有误。')

        db = self.db or f"cc_db{farm_code}"

        if len(tags_lis) == 0:
            logger.error('请输入准确的字段名称！')
            return pd.DataFrame()
        if isinstance(turbine_code, str):
            turbine_code = [turbine_code]

        tag_time = tag_maps_all[tag_maps_all["GENERAL_NAME_EN"] == "real_time"]["TAG_NAME_EN"].iloc[0]
        tag_turbine = tag_maps_all[tag_maps_all["GENERAL_NAME_EN"] == "turbine_code"]["TAG_NAME_EN"].iloc[0]

        tags_lis = list(set(["real_time", "turbine_code"] + tags_lis))
        new_tag_maps = tag_maps_all[tag_maps_all["GENERAL_NAME_EN"].isin(tags_lis)]
        turbine_code_str = ', '.join(["'{}'".format(tl) for tl in turbine_code])

        sqlstr = f"""SELECT {self.build_query_field(new_tag_maps['TAG_NAME_EN'], new_tag_maps['GENERAL_NAME_EN'])}
         FROM {db}.{table_name} WHERE {tag_turbine} IN ({turbine_code_str})"""

        if start_date is not None:
            sqlstr = sqlstr + f" AND {tag_time} >= '{start_date}'"
        if end_date is not None:
            sqlstr = sqlstr + f" AND {tag_time} < '{end_date}'"
        sqlstr = sqlstr + ';'
        df = pd.read_sql_query(sqlstr, self.engine)

        # 设置时间索引
        df["real_time"] = pd.to_datetime(df["real_time"])
        df.set_index("real_time", drop=True, inplace=True)
        return df

    def build_query_field(self, origin_cols, transform_cols):
        field_list = []
        for orig_col, transform_col in zip(origin_cols, transform_cols):
            field_list.append(f"{orig_col.lower()} AS {transform_col}")

        return ",".join(field_list)


if __name__ == '__main__':

    dt = PVDataTools("D:\project\GearingBoxOilFilterFDModel\光伏点表映射汇总表.csv",
                     username="root",
                     password="taosdata", host="172.16.0.14", port="6041", db=IB_DB
                     )
    df = dt.get_data(farm_code='95004', turbine_code='95004001', turbine_type="sun2000_125ktl_c1", table_name="sun2000_125ktl_c1",
                     col_names=['group_current1', 'group_voltage1', 'group_current2', 'group_voltage2'],
                     start_date='2024-10-24', end_date='2024-10-25')

    print(df)
