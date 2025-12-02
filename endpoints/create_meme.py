import allure
from endpoints.endpoint import Endpoint


class CreateMeme(Endpoint):

    @allure.step("Create a new meme"):
    def create_new_meme(self, payload):