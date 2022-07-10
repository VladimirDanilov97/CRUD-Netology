from numpy import product
from rest_framework import serializers
from .models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта
    class Meta:
        model = Product
        fields = ['title', 'description']

class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    class Meta:
        model = Stock
        fields = '__all__'
    # настройте сериализатор для склада

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        for i in validated_data:
            print(i)
        # создаем склад по его параметрам
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
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        for position in positions:
            stock_product = StockProduct.objects.get(stock=stock, product=position.get('product'))
            if position.get('quantity'):
                stock_product.quantity = position.get('quantity')
            if position.get('price'):
                stock_product.price = position.get('price')
            stock_product.save()

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock
