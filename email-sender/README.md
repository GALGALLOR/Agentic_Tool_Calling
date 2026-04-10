Email Sender (Python)
=====================

This small project sends email via SMTP using credentials stored in a `.env` file.

Files
- `send_email.py` — main sender script
- `.env.template` — template for environment variables
- `requirements.txt` — Python dependencies
- `.gitignore` — ignores `.env` and logs
- `examples/README.md` — quick run examples

Quick start

1. Create a virtualenv and install deps:

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\\Scripts\\Activate on Windows
pip install -r requirements.txt
```

2. Copy `.env.template` to `.env` and fill values (Gmail users may need an App Password):

```bash
cp .env.template .env
```

3. Send a test message:

```bash
python send_email.py --to galgalloroba.gr.gr.gr@gmail.com --subject "test" --body "I am testing you."
```

Notes
- For Gmail, prefer an App Password (accounts with 2FA). If you need OAuth2, ask and I can add it.
- Do not commit your `.env`.

OAuth2 option
- This project includes `send_email_oauth.py` which uses Google's OAuth2 flow and the Gmail API.
- Steps:
	1. Go to Google Cloud Console → APIs & Services → Credentials. Create an OAuth 2.0 Client ID for "Desktop app" and download the JSON as `credentials.json` into the `email-sender` folder.
	2. Enable the Gmail API for your project in Cloud Console.
	3. Install extra dependencies: `pip install -r requirements.txt` (includes `google-auth-oauthlib` and friends).
	4. Run the oauth sender once to authorize:

```powershell
python send_email_oauth.py --to galgalloroba.gr.gr.gr@gmail.com --subject "test" --body "I am testing you."
```

	A browser window will open to let you grant permission; the token will be saved to `token.json`.

Use OAuth2 if you prefer not to use App Passwords.

Detailed OAuth2 setup (Web client or Desktop client)

- Enable the Gmail API
	1. Open the Cloud Console: https://console.developers.google.com/apis/library/gmail.googleapis.com
	2. Select your project and click **Enable**. Wait a few minutes for propagation if you just enabled it.

- Create OAuth credentials
	- Desktop app (recommended for local scripts):
		1. APIs & Services → Credentials → Create Credentials → OAuth client ID → Application type: **Desktop app** → Create.
		2. Download the JSON and save it as `credentials.json` in `email-sender`.
		3. Run the script; it will open a browser and authorize with a redirect URI handled by the local server automatically.

	- Web client (if you already created one and want to keep it):
		1. In the Web client settings add the exact redirect URI you will use, for example `http://localhost:5000/` (match the `--port` you pass to the script).
		2. Download the client JSON to `credentials.json`.
		3. Run the script with the same port: `python send_email_oauth.py --port 5000 ...`.

- Consent screen & test users
	- If your OAuth consent screen is set to **External** and your app is in testing, add the Google account(s) you will use as **Test users** in the OAuth consent screen settings; otherwise Google will block the sign-in.

- Common errors & troubleshooting
	- Error 400 `redirect_uri_mismatch`: means the OAuth client is not a Desktop app and the redirect URI used by the local server is not listed in the Web client. Fix by creating a Desktop client or adding the exact `http://localhost:PORT/` redirect URI to the Web client.
	- HttpError 403 `accessNotConfigured` or "Gmail API has not been used in project ...": enable the Gmail API for your project and wait a few minutes.
	- If you change clients or ports, delete `token.json` so a fresh authorization flow runs:
		```powershell
		Remove-Item .\email-sender\token.json -ErrorAction SilentlyContinue
		```

- Full run example (from repository root)
	```powershell
	Set-Location .\email-sender
	. .\.venv\Scripts\Activate
	pip install -r requirements.txt
	python send_email_oauth.py --to galgalloroba.gr.gr.gr@gmail.com --subject "test" --body "I am testing you." --port 5000
	```

