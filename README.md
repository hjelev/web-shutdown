# web-shutdown
Shutdown a linux pc with a post request

## Installation
```bash
git clone 
cd web-shutdown
pip install -r requirements.txt
sudo cp web-shutdown.service /etc/systemd/system/
sudo systemctl enable web-shutdown
sudo systemctl start web-shutdown
sudo systemctl status web-shutdown
```

If all is green, you can now shutdown your pc with a post request to port 4321 path /shutdown like this:
```bash
curl -X POST http://localhost:4321/shutdown
```
