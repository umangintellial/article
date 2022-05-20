from django.contrib import admin
from articletag.models import *


# Register your models here.
class AdminUser(admin.ModelAdmin):
    list = ['user_name','user_email']

class AdminArticle(admin.ModelAdmin):
    list = ['article_title','article_content']

class AdminTag(admin.ModelAdmin):
    list = ['tag_name']

class AdminArticleTag(admin.ModelAdmin):
    list = ['article_id','tag_id']    


admin.site.register(User,AdminUser)
admin.site.register(Article,AdminArticle)
admin.site.register(Tag,AdminTag)
admin.site.register(ArticleTag,AdminArticleTag)