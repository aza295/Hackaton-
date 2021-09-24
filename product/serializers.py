from rest_framework import   serializers

from review.serializers import ReviewDetailSerializer
from .models import Category, Post, PostImage, Comment, Favorite



class CategorySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only =True)
    class Meta:
        model = Category
        fields = '__all__'


class PostSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','title','category','created_at','text',)

    """def to_representation отвечает за то в каком виде возвращается(Переопределяет) Responce"""

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data
        representation['author'] = instance.author.email
        representation['review'] = ReviewDetailSerializer(instance.review_set.all(), many=True).data
        representation['likes'] = instance.likes.count()
        representation['images'] = PostImageSerialzier(instance.images.all(), many=True,
                                                       context=self.context).data
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        post = Post.objects.create(**validated_data)
        return post

# -------------------------------------------------------------
#
class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['likes'] = instance.likes.count()
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return rep



# ------------------------------------


class PostImageSerialzier(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'

    def get_image_url(self,obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
            else:
                ulr = ''
            return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['image'] = self.get_image_url(instance)
        return representation







# --------------------------------------------------------------
class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(write_only=True,
                                                     queryset=Post.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        # fields = ('id','text','user','post')

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)



class FavoritePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('post','id')

    def get_favorite(self, obj,request):
        if obj.favorite and request.user and request.user == obj.user:
            return obj.favorite
        return ''
















