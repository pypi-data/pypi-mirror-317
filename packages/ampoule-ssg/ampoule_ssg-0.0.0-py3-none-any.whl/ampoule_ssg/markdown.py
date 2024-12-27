import re
import bs4 as beautifulsoup
import sys


def only_chars(string, chars):
    chars = set(chars)
    all_chars = set(string)
    return all_chars.issubset(chars)


inline_regex = r"""
(?P<imageFlag>!?) \[ (?P<urlText>[^\[\]]*) \] \((?P<urlDestination>[^\(\)]*)\)     # hyperlink or media
|
(?P<em>\*{1,7}) (?P<textEm>(?:\\\*|[^*])*) (?P=em)                                 # emphasis with * not requiring space on either side
|
(?:^|\s)(?P<em2>_{1,7}) (?P<textEm2>(?:\\.|[^*])*) (?P=em2)(?=\s|$)                # emphasis with _ requiring space on at least one side
|
[`] (?P<textCode>(?:\\[`]|[^`])*) [`]                                              # inline code
|
(?P<strike>~{2}) (?P<textStrike>(?:\\[~]|[^~])*) (~{2})                            # strikethrough
|
(?P<diff>\-\-|\+\+) (?P<textDiff>(?:\\[-+]|[^-+])*) (?P=diff)                      # diffs
"""


def leading(string, character):
    return len(string) - len(string.lstrip(character))


def trailing(string, character):
    return len(string) - len(string.rstrip(character))


class Element:
    def __init__(self):
        self.classes = []
        self.content = None
        pass

    def __repr__(self):
        return "Void block"

    @property
    def tag_name(self):
        return "m-void"


class Container(Element):
    def __init__(self, content):
        super().__init__()
        self.content = parse_line(content)

    def __repr__(self):
        return "Generic container element: " + repr(self.content)


class Rule(Element):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "Rule"

    @property
    def tag_name(self):
        return "hr"


class HardBreak(Element):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "Hard break"

    @property
    def tag_name(self):
        return "br"


class Heading(Container):
    def __init__(self, content, level):
        super().__init__(content)
        self.level = level
        pass

    def __repr__(self):
        return f"Heading level {self.level}:\n\t" + repr(self.content)

    @property
    def tag_name(self):
        return "h" + str(self.level)


class Paragraph(Container):
    def __init__(self, content):
        super().__init__("")
        self.content = parse_line(content)

    def __repr__(self):
        return "Paragraph:\n\t" + repr(self.content)

    @property
    def tag_name(self):
        return "p"


class CodeBlock(Element):
    def __init__(self, content, language="text"):
        super().__init__()
        self.content = content
        self.language = language

    def __repr__(self):
        return f"Code block ({self.language}):\n\t" + repr(self.content)

    @property
    def tag_name(self):
        return "pre"


class UnorderedList(Element):
    def __init__(self, content):
        super().__init__()
        self.content = content

    def __repr__(self):
        return "Unordered list:\n\t" + repr(self.content)

    @property
    def tag_name(self):
        return "ul"


class OrderedList(Element):
    def __init__(self, content):
        super().__init__()
        self.content = content

    def __repr__(self):
        return "Ordered list:\n\t" + repr(self.content)

    @property
    def tag_name(self):
        return "ol"


class ListItem(Element):
    def __init__(self, content):
        super().__init__()
        self.content = tokenise(content)

    def __repr__(self):
        return "List item:\n\t" + repr(self.content)

    @property
    def tag_name(self):
        return "li"


class Blockquote(Paragraph):
    def __init__(self, content):
        super().__init__("")
        self.content = tokenise(content)

    def __repr__(self):
        return "Blockquote:\n\t" + repr(self.content)

    @property
    def tag_name(self):
        return "blockquote"


class Emphasis(Container):
    def __init__(self, content, value):
        super().__init__(content)
        self.value = value
        if value >= 4:
            self.classes.append("emphasis-3")
        if value % 4 >= 2:
            self.classes.append("emphasis-2")
        if value % 2:
            self.classes.append("emphasis-1")

    def __repr__(self):
        return f"Emphasis ({self.value}): " + repr(self.content)

    @property
    def tag_name(self):
        return "em" if self.value == 1 else "strong"


