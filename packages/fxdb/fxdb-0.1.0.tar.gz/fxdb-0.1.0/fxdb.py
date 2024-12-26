import sqlite3
from pathlib import Path
from datetime import datetime
import shutil
from contextlib import contextmanager


class fxdb:
    def __init__(self, path="fxdb"):
        """
        Initialize the database connection

        Args:
            path: Database path, can be a str or pathlib.Path object. If no suffix is provided, .db suffix will be added automatically.
                 Supported suffixes: .db, .sqlite3
        """
        self.db_path = Path(path)
        if self.db_path.suffix == "":
            self.db_path = self.db_path.with_suffix(".db")
        elif self.db_path.suffix not in [".db", ".sqlite3"]:
            raise ValueError("Database file must have a .db or .sqlite3 suffix")

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row  # Support returning results as dictionaries
        self.cur = self.conn.cursor()

    @contextmanager
    def transaction(self):
        """Provide a transaction context manager"""
        try:
            yield
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def __getitem__(self, tablename):
        """
        Support accessing table objects via db['tablename'].
        If the table does not exist, a table with only an id column will be created automatically.
        """
        if tablename not in self.tablenames:
            self.create(tablename)
        return Table(self, tablename)

    @property
    def tablenames(self):
        """Get all user-created table names"""
        self.cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        return [row["name"] for row in self.cur.fetchall()]

    def create(self, tablename, columns=None, id_column='id'):
        """
        Create a new table with support for defining multiple columns.

        Args:
            tablename: Name of the table to be created
            columns: Dictionary defining columns, e.g., {"name": "TEXT", "age": "INTEGER"}.
                     If None, only the default auto-increment primary key column will be created.
            id_column: Name of the primary key column, default is 'id'
        """
        table = Table(self, tablename, id_column)
        if columns is None:
            columns = {id_column: "INTEGER PRIMARY KEY AUTOINCREMENT"}
        else:
            columns = {id_column: "INTEGER PRIMARY KEY AUTOINCREMENT", **columns}

        column_definitions = ", ".join([f"{col} {dtype}" for col, dtype in columns.items()])
        with self.transaction():
            self.cur.execute(
                f"CREATE TABLE IF NOT EXISTS {tablename} ({column_definitions})"
            )
        return table

    def backup(self, backup_dir="database_backup", keep_num=5):
        """
        Backup the database

        Args:
            backup_dir: Backup directory, default is database_backup in the current directory
            keep_num: Number of backups to keep, default is 5
        """
        backup_path = Path(backup_dir)
        backup_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_backup = backup_path / f"{self.db_path.stem}_{timestamp}.db"
        shutil.copy2(self.db_path, new_backup)
        print(f"Database backed up to: {new_backup}")

        # Delete excess backups
        backups = sorted(backup_path.glob(f"{self.db_path.stem}_*.db"))
        for old_backup in backups[:-keep_num]:
            old_backup.unlink()
            print(f"Deleted old backup: {old_backup}")

    def __del__(self):
        """Close the database connection"""
        if hasattr(self, "conn"):
            self.conn.close()


class Table:
    def __init__(self, db, name, id_column='id'):
        self.db = db
        self.name = name
        self.id_column = id_column

    @property
    def columns(self):
        """Get all column names of the table"""
        self.db.cur.execute(f"PRAGMA table_info({self.name})")
        return [row["name"] for row in self.db.cur.fetchall()]

    def create_missing_columns(self, columns):
        """Batch check and create missing columns"""
        existing_columns = set(self.columns)
        missing_columns = {col: dtype for col, dtype in columns.items() if col not in existing_columns}
        with self.db.transaction():
            for col, dtype in missing_columns.items():
                self.db.cur.execute(f"ALTER TABLE {self.name} ADD COLUMN {col} {dtype}")
            if missing_columns:
                print(f"Added columns to table [{self.name}]: {', '.join(missing_columns.keys())}")

    def insert(self, **kwargs):
        """Before inserting data, dynamically check and create missing columns"""
        self.create_missing_columns({key: "TEXT" for key in kwargs.keys()})
        columns = ", ".join(kwargs.keys())
        placeholders = ", ".join(["?"] * len(kwargs))
        values = tuple(kwargs.values())
        with self.db.transaction():
            self.db.cur.execute(
                f"INSERT INTO {self.name} ({columns}) VALUES ({placeholders})", values
            )
    def insert_from_dict(self, data):
        """Insert data from a dictionary or a list of dictionaries
        
        Args:
            data: A single dictionary or a list of dictionaries. If the keys are inconsistent in the list, the union of all keys will be taken
        """
        if not data:
            return
            
        # Convert a single dictionary to a list
        if isinstance(data, dict):
            data = [data]
            
        # Get the union of all keys
        all_keys = set()
        for item in data:
            all_keys.update(item.keys())
            
        # Create missing columns
        self.create_missing_columns({key: "TEXT" for key in all_keys})
        
        # Batch insert data
        with self.db.transaction():
            try:
                # Prepare column names
                columns = ", ".join(all_keys)
                # Prepare placeholders for each row
                placeholders = ", ".join(["?"] * len(all_keys))
                
                # If the data size is less than 1000, insert all at once
                if len(data) <= 1000:
                    # Fill each data with None and flatten to a one-dimensional list
                    values = []
                    for item in data:
                        row_values = [item.get(key) for key in all_keys]
                        values.extend(row_values)
                    
                    # Construct SQL for multi-row insertion
                    multi_placeholders = "),(".join([placeholders] * len(data))
                    sql = f"INSERT INTO {self.name} ({columns}) VALUES ({multi_placeholders})"
                    
                    # Execute batch insertion
                    self.db.cur.execute(sql, values)
                else:
                    # Process data in batches, 1000 rows per batch
                    batch_size = 1000
                    for i in range(0, len(data), batch_size):
                        batch = data[i:i + batch_size]
                        # Fill each data with None and flatten to a one-dimensional list
                        values = []
                        for item in batch:
                            row_values = [item.get(key) for key in all_keys]
                            values.extend(row_values)
                        
                        # Construct SQL for multi-row insertion
                        multi_placeholders = "),(".join([placeholders] * len(batch))
                        sql = f"INSERT INTO {self.name} ({columns}) VALUES ({multi_placeholders})"
                        
                        # Execute batch insertion
                        self.db.cur.execute(sql, values)
            except Exception as e:
                # If any error occurs, the transaction will be rolled back automatically
                raise e

    def insert_from_df(self, df, include_index=False):
        """Insert data from a pandas DataFrame
        
        Args:
            df: pandas DataFrame object
            include_index: Whether to include the index column of the DataFrame, default is False.
                         If True, the index will be inserted as a column named 'index'
        """
        # If the index needs to be included
        if include_index:
            df = df.copy()
            df['index'] = df.index
            
        # Convert DataFrame to a list of dictionaries
        data = df.to_dict('records')
        # Insert data using insert_from_dict
        self.insert_from_dict(data)
        
    def _check_unique_constraint(self, keys, values):
        """Check and maintain unique constraints
        
        Args:
            keys: List of fields used to check uniqueness
            values: Dictionary of values to be checked
            
        Returns:
            str: Returns the index name
        """
        if not keys or not values:
            raise ValueError("keys and values must be specified")
            
        # Sort keys to maintain consistency
        sorted_keys = sorted(keys)
        
        # Construct index name
        index_name = f"idx_unique_{'_'.join(sorted_keys)}"
        
        # Check if the index exists
        self.db.cur.execute(f"""
        SELECT COUNT(*) FROM sqlite_master 
        WHERE type='index' AND name='{index_name}'
        """)

        if self.db.cur.fetchone()[0] == 0 :
            # Index does not exist, create a new index
            # Clear all existing indexes
            self.db.cur.execute(f"""
            SELECT name FROM sqlite_master 
            WHERE type='index' AND tbl_name='{self.name}'
            """)
            existing_indexes = self.db.cur.fetchall()
            print(existing_indexes)
            for idx in existing_indexes:
                self.db.cur.execute(f"DROP INDEX {idx[0]}")
            with self.db.transaction():
                # Delete duplicate records, keep the one with the largest id
                dup_fields = ','.join(sorted_keys)
                self.db.cur.execute(f"""
                DELETE FROM {self.name} 
                WHERE {self.id_column} NOT IN (
                    SELECT MAX({self.id_column}) 
                    FROM {self.name}
                    GROUP BY {dup_fields}
                )
                """)
                
                # Create unique index
                self.db.cur.execute(f"""
                CREATE UNIQUE INDEX {index_name} 
                ON {self.name}({','.join(sorted_keys)})
                """)
                
        return index_name

    def upsert(self, keys=None, **kwargs):
        """Insert or update data, dynamically check and create missing columns
        
        Args:
            keys: List of key fields used for upsert, the combination of these fields must be unique
            **kwargs: Fields and values to be inserted or updated
        """
        if not keys:
            raise ValueError("Key fields for upsert must be specified")
            
        # Create missing columns
        self.create_missing_columns({key: "TEXT" for key in kwargs.keys()})
        
        # Check and get the index name
        index_name = self._check_unique_constraint(keys, kwargs)
        
        columns = ", ".join(kwargs.keys())
        placeholders = ", ".join(["?"] * len(kwargs))
        values = tuple(kwargs.values())
        update_clause = ", ".join([f"{col}=excluded.{col}" for col in kwargs.keys() if col not in keys])
        conflict_clause = ", ".join(sorted(keys))
        
        try:
            with self.db.transaction():
                if len(values) <= 1000:
                    # If the data size is less than or equal to 1000, execute directly
                    self.db.cur.execute(
                        f"""
                        INSERT INTO {self.name} ({columns}) VALUES ({placeholders})
                        ON CONFLICT({conflict_clause}) DO UPDATE SET {update_clause}
                        """,
                        values,
                    )
                else:
                    # Process data in batches, 1000 rows per batch
                    batch_size = 1000
                    for i in range(0, len(values), batch_size):
                        batch_values = values[i:i + batch_size]
                        self.db.cur.execute(
                            f"""
                            INSERT INTO {self.name} ({columns}) VALUES ({placeholders})
                            ON CONFLICT({conflict_clause}) DO UPDATE SET {update_clause}
                            """,
                            batch_values,
                        )
        except Exception as e:
            # If any error occurs, the transaction will be rolled back automatically
            raise e
    def upsert_from_dict(self, data, keys=None):
        """Upsert data from a dictionary or a list of dictionaries
        
        Args:
            data: A single dictionary or a list of dictionaries
            keys: List of key fields used for upsert
        """
        if not data:
            return
            
        if isinstance(data, dict):
            data = [data]
            
        for item in data:
            self.upsert(keys=keys, **item)
            
    def upsert_from_df(self, df, keys=None, include_index=False):
        """Upsert data from a pandas DataFrame
        
        Args:
            df: pandas DataFrame object
            keys: List of key fields used for upsert
            include_index: Whether to include the index column of the DataFrame
        """
        if include_index:
            df = df.copy()
            df['idx'] = df.index.values
            
        data = df.to_dict('records')
        self.upsert_from_dict(data, keys=keys)

    def delete(self, **conditions):
        condition_clause = " AND ".join([f"{col}=?" for col in conditions.keys()])
        values = tuple(conditions.values())
        with self.db.transaction():
            self.db.cur.execute(
                f"DELETE FROM {self.name} WHERE {condition_clause}", values
            )

    def select(self, **conditions):
        condition_clause = " AND ".join([f"{col}=?" for col in conditions.keys()])
        values = tuple(conditions.values())
        self.db.cur.execute(
            f"SELECT * FROM {self.name} WHERE {condition_clause}", values
        )
        return [dict(row) for row in self.db.cur.fetchall()]

    def all(self):
        self.db.cur.execute(f"SELECT * FROM {self.name}")
        return [dict(row) for row in self.db.cur.fetchall()]

    def truncate(self):
        with self.db.transaction():
            self.db.cur.execute(f"DELETE FROM {self.name}")

    def drop(self):
        with self.db.transaction():
            self.db.cur.execute(f"DROP TABLE IF EXISTS {self.name}")


if __name__ == "__main__":
    pass