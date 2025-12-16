from rest_framework import viewsets, status, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import (
    User, Section, Material, Test, Question, Answer,
    TestResult, UserAnswer
)
from .serializers import (
    UserRegistrationSerializer, UserSerializer,
    SectionSerializer, SectionDetailSerializer,
    MaterialSerializer, MaterialDetailSerializer,
    TestSerializer, TestDetailSerializer, TestDetailForOwnerSerializer,
    TestSubmissionSerializer, TestResultSerializer
)
from .permissions import (
    IsAdminOrReadOnly, IsOwnerOrReadOnly,
    IsTeacherOrReadOnly, IsStudentOrOwner
)


def api_root(request):
    """Главная страница API с информацией о доступных эндпоинтах"""
    return render(request, 'learning/index.html')


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для управления пользователями"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Регистрация нового пользователя"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Получение информации о текущем пользователе"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class SectionViewSet(viewsets.ModelViewSet):
    """ViewSet для управления разделами"""
    queryset = Section.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SectionDetailSerializer
        return SectionSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Section.objects.all()
        elif user.is_teacher:
            # Преподаватели видят свои разделы и опубликованные
            return Section.objects.filter(Q(owner=user) | Q(is_published=True))
        else:
            # Студенты видят только опубликованные разделы
            return Section.objects.filter(is_published=True)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MaterialViewSet(viewsets.ModelViewSet):
    """ViewSet для управления материалами"""
    queryset = Material.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MaterialDetailSerializer
        return MaterialSerializer
    
    def get_queryset(self):
        user = self.request.user
        section_id = self.request.query_params.get('section', None)
        queryset = Material.objects.all()
        
        if section_id:
            queryset = queryset.filter(section_id=section_id)
        
        if user.is_admin:
            return queryset
        elif user.is_teacher:
            # Преподаватели видят свои материалы и опубликованные
            return queryset.filter(
                Q(section__owner=user) | Q(is_published=True)
            )
        else:
            # Студенты видят только опубликованные материалы
            return queryset.filter(is_published=True)
    
    def perform_create(self, serializer):
        section = serializer.validated_data['section']
        # Проверяем, что пользователь является владельцем раздела
        if section.owner != self.request.user and not self.request.user.is_admin:
            raise PermissionDenied("Вы не являетесь владельцем этого раздела")
        serializer.save()


class TestViewSet(viewsets.ModelViewSet):
    """ViewSet для управления тестами"""
    queryset = Test.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            user = self.request.user
            test = self.get_object()
            # Если пользователь владелец материала, показываем правильные ответы
            if hasattr(test, 'material') and hasattr(test.material, 'section'):
                if test.material.section.owner == user or user.is_admin:
                    return TestDetailForOwnerSerializer
            return TestDetailSerializer
        return TestSerializer
    
    def get_queryset(self):
        user = self.request.user
        material_id = self.request.query_params.get('material', None)
        queryset = Test.objects.all()
        
        if material_id:
            queryset = queryset.filter(material_id=material_id)
        
        if user.is_admin:
            return queryset
        elif user.is_teacher:
            # Преподаватели видят свои тесты и тесты опубликованных материалов
            return queryset.filter(
                Q(material__section__owner=user) | Q(material__is_published=True)
            )
        else:
            # Студенты видят только тесты опубликованных материалов
            return queryset.filter(material__is_published=True)
    
    def perform_create(self, serializer):
        material = serializer.validated_data['material']
        # Проверяем, что пользователь является владельцем материала
        if material.section.owner != self.request.user and not self.request.user.is_admin:
            raise PermissionDenied("Вы не являетесь владельцем этого материала")
        serializer.save()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def submit(self, request, pk=None):
        """Отправка ответов на тест"""
        test = self.get_object()
        user = request.user
        
        # Проверяем, что материал опубликован
        if not test.material.is_published:
            return Response(
                {'error': 'Материал не опубликован'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Проверяем, не проходил ли пользователь тест ранее
        test_result, created = TestResult.objects.get_or_create(
            test=test,
            user=user,
            defaults={'score': 0, 'is_passed': False}
        )
        
        if not created:
            return Response(
                {'error': 'Вы уже проходили этот тест'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = TestSubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        answers_data = serializer.validated_data['answers']
        total_points = 0
        max_points = 0
        
        # Обрабатываем каждый ответ
        for answer_data in answers_data:
            question_id = answer_data['question_id']
            selected_answer_ids = answer_data['answer_ids']
            
            try:
                question = Question.objects.get(id=question_id, test=test)
            except Question.DoesNotExist:
                return Response(
                    {'error': f'Вопрос с id {question_id} не найден'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            max_points += question.points
            
            # Получаем выбранные ответы
            selected_answers = Answer.objects.filter(
                id__in=selected_answer_ids,
                question=question
            )
            
            if selected_answers.count() != len(selected_answer_ids):
                return Response(
                    {'error': f'Некоторые ответы для вопроса {question_id} не найдены'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Создаем запись ответа пользователя
            user_answer = UserAnswer.objects.create(
                test_result=test_result,
                question=question
            )
            user_answer.selected_answers.set(selected_answers)
            
            # Проверяем правильность ответа
            correct_answers = Answer.objects.filter(question=question, is_correct=True)
            correct_answer_ids = set(correct_answers.values_list('id', flat=True))
            selected_answer_ids_set = set(selected_answer_ids)
            
            if question.question_type == 'single':
                # Для одного ответа - должен быть выбран ровно один правильный
                if len(selected_answer_ids_set) == 1 and selected_answer_ids_set == correct_answer_ids:
                    total_points += question.points
            else:
                # Для нескольких ответов - все правильные должны быть выбраны и никаких лишних
                if selected_answer_ids_set == correct_answer_ids:
                    total_points += question.points
        
        # Вычисляем процент правильных ответов
        if max_points > 0:
            score = int((total_points / max_points) * 100)
        else:
            score = 0
        
        # Обновляем результат теста
        test_result.score = score
        test_result.is_passed = score >= test.passing_score
        test_result.save()
        
        return Response(
            TestResultSerializer(test_result).data,
            status=status.HTTP_201_CREATED
        )


class TestResultViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для просмотра результатов тестов"""
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        test_id = self.request.query_params.get('test', None)
        queryset = TestResult.objects.all()
        
        if test_id:
            queryset = queryset.filter(test_id=test_id)
        
        if user.is_admin:
            return queryset
        elif user.is_teacher:
            # Преподаватели видят результаты своих тестов
            return queryset.filter(test__material__section__owner=user)
        else:
            # Студенты видят только свои результаты
            return queryset.filter(user=user)
