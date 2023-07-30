from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='products')
    title = models.CharField('Название', max_length=200)
    price = models.DecimalField('Цена', max_digits=15, decimal_places=2)
    description = models.TextField('Описание')
    image = models.ImageField('Фото', upload_to='shop', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = "Продукты"
        ordering = ['created_at']

    def __str__(self) -> str:
        return self.title


#так как у одного пользователя много избранных товаров, или наоборот у одного товара много избравших пользователей, то мы должны создать еще один класс для избранного
class Favorite(models.Model):
    product = models.ForeignKey(Product,
                             on_delete=models.CASCADE,
                             related_name='favorites')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favorites')
    is_favorite = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return f'{self.product} --> {self.user}'
