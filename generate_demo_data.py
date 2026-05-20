"""
Demo Data Generator
Creates realistic sample data for testing when you don't have real exports yet
"""
import json
import os
from parsers.utils import save_json

def generate_demo_ai_data():
    """Generate demo AI conversation data"""
    demo_files = [
        {"file": "betterme ai interviewer", "anxiety_markers": ["job_hunting", "ai_building"]},
        {"file": "Resume", "anxiety_markers": ["job_hunting"]},
        {"file": "Docker MLOps", "anxiety_markers": ["mlops_devops"]},
        {"file": "portfolio", "anxiety_markers": ["job_hunting", "finance_quant"]},
        {"file": "Generative AI with LangChain", "anxiety_markers": ["ai_building"]},
        {"file": "advances in financial machine learning", "anxiety_markers": ["finance_quant", "skill_gaps"]},
        {"file": "voice agent", "anxiety_markers": ["ai_building"]},
        {"file": "backtest", "anxiety_markers": ["finance_quant"]},
        {"file": "learning path", "anxiety_markers": ["skill_gaps"]},
        {"file": "test interview", "anxiety_markers": ["job_hunting"]},
    ]

    demo_activity = [
        {"prompt": "Build an AI Interviewer with RAG", "anxiety_markers": ["job_hunting", "ai_building"]},
        {"prompt": "How to deploy Docker containers", "anxiety_markers": ["mlops_devops", "skill_gaps"]},
        {"prompt": "Resume tips for data science roles", "anxiety_markers": ["job_hunting"]},
        {"prompt": "Explain trading algorithms", "anxiety_markers": ["finance_quant"]},
    ]

    marker_counts = {
        "job_hunting": 20,
        "ai_building": 12,
        "finance_quant": 10,
        "mlops_devops": 8,
        "skill_gaps": 5
    }

    result = {
        "chatgpt_topics": [],
        "claude_topics": [],
        "gemini_files": demo_files,
        "gemini_activity": demo_activity,
        "behavioral_inference": {
            "anxiety_markers_detected": marker_counts,
            "top_signal": "job_hunting",
            "conclusion": "Algorithm inferred job-hunting anxiety without explicit declaration"
        }
    }

    save_json(result, "output/ai_data.json")
    print("✅ Demo AI data generated")

def main():
    print("🎭 Generating demo data for testing...")
    print("⚠️  This is SAMPLE data - replace with real exports when available")
    print()

    os.makedirs("output", exist_ok=True)
    generate_demo_ai_data()

    print()
    print("✅ Demo data ready!")
    print()
    print("You can now run:")
    print("  python parsers/feature_engineering.py")
    print("  python parsers/gemini_embeddings.py")
    print()
    print("When you get your real ChatGPT/Gemini exports:")
    print("  1. Place them in data/chatgpt/ and data/takeout/")
    print("  2. Run: python parsers/ai_conversations_parser.py")

if __name__ == "__main__":
    main()
