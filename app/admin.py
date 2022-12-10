from django.contrib import admin, messages
from .models import Test, Question, QuestionList, Answer, Profile


class QuestionListInline(admin.TabularInline):
    model = QuestionList


class AnswerInline(admin.TabularInline):
    model = Answer

    def save_formset(self, request, form, formset, change):
        formset.save()
        cnt_true, cnt_total = 0, 0
        if not change:
            for f in formset.forms:
                obj = f.instance
                obj.user = request.user
                obj.save()


class TestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'text']
    inlines = [QuestionListInline]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['name', 'text']
    inlines = [AnswerInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Profile)
