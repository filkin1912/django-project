Online Store for Computer Games  

## 🌐 Application Overview

This Django web application features:

- **Public Storefront**:  
  - “All Games” page accessible to all visitors  
  - Game browsing with detailed views

- **Private User Area** (requires authentication):  
  - View owned/purchased games  
  - Manage profile and wallet balance  
  - Add, edit, and delete games for sale

---

## 🔄 Core Functionalities

- **User Management**:  
  Registration, login/logout, profile editing, and profile image support

- **Wallet System**:  
  Users can add funds and spend them on game purchases

- **Selling Model**:  
  When a user sells a game, the sale price is credited to their wallet

- **Purchase Flow**:  
  Users buy games from the public store; funds are deducted from their wallet

- **Ownership Tracking**:  
  Purchases are recorded to ensure unique ownership per user-game pair

---

## ⚙️ Getting Started

### 1. Environment Setup
```bash
python -m venv venv
source venv/bin/activate  # Windows (PowerShell): venv\Scripts\Activate.ps1  /   # Windows (CMD)
venv\Scripts\activate.bat
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configuration
Set environment variables in settings.py:
- `SECRET_KEY`
- `DEBUG`
- `DATABASES`

### 4. Database Setup
```bash
python manage.py migrate
```

### 5. Admin Access (Optional)
```bash
python manage.py createsuperuser
```

### 6. Run Server
```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000`

---

## 👤 App: `accounts` – User & Wallet Management

### Models
- **AppUser**  
  - `money`: User’s wallet balance  
  - `profile_picture`: Optional avatar  
  - `full_name`: Combines first and last name
  -  `display_name`: fallback to email if name is missing

### Forms
- `ProfileCreateForm`: Handles user registration  
- `ProfileEditForm`: Allows profile updates

### Views
- `SignUpView`: Registers and logs in users  
- `SignInView` / `SignOutView`: Authentication flow  
- `ProfileDetailsView`: Displays user info and game count  
- `ProfileEditView` / `ProfileDeleteView`: Profile management

---

## 🎮 App: `games` – Game Catalog & Transactions

### Models
- **GameModel**  
  - `title`, `game_picture`,`summary`, `price` (min: 10)  
  - `category`: Enum-based genre  
  - `user`: Seller reference

### Forms
- `GameAddForm`: Create new game listings  
- `GameEditForm`: Update existing games  
- `GameDeleteForm`: Confirm and remove games  
- `GameBuyForm`: Validate and process purchases

### Views
- `IndexView`: Public game listing  
- `my_games`: User’s own games  
- `game_add`: Add new game  
- `game_details`: View game info and ownership status  
- `game_buy`: Deduct funds and record purchase  
- `game_edit` / `game_delete`: Modify or remove games

### Notes
- Custom validators (e.g., `is_unique`) prevent duplicate purchases

---

## 🧩 App: `common` – Purchase Tracking

### Models
- **BoughtGame**  
  - `game`, `user`: Foreign keys  
  - `unique_together`: Ensures one purchase per user-game pair

### Forms
- `BoughtGameForm`: Used to create purchase records
- `GameCommentForm`: comment submission

### Views
- `bought_games`: Displays games purchased by a specific user
- `delete_comment`: allows users to delete their own comment

---

## 🔁 Data Flow Summary

1. **User Registration**:  
   Creates an `AppUser` with default balance and optional profile image

2. **Game Listing**:  
   Authenticated users can list games for sale. User lists games are visible to all

3. **Public Storefront**:  
   Displays all games for browsing and purchase

4. **Purchasing**:  
   Deducts funds, records ownership in `BoughtGame`

5. **Selling**:  
   Credits the seller’s wallet with the game price

6. **Comments**:
   User leaves comment - pne per game, deletable
---

## 🔐 Security & UX Considerations

- **Access Control**:  
  Restrict wallet, profile, and game management to authenticated users

- **Validation**:  
  - Enforce minimum game price  
  - Prevent duplicate purchases  
  - Validate user existence for pk-based views

- **Privacy**:  
  - Limit visibility of purchased games to the owner  
  - Avoid exposing user data through public endpoints

---

## 🧪 Running Tests

Each test file is placed in its corresponding app folder:

- `accounts/tests.py`
- `games/tests.py`
- `common/tests.py`

- `accounts`: check user registration and login flows using Django’s test client.
- `games`: verify game CRUD operations and purchase logic (funds deducted, seller credited, duplicates blocked).
- `common`: ensure comment rules (one per user per game, only author can delete) and purchase tracking integrity.

These tests simulate user actions via Django’s built‑in TestCase and confirm that the core business rules of 
the app work as expected.

Run all tests with:

```bash
python manage.py test

```

## 📈 Extensibility & Improvements

- Expand `Category` enum with more genres
- Enforce ownership-based permissions for game edits/deletes
- Strengthen session validation in purchase views
- Handle edge cases for invalid user IDs

---

