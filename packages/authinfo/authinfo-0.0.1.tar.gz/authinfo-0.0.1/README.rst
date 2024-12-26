########
authinfo
########


This module provides access to authentication credentials stored in
``.authinfo`` files.

``.authinfo`` files are based on ``.netrc`` files, and allow a bit more
flexibility.

They contain entries, formated as plain text, with ``key=${value}``
format fields.

``.authinfo`` files are multiprotocol and allow to do advanced matching.

``.authinfo`` files are typically encrypted using GPG, and this
library will invoke GPG to decrypt ``.authinfo.gpg`` files.


References:

- ``.netrc`` stuff:

  - https://linux.die.net/man/5/netrc
  - https://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-file.html

- ``.authinfo`` stuff:

  - https://www.emacswiki.org/emacs/GnusAuthinfo

