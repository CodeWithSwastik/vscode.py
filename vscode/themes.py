import enum
from .undef import undefined

# Code below has taken and modified from Tyriar/vscode-theme-generator
# https://github.com/Tyriar/vscode-theme-generator


class BaseColorSet:
    def __init__(self, background: str, foreground: str, colors: list):
        self.background = background
        self.foreground = foreground
        if not len(colors) == 4:
            raise ValueError("Length of accent colors must be 4")
        for i, color in enumerate(colors):
            setattr(self, f"color{i+1}", color)


class ColorSet:
    """
    type: 'light' | 'dark'
    base: BaseColorSet
    syntax: {
        boolean: string
        function: string
        functionCall: string
        identifier: string
        keyword: string
        number: string
        storage: string
        string: string
        stringEscape: string
        comment: string
        class: string
        classMember: string
        type: string
        modifier: string
        cssClass: string
        cssId: string
        cssTag: string
        markdownQuote: string
    }
    ui: {
        /** The color of the editor cursor/caret */
        cursor: string
        /** Visible whitespace (editor.renderWhitespace) */
        invisibles: string
        /** Indent guide */
        guide: string
        /** Line highlight, this will remove the line borders in favor of a solid highlight */
        lineHighlight: string

        findMatchHighlight: string
        currentFindMatchHighlight: string
        findRangeHighlight: string
        /** Highlights the line(s) of the current find match, this also applies to things like find symbol */
        rangeHighlight: string
        /** Highlights strings that match the current selection, excluding the selection itself */
        selectionHighlight: string

        selection: string
        wordHighlight: string
        wordHighlightStrong: string
        activeLinkForeground: string
    }
    terminal: {
        black: string
        red: string
        green: string
        yellow: string
        blue: string
        magenta: string
        cyan: string
        white: string
        brightBlack: string
        brightRed: string
        brightGreen: string
        brightYellow: string
        brightBlue: string
        brightMagenta: string
        brightCyan: string
        brightWhite: string
    }
    """

    def __init__(
        self,
        base: BaseColorSet,
        syntax: dict = None,
        ui: dict = None,
        terminal: dict = None,
        type: str = "dark",
    ):
        self.type = type
        self.base = base

        class DictClass:
            def __init__(self, data):
                if data is not None:
                    self.__dict__.update(data)

            def __getattr__(self, attr):
                try:
                    return self.__dict__[attr]
                except KeyError:
                    return None

        self.syntax = DictClass(syntax)
        self.ui = DictClass(ui)
        self.terminal = DictClass(terminal)


class FontStyle(enum.IntEnum):
    NONE = 0
    ITALIC = 1 << 0
    BOLD = 1 << 1
    UNDERLINE = 1 << 2


def global_setting_generator(name: str):
    def func(color):
        if not color:
            return undefined
        result = {name: color}
        return result

    return func


def simple_color_generator(name: str, scope: str, font_style: int = FontStyle.NONE):
    def func(color):
        color_rule = {"name": name, "scope": scope, "settings": {"foreground": color}}
        font_styles = []
        if font_style == FontStyle.ITALIC:
            font_styles.append("italic")

        if font_style == FontStyle.BOLD:
            font_styles.append("bold")

        if font_style == FontStyle.UNDERLINE:
            font_styles.append("underline")

        if len(font_styles) > 0:
            color_rule["settings"]["fontStyle"] = " ".join(font_styles)

        return color_rule

    return func


