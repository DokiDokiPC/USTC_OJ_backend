from utils import *
problem_info = "id=2002 name=测试问题 level=Easy ac_num=2 submit_num=10 description=输入两个数字a和b输出a+b " \
               "description=两个数字由空格分割每行一组一个数字为输入的两个数字的和每行一组 time_limit=1000 " \
               "memory_limit=10 "

post("problems/", problem_info)
