# Troubleshooting Vercel 500 Error

## Issue: Serverless Function Crashes (500 Error)

If you're seeing a 500 error after deployment, follow these steps:

## Step 1: Check Vercel Logs

1. Go to your Vercel dashboard
2. Click on your deployment
3. Click "View Function Logs" or "Logs" tab
4. Look for error messages that will tell you exactly what's failing

Common errors you might see:
- `ModuleNotFoundError`: Missing Python package
- `FileNotFoundError`: CSV files not found
- `ImportError`: Module import issues

## Step 2: Verify File Structure

Make sure your GitHub repository has this structure:
```
safeher-quiz-vercel/
├── api/
│   └── index.py
├── model/
│   ├── app.py
│   ├── stress_backend_simple.py
│   ├── config.py
│   └── datasets/
│       ├── emotional.csv
│       ├── safety.csv
│       ├── confidence.csv
│       ├── social_support.csv
│       ├── time_management.csv
│       ├── student.csv
│       ├── working_women.csv
│       └── housewife.csv
├── vercel.json
├── requirements.txt
└── .gitignore
```

## Step 3: Verify All Files Are Committed

Make sure ALL files, especially CSV files, are committed to Git:

```bash
git add .
git status  # Check if all files are staged
git commit -m "Fix: Include all required files"
git push origin main
```

## Step 4: Test Locally First

Before deploying, test that your code works locally:

```bash
# From project root
cd model
python app.py

# In another terminal, test the health endpoint
curl http://localhost:5000/health
```

## Step 5: Check Vercel Build Logs

In Vercel dashboard:
1. Go to your project
2. Click on the failed deployment
3. Check "Build Logs" for any build errors
4. Check "Function Logs" for runtime errors

## Common Fixes

### Fix 1: Missing Dependencies

If you see `ModuleNotFoundError`, update `requirements.txt`:

```txt
Flask==2.3.3
Flask-CORS==4.0.0
```

Then commit and redeploy:
```bash
git add requirements.txt
git commit -m "Fix: Update requirements"
git push origin main
```

### Fix 2: CSV Files Not Found

If you see `FileNotFoundError`, ensure:
1. All CSV files are in `model/datasets/` directory
2. All CSV files are committed to Git (not in .gitignore)
3. File paths are correct in `stress_backend_simple.py`

### Fix 3: Import Errors

If you see `ImportError`, check:
1. `api/index.py` correctly imports from `model.app`
2. Python path is set correctly
3. All Python files are in the right directories

## Debug Endpoint

Add this to `model/app.py` to help debug:

```python
@app.route("/debug", methods=["GET"])
def debug():
    import os
    return jsonify({
        "cwd": os.getcwd(),
        "files_in_model": os.listdir("model") if os.path.exists("model") else "model dir not found",
        "datasets_exists": os.path.exists("model/datasets"),
        "datasets_files": os.listdir("model/datasets") if os.path.exists("model/datasets") else "datasets not found"
    })
```

Then test:
```bash
curl https://your-app.vercel.app/debug
```

## Alternative: Deploy as Individual API Routes

If the single serverless function approach doesn't work, you can split into individual routes:

Create `api/get-questions.py`:
```python
from model.app import app
@app.route('/api/get-questions', methods=['POST'])
def get_questions():
    # Your code here
```

But for now, try the fixes above first.

## Still Not Working?

1. Share the exact error from Vercel logs
2. Verify all files are committed: `git ls-files | grep -E "\.(py|csv)$"`
3. Try deploying a minimal test first:
   - Create `api/test.py` with just `print("Hello")` and a simple return
   - Deploy that first to verify Vercel is working

