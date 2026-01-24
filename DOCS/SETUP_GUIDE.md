# Setup Guide

Complete installation and configuration guide for VIEW Rewards TV.

## Table of Contents
- [Prerequisites](#prerequisites)
- [System Requirements](#system-requirements)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
  - [1. Hedera Account Setup](#1-hedera-account-setup)
  - [2. Backend Setup](#2-backend-setup)
  - [3. Player Setup](#3-player-setup)
- [Configuration](#configuration)
- [Running the System](#running-the-system)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Common Issues](#common-issues)

---

## Prerequisites

### Required Accounts
- **Hedera Testnet Account** (free)
  - Get from: https://portal.hedera.com
  - You'll receive testnet HBAR for transactions
  
### Required Hardware
- **Development Machine** (Laptop/Desktop)
  - OS: Windows, macOS, or Linux
  - RAM: 4GB minimum
  - Network: Internet connection
  
- **RDK Device** (Raspberry Pi 4 or RDK Set-Top-Box)
  - RDK image installed
  - Network: Same LAN as development machine
  - SSH access enabled

### Required Software

**On Development Machine:**
- Node.js 16+ ([Download](https://nodejs.org))
- Git ([Download](https://git-scm.com))
- Text editor (VS Code recommended)

**On RDK Device:**
- Python 3.8+
- GStreamer 1.0
- Westeros compositor
- SSH client

---

## System Requirements

### Minimum Requirements

| Component | Specification |
|-----------|--------------|
| **Backend Server** | |
| CPU | 2 cores |
| RAM | 2GB |
| Storage | 500MB |
| Network | Broadband internet |
| **RDK Player** | |
| CPU | ARM Cortex-A72 (Raspberry Pi 4) |
| RAM | 2GB |
| Storage | 8GB SD card |
| Display | HDMI output (optional) |
| Network | WiFi or Ethernet |

### Recommended Requirements

| Component | Specification |
|-----------|--------------|
| **Backend Server** | |
| CPU | 4 cores |
| RAM | 4GB |
| Storage | 1GB SSD |
| Network | Stable broadband |
| **RDK Player** | |
| CPU | ARM Cortex-A72 |
| RAM | 4GB |
| Storage | 16GB SD card |
| Display | 1080p HDMI |
| Network | Wired Ethernet (for stability) |

---

## Quick Start

For experienced users who want to get running quickly:
```bash
# 1. Clone repository
git clone https://github.com/yourusername/view-rewards-tv.git
cd view-rewards-tv

# 2. Setup backend
cd backend
npm install
# Edit hedera_backend_nodejs.js with your Hedera credentials
node hedera_backend_nodejs.js

# 3. Setup player (on RDK)
scp player/player_with_redemption.py root@rdk-ip:/opt/
ssh root@rdk-ip
python3 /opt/player_with_redemption.py --display
```

For detailed step-by-step instructions, continue reading.

---

## Detailed Setup

### 1. Hedera Account Setup

#### Step 1.1: Create Hedera Testnet Account

1. Visit [Hedera Portal](https://portal.hedera.com)
2. Click "Create Account"
3. Select "Testnet"
4. Complete registration
5. **Save your credentials:**
   - Account ID (e.g., `0.0.1234567`)
   - Private Key (DER format)
   - Public Key

#### Step 1.2: Fund Your Account

1. Go to [Hedera Faucet](https://portal.hedera.com/faucet)
2. Enter your Account ID
3. Request 10,000 testnet HBAR
4. Wait for confirmation (~30 seconds)

#### Step 1.3: Create VIEW Token

**Option A: Use HashIO (Recommended for beginners)**

1. Visit [HashIO](https://hashio.io)
2. Connect wallet
3. Create Fungible Token:
   - Name: VIEW Rewards Token
   - Symbol: VIEW
   - Decimals: 0
   - Initial Supply: 1,000,000
4. **Save Token ID** (e.g., `0.0.7379174`)

**Option B: Use Backend Script (Advanced)**
```bash
# In backend directory
node scripts/create-token.js
# Follow prompts
# Save the returned Token ID
```

#### Step 1.4: Create NFT Collection

1. Run backend endpoint:
```bash
curl -X POST http://localhost:5000/admin/create-nft
```

2. **Save NFT Token ID** from response

#### Step 1.5: Create HCS Topic

1. Run backend endpoint:
```bash
curl -X POST http://localhost:5000/admin/create-hcs-topic
```

2. **Save Topic ID** from response

#### Step 1.6: Associate Tokens with User Account

If you have a separate user account (not treasury):
```bash
# Associate VIEW token
# Associate NFT collection
# (Use Hedera SDK or wallet interface)
```

---

### 2. Backend Setup

#### Step 2.1: Clone Repository
```bash
git clone https://github.com/yourusername/view-rewards-tv.git
cd view-rewards-tv
```

#### Step 2.2: Install Dependencies
```bash
cd backend
npm install
```

**Expected output:**
```
added 150 packages, and audited 151 packages in 15s
```

#### Step 2.3: Configure Credentials

Edit `hedera_backend_nodejs.js`:
```javascript
// Configuration (around line 13)
const OPERATOR_ID = '0.0.YOUR_TREASURY_ACCOUNT';
const OPERATOR_KEY = 'YOUR_DER_PRIVATE_KEY_HERE';
const USER_PRIVATE_KEY = 'YOUR_USER_PRIVATE_KEY_HERE';
const TOKEN_ID = '0.0.YOUR_VIEW_TOKEN_ID';
const NFT_TOKEN_ID = '0.0.YOUR_NFT_TOKEN_ID';
const HCS_TOPIC_ID = '0.0.YOUR_HCS_TOPIC_ID';
const TREASURY_ACCOUNT = '0.0.YOUR_TREASURY_ACCOUNT';
const USER_ACCOUNT = '0.0.YOUR_USER_ACCOUNT';
```

**Example:**
```javascript
const OPERATOR_ID = '0.0.5484966';
const OPERATOR_KEY = '302e020100300506032b657004220420a1b2c3d4...';
const USER_PRIVATE_KEY = '302e020100300506032b657004220420e5f6a7b8...';
const TOKEN_ID = '0.0.7379174';
const NFT_TOKEN_ID = '0.0.7724797';
const HCS_TOPIC_ID = '0.0.7724961';
const TREASURY_ACCOUNT = '0.0.5484966';
const USER_ACCOUNT = '0.0.5864245';
```

#### Step 2.4: Find Your IP Address

**Windows:**
```bash
ipconfig
# Look for "IPv4 Address" (e.g., 192.168.0.148)
```

**macOS/Linux:**
```bash
ifconfig
# Look for "inet" address (e.g., 192.168.0.148)
```

**Save this IP** - you'll need it for player configuration.

#### Step 2.5: Start Backend
```bash
node hedera_backend_nodejs.js
```

**Expected output:**
```
============================================================
🚀 HEDERA REWARDS BACKEND - Phase 2: NFT Badges
============================================================

Configuration:
  Operator: 0.0.5484966
  Token: 0.0.7379174 (VIEW)
  NFT Collection: 0.0.7724797 (BADGE)
  Treasury: 0.0.5484966
  User: 0.0.5864245
  Network: Hedera Testnet

✅ Server running on http://0.0.0.0:5000

Endpoints:
  GET  /health            - Health check
  POST /device/register   - Register device to account
  ...
```

#### Step 2.6: Test Backend

In a new terminal:
```bash
curl http://localhost:5000/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "service": "Hedera Rewards Backend",
  "timestamp": "2026-01-24T12:00:00.000Z"
}
```

---

### 3. Player Setup

#### Step 3.1: Prepare Video Files

On your RDK device, create directories:
```bash
ssh root@rdk-ip

# Create directories
mkdir -p /opt/premium

# Create or upload video files
# Example using wget (if you have test videos online):
cd /opt
wget https://example.com/test-video.mp4 -O Venice_10.mp4
wget https://example.com/test-ad.mp4 -O ad.mp4

cd /opt/premium
wget https://example.com/premium-video.mp4 -O premium_show.mp4
```

**Or copy from your laptop:**
```bash
# From your laptop
scp /path/to/video.mp4 root@rdk-ip:/opt/Venice_10.mp4
scp /path/to/ad.mp4 root@rdk-ip:/opt/ad.mp4
scp /path/to/premium.mp4 root@rdk-ip:/opt/premium/show.mp4
```

#### Step 3.2: Copy Player to RDK
```bash
# From your laptop (in project root)
scp player/player_with_redemption.py root@rdk-ip:/opt/
```

#### Step 3.3: Configure Player

SSH to RDK and edit the player:
```bash
ssh root@rdk-ip
nano /opt/player_with_redemption.py
```

Update the backend URL (around line 20):
```python
BACKEND_URL = "http://192.168.0.148:5000"  # ← Your laptop's IP
```

Update account ID (around line 18):
```python
ACCOUNT_ID = "0.0.5864245"  # ← Your user account ID
```

Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`)

#### Step 3.4: Make Player Executable
```bash
chmod +x /opt/player_with_redemption.py
```

#### Step 3.5: Test Player (Console Mode)
```bash
python3 /opt/player_with_redemption.py
```

**Expected output:**
```
============================================================
      REWARDS TV - Phase 2: NFT Achievement Badges
============================================================

  📁 Using default ad: /opt/ad.mp4

🖥️  Display: OFF
🔗 Blockchain: Hedera Testnet
   Account: 0.0.5864245
   Token: 0.0.7379174 (VIEW)

🔐 Device Security Check...
   Device ID: rdk_cpu_10000000a1b2c3d4...
   ✅ Device registered (new)

📺 Starting viewing session...
  📺 Session started: session_1737673200_abc...

🎁 Checking active benefits...
   No active benefits

💳 Checking balance...
   Balance: 0 VIEW

────────────────────────────────────────────────────────────
MAIN MENU
────────────────────────────────────────────────────────────
1. Watch Content
2. Redemption Center
3. Achievement Badges
4. Check Balance
0. Exit
────────────────────────────────────────────────────────────

Select option:
```

#### Step 3.6: Test Display Mode (Optional)

If you have HDMI display connected:
```bash
python3 /opt/player_with_redemption.py --display
```

---

## Configuration

### Environment Variables (Optional)

For security, you can use environment variables instead of hardcoding credentials:

**Backend:**

Create `.env` file:
```bash
HEDERA_OPERATOR_ID=0.0.5484966
HEDERA_OPERATOR_KEY=302e020100300506032b657004220420...
HEDERA_USER_KEY=302e020100300506032b657004220420...
HEDERA_TOKEN_ID=0.0.7379174
HEDERA_NFT_TOKEN_ID=0.0.7724797
HEDERA_HCS_TOPIC_ID=0.0.7724961
```

Update `hedera_backend_nodejs.js`:
```javascript
require('dotenv').config();

const OPERATOR_ID = process.env.HEDERA_OPERATOR_ID;
const OPERATOR_KEY = process.env.HEDERA_OPERATOR_KEY;
// ... etc
```

Install dotenv:
```bash
npm install dotenv
```

### Network Configuration

**Firewall Rules:**

Ensure port 5000 is accessible from RDK device:

**Windows:**
```bash
# Allow inbound on port 5000
netsh advfirewall firewall add rule name="Hedera Backend" dir=in action=allow protocol=TCP localport=5000
```

**macOS:**
```bash
# System Preferences → Security & Privacy → Firewall → Options
# Add Node.js and allow incoming connections
```

**Linux:**
```bash
sudo ufw allow 5000/tcp
```

---

## Running the System

### Development Mode

**Terminal 1 (Backend):**
```bash
cd backend
node hedera_backend_nodejs.js
```

**Terminal 2 (RDK via SSH):**
```bash
ssh root@rdk-ip
python3 /opt/player_with_redemption.py --display
```


## Verification

### 1. Verify Backend Health
```bash
curl http://localhost:5000/health
```

Expected: `{"status":"healthy",...}`

### 2. Verify Hedera Connection

Check backend logs for:
```
✅ Server running on http://0.0.0.0:5000
```

No errors about Hedera connection.

### 3. Verify Player Connection

In player, select "Check Balance" (option 4)

Expected:
```
🔄 Checking balance...
💳 Balance: X VIEW
```

### 4. Verify Blockchain Integration

1. Watch a video
2. Note the transaction ID from backend logs
3. Visit HashScan:
```
   https://hashscan.io/testnet/transaction/TRANSACTION_ID
```
4. Verify transaction appears

### 5. Verify Full Flow

1. **Earn tokens:** Watch video → Get 15 VIEW
2. **Check balance:** Menu option 4 → See updated balance
3. **View on blockchain:** Check HashScan account page
4. **Earn badge:** Watch first video → Get "First Watch" NFT
5. **View badges:** Menu option 3 → See badge
6. **Verify NFT:** Check HashScan NFT collection

---

## Troubleshooting

### Backend Won't Start

**Error: `Cannot find module '@hiero-ledger/sdk'`**

**Solution:**
```bash
cd backend
npm install
```

---

**Error: `EADDRINUSE: address already in use :::5000`**

**Solution:**
Port 5000 is already in use.

**Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID [PID] /F
```

**macOS/Linux:**
```bash
lsof -i :5000
kill -9 [PID]
```

Or change port in backend:
```javascript
const PORT = 5001;  // Use different port
```

---

**Error: `receipt for transaction ... contained error status INVALID_ACCOUNT_ID`**

**Solution:**
- Check `OPERATOR_ID` is correct
- Verify account exists on testnet
- Ensure you have testnet HBAR

---

### Player Won't Connect

**Error: `Backend unreachable`**

**Solution:**

1. **Check backend is running:**
```bash
   curl http://YOUR_LAPTOP_IP:5000/health
```

2. **Check firewall:**
   - Allow port 5000 on laptop
   - Ensure RDK and laptop on same network

3. **Check IP address in player:**
```python
   BACKEND_URL = "http://192.168.0.148:5000"  # Correct IP?
```

4. **Test connectivity from RDK:**
```bash
   ssh root@rdk-ip
   curl http://192.168.0.148:5000/health
```

---

**Error: `Device registration failed`**

**Solution:**

1. **Check backend logs** for detailed error
2. **Clear device registry** (restart backend)
3. **Try different account** if testing

---

### Video Won't Play

**Error: `File not found`**

**Solution:**
```bash
# Verify files exist
ls -la /opt/*.mp4
ls -la /opt/premium/*.mp4

# Check permissions
chmod 644 /opt/*.mp4
chmod 644 /opt/premium/*.mp4
```

---

**Error: `GStreamer error`**

**Solution:**

1. **Check GStreamer installation:**
```bash
   gst-launch-1.0 --version
```

2. **Test playback manually:**
```bash
   gst-launch-1.0 filesrc location=/opt/Venice_10.mp4 ! decodebin ! fakesink
```

3. **Install missing plugins:**
```bash
   apt-get install gstreamer1.0-plugins-base
   apt-get install gstreamer1.0-plugins-good
   apt-get install gstreamer1.0-plugins-bad
```

---

**Error: `Westeros error`**

**Solution:**

1. **Check Westeros is running:**
```bash
   ps aux | grep westeros
```

2. **Use console mode instead:**
```bash
   python3 /opt/player_with_redemption.py
   # (without --display flag)
```

---

### Blockchain Issues

**Error: `Transaction failed: INSUFFICIENT_ACCOUNT_BALANCE`**

**Solution:**

Treasury needs HBAR for transaction fees:
```bash
# Get testnet HBAR from faucet
# Visit: https://portal.hedera.com/faucet
# Request for your treasury account
```

---

**Error: `METADATA_TOO_LONG`**

**Solution:**

NFT metadata exceeds 100 bytes. Already fixed in current code, but if you see this:
```javascript
// Use shorter metadata
metadata: Buffer.from('badge_type')  // ✅ Short
// Not:
metadata: Buffer.from(JSON.stringify({...}))  // ❌ Too long
```

---

**Error: `TOKEN_NOT_ASSOCIATED_TO_ACCOUNT`**

**Solution:**

User account needs to associate with NFT token:
- Already handled automatically in code
- If error persists, backend will log it
- Check user has associated both VIEW token and NFT collection

---

## Common Issues

### Issue: Player shows balance 0, but I earned tokens

**Diagnosis:**
- Backend awarded tokens
- Mirror node hasn't updated yet

**Solution:**
- Wait 5-10 seconds
- Check balance again
- Verify on HashScan (source of truth)

---

### Issue: NFT badge not showing

**Diagnosis:**
- NFT minted but transfer failed
- User account not associated with NFT token

**Solution:**
- Check backend logs for NFT transfer status
- Verify on HashScan if NFT was minted
- Association happens automatically, but may fail first time

---

### Issue: VIP multiplier not working

**Diagnosis:**
- Benefit expired
- Not checking active benefits

**Solution:**
1. Check "Balance" menu (option 4)
2. See if VIP is listed as active
3. Check remaining time
4. Re-redeem if expired

---

### Issue: Can't redeem (insufficient balance)

**Diagnosis:**
- Local balance vs blockchain balance mismatch

**Solution:**
1. Check actual blockchain balance on HashScan
2. Backend may not have updated local tracking
3. Restart backend if needed
4. Balance queries go to Mirror Node (source of truth)

---

## Network Topology

### Typical Setup
```
Internet
    │
    ├─── Laptop (192.168.0.148)
    │    └─ Backend Server (Port 5000)
    │
    └─── Router (192.168.0.1)
         │
         └─── RDK Device (192.168.0.X)
              └─ Player Application
```

### Port Forwarding (If Needed)

If RDK can't reach laptop:

1. **Check same subnet:**
```bash
   # On laptop: 192.168.0.148
   # On RDK:    192.168.0.xxx  (same 192.168.0.x range?)
```

2. **Ping test:**
```bash
   # From RDK
   ping 192.168.0.148
```

3. **Disable VPN** on laptop (may block local network)

---

## Performance Tuning

### Backend Optimization

**Increase concurrent connections:**
```javascript
// In hedera_backend_nodejs.js
const server = app.listen(PORT, '0.0.0.0');
server.maxConnections = 100;
```

**Add request timeout:**
```javascript
app.use((req, res, next) => {
    req.setTimeout(30000);  // 30 seconds
    next();
});
```

### Player Optimization

**Reduce API calls:**
```python
# Cache balance locally, refresh every 30s instead of every check
```

**Pre-buffer video:**
```bash
# GStreamer queue settings
gst-launch-1.0 ... ! queue max-size-time=5000000000 ! ...
```

---

## Security Checklist

Before deploying:

- [ ] Private keys in environment variables (not source code)
- [ ] Firewall configured (only port 5000 open)
- [ ] HTTPS enabled for backend (production)
- [ ] Rate limiting implemented
- [ ] Input validation on all endpoints
- [ ] CORS configured properly
- [ ] Session expiration set
- [ ] Device registry limits enforced

---

## Next Steps

After successful setup:

1. **Test complete user journey** (see [USER_GUIDE.md](USER_GUIDE.md))
2. **Review blockchain transactions** on HashScan
3. **Explore API endpoints** (see [API_DOCUMENTATION.md](API_DOCUMENTATION.md))
4. **Understand architecture** (see [ARCHITECTURE.md](ARCHITECTURE.md))
5. **Check future enhancements** (see [FUTURE_WORK.md](FUTURE_WORK.md))

---

## Getting Help

If you encounter issues not covered here:

1. **Check backend logs** for detailed error messages
2. **Check player console** for error output
3. **Verify on HashScan** for blockchain state
4. **Review documentation** for specific components
5. **Create GitHub issue** with:
   - Error message
   - Steps to reproduce
   - System information
   - Logs (sanitize private keys!)

---

## Additional Resources

- **Hedera Documentation:** https://docs.hedera.com
- **Hedera Portal:** https://portal.hedera.com
- **HashScan Explorer:** https://hashscan.io/testnet
- **RDK Documentation:** https://developer.rdkcentral.com
- **GStreamer Guide:** https://gstreamer.freedesktop.org/documentation

---

**Setup complete! You're ready to use VIEW Rewards TV.** 🎉

For usage instructions, see [USER_GUIDE.md](USER_GUIDE.md)