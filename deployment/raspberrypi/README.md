# Deploy project on RasberryPi


1) Install requirements
```bash
sudo systemctl daemon-reload
```

2) Service activation
```bash
sudo systemctl enable api
sudo systemctl enable telegram
```

3) Service starting
```bash
sudo systemctl start api
sudo systemctl start telegram
```

4) Check status
```bash
systemctl status api
systemctl status telegram
```

4) Check logs
```bash
journalctl -u api -f
journalctl -u telegram -f
```