import bottle
import os
import platform

@bottle.route('/shutdown', method='POST')
def shutdown():
    system = platform.system()
    if system == 'Windows':
        os.system('shutdown /s /t 0')
    elif system == 'git a' or system == 'Linux':
        os.system('shutdown now')
    else:
        return "Shutdown not supported on this operating system."

@bottle.route('/')
def home():
    server_ip = bottle.request.urlparts.netloc.split(':')[0]
    return f"Make a POST request to http://{server_ip}/shutdown to shutdown the server."


if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=4321)
