from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from product.models import Post

User = get_user_model()




class Review(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор')
    post = models.ForeignKey(Post,
                                on_delete=models.CASCADE,
                                verbose_name='Товар')
    rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                                                            verbose_name='Рейтинг')

    def avr_rating(self):
        summ = 0
        ratings = Review.objects.filter(post=self)
        for rating in ratings:
            summ += rating.rate
        if len(ratings) > 0:
            return summ / len(ratings)
        else:
            return 'Нет рейтинга'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинг'

    def __str__(self):
        return f'Пост: {self.post}, Автор: {self.author}, Оценка: {self.rate}'
