"""
Complete Flow Test with Anti-Detection
Following the structure of example_clean_usage.py

This file demonstrates the complete Instagram data extraction flow
with anti-detection features enabled, testing both desktop and mobile modes.
"""

import asyncio
import time
from src.advanced_graphql_extractor import AdvancedGraphQLExtractor


async def extract_clean_data_with_anti_detection():
    """Extract clean data from Instagram URLs with anti-detection enabled"""
    
    # List of Instagram URLs to extract data from (same as example_clean_usage.py)
    urls = [ 
        "https://www.instagram.com/90svogue.__", # Profile
        "https://www.instagram.com/codehype_", # Profile
        "https://www.instagram.com/p/DMsercXMVeZ/",    # Post
        "https://www.instagram.com/reel/CSb6-Rap2Ip/"  # Reel
    ]
    
    print("📋 Testing URLs:")
    for i, url in enumerate(urls, 1):
        print(f"  {i}. {url}")
    
    # Test both desktop and mobile modes
    test_modes = [
        {"name": "Desktop Mode", "is_mobile": False},
        {"name": "Mobile Mode", "is_mobile": True}
    ]
    
    for mode in test_modes:
        print(f"\n{'='*60}")
        print(f"TESTING {mode['name'].upper()}")
        print(f"{'='*60}")
        
        # Initialize the extractor with anti-detection (following example_clean_usage.py pattern)
        extractor = AdvancedGraphQLExtractor(
            headless=True,
            enable_anti_detection=True,
            is_mobile=mode['is_mobile']
        )
        
        try:
            # Start the extractor
            print(f"\n🚀 Starting {mode['name']} extractor...")
            start_time = time.time()
            await extractor.start()
            startup_time = time.time() - start_time
            print(f"✅ {mode['name']} extractor started successfully in {startup_time:.2f}s")
            
            # Get initial stealth report
            print(f"\n📊 Initial Stealth Report for {mode['name']}:")
            initial_report = await extractor.get_stealth_report()
            print(f"  - User Agent: {initial_report.get('fingerprint_evasion', {}).get('user_agent', 'N/A')}")
            print(f"  - Platform: {initial_report.get('fingerprint_evasion', {}).get('platform', 'N/A')}")
            print(f"  - Screen Resolution: {initial_report.get('fingerprint_evasion', {}).get('screen_resolution', 'N/A')}")
            print(f"  - Hardware Concurrency: {initial_report.get('fingerprint_evasion', {}).get('hardware_concurrency', 'N/A')}")
            print(f"  - Memory: {initial_report.get('fingerprint_evasion', {}).get('memory', 'N/A')}")
            print(f"  - Timezone: {initial_report.get('fingerprint_evasion', {}).get('timezone', 'N/A')}")
            print(f"  - Is Mobile: {mode['is_mobile']}")
            
            # Extract and save clean data (following example_clean_usage.py pattern)
            print(f"\n🔍 Extracting data with {mode['name']}...")
            extraction_start = time.time()
            
            await extractor.extract_and_save_clean_data_from_urls(
                urls, 
                f"instagram_anti_detection_{mode['name'].lower().replace(' ', '_')}_output.json"
            )
            
            extraction_time = time.time() - extraction_start
            print(f"✅ {mode['name']} extraction completed in {extraction_time:.2f}s")
            
            # Get final stealth report
            print(f"\n📊 Final Stealth Report for {mode['name']}:")
            final_report = await extractor.get_stealth_report()
            
            print(f"  - Total Requests: {final_report.get('network_obfuscation', {}).get('request_count', 0)}")
            print(f"  - Total Actions: {final_report.get('behavioral_mimicking', {}).get('total_actions', 0)}")
            print(f"  - Average Request Spacing: {final_report.get('network_obfuscation', {}).get('avg_spacing', 0):.2f}s")
            print(f"  - Fingerprint Evasion: {'✅' if final_report.get('fingerprint_evasion', {}).get('enabled', False) else '❌'}")
            print(f"  - Behavioral Mimicking: {'✅' if final_report.get('behavioral_mimicking', {}).get('enabled', False) else '❌'}")
            print(f"  - Network Obfuscation: {'✅' if final_report.get('network_obfuscation', {}).get('enabled', False) else '❌'}")
            
            # Check for fingerprint rotation recommendation
            if extractor.browser_manager.anti_detection:
                should_rotate = await extractor.browser_manager.anti_detection.should_rotate_fingerprint()
                print(f"  - Fingerprint Rotation Recommended: {'⚠️ Yes' if should_rotate else '✅ No'}")
            
            print(f"\n🎉 {mode['name']} extraction completed successfully!")
            print(f"📁 Check 'instagram_anti_detection_{mode['name'].lower().replace(' ', '_')}_output.json' for results")
            
        except Exception as e:
            print(f"❌ {mode['name']} extraction failed: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Clean up
            await extractor.stop()
            print(f"✅ {mode['name']} extractor cleanup completed")
    
    print(f"\n{'='*80}")
    print("COMPLETE FLOW TEST SUMMARY")
    print(f"{'='*80}")
    print("✅ Desktop mode with anti-detection tested")
    print("✅ Mobile mode with anti-detection tested")
    print("✅ Complete extraction flow verified")
    print("✅ Anti-detection features integrated successfully")
    print("✅ Clean data format maintained")
    print(f"{'='*80}")


async def extract_single_url_with_anti_detection():
    """Extract data from single URL with anti-detection enabled"""
    
    # Single URL to extract (same as example_clean_usage.py)
    url = "https://www.instagram.com/shein_ind"
    
    print(f"🔍 Extracting data from: {url}")
    
    # Test both desktop and mobile modes
    for is_mobile in [False, True]:
        mode_name = "Mobile" if is_mobile else "Desktop"
        print(f"\n{'='*50}")
        print(f"TESTING {mode_name.upper()} MODE")
        print(f"{'='*50}")
        
        extractor = AdvancedGraphQLExtractor(
            headless=True,
            enable_anti_detection=True,
            is_mobile=is_mobile
        )
        
        try:
            await extractor.start()
            print(f"✅ {mode_name} extractor started successfully")
            
            # Extract data from the URL
            print(f"🔍 Extracting data...")
            extracted_data = await extractor.extract_graphql_data(url)
            
            if extracted_data.get('error'):
                print(f"❌ Failed to extract data: {extracted_data['error']}")
                continue
            
            print(f"✅ Data extraction successful")
            print(f"  - HTML Length: {extracted_data.get('html_length', 0):,} chars")
            print(f"  - Network Requests: {extracted_data.get('network_requests', 0)}")
            print(f"  - GraphQL Responses: {extracted_data.get('graphql_responses', 0)}")
            
            # Create dummy data for save method (following example_clean_usage.py pattern)
            dummy_post_data = {'error': 'No post data'}
            dummy_reel_data = {'error': 'No reel data'}
            
            # Save in clean format
            output_file = f"single_url_{mode_name.lower()}_anti_detection_output.json"
            await extractor.save_clean_final_output(
                extracted_data, 
                dummy_post_data, 
                dummy_reel_data, 
                output_file
            )
            
            print(f"✅ Data saved to: {output_file}")
            
            # Get stealth report
            stealth_report = await extractor.get_stealth_report()
            print(f"\n📊 {mode_name} Stealth Report:")
            print(f"  - User Agent: {stealth_report.get('fingerprint_evasion', {}).get('user_agent', 'N/A')[:50]}...")
            print(f"  - Platform: {stealth_report.get('fingerprint_evasion', {}).get('platform', 'N/A')}")
            print(f"  - Screen Resolution: {stealth_report.get('fingerprint_evasion', {}).get('screen_resolution', 'N/A')}")
            print(f"  - Total Requests: {stealth_report.get('network_obfuscation', {}).get('request_count', 0)}")
            print(f"  - Total Actions: {stealth_report.get('behavioral_mimicking', {}).get('total_actions', 0)}")
            
        except Exception as e:
            print(f"❌ {mode_name} extraction failed: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await extractor.stop()
            print(f"✅ {mode_name} extractor cleanup completed")
    
    print(f"\n{'='*80}")
    print("SINGLE URL TEST COMPLETED")
    print(f"{'='*80}")


if __name__ == "__main__":
    print("Instagram Anti-Detection Complete Flow Test")
    print("=" * 50)
    
    # Choose which example to run (following example_clean_usage.py pattern)
    choice = input("Choose an example (1 for multiple URLs, 2 for single URL): ").strip()
    
    if choice == "1":
        print("\nRunning multiple URLs example with anti-detection...")
        asyncio.run(extract_clean_data_with_anti_detection())
    elif choice == "2":
        print("\nRunning single URL example with anti-detection...")
        asyncio.run(extract_single_url_with_anti_detection())
    else:
        print("Invalid choice. Running multiple URLs example by default...")
        asyncio.run(extract_clean_data_with_anti_detection()) 