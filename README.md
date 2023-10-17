
# ductile-ui

![PyPI - Version](https://img.shields.io/pypi/v/ductile-ui)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ductile-ui)

A library provides declarative UI for [discord.py](https://github.com/Rapptz/discord.py).

## Features

- Declarative UI, inspired by [React](https://react.dev/).
- Component-oriented with State
- Fully typed

## Installation

**Python3.10 or higher is required**

**discord.py^2.2.0 is required; any compatibility under 2.1.x or 1.x is not guaranteed**

Using the latest stable release of discord.py is recommended

```bash
  pip install ductile-ui
```

## Usage/Examples

You can define component as return value of `View.render()`.
To store state, use `State`.

```python
# This example requires the 'message_content' privileged intent to function.


import random

import discord
from discord.ext import commands
from ductile import State, View, ViewObject
from ductile.controller import MessageableController
from ductile.ui import Button


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user}")
        print("Ready!")


class CounterView(View):
    def __init__(self) -> None:
        super().__init__()
        self.count = State(0, self)

    def render(self) -> ViewObject:
        e = discord.Embed(title="Counter", description=f"Count: {self.count.get_state()}")

        async def handle_increment(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            self.count.set_state(lambda x: x + 1)

        async def handle_decrement(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            self.count.set_state(lambda x: x - 1)

        async def stop(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            self.stop()

        # Define UI using ViewObject
        return ViewObject(
            embeds=[e],
            components=[
                Button("+1", style={"color": "blurple", "row": 0}, on_click=handle_increment),
                Button("-1", style={"color": "blurple", "row": 0}, on_click=handle_decrement),
                Button(
                    "random",
                    style={"color": "green", "row": 1},
                    # if you passed synchronous function to Button.on_click,
                    # library automatically calls `await interaction.response.defer()`.
                    on_click=lambda _: self.count.set_state(random.randint(0, 100)),
                ),
                Button("stop", style={"color": "red", "row": 1}, on_click=stop),
            ],
        )


bot = Bot()


@bot.command(name="counter")
async def send_counter(ctx: commands.Context) -> None:
    controller = MessageableController(CounterView(), messageable=ctx.channel)
    await controller.send()
    timed_out, states = await controller.wait()
    await ctx.send(f"Timed out: {timed_out}\nCount: {states['count']}")


bot.run("MY_COOL_BOT_TOKEN")

```