global_rules = [
    {
        "color": lambda s: s.base.background,
        "generate": global_setting_generator("background"),
    },
    {
        "color": lambda s: s.base.foreground,
        "generate": global_setting_generator("foreground"),
    },
]
token_rules = [
    # string: It's important that string is put first so that other scopes can override strings
    # within template expressions
    {
        "color": lambda s: s.syntax.string,
        "generate": simple_color_generator("String", "string"),
    },
    {
        "color": lambda s: s.syntax.stringEscape,
        "generate": simple_color_generator(
            "String Escape",
            "constant.character.escape, text.html constant.character.entity.named, punctuation.definition.entity.html",
        ),
    },
    {
        "color": lambda s: s.syntax.boolean,
        "generate": simple_color_generator("Boolean", "constant.language.boolean"),
    },
    {
        "color": lambda s: s.syntax.number,
        "generate": simple_color_generator("Number", "constant.numeric"),
    },
    {
        "color": lambda s: s.syntax.identifier,
        "generate": simple_color_generator(
            "Identifier",
            "variable, support.variable, support.class, support.constant, meta.definition.variable entity.name.function",
        ),
    },
    # support.type.object: module.exports (ts)
    {
        "color": lambda s: s.syntax.keyword,
        "generate": simple_color_generator(
            "Keyword",
            "keyword, modifier, variable.language.this, support.type.object, constant.language",
        ),
    },
    # support.function: eg. join in path.join in TypeScript
    {
        "color": lambda s: s.syntax.functionCall,
        "generate": simple_color_generator(
            "Function call", "entity.name.function, support.function"
        ),
    },
    # storage.type: var (ts)
    # storage.modifier: private (ts)
    {
        "color": lambda s: s.syntax.storage,
        "generate": simple_color_generator("Storage", "storage.type, storage.modifier"),
    },
    # module.support: imported modules in TypeScript
    {
        "color": lambda s: s.syntax.identifier,
        "generate": simple_color_generator(
            "Modules", "support.module, support.node", FontStyle.ITALIC
        ),
    },
    # support.type: `boolean` (ts)
    {
        "color": lambda s: s.syntax.type,
        "generate": simple_color_generator("Type", "support.type"),
    },
    # entity.name.type: `: SomeType` (ts)
    {
        "color": lambda s: s.syntax.type,
        "generate": simple_color_generator(
            "Type", "entity.name.type, entity.other.inherited-class"
        ),
    },
    {
        "color": lambda s: s.syntax.comment,
        "generate": simple_color_generator("Comment", "comment", FontStyle.ITALIC),
    },
    {
        "color": lambda s: getattr(s.syntax, "class"),
        "generate": simple_color_generator(
            "Class", "entity.name.type.class", FontStyle.UNDERLINE
        ),
    },
    # variable.object.property: `class A { meth = 0 }` (ts)
    # meta.field.declaration entity.name.function: `class A { meth = (lambda ): 0 }` (ts)
    {
        "color": lambda s: s.syntax.classMember,
        "generate": simple_color_generator(
            "Class variable",
            "variable.object.property, meta.field.declaration entity.name.function",
        ),
    },
    # meta.definition.method entity.name.function: `class A { meth() {} }` (ts)
    {
        "color": lambda s: s.syntax.classMember,
        "generate": simple_color_generator(
            "Class method", "meta.definition.method entity.name.function"
        ),
    },
    {
        "color": lambda s: s.syntax.function,
        "generate": simple_color_generator(
            "Function definition", "meta.function entity.name.function"
        ),
    },
    # punctuation.definition.template-expression: `${}`
    {
        "color": lambda s: s.syntax.keyword,
        "generate": simple_color_generator(
            "Template expression",
            "template.expression.begin, template.expression.end, punctuation.definition.template-expression.begin, punctuation.definition.template-expression.end",
        ),
    },
    {
        "color": lambda s: s.base.foreground,
        "generate": simple_color_generator(
            "Reset embedded/template expression colors",
            "meta.embedded, source.groovy.embedded, meta.template.expression",
        ),
    },
    {
        "color": lambda s: s.syntax.identifier,
        "generate": simple_color_generator("YAML key", "entity.name.tag.yaml"),
    },
    # modifier: This includes things like access modifiers, static, readonly, etc.
    {
        "color": lambda s: s.syntax.modifier,
        "generate": simple_color_generator("Modifier", "modifier"),
    },
    # JSON
    {
        "color": lambda s: s.syntax.identifier,
        "generate": simple_color_generator(
            "JSON key",
            "meta.object-literal.key, meta.object-literal.key string, support.type.property-name.json",
        ),
    },
    {
        "color": lambda s: s.syntax.keyword,
        "generate": simple_color_generator("JSON constant", "constant.language.json"),
    },
    # CSS
    {
        "color": lambda s: s.syntax.cssClass,
        "generate": simple_color_generator(
            "CSS class", "entity.other.attribute-name.class"
        ),
    },
    {
        "color": lambda s: s.syntax.cssId,
        "generate": simple_color_generator("CSS ID", "entity.other.attribute-name.id"),
    },
    {
        "color": lambda s: s.syntax.cssTag,
        "generate": simple_color_generator("CSS tag", "source.css entity.name.tag"),
    },
    # HTML
    {
        "color": lambda s: s.syntax.keyword,
        "generate": simple_color_generator(
            "HTML tag outer", "meta.tag, punctuation.definition.tag"
        ),
    },
    {
        "color": lambda s: s.syntax.identifier,
        "generate": simple_color_generator("HTML tag inner", "entity.name.tag"),
    },
    {
        "color": lambda s: s.syntax.functionCall,
        "generate": simple_color_generator(
            "HTML tag attribute", "entity.other.attribute-name"
        ),
    },
    # Markdown
    {
        "color": lambda s: s.syntax.keyword,
        "generate": simple_color_generator("Markdown heading", "markup.heading"),
    },
    {
        "color": lambda s: s.syntax.identifier,
        "generate": simple_color_generator(
            "Markdown link text",
            "text.html.markdown meta.link.inline, meta.link.reference",
        ),
    },
    {
        "color": lambda s: s.syntax.markdownQuote,
        "generate": simple_color_generator(
            "Markdown block quote", "text.html.markdown markup.quote"
        ),
    },
    {
        "color": lambda s: s.syntax.keyword,
        "generate": simple_color_generator(
            "Markdown list item",
            "text.html.markdown beginning.punctuation.definition.list",
        ),
    },
    {
        "color": lambda s: s.syntax.identifier,
        "generate": simple_color_generator(
            "Markdown italic", "markup.italic", FontStyle.ITALIC
        ),
    },
    {
        "color": lambda s: s.syntax.identifier,
        "generate": simple_color_generator(
            "Markdown bold", "markup.bold", FontStyle.BOLD
        ),
    },
    {
        "color": lambda s: s.syntax.identifier,
        "generate": simple_color_generator(
            "Markdown bold italic",
            "markup.bold markup.italic, markup.italic markup.bold",
            FontStyle.BOLD | FontStyle.ITALIC,
        ),
    },
    {
        "color": lambda s: s.syntax.string,
        "generate": simple_color_generator(
            "Markdown code block",
            "markup.fenced_code.block.markdown punctuation.definition.markdown",
        ),
    },
    {
        "color": lambda s: s.syntax.string,
        "generate": simple_color_generator(
            "Markdown inline code", "markup.inline.raw.string.markdown"
        ),
    },
    # Ini
    {
        "color": lambda s: s.syntax.identifier,
        "generate": simple_color_generator(
            "INI property name", "keyword.other.definition.ini"
        ),
    },
    {
        "color": lambda s: s.syntax.keyword,
        "generate": simple_color_generator(
            "INI section title", "entity.name.section.group-title.ini"
        ),
    },
    # C#
    {
        "color": lambda s: getattr(s.syntax, "class"),
        "generate": simple_color_generator(
            "C# class",
            "source.cs meta.class.identifier storage.type",
            FontStyle.UNDERLINE,
        ),
    },
    {
        "color": lambda s: s.syntax.classMember,
        "generate": simple_color_generator(
            "C# class method", "source.cs meta.method.identifier entity.name.function"
        ),
    },
    {
        "color": lambda s: s.syntax.functionCall,
        "generate": simple_color_generator(
            "C# function call",
            "source.cs meta.method-call meta.method, source.cs entity.name.function",
        ),
    },
    {
        "color": lambda s: s.syntax.type,
        "generate": simple_color_generator("C# type", "source.cs storage.type"),
    },
    {
        "color": lambda s: s.syntax.type,
        "generate": simple_color_generator(
            "C# return type", "source.cs meta.method.return-type"
        ),
    },  # Lambda function returns do not use storage.type scope
    {
        "color": lambda s: s.syntax.comment,
        "generate": simple_color_generator(
            "C# preprocessor", "source.cs meta.preprocessor"
        ),
    },
    {
        "color": lambda s: s.base.foreground,
        "generate": simple_color_generator(
            "C# namespace", "source.cs entity.name.type.namespace"
        ),
    },  # Override generic entity.name.type rule
]


def get_rgb(color: str) -> tuple:
    if color is None:
        return None
    return int(color[1:2], 16), int(color[3:5], 16), int(color[5:], 16)


def to_css_string(rgb: tuple) -> str:
    if rgb is None:
        return None

    return "#%02x%02x%02x" % rgb


import math


def lighten(color: str, amount: int) -> str:
    if color is None:
        return None

    MAX = 255
    r, g, b = get_rgb(color)
    r = min(math.floor(r + (r * amount)), MAX)
    g = min(math.floor(g + (g * amount)), MAX)
    b = min(math.floor(b + (b * amount)), MAX)

    return to_css_string((r, g, b))


