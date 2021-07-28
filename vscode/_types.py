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
        
