import platform
import subprocess
import bottle

@bottle.route('/')
def home():
    return '''
        <h1>Control your PC</h1>
        <form action="/monitor_off" method="post">
            <input type="submit" value="Turn Monitor Off">
        </form>
        <form action="/monitor_on" method="post">
            <input type="submit" value="Turn Monitor On">
        </form>
        <form action="/shutdown" method="post">
            <input type="submit" value="Shutdown PC">
        </form>
    '''

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

@bottle.route('/monitor_off', method='POST')
def monitor_off():
    operating_system = platform.system().lower()
    if 'windows' in operating_system:
        subprocess.call('nircmd monitor off', shell=True)
    elif 'linux' in operating_system:
        subprocess.call('xset dpms force off', shell=True)
    else:
        return bottle.HTTPResponse(status=500, body='Monitor off not supported on this operating system.')
    return 'Monitor off request received. The monitor will be turned off shortly.'

@bottle.route('/monitor_on', method='POST')
def monitor_on():
    operating_system = platform.system().lower()
    if 'windows' in operating_system:
        subprocess.call('nircmd monitor on', shell=True)
    elif 'linux' in operating_system:
        subprocess.call('xset dpms force on', shell=True)
    else:
        return bottle.HTTPResponse(status=500, body='Monitor on not supported on this operating_system.')
    return 'Monitor on request received. The monitor will be turned on shortly.'

if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=4321)
