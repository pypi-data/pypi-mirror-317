# WeirdGitter

WeirdGitter is a simple yet useful Continious Delivery script. Work with git and .sh/.bat scripts

## Installation

`pip install WeirdGitter`

## Usage

Pull a repo with scripts. Scripts should be in Home Directory.
There should be a `weirdgitter.toml` in repo containing:
```toml
scripts=["script1", "script2"]
```

WeirdGitter will run these scripts on pull.

Firstly, executes text, then build, and finally deploy.

Create a runner `.py` file, using the docs or this example:

```python
from weirdgitter import WeirdGitter

wg = WeirdGitter(
    repo_path='/path/to/repo',
    branch='deploy',
    name='MyProjectName',
    run_on_start=True
)

wg.run_loop()
```

Then run script in background (Will work until an error (ideally forerver))

Custom callback:
```python
from weirdgitter import WeirdGitter, WeirdGitterResult

import telebot

TG_TOKEN = "YOUR TELEGRAM BOT TOKEN"
CHAT_ID = "YOUR CHAT ID"

bot = telebot.TeleBot(TG_TOKEN)

def callback(result: WeirdGitterResult):
    if result.result_status is None:
        return
    res = f"`{result.name} | {result.result_status}`\n"
    for k in result.updates:
        res += f"`{k}`: {result.__dict__[k]}\n"
    
    bot.send_message(
        chat_id=CHAT_ID,
        text=res
    )
```

Feel free to ask for suggestions and bugs through [email](mailto:nikitos99099@gmail.com)
