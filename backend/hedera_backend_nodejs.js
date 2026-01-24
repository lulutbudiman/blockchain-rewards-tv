const { 
    Client, 
    PrivateKey, 
    AccountId, 
    TokenId,
    TopicId,
    TransferTransaction,
    TokenMintTransaction,
    TokenAssociateTransaction,
    NftId,
    TopicCreateTransaction,  // ← Add this
    TopicMessageSubmitTransaction  // ← Add this
} = require('@hiero-ledger/sdk');

const express = require('express');

// Configuration
const OPERATOR_ID = '0.0.5484966';  // Treasury account
const OPERATOR_KEY = '3030020100300706052b8104000a042204201ed7e8d655abdcb8f2aac568151a59dd3e8b0ef2af493d894d1acaaf4a14b89d';  // Your DER encoded private key
const USER_PRIVATE_KEY = '3030020100300706052b8104000a04220420e7c45f485c1d87375188bb91cd98499e00434ed13c483f200fd876be6f915fda';  // ← Add this
const TOKEN_ID = '0.0.7379174';
const NFT_TOKEN_ID = '0.0.7724797';  // NFT Collection
const HCS_TOPIC_ID = '0.0.7724961';  // ← HCS topic ID
const TREASURY_ACCOUNT = '0.0.5484966';
const USER_ACCOUNT = '0.0.5864245';

// Connect to Hedera Testnet
const client = Client.forTestnet();
client.setOperator(
    AccountId.fromString(OPERATOR_ID),
    PrivateKey.fromStringDer(OPERATOR_KEY)
);

// Express setup
const app = express();
app.use(express.json());

const PORT = 5000;

// In-memory storage
const ratings = [];
const sessions = new Map();
const benefits = new Map();
const deviceRegistry = new Map();
const nftAwards = new Map(); // account_id -> Set of badge types awarded
const nftSerials = new Map(); // account_id -> Map of badge_type -> serial_number

/**
 * Achievement definitions
 */
const ACHIEVEMENTS = {
    first_watch: {
        name: 'First Watch',
        description: 'Watched your first video',
        icon: '🥇',
        metadata: Buffer.from('first_watch')  // ← Much shorter!
    },
    rating_master: {
        name: 'Rating Master',
        description: 'Submitted 5 ratings',
        icon: '⭐',
        requirement: 5,
        metadata: Buffer.from('rating_master')
    },
    binge_watcher: {
        name: 'Binge Watcher',
        description: 'Watched 10 videos in total',
        icon: '📺',
        requirement: 10,
        metadata: Buffer.from('binge_watcher')
    },
    vip_member: {
        name: 'VIP Member',
        description: 'Activated VIP status',
        icon: '👑',
        metadata: Buffer.from('vip_member')
    }
};

/**
 * Check if account has VIP status and return multiplier
 */
function getRewardMultiplier(accountId) {
    const benefit = benefits.get(accountId);
    
    if (!benefit) {
        return 1.0;
    }
    
    // Check if benefit is still valid
    const now = Date.now();
    if (benefit.expiresAt && benefit.expiresAt < now) {
        benefits.delete(accountId);
        return 1.0;
    }
    
    // VIP gets 2x multiplier
    if (benefit.type === 'vip_day') {
        return 2.0;
    }
    
    return 1.0;
}

/**
 * Check if user has earned an achievement badge
 */
function hasAchievement(accountId, badgeType) {
    if (!nftAwards.has(accountId)) {
        return false;
    }
    return nftAwards.get(accountId).has(badgeType);
}

/**
 * Associate NFT token with user account (one-time setup)
 */
async function associateNFTWithUser(accountId) {
    try {
        console.log(`   🔗 Checking NFT association for ${accountId}...`);
        
        const tokenId = TokenId.fromString(NFT_TOKEN_ID);
        const userId = AccountId.fromString(accountId);
        const userKey = PrivateKey.fromStringDer(USER_PRIVATE_KEY);
        
        // Create association transaction
        const associateTx = await new TokenAssociateTransaction()
            .setAccountId(userId)
            .setTokenIds([tokenId])
            .freezeWith(client);
        
        // Sign with user's key
        const signedTx = await associateTx.sign(userKey);
        
        // Execute
        const txResponse = await signedTx.execute(client);
        const receipt = await txResponse.getReceipt(client);
        
        console.log(`   ✅ NFT token associated with user account`);
        return true;
        
    } catch (error) {
        // Check if already associated
        if (error.message && error.message.includes('TOKEN_ALREADY_ASSOCIATED_TO_ACCOUNT')) {
            console.log(`   ✅ NFT token already associated`);
            return true;
        }
        
        console.error(`   ❌ Association failed: ${error.message}`);
        return false;
    }
}

