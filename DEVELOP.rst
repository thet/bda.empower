Using the development buildout
------------------------------

Create a virtualenv in the package::

    $ virtualenv --clear .

Install requirements with pip::

    $ ./bin/pip install -r requirements.txt

Run buildout::

    $ ./bin/buildout

Start Plone in foreground::

    $ ./bin/instance fg

It is possible to create a set of testusers.
Follow the startup as below.
Then the GenericSetup need to be re-run again or a fresh site need to be created.

To start with testusers enabled (users will be printed out on startup and share all the same password)::

    $ TESTUSER=1 ./bin/instance fg

To start with testusers and custom password::

    $ TESTUSER=1 TESTPASSWORD=verysecret ./bin/instance fg
