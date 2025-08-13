# Chinese Numbers Practice

A minimal web application to practice pronouncing Chinese numbers. The backend is built with FastAPI in Python and uses Azure Cognitive Services for pronunciation assessment.

## Running locally

1. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
2. Set environment variables `AZURE_SPEECH_KEY` and `AZURE_SPEECH_REGION` with your Azure Speech credentials.
3. Start the server:
   ```bash
   uvicorn backend.main:app --reload
   ```
4. Open `http://localhost:8000` in your browser.

The page will show a random number and its Chinese reading. Record your pronunciation and the app will return an accuracy score from Azure.