/**
 * Mint NFT badge and transfer to user
 */
async function mintAndTransferNFT(accountId, badgeType) {
    try {
        const achievement = ACHIEVEMENTS[badgeType];
        
        console.log('   🎨 Minting NFT...');
        
        // First, ensure user account is associated with NFT token
        const isAssociated = await associateNFTWithUser(accountId);
        
        if (!isAssociated) {
            console.log('   ⚠️  Skipping NFT transfer - association failed');
            return null;
        }
        
        // Mint NFT
        const tokenId = TokenId.fromString(NFT_TOKEN_ID);
        const supplyKey = PrivateKey.fromStringDer(OPERATOR_KEY);
        
        const mintTx = await new TokenMintTransaction()
            .setTokenId(tokenId)
            .setMetadata([achievement.metadata])
            .execute(client);
        
        const mintRx = await mintTx.getReceipt(client);
        const serial = mintRx.serials[0].toNumber();
        const mintTxId = mintTx.transactionId.toString();
        
        console.log(`   ✅ NFT minted! Serial: ${serial}`);
        console.log(`   Mint TX: ${mintTxId}`);
        
        // Transfer NFT from treasury to user
        console.log(`   📤 Transferring NFT to user...`);
        
        const treasuryId = AccountId.fromString(TREASURY_ACCOUNT);
        const userId = AccountId.fromString(accountId);
        
        const transferTx = await new TransferTransaction()
            .addNftTransfer(tokenId, serial, treasuryId, userId)
            .setTransactionMemo(`Achievement: ${badgeType}`)
            .execute(client);
        
        const transferRx = await transferTx.getReceipt(client);
        const transferTxId = transferTx.transactionId.toString();
        
        console.log(`   ✅ NFT transferred to user!`);
        console.log(`   Transfer TX: ${transferTxId}`);
        console.log(`   🔗 HashScan: https://hashscan.io/testnet/transaction/${transferTxId}`);
        console.log(`   🎨 NFT View: https://hashscan.io/testnet/token/${NFT_TOKEN_ID}?s=${serial}`);
        
        return { 
            serial, 
            mint_transaction_id: mintTxId,
            transfer_transaction_id: transferTxId,
            owner: accountId
        };
        
    } catch (error) {
        console.error('   ❌ NFT minting/transfer failed:', error.message);
        return null;
    }
}

/**
 * Award achievement badge (NFT) to user
 */
async function awardBadge(accountId, badgeType) {
    try {
        // Check if already awarded
        if (hasAchievement(accountId, badgeType)) {
            return { success: true, already_owned: true };
        }
        
        const achievement = ACHIEVEMENTS[badgeType];
        if (!achievement) {
            return { success: false, error: 'Unknown badge type' };
        }
        
        console.log(`\n🏆 Awarding badge: ${achievement.name}`);
        console.log(`   User: ${accountId}`);
        console.log(`   Badge: ${achievement.icon} ${achievement.name}`);
        
        // Mint NFT
        const serial = await mintAndTransferNFT(accountId, badgeType);
        
        // Store badge award
        if (!nftAwards.has(accountId)) {
            nftAwards.set(accountId, new Set());
            nftSerials.set(accountId, new Map());
        }
        nftAwards.get(accountId).add(badgeType);
        
        if (serial !== null) {
            nftSerials.get(accountId).set(badgeType, serial);
        }
        
        console.log('   ✅ Badge awarded!');

        // Log to HCS
	await logToHCS('achievement', {
    	    account_id: accountId,
    	    badge_type: badgeType,
    	    badge_name: achievement.name,
    	    nft_serial: serial,
    	    nft_token_id: NFT_TOKEN_ID
	});
        
        return {
            success: true,
            badge: achievement.name,
            icon: achievement.icon,
            description: achievement.description,
            nft_serial: serial,
            newly_awarded: true
        };
        
    } catch (error) {
        console.error('   ❌ Badge award failed:', error.message);
        return { success: false, error: error.message };
    }
}

/**
 * Get total videos watched by account
 */
function getTotalVideosWatched(accountId) {
    let total = 0;
    for (const session of sessions.values()) {
        if (session.account_id === accountId) {
            total += session.videos_watched.length;
        }
    }
    return total;
}

/**
 * Check achievements for an account
 */
