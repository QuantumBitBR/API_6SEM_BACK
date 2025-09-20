from repositories.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()


    def get_user_by_id(self, userid):
        response = self.user_repository.get_by_id(userid)
        
        if response == None:
            return {
                "error": "User not found"
            }, 404
        
        return response, 200

    def delete_data_user(self, userid):
        user, status = self.get_user_by_id(userid)
        if status == 404:
            return user, status
        
        response_delete = self.user_repository.delete_data_user(userid)

        if response_delete:
            return {}, 200
        return {
            "error": "Something went wrong"
        }, 500
