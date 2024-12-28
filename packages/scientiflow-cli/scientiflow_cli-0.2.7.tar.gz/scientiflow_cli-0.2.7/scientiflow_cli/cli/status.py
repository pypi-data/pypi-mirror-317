import pathlib



def user_is_authenticated() -> bool:
    """Check if user is authenticated."""
    home = pathlib.Path.home()
    token_file = home / ".scientiflow" / "key"

    if token_file.exists():
        jwt_token = token_file.read_text()

        #TODO: Implement token verification using backend
        if (jwt_token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwibG9naW5FeHBpcmVzIjoxNzMwMDc4NDU0fQ.Ppa9RsbMfMo7q0ZfhD9To_vArAkmESaDJtUVRmzm920"):

            return True

    return False



def get_auth_token() -> str:
    home = pathlib.Path.home()
    token_file = home / ".scientiflow" / "key"

    return token_file.read_text()