from rest_framework.views import APIView

from django.http import Http404
from django.contrib.auth import get_user_model

from . import authentications


UserModel = get_user_model()


class CsrfExemptSessionAPIView(APIView):
    authentication_classes = (authentications.CsrfExemptSessionAuthentication,)


class CustomerOwnedAPIViewMixin(CsrfExemptSessionAPIView):
    owner: UserModel

    def dispatch(self, request, *args, **kwargs):
        try:
            self.owner = UserModel.objects.get(pk=kwargs.get("owner"))
        except UserModel.DoesNotExist:
            raise Http404

        if not request.user.is_superuser and request.user != self.owner:
            raise Http404

        return super().dispatch(request, *args, **kwargs)


class SuperuserAPIViewMixin(CsrfExemptSessionAPIView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404

        return super().dispatch(request, *args, **kwargs)
