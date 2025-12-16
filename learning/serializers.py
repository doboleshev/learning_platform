from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import (
    User, Section, Material, Test, Question, Answer,
    TestResult, UserAnswer
)


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'role', 'phone', 'first_name', 'last_name']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone', 'first_name', 'last_name', 'avatar', 'created_at']
        read_only_fields = ['id', 'created_at']


class AnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для ответа"""
    class Meta:
        model = Answer
        fields = ['id', 'text', 'order']
        read_only_fields = ['id']


class AnswerDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для ответа с указанием правильности (только для владельца)"""
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct', 'order']
        read_only_fields = ['id']


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для вопроса (без правильных ответов)"""
    answers = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'points', 'order', 'answers']
        read_only_fields = ['id']


class QuestionDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для вопроса с правильными ответами (для владельца)"""
    answers = AnswerDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'points', 'order', 'answers']
        read_only_fields = ['id']


class TestSerializer(serializers.ModelSerializer):
    """Сериализатор для теста"""
    questions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'passing_score', 'material', 'questions_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_questions_count(self, obj):
        return obj.questions.count()


class TestDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детального просмотра теста"""
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'passing_score', 'material', 'questions', 'created_at']
        read_only_fields = ['id', 'created_at']


class TestDetailForOwnerSerializer(serializers.ModelSerializer):
    """Сериализатор для детального просмотра теста владельцем (с правильными ответами)"""
    questions = QuestionDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'passing_score', 'material', 'questions', 'created_at']
        read_only_fields = ['id', 'created_at']


class MaterialSerializer(serializers.ModelSerializer):
    """Сериализатор для материала"""
    has_test = serializers.SerializerMethodField()
    
    class Meta:
        model = Material
        fields = ['id', 'title', 'content', 'section', 'order', 'is_published', 'has_test', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_has_test(self, obj):
        return hasattr(obj, 'test')


class MaterialDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детального просмотра материала"""
    test = TestSerializer(read_only=True)
    
    class Meta:
        model = Material
        fields = ['id', 'title', 'content', 'section', 'order', 'is_published', 'test', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class SectionSerializer(serializers.ModelSerializer):
    """Сериализатор для раздела"""
    materials_count = serializers.SerializerMethodField()
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = Section
        fields = ['id', 'title', 'description', 'owner', 'owner_username', 'materials_count', 'is_published', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_materials_count(self, obj):
        return obj.materials.count()


class SectionDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детального просмотра раздела"""
    materials = MaterialSerializer(many=True, read_only=True)
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = Section
        fields = ['id', 'title', 'description', 'owner', 'owner_username', 'materials', 'is_published', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserAnswerSubmitSerializer(serializers.Serializer):
    """Сериализатор для отправки ответов на тест"""
    question_id = serializers.IntegerField()
    answer_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )


class TestSubmissionSerializer(serializers.Serializer):
    """Сериализатор для отправки теста"""
    answers = UserAnswerSubmitSerializer(many=True)


class UserAnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для ответа пользователя"""
    question_text = serializers.CharField(source='question.text', read_only=True)
    selected_answers_text = serializers.SerializerMethodField()
    
    class Meta:
        model = UserAnswer
        fields = ['id', 'question', 'question_text', 'selected_answers', 'selected_answers_text']
        read_only_fields = ['id']
    
    def get_selected_answers_text(self, obj):
        return [answer.text for answer in obj.selected_answers.all()]


class TestResultSerializer(serializers.ModelSerializer):
    """Сериализатор для результата теста"""
    test_title = serializers.CharField(source='test.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_answers = UserAnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = TestResult
        fields = ['id', 'test', 'test_title', 'user', 'user_username', 'score', 'is_passed', 'user_answers', 'completed_at']
        read_only_fields = ['id', 'score', 'is_passed', 'completed_at']
