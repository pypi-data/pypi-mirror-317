#!/usr/bin/env python3

import os
import re
import shutil
import contextlib
import typing
import jinja2
import colorama
from datetime import datetime
from ruamel.yaml import YAML
from ampoule_ssg._utils import *


colorama.init()


class Document:
    """A type representing a document, which can be text or binary."""
    def __init__(self, file_name: typing.Union[str, bytes, os.PathLike], url_transform: typing.Callable = lambda x: x, front_matter_enabled: bool = True):
        """Create a new document object.

        :param file_name: The name of the file to read.
        :param url_transform: Function to change the file name to a different form.
        """
        self.file_name = file_name
        self.encoding = "utf-8"
        # If the file is text, read it.
        self.front_matter = YAML()
        self.front_matter.Constructor.add_constructor("tag:yaml.org,2002:timestamp", _no_date_constructor)
        self.content = ""
        self.date = datetime.fromtimestamp(os.path.getmtime(file_name))
        try:
            with open(file_name, "r", encoding=self.encoding) as f:
                print(colorama.Style.RESET_ALL, colorama.Style.BRIGHT, colorama.Fore.LIGHTWHITE_EX, f"Loading document {file_name}".ljust(shutil.get_terminal_size().columns), sep="")

                # Parse front matter if available.
                front_matter = ""
                if front_matter_enabled:
                    initial_line = f.readline()
                    if initial_line == "---\n":
                        print(colorama.Style.RESET_ALL, colorama.Fore.CYAN, "Front matter found", sep="")
                        line = ""
                        while line != "---\n":
                            line = f.readline()
                            if line != "---\n":
                                front_matter += line
                        print(colorama.Style.RESET_ALL, colorama.Fore.GREEN, "Front matter loaded", sep="")

                if front_matter and front_matter_enabled:
                    self.front_matter = self.front_matter.load(front_matter)

                    print(self.front_matter, type(self.front_matter))

                    if "DATE" in self.front_matter:
                        self.date = _parse_date_string(self.front_matter["DATE"])
                elif front_matter_enabled:   # put it back
                    self.content = initial_line

                print(colorama.Style.RESET_ALL, colorama.Fore.CYAN, "Reading content", sep="")

                self.content += f.read()

                print(colorama.Style.RESET_ALL, colorama.Fore.GREEN, "Content loaded", sep="")
                print(colorama.Style.RESET_ALL, colorama.Style.DIM, self.content[:128] + "..." if len(self.content) > 128 else self.content)
        except UnicodeDecodeError:
            print(colorama.Style.RESET_ALL, colorama.Fore.CYAN, "Text decoding failed, assuming binary", sep="")
            self.encoding = None
            with open(file_name, "rb") as f:
                self.content = f.read()
            print(colorama.Style.RESET_ALL, colorama.Fore.GREEN, "Binary content loaded", sep="")

        print(colorama.Style.RESET_ALL, colorama.Fore.CYAN, colorama.Style.DIM, f"Transforming URL {self.file_name} ->", end=" ", sep="")
        self.file_name = url_transform(self.file_name)
        print(colorama.Style.RESET_ALL, colorama.Style.BRIGHT, colorama.Fore.LIGHTYELLOW_EX, self.file_name)

        print(colorama.Style.RESET_ALL, end="")

    def __repr__(self):
        return f"Document({self.file_name})"

    def __str__(self):
        return self.content

    def __getitem__(self, item: str):
        """Get an item from the front matter of the document"""
        return self.front_matter[item]

    def __setitem__(self, item: str, value: typing.Any):
        """Set an item in the front matter of the document"""
        self.front_matter[item] = value

    def __delitem__(self, item: str):
        """Delete an item from the front matter of the document"""
        del self.front_matter[item]

    def __contains__(self, item: str):
        """Check if an item is in the front matter of the document"""
        return item in self.front_matter


