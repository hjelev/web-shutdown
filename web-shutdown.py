import platform
import subprocess
import bottle
import re
import time


@bottle.route('/')
def home():
    start_time = time.time()
    operating_system = platform.system().lower()
    if 'linux' in operating_system:
        output1 = subprocess.check_output('ddcutil --display 1 getvcp D6', shell=True).decode()
        output2 = subprocess.check_output('ddcutil --display 2 getvcp D6', shell=True).decode()
        input1 = subprocess.check_output('ddcutil --display 1 getvcp 60', shell=True).decode()
        input2 = subprocess.check_output('ddcutil --display 2 getvcp 60', shell=True).decode()
        monitor1_status = 'On' if 'DPM: On' in output1 else 'Off'
        monitor2_status = 'On' if 'DPM: On' in output2 else 'Off'
        monitor1_input = parse_input_source(input1)
        monitor2_input = parse_input_source(input2)
        cpu_count = subprocess.check_output('lscpu | grep "^CPU(s):"', shell=True).decode().split(':')[1]
        linux_distro = subprocess.check_output('grep PRETTY_NAME /etc/os-release | cut -d\'"\' -f2', shell=True).decode()
        cpu_model = subprocess.check_output('lscpu | grep "Model name"', shell=True).decode().split(':')[1]
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)
        return f'''
            <h1>Control your {platform.system()} PC</h1>
            <form action="/monitor_off" method="post">
                <input type="submit" value="Turn Monitor Off">
            </form>
            <form action="/monitor_on" method="post">
                <input type="submit" value="Turn Monitor On">
            </form>
            <form action="/monitor_input_hdmi" method="post">
                <input type="submit" value="Switch Monitor to HDMI">
            </form>
            <form action="/monitor_input_dp" method="post">
                <input type="submit" value="Switch Monitor to DP">
            </form>
            <form action="/shutdown" method="post">
                <input type="submit" value="Shutdown PC">
            </form>
            <p>Operating System: {platform.system()} ({platform.platform()})</p>
            <p>Linux Distribution: {linux_distro}</p>
            <p>CPU Model: {cpu_model}</p>
            <p>CPU(s): {cpu_count}</p>
            <p>Monitor 1 Status: {monitor1_status}</p>
            <p>Monitor 1 Input: {monitor1_input}</p>
            <p>Monitor 2 Status: {monitor2_status}</p>
            <p>Monitor 2 Input: {monitor2_input}</p>
            <p>Page generated in {elapsed_time} seconds.</p>
        '''
    else:
        return bottle.HTTPResponse(status=500, body='Monitor status and input not supported on this operating system.')

@bottle.route('/shutdown', method='POST')
def shutdown():
    operating_system = platform.system().lower()
    if 'windows' in operating_system:
        subprocess.call('shutdown /s /t 0', shell=True)
    elif 'darwin' in operating_system or 'linux' in operating_system:
        subprocess.call('sudo shutdown -h now', shell=True)
    else:
        return bottle.HTTPResponse(status=500, body='Shutdown not supported on this operating system. <br><a href="/">Return to home</a>')
    return 'Shutdown request received. The PC will shut down shortly.'

@bottle.route('/monitor_input_hdmi', method='POST')
def monitor_input_hdmi():
    operating_system = platform.system().lower()
    if 'linux' in operating_system:
        subprocess.call('ddcutil --display 1 setvcp 60 17', shell=True)  # Switch to HDMI
        subprocess.call('ddcutil --display 2 setvcp 60 17', shell=True)  # Switch to HDMI
        return 'Monitor input switched to HDMI.<br><a href="/">Return to home</a>'
    else:
        return bottle.HTTPResponse(status=500, body='Switching monitor input not supported on this operating system. <br><a href="/">Return to home</a>')

@bottle.route('/monitor_input_dp', method='POST')
def monitor_input_dp():
    operating_system = platform.system().lower()
    if 'linux' in operating_system:
        subprocess.call('ddcutil --display 1 setvcp 60 15', shell=True)  # Switch to DisplayPort
        subprocess.call('ddcutil --display 2 setvcp 60 15', shell=True)  # Switch to DisplayPort
        return 'Monitor input switched to DisplayPort.<br><a href="/">Return to home</a>'
    else:
        return bottle.HTTPResponse(status=500, body='Switching monitor input not supported on this operating system. <br><a href="/">Return to home</a>')

@bottle.route('/monitor_on', method='POST')
def monitor_on():
    operating_system = platform.system().lower()
    if 'windows' in operating_system:
        subprocess.call('nircmd monitor on', shell=True)
    elif 'linux' in operating_system:
        subprocess.call('ddcutil --display 1 setvcp D6 1', shell=True)  # Turn on first monitor
        subprocess.call('ddcutil --display 2 setvcp D6 1', shell=True)  # Turn on second monitor
    else:
        return bottle.HTTPResponse(status=500, body='Monitor on not supported on this operating_system.')
    return 'Monitor on request received. The monitor will be turned on shortly. <br><a href="/">Return to home</a>'

@bottle.route('/monitor_off', method='POST')
def monitor_off():
    operating_system = platform.system().lower()
    if 'windows' in operating_system:
        subprocess.call('nircmd monitor off', shell=True)
    elif 'linux' in operating_system:
        subprocess.call('ddcutil --display 1 setvcp D6 4', shell=True)  # Turn off first monitor
        subprocess.call('ddcutil --display 2 setvcp D6 4', shell=True)  # Turn off second monitor
    else:
        return bottle.HTTPResponse(status=500, body='Monitor off not supported on this operating system. <br><a href="/">Return to home</a>')
    return 'Monitor off request received. The monitor will be turned off shortly.<br><a href="/">Return to home</a>'

@bottle.route('/monitor_status', method='GET')
def monitor_status():
    operating_system = platform.system().lower()
    if 'linux' in operating_system:
        output = subprocess.check_output('ddcutil --display 1 getvcp D6', shell=True).decode()
        if 'DPM: On' in output:
            return 'On'
        elif 'DPM: Off' in output:
            return 'Off'
        else:
            return "Unable to determine monitor status. <br><a href="/">Return to home</a>"
    else:
        return bottle.HTTPResponse(status=500, body='Monitor status not supported on this operating system.<br><a href="/">Return to home</a>')

def parse_input_source(output):
    input_source_map = {
        '0x11': 'HDMI',
        '0x12': 'HDMI-2',
        '0x0f': 'DP',
        '0x10': 'DP-2',
    }
    match = re.search(r'\(sl=(0x\w{2})\)', output)
    if match:
        input_source_code = match.group(1)
        return input_source_map.get(input_source_code, 'Unknown')
    else:
        return 'Unknown'

@bottle.route('/monitor_input_status', method='GET')
def monitor_input_status():
    operating_system = platform.system().lower()
    if 'linux' in operating_system:
        output1 = subprocess.check_output('ddcutil --display 1 getvcp 60', shell=True).decode()
        return parse_input_source(output1)
    else:
        return bottle.HTTPResponse(status=500, body='Getting monitor input status not supported on this operating system.')
    
if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=4321, server='paste')
