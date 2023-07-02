from ast import literal_eval

from django.shortcuts import render, redirect, get_object_or_404
from .forms import StarCommentsForm
from django.urls import reverse
from django.core.paginator import Paginator
from .models import NaverMovie, StarComments
from django.contrib import messages
from collections import Counter
from konlpy.tag import Okt


def index(request):
    movielist = NaverMovie.objects.all().filter()
    q = request.GET.get('q', '')
    genre=''
    genrename='카테고리'
    ordername = '정렬하기'

    if q:
        movielist = movielist.filter(moviename__icontains=q)

    if request.GET.get('genre'):
        genre = request.GET.get('genre')
        movielist = NaverMovie.objects.all().filter(genre__icontains=genre)
        
        genrename =genre
        if genre == '멜로':
            genrename ='멜로/애정/로맨스'
        

    if request.GET.get('order'):
        if request.GET.get('order') == 'v':
            movielist = movielist.order_by('-valuation')
            ordername = '별점순'
        if request.GET.get('order') == 'od':
            movielist= movielist.order_by('-openingdate')
            ordername = '개봉날짜순'
        if request.GET.get('order') == 'n':
            movielist= movielist.order_by('moviename')
            ordername = '이름순'
    else:
        movielist = movielist.order_by('-openingdate')


    
    page= request.GET.get('page',1)
    paginator = Paginator(movielist, 25)  # 페이지당 50개씩 보여주기
    page_obj = paginator.get_page(page)

    

    return render(request,'index.html', {'movies': page_obj ,'q':q, 'genre':genre, 'genrename':genrename, 'ordername':ordername})


def detail(request, moviecode):
    movies = NaverMovie.objects.all().prefetch_related('starcomments_set').get(moviecode=moviecode)

    genrename='카테고리'
    ordername = '정렬하기'

    comment_set = movies.starcomments_set.all().exclude(content__exact='').order_by('-sctime')
    page= request.GET.get('page',1)
    paginator = Paginator(comment_set, 20) 
    page_obj = paginator.get_page(page)

    if request.method == 'POST':
        codeinst = NaverMovie.objects.get(moviecode=moviecode)    
        starscore = request.POST.get('star')
        if starscore:
            starscore = int(starscore)
        
        
        username =request.user.username
        create = StarComments.objects.create(
            userid = username,
            content = request.POST['content'],
            moviecode = codeinst,
            starscore = starscore,
        )
        return redirect(reverse('board:detail', kwargs={'moviecode':moviecode,})+f'#cmm')

    _wc = literal_eval(movies.wc)


    wc = [{"text":text, "weight": weight} for text, weight  in _wc.items()]


    return render(request, 'detail.html', {'movies':movies,'comment_set':page_obj, 'wc':wc, 'genrename':genrename, 'ordername':ordername, 'pageinfo':page})

def comment(request):
    codeinst = NaverMovie.objects.get(moviecode=int(request.POST['moviecode']))
    if request.method == 'POST':
        code = request.POST['moviecode']
        create = StarComments.objects.create(
            content = request.POST['content'],
            moviecode = codeinst,
            starscore = int(request.POST['star']),
        )
    return redirect(reverse('board:detail', kwargs={'moviecode':int(code) }))

def open(request):
    return render(request, 'open.html')


def wc(request):
    moviesall = NaverMovie.objects.all()

    for movies in moviesall:

        movies = NaverMovie.objects.all().prefetch_related('starcomments_set').get(moviecode=movies.moviecode)
        comment_set = movies.starcomments_set.all().exclude(content__exact='')
        textlist = []
        for review in comment_set:
            textlist.append(review.content)
        a = ''.join(textlist)

        stopwords = ['장면', '입니다', '영화', '진짜', '대해', '처음', '내내', '한번', '내용', '주인공', '서로', '보고', '하나', '정말', '최고', '이영화',
                     '같은', '있는', '이런', '없는', '평점', '없다', '모든', '그냥', '대한', '정도', '같다']
        okt = Okt()
        morpheme = okt.pos(a)
        noun_and_adj = []
        for word, tag in morpheme:
            if (tag in ['Noun', 'Adjective']) and (word not in stopwords):
                noun_and_adj.append(word)
        text = [n for n in noun_and_adj if len(n) > 1]
        count = Counter()
        count = Counter(text)
        result = dict(count.most_common(50))

        m = NaverMovie.objects.get(moviecode=movies.moviecode)
        m.wc = result
        m.save()


def wcm(request,moviecode): #함수화 해서 위랑 합쳐야됨

    movies = NaverMovie.objects.all().prefetch_related('starcomments_set').get(moviecode=moviecode)
    comment_set = movies.starcomments_set.all().exclude(content__exact='')
    textlist = []
    for review in comment_set:
        textlist.append(review.content)
    a= ''.join(textlist)

    stopwords = ['장면','입니다','영화','진짜','대해','처음','내내','한번','내용','주인공','서로','보고','하나','정말','최고','이영화','같은','있는','이런','없는','평점','없다','모든','그냥','대한','정도','같다']
    okt = Okt()
    morpheme = okt.pos(a)
    noun_and_adj = []
    for word, tag in morpheme:
        if (tag in ['Noun', 'Adjective']) and (word not in stopwords):
            noun_and_adj.append(word)
    text = [n for n in noun_and_adj if len(n) > 1]
    count = Counter()
    count = Counter(text)
    result = dict(count.most_common(50))

    m = NaverMovie.objects.get(moviecode=moviecode)
    m.wc = result
    m.save()

def heart(request, moviecode):
        movies = NaverMovie.objects.get(moviecode=moviecode)
        movies.heartcount += 1
        movies.save()
        return redirect(reverse('board:detail', kwargs={'moviecode':moviecode }))

def commentlike(request):
    moviecode = request.GET.get('moviecode')
    commentid = request.GET.get('commentid')
    if request.GET.get('page')=='':
        page = 1
    page = request.GET.get('page')
    comment = StarComments.objects.get(id=commentid)
    if request.GET.get('rc') == 'yes':
        comment.recomm += 1
    if request.GET.get('rc') == 'no':
        comment.unrecomm +=1
    comment.save()

    return redirect(reverse('board:detail', kwargs={'moviecode':moviecode,})+f'?page={page}#cmm')


# def board_update(request, board_id):
#     board = Board.objects.get(id=board_id)
#     form = BoardForm(instance=board)
#     if request.method == 'POST':
#         form = BoardForm(request.POST, instance=board)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('board:detail', args=[board_id]))

#     return render(request, 'board/update.html',{'form':form,'board':board})

# def board_delete(request, board_id):
#     board = Board.objects.get(id=board_id)
#     if request.method == 'POST':
#         board.delete()

#         return redirect(reverse('board:index'))

#     return render(request, 'board/delete.html', {'board':board})
