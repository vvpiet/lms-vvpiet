# Deploy Faculty Feedback System on Streamlit Community Cloud

## Step-by-Step Deployment Guide

### Prerequisites
- GitHub account (free)
- Streamlit Community Cloud account (free)

### Step 1: Push Code to GitHub

1. **Create a new GitHub repository:**
   - Go to https://github.com/new
   - Name it `faculty-feedback-system`
   - Add description: "Faculty Feedback Collection System"
   - Choose Public
   - Click "Create repository"

2. **Initialize Git locally:**
   ```powershell
   cd C:\Users\ho\Desktop\Feedback
   git init
   git add .
   git commit -m "Initial commit: Faculty feedback system"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/faculty-feedback-system.git
   git push -u origin main
   ```
   
   Replace `YOUR_USERNAME` with your GitHub username.

### Step 2: Prepare Streamlit App

The `streamlit_app.py` file is ready with:
- ✓ Student feedback submission (1-10 ratings)
- ✓ Admin dashboard with statistics
- ✓ Analytics with charts
- ✓ Data export (CSV)
- ✓ User authentication (login/register)

### Step 3: Deploy on Streamlit Community Cloud

1. **Go to Streamlit Community Cloud:**
   - Visit https://share.streamlit.io
   - Sign in with GitHub

2. **Deploy New App:**
   - Click "New app" button
   - Select your repository: `faculty-feedback-system`
   - Main file path: `streamlit_app.py`
   - Click "Deploy"

3. **Wait for deployment** (takes 1-2 minutes)

### Step 4: Access Your App

Once deployed, you'll get a URL like:
```
https://faculty-feedback-system-YOUR_USERNAME.streamlit.app
```

### Demo Credentials (Pre-loaded)

**Student Account:**
- Username: `student`
- Password: `student123`

**Admin Account:**
- Username: `admin`
- Password: `admin123`

## Features Available

### For Students
- 📝 Submit feedback form with faculty dropdown
- 📊 Rate on 6 dimensions (1-10 scale)
- 💬 Add optional comments
- 👤 Anonymous or identified feedback

### For Admins
- 📊 Dashboard with statistics
- 📈 Analytics with charts and graphs
- 📋 Export feedback as CSV
- 👥 View all submissions
- 📉 Faculty performance analysis

## File Structure

```
faculty-feedback-system/
├── streamlit_app.py          # Main Streamlit app
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── README.md                # Documentation
└── .gitignore               # Git ignore file
```

## Troubleshooting

### Issue: "Module not found" error
**Solution:** Make sure all dependencies are in `requirements.txt`

### Issue: Database not persisting
**Solution:** Streamlit Community Cloud uses ephemeral storage. Data will reset when app restarts. For persistent storage, you can upgrade to Streamlit for Teams or integrate with a cloud database.

### Issue: "Permission denied" on GitHub push
**Solution:** Generate a Personal Access Token:
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Use token as password instead of your password

## Customization Tips

1. **Change database location:** Edit `DB_PATH = "feedback_streamlit.db"` in streamlit_app.py

2. **Add more faculty:** Modify the `faculty_list` in the `init_database()` function

3. **Custom theme:** Edit `.streamlit/config.toml` to change colors

4. **Change demo credentials:** Modify the default user creation in `init_database()`

## Next Steps

- Share the public URL with students and faculty
- Monitor feedback through the admin dashboard
- Export data regularly for analysis
- Consider integrating with a cloud database for persistent storage

## Support

For issues with Streamlit deployment, visit:
- https://docs.streamlit.io/
- https://discuss.streamlit.io/

Enjoy your Faculty Feedback System! 🎓
