# -*- coding: utf-8 -*-
from collective.contentcreator import create_item_runner
from collective.contentcreator import load_json
from random import randint
from zope.component.hooks import getSite


max_items = 0
cnt_items = 0

def create_thread():
    global max_items
    global cnt_items

    max_items = randint(1, 40)
    cnt_items = 0

    def _create(subtree, type_):
        global cnt_items

        for cnt in range(1 if not cnt_items else 0, 3):

            if cnt_items >= max_items:
                break

            cnt_items += 1

            item = {
                '@type': type_,
                'title': u'test',
                'text': u'abc',
                'items': []
            }

            if cnt_items < max_items:
                _create(item['items'], 'Contribution')

            subtree.append(item)

    tree = []
    _create(tree, 'Case')
    _create(tree, 'Case')
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
