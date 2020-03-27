import functools
from datetime import datetime
import platform
import subprocess

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('sysinfo', __name__, url_prefix='/sysinfo')

@bp.route('/')
def index():
    sys_data = {"current_time": '',"machine_name": ''}
    try:
        sys_data['current_time'] = datetime.now().strftime("%d-%b-%Y , %I : %M : %S %p")
        sys_data['machine_name'] =  platform.node()
    except Exception as ex:
        print(ex)
    finally:
        return render_template("sysinfo/info.html", title='Raspberry Pi - System Information',
                                sys_data = sys_data)

def cpu_generic_details():
    try:
        items = [s.split('\t: ') for s in subprocess.check_output(["cat /proc/cpuinfo  | grep 'model name\|Hardware\|Serial' | uniq "], shell=True).splitlines()]
    except Exception as ex:
        print(ex)
    finally:
        return dict(cpu_genric_info = items)
 
@bp.context_processor
def boot_info():
    item = {'start_time': 'Na','running_since':'Na'}
    try:
        item['running_duration'] = subprocess.check_output(['uptime -p'], shell=True).decode("utf-8")
        item['start_time'] = subprocess.check_output(['uptime -s'], shell=True).decode("utf-8")
    except Exception as ex:
        print(ex)
    finally:
        return dict(boot_info = item)


@bp.context_processor
def os_name():
    os_info = subprocess.check_output("cat /etc/*-release | grep PRETTY_NAME | cut -d= -f2", shell=True).decode('utf-8')
    return dict(os_name=os_info)

@bp.context_processor
def memory_usage_info():
    try:
        item = {
         'total': 0,
         'used': 0,
         'available': 0
        }
        item['total'] = subprocess.check_output(["free -m -t | awk 'NR==2' | awk '{print $2'}"], shell = True).decode('utf-8')
        item['used'] = subprocess.check_output(["free -m -t | awk 'NR==3' | awk '{print $3'}"], shell = True).decode('utf-8')
        item['available'] = int(item['total']) - int(item['used'])
    except Exception as ex:
        print(ex)
    finally:
        return dict(memory_usage_info = item)
    
@bp.context_processor
def cpu_usage_info():
    item = {
        'in_use': 0
    }
    try:
        item['in_use'] = subprocess.check_output("top -b -n2 | grep 'Cpu(s)'|tail -n 1 | awk '{print $2 + $4 }'", shell = True).decode("utf-8")
    except Exception as ex:
        print(ex)
    finally:
        return dict(cpu_usage_info = item)

@bp.context_processor
def cpu_processor_count():
    proc_info = subprocess.check_output("nproc", shell = True).decode("utf-8").replace('\"', '')
    return dict(cpu_processor_count = proc_info)

@bp.context_processor
def cpu_core_frequency():
    core_frequency = subprocess.check_output("vcgencmd get_config arm_freq | cut -d= -f2", shell = True).decode("utf-8").replace('\"', '')
    return dict(cpu_core_frequency = core_frequency)

@bp.context_processor
def cpu_core_volt():
    core_volt = subprocess.check_output("vcgencmd measure_volts| cut -d= -f2", shell = True).decode("utf-8").replace('\"', '')
    return dict(cpu_core_volt = core_volt)

@bp.context_processor
def cpu_temperature():
    cpuInfo = {
        'temperature': 0,
        'color': 'white'
    }
    try:
        cpuTemp = float(subprocess.check_output(["vcgencmd measure_temp"], shell = True).split('=')[1].split('\'')[0])
        cpuInfo['temperature'] = cpuTemp
        
        if cpuTemp > 40 and cpuTemp < 50:
            cpuInfo['color'] = 'orange'
        elif cpuTemp > 50:
            cpuInfo['color'] = 'red'
        
        return cpuInfo
    except Exception as ex:
        print(ex)
    finally:
        return dict(cpu_temperature = cpuInfo)

@bp.context_processor
def disk_usage_list():
    try:
        items = [s.split() for s in subprocess.check_output(['df', '-h'], universal_newlines = True).splitlines()]
    except Exception as ex:
        print(ex)
    finally:
        return dict(disk_usage_info = items[1: ])

@bp.context_processor
def running_process_list():
    try:
        items = [s.split() for s in subprocess.check_output(["ps -Ao user,pid,pcpu,pmem,comm,lstart --sort=-pcpu"], shell = True, universal_newlines = True).splitlines()]
    except Exception as ex:
        print(ex)
    finally:
        return dict(running_process_info = items[1: ])

@bp.context_processor
def utility_processor():
    def short_date(a, b, c):
        return u'{0}{1}, {2}'.format(a, b, c)
    return dict(short_date = short_date)
