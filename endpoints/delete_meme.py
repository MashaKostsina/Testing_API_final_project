import allure
from endpoints.baseapi import BaseAPI


class DeleteMeme(BaseAPI):

    @allure.step("Delete meme by id")
    def delete_meme_by_id(self, meme_id):
        return self.send_request(method="DELETE", endpoint=f"/meme/{meme_id}")
