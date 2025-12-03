import allure
from endpoints.baseapi import BaseAPI
from authorization import Authorization


class GetMeme(BaseAPI):

    @allure.step("Get all memes")
    def get_all_memes(self):
        return self.send_request(method="GET", endpoint="/meme")

    @allure.step("Get meme by id")
    def get_meme_by_id(self, meme_id):
        return self.send_request(method="GET", endpoint=f"/meme/{meme_id}")

# auth = Authorization()
# auth.authorization({"name": "test"})
# print("Токен:", BaseAPI.token)
#
# meme_api = GetMeme()
# all_memes = meme_api.get_all_memes()
# print(all_memes.text)
