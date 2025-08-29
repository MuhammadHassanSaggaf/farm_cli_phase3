# Agrimate CLI

![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![SQLite](https://img.shields.io/badge/database-SQLite-lightgrey)
![Pipenv](https://img.shields.io/badge/dependencies-Pipenv-green)
![No License](https://img.shields.io/badge/license-none-lightgrey)

Agrimate is a simple, menu-driven command-line application designed to help farmers manage farm records easily — without the need for complex spreadsheets or technical skills. Agrimate stores data locally in an SQLite database and provides clear, guided prompts so farmers worldwide can track animals, feeds, inventory, sales, personnel, and feeding events.

---

## ✨ Key Features

* **Animal Management**: Add, view, search, and delete animals (tag, species, breed, DOB).
* **Feed Management**: Track feeds with unit, cost, and stock quantity.
* **Feeding Events**: Log feed given to animals and view feeding histories.
* **Inventory Tracking**: Manage tools and supplies with quantities and categories.
* **Sales Records**: Record sales transactions (product, quantity, price, total).
* **Personnel Management**: Keep simple staff records (name, role, salary).
* **Interactive Menus**: Numbered menus and prompts with clear success (✅) and error (❌) messages.
* **Seeder Script**: `seed.py` to populate the database with example data for testing/demo.

---

## ⚙️ Requirements

* **Python** 3.11 or newer
* **SQLite** (bundled with Python)

**Python packages (from `Pipfile` / dependencies):**

* SQLAlchemy
* colorama
* python-dotenv
* tabulate
* alembic

---

## 🧭 Installation

1. **Install Python (3.11+)**

   * Download from [https://www.python.org/downloads/](https://www.python.org/downloads/) and install.

2. **(Optional but recommended) Install Pipenv**

   ```bash
   pip install pipenv
   ```

3. **Extract the project**

   * Unzip `farm_cli_phase3.zip` into a folder. You should see `run.py`, `Pipfile`, and a `farm_cli/` directory.

4. **Install dependencies**

* Using Pipenv (recommended):

  ```bash
  cd /path/to/agrimate
  pipenv install
  pipenv shell
  ```

* Without Pipenv (system-wide):

  ```bash
  pip install SQLAlchemy colorama python-dotenv tabulate alembic
  ```

---

## 🚀 Running Agrimate

From the project folder (where `run.py` lives):

```bash
python run.py
```

You will see the main menu with numbered options. Type the number of the option you want and press **Enter**.

Main Menu example:

```
Main Menu
1. Animals
2. Feeds
3. Feed Events
4. Inventory
5. Sales
6. Personnel
0. Exit
```

Data is stored automatically in `farm.db` in the project folder.

---

## 📚 Menus & Commands (Quick Reference)

### Animals

* **Add Animal** — add tag, species, breed, DOB
* **View All Animals** — list animals and IDs
* **Find by ID / Tag** — look up an animal
* **Delete Animal** — remove an animal by ID

### Feeds

* **Add Feed** — name, unit (default `kg`), cost per unit, stock
* **List All Feeds** — show feeds and stock
* **Find by ID / Name**
* **Delete Feed**

### Feed Events

* **Record Feed Event** — link animal ID and feed ID, quantity, optional date
* **View Events for Animal** — feeding history for an animal
* **View Events for Feed** — feed usage history

### Inventory

* **Add Inventory Item** — name, category, quantity, unit (default `pcs`)
* **List Inventory**
* **Find Item by ID**
* **Delete Item**

### Sales

* **Record Sale** — product, quantity, unit price (total calculated)
* **List Sales**
* **Find Sale by ID**
* **Delete Sale**

### Personnel

* **Add Personnel** — name, role, salary
* **List Personnel**
* **Find by ID**
* **Delete Personnel**

---

## 🧾 Example Walkthrough

To add a feed called *Hay*:

1. From Main Menu → type `2` (Feeds) → Enter
2. Choose `1` (Add Feed)
3. When prompted:

   * `Feed name:` Hay
   * `Unit [kg]:` (press Enter for default)
   * `Cost per unit:` 5
   * `Stock quantity:` 100

You should see a confirmation like:

```
✅ Feed added: ID: 3 | Hay | Unit: kg | Cost/unit: 5.0 | Stock: 100
```

---

## 💾 Data Storage

* All records are saved to a local SQLite database file (`farm.db`).
* No internet required to run Agrimate.
* Use the `seed.py` script to populate demo data (optional).

---

## 🧩 Project Structure (typical)

```
agrimate/ or farm_cli_phase3/
├─ run.py
├─ seed.py
├─ Pipfile
├─ farm_cli/
│  ├─ models/
│  ├─ controllers/
│  └─ cli/ (menus and prompts)
└─ farm.db (created after first run)
```

---

## 🤝 Contributing & Support

* If you are a developer and want to improve Agrimate, feel free to fork the project, make changes, and suggest improvements.
* For feature requests or bug reports, include steps to reproduce and any error messages.

---

## 📞 Contact / Author

If you would like me to add an author block, contact info, or a project website, tell me what to include and I will update the README.

---

*Made with ❤️ for farmers — simple, local, and focused on doing the essentials well.*
