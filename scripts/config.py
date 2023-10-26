SAFETY_LEVEL = None

def load_safety_level():
    global SAFETY_LEVEL
    if SAFETY_LEVEL is None:
        from modules.shared import cmd_opts
        if hasattr(cmd_opts, 'safety_level'):
            SAFETY_LEVEL = cmd_opts.safety_level
            # convert to lower case
            if SAFETY_LEVEL is not None:
                SAFETY_LEVEL = SAFETY_LEVEL.lower()
            else:
                SAFETY_LEVEL = 'safe'
        else:
            SAFETY_LEVEL = 'safe'
    return SAFETY_LEVEL