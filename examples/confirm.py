# This example requires the 'message_content' privileged intent to function.


import discord
from discord.ext import commands
from ductile import State, View, ViewObject
from ductile.controller import InteractionController, MessageableController
from ductile.ui import Button


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user}")  # noqa: T201
        print("Ready!")  # noqa: T201


class ConfirmView(View):
    def __init__(self) -> None:
        super().__init__()
        self.approved = State[bool | None](None, self)
        self.description = State("Are you sure?", self)

    def render(self) -> ViewObject:
        async def handle_approve(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            self.approved.set_state(True)
            self.stop()

        async def handle_deny(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            self.approved.set_state(False)
            self.stop()

        return ViewObject(
            embeds=[discord.Embed(title="Confirm", description=self.description())],
            components=[
                Button("yes", style={"color": "green", "disabled": self.approved() is not None}, on_click=handle_approve),
                Button("no", style={"color": "red", "disabled": self.approved() is not None}, on_click=handle_deny),
            ],
        )

    async def on_timeout(self) -> None:
        self.description.set_state("Timed out.")
        self.approved.set_state(False)
        self.stop()


class SomeBreakingView(View):
    def __init__(self) -> None:
        super().__init__()
        # you can set state value type with generic type annotation.
        self.approved = State[bool | None](None, self)

    def render(self) -> ViewObject:
        e = discord.Embed(
            title="Some Breaking View",
            description="With great power comes great responsibility.",
        )
        e.add_field(name="Approved", value="Not selected yet" if self.approved() is None else self.approved())

        async def handle_execute(interaction: discord.Interaction) -> None:
            await interaction.response.send_message("Executing...")
            await interaction.edit_original_response(content="Executed!")

        async def wait_for_confirm(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            # you can set timeout in Controller constructor.
            # View.on_timeout will be called when the timeout expires.
            view = ConfirmView()
            controller = InteractionController(view, interaction=interaction, timeout=60, ephemeral=True)
            await controller.send()
            await controller.wait()
            self.approved.set_state(view.approved())

        return ViewObject(
            embeds=[e],
            components=[
                Button(
                    "execute",
                    style={"color": "green", "disabled": self.approved() is not True},
                    on_click=handle_execute,
                ),
                Button(
                    "confirm",
                    style={"color": "grey", "disabled": self.approved() is not None},
                    on_click=wait_for_confirm,
                ),
            ],
        )


bot = Bot()


@bot.command(name="breaking")
async def send_counter(ctx: commands.Context) -> None:
    controller = MessageableController(SomeBreakingView(), messageable=ctx.channel)
    await controller.send()
    await controller.wait()


bot.run("MY_COOL_BOT_TOKEN")
