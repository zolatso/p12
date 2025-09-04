---

## Prerequisites

1. **Python** (3.8 or higher recommended)  
2. **MySQL** (installed locally)  
3. **Virtual environment with dependencies**  

Create and activate a virtual environment, then install dependencies from `requirements.txt`:

```
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

pip install -r requirements.txt
```

## Installation & Setup

-----

### Step 1: Access MySQL

Once installed, access MySQL in the terminal:

```
mysql -u root -p
```

You will have created this password during the MySQL installation process.

-----

### Step 2: Create the Database

Inside the MySQL prompt, create a new database named `project12`:

```sql
CREATE DATABASE project12;
```

-----

### Step 3: Set Environment Variables

Two environment variables are required:

  * **`DB_PASSWORD`**: Provides limited access to the database (does not permit table creation).
  * **`DB_ROOT_PASSWORD`**: Provides root access.

For testing purposes, it may be simpler to use your root account.

#### Linux/Mac (bash/zsh)

```bash
export DB_PASSWORD=your_db_password
export DB_ROOT_PASSWORD=your_root_password
```

To make these permanent, add the lines above to your `~/.bashrc` or `~/.zshrc` file.

#### Windows (Command Prompt)

```batch
set DB_PASSWORD=your_db_password
set DB_ROOT_PASSWORD=your_root_password
```

#### Windows (PowerShell)

```powershell
$env:DB_PASSWORD="your_db_password"
$env:DB_ROOT_PASSWORD="your_root_password"
```

-----

### Step 4: Configure Database Connection

In `db/__init__.py`, you will find the following line:

```python
engine = db_connect(root=True)
```

This controls whether you connect to the database as **root** (`True`) or a standard user (`False`). You **must** be connected as root to initialize the tables.

-----

### Step 5: Initialize the Tables

In `main.py`, temporarily replace the line `cli_main()` with:

```python
recreate_initial_db()
```

Then, run the following command:

```bash
python main.py
```

This will create the tables and include some basic user accounts, roles, and permissions. Once this is complete, change the line `recreate_initial_db()` back to `cli_main()`.

-----

### Step 6: Using the Application

The application is now ready to use. For instructions, refer to the built-in help functions:

```bash
python main.py --help          # overall help
python main.py user --help     # user management help
python main.py client --help   # client management help
python main.py contract --help # contract management help
python main.py event --help    # event management help
```