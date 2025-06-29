# 🚀 Deployment Guide

## Deploy to Streamlit Cloud (Recommended)

### Step 1: Prepare Your Repository
1. Make sure your code is pushed to GitHub
2. Ensure your `.gitignore` includes `.streamlit/` to keep secrets local
3. Verify `requirements.txt` is up to date

### Step 2: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `all-trails-gentile`
5. Set the main file path: `app/main.py`
6. Click "Deploy!"

### Step 3: Configure Secrets (Important!)
After deployment, you need to add your OpenAI API key:

1. In your deployed app, go to the hamburger menu (☰) → "Settings"
2. Click "Secrets"
3. Add your OpenAI API key:
```toml
OPENAI_API_KEY = "your-api-key-here"
```
4. Click "Save"

### Step 4: Share Your App
- Your app will be available at: `https://your-app-name.streamlit.app`
- Share this link with anyone!

## Alternative Deployment Options

### Heroku
- More complex setup
- Requires `Procfile` and `runtime.txt`
- Good for custom domains

### Railway
- Simple deployment
- Good free tier
- Automatic deployments from GitHub

### Vercel
- Fast deployment
- Good for static sites
- May need additional configuration for Streamlit

## Environment Variables
Make sure to set these in your deployment platform:
- `OPENAI_API_KEY`: Your OpenAI API key

## Troubleshooting
- **403 Errors**: Normal with web scraping, users can try different URLs
- **API Key Issues**: Ensure secrets are properly configured
- **Import Errors**: Check that all dependencies are in `requirements.txt`

## Security Notes
- Never commit API keys to your repository
- Use environment variables/secrets for sensitive data
- The `.streamlit/` folder is ignored to keep secrets local 