def darken(color: str, amount: int) -> str:
    return lighten(color, -amount)


def add_alpha(color: str, alpha: int) -> str:
    if color is None:
        return None

    if len(color) != 7:
        raise ValueError("add_alpha only supports adding to #rrggbb format colors")

    alpha_hex = hex(round(alpha * 255))[2:]
    if len(alpha_hex) == 1:
        alpha_hex = "0" + alpha_hex

    return color + alpha_hex


def generate_fallback_color_set(s: BaseColorSet, type: str) -> ColorSet:
    func = darken if type == "light" else lighten
    syntax = {
        "boolean": s.color1,
        "function": s.color3,
        "functionCall": s.color4,
        "identifier": func(s.color1, 0.5),
        "keyword": s.color1,
        "number": s.color4,
        "storage": s.color1,
        "string": s.color2,
        "stringEscape": func(s.color2, 0.5),
        "comment": func(s.background, 2.0),
        "class": s.color3,
        "classMember": s.color3,
        "type": s.color3,
        "modifier": None,
        "cssClass": s.color1,
        "cssId": s.color2,
        "cssTag": s.color3,
        "markdownQuote": None,
    }
    ui = {
        "cursor": None,
        "invisibles": func(s.background, 0.2),
        "guide": func(s.background, 0.2),
        "lineHighlight": None,
        "findMatchHighlight": None,
        "currentFindMatchHighlight": None,
        "findRangeHighlight": None,
        "rangeHighlight": None,
        "selectionHighlight": None,
        "selection": None,
        "wordHighlight": None,
        "wordHighlightStrong": None,
        "activeLinkForeground": None,
    }
    terminal = {
        "black": None,
        "red": None,
        "green": None,
        "yellow": None,
        "blue": None,
        "magenta": None,
        "cyan": None,
        "white": None,
        "brightBlack": None,
        "brightRed": None,
        "brightGreen": None,
        "brightYellow": None,
        "brightBlue": None,
        "brightMagenta": None,
        "brightCyan": None,
        "brightWhite": None,
    }

    c = ColorSet(s, syntax, ui, terminal, type=type)
    return c


def generate_theme(name: str, color_set: ColorSet) -> dict:
    fallback = generate_fallback_color_set(color_set.base, color_set.type)
    theme = {
        "name": name,
        "tokenColors": [],
        "colors": {},
    }
    global_settings = {"name": "Global settings", "settings": {}}
    for generator in token_rules:
        color = generator["color"](color_set) or generator["color"](fallback)
        if color:
            theme["tokenColors"].append(generator["generate"](color))

    for generator in global_rules:
        color = generator["color"](color_set) or generator["color"](fallback)
        if color:
            generated = generator["generate"](color)
            global_settings["settings"][list(generated.keys())[0]] = color
    # theme["tokenColors"].append(global_settings)

    _applyWorkbenchColors(theme, color_set)

    def remove_none(dictionary: dict) -> dict:
        new = {}
        for key, val in dictionary.items():
            if isinstance(val, dict):
                new[key] = remove_none(val)
            elif val is None:
                pass
            else:
                new[key] = val
        return new

    return remove_none(theme)


def contrast(color: str) -> str:
    if color is None:
        return None
    r, g, b = get_rgb(color)
    luminance = r * 0.299 + g * 0.587 + b * 0.114
    return "#000000" if luminance > 192 else "#ffffff"


