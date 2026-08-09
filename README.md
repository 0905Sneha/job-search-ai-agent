## Data Persistence
This app uses SQLite for storing saved jobs and user preferences. This works fully when running locally (`streamlit run app.py`), providing persistent storage across sessions on your machine.

**Note:** Streamlit Cloud's free tier uses temporary containers that reset on redeploy/inactivity, so SQLite data does not persist on the live deployed version. For production use, this would be replaced with a hosted database (e.g., Supabase or PostgreSQL) to enable persistence across the deployed app's restarts. This is a planned future enhancement.
