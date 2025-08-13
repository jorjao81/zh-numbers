# Chinese Number Pronunciation Trainer

This is a web application designed to help users practice their pronunciation of Chinese numbers. The application displays a number, records the user's pronunciation, and uses Azure's AI-powered Speech Service to provide an accuracy score.

## Features

- Random number generation (1-999).
- Conversion of numbers to their idiomatic Chinese character representation.
- Browser-based audio recording.
- Real-time pronunciation assessment using Azure Cognitive Services.
- Clean, simple, and responsive user interface.

## Project Structure

```
/
├── backend/
│   ├── app.py              # Main Flask application with API endpoints
│   ├── number_converter.py # Logic for number-to-Chinese conversion
│   └── requirements.txt    # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css       # Styles for the frontend
│   └── js/
│       └── app.js          # Frontend JavaScript logic
├── templates/
│   └── index.html          # Main HTML page
├── .env.example            # Example environment file for credentials
├── .gitignore              # Git ignore file
└── README.md               # This file
```

## How to Set Up and Run

### Prerequisites

- Python 3.7+
- An active Microsoft Azure account with a Speech Service resource. You will need the **API Key** and **Region** for your resource.
- **FFmpeg**: The application uses the `pydub` library for audio conversion, which requires FFmpeg to be installed on the system.
  - On **macOS** (using [Homebrew](https://brew.sh/)): `brew install ffmpeg`
  - On **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
  - On **Windows**: Download the binaries from the [official FFmpeg website](https://ffmpeg.org/download.html) and add the `bin` directory to your system's PATH.

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Set Up a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
# For Unix/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages using pip.

```bash
pip install -r backend/requirements.txt
```

### 4. Configure Environment Variables

The application requires your Azure Speech Service credentials.

1.  Make a copy of the example environment file:
    ```bash
    cp .env.example .env
    ```
2.  Open the `.env` file in a text editor.
3.  Replace the placeholder values with your actual Azure Speech Key and Region.

    ```
    SPEECH_KEY=YOUR_AZURE_SPEECH_KEY
    SPEECH_REGION=YOUR_AZURE_SPEECH_REGION
    ```

### 5. Run the Application

Once the setup is complete, you can run the Flask application.

```bash
python backend/app.py
```

The application will be available at `http://127.0.0.1:5001`. Open this URL in your web browser. You may need to grant the browser permission to access your microphone.
