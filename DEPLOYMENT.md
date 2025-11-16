# Deployment Guide: GitHub + Vercel

This guide will walk you through deploying your Flask quiz application to GitHub and then to Vercel.

## Prerequisites

- Git installed on your computer
- A GitHub account
- A Vercel account (free tier available)
- Node.js installed (for Vercel CLI, optional but recommended)

## Part 1: Push to GitHub

### Step 1: Initialize Git Repository (if not already done)

1. Open your terminal/PowerShell in the project root directory (`E:\safeher_quiz_vercel`)

2. Check if Git is already initialized:
   ```bash
   git status
   ```

3. If Git is not initialized, run:
   ```bash
   git init
   ```

### Step 2: Add All Files to Git

1. Add all files to staging:
   ```bash
   git add .
   ```

2. Check what files will be committed:
   ```bash
   git status
   ```

### Step 3: Create Initial Commit

```bash
git commit -m "Initial commit: Flask quiz app ready for Vercel deployment"
```

### Step 4: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Repository name: `safeher-quiz-vercel` (or your preferred name)
5. Description: "Flask-based quiz application for stress assessment"
6. Choose **Public** or **Private** (your choice)
7. **DO NOT** initialize with README, .gitignore, or license (we already have these)
8. Click "Create repository"

### Step 5: Connect Local Repository to GitHub

1. After creating the repository, GitHub will show you commands. Use these:

   ```bash
   # Add remote repository (replace YOUR_USERNAME with your GitHub username)
   git remote add origin https://github.com/YOUR_USERNAME/safeher-quiz-vercel.git
   
   # Verify remote was added
   git remote -v
   ```

### Step 6: Push to GitHub

```bash
# Push to main branch (or master if that's your default)
git branch -M main
git push -u origin main
```

If prompted for credentials:
- Username: Your GitHub username
- Password: Use a **Personal Access Token** (not your GitHub password)
  - Create one at: Settings → Developer settings → Personal access tokens → Tokens (classic)
  - Select scopes: `repo` (full control of private repositories)

---

## Part 2: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard (Recommended for beginners)

#### Step 1: Sign Up / Log In to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Sign up or log in (you can use your GitHub account for easier integration)

#### Step 2: Import Project from GitHub

1. Click "Add New..." → "Project"
2. You'll see your GitHub repositories listed
3. Find `safeher-quiz-vercel` and click "Import"

#### Step 3: Configure Project

1. **Project Name**: Will auto-populate (you can change it)
2. **Framework Preset**: Leave as "Other" or select "Python" if available
3. **Root Directory**: Leave as `./` (project root)
4. **Build Command**: Leave empty (Vercel will auto-detect)
5. **Output Directory**: Leave empty
6. **Install Command**: Leave empty (Vercel uses `pip install -r requirements.txt` automatically)

#### Step 4: Environment Variables (Optional)

If you need any environment variables:
- Click "Environment Variables"
- Add variables like:
  - `FLASK_ENV=production`
  - `PORT=5000` (usually auto-set by Vercel)

#### Step 5: Deploy

1. Click "Deploy"
2. Wait for deployment to complete (usually 1-3 minutes)
3. You'll see a deployment URL like: `https://safeher-quiz-vercel.vercel.app`

#### Step 6: Test Your Deployment

Test the health endpoint:
```bash
curl https://your-app-name.vercel.app/health
```

Test the get-questions endpoint:
```bash
curl -X POST https://your-app-name.vercel.app/get-questions \
  -H "Content-Type: application/json" \
  -d "{\"role\": \"student\"}"
```

---

### Option B: Deploy via Vercel CLI (Advanced)

#### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

#### Step 2: Login to Vercel

```bash
vercel login
```

#### Step 3: Deploy

1. Navigate to project root:
   ```bash
   cd E:\safeher_quiz_vercel
   ```

2. Run deployment:
   ```bash
   vercel
   ```

