# Layer 2 Setup: Gemini Embeddings

## Step 1: Get Your FREE Gemini API Key

1. Visit: https://aistudio.google.com/app/apikey
2. Click **"Create API Key"**
3. Copy the key (starts with `AIza...`)

## Step 2: Add to .env File

Open `D:\privacy-report\.env` and add:

```
GEMINI_API_KEY=AIzaSy...your-key-here
```

Your .env should now have both keys:
```
OPENROUTER_API_KEY=sk-or-v1-...
GEMINI_API_KEY=AIzaSy...
```

## Step 3: Install Dependencies

```bash
cd D:\privacy-report
pip install -r requirements.txt
```

## Step 4: Run Layer 2

```bash
python parsers/gemini_embeddings.py
```

## What You'll See

The script will:
1. Load your Instagram, Google, and AI data
2. Apply "contextual padding" to each item (the secret sauce)
3. Get embeddings from Gemini API
4. Find TOP 10 most similar cross-platform pairs
5. Save to `output/embeddings.json`

## Expected Output

```
🚨 MOST SURPRISING HIDDEN CONNECTIONS FOUND:

1. SIMILARITY: 0.891
   Gemini Files: "betterme ai interviewer"
   ↕️
   Instagram Ads: "Final Round AI"
   💡 Meaning: Gemini Files → Instagram Ads surveillance connection
```

This shows Instagram KNEW you were building an AI interviewer before you told anyone!
