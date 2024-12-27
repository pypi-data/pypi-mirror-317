from elements.core import request, chevron_template, TemplateError, TEMPLATE_PATH, abort, Timestamp
from elements.sessions.utilities import session
from elements.notes import Note
from pathlib import Path

# The 'edit' action is used to generate a new Note
# element in a directory corresponding to the given 
# path. 

# A GET request will return any template found at
# the relevant location (forms/comment) or a
# minimal HTML form for the comment.

# A POST request will make the Note and return it
# in the relevant template (components/comment)
# if one exists. Otherwise the flattened data will 
# be returned.

def edit(*args, **kwargs):
    s = session()
    if s is None:
        return abort(401)

    defaults = kwargs['defaults']
    tag = kwargs.get('tag') or ""
    db = kwargs.get('db')

    if len(args) < 1 or args[0] == None:
        return abort(500, "Can't edit an empty element")

    el = args[0]

    if request.method == "GET":
        template = Path(tag, 'forms', 'edit').with_suffix('.mo')

        try:
            data = { **request.query, 'session': s, 'element': el }
            return chevron_template(str(template), **defaults(data))

        except TemplateError as e:
            return f'''<form method="POST" action="{ el.url }edit">
                <textarea name="content">{ el.content }</textarea>
                <br/>
                <input type="submit" value="Send" />
            </form>'''

    elif request.method == "POST":
        
        # This is an incomplete solution - needs to account for
        # tags as well as content dictionaries
        if isinstance(el.content, dict):
            el.content.update(request.forms.dict)
        else:
            el.content = request.forms.get('content') or el.content

        el.ts = Timestamp()

        template = Path(tag, 'components', el.directory).with_suffix('.mo')

        try:
            data = { 'session': s, 'data': el }
            return chevron_template(str(template), **defaults(data))

        except TemplateError as t:
            print('Could not render template:', t)
            return el.flatten()

            
            


