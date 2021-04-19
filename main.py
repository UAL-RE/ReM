#!/usr/bin/env python

import asyncio
import uvicorn

import readme_tool


# Multiple app solution running was based on:
#   https://gist.github.com/tenuki/ff67f87cba5c4c04fd08d9c800437477
class MyServer(uvicorn.Server):
    async def run(self, sockets=None):
        self.config.setup_event_loop()
        return await self.serve(sockets=sockets)


async def run():
    apps = []

    app_names = ['intake_form', 'figshare']
    app_port = list(range(8000, 8000+len(app_names)))
    for name, port in zip(app_names, app_port):
        config = uvicorn.Config(f"readme_tool.{name}:app", port=port)
        server = MyServer(config=config)
        apps.append(server.run())
    return await asyncio.gather(*apps)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    # uvicorn.run("readme_tool.intake_form:app", port=8000, reload=True)
