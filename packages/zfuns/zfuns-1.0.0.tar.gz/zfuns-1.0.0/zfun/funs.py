import base64
import os
import re
from io import BytesIO
from io import StringIO
from pprint import pprint
from time import localtime
from time import strftime

import dash_mantine_components as dmc
import dash_tabulator.DashTabulator as Table
import pandas
import pymysql
import PyPDF2
import requests
import sqlalchemy
import winrm  # pip install pywinrm


def make_dir_force(pathf):
    """如果不存在则创建

    Args:
        pathf (str): 文件夹路径

    Returns:
        str: 返回创建的文件夹的绝对路径
    """
    if not os.path.exists(pathf):
        os.mkdir(pathf)
    return os.path.abspath(pathf)


def make_script(fpath, command, action=None):
    """创建一个可执行的文件。

    Args:
        fpath (str): 文件绝对路径
        s (str): 可执行的命令
    """
    fpath = os.path.abspath(fpath)
    with open(fpath, "w") as f:
        f.write(command + "\n")
    os.system("chmod +x " + fpath)
    if action == "run":
        os.system(fpath)
    if action == "print":
        print(fpath)
    return fpath


def pdf_merger(pdf_list, pdf_out):
    """合并多个pdf

    Args:
        pdf_list (list): 需要合并的PDF路径列表
        pdf_out (str): 合并后的输出路径
    """
    merger = PyPDF2.PdfFileMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(pdf_out)
    merger.close()
    return pdf_out


def pdf_paste(file_marker, file_in, pnum=0, file_out=None):
    """覆盖2个pdf文件。

    Args:
        file_marker (str): 水印文件
        file_main (str): 主文件
        file_out (str): 输出文件
    """
    pdf_watermark = PyPDF2.PdfFileReader(open(file_marker, "rb"))
    pdf_input = PyPDF2.PdfFileReader(file_in)
    pdf_output = PyPDF2.PdfFileWriter()
    pageCount = pdf_input.getNumPages()
    for i in range(pageCount):
        if i - pnum in [0, pageCount]:  # test 负号表示倒数
            page = pdf_input.getPage(i)
            page.mergePage(pdf_watermark.getPage(0))
            page.compressContentStreams()
            pdf_output.addPage(page)
        else:
            pdf_output.addPage(pdf_input.getPage(i))
    if not file_out:
        file_out = file_in
    pdf_output.write(open(file_out, "wb"))


def text_to_range(t, k=4):
    """生产序列文件， 主要用于数据库查询。

    Args:
        t (str): 多行字符串
            1. !ada-3 : 叹号开始表示一个字符串，忽略 -
            2. adab : 没有 - 表示一个字符串
            3. A001-A012 : - 表示范围
        k (int, optional): 末尾多少位是序列. Defaults to 4.

    Returns:
        list: 返回所有的数据
    """
    if not t:
        return "格式不正确"  # todo 必须返回list
    t = t.strip()
    sample_set = []
    for i in t.split("\n"):
        i_line = i.strip().replace("\r", "")
        if i_line[0] == "!" or i_line.count("-") == 0:
            sample_set.append(i_line.replace("!", ""))
            continue
        if i_line.count("-") == 1:
            start, end = i_line.split("-")
            fix_start, fix_end = start[:-k], end[:-k]
            if fix_start != fix_end:
                return "前缀不一致"
            i_start = int(start[-k:])
            i_end = int(end[-k:])
            for j in range(i_start, i_end + 1):
                suffix = str(j + 10**k)[1:]
                sample_set.append(fix_start + suffix)
    return sample_set


def remove_upprintable_chars(s):
    """移除字符串中的不可见字符

    Args:
        s : 字符串
    """

    if s:
        return "".join(x for x in str(s) if x.isprintable())


####### 数据库 ########


