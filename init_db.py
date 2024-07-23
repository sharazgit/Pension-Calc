from database import PensionDatabase

def init_db():
    db = PensionDatabase()

    # Add sample DB schemes
    db.add_db_scheme("Standard DB Scheme", 0.0167, 65)  # 1/60th accrual, NRA 65
    db.add_db_scheme("Generous DB Scheme", 0.0200, 60)  # 1/50th accrual, NRA 60

    # Add sample DC schemes
    db.add_dc_scheme("Basic DC Scheme", 0.05)  # 5% contribution
    db.add_dc_scheme("Enhanced DC Scheme", 0.10)  # 10% contribution

    db.close()

if __name__ == "__main__":
    init_db()