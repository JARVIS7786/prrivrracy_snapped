"""
Demo Data Generator
Generates realistic fake data for "Rahul, 23, Mumbai"
so people can try the tool without uploading their own data.
"""

import sys
import json
from pathlib import Path

# Windows encoding fix
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def generate_demo_instagram_data():
    """Generate realistic Instagram data for demo user"""
    return {
        "advertiser_count": 3847,
        "advertisers_sample": [
            "Swiggy",
            "Zomato",
            "Flipkart",
            "Amazon India",
            "Myntra",
            "CRED",
            "PhonePe",
            "Paytm",
            "Dream11",
            "MPL",
            "Unacademy",
            "BYJU'S",
            "upGrad",
            "Scaler",
            "Naukri.com",
            "LinkedIn India",
            "BookMyShow",
            "Netflix India",
            "Amazon Prime Video",
            "Disney+ Hotstar",
            "Spotify India",
            "Boat",
            "OnePlus India",
            "Xiaomi India",
            "Samsung India",
            "Jio",
            "Airtel",
            "Ola",
            "Uber India",
            "MakeMyTrip"
        ],
        "industries": {
            "Tech & Apps": 287,
            "Fashion & Beauty": 156,
            "Finance": 98,
            "Food": 234,
            "Travel": 67,
            "Education": 189,
            "Entertainment": 145,
            "Health": 78,
            "Other": 2593
        },
        "ad_categories": [
            "Engaged shoppers",
            "Facebook access (mobile): all mobile devices",
            "Mobile network or device users",
            "Potential mobile network or device change",
            "Wi-Fi Usage",
            "Relationship status: single",
            "Education level: Associate or Bachelors Degree",
            "Age: 18-24"
        ],
        "locations": [
            "Mumbai, Maharashtra",
            "Andheri, Mumbai",
            "Bandra, Mumbai",
            "Pune, Maharashtra",
            "Thane, Maharashtra",
            "Navi Mumbai, Maharashtra",
            "Maharashtra"
        ],
        "recent_searches": [
            {"query": "#viratkohli", "time": "May 18, 2026 9:45 pm"},
            {"query": "#ipl2026", "time": "May 18, 2026 9:30 pm"},
            {"query": "#mumbaiindians", "time": "May 18, 2026 8:15 pm"},
            {"query": "#python", "time": "May 17, 2026 2:30 pm"},
            {"query": "#machinelearning", "time": "May 17, 2026 2:15 pm"},
            {"query": "#coding", "time": "May 17, 2026 11:00 am"},
            {"query": "#deepikapadukone", "time": "May 16, 2026 10:30 pm"},
            {"query": "#bollywood", "time": "May 16, 2026 10:15 pm"},
            {"query": "#ranveersingh", "time": "May 16, 2026 10:00 pm"},
            {"query": "#jobsearch", "time": "May 15, 2026 3:45 pm"}
        ]
    }

