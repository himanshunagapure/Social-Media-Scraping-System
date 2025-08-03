"""
Instagram Scraper - Main Entry Point
Simple interface for scraping Instagram URLs with anti-detection features

Usage:
    from main import InstagramScraper
    
    scraper = InstagramScraper()
    result = await scraper.scrape(urls)
    
    # Or use the convenience function
    result = await scrape_instagram_urls(urls)
"""

import asyncio
import json
import time
from typing import List, Dict, Any, Optional
from src.advanced_graphql_extractor import AdvancedGraphQLExtractor


class InstagramScraper:
    """
    Main Instagram scraper class with anti-detection features
    
    Provides a simple interface for scraping Instagram URLs and returning
    clean, structured JSON data.
    """
    
    def __init__(self, 
                 headless: bool = True, 
                 enable_anti_detection: bool = True,
                 is_mobile: bool = False,
                 output_file: Optional[str] = None):
        """
        Initialize the Instagram scraper
        
        Args:
            headless: Run browser in headless mode (default: True)
            enable_anti_detection: Enable anti-detection features (default: True)
            is_mobile: Use mobile user agent and viewport (default: False)
            output_file: Optional file path to save results (default: None)
        """
        self.headless = headless
        self.enable_anti_detection = enable_anti_detection
        self.is_mobile = is_mobile
        self.output_file = output_file
        self.extractor = None
        
    async def scrape(self, urls: List[str]) -> Dict[str, Any]:
        """
        Scrape data from a list of Instagram URLs
        
        Args:
            urls: List of Instagram URLs to scrape
            
        Returns:
            Dictionary containing:
            - success: Boolean indicating overall success
            - data: List of scraped data objects
            - summary: Summary statistics
            - errors: List of any errors encountered
            - output_file: Path to saved file (if output_file was specified)
        """
        if not urls:
            return {
                'success': False,
                'error': 'No URLs provided',
                'data': [],
                'summary': {},
                'errors': []
            }
        
        print(f"🚀 Starting Instagram scraper...")
        print(f"   URLs to process: {len(urls)}")
        print(f"   Anti-detection: {'✅ Enabled' if self.enable_anti_detection else '❌ Disabled'}")
        print(f"   Mobile mode: {'✅ Enabled' if self.is_mobile else '❌ Disabled'}")
        print(f"   Headless mode: {'✅ Enabled' if self.headless else '❌ Disabled'}")
        
        start_time = time.time()
        all_extracted_data = []
        errors = []
        
        try:
            # Initialize the extractor
            self.extractor = AdvancedGraphQLExtractor(
                headless=self.headless,
                enable_anti_detection=self.enable_anti_detection,
                is_mobile=self.is_mobile
            )
            
            # Start the extractor
            print(f"\n🔧 Initializing extractor...")
            await self.extractor.start()
            print(f"✅ Extractor initialized successfully")
            
            # Get initial stealth report
            if self.enable_anti_detection:
                print(f"\n📊 Anti-detection status:")
                stealth_report = await self.extractor.get_stealth_report()
                print(f"   - User Agent: {stealth_report.get('fingerprint_evasion', {}).get('user_agent', 'N/A')[:50]}...")
                print(f"   - Platform: {stealth_report.get('fingerprint_evasion', {}).get('platform', 'N/A')}")
                print(f"   - Screen Resolution: {stealth_report.get('fingerprint_evasion', {}).get('screen_resolution', 'N/A')}")
                print(f"   - Timezone: {stealth_report.get('fingerprint_evasion', {}).get('timezone', 'N/A')}")
            
            # Process each URL
            print(f"\n🔍 Processing URLs...")
            for i, url in enumerate(urls, 1):
                print(f"\n[{i}/{len(urls)}] Processing: {url}")
                
                try:
                    # Extract data from the URL
                    extracted_data = await self.extractor.extract_graphql_data(url)
                    
                    if extracted_data.get('error'):
                        error_msg = f"Failed to extract data from {url}: {extracted_data['error']}"
                        print(f"❌ {error_msg}")
                        errors.append({
                            'url': url,
                            'error': extracted_data['error'],
                            'index': i
                        })
                        continue
                    
                    # Determine content type and create clean entry
                    content_type = self._determine_content_type_from_url(url, extracted_data)
                    
                    clean_entry = {
                        "url": url,
                        "content_type": content_type
                    }
                    
                    # Add data based on content type
                    if content_type == "profile":
                        user_data = extracted_data.get('user_data', {})
                        clean_entry.update({
                            "full_name": user_data.get('full_name'),
                            "username": user_data.get('username'),
                            "followers_count": self._format_count(user_data.get('followers_count')),
                            "following_count": self._format_count(user_data.get('following_count')),
                            "biography": user_data.get('biography', ''),
                            "bio_links": user_data.get('bio_links', []),
                            "is_private": user_data.get('is_private', False),
                            "is_verified": user_data.get('is_verified', False),
                            "is_business_account": user_data.get('is_business_account', False),
                            "is_professional_account": user_data.get('is_professional_account', True),
                            "business_email": user_data.get('business_email'),
                            "business_phone_number": user_data.get('business_phone_number'),
                            "business_category_name": user_data.get('business_category_name')
                        })
                        
                    elif content_type in ["article", "video"]:
                        meta_data = extracted_data.get('meta_data', {})
                        script_data = extracted_data.get('script_data', {})
                        
                        clean_entry.update({
                            "likes_count": self._format_count(meta_data.get('likes_count') or script_data.get('likes')),
                            "comments_count": self._format_count(meta_data.get('comments_count') or script_data.get('comments')),
                            "username": (meta_data.get('username') or 
                                       meta_data.get('username_from_title') or
                                       script_data.get('username')),
                            "post_date": meta_data.get('post_date'),
                            "caption": (meta_data.get('caption') or script_data.get('caption'))
                        })
                    
                    # Always include business fields, even if null
                    business_fields = ['business_email', 'business_phone_number', 'business_category_name']
                    for field in business_fields:
                        if field not in clean_entry:
                            clean_entry[field] = None
                        elif clean_entry[field] == '':
                            clean_entry[field] = None
                    
                    # Try to extract business email from biography if not found
                    if not clean_entry.get('business_email') and clean_entry.get('biography'):
                        import re
                        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', clean_entry['biography'])
                        if email_match:
                            clean_entry['business_email'] = email_match.group(0)
                    
                    # Remove None values for non-business fields
                    clean_entry = {k: v for k, v in clean_entry.items() if v is not None or k in business_fields}
                    all_extracted_data.append(clean_entry)
                    
                    print(f"✅ Successfully extracted {content_type} data")
                    
                except Exception as e:
                    error_msg = f"Error processing {url}: {str(e)}"
                    print(f"❌ {error_msg}")
                    errors.append({
                        'url': url,
                        'error': str(e),
                        'index': i
                    })
                    continue
            
            # Save to file if specified
            output_file_path = None
            if self.output_file:
                try:
                    with open(self.output_file, 'w', encoding='utf-8') as f:
                        json.dump(all_extracted_data, f, indent=2, ensure_ascii=False, default=str)
                    output_file_path = self.output_file
                    print(f"\n💾 Results saved to: {self.output_file}")
                except Exception as e:
                    print(f"❌ Error saving to file: {e}")
            
            # Calculate summary statistics
            total_time = time.time() - start_time
            content_types = {}
            for entry in all_extracted_data:
                content_type = entry.get('content_type', 'unknown')
                content_types[content_type] = content_types.get(content_type, 0) + 1
            
            summary = {
                'total_urls': len(urls),
                'successful_extractions': len(all_extracted_data),
                'failed_extractions': len(errors),
                'success_rate': len(all_extracted_data) / len(urls) * 100 if urls else 0,
                'total_time_seconds': total_time,
                'average_time_per_url': total_time / len(urls) if urls else 0,
                'content_type_breakdown': content_types
            }
            
            # Get final stealth report
            final_stealth_report = None
            if self.enable_anti_detection and self.extractor:
                try:
                    final_stealth_report = await self.extractor.get_stealth_report()
                except:
                    pass
            
            print(f"\n🎉 Scraping completed!")
            print(f"   - Total time: {total_time:.2f} seconds")
            print(f"   - Success rate: {summary['success_rate']:.1f}%")
            print(f"   - Successful extractions: {summary['successful_extractions']}")
            print(f"   - Failed extractions: {summary['failed_extractions']}")
            
            if content_types:
                print(f"   - Content types:")
                for content_type, count in content_types.items():
                    print(f"     • {content_type.title()}: {count}")
            
            return {
                'success': len(errors) == 0,
                'data': all_extracted_data,
                'summary': summary,
                'errors': errors,
                'output_file': output_file_path,
                'stealth_report': final_stealth_report
            }
            
        except Exception as e:
            error_msg = f"Critical error during scraping: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg,
                'data': all_extracted_data,
                'summary': {
                    'total_urls': len(urls),
                    'successful_extractions': len(all_extracted_data),
                    'failed_extractions': len(urls),
                    'success_rate': 0,
                    'total_time_seconds': time.time() - start_time
                },
                'errors': errors + [{'url': 'ALL', 'error': error_msg, 'index': 0}],
                'output_file': None
            }
        
        finally:
            # Clean up
            if self.extractor:
                try:
                    await self.extractor.stop()
                    print(f"✅ Extractor cleanup completed")
                except Exception as e:
                    print(f"⚠️ Warning during cleanup: {e}")
    
    def _determine_content_type_from_url(self, url: str, data: Dict[str, Any]) -> str:
        """Determine content type from URL and data"""
        if '/reel/' in url:
            return "video"
        elif '/p/' in url:
            # Check if it's actually a video post
            if (data.get('meta_data', {}).get('content_type') == 'video' or
                data.get('script_data', {}).get('is_video') or
                data.get('script_data', {}).get('video_url')):
                return "video"
            else:
                return "article"
        else:
            return "profile"
    
    def _format_count(self, count) -> str:
        """Format count numbers to readable format (e.g., 16000 -> 16K)"""
        if count is None:
            return None
        
        try:
            count = int(count)
            if count >= 1000000:
                return f"{count/1000000:.1f}M".replace('.0', '')
            elif count >= 1000:
                return f"{count/1000:.1f}K".replace('.0', '')
            else:
                return str(count)
        except (ValueError, TypeError):
            return str(count) if count else None


