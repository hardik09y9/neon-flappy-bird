# Neon Flappy Bird

A browser-playable Flappy Bird-style arcade game with a dark neon aesthetic, built with Python and Streamlit.

## Run locally

1. Install Python 3.9 or newer.
2. Open a terminal in this folder.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the game:

   ```bash
   streamlit run app.py
   ```

5. Open the local URL printed by Streamlit (usually http://localhost:8501).

## Deploy free with Streamlit Community Cloud

1. Create a GitHub account if you don't already have one.
2. Create a new **public** GitHub repository, e.g. `neon-flappy-bird`.
3. Upload `app.py`, `requirements.txt`, and `README.md` to the repository.
4. Visit https://share.streamlit.io/ and sign in with GitHub.
5. Choose **Create app**, select your repository, branch (`main`), and main file path (`app.py`).
6. Click **Deploy**. Streamlit will build the app and provide a public URL.

## Controls

- Spacebar / Up Arrow: flap
- Mouse click / touchscreen tap: flap
- Start Game: begin or restart
- Sound: toggle sound effects

Best score is stored in the browser's local storage on that device.
