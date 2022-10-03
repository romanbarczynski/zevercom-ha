# ZeverCOM Home Assistant device via mqtt

This module reads details directly from ZEVERCOM WiFi device and push data into mqtt broker (along with home assistant configuration for it).

Data pushed:

- from power metter:
  - Line PAC
  - Line Energy In
  - Line Energy Out

- from first inverter:
  - PAC
  - Energy (Today)

## Quick start

Create config file `zevercom.conf`:

```yaml
mqtt_server: mqtt               # IP address or resolvable name of mqtt broker
zevercom_ip: 172.17.0.192       # IP address or resolvable name of zevercom
topic: zevercom                 # mqtt topic prefix
device_id: '0xdeadbeef00000001' # random device ID 
```

If you're using docker-compose add it as service:

```yaml
  zevercom:
    restart: unless-stopped
    image: ghcr.io/rombarcz/zevercom-ha:latest
    volumes:
      - ./zevercom/zevercom.conf:/etc/zevercom.conf:ro
    depends_on:
      - mqtt
```

If you're using just docker:

```bash
docker pull ghcr.io/rombarcz/zevercom-ha:latest
docker run -it -v $PWD/zevercom.conf:/etc/zevercom.conf:ro ghcr.io/rombarcz/zevercom-ha:latest
```

You can also run this natively:

1. Copy `zevercom.conf` to `/etc/`
2. Install requirements: `pip install -r requirements.txt`
3. Run: `python zevercom.py`

