from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Section, Material, Test, Question, Answer, TestResult, UserAnswer


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'is_staff', 'created_at']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('role', 'phone', 'avatar')
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('role', 'phone', 'avatar', 'email')
        }),
    )


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'test', 'question_type', 'points', 'order']
    list_filter = ['question_type', 'test']
    search_fields = ['text', 'test__title']
    inlines = [AnswerInline]
    ordering = ['test', 'order']


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title', 'material', 'passing_score', 'created_at']
    list_filter = ['created_at', 'passing_score']
    search_fields = ['title', 'material__title']
    readonly_fields = ['created_at', 'updated_at']


class MaterialInline(admin.TabularInline):
    model = Material
    extra = 1
    fields = ['title', 'order', 'is_published']


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'is_published', 'created_at']
    list_filter = ['is_published', 'created_at', 'owner']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [MaterialInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'order', 'is_published', 'created_at']
    list_filter = ['is_published', 'created_at', 'section']
    search_fields = ['title', 'content', 'section__title']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(section__owner=request.user)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'is_correct', 'order']
    list_filter = ['is_correct', 'question__test']
    search_fields = ['text', 'question__text']


class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0
    readonly_fields = ['question', 'selected_answers']
    can_delete = False


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'test', 'score', 'is_passed', 'completed_at']
    list_filter = ['is_passed', 'completed_at', 'test']
    search_fields = ['user__username', 'test__title']
    readonly_fields = ['test', 'user', 'score', 'is_passed', 'completed_at']
    inlines = [UserAnswerInline]
    
    def has_add_permission(self, request):
        return False


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['test_result', 'question', 'get_selected_answers']
    list_filter = ['test_result__test', 'test_result__user']
    readonly_fields = ['test_result', 'question', 'selected_answers']
    
    def get_selected_answers(self, obj):
        return ", ".join([answer.text for answer in obj.selected_answers.all()])
    get_selected_answers.short_description = 'Выбранные ответы'
    
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
