### 框架说明

py_framework开发框架，参照spring boot项目开发框架进行设计，重点提升python开发的便捷性和规范性。

### 重点功能

* 多环境配置支持。bootstrap.yml定义项目共享配置，根据不同的环境加载不同的配置文件：application-[环境].yml。
* 流式数据处理。通过json文件自定义数据处理流程，基于pandas完成多流程数据共享和存储，支持：jdbc数据、pandas、llm和自定义扩展函数。
* WEB框架支持。在python函数添加post_mapping或get_mapping，实现函数到web接口动态映射。

### 启动py应用

* 入口函数 : from py_framework.py_application import PyApplication
* module_scans([sys.modules[\__name__]]) : 扫描所有py文件。检查py语法、导入注解函数。例如：自动导入包含post_mapping的注解。
* .root_dir(os.path.abspath('.')) : 声明作业目录。用于加载配置文件等操作。
* .run_fn([fn]) : 启动运行函数。fn:为import的函数。
* .enable_web(True) : 是否启用web接口服务。默认读取：application.web下的web配置。
* .start() : 启动服务。

### 新建项目结构

* 项目结构参考如下：
  ![img.png](assets/py_structrue.png)
* docker : python项目打包目录
    * build_docker.sh : 打包脚本。 构建打包内容，执行docker打包。
    * Dockerfile : 镜像构建。安装requirements.txt、添加项目代码、启动运行脚本。
    * requirements.txt : 项目依赖。 使用pip安装需要的格式，例如：py_rtf_framework==1.1.3
    * start-py.sh : python项目启动脚本。 根据项目类型配置，主要包括两类：非WEB项目 和 WEB项目，其中WEB项目使用gunicorn启动服务代理，
      非WEB项目使用安装的python解释器运行脚本，例如：/opt/conda/envs/default/bin/python xxx.py 。
* src : 项目源码目录。包括三类文件：项目入口文件、yml配置文件和模块代码。
    * 项目入口文件，即在启动时需要指定的py脚本。需要放到src根目录下。
    * yml配置文件，包括：bootstrap.yml、application-[env].yml。
    * 模块代码，即：创建python代码包。将模块代码文件放到其中。

### 定时任务配置

* 使用基于cron表达式配置定时任务。
* 引入：from py_framework.schedule.job_scheduler import scheduled
* 配置：@scheduled('1/2 0/1 * * * ?')

### SQL默认参数

* 使用verb:jdbc_query执行数据查询，支持使用input:DataFrame中列作为参数，同时系统将时间作为默认参数加入。
* 使用input:DataFrame中列作为参数，需配置："input_as_param": true
* sql支持参数化直接替换，两种格式：${参数名}和#{参数名}，区别为：#{参数名}替换参数值带单引号。
* 系统默认参数名称：
  * sys_date：当前日期，例如：2024-08-21
  * sys_datetime：当前时间，例如：2024-08-21 14:22:22
  * sys_datetime_min：当天时间最小值，例如：2024-08-21 00:00:00
  * sys_datetime_max：当天时间最大值，例如：2024-08-21 23:59:59
  * last_date：昨天日期，例如：2024-08-20
  * last_datetime：昨天时间，例如：2024-08-20 14:22:22
  * last_datetime_min：昨天时间最小值，例如：2024-08-20 00:00:00
  * last_datetime_max：昨天时间最大值，例如：2024-08-20 23:59:59