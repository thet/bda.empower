# -*- coding: utf-8 -*-
from plone import api

import os


INSTALL_DEV_USERS = os.environ.get("DEVUSER", False)

DEV_PW = os.environ.get("DEVPASSWORD", "empower!me")

DEV_USERS = [
    {
        "email": "admin@empower-help.net",
        "username": "empower_admin",
        "password": DEV_PW,
        "roles": ("Member", "Site Administrator", "Editor", "Contributor"),
        "properties": {
            "fullname": "Adele Ming",
            "description": "Administratorin",
        },
    },
    {
        "email": "coord1@empower-help.net",
        "username": "empower_coordinator_1",
        "password": DEV_PW,
        "roles": ("Member", "Editor", "Contributor"),
        "properties": {
            "fullname": "Cordula Nator",
            "description": "Koordinatiorin 1",
        },
    },
    {
        "email": "coord2@empower-help.net",
        "username": "empower_coordinator_2",
        "password": DEV_PW,
        "roles": ("Member", "Editor", "Contributor"),
        "properties": {
            "fullname": "Cornelius Radiator",
            "description": "Koordinatior 2",
        },
    },
    {
        "email": "client1@empower-help.net",
        "username": "empower_client_1",
        "password": DEV_PW,
        "roles": ("Member",),
        "properties": {
            "fullname": "Clint Westlawn",
            "description": "Klient 1",
        },
    },
    {
        "email": "client2@empower-help.net",
        "username": "empower_client_2",
        "password": DEV_PW,
        "roles": ("Member",),
        "properties": {
            "fullname": "Clinisha Betro",
            "description": "Klientin 2",
        },
    },
    {
        "email": "expert1@empower-help.net",
        "username": "empower_expert_1",
        "password": DEV_PW,
        "roles": ("Member",),
        "properties": {
            "fullname": "Experina Artel",
            "description": "Expertin 1",
        },
    },
    {
        "email": "expert2@empower-help.net",
        "username": "empower_expert_2",
        "password": DEV_PW,
        "roles": ("Member",),
        "properties": {
            "fullname": "Exander Pertl",
            "description": "Experte 2",
        },
    },
    {
        "email": "expert3@empower-help.net",
        "username": "empower_expert_3",
        "password": DEV_PW,
        "roles": ("Member",),
        "properties": {
            "fullname": "Expeditus Mayr",
            "description": "Experte 3",
        },
    },
]


def create_dev_users():
    if not INSTALL_DEV_USERS:
        return
    for record in DEV_USERS:
        try:
            api.user.create(**record)
        except ValueError:
            # this happens if the user already exists, i.e. onm reinstall.
            pass


if INSTALL_DEV_USERS:
    print("=" * 80)
    print("Activating Potential DEV Users With Password \n")
    print("    {0}\n".format(DEV_PW))
    for record in DEV_USERS:
        print(
            " - {0} ({1})".format(
                record["email"], record["properties"]["description"]
            )
        )
    print("=" * 80)
