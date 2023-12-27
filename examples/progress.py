import vscode
import asyncio

ext = vscode.Extension("Progress")


async def a_long_task():
    await asyncio.sleep(3)  # Simulate a long task
    return "Result!"


@ext.command()
async def long_task_1(ctx: vscode.Context):
    # Show a progress bar in the status bar
    async with ctx.window.progress("Running long task 1!") as p:
        res = await a_long_task()

    await ctx.window.show(vscode.InfoMessage("Long task 1 completed!"))


@ext.command()
async def long_task_2(ctx: vscode.Context):
    # Show a progress bar in the notification area
    # and notify the user of progress periodically
    async with ctx.window.progress(
        "Running long task 2!", vscode.ProgressLocation.Notification
    ) as p:
        await asyncio.sleep(3)
        for i in range(1, 10):
            await asyncio.sleep(1)
            await p.report(increment=10, message=f"{i*10}% Done")

    await ctx.window.show(vscode.InfoMessage("Long task 2 completed!"))


ext.run()
