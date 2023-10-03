# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .author import author_views
from .publication import publication_views

views = [user_views, index_views, auth_views, publication_views, author_views] 

# blueprints must be added to this list