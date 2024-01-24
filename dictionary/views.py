from unicodedata import name
from django.shortcuts import render, redirect

from numpy import double
import logging
logger = logging.getLogger(__name__)


from .utils import calculate_progress_rate

# Create your views here.
from .models import Word, UserWord

#クラスベースのビューを作るため
from django.views import View
from django.http import HttpResponse
from django.utils import timezone
from statistics import mean

#スクレイピングのコードをインポート
from . import getdef, word_test

import time
import random
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class word_frequency:
    id: int
    frequency: double







#Viewを継承してGET文、POST文の関数を作る
class SearchView(View):

    def get(self, request, *args, **kwargs):
        Parts = []
        Definitions = []
        Examples = []
        Synonyms = []
        count_p = 0

        if "search_word" in request.GET:
            if request.GET["search_word"] != "":
                word = request.GET["search_word"]
                dif = getdef.getdef(word)

            
                

            context = {"serch_word" : word,
                       "url" : "https://www.merriam-webster.com/dictionary/" + word,
                       "dif" : dif
                       }
        

            return render(request,"dictionary/results.html",context)

        return render(request,"dictionary/serch_base.html")

    def post(self, request, *args, **kwargs):
        pass

index   = SearchView.as_view()

def get_not_recently_reviewed_words(hours=24):
    # 現在から指定時間前のタイムスタンプを取得
    time_threshold = timezone.now() - timedelta(hours=hours)

    # 最後のレビュータイムが time_threshold よりも新しい単語を選択
    not_recently_reviewed_words = UserWord.objects.filter(last_review_time__lt=time_threshold)

    return not_recently_reviewed_words

def select_word_for_quiz():
    # 直近にレビューした単語を取得
    recently_reviewed_words = get_not_recently_reviewed_words()

    # frequency を計算（ここでは簡単のためランダムに選択）
    selected_word = random.choice(recently_reviewed_words)

    return selected_word


def example_test(request, start, end):
    request.session['start'] = start
    request.session['end'] = end

    # ここでテスト範囲を文字列としてセッションにも保存します
    range_str = f"{start}-{end}"
    request.session['selected_range'] = range_str
    print(f"Setting selected_range in session: {range_str}")


    print(f'Session start: {request.session["start"]}, end: {request.session["end"]}')  # Debugging line


    if 'question_number' not in request.session:
        request.session['question_number'] = 0

    question_number = request.session['question_number']

    if 'score' not in request.session or question_number == 0:
        request.session['score'] = 0


    if 'test_set' not in request.session or question_number == 0:
        test_set = [[[] for j in range(3)] for i in range(5)]  
        # ここで各種処理を行いtest_setを更新
        print("-----------------------------")
        test_word = []
        test_difs = []
        choices_pre = [5]
        choices = []
        test_set = [[[] for j in range(3)] for i in range(5)]
        frequencies = []
        change = True

        print("1----------------------1")
        

        for i in range(start, end):
            user_word, created = UserWord.objects.get_or_create(word=Word.objects.get(id=i))

            if created:
                user_word.correct_count = 0
                user_word.total_count = 0
                user_word.response_times = []
                user_word.last_answer_time = None
                user_word.save()

            # 正答率を計算
            accuracy_rate = user_word.correct_count / user_word.total_count if user_word.total_count > 0 else float('inf')

            # 平均回答時間を計算
            average_response_time = mean(user_word.response_times) if user_word.response_times else 0
            # 平均回答時間の正規化
            MAX_AVERAGE_RESPONSE_TIME = 60  # 60 seconds = 1 minute
            normalized_average_response_time = average_response_time / MAX_AVERAGE_RESPONSE_TIME

            # 最終回答からの経過時間を計算
            time_since_last_answer = (timezone.now() - user_word.last_answer_time).total_seconds() / 3600 if user_word.last_answer_time else float('inf')
            # 最終回答からの経過時間の正規化
            MAX_TIME_SINCE_LAST_ANSWER = 72  # 72 hours = 3 days
            normalized_time_since_last_answer = time_since_last_answer / MAX_TIME_SINCE_LAST_ANSWER

            # 正規化された変数を合計してfrequencyを計算
            frequency = accuracy_rate + normalized_average_response_time + normalized_time_since_last_answer

            # frequencyが3を超えないようにする（各変数が最大1で、3変数合計で最大3）
            frequency = min(frequency, 3)

            j = i % 100

            #出現頻度を定める値を、それぞれ格納
            frequencies.append(word_frequency(i, frequency))
            
        # print(frequencies)

        for i in range(len(frequencies)):
            if not change:  #交換の余地無しで繰り返し脱出
                break
            change = False  #交換の余地無しと仮定
            for j in range(len(frequencies) - i - 1):
                if frequencies[j].frequency < frequencies[j+1].frequency: #左の方が大きい場合
                    frequencies[j], frequencies[j+1] = frequencies[j+1], frequencies[j] #前後入れ替え
                    change = True #交換の余地ありかも

        # print(frequencies)
        
        for i in range(5):
            test_word.append(Word.objects.get(id = frequencies[i].id).word_name)



        for i in range(5):
            choices_pre = []
            choices_pre.append(test_word[i])

            while(len(choices_pre) < 4):
                b = random.randint(start, end)
                if(b != frequencies[i].id):
                    b_word = Word.objects.get(id = b).word_name
                    choices_pre.append(b_word)

            choices.append(choices_pre)

            print(choices_pre)

        

        for i in range(5):
            test_set[i][0] = test_word[i]

        for i in range(5):
            random.shuffle(choices[i])


        for i in range(5):
            test_set[i][2] = choices[i]


        
        print(test_word)
        print("2------------------------2")

        
        for i in range(len(test_word)):
            print(str(i) + "-------------------------")
            print(test_word[i])
            e_s = word_test.get_example(test_word[i])
            # print("e_s = ")
            # print(e_s)
            # e = random.choice(e_s)
            # print("e = " + e)
            test_difs.append(e_s)
            # print(test_difs)

        for i in range(5):
            test_set[i][1] = test_difs[i]

        for i in range(5):
            print(test_set[i][2])

        request.session['test_set'] = test_set  # test_setをセッションに保存
    else:
        test_set = request.session['test_set']  # 既にセッションにtest_setがある場合はそれを利用


    if question_number >= 5:
        del request.session['question_number']
        score = request.session.pop('score')  # スコアをセッションから取得し、セッションから削除
        return redirect('dictionary:quiz_done', score=score)  # スコアを渡してクイズ終了ページにリダイレクト
    
    message = request.session.pop('message', None)  # セッションからメッセージを取得し、セッションから削除


    question = test_set[question_number]

    request.session['correct_answer'] = question[0]

    print(test_set[question_number])

    range_param = request.GET.get('range')
    print(f"Range parameter in /test/101/200/ view: {range_param}") 


    context = {
        "question"   : question,
        'message': message,
        'question_number': question_number + 1
    }

    request.session['start_time'] = timezone.now().isoformat()

    return render(request, "dictionary/test.html", context)

        # print(a_word.name)
        

