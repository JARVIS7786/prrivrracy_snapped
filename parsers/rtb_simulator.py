"""
Real-Time Bidding (RTB) Auction Simulator
Simulates the 100ms auction that happens every time you open Instagram.
Shows how advertisers bid on your attention based on demographics and behavior.
"""

import sys
import json
import time
from collections import defaultdict
from utils import load_json

# Windows encoding fix
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Indian market CPM rates (Rupees per 1000 impressions)
CPM_RATES = {
    "Education": 1205,
    "Tech & Apps": 987,
    "Finance": 876,
    "Entertainment": 654,
    "Fashion": 543,
    "Food": 432,
    "Travel": 398,
    "Health": 321,
    "Other": 180
}

# Demographic multipliers
DEMOGRAPHIC_MULTIPLIERS = {
    "is_single": 1.3,
    "is_educated": 1.2,
    "is_engaged_shopper": 1.4,
    "potential_device_change": 1.5
}

# Map advertisers to their industries
ADVERTISER_INDUSTRIES = {
    "LinkedIn APAC": "Education",
    "Final Round AI": "Education",
    "Scaler": "Education",
    "Naukri": "Education",
    "BookMyShow": "Entertainment",
    "Netflix India": "Entertainment",
    "Amazon Prime Video": "Entertainment",
    "Hotstar": "Entertainment",
    "Cashify": "Tech & Apps",
    "Replit": "Tech & Apps",
    "Tanishq": "Fashion",
    "The Souled Store": "Fashion",
    "Rare Rabbit": "Fashion",
    "Foxtale": "Health",
    "IKEA": "Other",
    "Lenovo": "Tech & Apps",
    "Dream11": "Entertainment",
    "Paytm": "Finance",
    "PhonePe": "Finance",
    "CRED": "Finance"
}

def calculate_bid(advertiser, industry, user_demographics, affinity_scores):
    """
    Calculate final bid for an advertiser based on:
    1. Base CPM for their industry
    2. Demographic multipliers
    3. Affinity score multipliers
    """

    # Step 1: Get base CPM
    base_cpm = CPM_RATES.get(industry, CPM_RATES["Other"])

    # Step 2: Apply demographic multipliers
    demographic_multiplier = 1.0
    for demo, multiplier in DEMOGRAPHIC_MULTIPLIERS.items():
        if user_demographics.get(demo, False):
            demographic_multiplier *= multiplier

    # Step 3: Apply affinity multipliers
    # Map industries to affinity scores
    industry_affinity_map = {
        "Education": "coding_score",
        "Tech & Apps": "coding_score",
        "Entertainment": "entertainment_score",
        "Fashion": "shopping_score",
        "Finance": "coding_score",
        "Health": "spiritual_score",
        "Travel": "local_mumbai_score",
        "Food": "local_mumbai_score"
    }

    affinity_key = industry_affinity_map.get(industry, "entertainment_score")
    affinity_score = affinity_scores.get(affinity_key, 0.5)

    # Affinity multiplier: 1 + (affinity_score × 0.5)
    # So 1.0 affinity = 1.5x multiplier, 0.5 affinity = 1.25x multiplier
    affinity_multiplier = 1 + (affinity_score * 0.5)

    # Final bid calculation
    final_bid = base_cpm * demographic_multiplier * affinity_multiplier

    return {
        "advertiser": advertiser,
        "industry": industry,
        "base_cpm": base_cpm,
        "demographic_multiplier": round(demographic_multiplier, 2),
        "affinity_multiplier": round(affinity_multiplier, 2),
        "final_bid": round(final_bid, 2)
    }

