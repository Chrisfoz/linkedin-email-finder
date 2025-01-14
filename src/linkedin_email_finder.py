import os
import pandas as pd
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from typing import Dict, List
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LinkedInEmailFinder:
    def __init__(self):
        # Initialize the web search agent
        self.search_agent = Agent(
            name="Email Search Agent",
            model=OpenAIChat(id="gpt-4o"),
            tools=[DuckDuckGo()],
            instructions=[
                "Search for professional email addresses from publicly available sources",
                "Focus on company websites and professional directories",
                "Always include sources in responses",
                "Respect privacy and only return publicly available business email addresses",
            ],
            show_tool_calls=True,
            markdown=True,
        )
        
        # Load configuration from environment variables
        self.batch_size = int(os.getenv('BATCH_SIZE', '5'))
        self.delay = int(os.getenv('DELAY_BETWEEN_REQUESTS', '2'))
        self.output_file = os.getenv('OUTPUT_FILE', 'email_search_results.csv')
        
    def load_connections(self, file_path: str) -> pd.DataFrame:
        """Load and preprocess LinkedIn connections data"""
        try:
            df = pd.read_csv(file_path)
            # Clean column names and remove unnamed columns
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            return df
        except Exception as e:
            print(f"Error loading connections file: {e}")
            raise
    
    def search_email(self, name: str, company: str = None, position: str = None) -> Dict:
        """Search for email address using the web agent"""
        try:
            query = f"Find business email for {name}"
            if company:
                query += f" who works at {company}"
            if position:
                query += f" as {position}"
                
            response = self.search_agent.chat(query)
            return {
                'name': name,
                'company': company,
                'position': position,
                'query': query,
                'response': response,
                'source': self._extract_source(response),
                'email': self._extract_email(response)
            }
        except Exception as e:
            print(f"Error searching email for {name}: {e}")
            return {
                'name': name,
                'company': company,
                'position': position,
                'query': query,
                'response': str(e),
                'source': '',
                'email': ''
            }
    
    def _extract_source(self, response: str) -> str:
        """Extract source URLs from the agent response"""
        return response.split('Source:')[-1].strip() if 'Source:' in response else ''
    
    def _extract_email(self, response: str) -> str:
        """Extract email address from the response"""
        import re
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        emails = re.findall(email_pattern, response)
        return emails[0] if emails else ''
    
    def process_connections(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process connections in batches to find missing emails"""
        results = []
        
        # Filter connections without emails
        missing_emails = df[df['Email'].isna() | (df['Email'] == '')]
        total = len(missing_emails)
        
        print(f"\nProcessing {total} connections missing emails...")
        
        for i in range(0, total, self.batch_size):
            batch = missing_emails.iloc[i:i+self.batch_size]
            
            for _, row in batch.iterrows():
                result = self.search_email(
                    name=row['Full Name'],
                    company=row.get('Company', None),
                    position=row.get('Position', None)
                )
                results.append(result)
                time.sleep(self.delay)  # Rate limiting
                
            processed = min(i + self.batch_size, total)
            print(f"Progress: {processed}/{total} connections processed")
        
        # Create results DataFrame
        results_df = pd.DataFrame(results)
        return results_df
    
    def save_results(self, results_df: pd.DataFrame):
        """Save results to CSV file"""
        try:
            results_df.to_csv(self.output_file, index=False)
            print(f"\nResults saved to {self.output_file}")
        except Exception as e:
            print(f"Error saving results: {e}")

def main():
    try:
        # Initialize the email finder
        finder = LinkedInEmailFinder()
        
        # Load connections
        print("Loading LinkedIn connections...")
        connections_df = finder.load_connections('Connections.csv')
        
        # Process connections and find emails
        results_df = finder.process_connections(connections_df)
        
        # Save results
        finder.save_results(results_df)
        
        # Print summary
        print("\nEmail Search Summary:")
        print(f"Total connections processed: {len(results_df)}")
        print(f"Emails found: {len(results_df[results_df['email'].str.len() > 0])}")
        print(f"Successful searches with sources: {len(results_df[results_df['source'].str.len() > 0])}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()