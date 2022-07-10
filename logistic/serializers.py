from numpy import product
from rest_framework import serializers
from .models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description']

class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    class Meta:
        model = Stock
        fields = '__all__'

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        for i in validated_data:
            print(i)
        stock = super().create(validated_data)
        for position in positions:
            stock_product = StockProduct(
                stock=stock,
                product=position['product'], 
                quantity=position['quantity'],
                price=position['price'] 
            ).save()
        return stock

    def update(self, instance, validated_data):
        try:
            positions = validated_data.pop('positions')
        except KeyError:
            positions = []
        stock = super().update(instance, validated_data)
        for position in positions:
            stock_product = StockProduct.objects.get(stock=stock, product=position.get('product'))
            if position.get('quantity'):
                stock_product.quantity = position.get('quantity')
            if position.get('price'):
                stock_product.price = position.get('price')
            stock_product.save()
        return stock
