# coding=utf-8
import ctypes
import os
import sys

dir_name, _ = os.path.split(os.path.abspath(__file__))

# 加载 C lib
lib = ctypes.cdll.LoadLibrary(dir_name + "/libstr_print.so")

# 接口参数类型映射
lib.str_print.argtypes = [ctypes.c_char_p]
lib.str_print.restype = None


def str_print(text):
    # 调用接口
    lib.str_print(text.encode())
