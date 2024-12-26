import io

from setuptools import setup, find_packages


with io.open("__init__.py", "r") as fi:
	local_namespace = {}
	exec(fi.read(), local_namespace)
	module_version = local_namespace["__version__"]


setup(
 name="authinfo",
 description="Parse credentials in ~/.authinfo files, either plain text or GPG-encrypted.",
 version=module_version,
 packages=find_packages(include=["authinfo"]),
 package_dir={"authinfo": "."},
 py_modules=[
  "authinfo.__init__",
 ],
)
