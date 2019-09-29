# -*- coding: utf-8 -*-
"""Init and utils."""

# Raise batch size to almost unlimited.
# We do not want to deal with context.items batching YET.
import plone.restapi.batching
plone.restapi.batching.DEFAULT_BATCH_SIZE = 10000

# NO ARCHETYPES CHECKER
try:
    import Products.Archetypes

    Products.Archetypes
except ImportError:
    pass
else:
    raise RuntimeError("Archetypes detected")
