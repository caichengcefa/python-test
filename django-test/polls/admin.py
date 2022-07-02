from django.contrib import admin

from .models import Question,Choice

admin.site.register(Choice)

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

# 列表的形式
# class ChoiceInline(admin.TabularInline):
#     model = Choice

# 对于模型字段重新排列
class QuestionAdmin(admin.ModelAdmin):
    # fields = ['pub_date', 'question_text']
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    fieldsets = [
        ('Question information',               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'],  'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)