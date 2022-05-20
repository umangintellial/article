from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=50)
    user_email = models.EmailField()
    user_password = models.CharField(max_length=50)

    def __str__(self):
        return self.user_name

class Article(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    article_title = models.CharField(max_length=50)
    article_image = models.ImageField(upload_to='images/')
    article_content = models.CharField(max_length=1000)
    article_status = models.IntegerField()

    def __str__(self):
        return "{} - {} - {}".format(self.id, self.article_title, self.article_status)


class Tag(models.Model):
    tag_name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return "{} - {}".format(self.id, self.tag_name)


class ArticleTag(models.Model):
    article_id = models.ForeignKey(Article,on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag,on_delete=models.CASCADE)


    def __str__(self):
        return "{} - {} - {}".format(self.id, self.article_id, self.tag_id)



