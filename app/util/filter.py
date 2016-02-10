from ..app import app

@app.template_filter('format_date')
def format_date(date, format='%Y-%m-%d %H:%M'):
    return '{0:{1}}'.format(date, format)
