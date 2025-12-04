from lib import CONN, CURSOR

class Dog:
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    # -------------------------
    # TABLE METHODS
    # -------------------------

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            );
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS dogs;")
        CONN.commit()

    # -------------------------
    # INSTANCE METHODS
    # -------------------------

    def save(self):
        """Insert new row OR update existing."""
        if self.id is None:
            sql = "INSERT INTO dogs (name, breed) VALUES (?, ?)"
            CURSOR.execute(sql, (self.name, self.breed))
            CONN.commit()
            self.id = CURSOR.lastrowid
        else:
            sql = "UPDATE dogs SET name=?, breed=? WHERE id=?"
            CURSOR.execute(sql, (self.name, self.breed, self.id))
            CONN.commit()
        return self

    def update(self):
        """Force update an existing row."""
        sql = "UPDATE dogs SET name = ?, breed = ? WHERE id = ?"
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()

    # -------------------------
    # CLASS CONSTRUCTORS
    # -------------------------

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        """Convert DB row -> Dog instance."""
        return cls(id=row[0], name=row[1], breed=row[2])

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM dogs"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM dogs WHERE name = ? LIMIT 1"
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.new_from_db(row) if row else None

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM dogs WHERE id = ? LIMIT 1"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.new_from_db(row) if row else None

    # -------------------------
    # BONUS
    # -------------------------

    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = "SELECT * FROM dogs WHERE name=? AND breed=? LIMIT 1"
        row = CURSOR.execute(sql, (name, breed)).fetchone()

        if row:
            return cls.new_from_db(row)
        else:
            dog = cls(name, breed)
            dog.save()
            return dog

