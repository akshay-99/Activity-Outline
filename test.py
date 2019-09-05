import subprocess
import csv
import datetime
import os

def get_current_data():
    
    xid_proc = subprocess.Popen("xprop -root 32x '\t$0' _NET_ACTIVE_WINDOW | cut -f 2", shell=True, stdout=subprocess.PIPE).stdout
    xid = xid_proc.read().decode().split('\n')[0]

    data_proc = subprocess.Popen(f"xprop -id {xid} _NET_WM_NAME _NET_WM_PID WM_CLASS _NET_WM_USER_TIME", shell=True, stdout=subprocess.PIPE).stdout
    data_str = data_proc.read().decode().split('\n')

    data = {'xid': xid, 'date': datetime.datetime.now()}
    for d in data_str:
        if d:
            
            kv = d.split('=') if '=' in d else d.split(':')
            key = kv[0].strip()
            value = kv[1].strip()
            data[key] = value.replace('"', '')

    

    pid = int(data['_NET_WM_PID(CARDINAL)'])
    cmd_proc = subprocess.Popen(f"ps -p {pid} -o comm=", shell=True, stdout=subprocess.PIPE).stdout
    data['cmd'] = cmd_proc.read().decode().split('\n')[0]
    return data 

def append_row(filename, data):
    
    row = [data['date'], data['xid'], data['_NET_WM_PID(CARDINAL)'], data['_NET_WM_NAME(UTF8_STRING)'], data['cmd'], data.get('_NET_WM_USER_TIME(CARDINAL)', None)]
    
    today = datetime.datetime.now().strftime("%m-%d-%Y")
    csv_dir_name = 'csv_data'
    script_path = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists( os.path.join( script_path, csv_dir_name) ):
        os.mkdir( os.path.join( script_path, csv_dir_name) )
    filepath = os.path.join( script_path, csv_dir_name, f'{filename}-{today}.csv' )

    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow(['Date', 'xid', 'pid', 'title', 'process', 'timeactive'])

    with open(filepath, 'a') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerow(row)

if __name__ == '__main__':
    data = get_current_data()
    append_row('watch', data)

