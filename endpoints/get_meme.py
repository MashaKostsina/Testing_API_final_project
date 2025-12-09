import allure
from endpoints.baseapi import BaseAPI


class GetMeme(BaseAPI):

    @allure.step("Get all memes")
    def get_all_memes_endpoint(self):
        return self.send_request(method="GET", endpoint="/meme")

    @allure.step("Get meme by id")
    def get_meme_by_id_endpoint(self, meme_id):
        return self.send_request(method="GET", endpoint=f"/meme/{meme_id}")
