from werkzeug.security import safe_str_cmp
from models.user import UserModel

def authenticate(username, password):
    """
    Function that get called when a user calls the /auth endpoint with their username and password
    :param username: User's username {str}
    :param password: User's un-encrypted password {str}
    :return: a Usermodel Object if authentication was successful, None otherwise
    """
    user = UserModel.find_by_username(username)

    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    """
    Function that gets called when the user has already authenicated and FLask JWT verified their authorization header
    is correct
    :param payload: A dictionary with 'identity' key, which is the user id
    :return: A UserModel object
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)