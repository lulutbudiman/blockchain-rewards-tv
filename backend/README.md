# Backend Server

Node.js/Express backend for VIEW Rewards TV.

## Quick Start
```bash
npm install
node hedera_backend_nodejs.js
```

## Configuration

Edit `hedera_backend_nodejs.js` and update:
```javascript
const OPERATOR_ID = '0.0.YOUR_ACCOUNT';
const OPERATOR_KEY = 'YOUR_PRIVATE_KEY';
const USER_PRIVATE_KEY = 'USER_PRIVATE_KEY';
const TOKEN_ID = '0.0.YOUR_TOKEN_ID';
const NFT_TOKEN_ID = '0.0.YOUR_NFT_TOKEN_ID';
const HCS_TOPIC_ID = '0.0.YOUR_HCS_TOPIC_ID';
```

## Environment Variables (Recommended)

Create `.env` file:
```
HEDERA_OPERATOR_ID=0.0.YOUR_ACCOUNT
HEDERA_OPERATOR_KEY=YOUR_PRIVATE_KEY
HEDERA_USER_KEY=USER_PRIVATE_KEY
HEDERA_TOKEN_ID=0.0.YOUR_TOKEN_ID
HEDERA_NFT_TOKEN_ID=0.0.YOUR_NFT_TOKEN_ID
HEDERA_HCS_TOPIC_ID=0.0.YOUR_HCS_TOPIC_ID
```

Then install dotenv:
```bash
npm install dotenv
```

## API Endpoints

See [API_DOCUMENTATION.md](../docs/API_DOCUMENTATION.md)

## Running
```bash
# Production
npm start

# Development (auto-restart)
npm run dev
```

Server runs on: http://localhost:5000