class Code(Element):
    def __init__(self, content):
        super().__init__()
        self.content = [content]

    def __repr__(self):
        return f"Inline code: {self.content}"

    @property
    def tag_name(self):
        return "code"


class Strikethrough(Container):
    def __init__(self, content):
        super().__init__(content)

    def __repr__(self):
        return f"Strikethrough: {repr(self.content)}"

    @property
    def tag_name(self):
        return "s"


class Diff(Container):
    def __init__(self, content, value):
        super().__init__(content)
        self.value = value

    def __repr__(self):
        return f"Diff ({self.value}): {self.content}"

    @property
    def tag_name(self):
        return "ins" if self.value == "++" else "del"


class Link(Element):
    def __init__(self, content, destination, image=False):
        super().__init__()
        self.content = parse_line(content)
        self.destination = destination
        self.image = image

    def __repr__(self):
        return f"{'Image' if self.image else 'Link'}: {self.content} -> {self.destination}"

    @property
    def tag_name(self):
        return "a"


class Image(Link):
    def __init__(self, text, destination):
        super().__init__(text, destination, True)

    @property
    def tag_name(self):
        return "img"


def parse_line(source):
    if trailing(source, "\\") == 1:
        source = source.rstrip("\\")
        hard_break = True
    else:
        hard_break = False

    tokens = []
    pattern = re.compile(inline_regex, re.MULTILINE | re.DOTALL | re.VERBOSE)
    matches = pattern.finditer(source)

    lookup = 0
    for i in matches:
        l = i.start()
        r = i.end()
        tokens.append(source[lookup:l])

        lookup = r

        if i.group("em"):
            tokens.append(Emphasis(i.group("textEm"), len(i.group("em"))))
        if i.group("em2"):
            tokens.append(Emphasis(i.group("textEm2"), len(i.group("em2"))))
        if i.group("textCode"):
            tokens.append(Code(i.group("textCode")))
        if i.group("strike"):
            tokens.append(Strikethrough(i.group("textStrike")))
        if i.group("diff"):
            tokens.append(Diff(i.group("textDiff"), i.group("diff")))
        if i.group("urlText"):
            if i.group("imageFlag"):
                tokens.append(Image(i.group("urlText"), i.group("urlDestination")))
            else:
                tokens.append(Link(i.group("urlText"), i.group("urlDestination")))

    tokens.append(source[lookup:])

    if hard_break:
        tokens.append(HardBreak())

    return tokens


