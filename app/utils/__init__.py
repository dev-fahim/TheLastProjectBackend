from profile_app.models import (
    MainUserProfile,
    SubUserProfile
)
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import Response, APIView, status
from django.shortcuts import get_object_or_404


def get_main_user(user_model: User):

    try:
        return SubUserProfile.objects.get(user_id=user_model).select_related('main_user').main_user
    except ObjectDoesNotExist:
        return MainUserProfile.objects.get(user_id=user_model)


class OwnRetrieveUpdateDestroyAPIView(APIView):

    own_serializer_class = None
    own_model = None

    def get_object(self, pk):
        queryset = self.own_model
        obj = get_object_or_404(queryset, pk=pk, main_user_id=get_main_user(self.request.user))
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, pk, format=None):
        query = self.get_object(pk)
        serializer = self.own_serializer_class(query, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        query = self.get_object(pk)
        serializer = self.own_serializer_class(query, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OwnListCreateAPIView(APIView):

    own_model = None
    own_serializer_class = None

    def get_queryset(self):
        return self.own_model\
            .objects\
            .filter(main_user_id=get_main_user(self.request.user))\
            .order_by('-id')

    def get(self, *args, **kwargs):
        queryset = self.get_queryset()
        serialized = self.own_serializer_class(
            instance=queryset, many=True, context={'request': self.request}
        )
        return Response(serialized.data)

    def post(self, request, format=None):
        serializer = self.own_serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OwnListAPIView(APIView):

    own_model = None
    own_serializer_class = None

    def get_queryset(self):
        return self.own_model \
            .objects \
            .filter(main_user_id=get_main_user(self.request.user))

    def get(self, *args, **kwargs):
        queryset = self.get_queryset()
        serialized = self.own_serializer_class(
            instance=queryset, many=True, context={'request': self.request}
        )
        return Response(serialized.data)
