import asyncio
import httpx
import os
from typing import Generator, AsyncGenerator, Union, Coroutine
from string import punctuation
from random import choice
from random import randint


class AsyncImager:
    """Asynchronous implementation of Imager (default provider)"""

    def __init__(
        self,
        timeout: int = 20,
        proxies: dict = {},
    ):
        self.image_gen_endpoint: str = "https://image.pollinations.ai/prompt/%(prompt)s"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
        }
        self.session = httpx.AsyncClient(
            headers=self.headers, timeout=timeout, proxies=proxies
        )
        self.timeout = timeout
        self.prompt: str = "AI-generated image - pytgpt"
        self.image_extension: str = "jpeg"

    async def generate(
        self, prompt: str, amount: int = 1, stream: bool = False, additives: bool = True
    ) -> list[bytes]:

        assert bool(prompt), "Prompt cannot be null"
        assert isinstance(
            amount, int
        ), f"Amount should be an integer only not {type(amount)}"
        assert amount > 0, "Amount should be greater than 0"
        ads = lambda: (
            ""
            if not additives
            else choice(punctuation)
            + choice(punctuation)
            + choice(punctuation)
            + choice(punctuation)
            + choice(punctuation)
        )

        async def for_stream():
            for _ in range(amount):
                resp = await self.session.get(
                    url=self.image_gen_endpoint % dict(prompt=prompt + ads()),
                    timeout=self.timeout,
                )
                resp.raise_for_status()
                yield resp.content

        async def for_non_stream():
            response = []

            async for image in for_stream():
                response.append(image)
            return response

        self.prompt = prompt
        return for_stream() if stream else await for_non_stream()

    async def save(
        self,
        response: list[bytes],
        name: str = None,
        dir: str = os.getcwd(),
        filenames_prefix: str = "",
    ) -> list[str]:

        assert isinstance(
            response, (list, AsyncGenerator)
        ), f"Response should be of {list} or {AsyncGenerator} types not {type(response)}"
        name = self.prompt if name is None else name

        filenames: list = []

        count = 0
        if isinstance(response, AsyncGenerator):
            new_response = []
            async for image in response:
                new_response.append(image)
            response = new_response

        for image in response:

            def complete_path():
                count_value = "" if count == 0 else f"_{count}"
                return os.path.join(
                    dir, name + count_value + "." + self.image_extension
                )

            while os.path.isfile(complete_path()):
                count += 1

            absolute_path_to_file = complete_path()
            filenames.append(filenames_prefix + os.path.split(absolute_path_to_file)[1])

            with open(absolute_path_to_file, "wb") as fh:
                fh.write(image)

        return filenames


class AsyncProdia(AsyncImager):

    def __init__(self, timeout: int = 30, proxies: dict[str, str] = {}):

        super().__init__(timeout=timeout, proxies=proxies)
        self.image_extension: str = "png"

    async def _generate(self, prompt: str) -> bytes:

        try:
            resp = await self.session.get(
                "https://api.prodia.com/generate",
                params={
                    "new": "true",
                    "prompt": prompt,
                    "model": "dreamshaper_6BakedVae.safetensors [114c8abb]",
                    "negative_prompt": "(nsfw:1.5),verybadimagenegative_v1.3, ng_deepnegative_v1_75t, (ugly face:0.5),cross-eyed,sketches, (worst quality:2), (low quality:2.1), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, bad anatomy, DeepNegative, facing away, tilted head, {Multiple people}, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worstquality, low quality, normal quality, jpegartifacts, signature, watermark, username, blurry, bad feet, cropped, poorly drawn hands, poorly drawn face, mutation, deformed, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, extra fingers, fewer digits, extra limbs, extra arms,extra legs, malformed limbs, fused fingers, too many fingers, long neck, cross-eyed,mutated hands, polar lowres, bad body, bad proportions, gross proportions, text, error, missing fingers, missing arms, missing legs, extra digit, extra arms, extra leg, extra foot, repeating hair",
                    "steps": "50",
                    "cfg": "9.5",
                    "seed": randint(1, 10000),
                    "sampler": "Euler",
                    "aspect_ratio": "square",
                },
                timeout=self.timeout,
            )
            data = resp.json()
            while True:
                resp = await self.session.get(
                    f"https://api.prodia.com/job/{data['job']}", timeout=self.timeout
                )
                json = resp.json()
                if json["status"] == "succeeded":
                    resp = await self.session.get(
                        f"https://images.prodia.xyz/{data['job']}.png?download=1",
                        timeout=self.timeout,
                    )
                    return resp.content

        except Exception as e:
            print(e)
            raise Exception("Unable to generate image") from e

    async def generate(
        self,
        prompt: str,
        amount: int = 1,
        stream: bool = False,
        additives: bool = False,
    ) -> list[bytes]:

        self.prompt = prompt
        get_prompt: object = lambda prompt: (
            f"prompt {randint(1, 10000)}" if additives else prompt
        )

        async def for_stream():
            for _ in range(amount):
                yield await self._generate(get_prompt(prompt))

        async def for_non_stream():
            resp = []
            for _ in range(amount):
                resp.append(await self._generate(get_prompt(prompt)))
            return resp

        return for_stream() if stream else await for_non_stream()


class Imager:
    """Default Image provider"""

    def __init__(
        self,
        timeout: int = 15,
        proxies: dict = {},
    ):

        self.loop = asyncio.get_event_loop()
        self.async_imager = AsyncImager(timeout=timeout, proxies=proxies)

    def generate(
        self, prompt: str, amount: int = 1, 
        stream: bool = False, 
        additives: bool = True
    ) -> list[bytes]:

        return self.loop.run_until_complete(
            self.async_imager.generate(
                prompt=prompt,
                amount=amount,
                stream=stream,
                additives=additives,
            )
        )

    def save(
        self,
        response: list[bytes],
        name: str = None,
        dir: str = os.getcwd(),
        filenames_prefix: str = "",
    ) -> list[str]:
    
        return self.loop.run_until_complete(
            self.async_imager.save(
                response=response,
                name=name, 
                dir=dir, 
                filenames_prefix=filenames_prefix
            )
        )


class Prodia(Imager):
    """
    This class provides methods for generating images based on prompts.
    """

    def __init__(self, 
                 timeout: int = 30, 
                 proxies: dict[str, str] = {}
                 ):

        super().__init__(timeout=timeout, proxies=proxies)
        self.image_extension: str = "png"
        self.loop = asyncio.get_event_loop()
        self.async_prodia = AsyncProdia(timeout=timeout, proxies=proxies)

    def _generate(
                    self,
                   prompt: str
                ) -> bytes:

        return self.loop.run_until_complete(self.async_prodia._generate(prompt=prompt))

    def generate(
        self,
        prompt: str,
        amount: int = 1,
        stream: bool = False,
        additives: bool = False,
    ) -> list[bytes]:
        
        return self.loop.run_until_complete(
            self.async_prodia.generate(
                prompt=prompt,
                amount=amount,
                stream=stream,
                additives=additives,
            )
        )


if __name__ == "__main__":
    bot = Prodia()
    resp = bot.generate("Coding bot ", 1, stream=False)
    bot.save(resp)
    
"""
from Pycodz.imager import Imager
img = Imager()
objec = img.generate("girl" , amount=1)
img.save(objec)
"""