def simulate_rtb_auction():
    """Simulate the real-time bidding auction"""

    print("\n" + "="*70)
    print("REAL-TIME BIDDING AUCTION SIMULATOR")
    print("="*70)
    print("Simulating the 100ms auction that happens when you open Instagram...")
    print("="*70 + "\n")

    time.sleep(0.5)

    # Load user data
    print("[T+0ms] Loading user profile...")
    time.sleep(0.1)

    user_features = load_json("../output/user_feature_matrix.json")
    instagram_data = load_json("../output/instagram_data.json")

    user_demographics = user_features.get("user_demographics", {})
    affinity_scores = user_features.get("affinity_scores_normalized", {})

    print(f"[T+10ms] User profile loaded:")
    print(f"  - Single: {user_demographics.get('is_single')}")
    print(f"  - Educated: {user_demographics.get('is_educated')}")
    print(f"  - Engaged Shopper: {user_demographics.get('is_engaged_shopper')}")
    print(f"  - Device Change Likely: {user_demographics.get('potential_device_change')}")
    print(f"  - Top Affinity: Bollywood ({affinity_scores.get('bollywood_score', 0)})")
    time.sleep(0.1)

    # Select top 8 bidders
    print("\n[T+20ms] Broadcasting bid request to ad exchanges...")
    time.sleep(0.1)

    # Create diverse set of bidders
    bidders = [
        "LinkedIn APAC",
        "BookMyShow",
        "Cashify",
        "Tanishq",
        "Final Round AI",
        "Dream11",
        "Paytm",
        "Netflix India"
    ]

    print(f"[T+30ms] {len(bidders)} advertisers responding...")
    time.sleep(0.1)

    # Calculate bids
    print("\n[T+40ms] Calculating bids...\n")
    time.sleep(0.1)

    bids = []
    for advertiser in bidders:
        industry = ADVERTISER_INDUSTRIES.get(advertiser, "Other")
        bid_data = calculate_bid(advertiser, industry, user_demographics, affinity_scores)
        bids.append(bid_data)

        print(f"  {advertiser:25s} | Industry: {industry:15s} | Bid: Rs.{bid_data['final_bid']:8.2f}")
        time.sleep(0.1)

    # Sort by bid amount
    bids.sort(key=lambda x: x['final_bid'], reverse=True)

    print("\n[T+80ms] Auction complete! Determining winner...")
    time.sleep(0.1)

    # Winner
    winner = bids[0]
    second_price = bids[1]['final_bid'] if len(bids) > 1 else winner['final_bid']

    print("\n" + "="*70)
    print("AUCTION RESULTS")
    print("="*70)
    print(f"\nWINNER: {winner['advertiser']}")
    print(f"Industry: {winner['industry']}")
    print(f"Winning Bid: Rs.{winner['final_bid']:.2f} per 1000 impressions")
    print(f"Actual Price Paid (2nd price auction): Rs.{second_price:.2f}")
    print(f"\nBid Breakdown:")
    print(f"  Base CPM: Rs.{winner['base_cpm']}")
    print(f"  × Demographic Multiplier: {winner['demographic_multiplier']}x")
    print(f"  × Affinity Multiplier: {winner['affinity_multiplier']}x")
    print(f"  = Final Bid: Rs.{winner['final_bid']:.2f}")

    print("\n[T+100ms] Ad delivered to user's screen.")
    print("="*70)

    # Show full leaderboard
    print("\nFULL LEADERBOARD:")
    print("-"*70)
    for i, bid in enumerate(bids, 1):
        print(f"{i}. {bid['advertiser']:25s} Rs.{bid['final_bid']:8.2f}  "
              f"(Base: {bid['base_cpm']}, Demo: {bid['demographic_multiplier']}x, "
              f"Affinity: {bid['affinity_multiplier']}x)")
    print("-"*70)

    # Calculate annual revenue
    sessions_per_day = 8
    ads_per_session = 12
    days_per_year = 365

    # Average of top 3 bids
    top_3_bids = [b['final_bid'] for b in bids[:3]]
    avg_winning_bid = sum(top_3_bids) / len(top_3_bids) / 1000  # Convert to per-impression

    annual_revenue = sessions_per_day * ads_per_session * days_per_year * avg_winning_bid
    instagram_cut = annual_revenue * 0.3  # 30% platform fee
    advertiser_spend = annual_revenue * 0.7

    total_advertiser_pressure = user_features.get("advertiser_pressure", 0)

    print(f"\nANNUAL REVENUE CALCULATION:")
    print(f"  Sessions per day: {sessions_per_day}")
    print(f"  Ads per session: {ads_per_session}")
    print(f"  Days per year: {days_per_year}")
    print(f"  Avg winning bid (top 3): Rs.{avg_winning_bid:.4f} per impression")
    print(f"\n  Total annual revenue generated: Rs.{annual_revenue:,.2f}")
    print(f"  Instagram keeps (30%): Rs.{instagram_cut:,.2f}")
    print(f"  Advertisers spend (70%): Rs.{advertiser_spend:,.2f}")
    print(f"  You were paid: Rs.0.00")
    print(f"\n  YOUR DATA PRICE TAG: Rs.{annual_revenue:,.2f}")
    print(f"\n  Total advertisers competing: {total_advertiser_pressure}")

    # Save detailed results
    auction_results = {
        "top_bidders": bids[:5],
        "winner": winner,
        "second_price": second_price,
        "all_bids": bids,
        "user_demographics": user_demographics,
        "affinity_scores": affinity_scores,
        "total_advertisers": total_advertiser_pressure,
        "sessions_per_day": sessions_per_day,
        "ads_per_session": ads_per_session,
        "days_per_year": days_per_year,
        "avg_winning_bid": round(avg_winning_bid, 4),
        "annual_revenue_generated": round(annual_revenue, 2),
        "instagram_keeps": round(instagram_cut, 2),
        "advertiser_spend": round(advertiser_spend, 2),
        "you_were_paid": 0,
        "your_data_price_tag": round(annual_revenue, 2)
    }

    with open("../output/rtb_results.json", "w") as f:
        json.dump(auction_results, f, indent=2)

    print(f"\nDetailed results saved to output/rtb_results.json")
    print("="*70 + "\n")

if __name__ == "__main__":
    simulate_rtb_auction()
