import os

def main():
    if os.name == 'nt':
        os.system(f'"{os.path.abspath(os.path.dirname(__file__))}/androidMonitor-v1.1.exe"')
    else:
        print('此功能目前只Windows系统，支持其它系统暂不支持~')

if __name__ == '__main__':
    main()