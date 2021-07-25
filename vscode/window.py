# IPC Commands are in the following format
# {2digitcode}: {arg1}|||{arg2}|||{argn}

def show_info_message(text, *args):
    print(f'IM: {text}' + '|||'*bool(args) + '|||'.join(args), flush=True, end='')
    return text
