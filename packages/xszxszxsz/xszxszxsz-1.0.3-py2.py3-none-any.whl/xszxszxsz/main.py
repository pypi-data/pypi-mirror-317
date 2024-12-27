

def one():
        print("这个是第一题")
        print(
            "import matplotlib.pyplot as plt\nimport numpy as np\nx=np.linspace(-1,1,400)\ny=x**2\nplt.Figure(figsize=(8,6))\nplt.plot(x,y,linewidth=1,color='green')\nplt.xlim([-1,1])\nplt.ylim([0,3])\nplt.xticks(np.arange(-1,1.5,0.5))\nplt.yticks(np.arange(0,3.5,0.5))\nplt.xlabel('this is x')\nplt.ylabel('this is y')\nplt.grid(True)\nplt.show()\n")


def two():
    print("#这个是清华园导入，在cmd输入的# pip install -1 https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/ pandas")
    print("import pandas as pd\ndf=pd.read_csv('source.csv')\ndf['项目'].replace("",None)\nclean_gender_df=df.loc[df['项目'].isin(['乒乓球','羽毛球'])]\nclean_data=df.loc[df['年龄']>=55]\ndf1=clean_data.loc[df['项目']=='乒乓球']\ndf2=clean_data.loc[df['项目']=='羽毛球']\ndf1.to_csv('out1.csv',index=False,encoding='utf-8')\ndf2.to_csv('out2.csv',index=False,encoding='utf-8')\n")

def three():
        print("这个是第三题")
        print("import pandas as pd\nimport matplotlib.pyplot as plt\ndata=pd.read_excel('book_sale.xls',nrows=10)\nplt.rcParams['font.sans-serif']=['SimHei']\nplt.plot(data['月份'],data['数据挖掘\n(单位：万册）'],label='数据挖掘')\nplt.plot(data['月份'],data['计算机组成原理\n(单位：万册）'],label='计算机组成原理')\nplt.plot(data['月份'],data['数据库\n(单位：万册）'],label='数据库')\nplt.legend()\nplt.ylabel('销量（万册）')\nplt.show()\n")

def four():
        print("这个是写在vscode上的别搞错了")
        print("# <!DOCTYPE html>\n# <html lang= 'en' >\n#     <head>\n#         <script src='lib/echarts.min.js'></script>\n#     </head>\n#     <body>\n#         <div style='width:600px;height:400px'></div>\n#         <script>\n#             var mCharts = echarts.init(document.querySelector('div'))\n#             var option = {\n#                 series:[\n#                 {\n#\n#                     type :'pie',\n#                     data :[\n#                         {name:'优秀',value:2},\n#                         {name:'良好'',value:14},\n#                         {name: '一般',value:4},\n#                         {name:'及格', value:4},\n#                         {name:'不及格', value:4}\n#                     ]\n#                 }\n#             ]\n#         }\n#         mCharts.setOption(option)//一定注意这个O必须大写否则无法识别函数，出不来图\n#         </script>\n#     </body>\n#     </html>\n")
def test_print():
    print("我还是想说，这个考试真的愚蠢")


if __name__ == '__main__':
    test_print()
    one()
    two()
    three()
    four()
