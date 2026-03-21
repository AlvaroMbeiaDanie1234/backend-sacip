import time
import random
import requests
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from datetime import datetime
import feedparser
from bs4 import BeautifulSoup
# snscrape has been completely removed from the project
SNSCRAPE_AVAILABLE = False  # Always False since snscrape is no longer part of the project
sntwitter = None
sninstagram = None
snfacebook = None
snreddit = None

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import zendriver as zd

from django.conf import settings
from .models import PerfilRedeSocial, Postagem


class ProxyRotator:
    """Class to handle proxy rotation for ethical scraping"""
    
    def __init__(self):
        self.proxies = self._load_proxies()
        self.current_proxy_index = 0
        self.failed_proxies = set()  # Track failed proxies
    
    def _load_proxies(self) -> List[str]:
        """Load proxy list from settings or external source"""
        # This could be loaded from settings or an external proxy service
        # For now, we'll return an empty list and let individual requests decide
        return getattr(settings, 'SCRAPING_PROXIES', [])
    
    def _is_proxy_working(self, proxy: str) -> bool:
        """Test if a proxy is working"""
        try:
            test_url = 'http://httpbin.org/ip'  # A simple test endpoint
            proxies = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}'
            }
            response = requests.get(test_url, proxies=proxies, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def get_next_working_proxy(self) -> Optional[Dict[str, str]]:
        """Get next working proxy in rotation"""
        if not self.proxies:
            return None
        
        # Try to find a working proxy
        for _ in range(len(self.proxies)):
            proxy = self.proxies[self.current_proxy_index % len(self.proxies)]
            self.current_proxy_index += 1
            
            # Skip if we've already determined this proxy doesn't work
            if proxy in self.failed_proxies:
                continue
            
            # Test if proxy is working
            if self._is_proxy_working(proxy):
                # Format for requests library
                return {
                    'http': f'http://{proxy}',
                    'https': f'http://{proxy}'
                }
            else:
                # Mark as failed to avoid trying again
                self.failed_proxies.add(proxy)
        
        # If no working proxies found, return None
        return None
    
    def get_next_proxy(self) -> Optional[Dict[str, str]]:
        """Get next proxy in rotation (with working status check)"""
        return self.get_next_working_proxy()


class EthicalScraper:
    """Main class for ethical social media scraping"""
    
    def __init__(self):
        self.proxy_rotator = ProxyRotator()
        self.ua = UserAgent()
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Initialize Selenium webdriver with proxy support
        self.webdriver = None
        
    def _setup_selenium_driver(self, proxy: Optional[Dict[str, str]] = None):
        """Setup Selenium WebDriver with proxy support"""
        chrome_options = Options()
        
        # Add various options to avoid detection
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Add proxy if provided
        if proxy:
            proxy_server = proxy.get('http', '').replace('http://', '')
            if proxy_server:
                chrome_options.add_argument(f'--proxy-server=http://{proxy_server}')
        
        # Set a realistic user agent
        chrome_options.add_argument(f'--user-agent={self.ua.random}')
        
        # Create undetected Chrome driver with zendriver
        try:
            # zendriver doesn't use Chrome options in the same way
            # Instead, we pass arguments directly
            args = []
            if proxy:
                proxy_server = proxy.get('http', '').replace('http://', '')
                if proxy_server:
                    args.append(f'--proxy-server=http://{proxy_server}')
            
            # Add other options as arguments
            args.extend([
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled',
                f'--user-agent={self.ua.random}'
            ])
            
            self.webdriver = zd.start(
                headless=False,  # Set to True if you want headless mode
                # Add the arguments
                args=args
            )
            
            # Execute script to remove webdriver property
            self.webdriver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except Exception as e:
            print(f"Error setting up Chrome driver: {str(e)}")
            # Fallback to regular Chrome if zendriver fails
            self.webdriver = webdriver.Chrome(options=chrome_options)
            self.webdriver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    def _teardown_selenium_driver(self):
        """Close and cleanup Selenium WebDriver"""
        if self.webdriver:
            self.webdriver.quit()
            self.webdriver = None
    
    def scrape_with_selenium(self, url: str, wait_selector: Optional[str] = None, use_proxy: bool = True) -> Optional[str]:
        """Scrape content using Selenium with proxy support"""
        # Add random delay to be respectful
        time.sleep(random.uniform(2, 5))
        
        # Get proxy if needed
        proxy = self.proxy_rotator.get_next_proxy() if use_proxy else None
        
        try:
            # Setup driver with proxy
            self._setup_selenium_driver(proxy)
            
            # Navigate to URL
            self.webdriver.get(url)
            
            # Check for common CMS error pages or access denied
            page_title = self.webdriver.title.lower() if self.webdriver.title else ""
            if any(term in page_title for term in ['access denied', '403 forbidden', '404 not found', 'captcha', 'blocked']):
                print(f"⚠️  Blocked by CMS or anti-bot protection at {url}")
                return None
            
            # Wait for specific element if selector provided
            if wait_selector:
                wait = WebDriverWait(self.webdriver, 10)
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, wait_selector)))
                except Exception as timeout_error:
                    print(f"⏱️  Timeout waiting for element at {url}: {str(timeout_error)}")
                    # Continue anyway, the element might not be critical
                    pass
            else:
                # Wait a bit for page to load
                time.sleep(3)
            
            # Get page source
            page_source = self.webdriver.page_source
            
            return page_source
        except Exception as e:
            error_msg = str(e)
            # Check for common CMS/anti-bot errors
            if 'cms' in error_msg.lower() or 'cloudflare' in error_msg.lower() or 'akamai' in error_msg.lower():
                print(f"🚫 CMS/Anti-bot protection detected at {url}: {error_msg}")
            else:
                print(f"❌ Error scraping with Selenium {url}: {error_msg}")
            return None
        finally:
            # Cleanup
            self._teardown_selenium_driver()
    
    def _make_request(self, url: str, use_proxy: bool = True) -> Optional[requests.Response]:
        """Make a request with optional proxy rotation and rate limiting"""
        # Add respectful delay to implement rate limiting
        self._respectful_delay(url)
        
        # Get proxy if needed
        proxies = self.proxy_rotator.get_next_proxy() if use_proxy else None
        
        try:
            response = self.session.get(
                url,
                proxies=proxies,
                timeout=30,
                headers={'User-Agent': self.ua.random}  # Refresh user agent
            )
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Error making request to {url}: {str(e)}")
            return None
    
    def _respectful_delay(self, url: str):
        """Implement rate limiting based on domain to be respectful to servers"""
        domain = urlparse(url).netloc
        
        # Get last access time for this domain
        last_access = getattr(self, '_last_access_times', {})
        current_time = time.time()
        
        # Set default if not initialized
        if not hasattr(self, '_last_access_times'):
            self._last_access_times = {}
        
        # Check if we accessed this domain recently
        if domain in self._last_access_times:
            time_since_last = current_time - self._last_access_times[domain]
            
            # Minimum delay of 1-3 seconds between requests to same domain
            min_delay = random.uniform(1, 3)
            if time_since_last < min_delay:
                time.sleep(min_delay - time_since_last)
        
        # Update last access time
        self._last_access_times[domain] = time.time()
    
    def scrape_with_selenium(self, url: str, wait_selector: Optional[str] = None, use_proxy: bool = True) -> Optional[str]:
        """Scrape content using Selenium with proxy support and rate limiting"""
        # Add respectful delay to be respectful
        self._respectful_delay(url)
        
        # Get proxy if needed
        proxy = self.proxy_rotator.get_next_proxy() if use_proxy else None
        
        try:
            # Setup driver with proxy
            self._setup_selenium_driver(proxy)
            
            # Navigate to URL
            self.webdriver.get(url)
            
            # Wait for specific element if selector provided
            if wait_selector:
                wait = WebDriverWait(self.webdriver, 10)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, wait_selector)))
            else:
                # Wait a bit for page to load
                time.sleep(3)
            
            # Get page source
            page_source = self.webdriver.page_source
            
            return page_source
        except Exception as e:
            print(f"Error scraping with Selenium {url}: {str(e)}")
            return None
        finally:
            # Cleanup
            self._teardown_selenium_driver()
    
    def scrape_twitter_profile(self, username: str) -> Optional[Dict]:
        """Scrape public Twitter/X profile information using alternative methods"""
        # snscrape has been removed, using alternative approach
        try:
            # Using Selenium to scrape Twitter profile
            url = f'https://twitter.com/{username}'
            page_source = self.scrape_with_selenium(url, wait_selector='[data-testid="primaryColumn"]', use_proxy=True)
            
            if not page_source:
                print(f"⚠️  Failed to get Twitter profile page for {username}")
                return None
                
            soup = BeautifulSoup(page_source, 'html.parser')
            # Extract profile information using BeautifulSoup
            name_element = soup.find('h2', {'data-testid': 'primaryColumn'})
            bio_element = soup.find('div', {'data-testid': 'UserDescription'})
            
            profile_data = {
                'nome_usuario': username,
                'nome_completo': name_element.get_text().strip() if name_element else username,
                'biografia': bio_element.get_text().strip() if bio_element else '',
                'url_perfil': url,
                'plataforma': 'twitter'
            }
            
            print(f"✅ Successfully scraped Twitter profile for {username}")
            return profile_data
            
        except Exception as e:
            print(f"❌ Error scraping Twitter profile {username}: {str(e)}")
            import traceback
            traceback.print_exc()
        
        return None
    
    def scrape_twitter_posts(self, username: str, limit: int = 10) -> List[Dict]:
        """Scrape public Twitter/X posts using alternative methods"""
        # snscrape has been removed, using alternative approach
        posts = []
        try:
            # Using Selenium to scrape Twitter posts
            url = f'https://twitter.com/{username}'
            print(f"   🐦 Scraping Twitter posts from {url}...")
            
            page_source = self.scrape_with_selenium(url, wait_selector='[data-testid="tweet"]', use_proxy=True)
            
            if not page_source:
                print(f"   ⚠️  Failed to load Twitter page for {username}")
                return []
            
            # Check if we hit rate limiting or CMS protection
            if 'Something went wrong' in page_source or 'Rate Limit' in page_source:
                print(f"   ⚠️  Twitter returned an error page (possible rate limit or CMS block)")
                return []
            
            soup = BeautifulSoup(page_source, 'html.parser')
            tweet_elements = soup.find_all('article', {'data-testid': 'tweet'})
            
            print(f"   📊 Found {len(tweet_elements)} tweets on page")
            
            for i, tweet_element in enumerate(tweet_elements[:limit]):
                # Extract tweet content
                content_element = tweet_element.find('div', {'data-testid': 'tweetText'})
                content = content_element.get_text().strip() if content_element else ''
                
                if content:  # Only add if there's actual content
                    posts.append({
                        'post_id': f'tweet_{i}_{username}',
                        'conteudo': content,
                        'data_postagem': datetime.now(),
                        'curtidas': 0,
                        'comentarios': 0,
                        'compartilhamentos': 0,
                        'url_postagem': url,
                        'marcadores': '',
                    })
            
            print(f"   ✅ Extracted {len(posts)} posts from Twitter")
            
        except Exception as e:
            print(f"   ❌ Error scraping Twitter posts for {username}: {str(e)}")
            import traceback
            traceback.print_exc()
        
        return posts
    
    def scrape_instagram_profile(self, username: str) -> Optional[Dict]:
        """Scrape public Instagram profile information"""
        # snscrape has been removed, using alternative approach
        try:
            # Using Selenium to scrape Instagram profile
            url = f'https://instagram.com/{username}'
            page_source = self.scrape_with_selenium(url, wait_selector='header', use_proxy=True)
            
            if page_source:
                soup = BeautifulSoup(page_source, 'html.parser')
                header_element = soup.find('header')
                
                if header_element:
                    # Extract profile information
                    full_name_element = header_element.find('h2', {'class': '_7UhW9'})
                    bio_element = header_element.find('div', {'class': '-vDIg'})
                    
                    return {
                        'nome_usuario': username,
                        'nome_completo': full_name_element.get_text().strip() if full_name_element else username,
                        'biografia': bio_element.get_text().strip() if bio_element else '',
                        'url_perfil': url,
                        'plataforma': 'instagram'
                    }
        except Exception as e:
            print(f"Error scraping Instagram profile {username}: {str(e)}")
        
        return None
    
    def scrape_instagram_posts(self, username: str, limit: int = 10) -> List[Dict]:
        """Scrape public Instagram posts"""
        posts = []
        try:
            # Using Selenium to scrape Instagram posts
            url = f'https://instagram.com/{username}'
            page_source = self.scrape_with_selenium(url, wait_selector='article', use_proxy=True)
            
            if page_source:
                soup = BeautifulSoup(page_source, 'html.parser')
                post_elements = soup.find_all('article')
                
                for i, post_element in enumerate(post_elements[:limit]):
                    # Extract post information
                    caption_element = post_element.find('div', {'class': 'C4VMK'})
                    caption = caption_element.get_text().strip() if caption_element else ''
                    
                    posts.append({
                        'post_id': f'insta_post_{i}',
                        'conteudo': caption,
                        'data_postagem': datetime.now(),
                        'curtidas': 0,  # Would need more complex parsing
                        'comentarios': 0,
                        'compartilhamentos': 0,
                        'url_postagem': url,
                        'marcadores': '',
                    })
        except Exception as e:
            print(f"Error scraping Instagram posts for {username}: {str(e)}")
        
        return posts
    
    def scrape_facebook_public_posts(self, page_name: str, limit: int = 10) -> List[Dict]:
        """Scrape public Facebook posts (requires careful implementation)"""
        posts = []
        # Facebook is very restrictive, using generic scraping as an alternative
        # This is a placeholder for more complex implementation
        try:
            # Using Selenium to scrape Facebook page
            url = f'https://facebook.com/{page_name}'
            page_source = self.scrape_with_selenium(url, wait_selector='[data-pagelet="Feed"]', use_proxy=True)
            
            if page_source:
                soup = BeautifulSoup(page_source, 'html.parser')
                # Find Facebook post elements (this is a simplified approach)
                post_elements = soup.find_all('div', {'data-testid': 'fbfeed_story'})
                
                for i, post_element in enumerate(post_elements[:limit]):
                    # Extract post content
                    content_element = post_element.find('div', {'data-testid': 'post_message'})
                    content = content_element.get_text().strip() if content_element else ''
                    
                    posts.append({
                        'post_id': f'fb_post_{i}',
                        'conteudo': content,
                        'data_postagem': datetime.now(),
                        'curtidas': 0,  # Would need more complex parsing
                        'comentarios': 0,
                        'compartilhamentos': 0,
                        'url_postagem': url,
                        'marcadores': '',
                    })
        except Exception as e:
            print(f"Error scraping Facebook posts for {page_name}: {str(e)}")
            
        return posts
    
    def scrape_reddit_profile(self, username: str) -> Optional[Dict]:
        """Scrape Reddit user profile"""
        try:
            # Get user info from Reddit API
            response = self._make_request(f'https://www.reddit.com/user/{username}/about.json')
            if response:
                data = response.json()
                user_data = data['data']
                return {
                    'nome_usuario': user_data.get('name', username),
                    'nome_completo': f"u/{user_data.get('name', username)}",
                    'biografia': user_data.get('subreddit', {}).get('public_description', ''),
                    'url_perfil': f'https://reddit.com/user/{username}',
                    'plataforma': 'reddit'
                }
        except Exception as e:
            print(f"Error scraping Reddit profile {username}: {str(e)}")
        
        return None
    
    def scrape_reddit_posts(self, username: str, limit: int = 10) -> List[Dict]:
        """Scrape Reddit posts by user"""
        posts = []
        try:
            response = self._make_request(f'https://www.reddit.com/user/{username}/submitted.json')
            if response:
                data = response.json()
                for i, item in enumerate(data['data']['children'][:limit]):
                    post_data = item['data']
                    posts.append({
                        'post_id': post_data.get('id', str(i)),
                        'conteudo': post_data.get('title', '') + ' ' + post_data.get('selftext', ''),
                        'data_postagem': datetime.fromtimestamp(post_data.get('created_utc', time.time())),
                        'curtidas': post_data.get('score', 0),
                        'comentarios': post_data.get('num_comments', 0),
                        'compartilhamentos': 0,  # Reddit doesn't have shares in the traditional sense
                        'url_postagem': f"https://reddit.com{post_data.get('permalink', '')}",
                        'marcadores': '',
                    })
        except Exception as e:
            print(f"Error scraping Reddit posts for {username}: {str(e)}")
        
        return posts
    
    def scrape_generic_social_content(self, url: str) -> List[Dict]:
        """Scrape generic social media content from a URL"""
        posts = []
        
        # Try regular requests first
        response = self._make_request(url)
        soup = None
        
        if response:
            soup = BeautifulSoup(response.content, 'html.parser')
        else:
            # If regular requests fail, try with Selenium
            page_source = self.scrape_with_selenium(url)
            if page_source:
                soup = BeautifulSoup(page_source, 'html.parser')
        
        if soup:
            # This is a basic implementation - in practice, you'd need platform-specific selectors
            # Look for common social media post patterns
            post_elements = soup.find_all(['div', 'article'], class_=lambda x: x and any(keyword in x.lower() for keyword in ['post', 'tweet', 'status', 'entry', 'feed', 'timeline']))
            
            for i, element in enumerate(post_elements):
                posts.append({
                    'post_id': f'generic_{i}',
                    'conteudo': element.get_text()[:500],  # Limit content
                    'data_postagem': datetime.now(),
                    'curtidas': 0,  # Not available in generic scraping
                    'comentarios': 0,
                    'compartilhamentos': 0,
                    'url_postagem': url,
                    'marcadores': '',
                })
        
        return posts