def answer(request):
    if request.method == 'POST':
        start_time = datetime.fromisoformat(request.session.get('start_time'))
        end_time = timezone.now()  # 終了時間を取得
        response_time = (end_time - start_time).total_seconds()  # レスポンス時間を計算

        choices = request.POST.getlist('choices')  # ユーザーの選択肢を取得
        correct_answer = request.session['correct_answer']  # 正解の情報をセッションから取得


        # ここで選択肢の正誤を判定
        correct = correct_answer in choices  # 選択肢が正解と一致するかチェック

        user_word = UserWord.objects.get(word=Word.objects.get(word_name=correct_answer))

        user_word.total_count += 1  # 合計回答数を更新

        # 正解か不正解かのメッセージをセッションに保存
        if correct: 
            request.session['message'] = 'Correct!'
            request.session['score'] += 1  # スコアを増やす
        else:  
            request.session['message'] = 'Incorrect'

        if len(user_word.response_times) >= 3:  # 既存の回答時間が3つ以上あれば
            user_word.response_times.pop(0)  # 最初の回答時間を削除
            user_word.response_times.append(response_time)  # 新たな回答時間を追加
        else:
            user_word.response_times.append(response_time)  # 新たな回答時間を追加

        user_word.last_answer_time = timezone.now()  # 最終回答時間を更新

        request.session['user_choices'] = choices  # ユーザーの選択肢をセッションに保存

        request.session['question_number'] += 1  # 問題番号を進める
        
        print("-----------------------")
        print(response_time)
        print("-----------------------")

        user_word.save()  # データベースに保存

        return redirect('dictionary:result')  # クイズページにリダイレクト
    


def result(request):
    choices = request.session.get('user_choices')  # ユーザーの選択肢をセッションから取得
    correct_answer = request.session.get('correct_answer')  # 正解の情報をセッションから取得
    message = request.session.get('message')  # メッセージをセッションから取得

    context = {
        'choices': choices,
        'correct_answer': correct_answer,
        'message': message,
    }

    return render(request, "dictionary/result.html", context)

class SelectTestRangeView(View):
    def get(self, request, *args, **kwargs):
        print("SelectTestRangeView get method called")  # <-- 追加
        range_param = request.GET.get('range')
        print(f"Range parameter: {range_param}")  # <-- 追加
        
        range_38 = [(i*100+1, (i+1)*100) for i in range(38)]
        progress_rate = calculate_progress_rate()

        selected_range = request.session.get('selected_range', '1-100')
        print(f"Getting selected_range from session: {selected_range}")

        return render(request, "dictionary/select_test_range.html", {'range_38': range_38, 'progress_rate': progress_rate, 'selected_range': selected_range})






def Menu(request):
    return render(request, "dictionary/frontpage.html")

def quiz_done(request, score):
    selected_range = request.session.get('selected_range', 'Not set')
    logger.info(f"Retrieved range from session: {selected_range}")
    
    return render(request, "dictionary/quiz_done.html", {'score': score})



def Test(request):
    return render(request, "dictionary/test.html")

