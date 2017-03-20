# coding=utf8

import sys, json, os
import threading
from search_files import lucene_rank


def searchOne(line):
    global luc_inst
    jsonobj = json.loads(line)
    query_file_name = jsonobj["file_name"]
    query_desc = jsonobj["description"].encode("utf8")
    doc_list = luc_inst.search_full(query_desc, top_n)
    one_record = query_file_name + ' ' + ' '.join(doc_list) + '\n'
    return one_record


def threadFunc(line):
    global totalNum, mutex
    # 打印线程名
    threadName = threading.currentThread().getName()
    print "start " + threadName
    one_record = searchOne(line)
    print "threadName: " + str(threadName) + " one_record: " + str(one_record)
    # 取得锁
    mutex.acquire()
    fileout.write(one_record)
    totalNum += 1
    print "totalNum: " + str(totalNum)
    # 释放锁
    mutex.release()
    print "finish " + threadName


def AnalysisWenShuData(zipLists):
    # 定义全局变量
    global totalNum, totalZipFile, mutex
    totalNum = 0
    # 创建锁
    mutex = threading.Lock()
    # 定义线程池
    threads = []
    # 先创建线程对象
    for x in xrange(0, len(zipLists)):
        threads.append(threading.Thread(target=threadFunc, args=(zipLists[x],)))
    # 启动所有线程
    for t in threads:
        t.start()
    # 主线程中等待所有子线程退出
    for t in threads:
        t.join()
    # 打印执行结果
    print "totalNum: " + str(totalNum)


if __name__ == '__main__':
    global luc_inst, fileout
    if len(sys.argv) < 2:
        print "Usage: python search_topn.py input_file top_n"
        sys.exit(1)
    luc_inst = lucene_rank()
    path = os.path.abspath(sys.argv[1])
    top_n = int(sys.argv[2])
    file = open(path, 'r')
    print top_n
    print path
    lines = file.readlines()
    file.close()

    threaNum = 32
    lineNum = len(lines)
    N = lineNum / threaNum + 1
    if lineNum % threaNum == 0:
        N = lineNum / threaNum
    zipLists = [lines[i:i + N] for i in range(0, lineNum, N)]
    if threaNum > len(zipLists):
        threaNum = len(zipLists)
    AnalysisWenShuData(zipLists)
    fileout.close()