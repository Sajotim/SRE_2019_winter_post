import req_var_HTTP
import compute_time
import send_var_SMTP
def main(ch):
    if ch=='1':
        req_var_HTTP.main()
        compute_time.main()
        re=send_var_SMTP.mail('domain.txt')
        if re:  print('Mail Suc')
        else:   print('Mail Failed')
    elif ch=='2':
        try:
            compute_time.main()
            re = send_var_SMTP.mail('domain.txt')
            if re:
                print('Mail Suc')
            else:
                print('Mail Failed')
        except IOError:
            print("file doesn't existed,check if first time.\n" )

if __name__ == '__main__':
    while 1:
        choice = input('enter 1 for New Process, 2 for Half\n')
        if not choice.isdigit(): continue
        if choice in ('1','2'): break
    print('choice:%c'%choice)
    main(choice)