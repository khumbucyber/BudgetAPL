#!/bin/bash

###変数定義
base_dir="/usr/src/BudgetAPL/BudgetReport/"
in_dir=${base_dir}"in_data/"
mst_dir=${base_dir}"mst/"
out_dir=${base_dir}"out_data/"

year_month_file=${mst_dir}"year_month.csv"
merge_file=${out_dir}"merge.csv"

rm ${merge_file}

cd ${in_dir}
file_array=($(ls 収入・支出詳細*))

header_flg=0

for file in ${file_array[@]}; do
	echo "処理中："${file}
	iconv -f SJIS ${file} > ${in_dir}"SJIS_"${file}
	year_month=`grep ${file} ${year_month_file} | cut -d , -f 2`
	fis_year=`grep ${file} ${year_month_file} | cut -d , -f 3`
	while read line
	do
		col_culc=`echo ${line} | cut -d , -f 1`
		if [ ${col_culc} = '"計算対象"' ]; then
			if [ ${header_flg} = 0 ]; then
				echo '"ファイル名","年度","年月","収支区分",'${line} >> ${merge_file}
				header_out_flg=1
			else
				echo "PG ERROR：通り得ないロジック"
			fi
		else
			col_amnt=`echo ${line} | cut -d , -f 4 | tr -d '"'`
			if [ ${col_amnt} -gt 0 ]; then
				inex_cat="in"
			else
				inex_cat="out"
			fi
			echo '"'${file}'","'${fis_year}'","'${year_month}'","'${inex_cat}'",'${line} >> ${merge_file}
		fi
	done < ${in_dir}"SJIS_"${file}
done

rm ${in_dir}"SJIS*"

echo "処理完了：${merge_file} を出力しました。BudgetReportにペーストし分析できます。"

exit 0
