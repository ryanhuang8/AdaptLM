import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def run_vellum_scraper(output_file: str):
    """
    Scrape the Vellum LLM leaderboard and extract task categories with top 5 models
    Returns: Dictionary with task categories and their top 5 models
    """
    print("🔄 Scraping Vellum LLM Leaderboard...")
    
    url = "https://www.vellum.ai/llm-leaderboard"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Fetch the page
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract task categories and models using CSS classes
        task_data = best_models(soup)
        task_data["task_categories"]["Best in Empathy and Emotional Intelligence"] = ["Hume"]
        task_data["task_categories"]["Fastest Inference LLM"] = ["Groq"]
        
        # Save to JSON file
        with open(output_file, 'w') as f:
            json.dump(task_data, f, indent=2)
        
        print(f"✅ Successfully scraped and saved to {output_file}")
        print(f"📊 Found {len(task_data['task_categories'])} task categories")

        return task_data
        
    except Exception as e:
        print(f"❌ Error scraping leaderboard: {str(e)}")
        return None

def best_models(html_content):
    """
    Extract task categories and their top 5 models using CSS classes
    """
    task_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "task_categories": {}
    }
    
    # Find all leaderboard sections using the graph_wrap class
    leaderboard_sections = html_content.find_all(class_="graph_wrap")
    
    for section in leaderboard_sections:
        # Find best models per task category
        section_name = section.find(class_="model_header").get_text().strip() or ""
        models = best_models_per_task_category(section)
        if section_name and models:
            task_data["task_categories"][section_name] = models

    return task_data

def best_models_per_task_category(task_section):
    """
    Extract models and scores
    """
    models_html = task_section.find_all(class_="graph_collection-item")
    models = [{
        "name": model.find(class_="graph_block-text").get_text().strip(),
        "score": model.find(class_="height_percentage").get_text().strip(),
    } for model in models_html]
    
    # Sort by score and return top 5
    sorted_models = sorted(models, key=lambda x: float(x["score"].replace("%", "")), reverse=True)
    model_names = [model["name"] for model in sorted_models]
    return model_names