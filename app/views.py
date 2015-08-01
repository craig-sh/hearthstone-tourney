from app import app
from .models import Region


@app.route('/')
@app.route('/index')
def index():
    regions = Region.query.all()
    return 'Hello, World' + str(regions)
