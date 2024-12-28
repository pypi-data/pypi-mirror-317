"""passlib3.ext.django.models -- monkeypatch django hashing framework

this plugin monkeypatches django's hashing framework
so that it uses a passlib3 context object, allowing handling of arbitrary
hashes in Django databases.
"""
