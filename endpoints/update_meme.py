import allure
from endpoints.baseapi import BaseAPI
from endpoints.authorization import Authorization


class UpdateMeme(BaseAPI):

    @allure.step("Update a new meme")
    def update_meme_endpoint(self, meme_id, payload):
        return self.send_request(method="PUT", endpoint=f"/meme/{meme_id}", json=payload)

# auth = Authorization()
#
# print(auth.authorization({"name": "test_user"}).json())
#
# print(BaseAPI.token)
#
# print(auth.is_alive(BaseAPI.token).text)
#
# update = UpdateMeme()
# print(update.update_meme(1703, {"id": 1703,
#                                                 "text": "Test meme text UPDATED",
#                                                 "url": "https://example.com/meme.jpg",
#                                                 "tags": ["funny", "test"],
#                                                 "info": {"colors": ["red", "blue"],
#                                                 "objects": ["text", "image"]}}).json())
