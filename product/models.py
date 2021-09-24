from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from account.models import User



class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(primary_key=True,)

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='posts')
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title



class PostImage(models.Model):
    image = models.ImageField(upload_to='posts',blank=True,null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='images')



# ------------------------------------------------------------------------------------------------------------

class Comment(models.Model):
    post = models.ForeignKey(Post,
                                    on_delete=models.CASCADE,
                                    related_name='comments',
                                    verbose_name='Публикация')

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='comments',
                             verbose_name='Автор')
    text = models.TextField('Текст',)
    created_at = models.DateTimeField('Дата создания',auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.post} -->{self.user}'


class Like(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='likes')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='likes')
    is_liked = models.BooleanField(default=False)














# -------------------------------------------

class Favorite(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='favorites')
    is_favorite = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Избранные'
        verbose_name_plural = 'Избранные'

