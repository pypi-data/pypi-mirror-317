import pandas as pd
import logging
import logging.config
from functools import reduce
import quopri
import os.path
import pathlib
import argparse

# 加载配置文件
logging.config.fileConfig('./app.ini')
logger = logging.getLogger()

# 所有使用字段
fieldsname = ['姓名','单位','职务','电话1','电话2']
example = {
    '姓名':'飞流',
    '单位':'银行',
    '职务':'主管',
    '电话1':'1234',
    '电话2':"222"
}

# 定义一个函数用于生成vCard格式文本
# param: 姓名、职务、单位、电话1、电话2
def _generatevcard(info):
    # 检查：不能有换行，否则报错
    def validate(e):
        for k, v in e.items():
            if k in fieldsname and '\n' in v:
                raise ValueError(f"姓名为 {e['姓名']}的 {k} 字段数据存在换行，请检查并移除！")
    # 中文quotedPrintable编码
    def encodeMy(info):
        # 对姓名、单位、职务等中文进行quotedprintable编码
        for e in ['姓名','单位','职务']:
            info[e] = ";ENCODING=QUOTED-PRINTABLE:"+ str(quopri.encodestring(info[e].encode('utf8'), quotetabs=True),encoding='ascii')
    validate(info)
    encodeMy(info)
    # 姓名
    vcard_template = f"BEGIN:VCARD\r\nVERSION:3.0\r\nFN{info['姓名']}"
    # 电话
    if '电话1' in info and len(info['电话1']) > 0 and not info['电话1'].isspace():
        vcard_template += "\r\nTEL;VALUE=uri;TYPE=cell:{}".format(info['电话1'])
    if '电话2' in info and len(info['电话2']) > 0 and not info['电话2'].isspace():
        vcard_template += "\r\nTEL;VALUE=uri;PREF=1;TYPE=cell:{}".format(info['电话2'])
    # 职务
    vcard_template += "\r\nTITLE{}".format(info['职务'])
    # 单位
    vcard_template += "\r\nORG;TYPE=work{}".format(info['单位'])
    vcard_template += "\r\nEND:VCARD"
    return vcard_template

# 读取文件，返回列表
# 参数:directory(目录)、encoding(编码方式，默认utf8)
# 格式： ['姓名','职务','单位','电话1','电话2']
def _readfromexcel(directory, encoding='utf-8'):
    with open(directory, 'r') as csvfile:
        logger.info(f"正读取excel：{directory}")
        df = pd.read_excel(directory, usecols=fieldsname).fillna('').astype(str)
        rows = df.to_dict(orient='records')

    for index, item in enumerate(rows):
        logger.debug(f"第{index+1}行：{item}")
    logger.info(f"读取完成，共{len(rows)}条")
    return rows

# 生成vcf文件
# excelin: 输入excel文件。表头为 ['姓名','职务','单位','电话1','电话2']
# vcfout:  输出vcf文件
# batch_size: 输出vcf文件中的联系人最大数量
def excel2vcf(vcfout,excelin, batch_size=300):
    rows = _readfromexcel(excelin)
        
    outname, ext = os.path.splitext(vcfout)
    # 分批处理
    for index, batch in enumerate([rows[i:i + batch_size] for i in range(0, len(rows), batch_size)]):
        vcf = '\r\n'.join(map(_generatevcard, batch))
        with open(outname+"_"+str(index)+ext, 'w', encoding='utf-8') as file_obj:
            file_obj.write(vcf)
    logger.info(f"导出vcf完成") 


def main():
    parser = argparse.ArgumentParser(prog='excel2vcf', description="将 excel 文件转化成 vcard 格式文件。注意excel的内容里不要有换行！")
    parser.add_argument('out_vcf', type=pathlib.Path, help='生成联系人vcf文件的输出路径')
    parser.add_argument('in_excel', type=pathlib.Path, help='联系人excel文件的输入路径。表头包含姓名,单位,职务,电话1,电话2等字段')
    ns = parser.parse_args()

    if not os.path.exists(ns.in_excel):
        logger.error(f"{ns.in_excel} 文件不存在!")

    excel2vcf(ns.out_vcf, ns.in_excel)

if __name__ == '__main__':
    maim()