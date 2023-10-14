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
        print(f"Logged in as {self.user}")  # noqa: T201
        print("Ready!")  # noqa: T201


class CounterView(View):
    def __init__(self) -> None:
        super().__init__()
        # state value type will be inferred from the initial value
        # self.count: State[int]
        self.count = State(0, self)

    def render(self) -> ViewObject:
        # you can define component callback inside render method.

        # use State.get_state to get the current value of the state.
        # also you can use State as callable to get the current value.
        # in this example, self.count() is equivalent to self.count.get_state()
        e = discord.Embed(title="Counter", description=f"Count: {self.count.get_state()}")

        async def handle_increment(interaction: discord.Interaction) -> None:
            # use defer if you only update State in callback.
            await interaction.response.defer()

            # if you pass callable to State.set_state, the callable will be called with the current value of the state.
            # in this example, x is the current value of the state.
            self.count.set_state(lambda x: x + 1)

        async def handle_decrement(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            self.count.set_state(lambda x: x - 1)

        async def handle_reset(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            # also you can pass new value to State.set_state.
            self.count.set_state(0)

        async def stop(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            # stop the view. this will cause View.wait to return.
            self.stop()

        # Define UI using ViewObject
        return ViewObject(
            embeds=[e],
            components=[
                # components are fully typed with TypedDict.
                # you can pass callback to Button.on_click.
                Button("+1", style={"color": "blurple", "row": 0}, on_click=handle_increment),
                Button("-1", style={"color": "blurple", "row": 0}, on_click=handle_decrement),
                Button(
                    "reset",
                    # you can set style with conditional expression.
                    style={"color": "grey", "row": 1, "disabled": self.count.get_state() == 0},
                    on_click=handle_reset,
                ),
                Button(
                    "random",
                    style={"color": "green", "row": 1},
                    # if you passed synchronous function to Button.on_click,
                    # library automatically calls `await interaction.response.defer()`.
                    on_click=lambda _: self.count.set_state(random.randint(0, 100)),  # noqa: S311
                ),
                Button("stop", style={"color": "red", "row": 1}, on_click=stop),
            ],
        )


bot = Bot()


@bot.command(name="counter")
async def send_counter(ctx: commands.Context) -> None:
    # use controller to send and control View.
    controller = MessageableController(CounterView(), messageable=ctx.channel)
    await controller.send()

    # await controller.wait returns a ViewResult, when View.stop is called.
    # you must call View.stop to get State out of the View.
    # ViewResult.timed_out is True if the View timed out.
    # ViewResult.states is a dict of State. the key is the name of instance attribute.
    timed_out, states = await controller.wait()
    await ctx.send(f"Timed out: {timed_out}\nCount: {states['count']}")


bot.run("MY_COOL_BOT_TOKEN")
