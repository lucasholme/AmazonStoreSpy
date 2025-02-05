🛒 Seller ASIN Tracker Bot
==========================

This project is a **Discord bot** that integrates with the **Keepa API** to track **Amazon sellers' ASINs** and update a local SQLite database. The bot can fetch ASINs from multiple sellers, store them, and notify users of any newly added ASINs.

🚀 Features
-----------

-   ✅ **Fetch ASINs** -- Calls the Keepa API to retrieve ASINs for specified sellers.
-   ✅ **Track Changes** -- Compares stored ASINs with new ones to detect changes.
-   ✅ **Database Integration** -- Stores seller names and ASINs in an SQLite database.
-   ✅ **Automated Updates** -- Updates the database with the latest ASIN data.
-   ✅ **Discord Bot Commands** -- Allows users to retrieve updates directly from Discord.

📥 Installation
---------------

Ensure you have **Python 3.x** installed on your system.

### 1️⃣ Clone the Repository

```
git clone https://github.com/your-username/seller-asin-tracker.git
```

### 2️⃣ Install Dependencies

```
pip install discord.py requests sqlite3
```

🛠️ Usage
---------

### 1️⃣ Set Up Your API Key and Seller IDs

Edit the `fetch_asins()` function in `bot.py` to include your **Keepa API key** and the **seller IDs** you want to track:

```
api_key = 'your_keepa_api_key'
seller_ids = {
    "SellerName1": "StorefrontID1",
    "SellerName2": "StorefrontID2"
}
```

### 2️⃣ Run the Bot

```
python bot.py
```

### 3️⃣ Discord Commands

Once the bot is running, you can use the following command in your Discord server:

-   **`!update`** -- Displays newly added ASINs for tracked sellers.

🗄️ Database Structure
----------------------

The bot uses an **SQLite database (`sellers.db`)** with the following structure:

| Column | Type | Description |
| --- | --- | --- |
| `name` | TEXT | Name of the Amazon seller |
| `asins` | TEXT | Comma-separated list of ASINs |

🔄 How It Works
---------------

1.  **Fetch ASINs** -- Retrieves ASINs for each seller using the Keepa API.
2.  **Check for Updates** -- Compares the newly fetched ASINs with those stored in the database.
3.  **Store Data** -- If a seller isn't in the database, their ASINs are stored.
4.  **Detect New ASINs** -- If a seller adds new ASINs, they are detected and stored.
5.  **Update the Database** -- Deletes old ASINs and replaces them with the latest ones.
6.  **Discord Bot Notification** -- Users can check new ASINs by running `!update`.

🔥 Example Output
-----------------

When the bot detects new ASINs, it outputs something like this:

```
{
    "SellerName1": ["B08N5WRWNW", "B09F3G23P4"],
    "SellerName2": ["B07KQXGK67"]
}
```

🛑 Notes
--------

⚠️ **API Limitations** -- Ensure your Keepa API plan allows sufficient requests.\
⚠️ **Database Persistence** -- The database resets on each update to maintain current ASINs.\
⚠️ **Discord Bot Token** -- Replace `"INSERT_DISCORD_TOKEN"` with your bot's token before running.

📜 License
----------

This project is open-source under the MIT License.
