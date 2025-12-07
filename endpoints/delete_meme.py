import allure
from endpoints.baseapi import BaseAPI
from endpoints.authorization import Authorization


class DeleteMeme(BaseAPI):

    @allure.step("Delete meme by id")
    def delete_meme_by_id(self, meme_id):
        return self.send_request(method="DELETE", endpoint=f"/meme/{meme_id}")


# auth = Authorization()
#
# print(auth.authorization({"name": "test_user"}).json())
#
# print(BaseAPI.token)
#
# print(auth.is_alive(BaseAPI.token).text)
#
# dele_m = DeleteMeme()
#
# print(dele_m.delete_meme_by_id(1703))