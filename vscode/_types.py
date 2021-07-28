from .utils import *

class ActivityBar:
    """
    Content settings for the activity bar.
    """

    def __init__(self, id: str, title: str, icon: str) -> None:
        self.id = id
        self.title = title
        self.icon = icon


class StaticWebview:
    """
    Content settings for a Static Webview.
    """

    def __init__(self, id: str, html: str, title: str = None) -> None:
        self.id = id
        self.html = html
        self.title = title


class InputBoxOptions:
    """
    Options to configure the behavior of the input box UI.
    """

    def __init__(
        self,
        title: str = None,
        password: bool = None,
        ignore_focus_out: bool = None,
        prompt: str = None,
        place_holder: str = None,
        value: str = None,
    ) -> None:
        self.title = title
        self.password = password
        self.ignoreFocusOut = ignore_focus_out
        self.prompt = prompt
        self.placeHolder = place_holder
        self.value = value


class QuickPickOptions:
    """
    Options to configure the behavior of the quick pick UI.
    """

    def __init__(
        self,
        title: str = None,
        can_pick_many: bool = None,
        ignore_focus_out: bool = None,
        match_on_description: bool = None,
        place_holder: str = None,
        match_on_detail: bool = None,
    ) -> None:
        self.title = title
        self.canPickMany = can_pick_many
        self.ignoreFocusOut = ignore_focus_out
        self.matchOnDescription = match_on_description
        self.placeHolder = place_holder
        self.matchOnDetail = match_on_detail

class QuickPickItem:
    """
    Content settings for a Quick Pick Item.
    """

    def __init__(self, label: str = None, detail: str = None, description: str = None, **options) -> None:
        self.label = label
        self.detail = detail
        self.description = description
        self.__dict__.update(options)


class Undefined:
    """
    An instance of this class is returned everytime javascript returns undefined.
    """

    def __str__(self):
        return "undefined"

    def __bool__(self):
        return False

    def __eq__(self, other):
        return isinstance(other, self.__class__)


undefined = Undefined()

class Disposable:
    """
    Represents a type which can release resources, such as event listening or a timer.
    """
    def __init__(self, id):
        self.id = id

    def dispose(self):
        print(f'DI: {self.id}', flush=True, end='')
        
class Position:
    """
    Represents a line and character position, such as the position of the cursor.
    """
    def __init__(self, line:int, character: int):
        self.line = line
        self.character = character

    @staticmethod
    def from_dict(data: dict):
        pos = Position(0,0)
        pos.__dict__.update(data)
        return pos

    def __eq__(self, other):
        return self.line == other.line and self.character == other.character

    def __sub__(self, other):
        return self.compare(other)

    def __lt__(self, other):
        return self.line < other.line or (self.line == other.line and self.character < other.character)

    def __le__(self, other):
        return  self == other or self < other
    
    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other    
        
    def compare(self, other):
        return 1 if self > other else -1 if self < other else 0

    def __repr__(self):
        return f'{self.line}:{self.character}'
        
class Range:
    "A range represents an ordered pair of two positions. It is guaranteed that start.isBeforeOrEqual(end)"
    
    def __init__(self, start: Position, end: Position):
        self.start = start
        self.end = end

    @staticmethod
    def from_dict(data):
        return Range(Position.from_dict(data['start']),Position.from_dict(data['end']))
    
    @property
    def __dict__(self):
        return {'start': self.start.__dict__, 'end': self.end.__dict__}

    @property
    def is_empty(self):
        return self.start == self.end

    @property
    def in_single_line(self):
        return self.start.line == self.end.line

    def __repr__(self):
        return f'[{self.start},{self.end}]'

    def __eq__(self, other):
        return self.start == other.start and self.end == other

    def __contains__(self, other):
        if isinstance(other, Position):
            return self.start <= other <= self.end
        else:
            return self.start <= other.start and self.end >= other.end 

    def intersection(self, other):
        if self.end < other.start or other.end < self.start:
            return undefined
        
        start = max(self.start, other.start)
        end = min(self.end, other.end)

        return Range(start, end)

    def union(self, other):
        start = min(self.start, other.start)
        end = max(self.end, other.end)

        return Range(start, end)




class TextDocument:
    """
    Represents a text document, such as a source file. Text documents have lines and knowledge about an underlying resource like a file.
    """
    def __init__(self, data):
        self.__dict__.update(data)

    def get_text(self, location: Range = None) -> str:
        """
        Get the text of this document. A substring can be retrieved by providing a range. The range will be adjusted.
        """
        if location is not None:
            if isinstance(location, Range):
                location = location.__dict__
            location = json.dumps(location)
            print(f'GT: {location}', flush=True, end="")
        else:
            print('GT', flush=True, end="")

        return json_input()
    
    # TODO: TextDocument methods
