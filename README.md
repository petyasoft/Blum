
# Software for Blum telegram Bot

## Requirements
- Python 3.11 (you can install it [here](https://www.python.org/downloads/release/python-3110/))
- Telegram API_ID and API_HASH (you can get them [here](https://my.telegram.org/auth?to=apps))



1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Get your API_ID and API_HASH:
   - Go to [my.telegram.org](https://my.telegram.org/auth?to=apps)
   - Sign in with your Telegram account
   - Create a new application to get your API_ID and API_HASH

3. Configure the application:
   - Open `config.py` and add your `API_ID` and `API_HASH`:
     ```python
     API_ID = your_api_id
     API_HASH = 'your_api_hash'
     ```

   - If you want to use a proxy, set `USE_PROXY` in `config.py` to `True`, otherwise set it to `False`:
     ```python
     USE_PROXY = True  # or False
     ```

   - If `USE_PROXY` is `True`, open `proxy.txt` and fill it out using the example provided. Ensure there are no extra lines in the file.
   Proxy format : ip:port:login:password session_name, session name is which use this proxy (WITHOUT .session, only session name)
   ```txt
   192.168.1.1:1234:username:password session1
   192.168.1.2:2934:username:password session2
   192.168.1.3:3834:username:password session3
   192.168.5.1:2884:username:password session4
   ```
   And don't forget set proxy type in `config.py`
   ```python
   PROXY_TYPE = "socks5" # or http
   ```

5. IMPORTANT Create a `sessions` folder



## Usage

1. Run the bot:
   ```bash
   python main.py
   ```

2. The software will work with all accounts using the single `API_ID` and `API_HASH`. No need to change them for each account.

## Important Notes

- **Python Version:** The software runs on Python 3.11. Using a different version may cause errors.
- DONT USE MAIN ACCOUNT BECAUSE THERE IS ALWAYS A CHANCE TO GET BANNED IN TELEGRAM


---

Thank you for using Blum Telegram Bot! Don't forget to follow our [Telegram channel](https://t.me/petyasofts) for updates.

Ton wallet for donations : UQCcEj6OWmdJ8FIvY8tVmSsGddn57PEyn438qfzbcgEZzb-O

EVM wallet for donations : 0xf3eaaf294f5883DD062900E6d9c578F695b7D2D2

