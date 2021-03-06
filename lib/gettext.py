# This file is part of MyPaint.
# Copyright (C) 2015 by Andrew Chadwick <a.t.chadwick@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from __future__ import absolute_import

"""Function equivalents of (GLib) gettext's C macros.

Recommended usage:

  >>> from lib.gettext import C_
  >>> from lib.gettext import ngettext

Also supported, but mildly deprecated (consider C_ instead!):

  >>> from lib.gettext import gettext as _

Lots of older code uses ``from gettext import gettext as _``.
Don't do that in new code: pull in this module as ``lib.gettext``.
Importing this module should still work from within lib/ if code
still uses a relative import, however.

"""

from warnings import warn
from gi.repository import GLib


# Older code in lib imports these as "from gettext import gettext as _".
# Pull them in for backwards compat.
# Might change these to _Glib.dgettext/ngettext instead.

from gettext import gettext
from gettext import ngettext


# Newer code should use C_() even for simple cases, and provide contexts
# for translators.

def C_(context, msgid):
    """Translated string with supplied context.

    Convenience wrapper around g_dpgettext2. It's a function not a
    macro, but use it as if it was a C macro only.

    """
    g_dpgettext2 = GLib.dpgettext2
    try:
        result = g_dpgettext2(None, context, msgid)
    except TypeError as e:
        # Expect "Argument 0 does not allow None as a value" sometimes.
        # This is a known problem with Ubuntu Server 12.04 when testing
        # lib - that version of g_dpgettext2() does not appear to allow
        # NULL for its first arg.
        wtmpl = "C_(): g_dpgettext2() raised %r. Try a newer GLib?"
        warn(
            wtmpl % (e,),
            RuntimeWarning,
            stacklevel = 1,
        )
        result = msgid
    return result
