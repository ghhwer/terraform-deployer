def options_present(expected, options):
    for opt in expected:
        if (opt not in options.keys()):
            raise ValueError(f'option {opt} was not present in .envfile or .envsecrets')