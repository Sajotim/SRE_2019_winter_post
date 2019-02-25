#适配Unix，更改文件中的路径,以及执行权限
mypath="/home/miseria/DomainQuery"
cd ${mypath}
python ${mypath}/compute_time.py >> ${mypath}/compute_time.py.log 2>&1
python ${mypath}/send_var_SMTP.py >> ${mypath}/send_var_SMTP.py.log 2>&1