from product.models import Post
from .models import Review
from rest_framework import serializers



class CreateReviewSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Post.objects.all())
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, attrs):
        post = attrs.get('post')
        request = self.context.get('request')
        author = request.user
        if Review.objects.filter(post=post, author=author).exists():
            raise serializers.ValidationError('Нельзя поставить рейтинг дважды')
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)




class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
