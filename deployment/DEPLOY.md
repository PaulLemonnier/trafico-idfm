# Deploy project
These commands will allow you to deploy the project so that the applications launch when the Raspberry Pi starts up.

0) Move the services to systemd

Navigate to the deployment folder.

```bash
sudo cp raspberrypi/api.service raspberrypi/telegram.service /etc/systemd/system/
sudo cp waveshare_screen/activate-lcd.service waveshare_screen/screen.service /etc/systemd/system/
```

1) Install requirements
```bash
sudo systemctl daemon-reload
```

2) Service activation
```bash
sudo systemctl enable api
sudo systemctl enable telegram
sudo systemctl enable activate-lcd
sudo systemctl enable screen
```

3) Service starting
```bash
sudo systemctl start api
sudo systemctl start telegram
sudo systemctl start activate-lcd
sudo systemctl start screen
```

4) Check status
```bash
systemctl status api
systemctl status telegram
systemctl status start activate-lcd
systemctl status start screen
```

4) Check logs
```bash
journalctl -u api -f
journalctl -u telegram -f
journalctl -u activate-lcd -f
journalctl -u screen -f
```