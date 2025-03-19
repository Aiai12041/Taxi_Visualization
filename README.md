项目运行步骤
1、安装elasticsearch-8.17.0 kibana-8.17.0
2、使用kibana dev tool 按照"索引创建.txt"的代码创建索引
3、运行identify_od.py完成从txt到od的转换（也可以直接使用final_od.csv跳过该步骤）
4、运行adddata.py完成数据导入es
5、在终端进入big-screen-visualization文件夹运行 node server.cjs
6、在终端运行npm run dev（可能需要按照提示安装依赖）
7、进入生成的localhost网址
