import allure
from endpoints.baseapi import BaseAPI
from endpoints.authorization import Authorization


class CreateMeme(BaseAPI):

    @allure.step("Create a new meme")
    def create_new_meme(self, payload):
        return self.send_request(method="POST", endpoint="/meme", json=payload)


# auth = Authorization()
# print(auth.authorization({"name": "test_user"}).json())
#
# print(BaseAPI.token)
#
# print(auth.is_alive(BaseAPI.token).text)
# create = CreateMeme()
#
# print(create.create_new_meme({"text": "Test meme text",
#                               "url": "https://example.com/meme.jpg",
#                               "tags": ["funny", "test"],
#                               "info": {"colors": ["red", "blue"],
#                                        "objects": ["text", "image"]}}).json())