
from http.cookies import SimpleCookie


class LoginProps:
    def __init__(self, id: str, password: str):
        self.id = id
        self.password = password


class Authorization:
    def __init__(self, user_id: str, user_login: str, role: str, token: str):
        self.user_id = user_id
        self.user_login = user_login
        self.role = role
        self.token = token


async def authorization(context, login_props: LoginProps) -> Authorization:
    login_page = await context.new_page()
    await login_page.goto(
        "https://smartid.ssu.ac.kr/Symtra_sso/smln.asp?apiReturnUrl=https%3A%2F%2Fclass.ssu.ac.kr%2Fxn-sso%2Fgw-cb.php",
        wait_until="domcontentloaded")
    await login_page.fill("#userid", login_props.id)
    await login_page.fill("#pwd", login_props.password)
    await login_page.click(".btn_login")
    await login_page.wait_for_url("https://lms.ssu.ac.kr/", wait_until="domcontentloaded")
    #login_page.evaluate(f"location.href='https://canvas.ssu.ac.kr/learningx/dashboard?user_login={login_props.id}&locale=ko'")

    await login_page.goto(f"https://canvas.ssu.ac.kr/learningx/dashboard?user_login={login_props.id}&locale=ko", wait_until="domcontentloaded")

    user_data = await login_page.evaluate("""
        () => {
            const root = document.querySelector("#root");
            return {
                user_id: root.dataset.user_id,
                user_login: root.dataset.user_login,
                role: root.dataset.role,
                cookies: document.cookie
            };
        }
    """)
    print(user_data)
    cookies = SimpleCookie()
    cookies.load(user_data['cookies'])
    token = cookies.get('xn_api_token').value

    if not (token and user_data.get('user_id') and user_data.get('user_login') and user_data.get('role')):
        raise Exception("Profile does not exist!")

    return Authorization(
        user_id=user_data['user_id'],
        user_login=user_data['user_login'],
        role=user_data['role'],
        token=token
    )