def tokenise(source):
    tokens = []

    current_block = Element()

    lines = [line[1:] if line.startswith(" ") else line for line in source.split("\n")]  # remove leading spaces

    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.startswith(";"):
            # Void block

            tokens.append(current_block)
            current_block = Element()

            i += 1
        elif only_chars(line.strip(), "-_* ") and len(line.strip()) >= 3:
            # Horizontal rule

            tokens.append(current_block)
            current_block = Rule()

            i += 1
        elif (lines[i].startswith("*") or lines[i].startswith("+") or lines[i].startswith("-")) and lines[i][1:].startswith(" "):
            if not isinstance(current_block, UnorderedList):
                tokens.append(current_block)

            content = []

            while i < len(lines) and ((lines[i].startswith("*") or lines[i].startswith("+") or lines[i].startswith("-")) and lines[i][1:].startswith(" ")):
                inner_content = lines[i][2:].strip() + "\n"      # discard marker and space
                i += 1
                while i < len(lines) and lines[i].strip() and not ((lines[i].startswith("*") or lines[i].startswith("+") or lines[i].startswith("-")) and lines[i][1] == " "):
                    inner_content += lines[i] + "\n"
                    i += 1

                content.append(ListItem(inner_content))

            current_block = UnorderedList(content)
        elif re.match(r"^\d+\.", line):
            if not isinstance(current_block, UnorderedList):
                tokens.append(current_block)

            content = []

            while i < len(lines) and re.match(r"^ ?\d+\.", lines[i]) and len(lines[i].split(".", 1)) > 1:
                inner_content = lines[i].split(".", 1)[1] + "\n"      # discard number and period
                i += 1
                marker_length = len(lines[i].split(".", 1)[0]) + 1
                while i < len(lines) and lines[i].strip() and not re.match(r"^ ?\d+\.", lines[i]):
                    if re.match(r"^  \d+\.", lines[i]):
                        marker_length = 2
                    inner_content += lines[i][marker_length:] + "\n"
                    i += 1

                content.append(ListItem(inner_content))

            current_block = OrderedList(content)
        elif line.startswith("#") and leading(line.lstrip("#"), " "):
            tokens.append(current_block)

            content = line.lstrip("#").strip()
            current_block = Heading(content, leading(line, "#"))

            i += 1
        elif line.startswith(">"):
            if not isinstance(current_block, Blockquote):
                tokens.append(current_block)

            content = ""

            while i < len(lines) and (lines[i].startswith(">") or (not lines[i].startswith("#") and not lines[i].startswith(">") and lines[i].strip()) and not only_chars(line.strip(), "-_* ") and len(line.strip()) >= 3):
                content += lines[i].lstrip(">") + "\n"
                i += 1

            current_block = Blockquote(content)
        elif leading(line, "~") == 3 or leading(line, "`") == 3:
            if not isinstance(current_block, CodeBlock):
                tokens.append(current_block)

            language = line.lstrip("`~").strip()

            content = ""
            i += 1        # skip the opening fence
            while i < len(lines) and not lines[i].strip() in ("```", "~~~"):
                content += lines[i] + "\n"
                i += 1

            if i < len(lines):
                i += 1    # prevent a new block from beginning with the closing fence

            current_block = CodeBlock(content, language=language)
        elif i < len(lines) - 1 and (only_chars(lines[i+1].strip(), "=") or only_chars(lines[i+1].strip(), "-")) and lines[i+1].strip():
            tokens.append(current_block)

            content = line.strip()
            current_block = Heading(content, 1 if lines[i+1].startswith("=") else 2)

            i += 2
        else:
            if not isinstance(current_block, Paragraph):
                # Create a paragraph, if there is no other specifier
                tokens.append(current_block)

            content = ""

            while (i < len(lines)
                   and not lines[i].startswith("#")
                   and not lines[i].startswith(">")
                   and not lines[i].startswith(";")
                   and not lines[i].startswith("* ")
                   and not lines[i].startswith("+ ")
                   and not lines[i].startswith("- ")
                   and not lines[i].startswith("~~~")
                   and not lines[i].startswith("```")
                   and not re.match(r"^\d+\.", lines[i])
                   and lines[i].strip()):
                content += lines[i].strip() + "\n"
                i += 1

            current_block = Paragraph(content)

    tokens.append(current_block)

    return tokens


def make_html(ast):
    soup = beautifulsoup.BeautifulSoup()
    for i in ast:
        # Use bs4 to generate HTML
        if isinstance(i, str):
            soup.append(i)
        elif hasattr(i, "content") and i.tag_name != "m-void":
            tag = soup.new_tag(str(i.tag_name))
            if i.tag_name == "a":
                tag["href"] = i.destination
            if i.tag_name == "img":
                tag["src"] = i.destination
                tag["alt"] = " ".join(i.content)
            if i.tag_name == "pre":
                tag["data-language"] = i.language
            if i.classes:
                tag["class"] = " ".join(i.classes)
            try:
                if isinstance(i.content, list):
                    tag.append(make_html(i.content))
                elif i.content and i.tag_name != "img":
                    tag.string = i.content

                if i.tag_name == "img":
                    tag.string = ""
            except AttributeError as exc:
                # print(i)
                print(exc, file=sys.stderr)
            soup.append(tag)
    return soup


def markdown2html(markdown):
    return make_html(tokenise(markdown))

