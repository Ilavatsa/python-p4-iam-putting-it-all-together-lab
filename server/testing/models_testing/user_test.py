import pytest
from sqlalchemy.exc import IntegrityError
from app import app
from models import db, User, Recipe

@pytest.fixture(scope='module')
def setup_app():
    '''Set up the Flask application context and create necessary tables.'''

    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app_test.db'
    with app.app_context():
        db.create_all()
        yield app  # Provide the fixture object
        db.session.remove()
        db.drop_all()

class TestUser:
    def setup_method(self, method):
        '''Ensure a clean state before each test method.'''

        with app.app_context():
            User.query.delete()
            db.session.commit()

    def test_has_attributes(self, setup_app):
        with app.app_context():
            user = User(
                username="Liz",
                image_url="https://prod-images.tcm.com/Master-Profile-Images/ElizabethTaylor.jpg",
                bio="""Dame Elizabeth Rosemond Taylor DBE (February 27, 1932""" + \
                    """ - March 23, 2011) was a British-American actress. """ + \
                    """She began her career as a child actress in the early""" + \
                    """ 1940s and was one of the most popular stars of """ + \
                    """classical Hollywood cinema in the 1950s. She then""" + \
                    """ became the world's highest paid movie star in the """ + \
                    """1960s, remaining a well-known public figure for the """ + \
                    """rest of her life. In 1999, the American Film Institute""" + \
                    """ named her the seventh-greatest female screen legend """ + \
                    """of Classic Hollywood cinema."""
            )
            user.password_hash = "whosafraidofvirginiawoolf"
            
            db.session.add(user)
            db.session.commit()

            created_user = User.query.filter_by(username="Liz").first()

            assert created_user.username == "Liz"
            assert created_user.image_url == "https://prod-images.tcm.com/Master-Profile-Images/ElizabethTaylor.jpg"
            assert created_user.bio == \
                """Dame Elizabeth Rosemond Taylor DBE (February 27, 1932""" + \
                """ - March 23, 2011) was a British-American actress. """ + \
                """She began her career as a child actress in the early""" + \
                """ 1940s and was one of the most popular stars of """ + \
                """classical Hollywood cinema in the 1950s. She then""" + \
                """ became the world's highest paid movie star in the """ + \
                """1960s, remaining a well-known public figure for the """ + \
                """rest of her life. In 1999, the American Film Institute""" + \
                """ named her the seventh-greatest female screen legend """ + \
                """of Classic Hollywood cinema."""
            
            with pytest.raises(AttributeError):
                created_user.password_hash

    def test_requires_username(self, setup_app):
        user = User()
        with pytest.raises(IntegrityError):
            db.session.add(user)
            db.session.commit()

    def test_requires_unique_username(self, setup_app):
        user_1 = User(username="Ben")
        user_2 = User(username="Ben")

        with pytest.raises(IntegrityError):
            db.session.add_all([user_1, user_2])
            db.session.commit()

    def test_has_list_of_recipes(self, setup_app):
        user = User(username="Prabhdip")

        recipe_1 = Recipe(
            title="Delicious Shed Ham",
            instructions="""Or kind rest bred with am shed then. In""" + \
                """ raptures building an bringing be. Elderly is detract""" + \
                """ tedious assured private so to visited. Do travelling""" + \
                """ companions contrasted it. Mistress strongly remember""" + \
                """ up to. Ham him compass you proceed calling detract.""" + \
                """ Better of always missed we person mr. September""" + \
                """ smallness northward situation few her certainty""" + \
                """ something.""",
            minutes_to_complete=60,
        )
        recipe_2 = Recipe(
            title="Hasty Party Ham",
            instructions="""As am hastily invited settled at limited""" + \
                         """ civilly fortune me. Really spring in extent""" + \
                         """ an by. Judge but built gay party world. Of""" + \
                         """ so am he remember although required. Bachelor""" + \
                         """ unpacked be advanced at. Confined in declared""" + \
                         """ marianne is vicinity.""",
            minutes_to_complete=30,
        )

        user.recipes.append(recipe_1)
        user.recipes.append(recipe_2)

        db.session.add_all([user, recipe_1, recipe_2])
        db.session.commit()

        assert user.id
        assert recipe_1.id
        assert recipe_2.id

        assert recipe_1 in user.recipes
        assert recipe_2 in user.recipes
