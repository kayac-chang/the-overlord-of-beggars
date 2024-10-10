import aiohttp

from .model import Response

USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"


async def get_access_token(mid_v: str) -> str:
    """
    get the access token from the open point

    POST https://lovefood.openpoint.com.tw/LoveFood/api/Auth/FrontendAuth/AccessToken?mid_v=$mid_v
    headers:
        - user-agent
    """

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"https://lovefood.openpoint.com.tw/LoveFood/api/Auth/FrontendAuth/AccessToken?mid_v={mid_v}",
            headers={"user-agent": USER_AGENT},
        ) as response:

            response_json = await response.json()

            res = Response[str].model_validate(response_json)

            return res.element
