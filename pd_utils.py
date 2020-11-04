import pandas as pd
import numpy as np


def create_df():
    # 生成时间序列
    dates = pd.date_range('20160101', periods=6)
    # index相当于索引参考数据库中的索引，即行。
    # 生成DataFrame的第一种方式：通过np来生成
    df1 = pd.DataFrame(np.random.randn(6,4), index=dates, columns=['A','B','C','D'])

    # 通过数组创建
    arr = [0, 1, 2, 3, 4]
    df2 = pd.Series(arr) # 如果不指定索引，则默认从 0 开始


    # 生成DataFrame的第二种方式：通过字典生成
    df3 =pd.DataFrame({'A' : 1.,
                       'B' : pd.Timestamp('20130102'),
                       'C' : pd.Series(1,index=list(range(4)),dtype='float32'),
                       'D' : np.array([3] * 4,dtype='int32'),
                       'E' : pd.Categorical(["test","train","test","train"]), # 将类别信息转化成数值信息
                       'F' : 'foo'})
    return df1, df2, df3

def select_df(df1, df2, df3):
    # df['A']与df.A选择列是等效的
    print(df3['A'], df3.A)  # 选中列名

    # select by label: loc
    print(df3.loc[:, ["A", "B"]])
    print(df3[["A", "B"]])

    # 选择行也是等效的。注意[0:3)是左闭(包含)右开（开除）
    print(df1[0:3])
    print(df1['20160101':'20160103'])  # 选中行号

    # select by position: iloc
    # 前三行数据
    print(df3.iloc[0:3])
    # 方法二
    print(df3.head(3))

    # 结合前面两种选择数据的方法：即按标签和位置选择数据
    # mixed selection: ix(已移除)
    # 第1-3行、A和C列的数据
    print(df3.loc[:3, ['A', 'C']])

    # Boolean indexing
    # 选择df中A列表大于0的所有的行数据
    print(df3[df3["A"] > 0])

def set_value_df(df3):
    df3['F'] = np.nan
    print(df3)

def process_nan_df(df3):
    # 剔除df中有Nan的行(也可单独对某一列进行处理)
    # print(df3.dropna(axis=0, how='any'))
    # how={'any', 'all'}：any有一个Nan即剔除；all全部为Nan即剔除。

    # 显示出pd的A列中值是否为Nan；是为True否为False
    print(df3["A"].isnull())
    # 进一步处理
    # 判断pd中是否有nan，有的话返回True，没有的话返回False。any：只要包含一个true则返回true
    print(np.any(pd.isnull(df3)) == True)

    # 将Nan值填充为0
    df3['F'].fillna(value=0,inplace=True)
    print(df3)

def concat_df(df1, df2, df3):
    # 将三个df进行合并，按行合并，ignore_index：忽略三个df之前的索引
    res = pd.concat([df1, df2, df3], axis=0, ignore_index=True)
    print(res)
    # 参考SQL的join操作：outer join
    res = pd.concat([df2, df3], axis=1, join='outer')
    print(res)
    # inner join：理解为将两个df的index作为连接条件进行join
    res = pd.concat([df2, df3], axis=1, join='inner')
    print(res)
    # # 默认向下追加数据
    res = df1.append(df3, ignore_index=True)
    print(res)

def merge_df(df1, df2, df3):
    # merging two df by key/keys. (may be used in database)
    res = pd.merge(df1, df3, on='A')
    # consider two keys
    # default for how='inner'：即取交集,'outer’取并集.
    # how = ['left', 'right', 'outer', 'inner']
    res = pd.merge(df1, df3, on=['A', 'C'], how='inner')

    # indicator：将join的具体信息显示出来即怎么进行merge。
    res = pd.merge(df1, df3, on='A', how='outer', indicator=True)
    # 通过对比index来进行join操作
    # left_index and right_index
    res = pd.merge(df1, df3, left_index=True, right_index=True, how='outer')

def read_csv_pd(info_path):
    names = ["city_code", "city_name", "district_code", "district_name", "bizcircle_id", "bizcircle_name",
             "resblock_id", "resblock_name", "year", "month", "district_refer_price", "district_trans_amount",
             "bizcircle_refer_price", "bizcircle_trans_amount", "resblock_refer_price", "resblock_trans_amount",
             "room_range"]
    # 文件中不包含header的行
    all_info = pd.read_csv(info_path, sep="\t", header=None, names=names)
    # 按城区分组，每组内按照bizcircle_trans_amount降序排列
    district_groupby_bizcircle = all_info.groupby("district_code").apply(
        lambda x: x.sort_values("bizcircle_trans_amount", ascending=False))
    beijing = all_info[all_info['city_code'].isin(["110000"])]
    # df[df['列名'].isin([相应的值])]返回值为一整行的数据。通过index获得索引值


if __name__ == "__main__":
    df1, df2, df3 = create_df()
    # select_df(df1, df2, df3)
    # set_value_df(df3)
    # process_nan_df(df3)
    # concat_df(df1, df2, df3)
    merge_df(df1, df2, df3)