class Index:
    """A type representing an index of documents."""
    def __init__(self, directory: typing.Union[str, bytes, os.PathLike], recursive: bool = False,
                 url_transform: typing.Callable = lambda x: x, sort_by: typing.Callable = lambda x: x.file_name, reverse: bool = False,
                 exclude: typing.Union[str, None] = None, static: bool = False):
        """Create a new index object.

        :param directory: The directory to read the files from.
        :param recursive: Whether to read files from subdirectories.
        :param url_transform: Function to change the file name to a different form.
        :param sort_by: Function returning a key to sort the documents by.
        :param exclude: Regular expression to exclude files from the index.
        """
        self.directory = directory
        self.static = static
        # Temporarily move to the specified directory in order to read the files.
        if exclude:
            regex = re.compile(exclude)
        else:
            regex = re.compile("(?!)")
        with _in_directory(directory):
            if recursive:
                self.file_names = [os.path.join(dir_path, f) for dir_path, dir_name, filenames in os.walk(".") for f in filenames if not regex.search(f)]
            else:
                self.file_names = [i for i in os.listdir() if os.path.isfile(i) and not regex.search(i)]

            self.documents = sorted([Document(i, url_transform, front_matter_enabled=not static) for i in self.file_names], key=sort_by, reverse=reverse)
        self.__current_index = 0

    def __iter__(self):
        self.__current_index = 0
        return self

    def __next__(self):
        if self.__current_index >= len(self.documents):
            raise StopIteration
        else:
            self.__current_index += 1
            return self.documents[self.__current_index - 1]

    def __repr__(self):
        return f"Index({self.directory}): {self.documents}"

    def __len__(self):
        return len(self.documents)


class Site:
    """A type representing a website."""
    def __init__(self, build_dir: typing.Union[str, bytes, os.PathLike], template_dir: typing.Union[str, bytes, os.PathLike] = "templates"):
        """Create a new site object.

        :param build_dir: The directory to build the site in.
        :param template_dir: The directory to read the templates from.
        """
        self.build_dir: str = build_dir
        self.template_engine: jinja2.Environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
        self.pages: dict[str, typing.Union[Static, Page]] = {}
        self.context: dict[str, typing.Any] = {}

    def add_page(self, location: typing.Union[str, bytes, os.PathLike], page: typing.Union["Static", "Page"]):
        """Add a page to the site.

        :param location: The location the page should be saved to.
        :param page: The page object itself.
        """
        if location.endswith("/"):
            location += "index.html"
        location = location.lstrip("/")            # interpret it as site root, not OS root
        self.pages[location] = page

    def add_from_index(self, index: Index, location: typing.Union[str, bytes, os.PathLike], template: typing.Union[str, None] = None, **kwargs):
        """Add pages to the site from an index.

        :param index: The index to read the documents from.
        :param location: The location to save the pages to.
        :param template: The template to use for the pages.
        :param static: Whether to treat them as static files.
        :param kwargs: Additional keyword arguments to pass to the template when rendering.
        """
        location = location.lstrip("/")            # interpret it as site root, not OS root
        kwargs = {**self.context, **kwargs}
        if index.static:
            for document in index:
                self.pages[os.path.join(location, document.file_name)] = Static(self, document)
        else:
            for document in index:
                self.pages[os.path.join(location, document.file_name)] = Page(self, template, document, **kwargs)

    def filter(self, name: str):
        """Decorator to add a filter to the template engine.

        :param name: The name the filter will be used with in Jinja2.
        """
        def decorator(func):
            self.template_engine.filters[name] = func
            return func

        return decorator

    def test(self, name: str):
        """Decorator to add a test to the template engine.

        :param name: The name the test will be used with in Jinja2.
        """
        def decorator(func):
            self.template_engine.tests[name] = func
            return func

        return decorator

    def build(self, dont_delete: typing.Optional[list[str]] = None):
        """Build the site in its directory."""
        # Clear the build directory if it exists.
        if os.path.isdir(self.build_dir):
            _delete_directory_contents(self.build_dir, dont_delete=dont_delete)
        for location, page in self.pages.items():
            # Create the required directories.
            os.makedirs(os.path.join(self.build_dir, os.path.dirname(location)), exist_ok=True)
            if isinstance(page, str):
                with open(os.path.join(self.build_dir, location), "w") as f:
                    f.write(page)
            elif isinstance(page, bytes):
                with open(os.path.join(self.build_dir, location), "wb") as f:
                    f.write(page)
            else:
                raise ValueError(f"{type(page)} cannot be used as a document")


class Page(str):
    """A type representing a page, which is a rendered template."""
    def __new__(cls, site: Site, template: str, document: Document = None, **kwargs):
        kwargs = {**site.context, **kwargs}
        return site.template_engine.get_template(template).render(document=document, **kwargs)


class Static(bytes):
    """A type representing a static file, which is binary content that is not templated."""
    def __new__(cls, site: Site, document: Document):
        return document.content
