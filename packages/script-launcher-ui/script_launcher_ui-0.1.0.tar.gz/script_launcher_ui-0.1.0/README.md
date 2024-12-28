# Script Launcher UI

A simple PyQt6 based UI for script configuration and launching.

## Installation

```bash
pip install script-launcher-ui
```

## Usage

```python
from script_launcher_ui import ScriptLauncherUI

def on_submit():
    print("Configuration submitted")

ui = ScriptLauncherUI(style='light')
ui.add_label('Welcome to Script Launcher')
ui.add_text_input_module('script_path', 'Script Path', 'Enter script path')
ui.add_button("Submit", on_submit)
ui.start()
```

## Features

- Simple and intuitive UI
- Customizable styles
- Configuration saving and loading
- Easy integration with existing scripts

## License

MIT
