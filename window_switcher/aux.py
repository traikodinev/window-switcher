from subprocess import check_output

def get_windows():
    wmctrl_out = check_output(['wmctrl', "-l"]).decode('utf-8')
    wmctrl_out = wmctrl_out.split('\n')
    all_windows = []

    # parse wmctrl output
    # reverse order of opening
    for window in wmctrl_out[::-1]:
        attrs = window.split()
        if len(attrs) < 4:
            continue

        id = attrs[0]
        name = ' '.join(attrs[3:])
        all_windows.append({
            'id': id,
            'name': name.lower()
        })

    return all_windows
