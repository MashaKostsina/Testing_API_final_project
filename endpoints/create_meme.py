import allure
from endpoints.baseapi import BaseAPI


class CreateMeme(BaseAPI):

    @allure.step("Create a new meme")
    def create_new_meme(self, payload):
        return self.send_request(method="POST", endpoint="/meme", json=payload)
