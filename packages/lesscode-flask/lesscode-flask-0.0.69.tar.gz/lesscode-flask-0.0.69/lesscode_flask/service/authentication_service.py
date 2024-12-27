import json
from urllib.parse import unquote

# from lesscode_flask.model.auth_client import AuthClient
# from lesscode_flask.model.auth_permission import AuthPermission
from lesscode_flask.model.user import ApiUser, User, AnonymousUser
# from lesscode_flask.service.auth_client_service import AuthClientService
# from lesscode_flask.service.auth_permission_service import AuthPermissionService
from lesscode_flask.utils.helpers import app_config
from lesscode_flask.utils.redis.redis_helper import RedisHelper


def get_gateway_user(user_json):
    """
    网关传输信息中获取用户信息
    :param apikey:
    :return:
    """
    if user_json:
        user_dict = json.loads(user_json)
        if user_dict and isinstance(user_dict, dict):
            if type(user_dict["roleIds"]) == str:
                user_dict["roleIds"] = json.loads(user_dict["roleIds"])
            user = User(
                id=user_dict["id"],
                username=user_dict["username"],
                display_name=unquote(user_dict["display_name"]),
                phone_no=user_dict["phone_no"],
                permissions=[],
                roleIds=user_dict["roleIds"],
                client_id=user_dict["client_id"]
            )
            return user
    return AnonymousUser()


def get_token_user(token):
    """
    根据token获取用户信息。

    该函数通过Redis缓存来获取用户信息。如果在缓存中找到了对应的用户数据，
    则会创建一个User对象并返回；如果没有找到，则返回一个AnonymousUser对象。

    参数:
    - token (str): 用户的令牌。

    返回:
    - User: 如果找到了用户信息，则返回一个User对象。
    - AnonymousUser: 如果没有找到用户信息，则返回一个AnonymousUser对象。
    """
    # 生成用户缓存键
    user_cache_key = f"oauth2:user:{token}"

    # 从Redis中获取用户数据
    user_dict = RedisHelper(app_config.get("REDIS_OAUTH_KEY", "redis")).sync_hgetall(user_cache_key)

    # 检查是否获取到了用户数据
    if user_dict:
        # 创建并返回User对象
        user = User(
            id=user_dict.get("id"),
            username=user_dict.get("username"),
            display_name=user_dict.get("display_name"),
            phone_no=user_dict.get("phone_no"),
            email=user_dict.get("email"),
            permissions=json.loads(user_dict.get("permissions")) if user_dict.get("permissions") is not None else [],
            client_id=user_dict.get("client_id")
        )
        return user
    # 如果没有获取到用户数据，返回AnonymousUser对象
    return AnonymousUser()


def get_api_user(apikey):
    """
    使用API key 获取用户信息
    :param apikey:
    :return:
    """
    cache_key = f"oauth2:apikey_user_info:{apikey}"
    # 优先从缓存中获取
    user_dict = RedisHelper(app_config.get("REDIS_OAUTH_KEY", "redis")).sync_hgetall(cache_key)
    if user_dict:
        user = ApiUser.to_obj(user_dict)
        return user
    # else:
    #     # 库里查询
    #     authClient = AuthClientService().get_one([AuthClient.client_id == apikey])
    #     if authClient:
    #         authPermission = AuthPermissionService().get_items([AuthPermission.client_id == authClient.id])
    #         permissions = [permission.resource_id for permission in authPermission]
    #         user = ApiUser(authClient.id, authClient.client_id, authClient.client_name, permissions)
    #         RedisHelper(app_config.get("REDIS_OAUTH_KEY", "redis")).sync_hset(cache_key,
    #                                                                           mapping=user.to_dict(),
    #                                                                           time=authClient.token_expires_in)
    #         return user
    return AnonymousUser()
