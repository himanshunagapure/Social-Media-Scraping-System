# Instagram Data Scraper

A sophisticated Instagram data extraction tool that uses browser automation with network request capture to extract GraphQL data from Instagram profiles, posts, and reels.

## 🚀 Features

- **Advanced Network Monitoring**: Captures GraphQL and API requests/responses in real-time
- **Multi-Content Support**: Extracts data from profiles, posts, and reels
- **Stealth Browser Automation**: Uses Playwright with anti-detection measures
- **Clean Data Output**: Structured JSON output with formatted data
- **Comprehensive Data Extraction**: User info, engagement metrics, business data, and more
- **Popup Handling**: Automatically handles Instagram login/signup popups
- **Error Handling**: Robust error handling and recovery mechanisms

## 📋 Prerequisites

- Python 3.8+
- Playwright browser automation
- Required Python packages (see Installation section)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd insta-scraper
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv insta-venv
   # On Windows
   insta-venv\Scripts\activate
   # On macOS/Linux
   source insta-venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install playwright beautifulsoup4 fake-useragent aiohttp
   ```

4. **Install Playwright browsers**:
   ```bash
   playwright install chromium
   ```

## 🏗️ Architecture

The project consists of two main components:

### 1. BrowserManager (`src/browser_manager.py`)
- **Purpose**: Handles browser automation with stealth configuration
- **Key Features**:
  - Anti-detection measures (webdriver masking, user agent rotation)
  - Instagram popup handling
  - Page navigation and content extraction
  - Screenshot capabilities for debugging

### 2. AdvancedGraphQLExtractor (`src/advanced_graphql_extractor.py`)
- **Purpose**: Extracts data using network request monitoring
- **Key Features**:
  - Real-time network request/response capture
  - GraphQL and API data extraction
  - Multiple data parsing methods (meta tags, scripts, API responses)
  - Clean data formatting and export

## 📖 Usage

### Basic Usage

```python
import asyncio
from src.advanced_graphql_extractor import AdvancedGraphQLExtractor

async def main():
    # Initialize extractor
    extractor = AdvancedGraphQLExtractor(headless=True)
    
    try:
        # Start the extractor
        await extractor.start()
        
        # Extract data from URLs
        urls = [
            "https://www.instagram.com/username/",  # Profile
            "https://www.instagram.com/p/post_id/", # Post
            "https://www.instagram.com/reel/reel_id/" # Reel
        ]
        
        # Extract and save clean data
        await extractor.extract_and_save_clean_data_from_urls(
            urls, 
            "instagram_final_output.json"
        )
        
    finally:
        await extractor.stop()

# Run the extraction
asyncio.run(main())
```

### Advanced Usage

```python
import asyncio
from src.advanced_graphql_extractor import AdvancedGraphQLExtractor

async def advanced_extraction():
    extractor = AdvancedGraphQLExtractor(headless=False)  # Show browser for debugging
    
    try:
        await extractor.start()
        
        # Extract profile data
        profile_data = await extractor.extract_user_profile_data("username")
        
        # Extract post data
        post_data = await extractor.extract_post_data("post_id")
        
        # Extract reel data
        reel_data = await extractor.extract_reel_data("reel_id")
        
        # Save detailed data
        await extractor.save_scraped_data_to_json(
            profile_data, post_data, reel_data, 
            "detailed_scraped_data.json"
        )
        
        # Save clean output
        await extractor.save_clean_final_output(
            profile_data, post_data, reel_data, 
            "clean_final_output.json"
        )
        
    finally:
        await extractor.stop()

asyncio.run(advanced_extraction())
```

## 📊 Data Structure

### Profile Data
```json
{
  "url": "https://www.instagram.com/username/",
  "content_type": "profile",
  "full_name": "User Full Name",
  "username": "username",
  "followers_count": "1.2M",
  "following_count": "500",
  "biography": "User bio text...",
  "bio_links": [...],
  "is_private": false,
  "is_verified": true,
  "is_business_account": true,
  "is_professional_account": true,
  "business_email": "contact@business.com",
  "business_phone_number": "+1234567890",
  "business_category_name": "Business Category"
}
```

### Post/Reel Data
```json
{
  "url": "https://www.instagram.com/p/post_id/",
  "content_type": "article",
  "likes_count": "1.5K",
  "comments_count": "234",
  "username": "username",
  "post_date": "January 15, 2024",
  "caption": "Post caption text..."
}
```

## 🔧 Configuration

### Browser Settings
- **Headless Mode**: Set `headless=True` for faster execution, `False` for debugging
- **User Agent**: Automatically rotated using `fake-useragent`
- **Viewport**: 1920x1080 resolution
- **Stealth Features**: WebDriver masking, plugin simulation, language settings

### Network Monitoring
- **Filtered Endpoints**: Captures GraphQL and API requests
- **Response Processing**: Handles JSON, compressed (zstd) responses
- **Error Handling**: Graceful handling of failed requests

## 🚨 Anti-Detection Features

1. **Browser Fingerprinting Protection**:
   - WebDriver property masking
   - Plugin array simulation
   - Language preferences
   - Random user agent rotation

2. **Human-like Behavior**:
   - Random delays between actions
   - Natural navigation patterns
   - Realistic viewport settings

3. **Request Headers**:
   - Standard browser headers
   - Accept-Language settings
   - DNT (Do Not Track) headers

## 📁 Output Files

### 1. Clean Final Output (`instagram_final_output.json`)
- Structured, clean data format
- Formatted counts (1.2K, 1.5M)
- Business information included
- Ready for analysis

### 2. Detailed Scraped Data (`scraped_data.json`)
- Complete extraction metadata
- Network analysis
- Raw API responses
- Success indicators
- Missing data analysis

## 🧪 Testing

### Run Example Usage
```bash
python example_clean_usage.py
```

### Test Browser Manager
```bash
python src/browser_manager.py
```

### Test Advanced Extractor
```bash
python src/advanced_graphql_extractor.py
```

## ⚠️ Important Notes

1. **Rate Limiting**: Instagram may rate-limit requests. Use delays between extractions.
2. **Authentication**: Some content may require login for access.
3. **Legal Compliance**: Ensure compliance with Instagram's Terms of Service.
4. **Data Usage**: Respect user privacy and data protection regulations.

## 🔍 Troubleshooting

### Common Issues

1. **Browser Launch Failures**:
   - Ensure Playwright is properly installed
   - Check system dependencies
   - Try running with `headless=False` for debugging

2. **Network Request Failures**:
   - Check internet connection
   - Verify URL format
   - Instagram may block automated access

3. **Data Extraction Issues**:
   - Instagram layout changes may affect selectors
   - Popup handling may need updates
   - Check for rate limiting

### Debug Mode
```python
# Enable debug mode for troubleshooting
extractor = AdvancedGraphQLExtractor(headless=False)
# Check screenshots in project directory
```

## 📈 Performance Tips

1. **Batch Processing**: Process multiple URLs in sequence
2. **Headless Mode**: Use `headless=True` for faster execution
3. **Resource Management**: Always call `extractor.stop()` to clean up
4. **Error Recovery**: Implement retry logic for failed extractions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational purposes. Please ensure compliance with Instagram's Terms of Service and applicable laws.

## 🔗 Dependencies

- `playwright`: Browser automation
- `beautifulsoup4`: HTML parsing
- `fake-useragent`: User agent rotation
- `aiohttp`: Async HTTP client
- `asyncio`: Async programming support

---

**Disclaimer**: This tool is for educational and research purposes. Users are responsible for complying with Instagram's Terms of Service and applicable laws regarding web scraping and data collection. 