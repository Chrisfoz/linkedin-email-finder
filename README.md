# LinkedIn Email Finder

A Phidata-based tool for finding missing email addresses from LinkedIn connections using AI agents and web searching.

## Overview

This tool helps you find missing email addresses for your LinkedIn connections by using AI agents to search publicly available business contact information. It uses the Phidata framework for agent orchestration and focuses on ethical data collection practices.

## Features

- Automated email discovery for LinkedIn connections
- Batch processing with rate limiting
- Source tracking for all found information
- Privacy-focused approach using only public business information
- Detailed reporting and CSV export

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Chrisfoz/linkedin-email-finder.git
cd linkedin-email-finder
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and settings
```

## Project Structure

```
linkedin-email-finder/
├── src/
│   └── linkedin_email_finder.py
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Usage

1. Export your LinkedIn connections to a CSV file
2. Place the CSV file in the project directory as 'Connections.csv'
3. Run the script:
```bash
python src/linkedin_email_finder.py
```

## Output

The script will generate an 'email_search_results.csv' file containing:
- Names and companies from your connections
- Found email addresses
- Sources for the information
- Search query used

## Privacy and Ethics

This tool is designed to:
- Only search for publicly available business contact information
- Respect rate limits and robots.txt
- Document sources for all found information
- Not attempt to access private or protected information

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.