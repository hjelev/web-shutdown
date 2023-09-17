import platform
import subprocess
import bottle

@bottle.route('/')
def home():
    message = "Make a POST request to /shutdown to shutdown the PC\n" \
              "Make a POST request to /wakeup to wake up the monitor"
    return message

@bottle.route('/shutdown', method='POST')
def shutdown():
    operating_system = platform.system().lower()
    if 'windows' in operating_system:
        subprocess.call('shutdown /s /t 0', shell=True)
    elif 'darwin' in operating_system or 'linux' in operating_system:
        subprocess.call('sudo shutdown -h now', shell=True)
    else:
        return bottle.HTTPResponse(status=500, body='Shutdown not supported on this operating system.')
    return 'Shutdown request received. The PC will shut down shortly.'

@bottle.route('/wakeup', method='POST')
def wakeup():
    operating_system = platform.system().lower()
    if 'windows' in operating_system:
        subprocess.call('powershell -c "(New-Object -ComObject Shell.Application).ToggleDesktop()"', shell=True)
    elif 'darwin' in operating_system:
        subprocess.call('caffeinate -u -t 1', shell=True)
    elif 'linux' in operating_system:
        subprocess.call('xset dpms force on', shell=True)
    else:
        return bottle.HTTPResponse(status=500, body='Monitor wake not supported on this operating system.')
    return 'Monitor wake request received. The monitor will be woken up shortly.'

if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=4321)