class SocialMediaScraperService:
    """Service class to manage social media scraping operations"""
    
    def __init__(self):
        self.scraper = EthicalScraper()
    
    def sync_profile_data(self, perfil_id: int) -> bool:
        """Sync profile data from social media platform"""
        try:
            perfil = PerfilRedeSocial.objects.get(id=perfil_id)
            plataforma = perfil.plataforma
            username = perfil.nome_usuario
            
            print(f"\n🔄 Starting profile sync for {username} on {plataforma}...")
            
            if plataforma == 'twitter':
                profile_data = self.scraper.scrape_twitter_profile(username)
            elif plataforma == 'instagram':
                profile_data = self.scraper.scrape_instagram_profile(username)
            elif plataforma == 'facebook':
                # For Facebook, we could use the generic scraping approach
                profile_data = None  # Facebook profile scraping is complex, so we'll skip it for now
            elif plataforma == 'reddit':
                profile_data = self.scraper.scrape_reddit_profile(username)
            else:
                # For other platforms, we might need different approaches
                print(f"⚠️  Unknown platform: {plataforma}")
                profile_data = None
            
            if profile_data:
                perfil.nome_completo = profile_data.get('nome_completo', perfil.nome_completo)
                perfil.biografia = profile_data.get('biografia', perfil.biografia)
                perfil.url_perfil = profile_data.get('url_perfil', perfil.url_perfil)
                perfil.save()
                print(f"✅ Profile synced successfully for {username}")
                return True
            else:
                print(f"⚠️  No data retrieved for {username} on {plataforma}")
                return False
                
        except PerfilRedeSocial.DoesNotExist:
            print(f"❌ Profile {perfil_id} not found")
            return False
        except Exception as e:
            print(f"❌ Error syncing profile {perfil_id}: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def sync_profile_posts(self, perfil_id: int, limit: int = 10) -> int:
        """Sync posts from a social media profile"""
        try:
            perfil = PerfilRedeSocial.objects.get(id=perfil_id)
            plataforma = perfil.plataforma
            username = perfil.nome_usuario
            new_posts_count = 0
            
            print(f"\n📥 Starting post sync for {username} on {plataforma} (limit: {limit})...")
            
            if plataforma == 'twitter':
                posts_data = self.scraper.scrape_twitter_posts(username, limit)
            elif plataforma == 'instagram':
                posts_data = self.scraper.scrape_instagram_posts(username, limit)
            elif plataforma == 'facebook':
                # For Facebook, use generic scraping as snscrape may not work well
                posts_data = self.scraper.scrape_generic_social_content(perfil.url_perfil)
            elif plataforma == 'reddit':
                posts_data = self.scraper.scrape_reddit_posts(username, limit)
            else:
                # For other platforms or generic URLs
                posts_data = self.scraper.scrape_generic_social_content(perfil.url_perfil)
            
            if not posts_data:
                print(f"⚠️  No posts found for {username} on {plataforma}")
                return 0
            
            print(f"📊 Found {len(posts_data)} posts to process")
            
            for i, post_data in enumerate(posts_data, 1):
                try:
                    # Check if post already exists
                    post, created = Postagem.objects.get_or_create(
                        post_id=post_data['post_id'],
                        perfil=perfil,
                        defaults={
                            'conteudo': post_data['conteudo'],
                            'data_postagem': post_data['data_postagem'],
                            'curtidas': post_data['curtidas'],
                            'comentarios': post_data['comentarios'],
                            'compartilhamentos': post_data['compartilhamentos'],
                            'url_postagem': post_data['url_postagem'],
                            'marcadores': post_data['marcadores'],
                        }
                    )
                    
                    if created:
                        new_posts_count += 1
                        if new_posts_count % 5 == 0:  # Log every 5 new posts
                            print(f"   ↳ Added {new_posts_count} new posts so far...")
                            
                except Exception as post_error:
                    print(f"⚠️  Error processing post {i}: {str(post_error)}")
                    continue  # Continue with next post instead of failing completely
            
            print(f"✅ Successfully added {new_posts_count} new posts for {username}")
            return new_posts_count
            
        except PerfilRedeSocial.DoesNotExist:
            print(f"❌ Profile {perfil_id} not found")
            return 0
        except Exception as e:
            print(f"❌ Error syncing posts for profile {perfil_id}: {str(e)}")
            import traceback
            traceback.print_exc()
            return 0
    
    def scrape_profile_and_posts(self, perfil_id: int, limit: int = 10) -> Dict[str, int]:
        """Complete sync of profile and posts"""
        print(f"\n{'='*60}")
        print(f"🚀 Starting complete sync for Profile ID: {perfil_id}")
        print(f"{'='*60}")
        
        try:
            # First sync profile data
            print("\n📋 Step 1: Syncing profile data...")
            profile_synced = self.sync_profile_data(perfil_id)
            
            # Then sync posts
            print("\n📝 Step 2: Syncing posts...")
            posts_count = self.sync_profile_posts(perfil_id, limit)
            
            print(f"\n{'='*60}")
            print(f"✅ Complete sync finished for Profile ID: {perfil_id}")
            print(f"   - Profile synced: {profile_synced}")
            print(f"   - New posts found: {posts_count}")
            print(f"{'='*60}\n")
            
            return {
                'profile_synced': profile_synced,
                'new_posts_count': posts_count
            }
            
        except Exception as e:
            print(f"\n❌ Critical error in complete sync for Profile ID {perfil_id}: {str(e)}")
            import traceback
            traceback.print_exc()
            # Return partial results instead of failing completely
            return {
                'profile_synced': False,
                'new_posts_count': 0,
                'error': str(e)
            }
    
    def scrape_by_platform(self, plataforma: str, limit: int = 10) -> List[Dict]:
        """Scrape multiple profiles from a specific platform"""
        print(f"\n{'='*80}")
        print(f"🌐 Starting platform-wide scan for: {plataforma.upper()}")
        print(f"{'='*80}\n")
        
        perfis = PerfilRedeSocial.objects.filter(plataforma=plataforma, ativo=True)
        total_perfis = perfis.count()
        
        print(f"📊 Found {total_perfis} active profile(s) to scan on {plataforma}\n")
        
        results = []
        success_count = 0
        error_count = 0
        
        for i, perfil in enumerate(perfis, 1):
            try:
                print(f"\n▶️  Processing profile {i}/{total_perfis}: {perfil.nome_usuario}")
                result = self.scrape_profile_and_posts(perfil.id, limit)
                
                if result.get('profile_synced') or result.get('new_posts_count', 0) > 0:
                    success_count += 1
                else:
                    error_count += 1
                
                results.append({
                    'perfil_id': perfil.id,
                    'perfil_nome': perfil.nome_usuario,
                    'result': result,
                    'status': 'success' if (result.get('profile_synced') or result.get('new_posts_count', 0) > 0) else 'warning'
                })
                
            except Exception as e:
                error_count += 1
                print(f"\n❌ Error processing profile {perfil.nome_usuario} (ID: {perfil.id}): {str(e)}")
                import traceback
                traceback.print_exc()
                
                # Add error result but continue with next profile
                results.append({
                    'perfil_id': perfil.id,
                    'perfil_nome': perfil.nome_usuario,
                    'result': {
                        'profile_synced': False,
                        'new_posts_count': 0,
                        'error': str(e)
                    },
                    'status': 'error'
                })
                # Continue with next profile - don't let one failure stop the whole scan
        
        print(f"\n{'='*80}")
        print(f"🏁 Platform scan completed for {plataforma.upper()}")
        print(f"   ✅ Successful: {success_count}")
        print(f"   ⚠️  With warnings: {error_count}")
        print(f"   📊 Total processed: {len(results)}/{total_perfis}")
        print(f"{'='*80}\n")
        
        return results