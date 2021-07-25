# IPC Commands are in the following format
# {2digitcode}: {arg1}|||{arg2}|||{argn}

def _base(code, text, *args):
    print(f'{code}: {text}' + '|||'*bool(args) + '|||'.join(args), flush=True, end='')
    return text    

def show_info_message(text, *args):
    return _base('IM', text, *args)

def show_warn_message(text, *args):
    return _base('WM', text, *args)

def show_error_message(text, *args):
    return _base('EM', text, *args)

