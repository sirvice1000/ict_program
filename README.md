# ICT Trading Platform - Knowledge Base & Journal

A professional desktop application for tracking ICT (Inner Circle Trader) concepts and managing your trading journal.

## 🚀 Features

### 📚 Knowledge Base
- Store and organize trading concepts (FVG, Order Blocks, MSS, etc.)
- Add definitions, identification steps, trading rules, and examples
- Track key points, related concepts, and resources
- Search and filter by category
- Personal notes section for each concept

### 📊 Trade Journal
- Log all your trades with complete details
- Track entry, stop loss, take profit, and exit prices
- Automatic P&L calculation
- Tag trades with ICT concepts used
- Add chart screenshots
- Filter by outcome (Win/Loss/Pending)

### 📈 Analytics Dashboard
- Win rate and P&L statistics
- Best and worst trade tracking
- Trading performance insights
- Knowledge base statistics

## 🛠️ Installation

### Step 1: Install Python
Make sure you have Python 3.8 or higher installed:
```bash
python --version
```

### Step 2: Create Project Structure
Create the following folder structure in `E:\Codeing\ICT\ict_program`:

```
ict_program/
├── main.py
├── requirements.txt
├── README.md
├── database/
│   ├── __init__.py
│   └── db_manager.py
└── gui/
    ├── __init__.py
    ├── main_window.py
    ├── knowledge_tab.py
    ├── journal_tab.py
    └── analytics_tab.py
```

### Step 3: Create Empty __init__.py Files
In both `database/` and `gui/` folders, create empty files named `__init__.py`

### Step 4: Install Dependencies
Open Command Prompt in the project folder and run:
```bash
pip install -r requirements.txt
```

### Step 5: Run the Application
```bash
python main.py
```

## 📁 Project Structure

- **main.py** - Application entry point
- **database/** - Database layer
  - **db_manager.py** - SQLite database operations
- **gui/** - User interface components
  - **main_window.py** - Main application window
  - **knowledge_tab.py** - Knowledge base interface
  - **journal_tab.py** - Trade journal interface
  - **analytics_tab.py** - Analytics dashboard
- **trading_data.db** - SQLite database (created automatically)

## 💾 Database

The application uses SQLite for data storage. All data is stored locally in `trading_data.db`.

### Tables:
- **concepts** - Trading concepts and definitions
- **key_points** - Key points for each concept
- **related_concepts** - Related concept links
- **resources** - Learning resources
- **trades** - Trade journal entries
- **trade_concepts** - Links trades to concepts used

## 🎨 Features to Add (Future)

- [ ] Export data to PDF
- [ ] Chart image viewer
- [ ] Trade calendar view
- [ ] Concept relationship graph
- [ ] Import/Export data (JSON, CSV)
- [ ] Dark/Light theme toggle
- [ ] Multi-currency P&L tracking
- [ ] Advanced filtering and sorting
- [ ] Trade tags and custom fields
- [ ] Backup and restore functionality

## 💰 Monetization Ideas

1. **Basic Version (Free)**
   - Limited to 50 concepts and 100 trades
   - Core features only

2. **Pro Version ($49-99 one-time)**
   - Unlimited concepts and trades
   - Advanced analytics
   - PDF export
   - Priority support

3. **Premium Features (Add-ons)**
   - Cloud sync ($9/month)
   - Mobile companion app
   - AI trade analysis
   - Community concept sharing

## 📝 License

Copyright © 2024. All rights reserved.

## 🤝 Support

For issues or questions, contact: [your-email@example.com]

---

**Built for traders, by traders. Master ICT concepts and improve your trading performance!** 🚀