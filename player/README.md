# Player Application

Python-based video player for RDK/Raspberry Pi with blockchain rewards.

## Requirements

- Python 3.8+
- GStreamer 1.0
- Westeros compositor (for display mode)

## Configuration

Edit `player_with_redemption.py` and update:
```python
ACCOUNT_ID = "0.0.YOUR_ACCOUNT"
TOKEN_ID = "0.0.YOUR_TOKEN_ID"
BACKEND_URL = "http://YOUR_BACKEND_IP:5000"
```

## Running

Console mode (no display):
```bash
python3 player_with_redemption.py
```

Display mode (HDMI output):
```bash
python3 player_with_redemption.py --display
```

## Installation on RDK
```bash
# Copy to device
scp player_with_redemption.py root@rdk-ip:/opt/

# Make executable
ssh root@rdk-ip
chmod +x /opt/player_with_redemption.py

# Run
python3 /opt/player_with_redemption.py
```

## Video Files

Place video files in:
- Regular content: `/opt/*.mp4`
- Premium content: `/opt/premium/*.mp4`
- Ad video: `/opt/ad.mp4`