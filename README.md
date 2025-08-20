# Install the app dependencies
```bash
pip install -r requirements. txt
```

# Run the app
```shell 
.venv/Scripts/activate
```

# Check if ON DELETE CASCADE  CONSTRAINT is present
```bash
echo "PRAGMA foreign_key_list(carts);" | sqlite3 market_hall.db
```