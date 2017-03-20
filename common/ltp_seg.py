#! /bin/python
# coding=utf8

import sys, os, re
from pyltp import Segmentor


class ltp:
    def __init__(self):
        self.segmentor = Segmentor()
        self.segmentor.load("/home/gwlin/extend/data/program/gen-lda-data/pyltp/ltp_data/cws.model")

    def __del__(self):
        self.segmentor.release()

    def seg_text(self, text):
        words = self.segmentor.segment(text)
        return words