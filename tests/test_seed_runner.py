"""Test seed runner for idempotency and data validation."""

import os
import sys
from pathlib import Path
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import Base, User, Client, Case, PropertyOpinion
from scripts.seed_via_models import seed_data as run_seed

# Use tmp_seed.db for testing
TEST_DB = "sqlite:///./tmp_seed.db"

@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    """Set up test database before any tests run."""
    os.environ["DATABASE_URL"] = TEST_DB
    # Create tables first
    engine = create_engine(TEST_DB, echo=False)
    Base.metadata.create_all(bind=engine)
    engine.dispose()
    yield
    # Cleanup at end
    
@pytest.fixture(scope="module")
def engine():
    """Create test database engine."""
    engine = create_engine(TEST_DB, echo=False)
    yield engine
    engine.dispose()

@pytest.fixture
def session(engine):
    """Create test database session."""
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_seed_creates_expected_data(session):
    """Test that seed runner creates expected rows."""
    # Run seed for the first time
    result = run_seed()
    assert result == 0, "Seed runner should return 0 on success"
    
    # Verify expected data
    user_count = session.query(User).count()
    client_count = session.query(Client).count()
    case_count = session.query(Case).count()
    opinion_count = session.query(PropertyOpinion).count()
    
    assert user_count >= 2, f"Expected at least 2 users, got {user_count}"
    assert client_count >= 2, f"Expected at least 2 clients, got {client_count}"
    assert case_count >= 1, f"Expected at least 1 case, got {case_count}"
    assert opinion_count >= 1, f"Expected at least 1 property opinion, got {opinion_count}"
    
    # Verify user emails
    amit = session.query(User).filter_by(email="amit.sharma@legalindia.ai").first()
    priya = session.query(User).filter_by(email="priya.patel@legalindia.ai").first()
    
    assert amit is not None, "User Amit Sharma should exist"
    assert priya is not None, "User Priya Patel should exist"
    assert amit.role == "lawyer", "Amit should be a lawyer"
    assert priya.role == "lawyer", "Priya should be a lawyer"

def test_seed_idempotency(session):
    """Test that running seed twice doesn't duplicate data."""
    # Get counts after first seed
    user_count_1 = session.query(User).count()
    client_count_1 = session.query(Client).count()
    case_count_1 = session.query(Case).count()
    opinion_count_1 = session.query(PropertyOpinion).count()
    
    # Run seed again
    result = run_seed()
    assert result == 0, "Second seed run should also succeed"
    
    # Get counts after second seed
    session.expire_all()  # Clear session cache
    user_count_2 = session.query(User).count()
    client_count_2 = session.query(Client).count()
    case_count_2 = session.query(Case).count()
    opinion_count_2 = session.query(PropertyOpinion).count()
    
    # Counts should be identical (idempotent)
    assert user_count_1 == user_count_2, f"User count changed: {user_count_1} -> {user_count_2}"
    assert client_count_1 == client_count_2, f"Client count changed: {client_count_1} -> {client_count_2}"
    assert case_count_1 == case_count_2, f"Case count changed: {case_count_1} -> {case_count_2}"
    assert opinion_count_1 == opinion_count_2, f"Opinion count changed: {opinion_count_1} -> {opinion_count_2}"
    
    print(f"\nIdempotency verified - Users: {user_count_2}, Clients: {client_count_2}, "
          f"Cases: {case_count_2}, Property Opinions: {opinion_count_2}")

def test_cleanup():
    """Clean up temporary database file."""
    db_path = Path("./tmp_seed.db")
    if db_path.exists():
        db_path.unlink()
        print("\nCleaned up tmp_seed.db")

