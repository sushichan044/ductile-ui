# This example requires the 'message_content' privileged intent to function.


import discord
from discord.ext import commands
from ductile import View, ViewObject
from ductile.controller import MessageableController
from ductile.pagination import Paginator
from ductile.ui import Button

PAGES = [
    "Page 1",
    "Page 2",
    "Page 3",
    "Page 4",
    "Page 5",
]


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user}")  # noqa: T201
        print("Ready!")  # noqa: T201


class PaginationView(View):
    def __init__(self) -> None:
        super().__init__()
        # initialize Paginator with source data and configuration.
        self.page = Paginator(self, source=PAGES, config={"page_size": 2})

    def render(self) -> ViewObject:
        # you can define component callback inside render method.
        e = discord.Embed(title="Pagination").add_field(
            name="page content",
            # you can get current page chunk data.
            value="\n".join(self.page.data),
        )

        # Define UI using ViewObject
        return ViewObject(
            embeds=[e],
            components=[
                Button(
                    "<<",
                    # you can use at_first and at_last property: returns whether the current page is the first/last page.
                    style={"color": "grey", "disabled": self.page.at_first},
                    # go_first, go_previous, go_next, go_last methods: go to first/previous/next/last page.
                    # these will automatically call `View.sync`.
                    on_click=self.page.go_first,
                ),
                Button(
                    "<",
                    style={"color": "grey", "disabled": self.page.at_first},
                    on_click=self.page.go_previous,
                ),
                Button(
                    # you can get current page number and max page number.
                    f"{self.page.current_page}/{self.page.max_page}",
                    style={"color": "grey", "disabled": True},
                ),
                Button(
                    ">",
                    style={"color": "grey", "disabled": self.page.at_last},
                    on_click=self.page.go_next,
                ),
                Button(
                    ">>",
                    style={"color": "grey", "disabled": self.page.at_last},
                    on_click=self.page.go_last,
                ),
            ],
        )


bot = Bot()


@bot.command(name="page")
async def send_counter(ctx: commands.Context) -> None:
    # use controller to send and control View.
    controller = MessageableController(PaginationView(), messageable=ctx.channel)
    await controller.send()


bot.run("MY_COOL_BOT_TOKEN")
