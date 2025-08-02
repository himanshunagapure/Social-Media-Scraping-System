"""
Example usage of the clean Instagram data extraction functionality

This file demonstrates how to use the AdvancedGraphQLExtractor to extract
clean, structured data from Instagram URLs and save it in the requested format.
"""

import asyncio
from src.advanced_graphql_extractor import AdvancedGraphQLExtractor


async def extract_clean_data():
    """Extract clean data from Instagram URLs"""
    
    # List of Instagram URLs to extract data from
    urls = [
        "https://www.instagram.com/shein_ind/",  # Profile
        "https://www.instagram.com/90svogue.__",
        "https://www.instagram.com/codehype_",
        "https://www.instagram.com/p/DMsercXMVeZ/",    # Post
        "https://www.instagram.com/reel/CSb6-Rap2Ip/"  # Reel
    ]
    
    # Initialize the extractor
    extractor = AdvancedGraphQLExtractor(headless=True)
    
    try:
        # Start the extractor
        await extractor.start()
        print("✅ Extractor started successfully")
        
        # Extract and save clean data
        await extractor.extract_and_save_clean_data_from_urls(urls, "instagram_final_output.json")
        
        print("\n🎉 Extraction completed!")
        print("📁 Check 'instagram_final_output.json' for the clean data structure.")
        
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        await extractor.stop()
        print("✅ Extractor cleanup completed")


async def extract_single_url():
    """Extract data from a single URL and save in clean format"""
    
    # Single URL to extract
    url = "https://www.instagram.com/shein_ind"
    
    extractor = AdvancedGraphQLExtractor(headless=True)
    
    try:
        await extractor.start()
        print("✅ Extractor started successfully")
        
        # Extract data from the URL
        extracted_data = await extractor.extract_graphql_data(url)
        
        if extracted_data.get('error'):
            print(f"❌ Failed to extract data: {extracted_data['error']}")
            return
        
        # Create a dummy list with single item for the save method
        dummy_post_data = {'error': 'No post data'}
        dummy_reel_data = {'error': 'No reel data'}
        
        # Save in clean format
        await extractor.save_clean_final_output(extracted_data, dummy_post_data, dummy_reel_data, "single_url_output.json")
        
        print("\n🎉 Single URL extraction completed!")
        print("📁 Check 'single_url_output.json' for the clean data structure.")
        
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await extractor.stop()
        print("✅ Extractor cleanup completed")


if __name__ == "__main__":
    print("Instagram Clean Data Extraction Examples")
    print("=" * 50)
    
    # Choose which example to run
    choice = input("Choose an example (1 for multiple URLs, 2 for single URL): ").strip()
    
    if choice == "1":
        print("\nRunning multiple URLs example...")
        asyncio.run(extract_clean_data())
    elif choice == "2":
        print("\nRunning single URL example...")
        asyncio.run(extract_single_url())
    else:
        print("Invalid choice. Running multiple URLs example by default...")
        asyncio.run(extract_clean_data()) 