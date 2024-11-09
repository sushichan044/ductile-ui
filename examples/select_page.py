# This example requires the 'message_content' privileged intent to function.


from typing import Literal

import discord
from discord.ext import commands
from typing_extensions import TypeIs

from ductile import State, View, ViewObject
from ductile.controller import MessageableController
from ductile.ui import Button, Select


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user}")  # noqa: T201
        print("Ready!")  # noqa: T201


def is_page_value(value: str) -> TypeIs[Literal["1", "2", "3", "4"]]:
    return value in {"1", "2", "3", "4"}


class SelectView(View):
    def __init__(self) -> None:
        super().__init__()
        # you can set generic type annotation implicitly.
        self.current_page = State[Literal["1", "2", "3", "4"]]("1", self)
        self.disabled = State(False, self)  # noqa: FBT003

    def render(self) -> ViewObject:
        pages = {"1": "Page content 1", "2": "Page content 2", "3": "Page content 3", "4": "Page content 4"}

        # self.current_page() is equivalent to self.current_page.get_state()
        e = discord.Embed(title="Multi-Page Sample", description=pages[self.current_page()])

        async def handle_select(interaction: discord.Interaction, values: list[str]) -> None:
            await interaction.response.defer()

            new_value = p if is_page_value(p := values[0]) else self.current_page()
            self.current_page.set_state(new_value)

        async def stop(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            self.disabled.set_state(True)
            # stop the view. this will cause View.wait to return.
            self.stop()

        # Define UI using ViewObject
        return ViewObject(
            embeds=[e],
            components=[
                Select(
                    config={"min_values": 1, "max_values": 1},
                    style={"disabled": self.disabled(), "placeholder": "Select page to see."},
                    options=[
                        {
                            "label": f"page{page}",  # label: option label, displayed to user
                            "value": page,  # value: option value, returned to callback
                            "default": self.current_page() == page,
                        }
                        for page in pages
                    ],
                    on_select=handle_select,
                ),
                Button("stop", style={"disabled": self.disabled(), "color": "red"}, on_click=stop),
            ],
        )


bot = Bot()


@bot.command(name="page")
async def send_select(ctx: commands.Context) -> None:
    # you can set view timeout in Controller constructor.
    controller = MessageableController(SelectView(), messageable=ctx.channel, timeout=None)
    await controller.send()


bot.run("MY_COOL_BOT_TOKEN")
