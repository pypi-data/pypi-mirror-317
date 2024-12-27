from elements.core import request, chevron_template, TemplateError, TEMPLATE_PATH, abort
from elements.sessions.utilities import session
from elements.notes import Note
from pathlib import Path

# The 'comment' action is used to generate a new Note
# element in a directory corresponding to the given 
# path. 

# A GET request will return any template found at
# the relevant location (forms/comment) or a
# minimal HTML form for the comment.

# A POST request will make the Note and return it
# in the relevant template (components/comment)
# if one exists. Otherwise the flattened data will 
# be returned.

def comment(*args, **kwargs):
    s = session()
    if s is None:
        return abort(401)

    defaults = kwargs['defaults']
    tag = kwargs.get('tag') or ""
    db = kwargs.get('db')

    if len(args) >= 1:
        path = args[0]
    else:
        path = ""
    
    if request.method == "GET":
        template = Path(tag, 'forms', 'comment').with_suffix('.mo')

        try:
            data = { **request.query, 'session': s }
            return chevron_template(str(template), **defaults(data))

        except TemplateError as e:
            return f'''<form method="POST" action="comment">
                <textarea name="content"></textarea>
                <input type="submit" value="Send" />
            </form>'''

    elif request.method == "POST":
        n = Note(**request.forms, author=s.member)
        save_destination = Path('notes', path)

        n.save(path=save_destination)

        # Should this be a property of Note? Probably not
        n.delete = True

        # This should probably happen automatically with the 'save'?
        db.notes.add(n)

        template = Path(tag, 'components', 'comment').with_suffix('.mo')

        try:
            data = { **request.query, 'session': s, 'data': n }
            return chevron_template(str(template), **defaults(data))

        except TemplateError:
            return n.flatten()

            
            


