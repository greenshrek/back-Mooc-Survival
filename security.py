from models.user import UserModel

def authenticate(username, password):
    user = UserModel.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
