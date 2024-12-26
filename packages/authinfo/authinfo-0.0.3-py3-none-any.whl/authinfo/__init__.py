#!/usr/bin/env python
# SPDX-FileCopyrightText: 2024 Jérôme Carretero <cJ-authinfo@zougloub.eu> & contributors
# SPDX-License-Identifier: MIT
# .authinfo management

__version__ = "0.0.3"

import logging
import os
import re


logger = logging.getLogger(__name__)


default_candidates = [os.path.expanduser(_) for _ in ["~/.authinfo", "~/.authinfo.gpg"]]


def parse(text: str):
	"""
	"""
	entries = list()
	entry = dict() # pending entry
	word = None # pending entry word (key or value)
	quoting = False
	escaped = False
	k = None # pending entry key
	default = None

	for idx_line, line in enumerate(text.splitlines()):
		if line.startswith('#') or not line.strip():
			continue

		# TODO review format. why does python's netrc lexer take escapes without quotes?
		#logger.debug("Checking line: %s", line)

		chars = iter(enumerate(line))

		for i, c in chars:
			#logger.debug("Checking %s", c)
			if 0:
				pass
			elif word is None and c == "\"":
				word = ""
				for i, c in chars:
					if c == "\\":
						i, c = next(chars)
						if c == "n":
							word += "\n"
						elif c == "t":
							word += "\t"
						elif c in "\\\"":
							word += c
						else:
							logger.debug("Unneeded escape in quoted at (%d,%d) for %s", idx_line+1, i+1, c)
							word += c
					elif c == "\"":
						break
					else:
						word += c
			elif c == "\\": # TODO confirm that escapes are allowed in unquoted
				i, c = next(chars)
				if c == "n":
					word += "\n"
				elif c == "t":
					word += "\t"
				elif c in "\\\"":
					word += c
				else:
					logger.debug("Unneeded escape in unquoted at (%d,%d) for %s", idx_line+1, i+1, c)
					word += c
			elif c in " \t\n\r":
				#word += "\x1B[33m(end)\x1B[0m"
				#logger.debug("End of word %s", word)
				if k is None and word == "default":
					entries.append(entry)
					#logging.info("Adding default entry")
					entry = dict()
					entry["machine"] = True
					default = entry
				elif k is None:
					k = word
					#logger.debug("Found key: %s", k)
					if k in ("machine", "host"):
						if entry:
							entries.append(entry)
							entry = dict()
				else:
					#logger.debug("Found value: %s", word)
					entry[k] = word
					k = None
				word = None
			else:
				if word is None:
					word = ""
				#word += "\x1B[31m"
				word += c
				#word += "\x1B[0m"

		if k is not None:
			#logger.debug("Flush k %s word %s", k, word)
			entry[k] = word
			k = None
			word = None
		else:
			logger.warning("K %s word %s", k, word)

	if entry:
		entries.append(entry)

	if default:
		for entry in entries:
			for k, v in default.items():
				entry.setdefault(k, v)
		entries.remove(default)

	return entries


def gen_one(path):
	if path.endswith(".gpg"):
		import gnupg
		gpg = gnupg.GPG()
		with open(path, "rb") as f:
			decrypted_data = gpg.decrypt_file(f)
			if not decrypted_data.ok:
				raise ValueError(f"Failed to decrypt {filename}: {decrypted_data.status}")
			text = str(decrypted_data)
	else:
		with open(path, "r") as f:
			text = f.read()

	for entry in parse(text):
		yield entry


def gen(candidates=None):
	if candidates is None:
		candidates = default_candidates

	for candidate in candidates:
		if not os.path.exists(candidate):
			continue

		yield from gen_one(candidate)


def get_entry(candidates=None, **kw):
	"""
	Obtain entry matching specification
	"""
	for entry in gen(candidates=candidates):
		for k, v in kw.items():
			if v is None:
				continue
			if entry.get(k) is None:
				continue
			if entry.get(k) != v:
				break
		else:
			return entry
