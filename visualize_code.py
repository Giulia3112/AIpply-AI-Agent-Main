#!/usr/bin/env python3
"""
Code Visualization Tool for AIpply API
Analyzes the codebase structure and creates visual representations
"""

import ast
import os
from pathlib import Path
from typing import Dict, List, Set

def analyze_file(file_path: str) -> Dict:
    """Analyze a Python file and extract its structure"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        
        analysis = {
            'file': file_path,
            'classes': [],
            'functions': [],
            'imports': [],
            'from_imports': []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                analysis['functions'].append({
                    'name': node.name,
                    'args': [arg.arg for arg in node.args.args],
                    'line': node.lineno
                })
            elif isinstance(node, ast.ClassDef):
                analysis['classes'].append({
                    'name': node.name,
                    'line': node.lineno
                })
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    analysis['imports'].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                names = [alias.name for alias in node.names]
                analysis['from_imports'].append(f"{module}: {', '.join(names)}")
        
        return analysis
    except Exception as e:
        return {'file': file_path, 'error': str(e)}

def create_architecture_diagram():
    """Create a text-based architecture diagram"""
    print("\n" + "="*60)
    print("AIPPLY API ARCHITECTURE DIAGRAM")
    print("="*60)
    
    print("\nPROJECT STRUCTURE:")
    print("+-- main.py (FastAPI Application)")
    print("+-- startup_opps_api/")
    print("|   +-- models/")
    print("|   |   +-- opportunity.py (Pydantic Model)")
    print("|   +-- services/")
    print("|   |   +-- run_scraper.py (Scraping Service)")
    print("|   +-- scraper/")
    print("|       +-- scrapy_spider.py (Web Scraper)")
    print("|       +-- parser.py (Data Parser)")
    print("+-- frontend/ (HTML/CSS/JS)")

def create_api_flow_diagram():
    """Create API flow diagram"""
    print("\n" + "="*60)
    print("API REQUEST FLOW")
    print("="*60)
    
    print("\n1. Client Request -> /search endpoint")
    print("   +-- Query Parameters: keyword, region, type")
    print("   +-- FastAPI validation")
    print("\n2. Service Layer -> scrape_opportunities()")
    print("   +-- Initialize Scrapy CrawlerProcess")
    print("   +-- Configure StartupOpportunitiesSpider")
    print("   +-- Start crawling process")
    print("\n3. Scraping Layer -> StartupOpportunitiesSpider")
    print("   +-- Target URLs:")
    print("   |   +-- f6s.com/startups")
    print("   |   +-- opportunitydesk.org")
    print("   +-- Parse opportunity cards")
    print("   +-- Extract structured data")
    print("\n4. Data Processing -> Opportunity Model")
    print("   +-- Pydantic validation")
    print("   +-- Type conversion")
    print("   +-- JSON serialization")
    print("\n5. Response -> JSON array of opportunities")

def create_data_model_diagram():
    """Create data model diagram"""
    print("\n" + "="*60)
    print("DATA MODEL STRUCTURE")
    print("="*60)
    
    print("\nOpportunity Model:")
    print("+-- title: str (required)")
    print("+-- organization: str (required)")
    print("+-- type: Optional[str]")
    print("+-- eligibility: Optional[str]")
    print("+-- deadline: Optional[str]")
    print("+-- url: str (required)")

def analyze_codebase():
    """Analyze the entire codebase"""
    print("\n" + "="*60)
    print("CODEBASE ANALYSIS")
    print("="*60)
    
    files_to_analyze = [
        'main.py',
        'startup_opps_api/models/opportunity.py',
        'startup_opps_api/services/run_scraper.py',
        'startup_opps_api/scraper/scrapy_spider.py'
    ]
    
    for file_path in files_to_analyze:
        if os.path.exists(file_path):
            analysis = analyze_file(file_path)
            print(f"\nFILE: {file_path}")
            print("-" * 40)
            
            if 'error' in analysis:
                print(f"ERROR: {analysis['error']}")
                continue
                
            if analysis['classes']:
                print("Classes:")
                for cls in analysis['classes']:
                    print(f"   • {cls['name']} (line {cls['line']})")
            
            if analysis['functions']:
                print("Functions:")
                for func in analysis['functions']:
                    args = ', '.join(func['args']) if func['args'] else 'no args'
                    print(f"   • {func['name']}({args}) (line {func['line']})")
            
            if analysis['from_imports']:
                print("Imports:")
                for imp in analysis['from_imports']:
                    print(f"   • from {imp}")
        else:
            print(f"\nFile not found: {file_path}")

def create_dependency_graph():
    """Create dependency graph"""
    print("\n" + "="*60)
    print("DEPENDENCY GRAPH")
    print("="*60)
    
    print("\nmain.py")
    print("+-- FastAPI (external)")
    print("+-- startup_opps_api.models.opportunity")
    print("+-- startup_opps_api.services.run_scraper")
    print("\nstartup_opps_api/services/run_scraper.py")
    print("+-- scrapy (external)")
    print("+-- twisted (external)")
    print("+-- startup_opps_api.scraper.scrapy_spider")
    print("\nstartup_opps_api/scraper/scrapy_spider.py")
    print("+-- scrapy (external)")
    print("\nstartup_opps_api/models/opportunity.py")
    print("+-- pydantic (external)")

def main():
    """Main visualization function"""
    print("AIPPLY API CODE VISUALIZATION")
    print("=" * 60)
    
    create_architecture_diagram()
    create_api_flow_diagram()
    create_data_model_diagram()
    create_dependency_graph()
    analyze_codebase()
    
    print("\n" + "="*60)
    print("Visualization Complete!")
    print("="*60)

if __name__ == "__main__":
    main()
