# -*- coding: utf-8 -*-
from collective.contentcreator import create_item_runner
from collective.contentcreator import load_json
from random import choice
from random import randint
from zope.component.hooks import getSite


import loremipsum


max_items = 0
cnt_items = 0
max_depth = 0


def create_thread():
    global max_items
    global cnt_items

    max_items = randint(1, 40)
    cnt_items = 0


    def _create(subtree, type_, depth=0):
        global cnt_items
        global max_depth

        choices = [1, 1, 2, 2, 3, 4]
        if cnt_items:
            choices += [0, 0, 0]
        for cnt in range(choice(choices)):

            if type_ == 'Case':
                max_depth = randint(1, 6)

            if depth>max_depth:
                break

            depth += 1

            if cnt_items >= max_items:
                break

            cnt_items += 1

            txt = []
            for cnt in range(randint(1, 4)):
                txt_ = loremipsum.get_paragraph()
                if cnt == 0:
                    txt_ = u'<p><strong>{0}</strong></p>'.format(txt_)
                elif cnt == 1:
                    txt_ = '<p><em>{0}</em></p>'.format(txt_)
                else:
                    txt_ = '<p>{0}</p>'.format(txt_)
                txt.append(txt_)

            item = {
                '@type': type_,
                'title': loremipsum.get_sentence(),
                'text': '\n'.join(txt),
                'items': [],
            }

            if cnt_items < max_items:
                _create(item['items'], 'Contribution')

            subtree.append(item)

    tree = []
    _create(tree, 'Case')

    return tree



def example_content(context):
    # content_structure = load_json('example_content.json', __file__)

    create_item_runner(
        getSite().cases,  # "Cases" is aleady created.
        create_thread(),
        default_lang='de',
        default_wf_action='publish'
    )
