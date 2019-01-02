#!/usr/bin/python
#coding=utf-8
import re
import sys
import time
import MySQLdb
canshu=len(sys.argv)
def help():
    print "分析当天慢日志执行命令python %s today today" %sys.argv[0]
    print "分析以前慢日志执行命令python %s before 日志名字" %sys.argv[0]
def create_table():
    db=MySQLdb.connect("127.0.0.1","zjz","111111","test")
    cursor=db.cursor()
    cursor.execute("DROP TABLE IF EXISTS `mysql_slow_log`;")
    sql="""CREATE TABLE `mysql_slow_log` (
      `id` int(11)  unsigned NOT NULL AUTO_INCREMENT,
      `IP` varchar(15) NOT NULL,
      `Query_time` float(11,6) NOT NULL,
      `Lock_time` char(11) NOT NULL,
      `Rows_sent` int(11) NOT NULL,
      `Rows_examined` int(11) NOT NULL,
      `sql_time` datetime NOT NULL,
      `slow_sql` text NOT NULL,
      PRIMARY KEY (`id`),
      KEY `Query_time` (`Query_time`),
      KEY `Rows_examined` (`Rows_examined`),
      KEY `sql_time` (`sql_time`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
    cursor.execute(sql)
    db.close()
def insert_table():
    log_file=open(log_name)
    db=MySQLdb.connect("127.0.0.1","zjz","111111","test")
    cursor = db.cursor()
    content=''
    for line in log_file.readlines(): #把日志文件一次性读入内存，以列表方式显示
        line=line.strip('\n') #删除空白行回车
        content =content+line #添加到coneent默认文本
    re_mysql = re.findall('@\s+\[(.*?)\]#.*?Query_time: (.*?) Lock_time: (.*?) Rows_sent: (.*?)  Rows_examined: (.*?) Rows_affected: (.*?)  Rows_read: (.*?)#.*?timestamp=(.*?);(.*?);',content,re.I);  #具体匹配慢日志需要的参数,re.I忽略大小写
    for record in re_mysql:
           IP=record[0].strip()
           Query_time=record[1].strip()
           Lock_time=record[2].strip()
           Rows_sent=record[3].strip()
           Rows_examined=record[4].strip()
           timestamp=int(record[7])
           timeArray=time.localtime(timestamp)
           sql_time=time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
           slow_sql=record[8].strip()
           set_charset="set names utf8"
           sql = """INSERT INTO mysql_slow_log(IP,Query_time,Lock_time,Rows_sent,Rows_examined,sql_time,slow_sql)
                VALUES ('"""+IP+"""',"""+Query_time+""",'"""+Lock_time+"""',"""+Rows_sent+""","""+Rows_examined+""",'"""+sql_time+"""',\""""+slow_sql+"""\;\")""";
           try:
               cursor.execute(set_charset)
               cursor.execute(sql)
               print sql
               db.commit()
           except:
               db.rollback()
    log_file.close()
    db.close()
def main():
    global log_name
    if canshu!=3:
       print "参数数量错误,请检查!"
       help()
    else:
       create_table()
       xuanze=sys.argv[1]   #第一个参数(慢日志时间)
       log_before=sys.argv[2] #慢日志具体时间
       if xuanze=='today':
            log_name='/home/mysql-slow_query.log'
            import pdb;pdb.set_trace()
            insert_table()
       elif xuanze=='before':
            log_name='/home/%s' %log_before
            insert_table()
       else:
            print '参数类型选择错误,类型只包含today|before'
            help()
main()
