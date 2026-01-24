#!/usr/bin/env python3
"""
Video Player with Blockchain Rewards, Redemption, Rating, Binge Bonus, Device Fingerprinting, and NFT Badges
Phase 2: Complete with NFT Achievement System
"""

import subprocess
import threading
import time
import os
import sys
import requests
import json

# Configuration
AD_SKIP_DELAY = 5
AD_FULL_REWARD = 5
AD_SKIP_REWARD = 0
CONTENT_COMPLETE_REWARD = 10
CONTENT_PARTIAL_MIN_TIME = 30

# Blockchain configuration
ACCOUNT_ID = "0.0.5864245"
TOKEN_ID = "0.0.7379174"
BACKEND_URL = "http://192.168.0.148:5000"  # Your laptop IP
MIRROR_NODE = "https://testnet.mirrornode.hedera.com/api/v1"

# Westeros environment
WESTEROS_ENV = {
    'LD_PRELOAD': '/usr/lib/libwesteros_gl.so.0',
    'WESTEROS_SINK_USE_ESSRMGR': '1',
    'WESTEROS_SINK_USE_FREERUN': '1',
    'WESTEROS_GL_USE_GENERIC_AVSYNC': '1',
    'WESTEROS_GL_USE_REFRESH_LOCK': '1',
    'WESTEROS_DRM_CARD': '/dev/dri/card1',
    'WESTEROS_GL_GRAPHICS_MAX_SIZE': '1920x1080',
    'WESTEROS_GL_USE_BEST_MODE': '1',
    'PLAYERSINKBIN_USE_WESTEROSSINK': '1',
    'AAMP_ENABLE_WESTEROS_SINK': '1',
    'XDG_RUNTIME_DIR': '/tmp',
    'WAYLAND_DISPLAY': 'westeros-0',
}


def get_device_id():
    """Get unique device identifier from RDK hardware"""
    try:
        # Method 1: CPU Serial (Raspberry Pi specific)
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.startswith('Serial'):
                    serial = line.split(':')[1].strip()
                    if serial and serial != '0000000000000000':
                        return f"rdk_cpu_{serial}"
        
        # Method 2: Machine ID (systemd)
        with open('/etc/machine-id', 'r') as f:
            machine_id = f.read().strip()
            if machine_id:
                return f"rdk_machine_{machine_id}"
        
        # Method 3: MAC Address (fallback)
        import uuid
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                        for elements in range(0,2*6,2)][::-1])
        return f"rdk_mac_{mac}"
        
    except Exception as e:
        print(f"  ⚠️  Could not get device ID: {e}")
        return f"rdk_unknown_{int(time.time())}"


