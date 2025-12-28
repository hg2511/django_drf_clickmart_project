from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from carts.models import Cart, CartItems
from rest_framework.response import Response
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderItemSerializer
from orders.utils import send_order_notification
# Create your views here.

class PlaceOrderView(APIView):
    # the user must be logged in
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # first check if the cart is empty 
        cart = Cart.objects.get(user=request.user)
        # print("cart ==>", cart)
        # print("cart.items.count ==> ", cart.items.count())
        if not cart or cart.items.count() == 0:
            return Response({"error": "cart is empty."})

        # print("subtotal ==> ", cart.subtotal)
        # print("tax_amount ==> ", cart.tax_amount)
        # print("grand_total ==> ", cart.grand_total)
        # create the order
        order = Order.objects.create(
            user = request.user,
            subtotal = cart.subtotal,
            tax_amount = cart.tax_amount,
            grand_total = cart.grand_total,
        )


    # create the order item  
        for item in cart.items.all():
            OrderItem.objects.create(
                order = order,
                product = item.product,
                quantity = item.quantity,
                price = item.product.price,
                total_price = item.total_price
            )


    # clear the cart items
        cart.items.all().delete()
        cart.save()

    # notification email
        send_order_notification(order)


    # send the response to the frontend
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)