class MYSQL:
    """数据库链接"""

    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        engineStr = (
            f"mysql+pymysql://{self.user}:{self.pwd}@{self.host}:3306/{self.db}"
        )
        self.EE = sqlalchemy.create_engine(engineStr)

    def __GetConnect(self):
        if self.db:
            # noinspection PyBroadException
            try:
                self.conn = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.pwd,
                    database=self.db,
                    use_unicode=True,
                    charset="utf8",
                )
            except Exception as e:
                print(e)
                exit("Don't a MySQL or MSSQL database.")
        else:
            exit("No database.")
        cur = self.conn.cursor()
        if not cur:
            exit("Error connect")
        else:
            return cur

    @staticmethod
    def tidy_sql(sql):
        # sql = re.sub(r'\n\s*--sql\s*\n', ' ', sql) # 替换掉注释
        sql = re.sub(r"\s*\n\s*", " ", sql)  # 替换掉换行前后的空白
        return sql

    def exce_query(self, sql):
        """执行查询语句

        Args:
            sql(str) : 一条查询命令

        """
        cur = self.__GetConnect()
        cur.execute(sql)
        res = cur.fetchall()
        res_columns = ([i[0] for i in cur.description],)
        res = res_columns + res  ##res的第0个元素是标题。
        self.conn.close()
        return res

    def exec_nonquery(self, sqlList):
        """执行修改语句

        Args:
            sql (list): 一组修改命令

        Returns:
            str: 成功1, 失败0.
        """
        cur = self.__GetConnect()
        ok = 0
        # noinspection PyBroadException
        try:
            [cur.execute(i) for i in sqlList]
            self.conn.commit()
            ok = 1
        except Exception as e:
            print(e)
            self.conn.rollback()
        self.conn.close()
        return ok

    @staticmethod
    def update_insert_sql(table, column, value):
        """
        table : 'table name'
        column: ['c1','c2','c3']
        value : ["(1,'2','a')","(2,'3','b')"]
        NOTES : `ON DUPLICATE KEY UPDATE`, UNIQUE INDEX is necessary.
        """
        sql_col = [f"`{i}`" for i in column]
        sql_val = ",\n".join(value)
        sql = f"""
            INSERT INTO {table}({','.join([_ for _ in sql_col])}) 
            VALUE  {sql_val}
            ON DUPLICATE KEY UPDATE {','.join([_ + '=VALUES(' + _ + ')' for _ in sql_col])}
        """
        sql = re.sub(r"\s*\n\s*", "\n", sql)  ##tidy
        return sql

    def dataframe_to_db(self, dat, tb):
        """将dataFrame格式数据导入数据库表tb，默认数据库链接。

        Args:
            dat (objct): dataframe
            tb (str):  tb name
            con (object) : 数据库连接

        Returns:
            str: 执行的sql
        """
        dat = dat.fillna("")
        dat = dat.dropna(axis="columns", how="all")
        dat = dat.applymap(lambda x: str(x))
        # 再出数据以前更新DAT列以匹配数据库列
        dbcol = set(self.exce_query(f"SELECT * FROM {tb} LIMIT 1")[0])
        dat = dat[dbcol.intersection(dat.columns)]
        # END
        sqlValue = []
        for _, e in dat.iterrows():
            ival = "('" + e[0] + "','" + "','".join(e[1:]) + "')"
            sqlValue.append(ival)
        sql = self.update_insert_sql(tb, list(dat.columns), sqlValue)
        self.exec_nonquery([sql])
        return sql

    def update_db_by_dataframe(self, dat, table, oncol, keycol, cond="1=1"):
        """数据dat更新到table。

        Args:
            dat (df): pandas 数据表
            table (str): 需要更新到的表名
            keycol (list): 表的关键字列表[index key list]
            ee (object) : 数据库连接方式2
            cond (str): 更新过程指定数据行的条件

        Returns:
            df: 更新到数据库的数据表
        """
        select_col = str(keycol)[1:-1].replace("'", "`")
        sql = f"""
            SELECT {select_col}
            FROM {table}
            WHERE {cond}
        """
        datDB = pandas.read_sql(sql, self.EE)
        datDBdropCol = [
            i for i in datDB.columns if (i not in oncol) and (i in dat.columns)
        ]  # * 依上传表格为准。
        datDB.drop(datDBdropCol, inplace=True, axis=1)
        dat = pandas.merge(dat, datDB, how="left", on=oncol)
        self.dataframe_to_db(dat, table)
        return dat


