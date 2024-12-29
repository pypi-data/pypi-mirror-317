import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.models import Human
from db.db_connection import create_session

def get_fake_human_for_stats(session):
    first_name = "Fake"
    middle_name = "Stats"
    last_name = "Human"

    # Check if the human already exists
    existing_human = session.query(Human).filter_by(first_name=first_name, middle_name=middle_name, last_name=last_name).first()
    if existing_human:
        return existing_human.id

    # Create a new human
    human = Human(first_name=first_name, middle_name=middle_name, last_name=last_name)
    session.add(human)
    session.commit()  # Commit to get the human.id

    return human.id