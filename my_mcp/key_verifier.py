from fastmcp.server.auth import TokenVerifier,AccessToken

class KeyVerifier(TokenVerifier):

    async def verify_token(self, token: str) -> AccessToken | None:
        print("verify_token",token)
        #允许访问
        if token =="123456":
            return AccessToken(
                      token =token,
                      client_id="68-C6-AC-A2-D1-F0",#客户端唯一标识符
                      scopes=["write"] #允许访问的权限信息
                     #scopes=[]
            )
        else:
            return None