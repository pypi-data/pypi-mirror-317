# WeirdGitter

WeirdGitter is a simple yet useful Continious Delivery script. Work with git and .sh/.bat scripts

## Installation

`pip install WeirdGitter`

## Usage

Pull a repo with scripts. Scripts should be in Home Directory.
Scripts should be named `wg_test.sh`, `wg_build.sh`, `wg_deploy.sh` for unix and `wg_test.bat`, `wg_build.bat`, `wg_deploy.bat` for windows

Firstly, executes text, then build, and finally deploy.

Create a runner `.py` file, using the docs or this example:

```python
from weirdgitter import WeirdGitter

wg = WeirdGitter(
    repo_path='/path/to/repo',
    branch='deploy',
    name='MyProjectName'
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
