import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed, id=None):
        """Initialize a Dog instance with name, breed, and optional id."""
        self.name = name
        self.breed = breed
        self.id = id

    @classmethod
    def create_table(cls):
        """Create the dogs table if it doesn't exist."""
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the dogs table if it exists."""
        sql = "DROP TABLE IF EXISTS dogs"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """Save the Dog instance to the database."""
        if self.id is None:
            # Insert new record
            sql = "INSERT INTO dogs (name, breed) VALUES (?, ?)"
            CURSOR.execute(sql, (self.name, self.breed))
            CONN.commit()
            self.id = CURSOR.lastrowid
        else:
            # Update existing record
            self.update()
        return self

    @classmethod
    def create(cls, name, breed):
        """Create a new Dog instance and save it to the database."""
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        """Create a Dog instance from a database row."""
        # row is expected to be a tuple: (id, name, breed)
        return cls(name=row[1], breed=row[2], id=row[0])

    @classmethod
    def get_all(cls):
        """Return a list of Dog instances for all records in the database."""
        sql = "SELECT * FROM dogs"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        """Find and return a Dog instance by name."""
        sql = "SELECT * FROM dogs WHERE name = ? LIMIT 1"
        row = CURSOR.execute(sql, (name,)).fetchone()
        if row:
            return cls.new_from_db(row)
        return None

    @classmethod
    def find_by_id(cls, id):
        """Find and return a Dog instance by ID."""
        sql = "SELECT * FROM dogs WHERE id = ? LIMIT 1"
        row = CURSOR.execute(sql, (id,)).fetchone()
        if row:
            return cls.new_from_db(row)
        return None

    # Bonus Methods

    @classmethod
    def find_or_create_by(cls, name, breed):
        """Find a dog by name and breed, or create it if it doesn't exist."""
        sql = "SELECT * FROM dogs WHERE name = ? AND breed = ? LIMIT 1"
        row = CURSOR.execute(sql, (name, breed)).fetchone()
        
        if row:
            return cls.new_from_db(row)
        else:
            return cls.create(name, breed)

    def update(self):
        """Update the dog's record in the database."""
        sql = "UPDATE dogs SET name = ?, breed = ? WHERE id = ?"
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()
