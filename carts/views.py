from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItems
from rest_framework.response import Response
from carts.serializers import CartSerializer, CartItemSerializer
from products.models import Product
from rest_framework import status
# Create your views here.

class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # get or create the cart for the logged in users 
        cart, created = Cart.objects.get_or_create(user=request.user)
        # print("cart ==> ", cart)
        # print("created ==> ", created)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # lets take the input
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        if not product_id:
            return Response({"error": "product_id is required."})
        # get the product
        product = get_object_or_404(Product, id=product_id, is_active=True)
        # print("products ==> ", product)

        # get or create the cart
        # Final takeaway "_" = I’m intentionally ignoring this value. Get the cart for this user or create one; I don’t care if it was newly created.
        cart, _ = Cart.objects.get_or_create(user=request.user)

        # get or create the cart item
        item, created = CartItems.objects.get_or_create(cart=cart, product=product)

        if not created:
            item.quantity = item.quantity + int(quantity)
            item.save()
        
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ManageCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        # validate the payload
        if "change" not in request.data:
            return Response({"error": "Provide 'change' value."})
        
        change = int(request.data.get("change")) # change will be +1 or -1

        item = get_object_or_404(CartItems, pk=item_id, cart__user=request.user)
        product = item.product

        # check the stock for adding 
        if change > 0:
            if item.quantity + change > product.stock:
                return Response({"error": "Not enogh stock."})
            
        new_qty = item.quantity + change
        # change can be +1 or -1
        if new_qty <= 0:
            # remove item from cart
            item.delete()
            return Response({"success": "item is removed"})
        
        # save the new qty
        item.quantity = new_qty
        item.save()

        serializer = CartItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, item_id):
        item = get_object_or_404(CartItems, pk=item_id, cart__user=request.user)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)