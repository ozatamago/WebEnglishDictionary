import pandas as pd
from .models import Word

from .models import UserWord

def calculate_progress_rate():
    learned_words_count = UserWord.objects.filter(correct_count__gte=3).count()
    total_words_count = 3800  # または Word.objects.count() で取得可能
    progress_rate = (learned_words_count / total_words_count) * 100
    return progress_rate


def import_words_from_excel(file_path):
    # Excelファイルの全てのシート名を取得
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names

    for sheet_name in sheet_names:
        # 各シートを読み込む（ヘッダー行をスキップしない）
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

        # 1列目を単語のID、2列目を単語として取得
        word_data = df.iloc[:, 0:2].values

        # Wordモデルに保存
        for word_id, word_name in word_data:
            Word.objects.create(id=word_id, word_name=word_name)