def generate_demo_google_data():
    """Generate realistic Google data for demo user"""
    return {
        "google_searches": [
            {"value": "python interview questions", "time": "May 18, 2026"},
            {"value": "machine learning roadmap 2026", "time": "May 18, 2026"},
            {"value": "best data science courses india", "time": "May 17, 2026"},
            {"value": "mumbai indians vs csk highlights", "time": "May 17, 2026"},
            {"value": "ipl 2026 points table", "time": "May 17, 2026"},
            {"value": "react vs angular 2026", "time": "May 16, 2026"},
            {"value": "docker tutorial for beginners", "time": "May 16, 2026"},
            {"value": "best cafes in bandra mumbai", "time": "May 15, 2026"},
            {"value": "fighter movie review", "time": "May 15, 2026"},
            {"value": "salary negotiation tips india", "time": "May 14, 2026"}
        ],
        "youtube_watched": [
            {"value": "Python Full Course for Beginners", "time": "May 18, 2026"},
            {"value": "Machine Learning Tutorial - Krish Naik", "time": "May 18, 2026"},
            {"value": "MI vs CSK Full Match Highlights IPL 2026", "time": "May 17, 2026"},
            {"value": "Rohit Sharma Best Innings Compilation", "time": "May 17, 2026"},
            {"value": "Docker in 100 Seconds", "time": "May 16, 2026"},
            {"value": "System Design Interview Questions", "time": "May 16, 2026"},
            {"value": "Fighter - Official Trailer | Hrithik Roshan", "time": "May 15, 2026"},
            {"value": "Mumbai Food Tour - Street Food", "time": "May 15, 2026"},
            {"value": "How to Crack FAANG Interviews", "time": "May 14, 2026"},
            {"value": "Day in Life of Software Engineer Mumbai", "time": "May 14, 2026"},
            {"value": "Karan Aujla - Tauba Tauba", "time": "May 13, 2026"},
            {"value": "Stand Up Comedy - Zakir Khan", "time": "May 13, 2026"},
            {"value": "React Tutorial for Beginners", "time": "May 12, 2026"},
            {"value": "LeetCode Daily Challenge Solution", "time": "May 12, 2026"},
            {"value": "Mumbai Vlog - Weekend Vibes", "time": "May 11, 2026"}
        ],
        "maps_locations": [
            {"value": "IIT Bombay, Powai, Mumbai", "time": "May 18, 2026"},
            {"value": "Starbucks, Bandra West, Mumbai", "time": "May 17, 2026"},
            {"value": "Phoenix Marketcity, Kurla, Mumbai", "time": "May 16, 2026"},
            {"value": "Worli Sea Face, Mumbai", "time": "May 15, 2026"}
        ],
        "youtube_searches": [
            {"value": "python projects for resume", "time": "May 18, 2026"},
            {"value": "ipl 2026 highlights", "time": "May 17, 2026"},
            {"value": "bollywood songs 2026", "time": "May 15, 2026"}
        ]
    }

def generate_demo_ai_data():
    """Generate realistic AI conversation data for demo user"""
    return {
        "chatgpt_topics": [],
        "claude_topics": [],
        "gemini_files": [
            {"file": "resume_builder_project", "anxiety_markers": ["job_hunting"]},
            {"file": "interview_prep_notes", "anxiety_markers": ["job_hunting"]},
            {"file": "machine_learning_portfolio", "anxiety_markers": ["job_hunting", "skill_gaps"]},
            {"file": "docker_kubernetes_notes", "anxiety_markers": ["mlops_devops"]},
            {"file": "system_design_prep", "anxiety_markers": ["job_hunting"]},
            {"file": "leetcode_solutions", "anxiety_markers": ["job_hunting", "skill_gaps"]},
            {"file": "react_project_ideas", "anxiety_markers": ["ai_building"]},
            {"file": "data_science_roadmap", "anxiety_markers": ["skill_gaps"]},
            {"file": "salary_negotiation_tips", "anxiety_markers": ["job_hunting"]},
            {"file": "startup_ideas_2026", "anxiety_markers": ["ai_building"]}
        ],
        "gemini_activity": [
            {"prompt": "resume_builder_project.py", "anxiety_markers": ["job_hunting"]},
            {"prompt": "How to prepare for FAANG interviews", "anxiety_markers": ["job_hunting"]},
            {"prompt": "Best machine learning projects for portfolio", "anxiety_markers": ["job_hunting"]},
            {"prompt": "Docker vs Kubernetes comparison", "anxiety_markers": ["mlops_devops"]},
            {"prompt": "System design interview questions", "anxiety_markers": ["job_hunting"]},
            {"prompt": "LeetCode problem solving strategies", "anxiety_markers": ["skill_gaps"]}
        ],
        "behavioral_inference": {
            "anxiety_markers_detected": {
                "job_hunting": 15,
                "skill_gaps": 8,
                "mlops_devops": 5,
                "ai_building": 4,
                "finance_quant": 0
            },
            "top_signal": "job_hunting",
            "conclusion": "Algorithm inferred job-hunting anxiety without explicit declaration"
        }
    }

