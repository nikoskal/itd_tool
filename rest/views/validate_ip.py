from django.conf import settings


def valid_ip(client_ip):

    print "@@@@@@ call from client_ip:" + str(client_ip)

    try:
        settings.ALLOWED_IP
    except AttributeError:
        settings.ALLOWED_IP = None
        print "No IP based authorisation is implemented, please set ALLOWED_IP attribute in settings!!"
        return False

    print "@@@@@@ allowed_ip:" + str(settings.ALLOWED_IP)

    ip_list = list(settings.ALLOWED_IP)
    if '0.0.0.0' in ip_list:
        print "all ips are allowed", client_ip
        return True

    if client_ip in ip_list:
        print "list contains", client_ip
        return True
    else:
        return False

