from elements.core import request, chevron_template, TemplateError, abort
from elements.sessions.utilities import session
from elements.posts import Post
from pathlib import Path

def post(*args, **kwargs):
    s = session()
    if s is None:
        return abort(401)

    defaults = kwargs['defaults']
    tag = kwargs.get('tag') or ""
    db = kwargs.get('db')

    if request.method == "GET":
        template = Path(tag, 'forms', 'post').with_suffix('.mo')

        try:
            data = { **request.query, 'session': s }
            return chevron_template(str(template), **defaults(data))
        
        except TemplateError as e:
            return '<p>No form available</p>'
        # Return new post form

    elif request.method == "POST":
        p = Post(**request.forms, author=s.member)
        img = request.files.get('img')
        if img:
            p.attach(img, thumbnail=(300, 300))

        # This would be 'posts', but this time it's 'art'
        p.save(path=Path('art', s.member.name))
        db.posts.add(p)

        template = Path(tag, 'components', 'post').with_suffix('.mo')

        try:
            # TODO - Mappable elements
            data = { **request.query, 'session': s, 'data': p }
            return chevron_template(str(template), **defaults(data))

        except TemplateError:
            # TODO - fix this
            return f'<section class="pane"><img src="{p.first_media.preview_url}"></section>'
            return p.flatten()

