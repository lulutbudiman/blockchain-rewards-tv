# Future Work & Enhancements

Roadmap for production deployment, feature enhancements, and architectural improvements for VIEW Rewards TV.

## Table of Contents
- [Overview](#overview)
- [Phase 1: Production Readiness](#phase-1-production-readiness)
- [Phase 2: Smart Contract Integration](#phase-2-smart-contract-integration)
- [Phase 3: Advanced Authentication](#phase-3-advanced-authentication)
- [Phase 4: Scalability & Performance](#phase-4-scalability--performance)
- [Phase 5: Analytics & Insights](#phase-5-analytics--insights)
- [Phase 6: Enhanced Features](#phase-6-enhanced-features)
- [Phase 7: Cross-Chain & Interoperability](#phase-7-cross-chain--interoperability)
- [Research & Experimental](#research--experimental)
- [Timeline Estimates](#timeline-estimates)

---

## Overview

The current implementation serves as a **proof-of-concept** demonstrating blockchain integration in streaming media platforms. This document outlines the path from academic prototype to production-ready system.

**Current Status:**
- ✅ Functional token economy
- ✅ NFT achievement system
- ✅ Device fingerprinting
- ✅ HCS audit trail
- ⚠️ In-memory storage (not persistent)
- ⚠️ Hardcoded credentials (not secure)
- ⚠️ Single-server backend (not scalable)
- ⚠️ Python player (not optimized)

---

## Phase 1: Production Readiness

### 1.1 Persistent Storage Implementation

**Current Issue:**
- All data (sessions, benefits, device registry) stored in RAM
- Lost on server restart
- Not suitable for production

---

### 1.2 Secure Credential Management

**Current Issue:**
- Private keys hardcoded in source code
- Major security vulnerability
- Cannot be open-sourced safely

**Solution Options:**

#### Option A: Environment Variables (Basic)
#### Option B: AWS Secrets Manager / Google Cloud KMS
#### Option C: Hardware Security Module (HSM)


## Phase 2: Smart Contract Integration

### 2.1 Why Smart Contracts?

**Benefits:**
- ✅ **Trustless:** Code executes automatically, no backend trust needed
- ✅ **Transparent:** Anyone can verify reward logic
- ✅ **Immutable:** Rules can't be changed arbitrarily
- ✅ **Decentralized:** System can run without centralized server

**Tradeoffs:**
- ⚠️ **Complexity:** Solidity learning curve
- ⚠️ **Gas Costs:** Deployment and execution fees
- ⚠️ **Inflexibility:** Can't easily update logic
- ⚠️ **Debugging:** Harder to troubleshoot

---

### 2.2 Smart Contract Architecture

**Hybrid Approach (Recommended):**
```
Backend (Off-Chain)                Smart Contracts (On-Chain)
├─ Content delivery               ├─ Reward claiming (with proof)
├─ Session tracking               ├─ Benefit redemption
├─ Device fingerprinting          ├─ Achievement verification
├─ Proof generation               ├─ Token distribution rules
└─ UI/UX logic                    └─ Governance rules
```

**Why Hybrid?**
- Keep expensive operations off-chain (proof generation, validation)
- Put critical logic on-chain (token distribution, redemption)
- Balance cost, security, and flexibility

---

### 2.3 Reward Distribution Contract
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@hedera/contracts/HederaTokenService.sol";
import "@hedera/contracts/HederaResponseCodes.sol";

contract ViewRewardsDistributor is HederaTokenService {
    
    // Token addresses
    address public viewToken;
    address public nftCollection;
    
    // Backend signer address (for proof verification)
    address public backendSigner;
    
    // Reward amounts
    uint256 public constant AD_REWARD = 5;
    uint256 public constant CONTENT_REWARD = 10;
    uint256 public constant RATING_REWARD = 2;
    
    // Redemption costs
    uint256 public constant SKIP_ADS_COST = 50;
    uint256 public constant AD_FREE_HOUR_COST = 75;
    uint256 public constant PREMIUM_CONTENT_COST = 100;
    uint256 public constant VIP_STATUS_COST = 200;
    
    // Nonce tracking (prevent replay attacks)
    mapping(address => uint256) public nonces;
    
    // VIP status tracking
    mapping(address => uint256) public vipExpiresAt;
    
    // Events
    event RewardClaimed(address indexed user, uint256 amount, string rewardType);
    event BenefitRedeemed(address indexed user, string benefitType, uint256 cost);
    event VIPActivated(address indexed user, uint256 expiresAt);
    
    constructor(
        address _viewToken,
        address _nftCollection,
        address _backendSigner
    ) {
        viewToken = _viewToken;
        nftCollection = _nftCollection;
        backendSigner = _backendSigner;
    }
    
    /**
     * Claim reward with backend-signed proof
     */
    function claimReward(
        uint256 amount,
        string memory rewardType,
        uint256 nonce,
        bytes memory signature
    ) external {
        // Verify signature
        bytes32 messageHash = keccak256(abi.encodePacked(
            msg.sender,
            amount,
            rewardType,
            nonce
        ));
        
        bytes32 ethSignedHash = keccak256(abi.encodePacked(
            "\x19Ethereum Signed Message:\n32",
            messageHash
        ));
        
        address signer = recoverSigner(ethSignedHash, signature);
        require(signer == backendSigner, "Invalid signature");
        
        // Verify nonce (prevent replay)
        require(nonce == nonces[msg.sender], "Invalid nonce");
        nonces[msg.sender]++;
        
        // Apply VIP multiplier if active
        uint256 finalAmount = amount;
        if (isVIP(msg.sender)) {
            finalAmount = amount * 2;
        }
        
        // Transfer tokens
        int responseCode = HederaTokenService.transferToken(
            viewToken,
            address(this),
            msg.sender,
            int64(uint64(finalAmount))
        );
        
        require(
            responseCode == HederaResponseCodes.SUCCESS,
            "Token transfer failed"
        );
        
        emit RewardClaimed(msg.sender, finalAmount, rewardType);
    }
    
    /**
     * Redeem benefit (burn tokens)
     */
    function redeemBenefit(string memory benefitType) external {
        uint256 cost;
        
        if (keccak256(bytes(benefitType)) == keccak256(bytes("vip_day"))) {
            cost = VIP_STATUS_COST;
            
            // Activate VIP for 24 hours
            vipExpiresAt[msg.sender] = block.timestamp + 86400;
            emit VIPActivated(msg.sender, vipExpiresAt[msg.sender]);
            
        } else if (keccak256(bytes(benefitType)) == keccak256(bytes("premium_content"))) {
            cost = PREMIUM_CONTENT_COST;
        } else if (keccak256(bytes(benefitType)) == keccak256(bytes("ad_free_hour"))) {
            cost = AD_FREE_HOUR_COST;
        } else if (keccak256(bytes(benefitType)) == keccak256(bytes("skip_ads"))) {
            cost = SKIP_ADS_COST;
        } else {
            revert("Invalid benefit type");
        }
        
        // Burn tokens (transfer to treasury/burn address)
        int responseCode = HederaTokenService.transferToken(
            viewToken,
            msg.sender,
            address(this),  // Treasury
            int64(uint64(cost))
        );
        
        require(
            responseCode == HederaResponseCodes.SUCCESS,
            "Token transfer failed"
        );
        
        emit BenefitRedeemed(msg.sender, benefitType, cost);
    }
    
    /**
     * Check if user has active VIP status
     */
    function isVIP(address user) public view returns (bool) {
        return vipExpiresAt[user] > block.timestamp;
    }
    
    /**
     * Recover signer from signature
     */
    function recoverSigner(
        bytes32 ethSignedHash,
        bytes memory signature
    ) internal pure returns (address) {
        require(signature.length == 65, "Invalid signature length");
        
        bytes32 r;
        bytes32 s;
        uint8 v;
        
        assembly {
            r := mload(add(signature, 32))
            s := mload(add(signature, 64))
            v := byte(0, mload(add(signature, 96)))
        }
        
        return ecrecover(ethSignedHash, v, r, s);
    }
    
    /**
     * Update backend signer (governance function)
     */
    function updateBackendSigner(address newSigner) external {
        require(msg.sender == backendSigner, "Only current signer");
        backendSigner = newSigner;
    }
}
```

---

### 2.4 Backend Integration with Smart Contract
```javascript
// Generate proof for user
async function generateRewardProof(accountId, amount, rewardType) {
    const nonce = await contract.nonces(accountId);
    
    // Create message to sign
    const messageHash = ethers.utils.solidityKeccak256(
        ['address', 'uint256', 'string', 'uint256'],
        [accountId, amount, rewardType, nonce]
    );
    
    // Sign with backend private key
    const signature = await backendSigner.signMessage(
        ethers.utils.arrayify(messageHash)
    );
    
    return {
        amount,
        rewardType,
        nonce: nonce.toString(),
        signature
    };
}

// API endpoint to get proof
app.post('/proof/reward', async (req, res) => {
    const { account_id, amount, reason } = req.body;
    
    const proof = await generateRewardProof(account_id, amount, reason);
    
    res.json({
        success: true,
        proof: proof,
        contract_address: REWARD_CONTRACT_ADDRESS
    });
});
```

---

### 2.5 Player Integration with Smart Contract
```python
# Player calls smart contract directly
def claim_reward_from_contract(self, amount, reason):
    # Get proof from backend
    response = requests.post(
        f"{self.backend_url}/proof/reward",
        json={
            'account_id': self.account_id,
            'amount': amount,
            'reason': reason
        }
    )
    
    proof = response.json()['proof']
    
    # Call smart contract (using Web3 or Hedera SDK)
    contract_call = ContractExecuteTransaction()
        .setContractId(REWARD_CONTRACT_ID)
        .setGas(100000)
        .setFunction("claimReward",
            ContractFunctionParameters()
                .addUint256(proof['amount'])
                .addString(proof['rewardType'])
                .addUint256(proof['nonce'])
                .addBytes(bytes.fromhex(proof['signature'][2:]))
        )
        .execute(client)
    
    receipt = contract_call.getReceipt(client)
    
    print(f"✅ Claimed {amount} VIEW via smart contract!")
    return receipt
```

---

### 2.6 Smart Contract Deployment
```javascript
// Deploy script
const { ContractCreateFlow } = require("@hiero-ledger/sdk");

async function deployContract() {
    // Compile Solidity contract
    const bytecode = compiledContract.bytecode;
    
    // Deploy to Hedera
    const contractCreate = new ContractCreateFlow()
        .setBytecode(bytecode)
        .setGas(100000)
        .setConstructorParameters(
            new ContractFunctionParameters()
                .addAddress(VIEW_TOKEN_ID)
                .addAddress(NFT_TOKEN_ID)
                .addAddress(BACKEND_SIGNER_ADDRESS)
        )
        .execute(client);
    
    const receipt = await contractCreate.getReceipt(client);
    const contractId = receipt.contractId;
    
    console.log(`Contract deployed: ${contractId}`);
    return contractId;
}
```

**Estimated Effort:** 3-4 weeks

---

## Phase 3: Advanced Authentication

### 3.1 Session Key Architecture

**Current Problem:**
- User's master private key needed for every transaction
- Not practical for continuous device use
- Security risk if device compromised

**Solution: Session Keys**
```
User's Phone (Master Wallet)
    │
    │ 1. User approves device
    │
    ├──► Generate Session Key
    │    • 24-hour validity
    │    • Limited permissions (rewards only)
    │    • Device-specific
    │
    │ 2. Send encrypted session key to RDK
    │
RDK Device
    │
    ├──► Store session key (encrypted)
    │
    │ 3. Sign reward transactions with session key
    │
    ├──► Backend validates session key
    │
    │ 4. Session expires after 24h
    │
    └──► User re-authorizes from phone
```

---

### 3.2 Session Key Implementation
```solidity
// Smart contract with session key support
contract SessionKeyManager {
    
    struct SessionKey {
        address keyAddress;
        uint256 expiresAt;
        uint256 dailyLimit;
        uint256 usedToday;
        bool revoked;
    }
    
    mapping(address => mapping(address => SessionKey)) public sessionKeys;
    
    event SessionKeyCreated(
        address indexed masterKey,
        address indexed sessionKey,
        uint256 expiresAt
    );
    
    event SessionKeyRevoked(
        address indexed masterKey,
        address indexed sessionKey
    );
    
    /**
     * Create session key (signed by master key)
     */
    function createSessionKey(
        address sessionKeyAddress,
        uint256 duration,
        uint256 dailyLimit
    ) external {
        sessionKeys[msg.sender][sessionKeyAddress] = SessionKey({
            keyAddress: sessionKeyAddress,
            expiresAt: block.timestamp + duration,
            dailyLimit: dailyLimit,
            usedToday: 0,
            revoked: false
        });
        
        emit SessionKeyCreated(msg.sender, sessionKeyAddress, block.timestamp + duration);
    }
    
    /**
     * Revoke session key
     */
    function revokeSessionKey(address sessionKeyAddress) external {
        sessionKeys[msg.sender][sessionKeyAddress].revoked = true;
        emit SessionKeyRevoked(msg.sender, sessionKeyAddress);
    }
    
    /**
     * Validate session key
     */
    function isValidSessionKey(
        address masterKey,
        address sessionKey,
        uint256 amount
    ) public view returns (bool) {
        SessionKey memory key = sessionKeys[masterKey][sessionKey];
        
        if (key.keyAddress == address(0)) return false;
        if (key.revoked) return false;
        if (key.expiresAt < block.timestamp) return false;
        if (key.usedToday + amount > key.dailyLimit) return false;
        
        return true;
    }
}
```

---

### 3.3 Mobile App for Session Management

**React Native / Flutter App:**
```javascript
// Mobile app code
import { Wallet } from 'ethers';

class SessionKeyManager {
    
    async createSessionKeyForDevice(deviceId) {
        // Generate new session key
        const sessionWallet = Wallet.createRandom();
        
        // Master wallet signs transaction to authorize session key
        const tx = await contract.createSessionKey(
            sessionWallet.address,
            86400,  // 24 hours
            1000    // 1000 VIEW daily limit
        );
        
        await tx.wait();
        
        // Encrypt session key private key with device-specific password
        const encrypted = await encrypt(
            sessionWallet.privateKey,
            deviceId
        );
        
        // Send encrypted key to backend
        await api.registerSessionKey(deviceId, encrypted);
        
        // Show QR code for RDK to scan
        return {
            qrCode: generateQRCode(encrypted),
            expiresAt: Date.now() + 86400000
        };
    }
    
    async revokeSessionKey(sessionKeyAddress) {
        const tx = await contract.revokeSessionKey(sessionKeyAddress);
        await tx.wait();
        
        console.log('Session key revoked');
    }
    
    async listActiveSessions() {
        const sessions = await api.getActiveSessions(masterAddress);
        return sessions.map(s => ({
            deviceId: s.deviceId,
            expiresAt: s.expiresAt,
            dailyLimit: s.dailyLimit,
            usedToday: s.usedToday
        }));
    }
}
```

---

### 3.4 QR Code Authorization Flow
```
┌─────────────┐                          ┌─────────────┐
│ RDK Device  │                          │Mobile App   │
└──────┬──────┘                          └──────┬──────┘
       │                                        │
       │ 1. Show "Scan QR to authorize"        │
       │ ◄─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │
       │                                        │
       │                                        │ 2. User scans QR
       │                                        │ ──────────────►
       │                                        │
       │                                        │ 3. App shows device info
       │                                        │    "Authorize RDK-Living-Room?"
       │                                        │
       │                                        │ 4. User approves
       │                                        │ ──────────────►
       │                                        │
       │                                        │ 5. Generate session key
       │                                        │ ──────────────►
       │                                        │
       │ 6. Encrypted session key               │
       │ ◄──────────────────────────────────────│
       │                                        │
       │ 7. Store session key (encrypted)       │
       │ ──────────────►                        │
       │                                        │
       │ 8. "Device authorized! Valid 24h"      │
       │ ◄─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │
       │                                        │
```

**Estimated Effort:** 4-6 weeks (including mobile app)

---

### 3.5 Multi-Factor Authentication (MFA)

**For High-Value Transactions:**
```javascript
// Require MFA for redemptions over 100 VIEW
app.post('/redeem', requireMFA, async (req, res) => {
    const { benefit_type, mfa_code } = req.body;
    
    // Verify MFA code
    const isValid = await verifyMFACode(req.user.account_id, mfa_code);
    if (!isValid) {
        return res.status(401).json({ error: 'Invalid MFA code' });
    }
    
    // Process redemption
    // ...
});

// TOTP-based MFA
function verifyMFACode(accountId, code) {
    const secret = getUserMFASecret(accountId);
    const token = speakeasy.totp({
        secret: secret,
        encoding: 'base32'
    });
    
    return token === code;
}
```

**Estimated Effort:** 1-2 weeks

---

## Phase 5: Analytics & Insights

### 5.1 User Analytics Dashboard

**Web Dashboard Features:**
```
┌─────────────────────────────────────────────────────────┐
│  VIEW Rewards TV - Analytics Dashboard                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Total Users: 10,523        Active Today: 1,247         │
│  Total Tokens Earned: 2.5M  Total Redeemed: 850K        │
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Token Distribution (Last 30 Days)                │  │
│  │  [Line Chart: tokens earned over time]           │  │
│  └───────────────────────────────────────────────────┘  │
│                                                          │
│  ┌──────────────────────┐  ┌──────────────────────────┐ │
│  │  Top Content         │  │  Redemption Breakdown    │ │
│  │  1. Show A - 5.2K    │  │  VIP: 42%               │ │
│  │  2. Show B - 4.1K    │  │  Premium: 28%           │ │
│  │  3. Show C - 3.8K    │  │  Ad-Free: 20%           │ │
│  └──────────────────────┘  │  Skip Ads: 10%          │ │
│                            └──────────────────────────┘ │
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Achievement Progress                              │  │
│  │  First Watch: 95%   Rating Master: 62%            │  │
│  │  Binge Watcher: 38% VIP Member: 15%               │  │
│  └───────────────────────────────────────────────────┘  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Tech Stack:**
- **Frontend:** React + Chart.js / D3.js
- **Backend:** Same Node.js API + analytics endpoints
- **Data:** PostgreSQL aggregates + real-time queries

**Estimated Effort:** 2-3 weeks

---

### 5.2 Advertiser Insights

**Transparent Ad Analytics:**
```javascript
// API endpoint for advertisers
app.get('/analytics/ad-campaign/:campaignId', async (req, res) => {
    const { campaignId } = req.params;
    
    // Query HCS topic for all ad views
    const adViews = await queryHCS({
        topic: HCS_TOPIC_ID,
        filter: {
            type: 'reward',
            reason: 'Ad viewing',
            campaign_id: campaignId
        }
    });
    
    // Aggregate metrics
    const metrics = {
        total_impressions: adViews.length,
        total_completions: adViews.filter(v => v.completed).length,
        total_skips: adViews.filter(v => v.skipped).length,
        completion_rate: calculateCompletionRate(adViews),
        unique_viewers: new Set(adViews.map(v => v.account_id)).size,
        geographic_distribution: calculateGeoDistribution(adViews),
        time_distribution: calculateTimeDistribution(adViews),
        blockchain_proof: `https://hashscan.io/testnet/topic/${HCS_TOPIC_ID}`
    };
    
    res.json(metrics);
});
```

**Verifiable Metrics:**
- ✅ Every impression on blockchain (HCS)
- ✅ Advertiser can independently verify
- ✅ No trust required
- ✅ Real-time analytics

**Estimated Effort:** 1-2 weeks

---

### 5.3 Content Creator Analytics

**Track Content Performance:**
```javascript
// Content metrics
app.get('/analytics/content/:contentId', async (req, res) => {
    const { contentId } = req.params;
    
    const metrics = {
        total_views: await countViews(contentId),
        average_rating: await calculateAvgRating(contentId),
        completion_rate: await calculateCompletionRate(contentId),
        revenue_generated: await calculateRevenue(contentId),
        viewer_demographics: await getViewerDemographics(contentId),
        peak_viewing_times: await getPeakTimes(contentId)
    };
    
    res.json(metrics);
});
```

**Estimated Effort:** 1 week

---

## Phase 6: Enhanced Features

### 6.1 Social Features

**Share Achievements:**
```python
# Player code
def share_badge(self, badge_type):
    badge = self.badges[badge_type]
    
    # Generate shareable link
    share_url = f"https://viewrewards.tv/badge/{badge['nft_serial']}"
    
    # Generate image
    badge_image = generate_badge_image(badge)
    
    # Share options
    print(f"""
    🎉 Share your achievement!
    
    Link: {share_url}
    
    Share on:
    1. Twitter
    2. Facebook
    3. Copy link
    """)
```

**Leaderboards:**
```javascript
// Global leaderboard
app.get('/leaderboard', async (req, res) => {
    const { timeframe } = req.query;  // 'daily', 'weekly', 'all-time'
    
    const leaderboard = await db.query(`
        SELECT 
            account_id,
            SUM(amount) as total_earned,
            COUNT(*) as total_transactions,
            RANK() OVER (ORDER BY SUM(amount) DESC) as rank
        FROM rewards
        WHERE created_at > NOW() - INTERVAL '${timeframe}'
        GROUP BY account_id
        ORDER BY total_earned DESC
        LIMIT 100
    `);
    
    res.json({ leaderboard: leaderboard.rows });
});
```

**Estimated Effort:** 2-3 weeks

---

### 6.2 Referral Program

**Invite Friends, Earn Tokens:**
```javascript
// Referral system
const REFERRAL_BONUS = 50;  // Both parties get 50 VIEW

app.post('/referral/create', async (req, res) => {
    const { account_id } = req.body;
    
    // Generate unique referral code
    const code = generateReferralCode(account_id);
    
    await db.query(
        'INSERT INTO referral_codes (account_id, code, created_at) VALUES ($1, $2, NOW())',
        [account_id, code]
    );
    
    res.json({
        referral_code: code,
        referral_link: `https://viewrewards.tv/join?ref=${code}`
    });
});

app.post('/referral/redeem', async (req, res) => {
    const { new_account_id, referral_code } = req.body;
    
    // Find referrer
    const referrer = await db.query(
        'SELECT account_id FROM referral_codes WHERE code = $1',
        [referral_code]
    );
    
    if (referrer.rows.length === 0) {
        return res.status(400).json({ error: 'Invalid referral code' });
    }
    
    const referrer_id = referrer.rows[0].account_id;
    
    // Award bonus to both parties
    await transferTokens(new_account_id, REFERRAL_BONUS);  // New user
    await transferTokens(referrer_id, REFERRAL_BONUS);     // Referrer
    
    // Log referral
    await logToHCS('referral', {
        referrer: referrer_id,
        new_user: new_account_id,
        bonus: REFERRAL_BONUS
    });
    
    res.json({
        success: true,
        bonus: REFERRAL_BONUS,
        referrer: referrer_id
    });
});
```

**Estimated Effort:** 1-2 weeks

---

### 6.3 Tiered Membership System

**Beyond VIP:**
```javascript
// Membership tiers
const TIERS = {
    BRONZE: { minBalance: 100, multiplier: 1.2, perks: ['Ad skip'] },
    SILVER: { minBalance: 500, multiplier: 1.5, perks: ['Ad skip', 'Premium content'] },
    GOLD: { minBalance: 1000, multiplier: 1.8, perks: ['Ad skip', 'Premium', 'Early access'] },
    PLATINUM: { minBalance: 5000, multiplier: 2.0, perks: ['All perks', 'Exclusive content', 'Governance votes'] }
};

function getUserTier(totalEarned) {
    if (totalEarned >= TIERS.PLATINUM.minBalance) return 'PLATINUM';
    if (totalEarned >= TIERS.GOLD.minBalance) return 'GOLD';
    if (totalEarned >= TIERS.SILVER.minBalance) return 'SILVER';
    if (totalEarned >= TIERS.BRONZE.minBalance) return 'BRONZE';
    return 'BASIC';
}
```

**Estimated Effort:** 1 week

---

### 6.4 Dynamic Pricing

**Adjust rewards based on demand:**
```javascript
// Surge pricing for popular content
function calculateDynamicReward(contentId, baseReward) {
    const demand = getContentDemand(contentId);
    
    // Higher demand = higher rewards (to attract viewers)
    if (demand > 1000) return baseReward * 1.5;
    if (demand > 500) return baseReward * 1.2;
    return baseReward;
}

// Time-based bonuses
function getTimeBonusMultiplier() {
    const hour = new Date().getHours();
    
    // Off-peak hours (2am-6am) get bonus to fill inventory
    if (hour >= 2 && hour < 6) return 1.3;
    
    // Peak hours (8pm-11pm) normal rates
    if (hour >= 20 && hour < 23) return 1.0;
    
    return 1.1;
}
```

**Estimated Effort:** 1 week

---

## Phase 7: Cross-Chain & Interoperability

### 7.1 Multi-Chain Support

**Bridge to Other Blockchains:**
```
Hedera (Primary)
    │
    ├──► Ethereum (Mainnet)
    │    └─ VIEW ERC-20 token
    │
    ├──► Polygon (Layer 2)
    │    └─ Cheaper transactions
    │
    └──► Binance Smart Chain
         └─ Wider DeFi integration
```

**Cross-Chain Bridge:**
```solidity
// Bridge contract
contract ViewTokenBridge {
    
    event TokensLocked(address indexed user, uint256 amount, string targetChain);
    event TokensUnlocked(address indexed user, uint256 amount, string sourceChain);
    
    function lockTokens(uint256 amount, string memory targetChain) external {
        // Lock tokens on Hedera
        viewToken.transferFrom(msg.sender, address(this), amount);
        
        // Emit event for bridge oracle
        emit TokensLocked(msg.sender, amount, targetChain);
        
        // Oracle mints equivalent on target chain
    }
    
    function unlockTokens(
        address user,
        uint256 amount,
        string memory sourceChain,
        bytes memory proof
    ) external {
        // Verify burn proof from source chain
        require(verifyBurnProof(proof), "Invalid proof");
        
        // Unlock tokens
        viewToken.transfer(user, amount);
        
        emit TokensUnlocked(user, amount, sourceChain);
    }
}
```

**Estimated Effort:** 6-8 weeks

---

### 7.2 NFT Marketplace Integration

**List Badges for Sale:**
```javascript
// Integration with OpenSea / HashAxis
app.post('/marketplace/list', async (req, res) => {
    const { account_id, nft_serial, price } = req.body;
    
    // Create marketplace listing
    const listing = await marketplace.createListing({
        token_id: NFT_TOKEN_ID,
        serial: nft_serial,
        seller: account_id,
        price: price,
        currency: 'HBAR'
    });
    
    res.json({
        listing_url: `https://hashaxis.com/nft/${NFT_TOKEN_ID}/${nft_serial}`,
        listing_id: listing.id
    });
});
```

**Estimated Effort:** 2-3 weeks

---

## Phase 8: Player Rewrite (C/C++)

### 8.1 Why Rewrite Player?

**Current (Python):**
- ✅ Rapid development
- ✅ Easy to debug
- ❌ Slower performance
- ❌ Higher memory usage
- ❌ Not typical for production STBs

**Target (C/C++):**
- ✅ Native STB language
- ✅ Better performance
- ✅ Lower memory footprint
- ✅ Production-ready
- ❌ More complex
- ❌ Longer development time

---

### 8.2 C++ Player Architecture
```cpp
// Main player class
class ViewRewardsPlayer {
private:
    GstElement* pipeline;
    WesterosManager* compositor;
    BlockchainWallet* wallet;
    HttpClient* httpClient;
    DeviceFingerprint* deviceId;
    
public:
    ViewRewardsPlayer(const std::string& backendUrl, 
                      const std::string& accountId);
    
    void initialize();
    void playContent(const std::string& videoPath);
    void playAd(const std::string& adPath);
    bool claimReward(int amount, const std::string& reason);
    void showMenu();
    void checkBalance();
    void viewBadges();
    void redeemBenefit(const std::string& benefitType);
    
    ~ViewRewardsPlayer();
};

// Blockchain wallet interface
class BlockchainWallet {
private:
    std::string accountId;
    std::string backendUrl;
    HttpClient* client;
    
public:
    int getBalance();
    bool sendReward(int amount, const std::string& reason);
    std::vector<Badge> getBadges();
    bool redeemBenefit(const std::string& type);
};

// Device fingerprinting
class DeviceFingerprint {
public:
    static std::string getDeviceId() {
        // Try CPU serial
        std::string cpuSerial = readCPUSerial();
        if (!cpuSerial.empty()) {
            return "rdk_cpu_" + cpuSerial;
        }
        
        // Try machine ID
        std::string machineId = readMachineId();
        if (!machineId.empty()) {
            return "rdk_machine_" + machineId;
        }
        
        // Fallback to MAC
        std::string mac = getMACAddress();
        return "rdk_mac_" + mac;
    }
};
```

**Estimated Effort:** 4-6 weeks

---

### 8.3 Performance Comparison

| Metric | Python | C++ |
|--------|--------|-----|
| Startup time | 2-3s | <1s |
| Memory usage | 80-120MB | 20-40MB |
| Video decode CPU | 40-60% | 20-30% |
| API call latency | 50-100ms | 10-20ms |
| Binary size | N/A (interpreted) | 2-5MB |

---

See other documentation:
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design details
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API reference
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Installation instructions