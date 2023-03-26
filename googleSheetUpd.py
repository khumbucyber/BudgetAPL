import gspread
import json
import csv

###変数定義
#スプレッドシートキー
SPREADSHEET_KEY = '1Ahw6yg-VndkLyaNuo0yRw87iNsN2FJb1vu-yyKJq93A'       #BudgetReportファイル
#SPREADSHEET_KEY = '19oYRObLh-lsXzw4plqcz4NMs9165GBh4dWAdExuwvc4'        #python_testファイル

#sheet名
sheet_name='moneyforward_detail'

#カラム数
column_len=14

#カラム最右のアルファベット
column_to='N'

#inputファイル
input_file='/usr/src/BudgetAPL/BudgetReport/out_data/merge.csv'

###処理開始

#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials 

#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('/usr/src/BudgetAPL/BudgetReport/GoogleAPI/budget-276414-8c8482b6e248.json', scope)

#OAuth2の資格情報を使用してGoogle APIにログインします。
gs = gspread.authorize(credentials)

#共有設定したスプレッドシートのシート1を開く
workbook = gs.open_by_key(SPREADSHEET_KEY)
worksheet = workbook.worksheet(sheet_name)

#CSVファイルをOPEN (whth構文はファイルCLOSEを省略可能)
with open(input_file, newline="") as f:
	#CSVファイルを読み込み、readerオブジェクト作成
	reader = csv.reader(f, delimiter=",", quotechar='"')

	temp_list = []
	csv_file_len=0
	for row in reader:
		#readerから一時listに格納
		for column in range(column_len):
			temp_list.append(row[column])
		csv_file_len+=1
	
	#CSVファイルの列数・行数分のスプレッドシートupdate用リストを作成
	cell_list = worksheet.range('A1:'+column_to+str(csv_file_len))

	#一時listからスプレッドシートupdate用リストに格納
	i = 0
	for cell in cell_list:
		cell.value = temp_list[i]
		i+=1

#スプレッドシートのupdate実行
worksheet.update_cells(cell_list, value_input_option='USER_ENTERED')

#終了メッセージ
#print('処理完了：スプレッドシートファイル「'+workbook.getName()+'」シート名「'+sheet_name+'」を更新しました。件数＝'+str(csv_file_len)+'件')
print('スプレッドシート更新完了：件数＝'+str(csv_file_len)+'件')


