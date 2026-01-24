# User Guide

Complete guide for using VIEW Rewards TV - earn tokens by watching content and redeem them for benefits.

## Table of Contents
- [Getting Started](#getting-started)
- [Main Menu](#main-menu)
- [Watching Content](#watching-content)
- [Earning Tokens](#earning-tokens)
- [Rating Content](#rating-content)
- [Achievement Badges](#achievement-badges)
- [Redemption Center](#redemption-center)
- [Checking Your Balance](#checking-your-balance)
- [Understanding Benefits](#understanding-benefits)
- [Tips & Strategies](#tips--strategies)
- [Troubleshooting](#troubleshooting)
- [FAQs](#faqs)

---

## Getting Started

### First Launch

When you start VIEW Rewards TV for the first time, the system will:

1. **Perform Device Security Check**
```
   🔐 Device Security Check...
      Device ID: rdk_cpu_10000000a1b2c3d4...
      ✅ Device registered (new)
```
   - Your device is registered to your account
   - One device per account (prevents fraud)
   - You'll see "registered (new)" on first launch
   - Future launches show "verified (existing)"

2. **Start Viewing Session**
```
   📺 Starting viewing session...
      📺 Session started: session_1737673200_abc...
```
   - Tracks videos you watch for binge bonuses
   - Session persists until you exit

3. **Check Active Benefits**
```
   🎁 Checking active benefits...
      No active benefits
```
   - Shows if you have VIP, ad-free hour, etc.
   - Benefits display remaining time

4. **Check Blockchain Balance**
```
   💳 Checking balance...
      Balance: 0 VIEW
```
   - Your current VIEW token balance
   - Updated from Hedera blockchain

---

## Main Menu

After initialization, you'll see the main menu:
```
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

### Menu Options Explained

| Option | Description |
|--------|-------------|
| **1. Watch Content** | Browse and watch videos, earn tokens |
| **2. Redemption Center** | Spend tokens on benefits (ad-free, VIP, etc.) |
| **3. Achievement Badges** | View your earned NFT badges |
| **4. Check Balance** | See your token balance and active benefits |
| **0. Exit** | Close the application |

---

## Watching Content

### Step 1: Select "Watch Content" (Option 1)

You'll see the content library:
```
============================================================
📺 CONTENT LIBRARY
============================================================

  Regular Content:
  1. Venice_10.mp4 (Free)
  2. London_15.mp4 (Free)
  3. Paris_20.mp4 (Free)

  Premium Content:
  4. 🔒 Premium_Show_S01E01.mp4 (Requires Premium Access - 100 VIEW)
  5. 🔒 Exclusive_Documentary.mp4 (Requires Premium Access - 100 VIEW)

  0. Back to main menu
============================================================

  Select content:
```

### Step 2: Choose a Video

**Example: Select Option 1 (Venice_10.mp4)**

---

### Step 3: Watch Advertisement (if applicable)

**If you don't have ad-skip benefits:**
```
────────────────────────────────────────────────────────────
📺 ADVERTISEMENT
────────────────────────────────────────────────────────────
  📁 File: ad.mp4
  ⏱️  Duration: 15.0s
  🎁 Watch complete ad: +5 VIEW tokens!
  ⏭️  Skip after 5s

  ▶️  Ad playing...
  Press 's' + Enter to skip

  [████████████░░░░░░░░] 7.5s/15.0s [Skip: 's']
```

**Two Options:**

1. **Watch Complete Ad**
   - Wait for ad to finish
   - Earn **5 VIEW tokens** (VIP: 10 VIEW)
   - Ad completes automatically

2. **Skip After 5 Seconds**
   - Wait for skip timer (5s)
   - Press `s` then `Enter`
   - Earn **0 VIEW tokens**
   - Saves time but no reward

**If you have ad-skip benefit:**
```
────────────────────────────────────────────────────────────
📺 ADVERTISEMENT
────────────────────────────────────────────────────────────
  ✨ Ad skipped (active benefit)
  🎁 No reward (benefit used)
────────────────────────────────────────────────────────────
```

---

### Step 4: Watch Main Content
```
────────────────────────────────────────────────────────────
🎬 MAIN CONTENT
────────────────────────────────────────────────────────────
  📁 File: Venice_10.mp4
  ⏱️  Duration: 60.0s
  🎁 Complete: +10 VIEW tokens!

  ▶️  Content playing...
  Ctrl+C to stop

  [████████████████████] ⏱️  32.5s/60.0s
```

**Earning Rules:**

- **Complete video:** +10 VIEW (VIP: 20 VIEW)
- **Partial viewing (30s+):** +1-5 VIEW based on watch time
- **Less than 30s:** 0 VIEW

**Stopping Playback:**
- Press `Ctrl+C` to stop early
- You'll still earn partial rewards if watched 30s+

---

### Step 5: Rate the Content

After watching, you'll be prompted to rate:
```
────────────────────────────────────────────────────────────
⭐ RATE THIS CONTENT
────────────────────────────────────────────────────────────
  How would you rate this content?
  1 ⭐ - Poor
  2 ⭐⭐ - Fair
  3 ⭐⭐⭐ - Good
  4 ⭐⭐⭐⭐ - Very Good
  5 ⭐⭐⭐⭐⭐ - Excellent
  0 - Skip rating
────────────────────────────────────────────────────────────

  Your rating (0-5):
```

**Rating Rewards:**
- Submit any rating (1-5): **+2 VIEW** (VIP: 4 VIEW)
- Skip rating (0): No reward
- Rating helps improve content recommendations

---

### Step 6: View Session Summary
```
════════════════════════════════════════════════════════════
                      SESSION SUMMARY
════════════════════════════════════════════════════════════

  📺 Ad watched (15.0s):     +5 VIEW
  🎬 Content (60.0s):        +10 VIEW
  ⭐ Rating submitted:       +2 VIEW

  ──────────────────────────────────────────────────────────
  💰 Session earnings:  +17 VIEW

  🏆 Checking for new achievements...

  🎉 NEW ACHIEVEMENT UNLOCKED!
     🥇 First Watch
     Watched your first video
     NFT Serial: #1

  ⏳ Waiting for blockchain... 5 4 3 2 1 Done!
  🔗 Querying blockchain...
  💳 Blockchain balance: 17 VIEW
     Token ID: 0.0.7379174

════════════════════════════════════════════════════════════
```

**What Happens:**
1. **Summary shows all earnings** (ad + content + rating)
2. **Achievements checked** automatically
3. **New badges announced** if earned
4. **Blockchain confirmed** (5 second wait)
5. **Balance updated** from Hedera

---

## Earning Tokens

### Earning Methods

| Action | Base Reward | VIP Multiplier | VIP Reward |
|--------|-------------|----------------|------------|
| **Watch Ad (complete)** | 5 VIEW | 2x | 10 VIEW |
| **Watch Ad (skip)** | 0 VIEW | - | 0 VIEW |
| **Watch Content (complete)** | 10 VIEW | 2x | 20 VIEW |
| **Watch Content (partial 30s+)** | 1-5 VIEW | 2x | 2-10 VIEW |
| **Rate Content** | 2 VIEW | 2x | 4 VIEW |
| **Binge Bonus (3 videos)** | 5 VIEW | 2x | 10 VIEW |
| **Binge Bonus (5 videos)** | 15 VIEW | 2x | 30 VIEW |

### Binge Watching Bonuses

**Automatic Bonuses:**
- Watch **3 videos** in one session: **+5 VIEW** (VIP: 10 VIEW)
- Watch **5 videos** in one session: **+15 VIEW** (VIP: 30 VIEW)

**Example Session:**
```
Video 1: 15 VIEW (5 ad + 10 content)
Video 2: 15 VIEW (5 ad + 10 content)
Video 3: 15 VIEW + 5 BONUS = 20 VIEW ✨
Video 4: 15 VIEW (5 ad + 10 content)
Video 5: 15 VIEW + 15 BONUS = 30 VIEW ✨✨

Total: 95 VIEW in one session!
```

### VIP Multiplier

**How It Works:**
- Activate VIP Status (costs 200 VIEW)
- **All rewards doubled** for 24 hours
- Applies to: ads, content, ratings, bonuses
- Stacks with existing rewards

**VIP Example:**
```
Without VIP:
  Ad: 5 VIEW
  Content: 10 VIEW
  Rating: 2 VIEW
  Total: 17 VIEW

With VIP (2x):
  Ad: 10 VIEW ✨
  Content: 20 VIEW ✨
  Rating: 4 VIEW ✨
  Total: 34 VIEW ✨
```

---

## Rating Content

### Why Rate?

1. **Earn Tokens:** +2 VIEW per rating (VIP: 4 VIEW)
2. **Unlock Badge:** "Rating Master" badge at 5 ratings
3. **Improve Recommendations:** Help platform learn your preferences
4. **Support Creators:** Show appreciation for quality content

### How to Rate

After watching content, you'll see:
```
⭐ RATE THIS CONTENT
────────────────────────────────────────────────────────────
  Your rating (0-5):
```

**Input your rating:**
- `5` = Excellent (highly recommend)
- `4` = Very Good (enjoyed it)
- `3` = Good (worth watching)
- `2` = Fair (mediocre)
- `1` = Poor (didn't like it)
- `0` = Skip rating

**Tips:**
- Rate honestly - it helps content creators
- Don't skip ratings - free tokens!
- All ratings count toward "Rating Master" badge

---

## Achievement Badges

### View Your Badges

**Select Option 3 from Main Menu:**
```
============================================================
🏆 ACHIEVEMENT BADGES
============================================================

  🔄 Loading badges...

  📊 Progress: 3/4 badges earned

  🎖️  Owned Badges:

  🥇 First Watch
     Watched your first video
     NFT Serial: #1
     View: https://hashscan.io/testnet/token/0.0.7724797?s=1

  ⭐ Rating Master
     Submitted 5 ratings
     NFT Serial: #5
     View: https://hashscan.io/testnet/token/0.0.7724797?s=5

  👑 VIP Member
     Activated VIP status
     NFT Serial: #8
     View: https://hashscan.io/testnet/token/0.0.7724797?s=8


  🔓 Available Badges:

  🔒 Binge Watcher (10 required)
     Watched 10 videos in total

============================================================

  Press Enter to continue...
```

### Badge Types

#### 🥇 First Watch
**Requirement:** Watch your first video
**How to Earn:** Complete any video
**Rarity:** Common (everyone gets this first)

#### ⭐ Rating Master
**Requirement:** Submit 5 ratings
**How to Earn:** Rate 5 different videos (any star rating)
**Progress:** Check current count in badge menu
**Rarity:** Uncommon

#### 📺 Binge Watcher
**Requirement:** Watch 10 videos (total, across all sessions)
**How to Earn:** Keep watching! Progress tracked automatically
**Rarity:** Rare

#### 👑 VIP Member
**Requirement:** Activate VIP status
**How to Earn:** Redeem VIP Status for 200 VIEW
**Rarity:** Epic

### NFT Details

**What Are These Badges?**
- Real NFTs on Hedera blockchain
- Permanently owned by you
- Verifiable on HashScan
- Each badge has unique serial number

**Can I Trade Them?**
- Currently: No (non-transferable)
- Future: May enable trading/marketplace

**Where Can I See Them?**
- In the Achievement Badges menu (Option 3)
- On HashScan (click the provided links)
- In your Hedera wallet (if you have one)

---

## Redemption Center

### Access Redemption Center

**Select Option 2 from Main Menu:**
```
============================================================
💳 REDEMPTION CENTER
============================================================

  🔄 Checking balance...
  💰 Your Balance: 250 VIEW tokens

  📋 Fetching redemptions...

  Available Rewards:

  1. ✅ Skip Ads (1 session)
     Cost: 50 VIEW
     Skip all ads in your next viewing session

  2. ✅ Ad-Free Hour
     Cost: 75 VIEW
     No ads for 1 hour

  3. ✅ Premium Content Access
     Cost: 100 VIEW
     Unlock premium content library

  4. ✅ VIP Status (1 day)
     Cost: 200 VIEW
     All benefits + 2x rewards for 24 hours

  0. Cancel

────────────────────────────────────────────────────────────

  Select option (0-4):
```

### Available Benefits

#### 1. Skip Ads (50 VIEW)

**What It Does:**
- Skip all ads in your **next viewing session**
- Single-use benefit
- Consumed after one session

**Best For:**
- Quick viewing when you're in a hurry
- Don't need long-term ad removal

**Example:**
```
Redeem: Skip Ads
Start watching: All ads skipped automatically
Exit player: Benefit consumed
Next session: Ads return (need to redeem again)
```

---

#### 2. Ad-Free Hour (75 VIEW)

**What It Does:**
- No ads for **1 hour** (3600 seconds)
- Watch multiple videos ad-free
- Timer starts when redeemed

**Best For:**
- Binge watching session
- Multiple short videos
- Want uninterrupted experience

**Remaining Time Display:**
```
✨ Active: Ad-Free Hour
⏱️  Remaining: 42m 15s
```

---

#### 3. Premium Content Access (100 VIEW)

**What It Does:**
- Unlock premium content library
- Access exclusive shows/documentaries
- One-time unlock (no expiration)

**Best For:**
- Accessing specific premium content
- Permanent unlock
- Quality over quantity

**What Changes:**
```
Before:
  4. 🔒 Premium_Show.mp4 (Requires Premium Access)

After:
  4. ✅ Premium_Show.mp4 (Unlocked)
```

---

#### 4. VIP Status (200 VIEW) ⭐ **Best Value**

**What It Does:**
- **All benefits** included:
  - Skip all ads
  - Premium content access
  - 2x reward multiplier
- Valid for **24 hours**

**Benefits Breakdown:**
```
✨ VIP Status Active:
   • All ads automatically skipped
   • Premium library unlocked
   • 2x rewards on everything:
     - Ad viewing: 5 → 10 VIEW
     - Content: 10 → 20 VIEW
     - Rating: 2 → 4 VIEW
     - Binge bonuses: 2x
```

**Best For:**
- Serious viewers
- Maximizing token earnings
- Get more than you spend

**VIP Math:**
```
Cost: 200 VIEW

Earnings with VIP (10 videos):
  10 ads: 10 × 10 = 100 VIEW
  10 content: 10 × 20 = 200 VIEW
  10 ratings: 10 × 4 = 40 VIEW
  2 binge bonuses: (10 + 30) = 40 VIEW
  ──────────────────────────
  Total earned: 380 VIEW

Net profit: 380 - 200 = 180 VIEW ✅
Plus VIP Member badge! 👑
```

---

### Redemption Process

**Example: Redeeming VIP Status**

1. **Check Balance:**
```
   💰 Your Balance: 250 VIEW tokens
```

2. **Select Option 4:**
```
   Select option (0-4): 4
```

3. **Confirm:**
```
   Redeem: VIP Status (1 day)
   Cost: 200 VIEW
   Confirm? (y/n): y
```

4. **Processing:**
```
   🔄 Processing redemption...
   ✅ Redemption successful!
      Benefit: VIP Status (1 day)
      Cost: 200 VIEW
      Mode: Simulation (tokens tracked locally)

   🎉 Benefit activated!

   Press Enter to continue...
```

5. **Benefit Active:**
   - VIP status immediately active
   - Check "Check Balance" menu to see details
   - 2x multiplier applies to all future rewards

---

## Checking Your Balance

### View Balance Details

**Select Option 4 from Main Menu:**
```
  🔄 Checking balance...
  💳 Balance: 250 VIEW
  📺 Videos watched this session: 5

  ✨ Active Benefit: VIP Status (1 day)
  ⏱️  Time Remaining: 23h 45m

  🌟 VIP Perks Active:
     • All ads skipped
     • Premium content access
     • 2x rewards on everything

  🏆 Badges: 3/4 earned
```

### Balance Information

**What You'll See:**
1. **Current Token Balance** - Your VIEW tokens
2. **Session Stats** - Videos watched this session
3. **Active Benefits** - Current active benefits (if any)
4. **Remaining Time** - For time-limited benefits
5. **Badge Progress** - Achievement summary

---

## Understanding Benefits

### Benefit Status Indicators

#### No Active Benefits
```
🎁 Checking active benefits...
   No active benefits

💡 Visit Redemption Center to unlock perks!
```

#### Ad-Skip Benefit Active
```
✨ Active: Skip Ads (1 session)
- Ads will be skipped
```

#### Ad-Free Hour Active
```
✨ Active: Ad-Free Hour
⏱️  Time Remaining: 42m 15s

- Ad skipping enabled
```

#### Premium Content Active
```
✨ Active: Premium Content Access

- Premium library unlocked
```

#### VIP Status Active
```
✨ Active: VIP Status (1 day)
⏱️  Time Remaining: 23h 45m

🌟 VIP Perks Active:
   • All ads skipped
   • Premium content access
   • 2x rewards on everything
```

### Benefit Expiration

**What Happens When Benefits Expire:**

1. **Time-Based Benefits:**
   - Ad-Free Hour: Expires after 1 hour
   - VIP Status: Expires after 24 hours

2. **Usage-Based Benefits:**
   - Skip Ads: Consumed after one session

3. **Permanent Benefits:**
   - Premium Content: Never expires (until used)

**Expired Benefit:**
```
🎁 Checking active benefits...
   No active benefits
   (VIP Status expired)
```

---

## Tips & Strategies

### Earning Efficiently

#### Strategy 1: VIP Grinding
**Goal:** Maximize earnings with VIP multiplier

1. Save 200 VIEW (don't redeem anything else)
2. Redeem VIP Status
3. Watch 10+ videos in 24 hours
4. Earn 380+ VIEW with multiplier
5. Net profit: 180+ VIEW

**Best For:** Maximizing tokens

---

#### Strategy 2: Binge Bonus Focus
**Goal:** Hit binge bonuses quickly

1. Watch 5 videos in one session
2. Earn 2 binge bonuses:
   - 3 videos: +5 VIEW
   - 5 videos: +15 VIEW
3. Total bonus: +20 VIEW
4. With VIP: +40 VIEW

**Best For:** Quick earnings

---

#### Strategy 3: Rating Rewards
**Goal:** Easy tokens + badge

1. Always rate content (never skip)
2. Earn +2 VIEW per rating
3. 5 ratings = 10 VIEW + Rating Master badge
4. With VIP: 20 VIEW

**Best For:** Consistent small earnings

---

### Spending Wisely

#### Smart Redemption Order

**Early Game (0-200 VIEW):**
1. Save for VIP Status (200 VIEW)
2. Don't redeem anything else
3. Maximize earnings with VIP

**Mid Game (200-500 VIEW):**
1. Redeem VIP Status
2. Grind with 2x multiplier
3. Build token reserves

**Late Game (500+ VIEW):**
1. Redeem VIP when needed
2. Use ad-free for convenience
3. Premium content for variety

---

### Badge Hunting

**Fastest Badge Route:**

1. **First Watch** (1 video)
   - Watch any video: ✅

2. **Rating Master** (5 ratings)
   - Rate 5 videos: ✅

3. **VIP Member** (200 VIEW)
   - Save and redeem VIP: ✅

4. **Binge Watcher** (10 videos)
   - Watch 10 videos total: ✅

**Time to Collect All:**
- Without VIP: ~10 videos, ~3 hours
- With VIP: ~6-7 videos, ~2 hours (earn faster)

---

## Troubleshooting

### Common Issues

#### Issue: "Balance shows 0 but I earned tokens"

**Solution:**
1. Wait 5-10 seconds (blockchain sync)
2. Check balance again (Option 4)
3. Verify on HashScan:
   - Visit: https://hashscan.io/testnet/account/YOUR_ACCOUNT_ID
   - Check transactions

**Why:** Mirror node takes a few seconds to update

---

#### Issue: "Can't redeem (insufficient balance)"

**Solution:**
1. Check actual balance (Option 4)
2. Compare with redemption cost
3. Earn more tokens if needed

**Common Causes:**
- Balance not yet synced
- Already spent tokens
- Incorrect balance displayed

---

#### Issue: "VIP multiplier not working"

**Solution:**
1. Check active benefits (Option 4)
2. Verify VIP is active
3. Check remaining time
4. Re-redeem if expired

**How to Verify:**
```
Watch ad without VIP: 5 VIEW
Watch ad with VIP: 10 VIEW ✨
```

---

#### Issue: "Badge not showing up"

**Solution:**
1. Check badge menu (Option 3)
2. Verify requirements met
3. Wait for blockchain confirmation
4. Check HashScan NFT collection

**Troubleshooting:**
- Backend logs show if NFT minted
- HashScan shows all minted NFTs
- May take 10-15 seconds for display

---

#### Issue: "Premium content still locked"

**Solution:**
1. Redeem Premium Content Access (100 VIEW)
2. Or redeem VIP Status (200 VIEW)
3. Check active benefits (Option 4)
4. Restart player if needed

**Why:** Need to redeem benefit first

---

#### Issue: "Session bonus not awarded"

**Solution:**
1. Check videos watched count
2. Must watch in same session
3. 3 videos = first bonus
4. 5 videos = second bonus

**Example:**
```
Videos watched this session: 2
💡 Watch 1 more video(s) for bonus
```

---

## FAQs

### General Questions

**Q: What are VIEW tokens?**
A: VIEW is a fungible token on Hedera blockchain (Token ID: 0.0.7379174). You earn them by watching content and can redeem them for benefits.

**Q: Are these real blockchain tokens?**
A: Yes! All VIEW tokens exist on Hedera Testnet. You can verify transactions on HashScan.

**Q: Can I withdraw tokens to my wallet?**
A: Currently no. Tokens are tied to the platform. Future: may enable withdrawals.

**Q: Do tokens expire?**
A: No, VIEW tokens never expire. Redeem whenever you want.

---

### Earning Questions

**Q: How much can I earn per session?**
A: Without VIP: ~15-20 VIEW per video. With VIP: ~30-40 VIEW per video.

**Q: What's the fastest way to earn tokens?**
A: Redeem VIP Status (200 VIEW), then watch 10+ videos with 2x multiplier.

**Q: Do partial views count?**
A: Yes, if you watch 30+ seconds, you earn 1-5 VIEW based on watch time.

**Q: Can I earn unlimited tokens?**
A: Yes! No daily limit. Watch as much as you want.

---

### Badge Questions

**Q: What are achievement badges?**
A: NFTs on Hedera blockchain (Token ID: 0.0.7724797). Unique, collectible, verifiable.

**Q: How many badges are there?**
A: Currently 4 badges: First Watch, Rating Master, Binge Watcher, VIP Member.

**Q: Can I lose badges?**
A: No, once earned, badges are permanent.

**Q: Can I trade badges?**
A: Not currently. Future: may enable marketplace trading.

---

### Redemption Questions

**Q: What happens to redeemed tokens?**
A: Tokens are "burned" (removed from circulation). In simulation mode, tracked locally.

**Q: Can I cancel a redemption?**
A: No, redemptions are final. Choose carefully!

**Q: Do benefits stack?**
A: No. Only one benefit active at a time (VIP includes all benefits).

**Q: Can I gift tokens to friends?**
A: Not currently. Future: may enable peer-to-peer transfers.

---

### Technical Questions

**Q: What blockchain is this on?**
A: Hedera Hashgraph Testnet (not Ethereum).

**Q: Why is balance sometimes delayed?**
A: Blockchain takes 5-10 seconds to sync. Mirror Node caches data.

**Q: What if backend is offline?**
A: Player tracks earnings locally. Backend syncs when back online.

**Q: Can I use this on multiple devices?**
A: No, one device per account (security feature).

---

## Next Steps

### Learn More

- **Technical Details:** See [ARCHITECTURE.md](ARCHITECTURE.md)
- **API Reference:** See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Setup Guide:** See [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Future Features:** See [FUTURE_WORK.md](FUTURE_WORK.md)

### Blockchain Verification

- **Your Account:** https://hashscan.io/testnet/account/YOUR_ACCOUNT_ID
- **VIEW Token:** https://hashscan.io/testnet/token/0.0.7379174
- **NFT Badges:** https://hashscan.io/testnet/token/0.0.7724797
- **Event Log:** https://hashscan.io/testnet/topic/0.0.7724961

### Community

- **GitHub:** https://github.com/yourusername/view-rewards-tv
- **Issues:** Report bugs or request features
- **Feedback:** Share your experience

---

**Happy Watching! Earn rewards while enjoying great content.** 🎬🪙

**Remember:** Watch → Earn → Redeem → Repeat! 🔄