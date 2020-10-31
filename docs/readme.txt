
1.安装 python3.6 , 不能高于，安装做了版本判断
2.根据文档里面的development-guilde line 进行安装：
  https://www.zipline.io/development-guidelines.html#creating-a-development-environment
  如果是使用这个方式的话，需要source venv/bin/activate 后面才能执行zipline
2.1 官方文档这里使用venv独立环境安装：
$ python3 -m venv venv
$ source venv/bin/activate
$ etc/dev-install

2.2 正式环境中安装：
alias python="/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6"
etc/dev-install中的python修改为Python3
etc/dev-install

安装后加载数据
zipline ingest

3.安装 & 启动 jupyter
pip3 install --upgrade pip
pip3 install jupyter
启动juypter :
在tools创建jupyter目录，然后执行指令启动
/Users/apple/Tools/jupyter
python3 -m IPython notebook

4.在jupyther中使用:
%load_ext zipline
%%zipline --start 2017-1-1 --end 2017-4-20 --capital-base 100000
文档：https://github.com/jiangyongyuan/zipline-1


