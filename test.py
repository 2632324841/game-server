import requests,os
from common.cache import create_cache
import time,zipfile
from threading import Thread
import patoolib

server_path = os.getcwd()
steamcmd_path = os.path.join(server_path, 'steamcmd')
if os.path.isdir(steamcmd_path) == False:
    os.mkdir(steamcmd_path)
cacha = create_cache('file')
import subprocess

def run_non_blocking_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)

    # 使用 poll() 来检查进程是否结束
    while process.poll() is None:
        # 读取命令的输出
        output = process.stdout.readline()
        if output:
            #print(output.strip())
            cacha.set('init_steamcmd', output.strip())

    # 获取命令的最后输出
    final_output, _ = process.communicate()
    if final_output:
        cacha.set('init_steamcmd', final_output.strip())
        print(final_output.strip())

t = Thread(target=run_non_blocking_command, args=(os.path.join(steamcmd_path, 'steamcmd')))  # 创建线程
t.name = 'cmd'
t.start()  # 启动线程

while True:
    time.sleep(1)
    
