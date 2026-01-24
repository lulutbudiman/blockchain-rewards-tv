# API Documentation

Complete REST API reference for VIEW Rewards TV backend server.

## Table of Contents
- [Overview](#overview)
- [Base URL](#base-url)
- [Authentication](#authentication)
- [Response Format](#response-format)
- [Error Codes](#error-codes)
- [Rate Limiting](#rate-limiting)
- [Endpoints](#endpoints)
  - [Health & Status](#health--status)
  - [Device Management](#device-management)
  - [Rewards & Tokens](#rewards--tokens)
  - [Redemptions & Benefits](#redemptions--benefits)
  - [Content Ratings](#content-ratings)
  - [Session Management](#session-management)
  - [NFT Badges & Achievements](#nft-badges--achievements)
  - [Analytics & History](#analytics--history)
  - [Admin Endpoints](#admin-endpoints)

---

## Overview

The backend used in this project provides a RESTful API for managing blockchain-based viewer rewards, NFT achievements, and benefit redemptions. All blockchain interactions are handled server-side using the Hedera SDK.

**Technology:**
- **Framework:** Express.js (Node.js)
- **Protocol:** HTTP/REST
- **Data Format:** JSON
- **Blockchain:** Hedera Testnet

## Authentication

**Current Implementation:**
- No authentication required (development/demo mode)
- Account ID passed in request body/query parameters

**Production Implementation:**
- JWT tokens
- API keys
- Rate limiting per account

**Request Headers:**
```http
Content-Type: application/json
```

**Future (Production):**
```http
Authorization: Bearer <JWT_TOKEN>
X-API-Key: <API_KEY>
```

---

## Response Format

### Success Response
```json
{
  "success": true,
  "data": {
    // Response data
  },
  "timestamp": "2026-01-24T12:00:00.000Z"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": {
    // Additional error details
  },
  "timestamp": "2026-01-24T12:00:00.000Z"
}
```

---

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_REQUEST` | 400 | Malformed request or missing required fields |
| `INVALID_ACCOUNT` | 400 | Invalid Hedera account ID format |
| `DEVICE_ALREADY_REGISTERED` | 403 | Device registered to different account |
| `MULTIPLE_DEVICES_NOT_ALLOWED` | 403 | Account already has registered device |
| `FRAUD_DETECTED` | 403 | Fraudulent activity detected |
| `INSUFFICIENT_BALANCE` | 400 | Not enough tokens for redemption |
| `INVALID_BENEFIT` | 400 | Unknown benefit type |
| `INVALID_SESSION` | 400 | Session not found or expired |
| `TRANSACTION_FAILED` | 500 | Blockchain transaction failed |
| `SERVER_ERROR` | 500 | Internal server error |

---

## Rate Limiting

**Current:** No rate limiting (development)

**Production:**
- 100 requests per 15 minutes per IP
- 1000 requests per hour per account
- Burst limit: 20 requests per second

**Rate Limit Headers:**
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1737673200
```

---

## Endpoints

### Health & Status

#### GET /health

Check backend server health and connectivity.

**Request:**
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Hedera Rewards Backend",
  "timestamp": "2026-01-24T12:00:00.000Z",
  "version": "2.0.0",
  "uptime": 86400
}
```

**Status Codes:**
- `200 OK` - Service is healthy
- `503 Service Unavailable` - Service is down

---

### Device Management

#### POST /device/register

Register a device to an account (one-time setup).

**Request:**
```http
POST /device/register
Content-Type: application/json

{
  "account_id": "0.0.5864245",
  "device_id": "rdk_cpu_10000000a1b2c3d4..."
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `account_id` | string | Yes | Hedera account ID (format: `0.0.XXXXXXX`) |
| `device_id` | string | Yes | Unique device identifier |

**Response (Success - New Registration):**
```json
{
  "success": true,
  "message": "Device registered",
  "status": "new",
  "account_id": "0.0.5864245",
  "device_id": "rdk_cpu_10000000a1b2c3d4..."
}
```

**Response (Success - Already Registered):**
```json
{
  "success": true,
  "message": "Device already registered",
  "status": "existing",
  "account_id": "0.0.5864245"
}
```

**Response (Error - Fraud Detected):**
```json
{
  "success": false,
  "error": "Device already registered to another account",
  "fraud_detected": true,
  "registered_to": "0.0.XXXXXXX"
}
```

**Status Codes:**
- `200 OK` - Registration successful
- `403 Forbidden` - Fraud detected or multiple devices
- `400 Bad Request` - Invalid parameters

---

#### GET /device/verify

Verify device authorization for an account.

**Request:**
```http
GET /device/verify?account_id=0.0.5864245&device_id=rdk_cpu_10000000a1b2c3d4...
```

**Query Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `account_id` | string | Yes | Hedera account ID |
| `device_id` | string | Yes | Device identifier to verify |

**Response (Verified):**
```json
{
  "verified": true,
  "message": "Device verified",
  "account_id": "0.0.5864245"
}
```

**Response (Not Verified):**
```json
{
  "verified": false,
  "message": "Device registered to different account",
  "fraud_detected": true
}
```

**Status Codes:**
- `200 OK` - Check completed

---

#### GET /device/info

Get device registration information.

**Request (Specific Account):**
```http
GET /device/info?account_id=0.0.5864245
```

**Request (All Devices - Admin):**
```http
GET /device/info
```

**Query Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `account_id` | string | No | Filter by account ID |

**Response (Single Account):**
```json
{
  "success": true,
  "account_id": "0.0.5864245",
  "device_id": "rdk_cpu_10000000a1b2c3d4...",
  "device_id_preview": "rdk_cpu_10000000a1b2c3d4...",
  "registered_at": "2026-01-24T10:00:00.000Z"
}
```

**Response (All Devices):**
```json
{
  "success": true,
  "total_devices": 150,
  "registrations": [
    {
      "device_id_preview": "rdk_cpu_10000000a1b2c3d4...",
      "account_id": "0.0.5864245"
    },
    {
      "device_id_preview": "rdk_cpu_20000000b2c3d4e5...",
      "account_id": "0.0.5864246"
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Success

---

### Rewards & Tokens

#### POST /reward

Award VIEW tokens to a user account.

**Request:**
```http
POST /reward
Content-Type: application/json

{
  "account_id": "0.0.5864245",
  "amount": 5,
  "reason": "Ad viewing"
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `account_id` | string | No | Recipient account ID (defaults to `USER_ACCOUNT`) |
| `amount` | integer | Yes | Token amount (must be positive) |
| `reason` | string | No | Reason for reward (used in transaction memo) |

**Response:**
```json
{
  "success": true,
  "amount": 5,
  "transaction_id": "0.0.5484966@1737673200.123456789",
  "hashscan_url": "https://hashscan.io/testnet/transaction/0.0.5484966@1737673200.123456789",
  "recipient": "0.0.5864245",
  "memo": "Ad viewing"
}
```

**Status Codes:**
- `200 OK` - Tokens transferred successfully
- `400 Bad Request` - Invalid amount or account
- `500 Internal Server Error` - Transaction failed

**Notes:**
- VIP multiplier is applied automatically if user has active VIP status
- Transaction is logged to HCS (Hedera Consensus Service)
- Actual amount may differ if VIP multiplier applied

---

#### GET /balance

Check token balance for an account.

**Request:**
```http
GET /balance?account_id=0.0.5864245
```

**Query Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `account_id` | string | No | Account to check (defaults to `USER_ACCOUNT`) |

**Response:**
```json
{
  "success": true,
  "account_id": "0.0.5864245",
  "balance": 1250,
  "token_id": "0.0.7379174",
  "message": "Use Hedera Mirror Node REST API for balance queries",
  "mirror_node_url": "https://testnet.mirrornode.hedera.com/api/v1/accounts/0.0.5864245"
}
```

**Status Codes:**
- `200 OK` - Success

**Notes:**
- For real-time balance, query Hedera Mirror Node directly
- Response provides Mirror Node URL for direct queries

---

### Redemptions & Benefits

#### GET /redemptions

Get available redemption options and their costs.

**Request:**
```http
GET /redemptions
```

**Response:**
```json
{
  "success": true,
  "redemptions": [
    {
      "type": "skip_ads",
      "name": "Skip Ads (1 session)",
      "description": "Skip all ads in your next viewing session",
      "cost": 50,
      "duration": null
    },
    {
      "type": "ad_free_hour",
      "name": "Ad-Free Hour",
      "description": "No ads for 1 hour",
      "cost": 75,
      "duration": 3600
    },
    {
      "type": "premium_content",
      "name": "Premium Content Access",
      "description": "Unlock premium content library",
      "cost": 100,
      "duration": null
    },
    {
      "type": "vip_day",
      "name": "VIP Status (1 day)",
      "description": "All benefits + 2x rewards for 24 hours",
      "cost": 200,
      "duration": 86400
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Success

---

#### POST /redeem

Redeem tokens for a benefit.

**Request:**
```http
POST /redeem
Content-Type: application/json

{
  "account_id": "0.0.5864245",
  "benefit_type": "vip_day"
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `account_id` | string | No | Redeeming account (defaults to `USER_ACCOUNT`) |
| `benefit_type` | string | Yes | Type of benefit (`skip_ads`, `ad_free_hour`, `premium_content`, `vip_day`) |

**Response:**
```json
{
  "success": true,
  "benefit": "VIP Status (1 day)",
  "type": "vip_day",
  "cost": 200,
  "duration": 86400,
  "activated_at": 1737673200000,
  "expires_at": 1737759600000,
  "mode": "simulation",
  "transaction_id": "0.0.5484966@1737673200.123456789"
}
```

**Response (Error - Insufficient Balance):**
```json
{
  "success": false,
  "error": "Insufficient balance",
  "required": 200,
  "available": 150
}
```

**Status Codes:**
- `200 OK` - Redemption successful
- `400 Bad Request` - Invalid benefit type or insufficient balance
- `500 Internal Server Error` - Transaction failed

**Notes:**
- In simulation mode, tokens are not actually burned (tracked locally)
- Production would require user to sign transaction
- VIP activation triggers achievement check (VIP Member badge)
- Event logged to HCS

---

#### GET /benefits

Check active benefits for an account.

**Request:**
```http
GET /benefits?account_id=0.0.5864245
```

**Query Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `account_id` | string | No | Account to check (defaults to `USER_ACCOUNT`) |

**Response (Active Benefit):**
```json
{
  "success": true,
  "has_benefits": true,
  "benefit": {
    "type": "vip_day",
    "name": "VIP Status (1 day)",
    "activated_at": 1737673200000,
    "expires_at": 1737759600000,
    "remaining_seconds": 86100
  }
}
```

**Response (No Active Benefits):**
```json
{
  "success": true,
  "has_benefits": false
}
```

**Response (Expired Benefit):**
```json
{
  "success": true,
  "has_benefits": false,
  "message": "Benefit expired"
}
```

**Status Codes:**
- `200 OK` - Success

**Notes:**
- Expired benefits are automatically removed
- `remaining_seconds` calculated in real-time

---

### Content Ratings

#### POST /rate

Submit a content rating.

**Request:**
```http
POST /rate
Content-Type: application/json

{
  "account_id": "0.0.5864245",
  "content_id": "Venice_10.mp4",
  "rating": 5,
  "session_id": "session_1737673200_abc123"
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `account_id` | string | No | Rating account (defaults to `USER_ACCOUNT`) |
| `content_id` | string | No | Content identifier (defaults to "unknown") |
| `rating` | integer | Yes | Rating value (1-5 stars) |
| `session_id` | string | No | Associated session ID |

**Response:**
```json
{
  "success": true,
  "rating": 5,
  "reward": 4,
  "base_reward": 2,
  "multiplier": 2.0,
  "vip_bonus": true,
  "transaction_id": "0.0.5484966@1737673200.123456789",
  "hashscan_url": "https://hashscan.io/testnet/transaction/0.0.5484966@1737673200.123456789"
}
```

**Status Codes:**
- `200 OK` - Rating submitted successfully
- `400 Bad Request` - Invalid rating value (must be 1-5)
- `500 Internal Server Error` - Transaction failed

**Notes:**
- Base reward: 2 VIEW
- VIP multiplier applied automatically (2x → 4 VIEW)
- Rating logged to HCS
- Triggers achievement check (Rating Master badge at 5 ratings)

---

#### GET /ratings

Get rating history.

**Request (All Ratings):**
```http
GET /ratings
```

**Request (User's Ratings):**
```http
GET /ratings?account_id=0.0.5864245
```

**Query Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `account_id` | string | No | Filter by account ID |

**Response:**
```json
{
  "success": true,
  "total_ratings": 15,
  "ratings": [
    {
      "timestamp": 1737673200000,
      "account_id": "0.0.5864245",
      "content_id": "Venice_10.mp4",
      "rating": 5,
      "session_id": "session_1737673200_abc123"
    },
    {
      "timestamp": 1737673100000,
      "account_id": "0.0.5864245",
      "content_id": "London_15.mp4",
      "rating": 4,
      "session_id": "session_1737673200_abc123"
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Success

---

### Session Management

#### POST /session/start

Start a new viewing session.

**Request:**
```http
POST /session/start
Content-Type: application/json

{
  "account_id": "0.0.5864245"
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `account_id` | string | No | Session owner (defaults to `USER_ACCOUNT`) |

**Response:**
```json
{
  "success": true,
  "session_id": "session_1737673200_abc123def456",
  "started_at": 1737673200000,
  "account_id": "0.0.5864245"
}
```

**Status Codes:**
- `200 OK` - Session created

**Notes:**
- Session ID is unique and randomly generated
- Used to track videos watched for binge bonuses

---

#### POST /session/video

Track a video watched in a session.

**Request:**
```http
POST /session/video
Content-Type: application/json

{
  "session_id": "session_1737673200_abc123def456",
  "content_id": "Venice_10.mp4"
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `session_id` | string | Yes | Session ID from `/session/start` |
| `content_id` | string | No | Video identifier (defaults to "unknown") |

**Response:**
```json
{
  "success": true,
  "videos_watched": 3,
  "session_id": "session_1737673200_abc123def456"
}
```

**Status Codes:**
- `200 OK` - Video tracked
- `400 Bad Request` - Invalid session ID

**Notes:**
- Triggers achievement checks (First Watch, Binge Watcher badges)
- Video count used for binge bonus calculation

---

#### GET /session/bonus

Check and claim binge watching bonus.

**Request:**
```http
GET /session/bonus?session_id=session_1737673200_abc123def456&account_id=0.0.5864245
```

**Query Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `session_id` | string | Yes | Session ID to check |
| `account_id` | string | No | Account ID (defaults to session owner) |

**Response (Bonus Available):**
```json
{
  "success": true,
  "bonus": 30,
  "base_bonus": 15,
  "multiplier": 2.0,
  "vip_bonus": true,
  "videos_watched": 5,
  "message": "Watched 5+ videos!",
  "transaction_id": "0.0.5484966@1737673200.123456789",
  "hashscan_url": "https://hashscan.io/testnet/transaction/0.0.5484966@1737673200.123456789"
}
```

**Response (No Bonus Yet):**
```json
{
  "success": true,
  "bonus": 0,
  "videos_watched": 2,
  "message": "Watch 1 more video(s) for bonus"
}
```

**Status Codes:**
- `200 OK` - Success

**Bonus Tiers:**
- 3 videos: 5 VIEW (VIP: 10 VIEW)
- 5 videos: 15 VIEW (VIP: 30 VIEW)

**Notes:**
- Bonus awarded only once per tier per session
- VIP multiplier applied automatically
- Logged to HCS

---

### NFT Badges & Achievements

#### GET /badges

Get achievement badges (NFTs) for an account.

**Request:**
```http
GET /badges?account_id=0.0.5864245
```

**Query Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `account_id` | string | No | Account to check (defaults to `USER_ACCOUNT`) |

**Response:**
```json
{
  "success": true,
  "account_id": "0.0.5864245",
  "owned_count": 3,
  "total_badges": 4,
  "nft_token_id": "0.0.7724797",
  "owned_badges": [
    {
      "type": "first_watch",
      "name": "First Watch",
      "description": "Watched your first video",
      "icon": "🥇",
      "requirement": null,
      "owned": true,
      "nft_serial": 1,
      "nft_id": "0.0.7724797@1",
      "hashscan_url": "https://hashscan.io/testnet/token/0.0.7724797?s=1&k=first_watch"
    },
    {
      "type": "rating_master",
      "name": "Rating Master",
      "description": "Submitted 5 ratings",
      "icon": "⭐",
      "requirement": 5,
      "owned": true,
      "nft_serial": 5,
      "nft_id": "0.0.7724797@5",
      "hashscan_url": "https://hashscan.io/testnet/token/0.0.7724797?s=5&k=rating_master"
    },
    {
      "type": "vip_member",
      "name": "VIP Member",
      "description": "Activated VIP status",
      "icon": "👑",
      "requirement": null,
      "owned": true,
      "nft_serial": 8,
      "nft_id": "0.0.7724797@8",
      "hashscan_url": "https://hashscan.io/testnet/token/0.0.7724797?s=8&k=vip_member"
    }
  ],
  "available_badges": [
    {
      "type": "binge_watcher",
      "name": "Binge Watcher",
      "description": "Watched 10 videos in total",
      "icon": "📺",
      "requirement": 10,
      "owned": false
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Success

**Notes:**
- Each badge is a unique NFT on Hedera
- NFT serial number is unique per badge mint
- Badges are non-transferable (in current implementation)

---

#### POST /achievements/check

Manually trigger achievement check and award eligible badges.

**Request:**
```http
POST /achievements/check
Content-Type: application/json

{
  "account_id": "0.0.5864245"
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `account_id` | string | No | Account to check (defaults to `USER_ACCOUNT`) |

**Response:**
```json
{
  "success": true,
  "new_badges": [
    {
      "success": true,
      "badge": "Binge Watcher",
      "icon": "📺",
      "description": "Watched 10 videos in total",
      "nft_serial": 12,
      "newly_awarded": true,
      "mint_transaction_id": "0.0.5484966@1737673200.111111111",
      "transfer_transaction_id": "0.0.5484966@1737673200.222222222"
    }
  ],
  "total_new": 1
}
```

**Response (No New Badges):**
```json
{
  "success": true,
  "new_badges": [],
  "total_new": 0
}
```

**Status Codes:**
- `200 OK` - Success
- `500 Internal Server Error` - Achievement check failed

**Notes:**
- Automatically called after certain actions (video watch, rating, redemption)
- Can be called manually to force check
- NFTs minted and transferred during check

---

### Analytics & History

#### GET /events

Get HCS event log information.

**Request:**
```http
GET /events?account_id=0.0.5864245
```

**Query Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `account_id` | string | No | Filter by account (optional) |

**Response:**
```json
{
  "success": true,
  "message": "View events on HashScan",
  "topic_id": "0.0.7724961",
  "hashscan_url": "https://hashscan.io/testnet/topic/0.0.7724961",
  "account_id": "0.0.5864245",
  "note": "Events are publicly visible on Hedera blockchain"
}
```

**Status Codes:**
- `200 OK` - Success

**Notes:**
- Events are logged to HCS Topic
- All events publicly verifiable on HashScan
- Includes: rewards, ratings, redemptions, achievements, bonuses

---

### Admin Endpoints

#### POST /admin/create-nft

Create NFT collection (one-time setup).

**Request:**
```http
POST /admin/create-nft
Content-Type: application/json
```

**Response:**
```json
{
  "success": true,
  "message": "NFT Collection created!",
  "token_id": "0.0.7724797",
  "hashscan_url": "https://hashscan.io/testnet/token/0.0.7724797",
  "next_steps": [
    "1. Copy the token_id",
    "2. Add to config: const NFT_TOKEN_ID = \"0.0.7724797\";",
    "3. Restart backend",
    "4. Remove this endpoint for security"
  ]
}
```

**Status Codes:**
- `200 OK` - NFT collection created
- `500 Internal Server Error` - Creation failed

**Notes:**
- Should be called only once during setup
- Remove endpoint after creation for security
- NFT collection used for achievement badges

---

#### POST /admin/create-hcs-topic

Create HCS topic for event logging (one-time setup).

**Request:**
```http
POST /admin/create-hcs-topic
Content-Type: application/json
```

**Response:**
```json
{
  "success": true,
  "message": "HCS Topic created!",
  "topic_id": "0.0.7724961",
  "hashscan_url": "https://hashscan.io/testnet/topic/0.0.7724961",
  "next_steps": [
    "1. Copy the topic_id",
    "2. Add to config: const HCS_TOPIC_ID = \"0.0.7724961\";",
    "3. Restart backend",
    "4. Remove this endpoint for security"
  ]
}
```

**Status Codes:**
- `200 OK` - HCS topic created
- `500 Internal Server Error` - Creation failed

**Notes:**
- Should be called only once during setup
- Remove endpoint after creation for security
- Topic used for immutable event logging

---

## Usage Examples

### Example 1: Complete User Flow
```bash
# 1. Register device
curl -X POST http://localhost:5000/device/register \
  -H "Content-Type: application/json" \
  -d '{
    "account_id": "0.0.5864245",
    "device_id": "rdk_cpu_10000000a1b2c3d4..."
  }'

# 2. Start viewing session
curl -X POST http://localhost:5000/session/start \
  -H "Content-Type: application/json" \
  -d '{
    "account_id": "0.0.5864245"
  }'
# Response: {"session_id": "session_1737673200_abc123"}

# 3. Watch ad - claim reward
curl -X POST http://localhost:5000/reward \
  -H "Content-Type: application/json" \
  -d '{
    "account_id": "0.0.5864245",
    "amount": 5,
    "reason": "Ad viewing"
  }'

# 4. Track video in session
curl -X POST http://localhost:5000/session/video \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_1737673200_abc123",
    "content_id": "Venice_10.mp4"
  }'

# 5. Watch content - claim reward
curl -X POST http://localhost:5000/reward \
  -H "Content-Type: application/json" \
  -d '{
    "account_id": "0.0.5864245",
    "amount": 10,
    "reason": "Content viewing"
  }'

# 6. Rate content
curl -X POST http://localhost:5000/rate \
  -H "Content-Type: application/json" \
  -d '{
    "account_id": "0.0.5864245",
    "content_id": "Venice_10.mp4",
    "rating": 5,
    "session_id": "session_1737673200_abc123"
  }'

# 7. Check balance
curl http://localhost:5000/balance?account_id=0.0.5864245

# 8. Check badges
curl http://localhost:5000/badges?account_id=0.0.5864245

# 9. Redeem VIP status
curl -X POST http://localhost:5000/redeem \
  -H "Content-Type: application/json" \
  -d '{
    "account_id": "0.0.5864245",
    "benefit_type": "vip_day"
  }'

# 10. Check binge bonus
curl "http://localhost:5000/session/bonus?session_id=session_1737673200_abc123&account_id=0.0.5864245"
```

---

### Example 2: Check Active Benefits
```bash
curl http://localhost:5000/benefits?account_id=0.0.5864245
```

**Response:**
```json
{
  "success": true,
  "has_benefits": true,
  "benefit": {
    "type": "vip_day",
    "name": "VIP Status (1 day)",
    "activated_at": 1737673200000,
    "expires_at": 1737759600000,
    "remaining_seconds": 82800
  }
}
```

---

### Example 3: View Rating History
```bash
curl http://localhost:5000/ratings?account_id=0.0.5864245
```

---

## SDKs & Client Libraries

### JavaScript/Node.js
```javascript
const axios = require('axios');

class ViewRewardsClient {
    constructor(baseUrl, accountId) {
        this.baseUrl = baseUrl;
        this.accountId = accountId;
    }
    
    async registerDevice(deviceId) {
        const response = await axios.post(`${this.baseUrl}/device/register`, {
            account_id: this.accountId,
            device_id: deviceId
        });
        return response.data;
    }
    
    async claimReward(amount, reason) {
        const response = await axios.post(`${this.baseUrl}/reward`, {
            account_id: this.accountId,
            amount: amount,
            reason: reason
        });
        return response.data;
    }
    
    async getBalance() {
        const response = await axios.get(`${this.baseUrl}/balance`, {
            params: { account_id: this.accountId }
        });
        return response.data;
    }
    
    async getBadges() {
        const response = await axios.get(`${this.baseUrl}/badges`, {
            params: { account_id: this.accountId }
        });
        return response.data;
    }
}

// Usage
const client = new ViewRewardsClient('http://localhost:5000', '0.0.5864245');
await client.claimReward(5, 'Ad viewing');
```

---

### Python
```python
import requests

class ViewRewardsClient:
    def __init__(self, base_url, account_id):
        self.base_url = base_url
        self.account_id = account_id
    
    def register_device(self, device_id):
        response = requests.post(
            f"{self.base_url}/device/register",
            json={
                'account_id': self.account_id,
                'device_id': device_id
            }
        )
        return response.json()
    
    def claim_reward(self, amount, reason):
        response = requests.post(
            f"{self.base_url}/reward",
            json={
                'account_id': self.account_id,
                'amount': amount,
                'reason': reason
            }
        )
        return response.json()
    
    def get_balance(self):
        response = requests.get(
            f"{self.base_url}/balance",
            params={'account_id': self.account_id}
        )
        return response.json()
    
    def get_badges(self):
        response = requests.get(
            f"{self.base_url}/badges",
            params={'account_id': self.account_id}
        )
        return response.json()

# Usage
client = ViewRewardsClient('http://localhost:5000', '0.0.5864245')
result = client.claim_reward(5, 'Ad viewing')
print(result)
```

---

## Webhooks (Future)

**Coming Soon:**
- Real-time notifications for events
- Achievement unlocked webhooks
- Balance change notifications
- Transaction status updates
```json
{
  "event": "achievement_unlocked",
  "timestamp": 1737673200000,
  "data": {
    "account_id": "0.0.5864245",
    "badge_type": "first_watch",
    "badge_name": "First Watch",
    "nft_serial": 1
  }
}
```

---

## Changelog

### Version 2.0.0 (2026-01-24)
- ✅ Added NFT badge system (`/badges`, `/achievements/check`)
- ✅ Added HCS event logging (all endpoints)
- ✅ Added device fingerprinting (`/device/*`)
- ✅ Added VIP multiplier support (2x rewards)
- ✅ Fixed rating and binge bonus multipliers

### Version 1.0.0 (2026-01-20)
- ✅ Initial release
- ✅ Token rewards (`/reward`)
- ✅ Redemptions (`/redeem`, `/redemptions`)
- ✅ Ratings (`/rate`, `/ratings`)
- ✅ Sessions (`/session/*`)
- ✅ Benefits tracking (`/benefits`)

---

## Support

**Documentation:**
- [Architecture Guide](ARCHITECTURE.md)
- [Setup Guide](SETUP_GUIDE.md)
- [User Guide](USER_GUIDE.md)
- [Future Work](FUTURE_WORK.md)

**Blockchain Verification:**
- HashScan: https://hashscan.io/testnet
- Token: https://hashscan.io/testnet/token/0.0.7379174
- NFTs: https://hashscan.io/testnet/token/0.0.7724797
- HCS: https://hashscan.io/testnet/topic/0.0.7724961

**Issues:**
- GitHub: https://github.com/yourusername/view-rewards-tv/issues

---

**API Version:** 2.0.0  
**Last Updated:** January 24, 2026  
**Blockchain:** Hedera Testnet