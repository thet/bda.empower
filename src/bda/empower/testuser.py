# -*- coding: utf-8 -*-
from plone import api

import os

INSTALL_TEST_USERS = os.environ.get('TESTUSER', False)

TEST_PW = os.environ.get('TESTPASSWORD', "empower!me")

INIT_USERS = [
    {
        "email": "admin@empower-help.net",
        "username": "empower_admin",
        "password": TEST_PW,
        "roles": ("Member", "Manager"),
        "properties": {
            "fullname": "Adele Ming",
            "description": "Administratorin",
        },
    },
    {
        "email": "coord1@empower-help.net",
        "username": "empower_coordinator_1",
        "password": TEST_PW,
        "roles": ("Member", "Coordinator"),
        "properties": {
            "fullname": "Cordula Nator",
            "description": "Koordinatiorin 1",
        },
    },
    {
        "email": "coord2@empower-help.net",
        "username": "empower_coordinator_2",
        "password": TEST_PW,
        "roles": ("Member", "Coordinator"),
        "properties": {
            "fullname": "Cornelius Radiator",
            "description": "Koordinatior 2",
        },
    },
    {
        "email": "client1@empower-help.net",
        "username": "empower_client_1",
        "password": TEST_PW,
        "roles": ("Member", "Client"),
        "properties": {
            "fullname": "Clint Westlawn",
            "description": "Klient 1",
        },
    },
    {
        "email": "client2@empower-help.net",
        "username": "empower_client_2",
        "password": TEST_PW,
        "roles": ("Member", "Client"),
        "properties": {
            "fullname": "Clinisha Betro",
            "description": "Klientin 2",
        },
    },
    {
        "email": "expert1@empower-help.net",
        "username": "empower_expert_1",
        "password": TEST_PW,
        "roles": ("Member", "Expert"),
        "properties": {
            "fullname": "Experina Artel",
            "description": "Expertin 1",
        },
    },
    {
        "email": "expert2@empower-help.net",
        "username": "empower_expert_2",
        "password": TEST_PW,
        "roles": ("Member", "Expert"),
        "properties": {
            "fullname": "Exander Pertl",
            "description": "Experte 2",
        },
    },
    {
        "email": "expert3@empower-help.net",
        "username": "empower_expert_3",
        "password": TEST_PW,
        "roles": ("Member", "Expert"),
        "properties": {
            "fullname": "Expeditus Mayr",
            "description": "Experte 3",
        },
    },
]


def install_test_users():
    if not INSTALL_TEST_USERS:
        return
    for record in INIT_USERS:
        try:
            api.user.create(**record)
        except ValueError:
            # this happens if the user already exists, i.e. onm reinstall.
            pass


if INSTALL_TEST_USERS:
    print("=" * 80)
    print("Activating Potential Test Users With Password \n")
    print("    {0}\n".format(TEST_PW))
    for record in INIT_USERS:
        print(
            " - {0} ({1})".format(
                record["email"], record["properties"]["description"]
            )
        )
    print("=" * 80)
