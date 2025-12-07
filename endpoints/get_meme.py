import allure
from endpoints.baseapi import BaseAPI
from endpoints.authorization import Authorization


class GetMeme(BaseAPI):

    @allure.step("Get all memes")
    def get_all_memes_endpoint(self):
        return self.send_request(method="GET", endpoint="/meme")

    @allure.step("Get meme by id")
    def get_meme_by_id_endpoint(self, meme_id):
        return self.send_request(method="GET", endpoint=f"/meme/{meme_id}")

# auth = Authorization()
#
# print(auth.authorization({"name": "test_user"}).json())
#
# print(BaseAPI.token)
#
# print(auth.is_alive(BaseAPI.token).text)
#
#
# meme_api = GetMeme()
# print(meme_api.get_all_memes().json())
#
# print(meme_api.get_meme_by_id(1703).json())
