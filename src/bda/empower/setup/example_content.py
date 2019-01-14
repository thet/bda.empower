# -*- coding: utf-8 -*-
from .setupdevusers import DEV_USERS
from bda.empower import discourse
from collective.contentcreator import create_item_runner
from collective.contentcreator import load_json
from Products.CMFPlone.utils import safe_unicode
from zope.component.hooks import getSite

import loremipsum
import plone.api
import random


def create_text():
    txt = []
    cnt_bold = random.randint(1, 4)
    cnt_italic = random.randint(1, 4)
    for cnt in range(random.randint(1, 4)):
        txt_ = loremipsum.get_paragraph()
        if cnt == cnt_italic:
            txt_ = u"<em>{0}</em>".format(txt_)
        if cnt == cnt_bold:
            txt_ = u"<strong>{0}</strong>".format(txt_)
        txt_ = u"<p>{0}</p>".format(txt_)
        txt.append(txt_)
    return "\n".join(txt)


def create_content():
    cases = []
    for it in range(4):
        cases.append(create_case())
    return cases


def create_case():
    wsdefs = discourse.get_workspace_definitions()
    workspace = wsdefs.keys()[0]

    users = plone.api.user.get_users()
    users = map(lambda it: it.id, users)
    random.shuffle(users)
    client = users.pop()
    coordinator = users.pop()

    item = {
        "@type": "Case",
        "title": loremipsum.get_sentence(),
        "text": create_text(),
        "items": create_thread(workspace, users),
        "workspace": workspace,
        "client": safe_unicode(client),
        "coordinators": safe_unicode(coordinator),
        "expert_pool": u';'.join(users),
        "creators": safe_unicode(coordinator),
    }

    return item


def create_thread(current_workspace, expert_pool):

    workspace_definitions = discourse.get_workspace_definitions()

    def _create(parent_workspace, expert_pool, cnt, max_cnt, depth, max_depth):
        depth += 1
        if depth > max_depth:
            return []

        thread = []

        for _cnt in range(random.randint(2, 6)):  # min 2 answers per thread

            cnt += 1
            if cnt > max_cnt:
                return thread

            _current_workspace = parent_workspace
            experts_assigned = None
            if random.choice([1, 2, 3]) == 1:
                _current_workspace = random.choice(
                    workspace_definitions[parent_workspace]['next']
                )
                experts_assigned = random.sample(
                    expert_pool,
                    random.randint(1, 3)
                )

            item = {
                "@type": "Contribution",
                "title": loremipsum.get_sentence(),
                "text": create_text(),
                "items": _create(
                    _current_workspace,
                    expert_pool,
                    cnt,
                    max_cnt,
                    depth,
                    max_depth
                ),
                "workspace": _current_workspace,
                "creators": safe_unicode(random.choice(expert_pool)),
            }
            if experts_assigned:
                item['experts_assigned'] = u';'.join(experts_assigned)

            thread.append(item)

        return thread

    thread = _create(
        current_workspace,
        expert_pool,
        0,
        10,
        0,
        random.randint(4, 6)
    )
    return thread


def example_content(context):

    for record in DEV_USERS:
        try:
            plone.api.user.create(**record)
        except ValueError:
            # user already exists.
            pass

    # content_structure = load_json('example_content.json', __file__)
    create_item_runner(
        getSite().cases,  # "Cases" is aleady created.
        create_content(),
        default_lang="de",
        default_wf_action="publish",
    )
