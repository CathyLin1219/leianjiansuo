#!/usr/bin/env python
# coding=utf8

import sys, os, lucene

from java.nio.file import Paths
from org.apache.lucene.analysis.cn.smart import SmartChineseAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from common import path_define

"""
This script is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""
def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class lucene_rank:
    def __init__(self):
        lucene.initVM(vmargs=['-Djava.awt.headless=true'])
        lucene.getVMEnv().attachCurrentThread()
        directory = SimpleFSDirectory(Paths.get(path_define.INDEX_DIR))
        self.searcher = IndexSearcher(DirectoryReader.open(directory))
        self.analyzer = SmartChineseAnalyzer()

    def do_search(self, query_text, top_n):
        lucene.getVMEnv().attachCurrentThread()
        query = QueryParser("description", self.analyzer).parse(query_text)
        scoreDocs = self.searcher.search(query, top_n).scoreDocs
        return scoreDocs

    def search_full(self, query_text, top_n=20):
        """
        返回最全的搜索信息，标题、描述、罪名等
        使用：
        for i, title, description, criminal_name, sentenced_time, money, province, court, file_name, score in rst_docs:
            blablabla......
        :param query_text: 待搜索的query文本
        :param top_n: 搜索前n个相似结果
        :return: top n 的列表，每一个元素为(index, title, description, criminal_name, sentenced_time, money, province, court, file_name, score) 可根据需要使用部分内容
        """
        scoreDocs = self.do_search(query_text, top_n)
        i = 0
        rst_docs=[]
        for scoreDoc in scoreDocs:
            i = i + 1
            doc = self.searcher.doc(scoreDoc.doc)
            rst_docs.append((i, doc.get("title"), doc.get("description").replace(" ", ""),
            doc.get("criminal_name"), doc.get("sentenced_time"), doc.get("money"),
            doc.get("province"), doc.get("court"), doc.get("file_name"), scoreDoc.score))
        return rst_docs

    def search_as_dict(self, query_text, top_n):
        """
        返回简单信息，文件名及得分——字典
        :param query_text: 待搜索的query文本
        :param top_n: 搜索前n个相似结果
        :return: 字典，key：文件名， value:得分
        """
        scoreDocs = self.do_search(query_text, top_n)
        rst_dict = {}
        rst_elems = {}
        for scoreDoc in scoreDocs:
            doc = self.searcher.doc(scoreDoc.doc)
            rst_dict[doc.get("file_name")] = scoreDoc.score
            # 以下要素 --20170526
            rst_doc = {}
            rst_doc['surrender'] = doc.get("surrender")
            rst_doc['age_group'] = doc.get("age_group")
            rst_doc['reconciliation'] = doc.get("reconciliation")
            rst_doc['attempt'] = doc.get("attempt")
            rst_doc['meritorious'] = doc.get("meritorious")
            rst_doc['repetitious_theft'] = doc.get("repetitious_theft")
            rst_doc['restitution'] = doc.get("restitution")
            rst_doc['burglary'] = doc.get("burglary")
            rst_doc['pickpocket'] = doc.get("pickpocket")
            rst_doc['money_group'] = doc.get("money_group")
            rst_doc['amount_of_theft'] = doc.get("amount_of_theft")

            rst_elems[doc.get("file_name")] = rst_doc
        return rst_dict, rst_elems
