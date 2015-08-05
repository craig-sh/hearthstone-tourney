from app import app
from .models import Region, City


@app.route('/')
@app.route('/index')
def index():
    regions = Region.query.all()
    res = ''
    for region in regions:
        res += repr(region)
        res += '\n'
        print(City.query.filter_by(region_id=1).all())
        for city in City.query.filter_by(region_id=region.id).all():
            res += repr(city) + '||'
        res += '=========================\n\n'
    return res