####### web 工具 ########


def web_post(url, p=None):
    """
    请求url(post), 配合fastapi接口使用。p为列表。

    Args:
        url (url): url
        p (list): 必须是tuple或者list

    Returns:
        requtest object: json
    """
    r = requests.post(url, json=p, headers={"content-type": "application/json"})
    data = r.json()
    return data


def ctx_index(ctx):
    """dash plotly 小功能。获取当前出发的组件的索引。

    Args:
        ctx (object) : dash 对象

    Returns:
        触发组件的位置
    """
    if ctx.triggered_id:
        return [i["id"] for i in ctx.inputs_list].index(ctx.triggered_id)


def web_table(df, export=False, other_opt={}):
    """返回一个前端表格。简单版本。

    Args:
        df (pandas dataframe): 要显示的数据表
        export (bool, optional): 是否显示导出按钮. Defaults to False.
        other_opt (dict, optional): 其他表格控制选项. Defaults to {}.

    Returns:
        dash 组件: 返回dash组件
    """
    opt = {}
    opt["theme"] = "tabulator_simple"
    opt["col"] = {i: {"title": i, "field": i} for i in df.columns}
    opt["data"] = df.to_dict("records")
    opt["cellDblClick"] = True
    opt["options"] = {
        "selectable": False,
        "layout": "fitDataStretch",
        "pagination": "local",
        "paginationSize": 10,
        "paginationSizeSelector": [10, 20, 50, 100],
        "movableColumns": True,
    }
    if export:
        opt["downloadButtonType"] = {
            "css": "btn btn-primary",
            "text": "导出",
            "type": "xlsx",
        }
    # 其他参数的更新
    new_opt = dict(opt, **other_opt)
    for k in new_opt.keys():
        if (
            isinstance(new_opt[k], dict)
            and k in opt
            and isinstance(opt[k], dict)
        ):
            new_opt[k] = dict(new_opt[k], **opt[k])

    # 处理成默认参数
    new_opt["columns"] = list(new_opt["col"].values())
    del new_opt["col"]

    return Table(**new_opt)


def web_doc(notes, showList=True, showlab="展开", hidelab="收起", maxH=0):
    """生成折叠式的注释。

    Args:
        notes (字典): {"使用说明A：":['1','2',...], "使用说明B：":[]}

    Returns:
        dmc折叠组件。
    """

    c = []
    for i, v in notes.items():
        c.append(i)
        if showList:
            c.append(
                dmc.List(
                    [dmc.ListItem(j) for j in v],
                    withPadding="8px",
                    type="ordered",
                )
            )
        else:
            c.extend(v)

    notes = dmc.Spoiler(
        showLabel=showlab,
        hideLabel=hidelab,
        maxHeight=maxH,
        children=c,
    )
    return notes


def dcc_file_save(fc, fn=None, path=None, format="xls", sheet_name=None):
    """保存dccfile控件的文件

    Args:
        fc (bin): dcc file控件的文件内容
        fn (str): dcc file控件的文件名称
        path (str, optional): path不为空输出到文件，否则返回df. Defaults to None.

    Returns:
        多情况: path+fn 或者 pandas.DataFrame
    """
    f_content = fc.encode("utf8").split(b";base64,")[1]  # 读取文件内容。
    f_content = base64.b64decode(f_content)
    if path:
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path + fn, "wb") as f:
            f.write(f_content)
        return path + fn
    if format == "xls":
        df = pandas.read_excel(BytesIO(f_content), sheet_name=sheet_name)
    elif format == "csv":
        df = pandas.read_csv(StringIO(f_content.decode("utf-8")))
    elif format == "tsv":
        df = pandas.read_csv(StringIO(f_content.decode("utf-8")), sep="\t")
    return df


def webTabEdit():
    # todo
    "生产一个可编辑的表格，编辑后可以返回dataFrame"
    ...


if __name__ == "__main__":
    ...