def get_video_duration(video_path):
    """Get video duration"""
    try:
        result = subprocess.run(
            ['gst-discoverer-1.0', video_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        for line in result.stdout.split('\n'):
            if 'Duration:' in line:
                time_part = line.split('Duration:')[1].strip()
                parts = time_part.split(':')
                if len(parts) >= 3:
                    hours = int(parts[0])
                    minutes = int(parts[1])
                    seconds = float(parts[2])
                    return hours * 3600 + minutes * 60 + seconds
    except Exception:
        pass
    return None


class BlockchainWallet:
    """Wallet with redemption, rating, session, device fingerprinting, and NFT badges"""
    
    def __init__(self):
        self.account_id = ACCOUNT_ID
        self.token_id = TOKEN_ID
        self.backend_url = BACKEND_URL
        self.local_balance = 0
        self.active_benefits = None
        self.session_id = None
        self.videos_watched_count = 0
        self.device_id = get_device_id()
        self.device_verified = False
    
    def get_balance(self):
        """Get balance from blockchain"""
        try:
            response = requests.get(
                f"{MIRROR_NODE}/accounts/{self.account_id}",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'balance' in data and 'tokens' in data['balance']:
                    for token in data['balance']['tokens']:
                        if token['token_id'] == self.token_id:
                            return int(token['balance'])
                return 0
            else:
                return self.local_balance
        except Exception as e:
            print(f"  ⚠️  Blockchain query failed: {e}")
            return self.local_balance
    
    def register_device(self):
        """Register device with backend"""
        try:
            print(f"   Device ID: {self.device_id[:40]}...")
            
            response = requests.post(
                f"{self.backend_url}/device/register",
                json={
                    'account_id': self.account_id,
                    'device_id': self.device_id
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.device_verified = True
                    status = data.get('status', 'unknown')
                    if status == 'new':
                        print(f"   ✅ Device registered (new)")
                    else:
                        print(f"   ✅ Device verified (existing)")
                    return True
                else:
                    print(f"   ❌ Registration failed: {data.get('error')}")
                    return False
            elif response.status_code == 403:
                data = response.json()
                print(f"   ❌ BLOCKED: {data.get('error')}")
                if data.get('fraud_detected'):
                    print(f"   🚨 Fraud detection triggered!")
                return False
            else:
                print(f"   ⚠️  Backend error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ⚠️  Registration failed: {e}")
            return False
    
    def send_reward(self, amount, reason):
        """Send reward to backend with VIP multiplier"""
        # Apply VIP multiplier
        multiplier = self.get_reward_multiplier()
        actual_amount = int(amount * multiplier)
        
        if multiplier > 1.0:
            print(f"  ✨ VIP Bonus! {amount} → {actual_amount} VIEW (2x multiplier)")
        
        try:
            response = requests.post(
                f"{self.backend_url}/reward",
                json={
                    'account_id': self.account_id,
                    'amount': actual_amount,
                    'reason': reason
                },
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"  ✅ Reward sent: +{actual_amount} VIEW")
                self.local_balance += actual_amount
                return True
            else:
                print(f"  ⚠️  Backend: {response.status_code}")
                self.local_balance += actual_amount
                return False
        except Exception as e:
            print(f"  ⚠️  Backend unreachable: {e}")
            print(f"  📝 Tracking locally: +{actual_amount} VIEW")
            self.local_balance += actual_amount
            return False
    
    def get_redemptions(self):
        """Get available redemptions"""
        try:
            response = requests.get(
                f"{self.backend_url}/redemptions",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('redemptions', [])
            return []
        except Exception:
            return []
    
    def check_benefits(self):
        """Check active benefits"""
        try:
            response = requests.get(
                f"{self.backend_url}/benefits",
                params={'account_id': self.account_id},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('has_benefits'):
                    self.active_benefits = data.get('benefit')
                    return self.active_benefits
            self.active_benefits = None
            return None
        except Exception:
            return None
    
    def redeem(self, benefit_type):
        """Redeem tokens for benefit"""
        try:
            print(f"  🔄 Processing redemption...")
            response = requests.post(
                f"{self.backend_url}/redeem",
                json={
                    'account_id': self.account_id,
                    'benefit_type': benefit_type
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ Redemption successful!")
                print(f"     Benefit: {data.get('benefit')}")
                print(f"     Cost: {data.get('cost')} VIEW")
                if data.get('mode') == 'simulation':
                    print(f"     Mode: Simulation (tokens tracked locally)")
                return True, data
            else:
                data = response.json()
                print(f"  ❌ Redemption failed: {data.get('error')}")
                return False, data
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return False, None
    
    def has_premium_access(self):
        """Check if user has premium access"""
        if not self.active_benefits:
            return False
        
        benefit_type = self.active_benefits.get('type')
        return benefit_type in ['premium_content', 'vip_day']
    
    def has_ad_skip(self):
        """Check if user can skip ads"""
        if not self.active_benefits:
            return False
        
        benefit_type = self.active_benefits.get('type')
        return benefit_type in ['skip_ads', 'ad_free_hour', 'vip_day']
    
    def get_reward_multiplier(self):
        """Get reward multiplier for VIP"""
        if not self.active_benefits:
            return 1.0
        
        benefit_type = self.active_benefits.get('type')
        return 2.0 if benefit_type == 'vip_day' else 1.0
    
    def start_session(self):
        """Start a new viewing session"""
        try:
            response = requests.post(
                f"{self.backend_url}/session/start",
                json={'account_id': self.account_id},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                self.session_id = data.get('session_id')
                self.videos_watched_count = 0
                print(f"  📺 Session started: {self.session_id[:20]}...")
                return True
            return False
        except Exception as e:
            print(f"  ⚠️  Session start failed: {e}")
            return False
    
    def track_video(self, content_id):
        """Track video watched in session"""
        if not self.session_id:
            return False
        
        try:
            response = requests.post(
                f"{self.backend_url}/session/video",
                json={
                    'session_id': self.session_id,
                    'content_id': content_id
                },
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                self.videos_watched_count = data.get('videos_watched', 0)
                return True
            return False
        except Exception:
            return False
    
    def check_binge_bonus(self):
        """Check and claim binge watching bonus"""
        if not self.session_id:
            return 0, None
        
        try:
            response = requests.get(
                f"{self.backend_url}/session/bonus",
                params={
                    'session_id': self.session_id,
                    'account_id': self.account_id
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                bonus = data.get('bonus', 0)
                message = data.get('message', '')
                
                if bonus > 0:
                    print(f"  🎉 Binge Bonus: +{bonus} VIEW!")
                    print(f"     {message}")
                
                return bonus, message
            return 0, None
        except Exception as e:
            print(f"  ⚠️  Bonus check failed: {e}")
            return 0, None
    
    def submit_rating(self, content_id, rating):
        """Submit content rating"""
        try:
            print(f"  🔄 Submitting rating...")
            response = requests.post(
                f"{self.backend_url}/rate",
                json={
                    'account_id': self.account_id,
                    'content_id': content_id,
                    'rating': rating,
                    'session_id': self.session_id
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                reward = data.get('reward', 0)
                print(f"  ✅ Rating submitted: {rating} stars")
                print(f"  🎁 Reward: +{reward} VIEW")
                return True, reward
            else:
                print(f"  ❌ Rating failed")
                return False, 0
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return False, 0
    
    def get_badges(self):
        """Get user's achievement badges (NFTs)"""
        try:
            response = requests.get(
                f"{self.backend_url}/badges",
                params={'account_id': self.account_id},
                timeout=5
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception:
            return None
    
    def check_achievements(self):
        """Check for new achievements"""
        try:
            response = requests.post(
                f"{self.backend_url}/achievements/check",
                json={'account_id': self.account_id},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                new_badges = data.get('new_badges', [])
                
                # Display new badges
                for badge in new_badges:
                    if badge.get('newly_awarded'):
                        print(f"\n  🎉 NEW ACHIEVEMENT UNLOCKED!")
                        print(f"     {badge.get('icon')} {badge.get('badge')}")
                        print(f"     {badge.get('description')}")
                        if badge.get('nft_serial'):
                            print(f"     NFT Serial: #{badge.get('nft_serial')}")
                        time.sleep(2)
                
                return new_badges
            return []
        except Exception:
            return []


class WesterosManager:
    """Manages Westeros compositor"""
    
    def __init__(self):
        self.westeros_process = None
        self.is_running = False
    
    def start_westeros(self):
        """Start Westeros"""
        if self.is_running:
            return True
        
        print("  🖥️  Starting Westeros...")
        env = os.environ.copy()
        env.update(WESTEROS_ENV)
        
        cmd = [
            'westeros',
            '--renderer', '/usr/lib/libwesteros_render_embedded.so.0.0.0',
            '--embedded',
            '--display', 'westeros-0',
            '--window-size', '1920x1080'
        ]
        
        try:
            self.westeros_process = subprocess.Popen(
                cmd, env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(2)
            
            if self.westeros_process.poll() is None:
                self.is_running = True
                print("  ✅ Westeros started")
                return True
            return False
        except Exception as e:
            print(f"  ❌ Westeros error: {e}")
            return False
    
    def stop_westeros(self):
        """Stop Westeros"""
        if self.westeros_process:
            print("  🖥️  Stopping Westeros...")
            self.westeros_process.terminate()
            try:
                self.westeros_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.westeros_process.kill()
            self.is_running = False


class VideoPlayer:
    """Video player"""
    
    def __init__(self, use_display=False):
        self.process = None
        self.is_playing = False
        self.start_time = 0
        self.play_thread = None
        self.playback_successful = False
        self.playback_duration = 0
        self.was_stopped = False
        self.use_display = use_display
    
    def play(self, video_path):
        """Play video"""
        if not os.path.exists(video_path):
            return False
        
        self.is_playing = True
        self.start_time = time.time()
        self.playback_successful = False
        self.playback_duration = 0
        self.was_stopped = False
        
        if self.use_display:
            cmd = f'gst-launch-1.0 playbin uri=file://{video_path}'
        else:
            cmd = f'gst-launch-1.0 filesrc location="{video_path}" ! decodebin ! fakesink sync=true'
        
        env = os.environ.copy()
        if self.use_display:
            env.update(WESTEROS_ENV)
        
        self.play_thread = threading.Thread(target=self._play_worker, args=(cmd, env))
        self.play_thread.daemon = True
        self.play_thread.start()
        return True
    
    def _play_worker(self, cmd, env):
        """Playback worker"""
        try:
            self.process = subprocess.Popen(
                cmd, shell=True, env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = self.process.communicate()
            self.playback_duration = time.time() - self.start_time
            
            if not self.was_stopped:
                if "Got EOS" in (stdout + stderr) or self.process.returncode == 0:
                    self.playback_successful = True
        except Exception as e:
            self.playback_duration = time.time() - self.start_time
        finally:
            self.is_playing = False
    
    def stop(self):
        """Stop playback"""
        self.was_stopped = True
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.kill()
        self.is_playing = False
        self.playback_duration = time.time() - self.start_time
    
    def get_elapsed_time(self):
        """Get elapsed time"""
        if self.start_time > 0:
            return time.time() - self.start_time
        return 0
    
    def wait_for_completion(self, timeout=None):
        """Wait for completion"""
        if self.play_thread and self.play_thread.is_alive():
            self.play_thread.join(timeout=timeout)
    
    def is_still_playing(self):
        """Check if playing"""
        return self.is_playing and self.play_thread and self.play_thread.is_alive()


class AdManager:
    """Ad manager with skip and benefit support"""
    
    def __init__(self, ad_video_path, use_display=False, skip_ads=False):
        self.ad_path = ad_video_path
        self.player = VideoPlayer(use_display=use_display)
        self.ad_duration = get_video_duration(ad_video_path)
        self.use_display = use_display
        self.skip_ads = skip_ads
    
    def play_ad(self):
        """Play ad with skip or benefit"""
        result = {
            'completed': False,
            'skipped': False,
            'watch_time': 0,
            'reward': 0
        }
        
        # Check if ads should be skipped due to benefit
        if self.skip_ads:
            print("\n" + "─" * 60)
            print("📺 ADVERTISEMENT")
            print("─" * 60)
            print("  ✨ Ad skipped (active benefit)")
            print("  🎁 No reward (benefit used)")
            print("─" * 60)
            result['skipped'] = True
            result['watch_time'] = 0
            result['reward'] = 0
            time.sleep(2)
            return result
        
        if not os.path.exists(self.ad_path):
            return result
        
        duration_str = f"{self.ad_duration:.1f}s" if self.ad_duration else "unknown"
        ad_too_short = self.ad_duration and self.ad_duration <= AD_SKIP_DELAY
        
        print("\n" + "─" * 60)
        print("📺 ADVERTISEMENT")
        print("─" * 60)
        print(f"  📁 File: {os.path.basename(self.ad_path)}")
        print(f"  ⏱️  Duration: {duration_str}")
        if self.use_display:
            print(f"  🖥️  Playing on screen")
        print(f"  🎁 Watch complete ad: +{AD_FULL_REWARD} VIEW tokens!")
        
        if not ad_too_short:
            print(f"  ⏭️  Skip after {AD_SKIP_DELAY}s")
        print("")
        
        if not self.player.play(self.ad_path):
            return result
        
        print("  ▶️  Ad playing...")
        if not ad_too_short:
            print("  Press 's' + Enter to skip\n")
        else:
            print("")
        
        skip_enabled = False
        start_time = time.time()
        progress_total = self.ad_duration if self.ad_duration else 30
        
        try:
            while self.player.is_still_playing():
                elapsed = time.time() - start_time
                
                if not ad_too_short and not skip_enabled and elapsed >= AD_SKIP_DELAY:
                    skip_enabled = True
                    print(f"\n  ⏭️  Skip available! Press 's' + Enter\n")
                
                progress_bar = self._make_progress_bar(elapsed, progress_total)
                status = "[Skip: 's']" if skip_enabled else f"[{AD_SKIP_DELAY - elapsed:.0f}s]" if not ad_too_short else ""
                print(f"\r  {progress_bar} {elapsed:.1f}s/{progress_total:.1f}s {status}  ", end='', flush=True)
                
                if skip_enabled and self._check_skip():
                    print(f"\n\n  ⏭️  Ad skipped!")
                    self.player.stop()
                    result['skipped'] = True
                    result['watch_time'] = elapsed
                    result['reward'] = AD_SKIP_REWARD
                    break
                
                time.sleep(0.1)
            
            if not result['skipped']:
                self.player.wait_for_completion(timeout=5)
                result['watch_time'] = self.player.playback_duration
                
                if self.player.playback_successful:
                    result['completed'] = True
                    result['reward'] = AD_FULL_REWARD
                    print(f"\n\n  ✅ Ad complete! +{AD_FULL_REWARD} VIEW tokens!")
                    
        except KeyboardInterrupt:
            print(f"\n\n  ⏹️  Interrupted")
            self.player.stop()
            result['watch_time'] = self.player.get_elapsed_time()
        
        print("─" * 60)
        return result
    
    def _make_progress_bar(self, current, total, width=20):
        """Progress bar"""
        if total <= 0:
            total = 1
        filled = int(width * min(current, total) / total)
        return f"[{'█' * filled}{'░' * (width - filled)}]"
    
    def _check_skip(self):
        """Check skip input"""
        try:
            import select
            if select.select([sys.stdin], [], [], 0.0)[0]:
                return sys.stdin.readline().strip().lower() == 's'
        except:
            pass
        return False


class ContentPlayer:
    """Content player"""
    
    def __init__(self, video_path, use_display=False):
        self.video_path = video_path
        self.player = VideoPlayer(use_display=use_display)
        self.content_duration = get_video_duration(video_path)
        self.use_display = use_display
    
    def play_content(self):
        """Play content"""
        result = {
            'completed': False,
            'watch_time': 0,
            'reward': 0
        }
        
        if not os.path.exists(self.video_path):
            return result
        
        duration_str = f"{self.content_duration:.1f}s" if self.content_duration else "unknown"
        
        print("\n" + "─" * 60)
        print("🎬 MAIN CONTENT")
        print("─" * 60)
        print(f"  📁 File: {os.path.basename(self.video_path)}")
        print(f"  ⏱️  Duration: {duration_str}")
        if self.use_display:
            print(f"  🖥️  Playing on screen")
        print(f"  🎁 Complete: +{CONTENT_COMPLETE_REWARD} VIEW tokens!")
        print("")
        
        if not self.player.play(self.video_path):
            return result
        
        print("  ▶️  Content playing...")
        print("  Ctrl+C to stop\n")
        
        start_time = time.time()
        progress_total = self.content_duration if self.content_duration else 60
        
        try:
            while self.player.is_still_playing():
                elapsed = time.time() - start_time
                progress_bar = self._make_progress_bar(elapsed, progress_total)
                print(f"\r  {progress_bar} ⏱️  {elapsed:.1f}s/{progress_total:.1f}s  ", end='', flush=True)
                time.sleep(0.3)
            
            self.player.wait_for_completion(timeout=5)
            result['watch_time'] = self.player.playback_duration
            
            if self.player.playback_successful:
                result['completed'] = True
                result['reward'] = CONTENT_COMPLETE_REWARD
                print(f"\n\n  ✅ Complete! +{CONTENT_COMPLETE_REWARD} VIEW tokens!")
            else:
                if result['watch_time'] >= CONTENT_PARTIAL_MIN_TIME:
                    partial = min(5, int(result['watch_time'] / 60) + 1)
                    result['reward'] = partial
                    print(f"\n\n  📊 Partial: +{partial} VIEW")
                    
        except KeyboardInterrupt:
            print(f"\n\n  ⏹️  Stopped")
            self.player.stop()
            result['watch_time'] = self.player.get_elapsed_time()
            
            if result['watch_time'] >= CONTENT_PARTIAL_MIN_TIME:
                partial = min(5, int(result['watch_time'] / 60) + 1)
                result['reward'] = partial
                print(f"  📊 Partial: +{partial} VIEW")
        
        print("─" * 60)
        return result
    
    def _make_progress_bar(self, current, total, width=20):
        """Progress bar"""
        if total <= 0:
            total = 1
        filled = int(width * min(current, total) / total)
        return f"[{'█' * filled}{'░' * (width - filled)}]"


def prompt_rating(wallet, content_id):
    """Prompt user to rate content"""
    print("\n" + "─" * 60)
    print("⭐ RATE THIS CONTENT")
    print("─" * 60)
    print("  How would you rate this content?")
    print("  1 ⭐ - Poor")
    print("  2 ⭐⭐ - Fair")
    print("  3 ⭐⭐⭐ - Good")
    print("  4 ⭐⭐⭐⭐ - Very Good")
    print("  5 ⭐⭐⭐⭐⭐ - Excellent")
    print("  0 - Skip rating")
    print("─" * 60)
    
    try:
        choice = input("\n  Your rating (0-5): ").strip()
        rating = int(choice)
        
        if rating == 0:
            print("  Skipped rating")
            return 0
        
        if 1 <= rating <= 5:
            success, reward = wallet.submit_rating(content_id, rating)
            return reward if success else 0
        else:
            print("  Invalid rating")
            return 0
            
    except ValueError:
        print("  Invalid input")
        return 0
    except KeyboardInterrupt:
        print("\n  Skipped rating")
        return 0


def show_content_menu(wallet):
    """Show content selection menu with auto-detection"""
    print("\n" + "=" * 60)
    print("📺 CONTENT LIBRARY")
    print("=" * 60)
    
    has_premium = wallet.has_premium_access()
    
    # Auto-detect regular content
    regular_files = []
    if os.path.exists('/opt'):
        for f in os.listdir('/opt'):
            if f.endswith('.mp4') and f != 'ad.mp4':
                regular_files.append(f)
    
    # Auto-detect premium content
    premium_files = []
    if os.path.exists('/opt/premium'):
        for f in os.listdir('/opt/premium'):
            if f.endswith('.mp4'):
                premium_files.append(f)
    
    # Build menu
    options = {}
    current_num = 1
    
    if regular_files:
        print("\n  Regular Content:")
        for f in sorted(regular_files):
            print(f"  {current_num}. {f} (Free)")
            options[str(current_num)] = {'path': f'/opt/{f}', 'premium': False, 'name': f}
            current_num += 1
    
    if premium_files:
        print("\n  Premium Content:")
        for f in sorted(premium_files):
            if has_premium:
                print(f"  {current_num}. ✅ {f} (Unlocked)")
            else:
                print(f"  {current_num}. 🔒 {f} (Requires Premium Access - 100 VIEW)")
            options[str(current_num)] = {'path': f'/opt/premium/{f}', 'premium': True, 'name': f}
            current_num += 1
    
    if not regular_files and not premium_files:
        print("\n  ⚠️  No content found!")
        print("  Place .mp4 files in /opt/ (regular) or /opt/premium/ (premium)")
    
    print("\n  0. Back to main menu")
    print("=" * 60)
    
    try:
        choice = input("\n  Select content: ").strip()
        
        if choice == '0':
            return None, False
        elif choice in options:
            content = options[choice]
            
            # Check if premium and has access
            if content['premium'] and not has_premium:
                print("\n  🔒 This is premium content!")
                print("  💳 Redeem 'Premium Content Access' (100 VIEW) to unlock")
                print("  💡 Or get VIP Status (200 VIEW) for all benefits!")
                input("\n  Press Enter to continue...")
                return None, False
            
            # Check if file exists
            if os.path.exists(content['path']):
                if content['premium']:
                    print("\n  ✨ Accessing premium content...")
                return content['path'], content['premium']
            else:
                print(f"\n  ❌ File not found: {content['path']}")
                input("  Press Enter to continue...")
                return None, False
        else:
            print("  Invalid choice")
            return None, False
    except KeyboardInterrupt:
        return None, False


def show_redemption_menu(wallet):
    """Show redemption menu"""
    print("\n" + "=" * 60)
    print("💳 REDEMPTION CENTER")
    print("=" * 60)
    
    # Get current balance
    print("\n  🔄 Checking balance...")
    balance = wallet.get_balance()
    print(f"  💰 Your Balance: {balance} VIEW tokens")
    
    # Get available redemptions
    print("\n  📋 Fetching redemptions...")
    redemptions = wallet.get_redemptions()
    
    if not redemptions:
        print("  ⚠️  Could not load redemptions")
        input("\nPress Enter to continue...")
        return
    
    print("\n  Available Rewards:\n")
    
    for i, redemption in enumerate(redemptions, 1):
        cost = redemption['cost']
        can_afford = "✅" if balance >= cost else "❌"
        print(f"  {i}. {can_afford} {redemption['name']}")
        print(f"     Cost: {cost} VIEW")
        print(f"     {redemption['description']}")
        print()
    
    print("  0. Cancel")
    print("\n" + "-" * 60)
    
    try:
        choice = input("\n  Select option (0-{}): ".format(len(redemptions))).strip()
        
        if choice == '0':
            print("  Cancelled")
            return
        
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(redemptions):
            selected = redemptions[choice_idx]
            
            if balance < selected['cost']:
                print(f"\n  ❌ Insufficient balance!")
                print(f"     Need: {selected['cost']} VIEW")
                print(f"     Have: {balance} VIEW")
                input("\n  Press Enter to continue...")
                return
            
            # Confirm
            print(f"\n  Redeem: {selected['name']}")
            print(f"  Cost: {selected['cost']} VIEW")
            confirm = input("  Confirm? (y/n): ").strip().lower()
            
            if confirm == 'y':
                success, result = wallet.redeem(selected['type'])
                if success:
                    print("\n  🎉 Benefit activated!")
                    input("\n  Press Enter to continue...")
                else:
                    input("\n  Press Enter to continue...")
            else:
                print("  Cancelled")
        else:
            print("  Invalid choice")
            
    except ValueError:
        print("  Invalid input")
    except KeyboardInterrupt:
        print("\n  Cancelled")
    
    time.sleep(1)


def show_badges_menu(wallet):
    """Show user's achievement badges (NFTs)"""
    print("\n" + "=" * 60)
    print("🏆 ACHIEVEMENT BADGES")
    print("=" * 60)
    
    print("\n  🔄 Loading badges...")
    badges_data = wallet.get_badges()
    
    if not badges_data or not badges_data.get('success'):
        print("  ⚠️  Could not load badges")
        input("\n  Press Enter to continue...")
        return
    
    owned = badges_data.get('owned_badges', [])
    available = badges_data.get('available_badges', [])
    total = badges_data.get('total_badges', 0)
    owned_count = badges_data.get('owned_count', 0)
    nft_token_id = badges_data.get('nft_token_id', '')
    
    print(f"\n  📊 Progress: {owned_count}/{total} badges earned")
    
    if nft_token_id:
        print(f"  🎨 NFT Collection: {nft_token_id}")
        print(f"  🔗 HashScan: https://hashscan.io/testnet/token/{nft_token_id}")
    
    if owned:
        print("\n  🎖️  Owned Badges:\n")
        for badge in owned:
            print(f"  {badge['icon']} {badge['name']}")
            print(f"     {badge['description']}")
            if badge.get('nft_serial'):
                print(f"     NFT Serial: #{badge['nft_serial']}")
            if badge.get('hashscan_url'):
                print(f"     View: {badge['hashscan_url']}")
            print()
    else:
        print("\n  💡 No badges earned yet! Start watching to unlock achievements!")
    
    if available:
        print("\n  🔓 Available Badges:\n")
        for badge in available:
            req_text = f" ({badge['requirement']} required)" if badge.get('requirement') else ""
            print(f"  🔒 {badge['name']}{req_text}")
            print(f"     {badge['description']}")
            print()
    
    print("=" * 60)
    input("\n  Press Enter to continue...")


def print_banner(text, char="=", width=60):
    """Print banner"""
    print("")
    print(char * width)
    print(text.center(width))
    print(char * width)


def print_summary(wallet, ad_result, content_result, rating_reward=0, binge_bonus=0, binge_msg=None):
    """Print summary"""
    print_banner("SESSION SUMMARY", "═", 60)
    print("")
    
    if ad_result:
        if ad_result['completed']:
            print(f"  📺 Ad watched ({ad_result['watch_time']:.1f}s):     +{ad_result['reward']} VIEW")
        elif ad_result['skipped']:
            print(f"  📺 Ad skipped ({ad_result['watch_time']:.1f}s):     +{ad_result['reward']} VIEW")
    
    if content_result:
        if content_result['completed']:
            print(f"  🎬 Content ({content_result['watch_time']:.1f}s):        +{content_result['reward']} VIEW")
        elif content_result['reward'] > 0:
            print(f"  🎬 Partial ({content_result['watch_time']:.1f}s):        +{content_result['reward']} VIEW")
    
    if rating_reward > 0:
        print(f"  ⭐ Rating submitted:              +{rating_reward} VIEW")
    
    if binge_bonus > 0:
        print(f"  🎉 Binge bonus ({wallet.videos_watched_count} videos):         +{binge_bonus} VIEW")
    
    total = (ad_result['reward'] if ad_result else 0) + \
            (content_result['reward'] if content_result else 0) + \
            rating_reward + binge_bonus
    
    print("")
    print(f"  {'─' * 50}")
    print(f"  💰 Session earnings:  +{total} VIEW")
    
    # Check for new achievements
    print(f"\n  🏆 Checking for new achievements...")
    wallet.check_achievements()
    
    # Wait for blockchain
    print(f"\n  ⏳ Waiting for blockchain...", end='', flush=True)
    for i in range(5, 0, -1):
        print(f" {i}", end='', flush=True)
        time.sleep(1)
    print(" Done!")
    
    # Get balance
    print(f"  🔗 Querying blockchain...")
    balance = wallet.get_balance()
    print(f"  💳 Blockchain balance: {balance:,} VIEW")
    print(f"     Token ID: {TOKEN_ID}")
    
    if binge_msg and binge_bonus == 0:
        print(f"\n  💡 Tip: {binge_msg}")
    
    print("")
    print("═" * 60)


def main():
    """Main function"""
    print_banner("REWARDS TV - Phase 2: NFT Achievement Badges", "═", 70)
    
    # Parse arguments - all optional now
    ad_path = None
    use_display = False
    
    # Parse args
    for arg in sys.argv[1:]:
        if arg == '--display':
            use_display = True
        elif arg.endswith('.mp4'):
            # Assume this is an ad file
            if os.path.exists(arg):
                ad_path = arg
                print(f"  📁 Using ad file: {arg}")
            else:
                print(f"  ⚠️  Ad file not found: {arg}")
    
    # If no ad specified, try default location
    if not ad_path:
        if os.path.exists('/opt/ad.mp4'):
            ad_path = '/opt/ad.mp4'
            print(f"  📁 Using default ad: /opt/ad.mp4")
        else:
            print(f"  ℹ️  No ad file (content will play without ads)")
    
    # Show config
    print(f"\n🖥️  Display: {'ON' if use_display else 'OFF'}")
    print(f"🔗 Blockchain: Hedera Testnet")
    print(f"   Account: {ACCOUNT_ID}")
    print(f"   Token: {TOKEN_ID} (VIEW)")
    
    # Init wallet
    wallet = BlockchainWallet()
    
    # Device registration
    print(f"\n🔐 Device Security Check...")
    if not wallet.register_device():
        print("\n" + "=" * 60)
        print("❌ DEVICE REGISTRATION FAILED")
        print("=" * 60)
        print("\n  This device could not be registered.")
        print("  Possible reasons:")
        print("  • Device already registered to another account")
        print("  • Account already has a registered device")
        print("  • Network error")
        print("\n  Contact support if this is an error.")
        print("=" * 60)
        input("\n  Press Enter to exit...")
        return 1
    
    # Start session
    print(f"\n📺 Starting viewing session...")
    wallet.start_session()
    
    # Check for active benefits
    print(f"\n🎁 Checking active benefits...")
    benefits = wallet.check_benefits()
    
    if benefits:
        benefit_name = benefits['name']
        remaining = benefits.get('remaining_seconds', 0)
        print(f"   ✨ Active: {benefit_name}")
        print(f"   ⏱️  Remaining: {remaining // 60}m {remaining % 60}s")
        
        # Show what benefits are active
        benefit_type = benefits['type']
        if benefit_type == 'vip_day':
            print(f"   🌟 VIP Benefits:")
            print(f"      • Skip all ads")
            print(f"      • Access premium content")
            print(f"      • 2x reward multiplier")
        elif benefit_type in ['skip_ads', 'ad_free_hour']:
            print(f"   • Ads will be skipped")
        elif benefit_type == 'premium_content':
            print(f"   • Premium content unlocked")
    else:
        print(f"   No active benefits")
    
    # Get initial balance
    print(f"\n💳 Checking balance...")
    initial_balance = wallet.get_balance()
    print(f"   Balance: {initial_balance:,} VIEW")
    
    # Init Westeros
    westeros = None
    if use_display:
        westeros = WesterosManager()
        if not westeros.start_westeros():
            print("\n⚠️  Display failed, using console mode")
            use_display = False
    
    print("\n" + "─" * 60)
    print("MAIN MENU")
    print("─" * 60)
    print("1. Watch Content")
    print("2. Redemption Center")
    print("3. Achievement Badges")
    print("4. Check Balance")
    print("0. Exit")
    print("─" * 60)
    
    try:
        while True:
            choice = input("\nSelect option: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                # Show content selection
                content_to_play, is_premium = show_content_menu(wallet)
                
                if not content_to_play:
                    # Show menu again
                    print("\n" + "─" * 60)
                    print("MAIN MENU")
                    print("─" * 60)
                    print("1. Watch Content")
                    print("2. Redemption Center")
                    print("3. Achievement Badges")
                    print("4. Check Balance")
                    print("0. Exit")
                    print("─" * 60)
                    continue
                
                # Track in session
                content_id = os.path.basename(content_to_play)
                wallet.track_video(content_id)
                
                # Check if should skip ads
                skip_ads = wallet.has_ad_skip()
                
                ad_result = None
                if ad_path and not is_premium:  # Premium content has no ads
                    ad_manager = AdManager(ad_path, use_display=use_display, skip_ads=skip_ads)
                    ad_result = ad_manager.play_ad()
                    
                    if ad_result['reward'] > 0:
                        wallet.send_reward(ad_result['reward'], "Ad viewing")
                    
                    if ad_result['completed'] or ad_result['skipped']:
                        print("\n  Starting content in 2s...")
                        time.sleep(2)
                elif is_premium:
                    print("\n  ✨ Premium content - No ads!")
                    time.sleep(1)
                
                # Play content
                content_player = ContentPlayer(content_to_play, use_display=use_display)
                content_result = content_player.play_content()
                
                if content_result['reward'] > 0:
                    wallet.send_reward(content_result['reward'], "Content viewing")
                
                # Prompt for rating
                rating_reward = 0
                if content_result['completed'] or content_result['watch_time'] > 30:
                    rating_reward = prompt_rating(wallet, content_id)
                
                # Check binge bonus
                binge_bonus, binge_msg = wallet.check_binge_bonus()
                
                # Summary
                print_summary(wallet, ad_result, content_result, rating_reward, binge_bonus, binge_msg)
                
                # Show menu again
                print("\n" + "─" * 60)
                print("MAIN MENU")
                print("─" * 60)
                print("1. Watch Content")
                print("2. Redemption Center")
                print("3. Achievement Badges")
                print("4. Check Balance")
                print("0. Exit")
                print("─" * 60)
                
            elif choice == '2':
                # Redemption
                show_redemption_menu(wallet)
                
                # Refresh benefits
                benefits = wallet.check_benefits()
                
                # Show menu again
                print("\n" + "─" * 60)
                print("MAIN MENU")
                print("─" * 60)
                print("1. Watch Content")
                print("2. Redemption Center")
                print("3. Achievement Badges")
                print("4. Check Balance")
                print("0. Exit")
                print("─" * 60)
                
            elif choice == '3':
                # Achievement Badges
                show_badges_menu(wallet)
                
                # Show menu again
                print("\n" + "─" * 60)
                print("MAIN MENU")
                print("─" * 60)
                print("1. Watch Content")
                print("2. Redemption Center")
                print("3. Achievement Badges")
                print("4. Check Balance")
                print("0. Exit")
                print("─" * 60)
                
            elif choice == '4':
                # Check balance
                print(f"\n  🔄 Checking balance...")
                balance = wallet.get_balance()
                print(f"  💳 Balance: {balance:,} VIEW")
                print(f"  📺 Videos watched this session: {wallet.videos_watched_count}")
                
                # Show active benefits
                benefits = wallet.check_benefits()
                if benefits:
                    benefit_type = benefits['type']
                    benefit_name = benefits['name']
                    remaining = benefits.get('remaining_seconds', 0)
                    
                    print(f"\n  ✨ Active Benefit: {benefit_name}")
                    print(f"  ⏱️  Time Remaining: {remaining // 60}m {remaining % 60}s")
                    
                    if benefit_type == 'vip_day':
                        print(f"\n  🌟 VIP Perks Active:")
                        print(f"     • All ads skipped")
                        print(f"     • Premium content access")
                        print(f"     • 2x rewards on everything")
                    elif benefit_type in ['skip_ads', 'ad_free_hour']:
                        print(f"\n  • Ad skipping enabled")
                    elif benefit_type == 'premium_content':
                        print(f"\n  • Premium library unlocked")
                else:
                    print(f"\n  No active benefits")
                    print(f"  💡 Visit Redemption Center to unlock perks!")
                
                # Show badges summary
                badges_data = wallet.get_badges()
                if badges_data and badges_data.get('success'):
                    owned_count = badges_data.get('owned_count', 0)
                    total = badges_data.get('total_badges', 0)
                    print(f"\n  🏆 Badges: {owned_count}/{total} earned")
                    
            else:
                print("  Invalid choice")
        
    finally:
        if westeros:
            westeros.stop_westeros()
    
    print("\n✅ Thank you for using Rewards TV!")
    print(f"🔐 Device: {wallet.device_id[:30]}...")
    
    # Final badge check
    badges_data = wallet.get_badges()
    if badges_data and badges_data.get('success'):
        owned_count = badges_data.get('owned_count', 0)
        print(f"🏆 Total Badges Earned: {owned_count}")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Interrupted")
        sys.exit(1)