async function checkAchievements(accountId) {
    const newBadges = [];
    
    // Check first watch
    const videosWatched = getTotalVideosWatched(accountId);
    if (videosWatched >= 1 && !hasAchievement(accountId, 'first_watch')) {
        const result = await awardBadge(accountId, 'first_watch');
        if (result.newly_awarded) {
            newBadges.push(result);
        }
    }
    
    // Check binge watcher
    if (videosWatched >= 10 && !hasAchievement(accountId, 'binge_watcher')) {
        const result = await awardBadge(accountId, 'binge_watcher');
        if (result.newly_awarded) {
            newBadges.push(result);
        }
    }
    
    // Check rating master
    const userRatings = ratings.filter(r => r.account_id === accountId);
    if (userRatings.length >= 5 && !hasAchievement(accountId, 'rating_master')) {
        const result = await awardBadge(accountId, 'rating_master');
        if (result.newly_awarded) {
            newBadges.push(result);
        }
    }
    
    // Check VIP member
    const benefit = benefits.get(accountId);
    if (benefit && benefit.type === 'vip_day' && !hasAchievement(accountId, 'vip_member')) {
        const result = await awardBadge(accountId, 'vip_member');
        if (result.newly_awarded) {
            newBadges.push(result);
        }
    }
    
    return newBadges;
}

// Health check
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        service: 'Hedera Rewards Backend',
        timestamp: new Date().toISOString()
    });
});

