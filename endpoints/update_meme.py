import allure
from endpoints.baseapi import BaseAPI


class UpdateMeme(BaseAPI):

    @allure.step("Update a new meme")
    def update_meme_endpoint(self, meme_id, payload):
        return self.send_request(method="PUT", endpoint=f"/meme/{meme_id}", json=payload)
