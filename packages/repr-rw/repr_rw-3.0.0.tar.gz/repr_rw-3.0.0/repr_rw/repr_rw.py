import re

# strath is a dependency of syspathmodif.
from strath import\
	ensure_path_is_pathlib
from syspathmodif import\
	SysPathBundle


_ENCODING_UTF8 = "utf-8"
_MODE_R = "r"
_MODE_W = "w"
_NEW_LINE = "\n"

_REGEX_FROM_IMPORT = "from .+ import .+"


def _is_valid_import_statement(some_str):
	regex_match = re.match(_REGEX_FROM_IMPORT, some_str)
	return regex_match is not None


def _raise_import_statement_value_error(importation):
	if not _is_valid_import_statement(importation):
		raise ValueError(f"Import statements must match regex \""
			+ _REGEX_FROM_IMPORT + "\". Recieved \"" + importation + "\".")


def read_reprs(file_path, importations=None, paths=None):
	"""
	If a text file contains the representation of Python objects, this
	generator can read it to recreate those objects. Each line in the file
	must be a string returned by function repr. Empty lines are ignored. Each
	iteration of this generator yields one object.

	Recreating objects requires to import their class unless they are of a
	built-in type. For this purpose, you need to provide the necessary import
	statements as character strings. All import statements must match regular
	expression "from .+ import .+".

	The imported classes' package or module must be accessible for importation.
	It is already the case for standard and installed packages. For classes
	from other sources, you need to include the path to its package's or
	module's parent directory in list sys.path. If you provide the required
	paths to this generator, it will add them to sys.path, perform the imports
	and remove the paths from sys.path. If, instead, you choose to handle the
	paths out of this generator, you should not provide any path.

	Args:
		file_path (str or pathlib.Path): the path to a text file that contains
			object representations.
		importations (generator, list, set or tuple):
			class import statements (str). Defaults to None.
		paths (generator, list, set or tuple): the paths (str or pathlib.Path)
			to the imported classes. Defaults to None.

	Yields:
		an object recreated from its representation.

	Raises:
		FileNotFoundError: if the file indicated by argument file_path does
			not exist.
		ImportError: if an import statement is incorrect.
		ModuleNotFoundError: if an imported class' module or package cannot
			be found. An item in argument paths may be incorrect.
		NameError: if a required class was not imported.
		TypeError: if argument file_path or an item in argument paths is not
			of type str or pathlib.Path.
		ValueError: if an import statement does not match regular expression
			"from .+ import .+".
		Exception: any exception raised upon the parsing of an object
			representation.
	"""
	if importations is not None:
		if paths is not None:
			bundle = SysPathBundle(paths)

		for importation in importations:
			_raise_import_statement_value_error(importation)
			exec(importation)

		if paths is not None:
			bundle.clear()
			del bundle

	file_path = ensure_path_is_pathlib(file_path, False)

	with file_path.open(mode=_MODE_R, encoding=_ENCODING_UTF8) as file:
		for obj_repr in file:
			# The iterator yields one line at the time, including \n.
			obj_repr = obj_repr.strip()

			if len(obj_repr) >= 1:
				yield eval(obj_repr)


def write_reprs(file_path, objs):
	"""
	Writes the representation of Python objects in a text file. Each line is a
	string returned by function repr. If the file already exists, this function
	overwrites it.

	Args:
		file_path (str or pathlib.Path): the path to the text file that will
			contain the object representations.
		objs (generator, list, set or tuple): the objects whose representation
			will be written.

	Raises:
		TypeError: if argument file_path is not of type str or pathlib.Path.
	"""
	file_path = ensure_path_is_pathlib(file_path, False)

	with file_path.open(mode=_MODE_W, encoding=_ENCODING_UTF8) as file:
		for obj in objs:
			file.write(repr(obj) + _NEW_LINE)