def generate_demo_user_features():
    """Generate realistic user feature matrix for demo user"""
    return {
        "user_demographics": {
            "is_single": True,
            "is_educated": True,
            "is_engaged_shopper": True,
            "potential_device_change": False
        },
        "affinity_scores": {
            "cricket_score": 9,
            "coding_score": 12,
            "bollywood_score": 7,
            "spiritual_score": 1,
            "local_mumbai_score": 8,
            "shopping_score": 3,
            "entertainment_score": 8
        },
        "advertiser_pressure": 3847,
        "industry_breakdown": {},
        "locations_tracked": [
            "Mumbai, Maharashtra",
            "Andheri, Mumbai",
            "Bandra, Mumbai",
            "Pune, Maharashtra",
            "Thane, Maharashtra"
        ],
        "maps_visited": [
            "IIT Bombay, Powai, Mumbai",
            "Starbucks, Bandra West, Mumbai",
            "Phoenix Marketcity, Kurla, Mumbai"
        ],
        "total_data_points_analyzed": 87,
        "affinity_scores_normalized": {
            "cricket_score": 0.75,
            "coding_score": 1.0,
            "bollywood_score": 0.583,
            "spiritual_score": 0.083,
            "local_mumbai_score": 0.667,
            "shopping_score": 0.25,
            "entertainment_score": 0.667
        }
    }

def generate_demo_rtb_results():
    """Generate realistic RTB auction results for demo user"""
    return {
        "top_bidders": [
            {"advertiser": "Naukri.com", "industry": "Education", "final_bid": 3133.02, "base_cpm": 1205, "demographic_multiplier": 2.18, "affinity_multiplier": 1.19},
            {"advertiser": "LinkedIn India", "industry": "Education", "final_bid": 3133.02, "base_cpm": 1205, "demographic_multiplier": 2.18, "affinity_multiplier": 1.19},
            {"advertiser": "Flipkart", "industry": "Tech & Apps", "final_bid": 2567.89, "base_cpm": 987, "demographic_multiplier": 2.18, "affinity_multiplier": 1.19},
            {"advertiser": "CRED", "industry": "Finance", "final_bid": 2279.45, "base_cpm": 876, "demographic_multiplier": 2.18, "affinity_multiplier": 1.19},
            {"advertiser": "Dream11", "industry": "Entertainment", "final_bid": 1903.56, "base_cpm": 654, "demographic_multiplier": 2.18, "affinity_multiplier": 1.33}
        ],
        "winner": {
            "advertiser": "Naukri.com",
            "industry": "Education",
            "final_bid": 3133.02,
            "base_cpm": 1205,
            "demographic_multiplier": 2.18,
            "affinity_multiplier": 1.19
        },
        "second_price": 3133.02,
        "user_demographics": {
            "is_single": True,
            "is_educated": True,
            "is_engaged_shopper": True,
            "potential_device_change": False
        },
        "affinity_scores": {
            "cricket_score": 0.75,
            "coding_score": 1.0,
            "bollywood_score": 0.583,
            "spiritual_score": 0.083,
            "local_mumbai_score": 0.667,
            "shopping_score": 0.25,
            "entertainment_score": 0.667
        },
        "total_advertisers": 3847,
        "sessions_per_day": 8,
        "ads_per_session": 12,
        "days_per_year": 365,
        "avg_winning_bid": 0.002944,
        "annual_revenue_generated": 103219.20,
        "instagram_keeps": 30965.76,
        "advertiser_spend": 72253.44,
        "you_were_paid": 0,
        "your_data_price_tag": 103219.20
    }

def main():
    """Generate all demo data files"""
    print("\n" + "="*60)
    print("DEMO DATA GENERATOR")
    print("="*60)
    print("Generating realistic demo data for 'Rahul, 23, Mumbai'...")
    print("="*60 + "\n")

    output_dir = Path("../output")
    output_dir.mkdir(exist_ok=True)

    # Generate each dataset
    datasets = {
        "demo_instagram_data.json": generate_demo_instagram_data(),
        "demo_google_data.json": generate_demo_google_data(),
        "demo_ai_data.json": generate_demo_ai_data(),
        "demo_user_feature_matrix.json": generate_demo_user_features(),
        "demo_rtb_results.json": generate_demo_rtb_results()
    }

    for filename, data in datasets.items():
        filepath = output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ Generated: {filename}")

    print("\n" + "="*60)
    print("DEMO DATA GENERATION COMPLETE")
    print("="*60)
    print("\nDemo Profile:")
    print("  Name: Rahul")
    print("  Age: 23")
    print("  Location: Mumbai, Maharashtra")
    print("  Status: Single, Educated, Job Hunting")
    print("  Interests: Cricket, Coding, Bollywood")
    print("  Data Value: ₹103,219 per year")
    print("  Advertisers Tracking: 3,847 companies")
    print("\nFiles saved to output/ directory")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
