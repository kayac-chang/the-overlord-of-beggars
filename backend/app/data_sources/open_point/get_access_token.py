import aiohttp
from pydantic import TypeAdapter

from .model import ErrorResponse, SuccessResponse
from .share import USER_AGENT


async def get_access_token(mid_v: str) -> str:
    """
    get the access token from the open point

    POST /Auth/FrontendAuth/AccessToken?mid_v=$mid_v
    user-agent: $user_agent
    """

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"https://lovefood.openpoint.com.tw/LoveFood/api/Auth/FrontendAuth/AccessToken",
            params={"mid_v": mid_v},
            headers={"user-agent": USER_AGENT},
        ) as response:

            response_json = await response.json()

            res = TypeAdapter(SuccessResponse[str] | ErrorResponse).validate_python(
                response_json
            )

            if not res.is_success:
                raise Exception(res.message)

            return res.element
