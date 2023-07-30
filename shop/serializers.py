from rest_framework import serializers

from .models import Product, Favorite


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('user',)

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        if not request.user.is_staff:
            raise serializers.ValidationError('Можеть создать только админы')
        return super().create(validated_data)


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'image', )


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    

class FavoriteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('product', 'id')

        def get_favorite(self, obj):
            if obj.favorite:
                return obj.favorite
            return ''

        def to_representation(self, instance):
            rep = super().to_representation(instance)
            rep['favorite'] = self.get_favorite(instance)
            return rep
