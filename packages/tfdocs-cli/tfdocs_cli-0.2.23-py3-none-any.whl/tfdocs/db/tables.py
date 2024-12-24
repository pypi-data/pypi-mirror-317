from sqlite3 import Cursor


def create_block_table(cursor: Cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS block (
            block_id TEXT PRIMARY KEY,
            block_type TEXT NOT NULL,
            block_name TEXT NOT NULL,
            parent_id TEXT DEFAULT NULL,
            FOREIGN KEY (parent_id) REFERENCES block(block_id)            
        );
    """
    )


def create_attribute_table(cursor: Cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS attribute (
            attribute_id INTEGER PRIMARY KEY AUTOINCREMENT,
            attribute_type TEXT NOT NULL,
            attribute_name TEXT NOT NULL,
            description TEXT,
            description_type TEXT,
		    optional BOOLEAN NOT NULL CHECK(optional IN (1, 0)),
		    computed BOOLEAN NOT NULL CHECK(computed IN (1, 0)),
            block_id TEXT NOT NULL,
            UNIQUE (block_id, attribute_name)
            FOREIGN KEY (block_id) REFERENCES block(block_id)            
        );
    """
    )
