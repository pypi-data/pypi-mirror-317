def new_options_launch(extensions=None):
    options_args = [
        "--disable-blink-features=AutomationControlled"
        # https://github.com/AtuboDad/playwright_stealth/issues/11#issuecomment-2061649665
    ]
    options = {
        'ignore_default_args': [
            "--enable-automation",
            # disable info bar: https://github.com/puppeteer/puppeteer/issues/1765#issuecomment-525225345
        ],
        'args': options_args,
    }
    options_args.extend([
        "--test-type=gpu",
        # disable info bar: https://bugs.chromium.org/p/chromium/issues/detail?id=537776

        "--disable-features=Translate",
        "--arc-disable-locale-sync",
        "--disable-sync",
        "--hide-crash-restore-bubble",
        "--no-default-browser-check",
    ])
    if extensions:
        paths = ','.join(extensions)
        options_args.extend([
            f"--disable-extensions-except={paths}",
            f"--load-extension={paths}",
        ])
    return options


def new_options_context():
    return dict(
        no_viewport=True,  # https://github.com/microsoft/playwright/issues/20721,
    )


def new_options(**kwargs):
    return new_options_launch(**kwargs), new_options_context()
