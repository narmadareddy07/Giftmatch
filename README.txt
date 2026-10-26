GIFTMATCH WEBSITE
=================

START ON WINDOWS
1. Extract the GiftMatch_Project.zip folder somewhere easy to find (e.g. Desktop).
2. Make sure Python 3 is installed. If not, install it from https://www.python.org/downloads/ and tick "Add Python to PATH".
3. Double-click start.bat. The first run installs Flask and creates giftmatch.db (SQLite) with the six existing catalog products.
4. Open http://127.0.0.1:5000 in Chrome or Edge.
5. Keep the black command window open while using the website. Close it to stop the local server.

FEATURES
- Clickable GiftMatch logo and Home / About Us / Products / Contact Us navigation.
- Premium lavender-and-cream responsive design with improved spacing, contrast, and mobile layouts.
- Gift-finder preferences for recipient and gift style, plus occasion, budget, finish, delivery and personalisation filters.
- Search, sorting by price or delivery, and a browser-local wishlist.
- Matching suggestions are lightweight keyword/metadata-based guidance, not AI-generated recommendations; review catalog data before relying on them.
- Product filters update immediately using product records loaded from SQLite.
- View Gift Details opens a product modal with an extra-information request field, copyable enquiry and share-link helper.
- Improved empty states, loading/error messaging, keyboard Escape-to-close behavior, and safe text rendering for catalog fields.
- Footer with purpose, navigation, contact details: 8019097373, mygiftmatch@gmail.com, Flat No. 301, Gayatri Towers, opposite Vanasthalipuram Police Station.
- SQLite-backed catalogue API: GET /api/products, GET /api/products/<id>, POST /api/products, PUT /api/products/<id>, DELETE /api/products/<id>.

CATALOGUE / CONTACT NOTES
- Existing catalog prices and delivery timelines are illustrative estimates; confirm them with suppliers.
- Replace hello@giftmatch.example and the address/social placeholders in templates/index.html with real business details before publishing.
- Product records are stored in giftmatch.db. The database is created and seeded on first launch; the JSON file is only used to seed a new/empty database.
- Wishlist items are saved in the current browser only (localStorage); they are not synced across devices.
- Recipient matching is a simple heuristic based on product names/descriptions/categories. Add structured tags to product data for more accurate matching.
- Product prices, delivery estimates and stock are illustrative; confirm with suppliers.
- This version is intended for local review and has not been deployed.


VISUAL UPDATE
The homepage now uses an editorial-style hero layout and a local image asset in /static/hero-gift.jpg. The catalogue still contains demo product records and indicative prices/timelines; verify supplier availability, pricing and delivery before using it commercially. The app remains local-only and has not been deployed online.
