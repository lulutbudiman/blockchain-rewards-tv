# Blockchain-Powered Video Streaming Rewards

A tokenized viewer rewards system for RDK STB/TV platforms, integrated with Hedera blockchain for transparent, verifiable engagement tracking and NFT achievement badges.

Platform - RDK RaspberryPi

Blockchain - Hedera

## 🎯 Overview

This project demonstrates a blockchain-based content monetization platform that rewards viewers with cryptocurrency tokens for watching content and engaging with ads. Built for RDK-V devices, it demonstrates how blockchain technology can create transparent, verifiable engagement metrics for the streaming industry.

## ✨ Key Features

### 🪙 Token Economy
- **VIEW Token** - Custom fungible token on Hedera (Token ID: `0.0.7379174`)
- Earn tokens by watching ads (5 VIEW) and content (10 VIEW)
- Rate content to earn bonus tokens (2 VIEW per rating)
- Binge watching bonuses (5-15 VIEW)

### 🏆 NFT Achievement Badges
- **First Watch** 🥇 - Watch your first video
- **Rating Master** ⭐ - Submit 5 ratings
- **Binge Watcher** 📺 - Watch 10 videos
- **VIP Member** 👑 - Activate VIP status
- Real NFTs minted on Hedera (Collection ID: `0.0.7724797`)

### 💳 Redemption System
- **Skip Ads** (50 VIEW) - Skip ads in next session
- **Ad-Free Hour** (75 VIEW) - No ads for 1 hour
- **Premium Content** (100 VIEW) - Unlock premium library
- **VIP Status** (200 VIEW) - All benefits + 2x reward multiplier for 24 hours

### 🔐 Security Features
- **Device Fingerprinting** - One device per account (Sybil resistance)
- **Fraud Detection** - Prevents multi-account abuse
- **Session Tracking** - Session management

### 📝 Blockchain Audit Trail
- **Hedera Consensus Service (HCS)** - All events logged immutably
- Transparent ad impression verification
- Public audit trail (Topic ID: `0.0.7724961`)
- Verifiable on HashScan

## 🏗️ Architecture
```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│   RDK Player    │                 │  Node.js Backend│               │  Hedera Network │
│   (Python)      │ ◄─────► │                          │ ◄─────► │   (Testnet)     │
└─────────────────┘         └─────────────────┘         └─────────────────┘
       │                            │                            │
       │ • GStreamer               │ • Token Transfers          │ • VIEW Token
       │ • Westeros                │ • NFT Minting              │ • NFT Collection
       │ • Device ID               │ • HCS Logging              │ • HCS Topic
       │ • Console Menu             │ • Device Registry          │ • Mirror Node
       │                            │ • Session Management       │
```

## 🛠️ Tech Stack

### Player (RDK/Raspberry Pi)
- **Language:** Python 3
- **Video:** GStreamer 1.0
- **Display:** Westeros Compositor
- **Platform:** RDKV, Raspberry Pi 4

### Backend
- **Runtime:** Node.js
- **Framework:** Express.js
- **Blockchain SDK:** @hiero-ledger/sdk
- **Network:** Hedera Testnet

### Blockchain
- **Network:** Hedera Hashgraph Testnet
- **Token Standard:** HTS (Hedera Token Service)
- **NFT Standard:** HTS Non-Fungible Tokens
- **Consensus:** HCS (Hedera Consensus Service)

## 🚀 Quick Start

### Prerequisites
- Raspberry Pi 4 with RDK image
- Node.js 16+ (for backend)
- Hedera testnet account
- Network connectivity

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/view-rewards-tv.git
cd view-rewards-tv
```

2. **Setup backend:**
```bash
cd backend
npm install
# Configure your Hedera credentials in hedera_backend_nodejs.js
node hedera_backend_nodejs.js
```

3. **Setup player (on RDK device):**
```bash
# Copy player to RDK
scp player/player_with_redemption.py root@rdk-device:/opt/

# On RDK device
ssh root@rdk-device
chmod +x /opt/player_with_redemption.py
python3 /opt/player_with_redemption.py --display
```

For detailed setup instructions, see [SETUP_GUIDE.md](docs/SETUP_GUIDE.md)

## 📊 System Capabilities

| Feature | Status | Description |
|---------|--------|-------------|
| Token Rewards | ✅ | Earn VIEW tokens for engagement |
| NFT Badges | ✅ | Achievement NFTs on Hedera |
| Redemptions | ✅ | 4 benefit types with expiration |
| Device Security | ✅ | One account per device |
| HCS Logging | ✅ | Immutable event audit trail |
| Premium Content | ✅ | Gated content with redemption |
| VIP Multiplier | ✅ | 2x rewards for VIP members |
| Session Tracking | ✅ | Binge watching bonuses |

## 📖 Documentation

- **[Architecture Guide](docs/ARCHITECTURE.md)** - System design and components
- **[API Documentation](docs/API_DOCUMENTATION.md)** - Backend API reference
- **[Setup Guide](docs/SETUP_GUIDE.md)** - Installation and configuration
- **[User Guide](docs/USER_GUIDE.md)** - How to use the system
- **[Blockchain Integration](docs/BLOCKCHAIN_INTEGRATION.md)** - Hedera implementation details
- **[Future Work](docs/FUTURE_WORK.md)** - Roadmap and enhancements

## 🔗 Blockchain Verification

All transactions are publicly verifiable on Hedera Testnet:

- **VIEW Token:** https://hashscan.io/testnet/token/0.0.7379174
- **NFT Collection:** https://hashscan.io/testnet/token/0.0.7724797
- **HCS Event Log:** https://hashscan.io/testnet/topic/0.0.7724961
- **User Account:** https://hashscan.io/testnet/account/0.0.5864245
- **Treasury Account:** https://hashscan.io/testnet/account/0.0.5484966

## 🎮 Demo Flow

1. **Watch Content** → Earn 15 VIEW (5 for ad + 10 for content)
2. **Rate Video** → Earn 2 VIEW bonus
3. **Watch 3+ Videos** → Unlock "First Watch" badge (NFT)
4. **Accumulate Tokens** → 200+ VIEW
5. **Redeem VIP Status** → Get 2x multiplier + all benefits
6. **Verify on HashScan** → See all transactions on blockchain

## 🔮 Future Enhancements

- **Smart Contracts:** Trustless reward distribution via Solidity
- **Session Key Authentication:** Secure device authorization without exposing master keys
- **Multi-Sig Wallets:** Enhanced security for high-value transactions
- **Analytics Dashboard:** Web UI for viewing stats and history
- **Multi-Device Support:** Sync across multiple devices
- **Cross-Chain Bridge:** Integrate with other blockchain networks

See [FUTURE_WORK.md](docs/FUTURE_WORK.md) for detailed roadmap.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - Initial work - [GitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- **IIT Madras** - MTech Information Security Program
- **Hedera Hashgraph** - Blockchain infrastructure
- **RDK Community** - Reference Design Kit platform
- **Comcast** - Westeros compositor

## 📞 Contact

For questions or collaboration opportunities:
- **Email:** your.email@example.com
- **GitHub:** [@yourusername](https://github.com/yourusername)
- **LinkedIn:** [Your Name](https://linkedin.com/in/yourprofile)

## 🌟 Show Your Support

If you find this project interesting, please ⭐ star the repository!

---

**Built with ❤️ for the future of decentralized media**
