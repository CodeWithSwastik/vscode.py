class Undefined:
    def __str__(self):
        return "undefined"

    def __bool__(self):
        return False

    def __eq__(self, other):
        return isinstance(other, self.__class__)


undefined = Undefined()


class ActivityBar:
    def __init__(self, id, title, icon):
        self.id = id
        self.title = title
        self.icon = icon


class StaticWebview:
    def __init__(self, id, html, title=None):
        self.id = id
        self.html = html
        self.title = title


class InputBoxOptions:
    def __init__(
        self,
        title=None,
        password=None,
        ignore_focus_out=None,
        prompt=None,
        place_holder=None,
        value=None,
    ):
        self.title = title
        self.password = password
        self.ignoreFocusOut = ignore_focus_out
        self.prompt = prompt
        self.placeHolder = place_holder
        self.value = value


class QuickPickOptions:
    def __init__(
        self,
        title=None,
        can_pick_many=None,
        ignore_focus_out=None,
        match_on_description=None,
        place_holder=None,
        match_on_detail=None,
    ):
        self.title = title
        self.canPickMany = can_pick_many
        self.ignoreFocusOut = ignore_focus_out
        self.matchOnDescription = match_on_description
        self.placeHolder = place_holder
        self.matchOnDetail = match_on_detail
