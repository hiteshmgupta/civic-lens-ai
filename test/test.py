import pandas as pd
import numpy as np
import random

# Configuration
NUM_ROWS = 1000
CATEGORIES = ['Finance', 'Tech', 'Climate', 'Security', 'Agriculture']
CONTROVERSY_LEVELS = ['Low', 'Moderate', 'High', 'Extreme']

data = []

for i in range(1, NUM_ROWS + 1):
    category = random.choice(CATEGORIES)
    duration_days = random.randint(14, 90)
    
    # Decide the target controversy level for this row to shape the variables
    expected_controversy = np.random.choice(CONTROVERSY_LEVELS, p=[0.4, 0.3, 0.2, 0.1])
    
    if expected_controversy == 'Low':
        # High consensus, low variance, low-med engagement
        comment_count = random.randint(5, 150)
        voter_count = random.randint(50, 500)
        upvote_ratio = random.uniform(0.85, 0.99) if random.choice([True, False]) else random.uniform(0.01, 0.15)
        sentiment_mean = random.uniform(0.5, 0.9) if upvote_ratio > 0.5 else random.uniform(-0.9, -0.5)
        sentiment_variance = random.uniform(0.01, 0.20)
        # One dominant stance
        stances = np.random.dirichlet((8.0, 1.0, 1.0, 1.0))
        
    elif expected_controversy == 'Moderate':
        # Mildly divided, medium variance, med engagement
        comment_count = random.randint(100, 400)
        voter_count = random.randint(300, 1000)
        upvote_ratio = random.uniform(0.65, 0.85) if random.choice([True, False]) else random.uniform(0.15, 0.35)
        sentiment_mean = random.uniform(-0.4, 0.4)
        sentiment_variance = random.uniform(0.25, 0.50)
        # Somewhat dominant stance, but others are present
        stances = np.random.dirichlet((4.0, 2.0, 2.0, 1.0))
        
    elif expected_controversy == 'High':
        # Divided, high variance, high engagement
        comment_count = random.randint(300, 800)
        voter_count = random.randint(800, 1500)
        upvote_ratio = random.uniform(0.40, 0.60)
        sentiment_mean = random.uniform(-0.2, 0.2)
        sentiment_variance = random.uniform(0.55, 0.80)
        # Evenly spread stances
        stances = np.random.dirichlet((2.0, 2.0, 1.5, 1.5))
        
    else: # Extreme
        # Perfectly polarized, max variance, max engagement
        comment_count = random.randint(600, 1000)
        voter_count = random.randint(1200, 2000)
        upvote_ratio = random.uniform(0.48, 0.52)
        sentiment_mean = random.uniform(-0.1, 0.1)
        sentiment_variance = random.uniform(0.85, 1.00)
        # Perfectly split between support and oppose
        stances = np.random.dirichlet((5.0, 5.0, 0.5, 0.5))

    # Calculate actual counts based on ratios
    upvotes = int(voter_count * upvote_ratio)
    downvotes = voter_count - upvotes
    view_count = voter_count * random.randint(2, 10)
    
    # Shuffle stances so "Support" isn't always the dominant one in low controversy
    np.random.shuffle(stances)
    support_count = int(comment_count * stances[0])
    oppose_count = int(comment_count * stances[1])
    neutral_count = int(comment_count * stances[2])
    suggestion_count = comment_count - (support_count + oppose_count + neutral_count)

    row = {
        'amendment_id': i,
        'amendment_title': f"Policy Proposal {i} ({category})",
        'category': category,
        'duration_days': duration_days,
        'comment_count': comment_count,
        'voter_count': voter_count,
        'view_count': view_count,
        'upvotes': upvotes,
        'downvotes': downvotes,
        'sentiment_mean': round(sentiment_mean, 3),
        'sentiment_variance': round(sentiment_variance, 3),
        'support_count': support_count,
        'oppose_count': oppose_count,
        'neutral_count': neutral_count,
        'suggestion_count': suggestion_count,
        'expected_controversy': expected_controversy
    }
    data.append(row)

# Create DataFrame and export
df = pd.DataFrame(data)

# You may need to run: pip install openpyxl
file_name = 'controversy_test_data_1000.xlsx'
df.to_excel(file_name, index=False, engine='openpyxl')

print(f"Successfully generated {NUM_ROWS} rows and saved to {file_name}")