def _applyWorkbenchColors(theme: dict, color_set: ColorSet) -> None:
    func = lighten if color_set.type == "light" else darken

    background1 = func(color_set.base.background, 0.1)
    background2 = color_set.base.background
    background3 = func(color_set.base.background, 0.1)
    background4 = func(color_set.base.background, 0.2)
    background5 = func(color_set.base.background, 0.3)
    color1Unfocused = darken(color_set.base.color1, 0.1)
    color1Inactive = darken(color_set.base.color1, 0.2)

    # Contrast colors
    # contrastActiveBorder: An extra border around active elements to separate them from others for greater contrast.
    # contrastBorder: An extra border around elements to separate them from others for greater contrast.

    # Base Colors
    # focusBorder: Overall border color for focused elements. This color is only used if not overridden by a component.
    theme["colors"]["focusBorder"] = color_set.base.color1
    # foreground: Overall foreground color. This color is only used if not overridden by a component.
    theme["colors"]["foreground"] = color_set.base.foreground
    # widget.shadow: Shadow color of widgets such as find/replace inside the editor.

    # Button Control
    # button.background: Button background color.
    theme["colors"]["button.background"] = color_set.base.color1
    # button.foreground: Button foreground color.
    theme["colors"]["button.foreground"] = contrast(
        theme["colors"]["button.background"]
    )
    # button.hoverBackground: Button background color when hovering.

    # Dropdown Control
    # dropdown.background: Dropdown background.
    theme["colors"]["dropdown.background"] = background5
    # dropdown.border: Dropdown border.
    # dropdown.foreground: Dropdown foreground.

    # Input Control
    # input.background: Input box background.
    theme["colors"]["input.background"] = background5
    # input.border: Input box border.
    # input.foreground: Input box foreground.
    # inputOption.activeBorder: Border color of activated options in input fields.
    theme["colors"]["inputOption.activeBorder"] = color_set.base.color1
    # inputValidation.errorBackground: Input validation background color for error severity.
    # inputValidation.errorBorder: Input validation border color for error severity.
    # inputValidation.infoBackground: Input validation background color for information severity.
    # inputValidation.infoBorder: Input validation border color for information severity.
    # inputValidation.warningBackground: Input validation background color for information warning.
    # inputValidation.warningBorder: Input validation border color for warning severity.

    # Scrollbar Control
    # scrollbar.shadow: Scrollbar shadow to indicate that the view is scrolled.
    # scrollbarSlider.activeBackground: Slider background color when active.
    # scrollbarSlider.background: Slider background color.
    # scrollbarSlider.hoverBackground: Slider background color when hovering.

    # Lists and Trees
    # list.activeSelectionBackground: List/Tree background color for the selected item when the list/tree is active. An active list/tree has keyboard focus, an inactive does not.
    theme["colors"]["list.activeSelectionBackground"] = add_alpha(
        color_set.base.color1, 0.5
    )
    # list.activeSelectionForeground: List/Tree foreground color for the selected item when the list/tree is active. An active list/tree has keyboard focus, an inactive does not.
    theme["colors"]["list.activeSelectionForeground"] = "#FFFFFF"
    theme["colors"]["list.dropBackground"] = add_alpha(color_set.base.color1, 0.5)
    # list.focusBackground: List/Tree background color for the focused item when the list/tree is active. An active list/tree has keyboard focus, an inactive does not.
    theme["colors"]["list.focusBackground"] = add_alpha(color_set.base.color1, 0.5)
    theme["colors"]["list.focusForeground"] = "#FFFFFF"
    # list.highlightForeground: List/Tree foreground color of the match highlights when searching inside the list/tree.
    theme["colors"]["list.highlightForeground"] = color_set.base.color1
    # list.hoverBackground: List/Tree background when hovering over items using the mouse.
    theme["colors"]["list.hoverBackground"] = add_alpha("#FFFFFF", 0.1)
    # list.inactiveSelectionBackground: List/Tree background color for the selected item when the list/tree is inactive. An active list/tree has keyboard focus, an inactive does not.
    theme["colors"]["list.inactiveSelectionBackground"] = add_alpha("#FFFFFF", 0.2)

    # Activity Bar
    # activityBar.background: Activity bar background color. The activity bar is showing on the far left or right and allows to switch between views of the side bar.
    theme["colors"]["activityBar.background"] = background4
    # activityBar.foreground: Activity bar foreground color (e.g. used for the icons). The activity bar is showing on the far left or right and allows to switch between views of the side bar.
    # activityBarBadge.background: Activity notification badge background color. The activity bar is showing on the far left or right and allows to switch between views of the side bar.
    theme["colors"]["activityBarBadge.background"] = color_set.base.color1
    # activityBarBadge.foreground: Activity notification badge foreground color. The activity bar is showing on the far left or right and allows to switch between views of the side bar.
    theme["colors"]["activityBarBadge.foreground"] = contrast(
        theme["colors"]["activityBarBadge.background"]
    )

    # Badge
    theme["colors"]["badge.background"] = color_set.base.color1
    theme["colors"]["badge.foreground"] = contrast(theme["colors"]["badge.background"])

    # Side Bar
    # sideBar.background: Side bar background color. The side bar is the container for views like explorer and search.
    theme["colors"]["sideBar.background"] = background3
    # sideBarSectionHeader.background: Side bar section header background color. The side bar is the container for views like explorer and search.
    theme["colors"]["sideBarSectionHeader.background"] = background4
    # sideBarTitle.foreground: Side bar title foreground color. The side bar is the container for views like explorer and search.

    # Editor Groups & Tabs
    # editorGroup.background: Background color of an editor group. Editor groups are the containers of editors. The background color shows up when dragging editor groups around.
    # editorGroup.border: Color to separate multiple editor groups from each other. Editor groups are the containers of editors.
    # editorGroup.dropBackground: Background color when dragging editors around.
    theme["colors"]["editorGroup.dropBackground"] = add_alpha(
        color_set.base.color1, 0.5
    )
    theme["colors"]["editorGroup.focusedEmptyBorder"] = color_set.base.color1
    # editorGroupHeader.noTabsBackground: Background color of the editor group title header when tabs are disabled. Editor groups are the containers of editors.
    # editorGroupHeader.tabsBackground: Background color of the tabs container. Tabs are the containers for editors in the editor area. Multiple tabs can be opened in one editor group. There can be multiple editor groups.
    theme["colors"]["editorGroupHeader.tabsBackground"] = background3
    # tab.activeBackground: Active tab background color. Tabs are the containers for editors in the editor area. Multiple tabs can be opened in one editor group. There can be multiple editor groups.
    # tab.activeForeground: Active tab foreground color in an active group. Tabs are the containers for editors in the editor area. Multiple tabs can be opened in one editor group. There can be multiple editor groups.
    # tab.border: Border to separate tabs from each other. Tabs are the containers for editors in the editor area. Multiple tabs can be opened in one editor group. There can be multiple editor groups.
    theme["colors"]["tab.border"] = add_alpha("#000000", 0.2)
    # tab.inactiveBackground: Inactive tab background color. Tabs are the containers for editors in the editor area. Multiple tabs can be opened in one editor group. There can be multiple editor groups.
    theme["colors"]["tab.activeBorder"] = color_set.base.color1
    theme["colors"]["tab.inactiveBackground"] = background4
    # tab.inactiveForeground: Inactive tab foreground color in an active group. Tabs are the containers for editors in the editor area. Multiple tabs can be opened in one editor group. There can be multiple editor groups.
    # tab.activeModifiedBorder: Border on top of the modified (dirty) active tabs in an active group.
    theme["colors"]["tab.activeModifiedBorder"] = color_set.base.color1
    # tab.inactiveModifiedBorder: Border on top of modified (dirty) inactive tabs in an active group.
    theme["colors"]["tab.inactiveModifiedBorder"] = color1Inactive
    # tab.unfocusedActiveModifiedBorder: Border on the top of modified (dirty) active tabs in an unfocused group.
    theme["colors"]["tab.unfocusedActiveModifiedBorder"] = color1Unfocused
    # tab.unfocusedInactiveModifiedBorder: Border on the top of modified (dirty) inactive tabs in an unfocused group.
    theme["colors"]["tab.unfocusedInactiveModifiedBorder"] = color1Inactive

    # Editor Colors
    # editor.background: Editor background color.
    theme["colors"]["editor.background"] = background2
    # editor.foreground: Editor default foreground color.
    theme["colors"]["editor.foreground"] = color_set.base.foreground
    # editorLineNumber.foreground: Color of editor line numbers.
    theme["colors"]["editorLineNumber.foreground"] = add_alpha("#FFFFFF", 0.3)
    theme["colors"]["editorLineNumber.activeForeground"] = color_set.base.color1
    # editorCursor.foreground: Color of the editor cursor.
    if color_set.ui.cursor:
        theme["colors"]["editorCursor.foreground"] = color_set.ui.cursor
    # editor.selectionBackground: Color of the editor selection.
    if color_set.ui.selection:
        theme["colors"]["editor.selectionBackground"] = color_set.ui.selection
    # editor.selectionHighlightBackground: Color for regions with the same content as the selection.
    if color_set.ui.selectionHighlight:
        theme["colors"][
            "editor.selectionHighlightBackground"
        ] = color_set.ui.selectionHighlight
    # editor.inactiveSelectionBackground: Color of the selection in an inactive editor.
    # editor.wordHighlightBackground: Background color of a symbol during read-access, like reading a variable.
    if color_set.ui.wordHighlight:
        theme["colors"]["editor.wordHighlightBackground"] = color_set.ui.wordHighlight
    # editor.wordHighlightStrongBackground: Background color of a symbol during write-access, like writing to a variable.
    if color_set.ui.wordHighlightStrong:
        theme["colors"][
            "editor.wordHighlightStrongBackground"
        ] = color_set.ui.wordHighlightStrong
    # editor.findMatchBackground: Color of the current search match.
    if color_set.ui.currentFindMatchHighlight:
        theme["colors"][
            "editor.findMatchBackground"
        ] = color_set.ui.currentFindMatchHighlight
    # editor.findMatchHighlightBackground: Color of the other search matches.
    if color_set.ui.findMatchHighlight:
        theme["colors"]["editor.findMatchHighlight"] = color_set.ui.findMatchHighlight
    # editor.findRangeHighlightBackground: Color the range limiting the search.
    if color_set.ui.findRangeHighlight:
        theme["colors"][
            "editor.findRangeHighlightBackground"
        ] = color_set.ui.findRangeHighlight
    # editor.hoverHighlightBackground: Highlight below the word for which a hover is shown.
    # editor.lineHighlightBackground: Background color for the highlight of line at the cursor position.
    # editor.lineHighlightBorder: Background color for the border around the line at the cursor position.
    theme["colors"]["editor.lineHighlightBorder"] = (
        color_set.ui.rangeHighlight
        if color_set.ui.rangeHighlight
        else add_alpha("#FFFFFF", 0.1)
    )
    # editorLink.activeForeground: Color of active links.
    if color_set.ui.activeLinkForeground:
        theme["colors"][
            "editorLink.activeForeground"
        ] = color_set.ui.activeLinkForeground
    # editor.rangeHighlightBackground: Background color of highlighted ranges, like by quick open and find features.
    theme["colors"]["editor.rangeHighlightBackground"] = add_alpha("#FFFFFF", 0.05)
    # editorWhitespace.foreground: Color of whitespace characters in the editor.
    if color_set.ui.invisibles:
        theme["colors"]["editorWhitespace.foreground"] = color_set.ui.invisibles
    # editorIndentGuide.background: Color of the editor indentation guides.
    if color_set.ui.guide:
        theme["colors"]["editorIndentGuide.background"] = color_set.ui.guide

    # Diff Editor Colors
    # diffEditor.insertedTextBackground: Background color for text that got inserted.
    # diffEditor.insertedTextBorder: Outline color for the text that got inserted.
    # diffEditor.removedTextBackground: Background color for text that got removed.
    # diffEditor.removedTextBorder: Outline color for text that got removed.

    # Editor Widget Colors
    # editorWidget.background: Background color of editor widgets, such as find/replace.
    theme["colors"]["editorWidget.background"] = background3
    # editorSuggestWidget.background: Background color of the suggest widget.
    # editorSuggestWidget.border: Border color of the suggest widget.
    # editorSuggestWidget.foreground: Foreground color of the suggest widget.
    # editorSuggestWidget.highlightForeground: Color of the match highlights in the suggest widget.
    # editorSuggestWidget.selectedBackground: Background color of the selected entry in the suggest widget.
    # editorHoverWidget.background: Background color of the editor hover.
    theme["colors"]["editorHoverWidget.background"] = background3
    # editorHoverWidget.border: Border color of the editor hover.
    # debugExceptionWidget.background: Exception widget background color.
    # debugExceptionWidget.border: Exception widget border color.
    # editorMarkerNavigation.background: Editor marker navigation widget background.
    theme["colors"]["editorMarkerNavigation.background"] = background3
    # editorMarkerNavigationError.background: Editor marker navigation widget error color.
    # editorMarkerNavigationWarning.background: Editor marker navigation widget warning color.

    # Peek View Colors
    # peekView.border: Color of the peek view borders and arrow.
    theme["colors"]["peekView.border"] = color_set.base.color1
    # peekViewEditor.background: Background color of the peek view editor.
    theme["colors"]["peekViewEditor.background"] = background1
    # peekViewEditor.matchHighlightBackground: Match highlight color in the peek view editor.
    # peekViewResult.background: Background color of the peek view result list.
    theme["colors"]["peekViewResult.background"] = background3
    # peekViewResult.fileForeground: Foreground color for file nodes in the peek view result list.
    # peekViewResult.lineForeground: Foreground color for line nodes in the peek view result list.
    # peekViewResult.matchHighlightBackground: Match highlight color in the peek view result list.
    # peekViewResult.selectionBackground: Background color of the selected entry in the peek view result list.
    # peekViewResult.selectionForeground: Foreground color of the selected entry in the peek view result list.
    # peekViewTitle.background: Background color of the peek view title area.
    theme["colors"]["peekViewTitle.background"] = background2
    # peekViewTitleDescription.foreground: Color of the peek view title info.
    # peekViewTitleLabel.foreground: Color of the peek view title.

    # Panel Colors
    # panel.background: Panel background color. Panels are shown below the editor area and contain views like output and integrated terminal.
    theme["colors"]["panel.background"] = background3
    # panel.border: Panel border color on the top separating to the editor. Panels are shown below the editor area and contain views like output and integrated terminal.
    theme["colors"]["panel.border"] = add_alpha("#FFFFFF", 0.1)
    # panelTitle.activeBorder: Border color for the active panel title. Panels are shown below the editor area and contain views like output and integrated terminal.
    theme["colors"]["panelTitle.activeBorder"] = add_alpha(
        color_set.base.foreground, 0.5
    )
    # panelTitle.activeForeground: Title color for the active panel. Panels are shown below the editor area and contain views like output and integrated terminal.
    # panelTitle.inactiveForeground: Title color for the inactive panel. Panels are shown below the editor area and contain views like output and integrated terminal.
    theme["colors"]["panelTitle.inactiveForeground"] = add_alpha(
        color_set.base.foreground, 0.5
    )

    # Status Bar Colors
    # statusBar.background: Standard status bar background color. The status bar is shown in the bottom of the window.
    theme["colors"]["statusBar.background"] = background1
    # statusBar.debuggingBackground: Status bar background color when a program is being debugged. The status bar is shown in the bottom of the window
    theme["colors"]["statusBar.debuggingBackground"] = color_set.base.color1
    theme["colors"]["statusBar.debuggingForeground"] = contrast(
        theme["colors"]["statusBar.debuggingBackground"]
    )
    # statusBar.foreground: Status bar foreground color. The status bar is shown in the bottom of the window.
    # statusBar.noFolderBackground: Status bar background color when no folder is opened. The status bar is shown in the bottom of the window.
    theme["colors"][
        "statusBar.noFolderBackground"
    ] = background1  # Don't make distinction between folder/no folder
    # statusBarItem.activeBackground: Status bar item background color when clicking. The status bar is shown in the bottom of the window.
    theme["colors"]["statusBarItem.activeBackground"] = add_alpha(
        color_set.base.color1, 0.5
    )
    # statusBarItem.hoverBackground: Status bar item background color when hovering. The status bar is shown in the bottom of the window.
    theme["colors"]["statusBarItem.hoverBackground"] = add_alpha("#FFFFFF", 0.1)
    # statusBarItem.prominentBackground: Status bar prominent items background color. Prominent items stand out from other status bar entries to indicate importance. The status bar is shown in the bottom of the window.
    # statusBarItem.prominentHoverBackground: Status bar prominent items background color when hovering. Prominent items stand out from other status bar entries to indicate importance. The status bar is shown in the bottom of the window.
    theme["colors"]["statusBarItem.remoteBackground"] = color_set.base.color1
    theme["colors"]["statusBarItem.remoteForeground"] = contrast(
        theme["colors"]["statusBarItem.remoteBackground"]
    )

    # Title Bar Colors (macOS)
    # titleBar.activeBackground: Title bar background when the window is active. Note that this color is currently only supported on macOS.
    theme["colors"]["titleBar.activeBackground"] = background1
    # titleBar.activeForeground: Title bar foreground when the window is active. Note that this color is currently only supported on macOS.
    # titleBar.inactiveBackground: Title bar background when the window is inactive. Note that this color is currently only supported on macOS.
    # titleBar.inactiveForeground: Title bar foreground when the window is inactive. Note that this color is currently only supported on macOS.

    # Notification Dialog Colors
    # notification.background: Notifications background color. Notifications slide in from the top of the window.
    # notification.foreground: Notifications foreground color. Notifications slide in from the top of the window.

    # Quick Picker
    # pickerGroup.border: Quick picker color for grouping borders.
    theme["colors"]["pickerGroup.border"] = add_alpha("#FFFFFF", 0.1)
    # pickerGroup.foreground: Quick picker color for grouping labels.

    # Terminal Colors
    # terminal.ansiBlack: 'Black' ansi color in the terminal.
    if color_set.terminal.black:
        theme["colors"]["terminal.ansiBlack"] = color_set.terminal.black
    # terminal.ansiBlue: 'Blue' ansi color in the terminal.
    if color_set.terminal.blue:
        theme["colors"]["terminal.ansiBlue"] = color_set.terminal.blue
    # terminal.ansiBrightBlack: 'BrightBlack' ansi color in the terminal.
    if color_set.terminal.brightBlack:
        theme["colors"]["terminal.ansiBrightBlack"] = color_set.terminal.brightBlack
    # terminal.ansiBrightBlue: 'BrightBlue' ansi color in the terminal.
    if color_set.terminal.brightBlue:
        theme["colors"]["terminal.ansiBrightBlue"] = color_set.terminal.brightBlue
    # terminal.ansiBrightCyan: 'BrightCyan' ansi color in the terminal.
    if color_set.terminal.brightCyan:
        theme["colors"]["terminal.ansiBrightCyan"] = color_set.terminal.brightCyan
    # terminal.ansiBrightGreen: 'BrightGreen' ansi color in the terminal.
    if color_set.terminal.brightGreen:
        theme["colors"]["terminal.ansiBrightGreen"] = color_set.terminal.brightGreen
    # terminal.ansiBrightMagenta: 'BrightMagenta' ansi color in the terminal.
    if color_set.terminal.brightMagenta:
        theme["colors"]["terminal.ansiBrightMagenta"] = color_set.terminal.brightMagenta
    # terminal.ansiBrightRed: 'BrightRed' ansi color in the terminal.
    if color_set.terminal.brightRed:
        theme["colors"]["terminal.ansiBrightRed"] = color_set.terminal.brightRed
    # terminal.ansiBrightWhite: 'BrightWhite' ansi color in the terminal.
    if color_set.terminal.brightWhite:
        theme["colors"]["terminal.ansiBrightWhite"] = color_set.terminal.brightWhite
    # terminal.ansiBrightYellow: 'BrightYellow' ansi color in the terminal.
    if color_set.terminal.brightYellow:
        theme["colors"]["terminal.ansiBrightYellow"] = color_set.terminal.brightYellow
    # terminal.ansiCyan: 'Cyan' ansi color in the terminal.
    if color_set.terminal.cyan:
        theme["colors"]["terminal.ansiCyan"] = color_set.terminal.cyan
    # terminal.ansiGreen: 'Green' ansi color in the terminal.
    if color_set.terminal.green:
        theme["colors"]["terminal.ansiGreen"] = color_set.terminal.green
    # terminal.ansiMagenta: 'Magenta' ansi color in the terminal.
    if color_set.terminal.magenta:
        theme["colors"]["terminal.ansiMagenta"] = color_set.terminal.magenta
    # terminal.ansiRed: 'Red' ansi color in the terminal.
    if color_set.terminal.red:
        theme["colors"]["terminal.ansiRed"] = color_set.terminal.red
    # terminal.ansiWhite: 'White' ansi color in the terminal.
    if color_set.terminal.white:
        theme["colors"]["terminal.ansiWhite"] = color_set.terminal.white
    # terminal.ansiYellow: 'Yellow' ansi color in the terminal.
    if color_set.terminal.yellow:
        theme["colors"]["terminal.ansiYellow"] = color_set.terminal.yellow

    # Debug
    # debugToolBar.background: Debug toolbar background color.
    theme["colors"]["debugToolBar.background"] = background4

    theme["colors"]["selection.background"] = color_set.base.color1


