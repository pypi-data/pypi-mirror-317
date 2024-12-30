# Recordwright [![PyPI version](https://badge.fury.io/py/recordwright.svg)](https://badge.fury.io/py/recordwright)

An extension for recording and playback of web interactions in [Playwright](https://pypi.python.org/pypi/playwright/).


While other interaction recorders generate code that you have to extend with your tests, Recordwright integrates the interactions into your test. The first time you run the test, the interaction is recorded, and the following time the recording is played back. If the interaction changes it can be simply recorded again. You do not need to rewrite the whole test.

Recordwright records every event and can also play back drag and drop operations.

## Installation

To install Recordwright
```bash
pip install recordwright
```

## Usage

The following example demonstates  the usage of Recordwright

```python
from playwright.sync_api import sync_playwright
from recordwright import install as install_recorder  # import Recordwright

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://demo.playwright.dev/todomvc")

        page.get_by_placeholder("What needs to be done?").wait_for()

        # injects the recording code into the page
        recorder = install_recorder(page)

        # if there is no replay file "todo.json, the recording is started and 
        # the result is stored in a replay file.
        # Otherwise the replay file will be replayed.
        recorder.interaction("todo", """
        - Click "What needs to be done"
        - Type "Test RecordWright"
        - Press Enter
        """)

        lis = page.get_by_test_id("todo-item")
        item = lis.first
        assert(item.inner_text() == "Test RecordWright")

        browser.close()
```
