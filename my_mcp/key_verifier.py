from fastmcp.server.auth import TokenVerifier,AccessToken

class KeyVerifier(TokenVerifier):

    async def verify_token(self, token: str) -> AccessToken | None:
        print("verify_token",token)
        #允许访问
        if token =="123456":
            return AccessToken(
                      token =token,
                      client_id="c8:95:ce:6c:94:df",#客户端唯一标识符
                      scopes=["write", "read"] #允许访问的权限信息
                     #scopes=[]
            )
        else:
            return None