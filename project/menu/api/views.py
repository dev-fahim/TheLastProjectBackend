import utils
from menu import models
from menu.api.serializers import MenuSerializer


class MenuListCreateAPIView(utils.OwnListCreateAPIView):

    own_serializer_class = MenuSerializer
    own_model = models.Menu


class MenuListRetrieveUpdateDestroyAPIView(utils.OwnRetrieveUpdateDestroyAPIView):

    own_serializer_class = MenuSerializer
    own_model = models.Menu