3. Follow the prompts:
   - Set up and deploy? **Yes**
   - Which scope? (Select your account)
   - Link to existing project? **No** (first time)
   - Project name? (Press Enter for default)
   - Directory? **./** (current directory)
   - Override settings? **No**

4. For production deployment:
   ```bash
   vercel --prod
   ```

---

## Post-Deployment Checklist

### ✅ Verify Deployment

1. **Health Check**: Visit `https://your-app.vercel.app/health`
   - Should return: `{"status": "healthy", "message": "Stress model API is running"}`

2. **Test Get Questions**:
   ```bash
   curl -X POST https://your-app.vercel.app/get-questions \
     -H "Content-Type: application/json" \
     -d "{\"role\": \"student\"}"
   ```

3. **Test Submit Answers**:
   ```bash
   curl -X POST https://your-app.vercel.app/submit-answers \
     -H "Content-Type: application/json" \
     -d "{\"role\": \"student\", \"answers\": [1,2,3,4,5,1,2,3]}"
   ```

### ✅ Update Frontend Configuration

If you have a frontend application, update the API base URL:

```javascript
// In your frontend code (e.g., stressService.js)
const STRESS_API_BASE_URL = 'https://your-app-name.vercel.app';
```

### ✅ Configure CORS (if needed)

The Flask app already has CORS enabled. If you need to add your frontend domain, update `model/config.py`:

```python
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8081",
    "https://your-frontend-domain.vercel.app",  # Add your frontend URL
]
```

After updating, commit and push to GitHub. Vercel will automatically redeploy.

---

## Automatic Deployments

Once connected to GitHub, Vercel will:
- ✅ Automatically deploy on every push to `main` branch
- ✅ Create preview deployments for pull requests
- ✅ Show deployment logs and status in Vercel dashboard

---

## Troubleshooting

### Issue: Build Fails

**Solution**: 
- Check Vercel build logs in the dashboard
- Ensure `requirements.txt` is in the root directory
- Verify all Python dependencies are listed

### Issue: "Module not found" errors

**Solution**:
- Ensure `model/` directory is committed to Git
- Check that all CSV files in `model/datasets/` are included
- Verify file paths in `stress_backend_simple.py` are relative

### Issue: 404 errors on routes

**Solution**:
- Check `vercel.json` configuration
- Ensure `api/index.py` exists and imports the Flask app correctly
- Verify routes in Flask app match expected paths

### Issue: CORS errors from frontend

**Solution**:
- Verify Flask-CORS is installed (`Flask-CORS==4.0.0` in requirements.txt)
- Check `model/config.py` includes your frontend URL
- Ensure CORS is enabled in `model/app.py` with `CORS(app)`

### Issue: Function timeout

**Solution**:
- Vercel free tier has a 10-second timeout on serverless functions
- For longer operations, consider optimizing your code or upgrading to Pro plan

---

## File Structure for Vercel

```
safeher_quiz_vercel/
├── api/
│   └── index.py              # Vercel serverless function entry point
├── model/
│   ├── app.py                # Flask application
│   ├── stress_backend_simple.py
│   ├── config.py
│   ├── requirements.txt
│   └── datasets/             # CSV files for questions
│       ├── student.csv
│       ├── working_women.csv
│       └── ...
├── vercel.json               # Vercel configuration
├── requirements.txt          # Root-level requirements for Vercel
├── .gitignore               # Git ignore rules
└── DEPLOYMENT.md            # This file
```

---

## Quick Reference Commands

### Git Commands
```bash
git add .
git commit -m "Your commit message"
git push origin main
```

### Vercel CLI Commands
```bash
vercel              # Deploy to preview
vercel --prod       # Deploy to production
vercel logs         # View deployment logs
```

### Testing API Endpoints
```bash
# Health check
curl https://your-app.vercel.app/health

# Get questions
curl -X POST https://your-app.vercel.app/get-questions \
  -H "Content-Type: application/json" \
  -d "{\"role\": \"student\"}"

# Submit answers
curl -X POST https://your-app.vercel.app/submit-answers \
  -H "Content-Type: application/json" \
  -d "{\"role\": \"student\", \"answers\": [1,2,3,4,5,1,2,3]}"
```

---

## Support

If you encounter issues:
1. Check Vercel deployment logs in the dashboard
2. Review GitHub Actions/commits
3. Test endpoints using curl or Postman
4. Verify all files are committed to Git

---

**Congratulations!** 🎉 Your quiz application is now live on Vercel!

