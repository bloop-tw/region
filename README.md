# bloop-tw/region
Localization string manager for pycord.

## Preparing Localization Files
To use Region, you must first create a new directory, such as `translation`, as they're easy to find and understand.

To use multiple languages, create multiple files such as:

```jsonc
// translation/en-US.json
{
  "hello": "Hello, World!",
  "data": {
    "important": "I love chocolate!"
  }
}
```
```jsonc
// translation/zh-TW.json
{
  "hello": "你好，世界！",
  "data": {
    "important": "我喜歡巧克力！"
  }
}
```

Now, you have two different locale strings and objects.

## Usage
To use Region, you'll first need to initialize:

```python
from replit import db
from region import init, region

init(
  translation_path"translation/", # path to the translation files
  database="database": db, # your database, for here: Replit db
  langs=[
    # pairs of supported languages
    # NAME            CODE
    ("English (US)", "en-US"),
    ("中文（繁體）",  "zh-TW")
  ]
)
```

To use Region, initialize a new instance:

```python
reg = region(ctx)
```

...where the `ctx` represents any Pycord context, such as `SlashCommandContext` or `Message`... they're all handled!

To retrieve strings and objects based on user's locale:

```python
# Get a string:
reg("hello") # Hello, World! or 你好，世界！

# Get an object:
reg.obj("data")['important'] # I love chocolate! or 我喜歡巧克力！
```

## Example Bot
This is an example Pycord Bot:
```python
import discord

bot = discord.Bot(...) # other args

@bot.slash_command(name="hello")
async def hello(ctx):
  reg = region(ctx) # take the context and prepare to use localization strings

  await ctx.respond(
    reg('hello') # get the greeting message
  )

  fake_data = reg.obj("data") # retrieve an object & things that are not strings
  await ctx.channel.send("The important message was: " + fake_data['important']) # do anything with the object

bot.run('...')
```