class ColorTheme:
    def __init__(
        self,
        name: str,
        display_name: str,
        version: str,
        type: str = "dark",
        description: str = None,
        publisher: str = None,
        keywords: list = None,
        icon: str = None,
    ):
        self.name = name
        self.display_name = display_name
        self.version = version
        types = {"dark": "vs-dark", "light": "vs", "hc": "hc-black"}
        if type.lower() not in types:
            raise ValueError("Theme type should be either dark, light or hc")
        self.type = types[type.lower()]
        self.description = description
        self.publisher = publisher
        self.keywords = keywords
        self.icon = icon
        self.repository = None
        self.data = {
            "name": self.display_name,
            "type": "dark",
            "colors": {
                "editor.background": "#263238",
                "editor.foreground": "#eeffff",
                "activityBarBadge.background": "#007acc",
                "sideBarTitle.foreground": "#bbbbbb",
            },
            "tokenColors": [
                {
                    "name": "Comment",
                    "scope": ["comment", "punctuation.definition.comment"],
                    "settings": {"fontStyle": "italic", "foreground": "#546E7A"},
                },
                {
                    "name": "Variables",
                    "scope": ["variable", "string constant.other.placeholder"],
                    "settings": {"foreground": "#EEFFFF"},
                },
                {
                    "name": "Colors",
                    "scope": ["constant.other.color"],
                    "settings": {"foreground": "#ffffff"},
                },
                {
                    "name": "Invalid",
                    "scope": ["invalid", "invalid.illegal"],
                    "settings": {"foreground": "#FF5370"},
                },
                {
                    "name": "Keyword, Storage",
                    "scope": ["keyword", "storage.type", "storage.modifier"],
                    "settings": {"foreground": "#C792EA"},
                },
                {
                    "name": "Operator, Misc",
                    "scope": [
                        "keyword.control",
                        "constant.other.color",
                        "punctuation",
                        "meta.tag",
                        "punctuation.definition.tag",
                        "punctuation.separator.inheritance.php",
                        "punctuation.definition.tag.html",
                        "punctuation.definition.tag.begin.html",
                        "punctuation.definition.tag.end.html",
                        "punctuation.section.embedded",
                        "keyword.other.template",
                        "keyword.other.substitution",
                    ],
                    "settings": {"foreground": "#89DDFF"},
                },
                {
                    "name": "Tag",
                    "scope": [
                        "entity.name.tag",
                        "meta.tag.sgml",
                        "markup.deleted.git_gutter",
                    ],
                    "settings": {"foreground": "#f07178"},
                },
                {
                    "name": "Function, Special Method",
                    "scope": [
                        "entity.name.function",
                        "meta.function-call",
                        "variable.function",
                        "support.function",
                        "keyword.other.special-method",
                    ],
                    "settings": {"foreground": "#82AAFF"},
                },
                {
                    "name": "Block Level Variables",
                    "scope": ["meta.block variable.other"],
                    "settings": {"foreground": "#f07178"},
                },
                {
                    "name": "Other Variable, String Link",
                    "scope": ["support.other.variable", "string.other.link"],
                    "settings": {"foreground": "#f07178"},
                },
                {
                    "name": "Number, Constant, Function Argument, Tag Attribute, Embedded",
                    "scope": [
                        "constant.numeric",
                        "constant.language",
                        "support.constant",
                        "constant.character",
                        "constant.escape",
                        "variable.parameter",
                        "keyword.other.unit",
                        "keyword.other",
                    ],
                    "settings": {"foreground": "#F78C6C"},
                },
                {
                    "name": "String, Symbols, Inherited Class, Markup Heading",
                    "scope": [
                        "string",
                        "constant.other.symbol",
                        "constant.other.key",
                        "entity.other.inherited-class",
                        "markup.heading",
                        "markup.inserted.git_gutter",
                        "meta.group.braces.curly constant.other.object.key.js string.unquoted.label.js",
                    ],
                    "settings": {"foreground": "#C3E88D"},
                },
                {
                    "name": "Class, Support",
                    "scope": [
                        "entity.name",
                        "support.type",
                        "support.class",
                        "support.other.namespace.use.php",
                        "meta.use.php",
                        "support.other.namespace.php",
                        "markup.changed.git_gutter",
                        "support.type.sys-types",
                    ],
                    "settings": {"foreground": "#FFCB6B"},
                },
                {
                    "name": "Entity Types",
                    "scope": ["support.type"],
                    "settings": {"foreground": "#B2CCD6"},
                },
                {
                    "name": "CSS Class and Support",
                    "scope": [
                        "source.css support.type.property-name",
                        "source.sass support.type.property-name",
                        "source.scss support.type.property-name",
                        "source.less support.type.property-name",
                        "source.stylus support.type.property-name",
                        "source.postcss support.type.property-name",
                    ],
                    "settings": {"foreground": "#B2CCD6"},
                },
                {
                    "name": "Sub-methods",
                    "scope": [
                        "entity.name.module.js",
                        "variable.import.parameter.js",
                        "variable.other.class.js",
                    ],
                    "settings": {"foreground": "#FF5370"},
                },
                {
                    "name": "Language methods",
                    "scope": ["variable.language"],
                    "settings": {"fontStyle": "italic", "foreground": "#FF5370"},
                },
                {
                    "name": "entity.name.method.js",
                    "scope": ["entity.name.method.js"],
                    "settings": {"fontStyle": "italic", "foreground": "#82AAFF"},
                },
                {
                    "name": "meta.method.js",
                    "scope": [
                        "meta.class-method.js entity.name.function.js",
                        "variable.function.constructor",
                    ],
                    "settings": {"foreground": "#82AAFF"},
                },
                {
                    "name": "Attributes",
                    "scope": ["entity.other.attribute-name"],
                    "settings": {"foreground": "#C792EA"},
                },
                {
                    "name": "HTML Attributes",
                    "scope": [
                        "text.html.basic entity.other.attribute-name.html",
                        "text.html.basic entity.other.attribute-name",
                    ],
                    "settings": {"fontStyle": "italic", "foreground": "#FFCB6B"},
                },
                {
                    "name": "CSS Classes",
                    "scope": ["entity.other.attribute-name.class"],
                    "settings": {"foreground": "#FFCB6B"},
                },
                {
                    "name": "CSS ID's",
                    "scope": ["source.sass keyword.control"],
                    "settings": {"foreground": "#82AAFF"},
                },
                {
                    "name": "Inserted",
                    "scope": ["markup.inserted"],
                    "settings": {"foreground": "#C3E88D"},
                },
                {
                    "name": "Deleted",
                    "scope": ["markup.deleted"],
                    "settings": {"foreground": "#FF5370"},
                },
                {
                    "name": "Changed",
                    "scope": ["markup.changed"],
                    "settings": {"foreground": "#C792EA"},
                },
                {
                    "name": "Regular Expressions",
                    "scope": ["string.regexp"],
                    "settings": {"foreground": "#89DDFF"},
                },
                {
                    "name": "Escape Characters",
                    "scope": ["constant.character.escape"],
                    "settings": {"foreground": "#89DDFF"},
                },
                {
                    "name": "URL",
                    "scope": ["*url*", "*link*", "*uri*"],
                    "settings": {"fontStyle": "underline"},
                },
                {
                    "name": "Decorators",
                    "scope": [
                        "tag.decorator.js entity.name.tag.js",
                        "tag.decorator.js punctuation.definition.tag.js",
                    ],
                    "settings": {"fontStyle": "italic", "foreground": "#82AAFF"},
                },
                {
                    "name": "ES7 Bind Operator",
                    "scope": [
                        "source.js constant.other.object.key.js string.unquoted.label.js"
                    ],
                    "settings": {"fontStyle": "italic", "foreground": "#FF5370"},
                },
                {
                    "name": "JSON Key - Level 0",
                    "scope": [
                        "source.json meta.structure.dictionary.json support.type.property-name.json"
                    ],
                    "settings": {"foreground": "#C792EA"},
                },
                {
                    "name": "JSON Key - Level 1",
                    "scope": [
                        "source.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json support.type.property-name.json"
                    ],
                    "settings": {"foreground": "#FFCB6B"},
                },
                {
                    "name": "JSON Key - Level 2",
                    "scope": [
                        "source.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json support.type.property-name.json"
                    ],
                    "settings": {"foreground": "#F78C6C"},
                },
                {
                    "name": "JSON Key - Level 3",
                    "scope": [
                        "source.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json support.type.property-name.json"
                    ],
                    "settings": {"foreground": "#FF5370"},
                },
                {
                    "name": "JSON Key - Level 4",
                    "scope": [
                        "source.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json support.type.property-name.json"
                    ],
                    "settings": {"foreground": "#C17E70"},
                },
                {
                    "name": "JSON Key - Level 5",
                    "scope": [
                        "source.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json support.type.property-name.json"
                    ],
                    "settings": {"foreground": "#82AAFF"},
                },
                {
                    "name": "JSON Key - Level 6",
                    "scope": [
                        "source.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json support.type.property-name.json"
                    ],
                    "settings": {"foreground": "#f07178"},
                },
                {
                    "name": "JSON Key - Level 7",
                    "scope": [
                        "source.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json support.type.property-name.json"
                    ],
                    "settings": {"foreground": "#C792EA"},
                },
                {
                    "name": "JSON Key - Level 8",
                    "scope": [
                        "source.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json meta.structure.dictionary.value.json meta.structure.dictionary.json support.type.property-name.json"
                    ],
                    "settings": {"foreground": "#C3E88D"},
                },
                {
                    "name": "Markdown - Plain",
                    "scope": [
                        "text.html.markdown",
                        "punctuation.definition.list_item.markdown",
                    ],
                    "settings": {"foreground": "#EEFFFF"},
                },
                {
                    "name": "Markdown - Markup Raw Inline",
                    "scope": ["text.html.markdown markup.inline.raw.markdown"],
                    "settings": {"foreground": "#C792EA"},
                },
                {
                    "name": "Markdown - Markup Raw Inline Punctuation",
                    "scope": [
                        "text.html.markdown markup.inline.raw.markdown punctuation.definition.raw.markdown"
                    ],
                    "settings": {"foreground": "#65737E"},
                },
                {
                    "name": "Markdown - Heading",
                    "scope": [
                        "markdown.heading",
                        "markup.heading | markup.heading entity.name",
                        "markup.heading.markdown punctuation.definition.heading.markdown",
                    ],
                    "settings": {"foreground": "#C3E88D"},
                },
                {
                    "name": "Markup - Italic",
                    "scope": ["markup.italic"],
                    "settings": {"fontStyle": "italic", "foreground": "#f07178"},
                },
                {
                    "name": "Markup - Bold",
                    "scope": ["markup.bold", "markup.bold string"],
                    "settings": {"fontStyle": "bold", "foreground": "#f07178"},
                },
                {
                    "name": "Markup - Bold-Italic",
                    "scope": [
                        "markup.bold markup.italic",
                        "markup.italic markup.bold",
                        "markup.quote markup.bold",
                        "markup.bold markup.italic string",
                        "markup.italic markup.bold string",
                        "markup.quote markup.bold string",
                    ],
                    "settings": {"fontStyle": "bold", "foreground": "#f07178"},
                },
                {
                    "name": "Markup - Underline",
                    "scope": ["markup.underline"],
                    "settings": {"fontStyle": "underline", "foreground": "#F78C6C"},
                },
                {
                    "name": "Markdown - Blockquote",
                    "scope": [
                        "markup.quote punctuation.definition.blockquote.markdown"
                    ],
                    "settings": {"foreground": "#65737E"},
                },
                {
                    "name": "Markup - Quote",
                    "scope": ["markup.quote"],
                    "settings": {"fontStyle": "italic"},
                },
                {
                    "name": "Markdown - Link",
                    "scope": ["string.other.link.title.markdown"],
                    "settings": {"foreground": "#82AAFF"},
                },
                {
                    "name": "Markdown - Link Description",
                    "scope": ["string.other.link.description.title.markdown"],
                    "settings": {"foreground": "#C792EA"},
                },
                {
                    "name": "Markdown - Link Anchor",
                    "scope": ["constant.other.reference.link.markdown"],
                    "settings": {"foreground": "#FFCB6B"},
                },
                {
                    "name": "Markup - Raw Block",
                    "scope": ["markup.raw.block"],
                    "settings": {"foreground": "#C792EA"},
                },
                {
                    "name": "Markdown - Raw Block Fenced",
                    "scope": ["markup.raw.block.fenced.markdown"],
                    "settings": {"foreground": "#00000050"},
                },
                {
                    "name": "Markdown - Fenced Bode Block",
                    "scope": ["punctuation.definition.fenced.markdown"],
                    "settings": {"foreground": "#00000050"},
                },
                {
                    "name": "Markdown - Fenced Bode Block Variable",
                    "scope": [
                        "markup.raw.block.fenced.markdown",
                        "variable.language.fenced.markdown",
                        "punctuation.section.class.end",
                    ],
                    "settings": {"foreground": "#EEFFFF"},
                },
                {
                    "name": "Markdown - Fenced Language",
                    "scope": ["variable.language.fenced.markdown"],
                    "settings": {"foreground": "#65737E"},
                },
                {
                    "name": "Markdown - Separator",
                    "scope": ["meta.separator"],
                    "settings": {"fontStyle": "bold", "foreground": "#65737E"},
                },
                {
                    "name": "Markup - Table",
                    "scope": ["markup.table"],
                    "settings": {"foreground": "#EEFFFF"},
                },
            ],
        }

    def set_repository(self, url: str, repo_type: str = "git") -> None:
        self.repository = {"type": repo_type, "url": url}

    def set_colors(self, background: str, foreground: str, accent_colors: list) -> None:
        base = BaseColorSet(background, foreground, accent_colors)
        color_set = ColorSet(base, type=self.type)
        self.data = generate_theme(self.display_name, color_set)
