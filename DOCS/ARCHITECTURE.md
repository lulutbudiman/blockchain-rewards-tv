# System Architecture

## Table of Contents
- [Overview](#overview)
- [System Components](#system-components)
- [Architecture Diagram](#architecture-diagram)
- [Component Details](#component-details)
- [Data Flow](#data-flow)
- [Blockchain Integration](#blockchain-integration)
- [Storage Architecture](#storage-architecture)
- [Security Model](#security-model)
- [Technology Stack](#technology-stack)
- [Design Decisions](#design-decisions)

---

## Overview

This project demonstartes a three-tier blockchain-integrated streaming rewards platform consisting of:

1. **Player (Client)** - RDK/Raspberry Pi Python application for video playback and user interaction
2. **Backend (Server)** - Node.js/Express.js API server for business logic and blockchain orchestration
3. **Blockchain (Hedera)** - Decentralized ledger for token transfers, NFTs, and event logging

The system demonstrates how traditional media platforms can integrate blockchain technology to create transparent, verifiable engagement metrics and tokenized reward systems.

---

## System Components

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                        USER DEVICE (RDK/RPi4)                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Player Application                      │  │
│  │  • Video Playback (GStreamer)                             │  │
│  │  • Display Management (Westeros)                          │  │
│  │  • User Interface (Console Menu)                          │  │
│  │  • Device Fingerprinting                                  │  │
│  │  • Blockchain Wallet Interface                            │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST
                              │
┌─────────────────────────────────────────────────────────────────┐
│                   BACKEND SERVER (Node.js)                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                     API Layer                              │  │
│  │  • Authentication & Session Management                    │  │
│  │  • Reward Distribution Logic                              │  │
│  │  • Redemption Engine                                      │  │
│  │  • Achievement Tracker                                    │  │
│  │  • Device Registry                                        │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                 Blockchain Interface                       │  │
│  │  • Hedera SDK Integration                                 │  │
│  │  • Transaction Signing                                    │  │
│  │  • NFT Minting & Transfer                                 │  │
│  │  • HCS Message Submission                                 │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   In-Memory Storage                        │  │
│  │  • Active Benefits (Map)                                  │  │
│  │  • Sessions (Map)                                         │  │
│  │  • Ratings (Array)                                        │  │
│  │  • Device Registry (Map)                                  │  │
│  │  • NFT Awards (Map)                                       │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Hedera SDK / REST API
                              │
┌─────────────────────────────────────────────────────────────────┐
│                      HEDERA NETWORK (Testnet)                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   Consensus Nodes                          │  │
│  │  • Transaction Processing                                 │  │
│  │  • Token Transfers (HTS)                                  │  │
│  │  • NFT Minting & Transfers                                │  │
│  │  • HCS Message Publishing                                 │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Mirror Nodes                            │  │
│  │  • REST API for queries                                   │  │
│  │  • Account balance lookups                                │  │
│  │  • Transaction history                                    │  │
│  │  • Token information                                      │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   Blockchain State                         │  │
│  │  • VIEW Token (0.0.7379174)                               │  │
│  │  • NFT Collection (0.0.7724797)                           │  │
│  │  • HCS Topic (0.0.7724961)                                │  │
│  │  • Account Balances                                       │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Architecture Diagram

### Component Interaction Flow
```
┌──────────┐         ┌──────────┐         ┌──────────┐         ┌──────────┐
│          │         │          │         │          │         │          │
│  Player  │────────▶│ Backend  │────────▶│  Hedera  │────────▶│ HashScan │
│  (RDK)   │◀────────│  (API)   │◀────────│ Network  │         │  (View)  │
│          │         │          │         │          │         │          │
└──────────┘         └──────────┘         └──────────┘         └──────────┘
     │                    │                     │
     │                    │                     │
     ▼                    ▼                     ▼
┌──────────┐         ┌──────────┐         ┌──────────┐
│ GStreamer│         │  Express │         │   HTS    │
│ Westeros │         │  Maps    │         │   NFT    │
│ Python   │         │  Hedera  │         │   HCS    │
│          │         │   SDK    │         │          │
└──────────┘         └──────────┘         └──────────┘
```

---

## Component Details

### 1. Player Application (RDK/Raspberry Pi)

**Technology:**
- **Language:** Python 3
- **Video Engine:** GStreamer 1.0
- **Compositor:** Westeros (Wayland-based)
- **Platform:** RDK (Reference Design Kit)

**Responsibilities:**
- Video playback (ads and content)
- User interface (console-based menu)
- Device fingerprinting (CPU serial, MAC address, machine ID)
- Blockchain wallet operations
- Session management
- Balance queries

**Key Classes:**
```python
BlockchainWallet     # Handles all blockchain interactions
WesterosManager      # Manages display compositor
VideoPlayer          # Core playback engine
AdManager            # Ad playback with skip logic
ContentPlayer        # Content playback
```

**Device Fingerprinting:**
```python
CPU Serial (/proc/cpuinfo)      # Hardware-based (best)
```

---

### 2. Backend Server (Node.js)

**Technology:**
- **Runtime:** Node.js 16+
- **Framework:** Express.js
- **SDK:** @hiero-ledger/sdk
- **Storage:** In-memory (Maps, Arrays)

**Responsibilities:**
- API endpoint management
- Business logic enforcement
- Blockchain transaction orchestration
- Device registry management
- Session tracking
- Achievement calculation
- Benefit expiration tracking
- HCS event logging

**API Endpoints:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/device/register` | POST | Register device to account |
| `/device/verify` | GET | Verify device authorization |
| `/device/info` | GET | Get device registration info |
| `/reward` | POST | Award tokens to user |
| `/balance` | GET | Check token balance |
| `/redemptions` | GET | List available redemptions |
| `/redeem` | POST | Redeem tokens for benefits |
| `/benefits` | GET | Check active benefits |
| `/rate` | POST | Submit content rating |
| `/session/start` | POST | Start viewing session |
| `/session/video` | POST | Track video in session |
| `/session/bonus` | GET | Check/claim binge bonus |
| `/badges` | GET | Get achievement badges |
| `/achievements/check` | POST | Check and award achievements |
| `/ratings` | GET | View rating history |
| `/events` | GET | View HCS event log |

**Storage Architecture:**
```javascript
// In-Memory Data Structures
const ratings = [];                    // All content ratings
const sessions = new Map();            // session_id -> session_data
const benefits = new Map();            // account_id -> benefit_data
const deviceRegistry = new Map();      // device_id -> account_id
const nftAwards = new Map();           // account_id -> Set<badge_types>
const nftSerials = new Map();          // account_id -> Map<badge_type, serial>
```

---

### 3. Hedera Blockchain

**Network:** Testnet (testnet.hedera.com)

**Services Used:**

#### Hedera Token Service (HTS)
- **VIEW Token (0.0.7379174)**
  - Type: Fungible Token
  - Symbol: VIEW
  - Decimals: 0
  - Supply: Minted on-demand by treasury
  - Purpose: Reward currency

- **Achievement NFTs (0.0.7724797)**
  - Type: Non-Fungible Token
  - Symbol: BADGE
  - Supply: Infinite (minted per achievement)
  - Metadata: Badge type identifier
  - Purpose: Collectible achievements

#### Hedera Consensus Service (HCS)
- **Event Log Topic (0.0.7724961)**
  - Memo: "VIEW Rewards TV - Event Log"
  - Purpose: Immutable audit trail
  - Events: Rewards, ratings, redemptions, achievements, bonuses

#### Account Structure
```
Treasury Account (0.0.5484966)
├─ Owns: Unlimited VIEW tokens
├─ Mints: NFT badges
├─ Signs: All blockchain transactions
└─ Distributes: Tokens to users

User Account (0.0.5864245)
├─ Receives: VIEW tokens (rewards)
├─ Receives: NFT badges (achievements)
├─ Holds: Token balance
└─ Associated: With NFT collection
```

---

## Data Flow

### Scenario 1: Watching Content and Earning Tokens
```
┌─────────┐                                  ┌─────────┐                                  ┌─────────┐
│ Player  │                                  │ Backend │                                  │ Hedera  │
└────┬────┘                                  └────┬────┘                                  └────┬────┘
     │                                            │                                            │
     │ 1. User selects "Watch Content"            │                                            │
     │ ─────────────────────────────────────────► │                                            │
     │                                            │                                            │
     │ 2. Track video in session                  │                                            │
     │ ─────────────────────────────────────────► │                                            │
     │                                            │ 3. Store session data                      │
     │                                            │ ─────────────────────────                  │
     │                                            │                                            │
     │ 4. Play ad (if no skip benefit)            │                                            │
     │ ◄─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │                                            │
     │                                            │                                            │
     │ 5. Ad completed - send reward claim        │                                            │
     │ ─────────────────────────────────────────► │                                            │
     │                                            │                                            │
     │                                            │ 6. Transfer 5 VIEW (ad reward)             │
     │                                            │ ──────────────────────────────────────────►│
     │                                            │                                            │
     │                                            │                                            │ 7. Execute transfer
     │                                            │                                            │ ──────────────────
     │                                            │                                            │
     │                                            │ 8. Transaction receipt                     │
     │                                            │ ◄──────────────────────────────────────────│
     │                                            │                                            │
     │                                            │ 9. Log to HCS                              │
     │                                            │ ──────────────────────────────────────────►│
     │                                            │                                            │
     │ 10. Reward confirmation                    │                                            │
     │ ◄─────────────────────────────────────────│                                            │
     │                                            │                                            │
     │ 11. Play main content                      │                                            │
     │ ◄─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │                                            │
     │                                            │                                            │
     │ 12. Content completed - send reward claim  │                                            │
     │ ─────────────────────────────────────────► │                                            │
     │                                            │                                            │
     │                                            │ 13. Transfer 10 VIEW (content reward)      │
     │                                            │ ──────────────────────────────────────────►│
     │                                            │                                            │
     │                                            │ 14. Transaction receipt                    │
     │                                            │ ◄──────────────────────────────────────────│
     │                                            │                                            │
     │                                            │ 15. Log to HCS                             │
     │                                            │ ──────────────────────────────────────────►│
     │                                            │                                            │
     │                                            │ 16. Check achievements                     │
     │                                            │ ──────────────────────────                 │
     │                                            │                                            │
     │                                            │ 17. First Watch badge earned!              │
     │                                            │ ──────────────────────────                 │
     │                                            │                                            │
     │                                            │ 18. Mint NFT                               │
     │                                            │ ──────────────────────────────────────────►│
     │                                            │                                            │
     │                                            │ 19. Transfer NFT to user                   │
     │                                            │ ──────────────────────────────────────────►│
     │                                            │                                            │
     │                                            │ 20. Log achievement to HCS                 │
     │                                            │ ──────────────────────────────────────────►│
     │                                            │                                            │
     │ 21. Show achievement notification          │                                            │
     │ ◄─────────────────────────────────────────│                                            │
     │     "🎉 First Watch badge earned!"         │                                            │
     │                                            │                                            │
```

---

### Scenario 2: Redeeming VIP Status
```
┌─────────┐                    ┌─────────┐                    ┌─────────┐
│ Player  │                    │ Backend │                    │ Hedera  │
└────┬────┘                    └────┬────┘                    └────┬────┘
     │                              │                              │
     │ 1. Select "Redemption Center"│                              │
     │ ────────────────────────────►│                              │
     │                              │                              │
     │ 2. Get redemptions & balance │                              │
     │ ◄────────────────────────────│                              │
     │                              │                              │
     │ 3. Choose "VIP Status"       │                              │
     │ ────────────────────────────►│                              │
     │                              │                              │
     │                              │ 4. Validate balance (≥200)   │
     │                              │ ─────────────────────────    │
     │                              │                              │
     │                              │ 5. Simulate token burn       │
     │                              │ ────────────────────────────►│
     │                              │                              │
     │                              │ 6. Activate benefit          │
     │                              │ (expires in 86400s)          │
     │                              │ ─────────────────────────    │
     │                              │                              │
     │                              │ 7. Check VIP achievement     │
     │                              │ ─────────────────────────    │
     │                              │                              │
     │                              │ 8. Mint VIP badge NFT        │
     │                              │ ────────────────────────────►│
     │                              │                              │
     │                              │ 9. Log redemption to HCS     │
     │                              │ ────────────────────────────►│
     │                              │                              │
     │ 10. Benefit activated!       │                              │
     │ ◄────────────────────────────│                              │
     │                              │                              │
     │ 11. All future rewards = 2x  │                              │
     │ (VIP multiplier active)      │                              │
     │                              │                              │
```

---

## Blockchain Integration

### Token Economics

**VIEW Token (0.0.7379174)**

| Action | Base Reward | VIP Multiplier | Total (VIP) |
|--------|-------------|----------------|-------------|
| Watch Ad (complete) | 5 VIEW | 2x | 10 VIEW |
| Watch Ad (skip) | 0 VIEW | - | 0 VIEW |
| Watch Content | 10 VIEW | 2x | 20 VIEW |
| Rate Content | 2 VIEW | 2x | 4 VIEW |
| Binge Bonus (3 videos) | 5 VIEW | 2x | 10 VIEW |
| Binge Bonus (5 videos) | 15 VIEW | 2x | 30 VIEW |

**Redemption Costs:**

| Benefit | Cost | Duration | Features |
|---------|------|----------|----------|
| Skip Ads | 50 VIEW | Single use | Skip ads once |
| Ad-Free Hour | 75 VIEW | 3600s | No ads for 1 hour |
| Premium Content | 100 VIEW | Until used | Unlock premium library |
| VIP Status | 200 VIEW | 86400s | All benefits + 2x rewards |

**Token Flow:**
```
Treasury (0.0.5484966)
    │
    │ Rewards ↓
    │
User (0.0.5864245)
    │
    │ Redemptions ↑ (simulated)
    │
Treasury (0.0.5484966)
```

---

### NFT Achievement System

**Collection: Achievement Badges (0.0.7724797)**

| Badge | Icon | Requirement | Metadata |
|-------|------|-------------|----------|
| First Watch | 🥇 | Watch 1 video | `first_watch` |
| Rating Master | ⭐ | Submit 5 ratings | `rating_master` |
| Binge Watcher | 📺 | Watch 10 videos total | `binge_watcher` |
| VIP Member | 👑 | Activate VIP status | `vip_member` |

**NFT Lifecycle:**
```
Achievement Earned
    ↓
Backend checks: hasAchievement()?
    ↓
Mint NFT with metadata
    ↓
Associate user account with NFT token (if first time)
    ↓
Transfer NFT from treasury to user
    ↓
Log to HCS
    ↓
Notify player
```

---

### Hedera Consensus Service (HCS) Logging

**Topic: Event Log (0.0.7724961)**

**Event Types:**
```javascript
// Reward Event
{
  "type": "reward",
  "timestamp": 1737673200000,
  "data": {
    "account_id": "0.0.5864245",
    "amount": 5,
    "reason": "Ad viewing",
    "transaction_id": "0.0.5484966@1737673200.123"
  }
}

// Rating Event
{
  "type": "rating",
  "timestamp": 1737673300000,
  "data": {
    "account_id": "0.0.5864245",
    "content_id": "Venice_10.mp4",
    "rating": 5,
    "session_id": "session_1737673200_abc123"
  }
}

// Redemption Event
{
  "type": "redemption",
  "timestamp": 1737673400000,
  "data": {
    "account_id": "0.0.5864245",
    "benefit_type": "vip_day",
    "benefit_name": "VIP Status (1 day)",
    "cost": 200,
    "expires_at": 1737759800000
  }
}

// Achievement Event
{
  "type": "achievement",
  "timestamp": 1737673500000,
  "data": {
    "account_id": "0.0.5864245",
    "badge_type": "first_watch",
    "badge_name": "First Watch",
    "nft_serial": 1,
    "nft_token_id": "0.0.7724797"
  }
}

// Binge Bonus Event
{
  "type": "binge_bonus",
  "timestamp": 1737673600000,
  "data": {
    "account_id": "0.0.5864245",
    "session_id": "session_1737673200_abc123",
    "videos_watched": 5,
    "bonus_amount": 30,
    "vip_multiplier": true
  }
}
```

**Benefits of HCS Logging:**
- ✅ Immutable record (can't be altered)
- ✅ Timestamped (consensus timestamp)
- ✅ Public (anyone can verify)
- ✅ Cheap (~$0.0001 per message)
- ✅ Ordered (sequence numbers)

---

## Storage Architecture

### Backend Storage Strategy

**Current Implementation: In-Memory (Development)**
```javascript
// Temporary, resets on server restart
const ratings = [];
const sessions = new Map();
const benefits = new Map();
const deviceRegistry = new Map();
const nftAwards = new Map();
const nftSerials = new Map();
```


## Security Model

### 1. Device Fingerprinting (Sybil Resistance)

**Purpose:** Prevent one person from creating multiple accounts

**Implementation:**
```python
def get_device_id():
    # Priority order:
    1. CPU Serial (/proc/cpuinfo)      # Hardware-based
    2. Machine ID (/etc/machine-id)    # OS-based
    3. MAC Address (uuid.getnode())    # Network-based
```

**Backend Enforcement:**
```javascript
deviceRegistry.set(device_id, account_id);
// Blocks: Different account on same device
// Blocks: Same account on multiple devices
```

**Fraud Detection:**
- ✅ One device per account
- ✅ One account per device
- ✅ Tracks device-account mapping
- ✅ Rejects conflicting registrations

---

### 2. Private Key Management

**Current Implementation (Demo):**
```javascript
// ⚠️ DEVELOPMENT ONLY
const OPERATOR_KEY = 'DER_ENCODED_PRIVATE_KEY';
const USER_PRIVATE_KEY = 'DER_ENCODED_PRIVATE_KEY';
```

**Security Concerns:**
- ❌ Private keys in source code
- ❌ No encryption at rest
- ❌ Single point of compromise

**Production Solutions:**

#### Option A: Hardware Security Module (HSM)
```javascript
const key = await hsm.getKey('hedera-operator-key');
```

#### Option B: Session Key Architecture (Recommended for RDK)
```
User's Phone (Master Key)
    ↓
Generate Session Key (24h validity)
    ↓
Send to RDK Device (encrypted)
    ↓
RDK signs transactions with session key
    ↓
Limited permissions (rewards only)
```

See [FUTURE_WORK.md](FUTURE_WORK.md) for detailed production authentication design.

---

### 3. Session Security

**Session ID Generation:**
```javascript
const session_id = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
```

**Properties:**
- ✅ Cryptographically random
- ✅ Unique per session
- ✅ Tied to specific account
- ✅ Backend validates on each request

**Improvements for Production:**
- Use JWT tokens with expiration
- Sign sessions with server secret
- Implement session revocation
- Add rate limiting per session

---

### 4. Benefit Expiration

**Time-based Benefits:**
```javascript
const benefitData = {
    type: benefit_type,
    name: redemption.name,
    activatedAt: Date.now(),
    expiresAt: Date.now() + (duration * 1000)  // Unix timestamp
};
```

**Expiration Check:**
```javascript
const now = Date.now();
if (benefit.expiresAt && benefit.expiresAt < now) {
    benefits.delete(userAccount);  // Auto-expire
}
```

---

## Technology Stack

### Player Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Language | Python | 3.8+ | Application logic |
| Video Engine | GStreamer | 1.0 | Video playback |
| Display | Westeros | Latest | Wayland compositor |
| HTTP Client | requests | 2.x | API communication |
| Platform | RDK | Latest | Set-top-box OS |

### Backend Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Runtime | Node.js | 16+ | JavaScript runtime |
| Framework | Express.js | 4.x | Web framework |
| Blockchain SDK | @hiero-ledger/sdk | Latest | Hedera integration |
| Language | JavaScript (ES6+) | - | Server logic |

### Blockchain Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Network | Hedera Hashgraph | Consensus & settlement |
| Consensus | Hedera Consensus Service (HCS) | Event logging |
| Tokens | Hedera Token Service (HTS) | Fungible & non-fungible tokens |
| Accounts | Hedera Account Service | Identity & balances |

---

## Performance Considerations

### Transaction Throughput

**Hedera Limits:**
- 10,000+ TPS (transactions per second)
- 3-5 second finality
- ~$0.0001 per transaction

## Monitoring & Observability

### What Can Be Monitored

**Blockchain (via HashScan):**
- ✅ All token transfers
- ✅ All NFT mints & transfers
- ✅ All HCS events
- ✅ Account balances
- ✅ Transaction success/failure

**Backend (via Logs):**
- API request/response times
- Error rates
- Device registrations
- Benefit activations
- Achievement awards

**Player (via Console):**
- Video playback success/failure
- Network connectivity
- Balance updates
- Badge notifications

---

## Security Threat Model

### Potential Threats

| Threat | Impact | Mitigation | Status |
|--------|--------|------------|--------|
| Sybil Attack (Multiple Accounts) | High | Device fingerprinting | ✅ Implemented |
| Replay Attack (Re-submit requests) | Medium | Session IDs, timestamps | ⚠️ Partial |
| Private Key Exposure | Critical | Session keys (future) | ⚠️ Demo only |
| Session Hijacking | Medium | Signed sessions (future) | ⚠️ Basic |
| DoS (Spam requests) | Medium | Rate limiting (future) | ❌ Not implemented |

### Defense in Depth
```
Layer 1: Device Fingerprinting
    ↓
Layer 2: Account-Device Binding
    ↓
Layer 3: Session Management
    ↓
Layer 4: Backend Validation
    ↓
Layer 5: Blockchain Consensus
    ↓
Layer 6: HCS Audit Trail
```

---

## Conclusion

This architecture demonstrates a complete blockchain-integrated streaming rewards platform suitable for academic demonstration and prototyping. The modular design allows for:

- ✅ **Clear separation of concerns** (Player / Backend / Blockchain)
- ✅ **Verifiable transparency** (HCS audit trail)
- ✅ **Scalable token economy** (Hedera HTS)
- ✅ **Gamified engagement** (NFT achievements)
- ✅ **Fraud resistance** (Device fingerprinting)

For production deployment considerations, see [FUTURE_WORK.md](FUTURE_WORK.md).

---