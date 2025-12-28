from django.urls import path
from users import views as UserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from products import views as ProductViews
from carts import views as CartViews
from orders import views as OrderViews

urlpatterns = [
    path("register/", UserView.RegisterView.as_view()),


    # Users APIs 
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("profile/", UserView.ProfileView.as_view()),

    # Products APIs
    # product list
    path("products/", ProductViews.ProductListView.as_view()),
    # product details
    path("products/<int:pk>/", ProductViews.ProductDetailView.as_view()),

    # Cart APIs
    path("cart/", CartViews.CartView.as_view()),

    # add to cart
    path("cart/add/", CartViews.AddToCartView.as_view()),

    # manage cart
    path("cart/items/<int:item_id>/", CartViews.ManageCartItemView.as_view()),

    # ORders
    path("orders/place/", OrderViews.PlaceOrderView.as_view())
]