# -*- coding: utf-8 -*-
"""Init and utils."""

# NO ARCHETYPES CHECKER
try:
    import Products.Archetypes

    Products.Archetypes
except ImportError:
    pass
else:
    raise RuntimeError("Archetypes detected")
