import pytest
from sqlalchemy.exc import IntegrityError
from app import app, db  # Import app and db from your application's main module
from models import Recipe  # Import your models to be tested

@pytest.fixture(scope='module')
def setup_app():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_app.db'  # Use a separate test database
    if not app.extensions.get('sqlalchemy'):
        db.init_app(app)
    with app.app_context():
        db.create_all()

    yield app  # Provide the fixture

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(setup_app):
    return setup_app.test_client()

class TestRecipe:
    def test_has_attributes(self, setup_app):
     with setup_app.app_context():
        # Create a recipe
        recipe = Recipe(
            title="Delicious Shed Ham",
            instructions="Long instructions here... and some more text to meet the 50 character minimum",
            minutes_to_complete=60
        )
        db.session.add(recipe)
        db.session.commit()

    def test_requires_title(self, setup_app):
        with setup_app.app_context():
            with pytest.raises(IntegrityError):
                # Attempt to add a recipe without a title (which should raise IntegrityError)
                recipe = Recipe()
                db.session.add(recipe)
                db.session.commit()

    def test_requires_50_plus_char_instructions(self, setup_app):
        with setup_app.app_context():
            with pytest.raises(IntegrityError):
                # Attempt to add a recipe with less than 50 characters in instructions
                recipe = Recipe(
                    title="Generic Ham",
                    instructions="Short instructions"
                )
                db.session.add(recipe)
                db.session.commit()

