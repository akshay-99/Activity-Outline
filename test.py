# Example Format
# _NET_WM_STATE(ATOM) = _NET_WM_STATE_FOCUSED
# WM_STATE(WM_STATE):
#                 window state: Normal
#                 icon window: 0x0
# _NET_WM_DESKTOP(CARDINAL) = 0
# _GTK_EDGE_CONSTRAINTS(CARDINAL) = 170
# _NET_FRAME_EXTENTS(CARDINAL) = 0, 0, 37, 0
# _NET_WM_ALLOWED_ACTIONS(ATOM) = _NET_WM_ACTION_MOVE, _NET_WM_ACTION_RESIZE, _NET_WM_ACTION_FULLSCREEN, _NET_WM_ACTION_MINIMIZE, _NET_WM_ACTION_SHADE, _NET_WM_ACTION_MAXIMIZE_HORZ, _NET_WM_ACTION_MAXIMIZE_VERT, _NET_WM_ACTION_CHANGE_DESKTOP, _NET_WM_ACTION_CLOSE, _NET_WM_ACTION_ABOVE, _NET_WM_ACTION_BELOW
# _NET_WM_USER_TIME(CARDINAL) = 5129473
# WM_NORMAL_HINTS(WM_SIZE_HINTS):
#                 program specified location: 483, 169
#                 program specified minimum size: 200 by 120
# _NET_WM_ICON(CARDINAL) = 
# WM_NAME(UTF8_STRING) = "test.py - productivity - Visual Studio Code"
# _NET_WM_NAME(UTF8_STRING) = "test.py - productivity - Visual Studio Code"
# XdndAware(ATOM) = BITMAP
# _MOTIF_WM_HINTS(_MOTIF_WM_HINTS) = 0x2, 0x0, 0x1, 0x0, 0x0
# _NET_WM_BYPASS_COMPOSITOR(CARDINAL) = 2
# WM_WINDOW_ROLE(STRING) = "browser-window"
# WM_CLASS(STRING) = "code", "Code"
# _NET_WM_WINDOW_TYPE(ATOM) = _NET_WM_WINDOW_TYPE_NORMAL
# _NET_WM_PID(CARDINAL) = 19051
# WM_LOCALE_NAME(STRING) = "en_IN"
# WM_CLIENT_MACHINE(STRING) = "akshay-HP-Pavilion-Laptop-15-cc1xx"
# WM_PROTOCOLS(ATOM): protocols  WM_DELETE_WINDOW, _NET_WM_PING

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

    print(script_path)

    if not os.path.exists( os.path.join( script_path, csv_dir_name) ):
        os.mkdir( os.path.join( script_path, csv_dir_name) )
    filepath = os.path.join( script_path, csv_dir_name, f'{filename}-{today}.csv' )

    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow(['Date', 'xid', 'pid', 'title', 'cmd', 'usertime'])

    with open(filepath, 'a') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerow(row)

if __name__ == '__main__':
    data = get_current_data()
    append_row('watch', data)