// Device registration endpoint
app.post('/device/register', (req, res) => {
    try {
        const { account_id, device_id } = req.body;
        
        if (!account_id || !device_id) {
            return res.status(400).json({
                success: false,
                error: 'Missing account_id or device_id'
            });
        }
        
        console.log('\n🔐 Device registration:');
        console.log(`   Account: ${account_id}`);
        console.log(`   Device: ${device_id.substring(0, 30)}...`);
        
        // Check if device is already registered
        if (deviceRegistry.has(device_id)) {
            const registeredAccount = deviceRegistry.get(device_id);
            
            if (registeredAccount === account_id) {
                // Same device, same account - OK
                console.log('   ✅ Device already registered to this account');
                return res.json({
                    success: true,
                    message: 'Device already registered',
                    status: 'existing'
                });
            } else {
                // Same device, different account - FRAUD ATTEMPT
                console.log('   ❌ FRAUD DETECTED: Device registered to different account!');
                console.log(`      Registered to: ${registeredAccount}`);
                console.log(`      Attempted by: ${account_id}`);
                
                return res.status(403).json({
                    success: false,
                    error: 'Device already registered to another account',
                    fraud_detected: true
                });
            }
        }
        
        // Check if account has a device already
        let accountHasDevice = false;
        for (const [devId, accId] of deviceRegistry.entries()) {
            if (accId === account_id) {
                accountHasDevice = true;
                console.log('   ⚠️  Account already has a registered device');
                console.log(`      Existing device: ${devId.substring(0, 30)}...`);
                break;
            }
        }
        
        if (accountHasDevice) {
            return res.status(403).json({
                success: false,
                error: 'Account already has a registered device',
                multiple_devices_not_allowed: true
            });
        }
        
        // Register new device
        deviceRegistry.set(device_id, account_id);
        console.log('   ✅ Device registered successfully');
        
        res.json({
            success: true,
            message: 'Device registered',
            status: 'new'
        });
        
    } catch (error) {
        console.error('   ❌ Registration error:', error.message);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Device verification endpoint
app.get('/device/verify', (req, res) => {
    try {
        const { account_id, device_id } = req.query;
        
        if (!account_id || !device_id) {
            return res.status(400).json({
                verified: false,
                error: 'Missing parameters'
            });
        }
        
        const registeredAccount = deviceRegistry.get(device_id);
        
        if (!registeredAccount) {
            return res.json({
                verified: false,
                message: 'Device not registered'
            });
        }
        
        if (registeredAccount === account_id) {
            return res.json({
                verified: true,
                message: 'Device verified'
            });
        } else {
            return res.json({
                verified: false,
                message: 'Device registered to different account',
                fraud_detected: true
            });
        }
        
    } catch (error) {
        res.status(500).json({
            verified: false,
            error: error.message
        });
    }
});

// Get device info (for debugging)
app.get('/device/info', (req, res) => {
    const { account_id } = req.query;
    
    if (account_id) {
        // Find device for this account
        for (const [devId, accId] of deviceRegistry.entries()) {
            if (accId === account_id) {
                return res.json({
                    success: true,
                    account_id: account_id,
                    device_id: devId,
                    device_id_preview: devId.substring(0, 30) + '...'
                });
            }
        }
        return res.json({
            success: true,
            account_id: account_id,
            device_id: null,
            message: 'No device registered'
        });
    }
    
    // Return all registrations (admin view)
    const registrations = [];
    for (const [devId, accId] of deviceRegistry.entries()) {
        registrations.push({
            device_id_preview: devId.substring(0, 30) + '...',
            account_id: accId
        });
    }
    
    res.json({
        success: true,
        total_devices: deviceRegistry.size,
        registrations: registrations
    });
});

// Award reward
app.post('/reward', async (req, res) => {
    try {
        const { account_id, amount, reason } = req.body;
        
        console.log('\n💰 Reward request:');
        console.log(`   Account: ${account_id || USER_ACCOUNT}`);
        console.log(`   Amount: ${amount} VIEW`);
        console.log(`   Reason: ${reason || 'N/A'}`);
        
        const tokenId = TokenId.fromString(TOKEN_ID);
        const treasuryId = AccountId.fromString(TREASURY_ACCOUNT);
        const userId = AccountId.fromString(account_id || USER_ACCOUNT);
        
        // Transfer tokens
        const transaction = await new TransferTransaction()
            .addTokenTransfer(tokenId, treasuryId, -amount)
            .addTokenTransfer(tokenId, userId, amount)
            .setTransactionMemo(reason || 'Reward')
            .execute(client);
        
        const receipt = await transaction.getReceipt(client);
        const txId = transaction.transactionId.toString();
        
        console.log('   ✅ Transaction successful!');
        console.log(`   TX ID: ${txId}`);
        
        // Log to HCS
        await logToHCS('reward', {
            account_id: account_id || USER_ACCOUNT,
            amount: amount,
            reason: reason || 'Reward',
            transaction_id: txId
        });
        
        res.json({
            success: true,
            amount: amount,
            transaction_id: txId,
            hashscan_url: `https://hashscan.io/testnet/transaction/${txId}`
        });
        
    } catch (error) {
        console.error('   ❌ Transaction failed:', error.message);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Get balance
app.get('/balance', async (req, res) => {
    try {
        const { account_id } = req.query;
        const accountToCheck = account_id || USER_ACCOUNT;
        
        console.log(`\n💳 Balance check: ${accountToCheck}`);
        
        res.json({
            success: true,
            account_id: accountToCheck,
            message: 'Use Hedera Mirror Node REST API for balance queries'
        });
        
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Redemption catalog
const REDEMPTIONS = [
    {
        type: 'skip_ads',
        name: 'Skip Ads (1 session)',
        description: 'Skip all ads in your next viewing session',
        cost: 50,
        duration: null
    },
    {
        type: 'ad_free_hour',
        name: 'Ad-Free Hour',
        description: 'No ads for 1 hour',
        cost: 75,
        duration: 3600
    },
    {
        type: 'premium_content',
        name: 'Premium Content Access',
        description: 'Unlock premium content library',
        cost: 100,
        duration: null
    },
    {
        type: 'vip_day',
        name: 'VIP Status (1 day)',
        description: 'All benefits + 2x rewards for 24 hours',
        cost: 200,
        duration: 86400
    }
];

// Get redemptions catalog
app.get('/redemptions', (req, res) => {
    res.json({
        success: true,
        redemptions: REDEMPTIONS
    });
});

// Redeem benefit
app.post('/redeem', async (req, res) => {
    try {
        const { account_id, benefit_type } = req.body;
        
        const userAccount = account_id || USER_ACCOUNT;
        
        console.log('\n🎁 Redemption request:');
        console.log(`   User: ${userAccount}`);
        console.log(`   Benefit: ${benefit_type}`);
        
        // Find redemption
        const redemption = REDEMPTIONS.find(r => r.type === benefit_type);
        
        if (!redemption) {
            return res.status(400).json({
                success: false,
                error: 'Invalid benefit type'
            });
        }
        
        console.log(`   Cost: ${redemption.cost} VIEW`);
        
        // Transfer tokens FROM user TO treasury (burn)
        const tokenId = TokenId.fromString(TOKEN_ID);
        const treasuryId = AccountId.fromString(TREASURY_ACCOUNT);
        const userId = AccountId.fromString(userAccount);
        
        // NOTE: In simulation mode (no user private key), we just track locally
        // In production, user would sign this transaction
        console.log('   💡 Simulation mode: Assuming user has sufficient balance');
        
        // For now, we do a treasury->user transfer of 0 just to test the flow
        // In production with user private key, this would be user->treasury
        try {
            const transaction = await new TransferTransaction()
                .addTokenTransfer(tokenId, treasuryId, -0)
                .addTokenTransfer(tokenId, userId, 0)
                .setTransactionMemo(`Redemption: ${benefit_type}`)
                .execute(client);
            
            const receipt = await transaction.getReceipt(client);
            const txId = transaction.transactionId.toString();
            
            console.log('   ✅ Transaction simulated');
            console.log(`   TX ID: ${txId}`);
        } catch (txError) {
            console.log('   ⚠️  Transaction skipped (simulation mode)');
        }
        
        // Activate benefit
        const benefitData = {
            type: benefit_type,
            name: redemption.name,
            activatedAt: Date.now(),
            expiresAt: redemption.duration ? Date.now() + (redemption.duration * 1000) : null
        };
        
        benefits.set(userAccount, benefitData);
        
        console.log('   ✅ Benefit activated!');
        if (benefitData.expiresAt) {
            const expiryDate = new Date(benefitData.expiresAt);
            console.log(`   ⏱️  Expires: ${expiryDate.toLocaleString()}`);
        }

        // Log to HCS
	await logToHCS('redemption', {
    	    account_id: userAccount,
    	    benefit_type: benefit_type,
    	    benefit_name: redemption.name,
    	    cost: redemption.cost,
    	    expires_at: benefitData.expiresAt
	});
        
        // Check for VIP achievement
        if (benefit_type === 'vip_day') {
            await checkAchievements(userAccount);
        }
        
        res.json({
            success: true,
            benefit: redemption.name,
            type: benefit_type,
            cost: redemption.cost,
            duration: redemption.duration,
            expires_at: benefitData.expiresAt,
            mode: 'simulation'
        });
        
    } catch (error) {
        console.error('   ❌ Redemption failed:', error.message);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Check active benefits
app.get('/benefits', (req, res) => {
    try {
        const { account_id } = req.query;
        const userAccount = account_id || USER_ACCOUNT;
        
        const benefit = benefits.get(userAccount);
        
        if (!benefit) {
            return res.json({
                success: true,
                has_benefits: false
            });
        }
        
        // Check if expired
        const now = Date.now();
        if (benefit.expiresAt && benefit.expiresAt < now) {
            benefits.delete(userAccount);
            return res.json({
                success: true,
                has_benefits: false,
                message: 'Benefit expired'
            });
        }
        
        // Calculate remaining time
        const remainingSeconds = benefit.expiresAt 
            ? Math.floor((benefit.expiresAt - now) / 1000)
            : null;
        
        res.json({
            success: true,
            has_benefits: true,
            benefit: {
                type: benefit.type,
                name: benefit.name,
                activated_at: benefit.activatedAt,
                expires_at: benefit.expiresAt,
                remaining_seconds: remainingSeconds
            }
        });
        
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Submit rating with VIP multiplier
app.post('/rate', async (req, res) => {
    try {
        const { account_id, content_id, rating, session_id } = req.body;
        
        if (!rating || rating < 1 || rating > 5) {
            return res.status(400).json({
                error: 'Rating must be between 1 and 5'
            });
        }
        
        const userAccount = account_id || USER_ACCOUNT;
        const contentIdentifier = content_id || 'unknown';
        
        console.log('\n⭐ Rating submission:');
        console.log(`   User: ${userAccount}`);
        console.log(`   Content: ${contentIdentifier}`);
        console.log(`   Rating: ${rating} stars`);
        
        // Store rating
        const ratingEntry = {
            timestamp: Date.now(),
            account_id: userAccount,
            content_id: contentIdentifier,
            rating: rating,
            session_id: session_id || 'unknown'
        };
        
        ratings.push(ratingEntry);
        
        console.log('   ✅ Rating recorded');

        // Log to HCS
	await logToHCS('rating', {
    	    account_id: userAccount,
    	    content_id: contentIdentifier,
    	    rating: rating,
    	    session_id: session_id || 'unknown'
	});
        
        // Check for achievements
        await checkAchievements(userAccount);
        
        // Award tokens for rating with VIP multiplier
        const baseReward = 2; // +2 VIEW for rating
        const multiplier = getRewardMultiplier(userAccount);
        const reward = Math.floor(baseReward * multiplier);
        
        if (multiplier > 1.0) {
            console.log(`   ✨ VIP multiplier: ${baseReward} × ${multiplier} = ${reward} VIEW`);
        }
        
        console.log(`   🎁 Awarding ${reward} VIEW for rating...`);
        
        const tokenId = TokenId.fromString(TOKEN_ID);
        const treasuryId = AccountId.fromString(TREASURY_ACCOUNT);
        const userId = AccountId.fromString(userAccount);
        
        const transaction = await new TransferTransaction()
            .addTokenTransfer(tokenId, treasuryId, -reward)
            .addTokenTransfer(tokenId, userId, reward)
            .setTransactionMemo(`Rating reward: ${rating} stars${multiplier > 1 ? ' (VIP)' : ''}`)
            .execute(client);
        
        const receipt = await transaction.getReceipt(client);
        const txId = transaction.transactionId.toString();
        
        console.log('   ✅ Reward transferred!');
        console.log(`   Transaction: ${txId}`);
        
        res.json({
            success: true,
            rating: rating,
            reward: reward,
            base_reward: baseReward,
            multiplier: multiplier,
            vip_bonus: multiplier > 1.0,
            transaction_id: txId,
            hashscan_url: `https://hashscan.io/testnet/transaction/${txId}`
        });
        
    } catch (error) {
        console.error('   ❌ Rating failed:', error.message);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Session tracking
app.post('/session/start', (req, res) => {
    const session_id = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    sessions.set(session_id, {
        videos_watched: [],
        start_time: Date.now(),
        account_id: req.body.account_id || USER_ACCOUNT
    });
    
    console.log(`\n📺 New session started: ${session_id}`);
    
    res.json({
        success: true,
        session_id: session_id
    });
});

app.post('/session/video', async (req, res) => {
    const { session_id, content_id } = req.body;
    
    if (!session_id || !sessions.has(session_id)) {
        return res.status(400).json({
            error: 'Invalid session'
        });
    }
    
    const session = sessions.get(session_id);
    session.videos_watched.push({
        content_id: content_id || 'unknown',
        timestamp: Date.now()
    });
    
    console.log(`   📹 Video tracked in session ${session_id} (total: ${session.videos_watched.length})`);
    
    // Check for achievements
    await checkAchievements(session.account_id);
    
    res.json({
        success: true,
        videos_watched: session.videos_watched.length
    });
});

// Session bonus with VIP multiplier
app.get('/session/bonus', async (req, res) => {
    try {
        const { session_id, account_id } = req.query;
        
        if (!session_id || !sessions.has(session_id)) {
            return res.json({
                success: true,
                bonus: 0,
                videos_watched: 0
            });
        }
        
        const session = sessions.get(session_id);
        const count = session.videos_watched.length;
        
        let baseBonus = 0;
        let message = '';
        
        if (count >= 5) {
            baseBonus = 15; // 5 VIEW for 3rd + 10 VIEW for 5th = 15 total
            message = 'Watched 5+ videos!';
        } else if (count >= 3) {
            baseBonus = 5;
            message = 'Watched 3+ videos!';
        }
        
        if (baseBonus > 0) {
            const userAccount = account_id || session.account_id || USER_ACCOUNT;
            
            // Apply VIP multiplier
            const multiplier = getRewardMultiplier(userAccount);
            const bonus = Math.floor(baseBonus * multiplier);
            
            console.log(`\n🎉 Binge bonus triggered!`);
            console.log(`   Session: ${session_id}`);
            console.log(`   Videos: ${count}`);
            console.log(`   Base bonus: ${baseBonus} VIEW`);
            
            if (multiplier > 1.0) {
                console.log(`   ✨ VIP multiplier: ${baseBonus} × ${multiplier} = ${bonus} VIEW`);
            } else {
                console.log(`   Bonus: ${bonus} VIEW`);
            }
            
            // Award bonus
            const tokenId = TokenId.fromString(TOKEN_ID);
            const treasuryId = AccountId.fromString(TREASURY_ACCOUNT);
            const userId = AccountId.fromString(userAccount);
            
            const transaction = await new TransferTransaction()
                .addTokenTransfer(tokenId, treasuryId, -bonus)
                .addTokenTransfer(tokenId, userId, bonus)
                .setTransactionMemo(`Binge bonus: ${count} videos${multiplier > 1 ? ' (VIP)' : ''}`)
                .execute(client);
            
            const receipt = await transaction.getReceipt(client);
            const txId = transaction.transactionId.toString();
            
            console.log('   ✅ Bonus awarded!');
            console.log(`   Transaction: ${txId}`);

            // Log to HCS
	    await logToHCS('binge_bonus', {
    		account_id: userAccount,
    		session_id: session_id,
    		videos_watched: count,
    		bonus_amount: bonus,
    		vip_multiplier: multiplier > 1.0
	    });
            
            res.json({
                success: true,
                bonus: bonus,
                base_bonus: baseBonus,
                multiplier: multiplier,
                vip_bonus: multiplier > 1.0,
                videos_watched: count,
                message: message,
                transaction_id: txId,
                hashscan_url: `https://hashscan.io/testnet/transaction/${txId}`
            });
        } else {
            res.json({
                success: true,
                bonus: 0,
                videos_watched: count,
                message: `Watch ${3 - count} more video(s) for bonus`
            });
        }
        
    } catch (error) {
        console.error('   ❌ Bonus calculation failed:', error.message);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Get ratings history
app.get('/ratings', (req, res) => {
    const account_id = req.query.account_id;
    
    let filteredRatings = ratings;
    if (account_id) {
        filteredRatings = ratings.filter(r => r.account_id === account_id);
    }
    
    res.json({
        success: true,
        total_ratings: filteredRatings.length,
        ratings: filteredRatings
    });
});

// Get user's badges
app.get('/badges', (req, res) => {
    try {
        const { account_id } = req.query;
        const userAccount = account_id || USER_ACCOUNT;
        
        const ownedBadges = [];
        const availableBadges = [];
        
        for (const [badgeType, achievement] of Object.entries(ACHIEVEMENTS)) {
            const owned = hasAchievement(userAccount, badgeType);
            
            const badgeInfo = {
                type: badgeType,
                name: achievement.name,
                description: achievement.description,
                icon: achievement.icon,
                requirement: achievement.requirement || null,
                owned: owned
            };
            
            if (owned) {
                // Add NFT serial if available
                const serialMap = nftSerials.get(userAccount);
                if (serialMap && serialMap.has(badgeType)) {
                    badgeInfo.nft_serial = serialMap.get(badgeType);
                    badgeInfo.nft_id = `${NFT_TOKEN_ID}@${serialMap.get(badgeType)}`;
                    badgeInfo.hashscan_url = `https://hashscan.io/testnet/token/${NFT_TOKEN_ID}?s=${serialMap.get(badgeType)}&k=${badgeType}`;
                }
                
                ownedBadges.push(badgeInfo);
            } else {
                availableBadges.push(badgeInfo);
            }
        }
        
        res.json({
            success: true,
            account_id: userAccount,
            owned_count: ownedBadges.length,
            total_badges: Object.keys(ACHIEVEMENTS).length,
            owned_badges: ownedBadges,
            available_badges: availableBadges,
            nft_token_id: NFT_TOKEN_ID
        });
        
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Check and award achievements
app.post('/achievements/check', async (req, res) => {
    try {
        const { account_id } = req.body;
        const userAccount = account_id || USER_ACCOUNT;
        
        console.log(`\n🏆 Checking achievements for ${userAccount}...`);
        
        const newBadges = await checkAchievements(userAccount);
        
        res.json({
            success: true,
            new_badges: newBadges,
            total_new: newBadges.length
        });
        
    } catch (error) {
        console.error('   ❌ Achievement check failed:', error.message);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

/**
 * Create HCS topic for logging events (run once)
 */
async function createHCSTopic() {
    try {
        console.log('\n📝 Creating HCS Topic...');
        
        const topicCreateTx = await new TopicCreateTransaction()
            .setTopicMemo("VIEW Rewards TV - Event Log")
            .setAdminKey(PrivateKey.fromStringDer(OPERATOR_KEY))
            .setSubmitKey(PrivateKey.fromStringDer(OPERATOR_KEY))
            .execute(client);
        
        const topicCreateRx = await topicCreateTx.getReceipt(client);
        const topicId = topicCreateRx.topicId;
        
        console.log('✅ HCS Topic Created!');
        console.log(`   Topic ID: ${topicId}`);
        console.log(`   Memo: VIEW Rewards TV - Event Log`);
        console.log('\n⚠️  IMPORTANT: Copy this Topic ID and add it to your config:');
        console.log(`   const HCS_TOPIC_ID = '${topicId}';`);
        console.log('\n   View on HashScan: https://hashscan.io/testnet/topic/' + topicId);
        
        return topicId.toString();
        
    } catch (error) {
        console.error('❌ Topic creation failed:', error.message);
        throw error;
    }
}

// TEMPORARY: Create HCS topic (call once)
app.post('/admin/create-hcs-topic', async (req, res) => {
    try {
        const topicId = await createHCSTopic();
        
        res.json({
            success: true,
            message: 'HCS Topic created!',
            topic_id: topicId,
            hashscan_url: `https://hashscan.io/testnet/topic/${topicId}`,
            next_steps: [
                '1. Copy the topic_id',
                '2. Add to config: const HCS_TOPIC_ID = "' + topicId + '";',
                '3. Restart backend',
                '4. Remove this endpoint for security'
            ]
        });
        
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

/**
 * Log event to HCS (Hedera Consensus Service)
 */
async function logToHCS(eventType, eventData) {
    try {
        const topicId = TopicId.fromString(HCS_TOPIC_ID);
        
        // Create event payload
        const event = {
            type: eventType,
            timestamp: Date.now(),
            data: eventData
        };
        
        const message = JSON.stringify(event);
        
        console.log(`   📝 Logging to HCS: ${eventType}`);
        
        // Submit message to topic
        const submitTx = await new TopicMessageSubmitTransaction()
            .setTopicId(topicId)
            .setMessage(message)
            .execute(client);
        
        const submitRx = await submitTx.getReceipt(client);
        const txId = submitTx.transactionId.toString();
        
        console.log(`   ✅ Logged to HCS`);
        console.log(`   TX: ${txId}`);
        
        return {
            success: true,
            transaction_id: txId,
            sequence_number: submitRx.topicSequenceNumber
        };
        
    } catch (error) {
        console.error(`   ⚠️  HCS logging failed: ${error.message}`);
        return { success: false, error: error.message };
    }
}

// Get HCS event log for account
app.get('/events', async (req, res) => {
    try {
        const { account_id } = req.query;
        
        res.json({
            success: true,
            message: 'View events on HashScan',
            topic_id: HCS_TOPIC_ID,
            hashscan_url: `https://hashscan.io/testnet/topic/${HCS_TOPIC_ID}`,
            account_id: account_id || 'all',
            note: 'Events are publicly visible on Hedera blockchain'
        });
        
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Start server
async function main() {
    try {
        console.log('\n' + '='.repeat(60));
        console.log('🚀 HEDERA REWARDS BACKEND - Phase 2: NFT Badges');
        console.log('='.repeat(60));
        console.log('\nConfiguration:');
        console.log(`  Operator: ${OPERATOR_ID}`);
        console.log(`  Token: ${TOKEN_ID} (VIEW)`);
        console.log(`  NFT Collection: ${NFT_TOKEN_ID} (BADGE)`);
        console.log(`  Treasury: ${TREASURY_ACCOUNT}`);
        console.log(`  User: ${USER_ACCOUNT}`);
        console.log(`  Network: Hedera Testnet`);
        
        app.listen(PORT, '0.0.0.0', () => {
            console.log(`\n✅ Server running on http://0.0.0.0:${PORT}`);
            console.log('\nEndpoints:');
            console.log('  GET  /health            - Health check');
            console.log('  POST /device/register   - Register device to account');
            console.log('  GET  /device/verify     - Verify device authorization');
            console.log('  GET  /device/info       - Get device registration info');
            console.log('  POST /reward            - Award tokens');
            console.log('  POST /redeem            - Redeem tokens for benefits');
            console.log('  GET  /benefits          - Check active benefits');
            console.log('  GET  /redemptions       - List redemption catalog');
            console.log('  GET  /balance           - Check balance');
            console.log('  POST /rate              - Submit content rating (+2 VIEW, VIP: +4)');
            console.log('  POST /session/start     - Start viewing session');
            console.log('  POST /session/video     - Track video in session');
            console.log('  GET  /session/bonus     - Check/claim binge bonus (VIP: 2x)');
            console.log('  GET  /ratings           - View ratings history');
            console.log('  GET  /badges            - Get achievement badges (NFTs)');
            console.log('  POST /achievements/check- Check and award achievements');
            console.log('\n🎨 NFT Collection:');
            console.log(`  Token ID: ${NFT_TOKEN_ID}`);
            console.log(`  HashScan: https://hashscan.io/testnet/token/${NFT_TOKEN_ID}`);
            console.log('\n📝 HCS Event Log:');
	    console.log(`  Topic ID: ${HCS_TOPIC_ID}`);
	    console.log(`  HashScan: https://hashscan.io/testnet/topic/${HCS_TOPIC_ID}`);
	    console.log(`  All events publicly logged and verifiable`);
            console.log('\n' + '='.repeat(60));
        });
        
    } catch (error) {
        console.error('❌ Startup failed:', error);
        process.exit(1);
    }
}

main();