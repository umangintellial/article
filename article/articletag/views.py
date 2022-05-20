from django.shortcuts import redirect, render
from articletag.models import *
from articletag.forms import *
from django.db.models import Count


def usersignup(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/userlogin/')
            except:
                pass            
    return render(request,'usersignup.html')


def userlogin(request):
    error_message = []
    if request.method == 'POST':
        email = request.POST.get('user_email')
        password = request.POST.get('user_password')
        if password and email:
            user = User.objects.get(user_email = email)
            if user and user.user_password == password:
               request.session['user_id'] = user.id
               return redirect('/')
            else:
                error_message = 'username and password is invalid!'
    return render(request,'userlogin.html',{'error_message':error_message})


def userlogout(request):
    request.session.clear()
    return redirect('/userlogin/')


def homepage(request):
    user_id = request.session.get('user_id')
    if user_id:
        print("-----------------")
        article_list = []; dicts={}
        all_article =Article.objects.filter(article_status = '1')
        all_tags_gropby_count =ArticleTag.objects.values('tag_id','tag_id__tag_name').annotate(Count('tag_id'))
        article_byid = {}
        for article in all_article:
            article_list.append(article.id)
            article_byid[article.id]=article
        all_tag = ArticleTag.objects.filter(article_id__in = article_list).values("article_id","tag_id__tag_name")
        
        #get all_tags name for articaletag table join tag table for article_id = article_id
        for tag in all_tag:
            article_object = article_byid[tag["article_id"]]
            tmp_tag = dicts.get(article_object, [])
            tmp_tag.append(tag["tag_id__tag_name"])

            #create dict for return value for home page and key:is article_object and value: his tags
            dicts[article_object] = tmp_tag
        for without_tag in article_byid.values():
            if without_tag not in dicts:
                dicts[without_tag] = []
                
        return render(request,'homepage.html',{'data':dicts,'tag_group':all_tags_gropby_count})
    else:
        return redirect('/userlogin/')    


def createarticle(request):       
    form = ArticleForm()
    user_id = request.session.get('user_id')
    if user_id:
        if request.method == 'POST':   
            tag_name = request.POST.get('tag_name')
            form = ArticleForm(request.POST, request.FILES)
            if form.is_valid():              
                form.save()
               
                artical_instance = form.instance
                tag_create_and_assinge(artical_instance,tag_name)
                return redirect('/homepage/')
            else:
                print(form.errors)        
        return render(request,'createarticle.html',{'form':form,'user_id':user_id})
    else:
        return redirect('/userlogin/')

    
def editarticle(request,id):
    user_id = request.session.get('user_id')
    if user_id:
        form = ArticleForm()
        get_article = Article.objects.get(id=id)
        all_tag = list(ArticleTag.objects.filter(article_id = id).values_list("tag_id__tag_name", flat = True))
        all_tag = ArticleTag.objects.filter(article_id = id)
        all_tag = ArticleTag.objects.filter(article_id = id).values("tag_id__tag_name")
        tag =''
        for tag1 in all_tag:
            tag += '#'; tag += tag1['tag_id__tag_name']   
        if request.method == 'POST':
            form = ArticleForm(request.POST,request.FILES, instance=get_article)
            if len(form.changed_data) >0: 
                if form.is_valid():
                    form.save()
                else:    
                    print(form.errors)
            tag_name = request.POST.get('tag_name')
            if request.POST.get('tag_name') !=  tag:            
                ArticleTag.objects.filter(article_id = id).delete()
                tag_create_and_assinge(get_article,tag_name)
            return redirect('/homepage/')      
        return render(request,'editarticle.html',{'form':form,'article':get_article,'all_tag':tag})
    else:
        return redirect('/homepage/')    


# delete article process
def deletearticle(request,id):
    user_id = request.session.get('user_id')    
    if user_id:
        article = Article.objects.get(id = id)   
        article.delete()
        return redirect('/homepage/')
    else:
        return redirect('/homepage/') 


# this method used for tag split and ckeck tag in table
# after the check create a new tag for get a user side
def tag_create_and_assinge(artical_instance,tag_name):
    tag_name_list = tag_name.split("#")
    tag_name_list = [t for t in tag_name_list if len(t)!=0]
    tag_objects = Tag.objects.filter(tag_name__in=tag_name_list)
    tag_id_list = []
    for tag in tag_objects:
        tag_name_list.remove(tag.tag_name)
        tag_id_list.append(tag.id)
    
    #bulk create tags for tag table
    new_tag_list = []
    for tag in tag_name_list:
        t = Tag(tag_name=tag)
        new_tag_list.append(t)    
    Tag.objects.bulk_create(new_tag_list)
    
    #check tags name in tag table and after store in tag_id_list in tag_id
    new_created_tag = Tag.objects.filter(tag_name__in = tag_name_list)
    for tag in new_created_tag:
        tag_id_list.append(tag.id)
    artical_tag_object_list = []

    #bulk create record for articletag table
    for tag_single_id in tag_id_list:
        artical_tag_object_list.append(ArticleTag(tag_id_id=tag_single_id, article_id=artical_instance))
    ArticleTag.objects.bulk_create(artical_tag_object_list)         
                        