async def scrape_instagram_urls(urls: List[str], 
                              headless: bool = True,
                              enable_anti_detection: bool = True,
                              is_mobile: bool = False,
                              output_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to scrape Instagram URLs
    
    Args:
        urls: List of Instagram URLs to scrape
        headless: Run browser in headless mode (default: True)
        enable_anti_detection: Enable anti-detection features (default: True)
        is_mobile: Use mobile user agent and viewport (default: False)
        output_file: Optional file path to save results (default: None)
        
    Returns:
        Dictionary containing scraping results
    """
    scraper = InstagramScraper(
        headless=headless,
        enable_anti_detection=enable_anti_detection,
        is_mobile=is_mobile,
        output_file=output_file
    )
    return await scraper.scrape(urls)


async def main():
    """Main function for command-line usage"""
    print("Instagram Scraper - Main Entry Point")
    print("=" * 50)
    
    # Example URLs (you can modify these or get them from user input)
    example_urls = [
        "https://www.instagram.com/90svogue.__",
        "https://www.instagram.com/codehype_",
        "https://www.instagram.com/p/DMsercXMVeZ/",
        "https://www.instagram.com/reel/CSb6-Rap2Ip/"
    ]
    
    print("Example URLs:")
    for i, url in enumerate(example_urls, 1):
        print(f"  {i}. {url}")
    
    # Ask user if they want to use example URLs or input their own
    choice = input("\nUse example URLs? (y/n): ").strip().lower()
    
    if choice == 'y':
        urls = example_urls
    else:
        print("\nEnter Instagram URLs (one per line, press Enter twice when done):")
        urls = []
        while True:
            url = input().strip()
            if not url:
                break
            if 'instagram.com' in url:
                urls.append(url)
            else:
                print("⚠️  Please enter a valid Instagram URL")
        
        if not urls:
            print("No valid URLs provided. Using example URLs.")
            urls = example_urls
    
    # Ask for scraper options
    print("\nScraper Options:")
    headless = input("Run in headless mode? (y/n, default: y): ").strip().lower() != 'n'
    anti_detection = input("Enable anti-detection? (y/n, default: y): ").strip().lower() != 'n'
    mobile = input("Use mobile mode? (y/n, default: n): ").strip().lower() == 'y'
    save_file = input("Save results to file? (y/n, default: y): ").strip().lower() != 'n'
    
    output_file = None
    if save_file:
        output_file = input("Enter output filename (default: instagram_scraped_data.json): ").strip()
        if not output_file:
            output_file = "instagram_scraped_data.json"
    
    print(f"\n🚀 Starting scraping with {len(urls)} URLs...")
    
    # Run the scraper
    result = await scrape_instagram_urls(
        urls=urls,
        headless=headless,
        enable_anti_detection=anti_detection,
        is_mobile=mobile,
        output_file=output_file
    )
    
    # Display results
    print(f"\n📊 FINAL RESULTS:")
    print(f"   Success: {'✅' if result['success'] else '❌'}")
    print(f"   Data entries: {len(result['data'])}")
    print(f"   Errors: {len(result['errors'])}")
    
    if result['data']:
        print(f"\n📋 Extracted Data Preview:")
        for i, entry in enumerate(result['data'][:3], 1):  # Show first 3 entries
            content_type = entry.get('content_type', 'unknown')
            url = entry.get('url', 'unknown')
            if content_type == 'profile':
                username = entry.get('username', 'unknown')
                followers = entry.get('followers_count', 'unknown')
                print(f"   {i}. Profile: @{username} ({followers} followers)")
            elif content_type in ['article', 'video']:
                username = entry.get('username', 'unknown')
                likes = entry.get('likes_count', 'unknown')
                print(f"   {i}. {content_type.title()}: @{username} ({likes} likes)")
    
    if result['errors']:
        print(f"\n❌ Errors encountered:")
        for error in result['errors']:
            print(f"   - {error['url']}: {error['error']}")
    
    if result['output_file']:
        print(f"\n💾 Results saved to: {result['output_file']}")


if __name__ == "__main__":
    # Run the main function
    asyncio.run(main()) 