import re
import os
import datetime
from typing import Generator

import pandas as pd
from tabulate import tabulate



class ParseLogException(Exception):...
class LogFilterException(ParseLogException):...
class LogAnalystException(ParseLogException):...
class StatisticsException(ParseLogException):...
class CompareException(ParseLogException):...



TIME_REGEX = r"^\[(?P<timepoint>.*?)\].*"
TIME_COLUMN_NAME = "timepoint"
#
class Color:
    WHITE =  "#FFFFFF"
    IVORY_WHITE = "#FAFAFA"
    GREEN = "#9ACD32"
    DARK_GREEN = "#01635E"
    RED = "#FA8072"
    LIGHT_BLUE = "#E4FFFF"



class Tool:

    @staticmethod
    def str2timestamp(time_str):
        return datetime.datetime.strptime(time_str, "%m/%d/%y %H:%M:%S:%f").timestamp()


    @staticmethod
    def is_float(value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False



class BaseLogFilter:

    def __call__(self, log_path) -> list[str]:
        raise NotImplemented(f"NotImplemented yet.")



class BaseLogAnalyst:

    def __call__(self, log_rows: list[str]) -> pd.DataFrame:
        raise NotImplemented(f"NotImplemented yet.")



class BaseStatistics:

    def __call__(self, df: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        raise NotImplemented(f"NotImplemented yet.")


class LogFilter(BaseLogFilter):

    def __init__(self, trait_regex:str):
        self.trait_regex = re.compile(trait_regex)


    def __call__(self, log_path):
        if not os.path.isfile(log_path):
            raise LogFilterException(f"log_path={log_path}, nonexistent or not a file.")

        with open(log_path, 'r', errors='ignore') as fd:
            stop_flag = False
            for row in fd:
                if stop_flag:
                    print("quit...., anyway")
                    break
                if re.match(self.trait_regex, row):
                    stop_flag = yield row



class LogAnalyst(BaseLogAnalyst):

    def __init__(self, analytic_regex):
        self.analytic_regex = re.compile(analytic_regex)


    def __call__(self, log_rows: list[str]) -> pd.DataFrame:
        record = []
        for row in log_rows:
            match = re.search(self.analytic_regex, row)
            if match:
                record.append(match.groupdict())
        df = pd.DataFrame(record)
        return df



class PartRepeatAnalyst(BaseLogAnalyst):

    def __init__(self, part_regex, ignore_time=True):
        self.ignore_time = ignore_time
        self.time_regex = re.compile(TIME_REGEX)
        self.part_regex = part_regex


    def _get_time(self, log_row: str):
        matched = re.match(self.time_regex, log_row)
        if not matched:
            raise LogAnalystException(f'Time not found in "{log_row}"')
        return Tool.str2timestamp(matched.groupdict()[TIME_COLUMN_NAME])


    def __call__(self, log_rows: list[str]) -> pd.DataFrame:
        record = []
        for row in log_rows:
            cols = re.findall(self.part_regex, row)
            if not self.ignore_time:
                cols.insert(0, (TIME_COLUMN_NAME, self._get_time(log_row=row)))
            record.append(dict(cols))
        df = pd.DataFrame(record)
        return df



class Statistics(BaseStatistics):

    def __init__(self, ignore_cols: list = None, group_cols: list = None):
        self.df: pd.DataFrame = None
        self.stat_func = ["mean", "median", "std"]
        self.head_offset = 0
        self.tail_offset = 0
        self.ignore_cols = [] if not ignore_cols else ignore_cols
        self.group_cols = [] if not group_cols else group_cols
        self.decimals = 3
        #
        if "STAT" not in self.group_cols:
            self.group_cols.append("STAT")


    def _offset_then_stat(self, aft_gp_df, func:str):
        if not hasattr(aft_gp_df, func):
            raise StatisticsException(f"Not support statistics function '{func}'.")
        if  len(aft_gp_df) < self.head_offset + self.tail_offset + 1:
            raise StatisticsException(f"After group, df only have {len(aft_gp_df)} rows, but head_offset+tail_offset={self.head_offset + self.tail_offset}.")
        df_slice = slice(self.head_offset, -self.tail_offset if self.tail_offset else None)
        return getattr(aft_gp_df.iloc[df_slice], func)()


    def _ignore(self):
        if self.ignore_cols:
            columns = self.df.columns.to_list()
            columns = [column for column in columns if column not in self.ignore_cols]
            self.df = self.df[columns]


    def _to_numeric(self):
        columns = self.df.columns.to_list()
        columns = [column for column in columns if column not in self.ignore_cols]
        columns = [column for column in columns if column not in self.group_cols]
        self.df[columns] = self.df[columns].apply(pd.to_numeric, errors='coerce')


    def _stat(self) -> list[pd.DataFrame]:
        stats = []
        for func in  self.stat_func:
            self.df["STAT"] = func
            stats.append(
                self.df.groupby(by=self.group_cols, as_index=False).apply(lambda gp_df: self._offset_then_stat(gp_df, func))
            )
        return stats


    def _merge(self, stats: list[pd.DataFrame]) -> pd.DataFrame:
        merged = pd.concat(stats, ignore_index=True)
        merged = merged.sort_values(by=self.group_cols)
        merged.set_index(self.group_cols, inplace=True)
        return merged


    def __call__(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        if df.empty:
            return pd.DataFrame()
        if kwargs.get("stat_func"):
            self.stat_func = kwargs["stat_func"]
        if kwargs.get("head_offset"):
            self.head_offset = abs(kwargs["head_offset"])
        if kwargs.get("tail_offset"):
            self.tail_offset = abs(kwargs["tail_offset"])
        if kwargs.get("decimals") or kwargs.get("decimals") == 0:
            self.decimals = abs(kwargs["decimals"])

        self.df = df
        self._to_numeric()
        self._ignore()
        return self._merge(self._stat()).round(self.decimals)



class BaseLog:
    filter: BaseLogFilter = None
    analyst: BaseLogAnalyst = None
    statistician: BaseStatistics = None

    def __init__(self, log_path: str, meta: dict =None):
        self.log_file = log_path
        self.meta = meta if meta else {"path": log_path if len(log_path) < 33 else f"{log_path[:15]}...{log_path[-15:]}"}
        self._filtered_rows: Generator = None
        self._analyzed_data: pd.DataFrame = None
        self._statistical_data: pd.DataFrame = None


    def _merge_meta_to_index(self, df: pd.DataFrame):
        meta_df = pd.DataFrame(self.meta, index=[0])
        old_index = df.index.to_frame(index=False)
        new_index = pd.merge(meta_df, old_index, how="cross")
        df.index = pd.MultiIndex.from_frame(new_index)


    @property
    def filtered_rows(self):
        if isinstance(self._filtered_rows, Generator):
            try:
                next(self._filtered_rows)
                self._filtered_rows.send(True)
            except StopIteration:
                ...
        self._filtered_rows = self.filter(self.log_file)
        return self._filtered_rows


    def get_rows(self):
        temp = pd.DataFrame(self.filtered_rows, columns=["content"])
        self._merge_meta_to_index(df=temp)
        return temp


    def analyze(self):
        if self._analyzed_data is None:
            self._analyze()
        return self._analyzed_data


    def calculate(self, *, stat_func: list = None, head_offset: int = 0, tail_offset: int = 0, decimals: int = 3, **kwargs):
        if self._statistical_data is None:
            self._calc_statistics(stat_func=stat_func, head_offset=head_offset,
                                  tail_offset=tail_offset, decimals=decimals, **kwargs)
        return self._statistical_data


    def _analyze(self):
        self._analyzed_data = self.analyst(self.filtered_rows)
        self._merge_meta_to_index(df=self._analyzed_data)
        return self._analyzed_data


    def _calc_statistics(self, **kwargs):
        self._statistical_data = self.statistician(self.analyze(), **kwargs)
        self._merge_meta_to_index(df=self._statistical_data)
        return self._statistical_data



class LogBundle:

    def __init__(self, logs: dict[str:dict], log_level_params: dict, job_level_params: dict, log_classes: list[BaseLog] = None):
        if not log_classes:
            self.log_classes = BaseLog.__subclasses__()
        else:
            self.log_classes = log_classes
        #
        self.logs = logs
        #
        self.log_objs = {}
        for cls in self.log_classes:
            self.log_objs[cls.__name__] = [cls(log_path=log_path, meta=log_meta)
                                                for log_path, log_meta in self.logs.items()]
        #
        self.log_level_params = log_level_params
        self.job_level_params = job_level_params
        #
        self.calculated: dict[str:pd.DataFrame] = None
        self.report: dict[str:pd.DataFrame] = None
        self.compare_report: dict[str:pd.DataFrame] = None


    def filter_rows(self):
        sheets = {}
        for sheet_name, log_objs in self.log_objs.items():
            sheets[sheet_name] = pd.concat([log_obj.get_rows() for log_obj in log_objs], ignore_index=False)
            sheets[sheet_name] = sheets[sheet_name].rename_axis(index={0:"seq"})
        return sheets


    def analyze(self):
        sheets = {}
        for sheet_name, log_objs in self.log_objs.items():
            sheets[sheet_name] = pd.concat([log_obj.analyze().dropna(axis=1, how='all') for log_obj in log_objs], ignore_index=False)
        return sheets


    def calculate(self):
        sheets = {}
        for sheet_name, log_objs in self.log_objs.items():
            sheets[sheet_name] = pd.concat([log_obj.calculate(**self.log_level_params) for log_obj in log_objs], ignore_index=False)
        self.calculated = sheets
        return self.calculated


    def generate_report(self):
        if not self.calculated:
            self.calculate()
        if not self.job_level_params["zip"]:
            self.report = self.calculated
            return self.report
        #
        sheets = {}
        for sheet_name, df in self.calculated.items():
            if df.empty:
                sheets[sheet_name] = pd.DataFrame()
                continue
            index_columns = df.index.names
            groupby = [col for col in index_columns if col not in self.job_level_params["zip"]]
            #
            stats = []
            for func in self.job_level_params["stat_func"]:
                calc_col_dict = {col: (col, func) for col in df.columns}
                stat_df = df.reset_index().groupby(groupby).agg(**calc_col_dict).reset_index()
                if "STAT" in stat_df.columns:
                    stat_df["STAT"] = [f'{func}({f})' for f in stat_df["STAT"].values]
                stat_df.set_index(groupby, inplace=True)
                stats.append(stat_df)
            #
            stat_df = pd.concat(stats, ignore_index=False).round(decimals=self.job_level_params["decimals"])
            sheets[sheet_name] = stat_df
            self.report = sheets
        return self.report


    def compare_by(self, group_col: list = None):
        if not self.report:
            self.generate_report()
        if not group_col:
            return self.report
        self.compare_report = {name: self._compare_by(df=sheet, group_col=group_col) for name, sheet in self.report.items()}
        return self.compare_report


    def _compare_by(self, df: pd.DataFrame, group_col: list) -> pd.DataFrame:
        if df.empty:
            return pd.DataFrame()
        index_cols = list(df.index.names)
        exclude_group_index = [col for col in index_cols if col not in group_col]
        _df = df.reset_index()
        excluded_group_all = [col for col in _df.columns if col not in group_col]
        parts = [df[excluded_group_all].set_index(exclude_group_index) for _, df in _df.groupby(group_col)]
        if not parts:
            return pd.DataFrame()
        main_part = parts[0]
        result = pd.DataFrame(index=main_part.index, columns=main_part.columns)
        for row in main_part.index:
            for col in main_part.columns:
                vals = []
                for part in parts:
                    vals.append(str(part.at[row, col]) if row in part.index and col in part.columns else "")
                result.at[row, col] = r" / ".join(vals)
        return result



class BaseComparator:
    WORSE = -1
    UNCHANGE = 0
    BETTER = 1

    def __call__(self, fieldname: str, val1: float, val2: float) -> int:
        raise NotImplemented(f"NotImplemented yet.")



class FrameFormat:

    def __init__(self, comparator: BaseComparator = None):
        self.comparator = comparator


    def df2string(self, df: pd.DataFrame):
        return tabulate(df, headers='keys', tablefmt='pretty')


    def df2excel(self, df: pd.DataFrame, writer: pd.ExcelWriter, sheet_name: str):
        index_len = len(df.index.names) if isinstance(df.index, pd.MultiIndex) else 1
        #
        df = df.reset_index()
        df.to_excel(writer, sheet_name=sheet_name, startrow=0, index=False, merge_cells=False)

        # Obtain the workbook and worksheet objects from the xlsxwriter library.
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        #
        self._shape_table(worksheet, df)
        self._format_table(workbook, sheet_name, worksheet, df, index_len)


    def _format_table(self, workbook, sheetname, worksheet, df: pd.DataFrame, index_len: int):
        styles = {
            'col': workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1, 'bg_color': Color.DARK_GREEN, 'font_color': Color.IVORY_WHITE}),
            'index': workbook.add_format({'align': 'right', 'border': 1, 'bg_color': Color.LIGHT_BLUE}),
            'value': workbook.add_format({'align': 'left', 'border': 1, 'bg_color': Color.WHITE})
        }
        # range of the data (do not include column row)
        num_rows, num_cols = df.shape
        # row exclude column row(first row), field start at 0
        start_row, start_col = 1, 0
        col_list = df.columns.to_list()
        #
        for col in range(num_cols):
            # write column row with styles
            worksheet.write(0, col + start_col, col_list[col], styles["col"])
            # write other rows with styles
            for row in range(num_rows):
                # index fields in row
                if col < index_len:
                        worksheet.write(row + start_row, col + start_col, df.iloc[row, col], styles["index"])
                        continue
                # value fields in row
                if pd.notna(df.iloc[row, col]):
                    val = df.iloc[row, col]
                    if "/" in str(val):
                        cell_color = self._cell_color(fieldname=f"{sheetname}.{col_list[col]}", valstr=val)
                        if cell_color not in styles:
                            styles[cell_color] = workbook.add_format({'align': 'left', 'border': 1, 'bg_color': cell_color})
                        worksheet.write(row + start_row, col + start_col, df.iloc[row, col], styles[cell_color])
                    else:
                        worksheet.write(row + start_row, col + start_col, df.iloc[row, col], styles['value'])
                else:
                    worksheet.write(row + start_row, col + start_col, "", styles['value'])


    def _cell_color(self, fieldname, valstr: str):
        values = [float(val.strip()) for val in valstr.split("/") if valstr.strip() and Tool.is_float(val.strip())]
        if len(values) < 2:
            return Color.WHITE
        if not self.comparator:
            return Color.WHITE
        #
        result = self.comparator(fieldname=fieldname, val1=values[0], val2=values[-1])
        if result == self.comparator.UNCHANGE:
            return Color.WHITE
        elif result == self.comparator.BETTER:
            return Color.GREEN
        elif result == self.comparator.WORSE:
            return Color.RED
        else:
            return Color.WHITE


    def _shape_table(self, worksheet, df: pd.DataFrame):
        # Set an appropriate header height.
        worksheet.set_row(0, 20)
        # Dynamically adjust the column widths based on the maximum length of each column.
        for i, column in enumerate(df.columns):
            # Obtain the length of the column names.
            max_length = len(str(column))
            # Determine the maximum length of all the data within the column.
            for item in df[column]:
                max_length = max(max_length, len(str(item)))
            # Set the column width, adding an additional space of 2.
            worksheet.set_column(i, i, max_length + 2)



def check(log_cls: BaseLog, log_path, stat_func=["mean"], head_offset=0, tail_offset=0, decimals=3, **kwargs):
    obj = log_cls(log_path=log_path)
    print("filted by filter".center(100, "="))
    print(Tool.df2string(obj.get_rows()))
    print("analyzed by analyst".center(100, "="))
    print(Tool.df2string(obj.analyze()))
    print()
    print("statistial data calculated by statistician".center(100, "="))
    print(Tool.df2string(obj.calculate(stat_func=stat_func, head_offset=head_offset, tail_offset=tail_offset,
                                       decimals=decimals, **kwargs)))
