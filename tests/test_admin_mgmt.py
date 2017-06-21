if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from itdtool.tasks import lsadmin_mgmt_task


def test_create_admin(admin_name, password, academic_entity):
    ls_admin = lsadmin_mgmt_task.create_admin(admin_name, password, academic_entity)
    print "test admin created:" + str(ls_admin)
    assert ls_admin


def test_remove_academic_admin(admin_name):
    print "admin to delete:"+ str(admin_name)
    result = lsadmin_mgmt_task.remove_admin(admin_name)
    print "admin to delete result:"+ str(result)
    assert result


def test_update_admin_pass(admin_name, newpass):
   print "admin to update:"+ str(admin_name)
   lsadmin_mgmt_task.update_admin_pass(admin_name, newpass)


def test_get_admin_academic(academic_name):
    print "get admin for academic ent:"+ str(academic_name)
    result = lsadmin_mgmt_task.get_admin_academic(academic_name)
    print "admin:"+ str(result)

if __name__ == "__main__":
    admin_name = "ntua_admin3"
    password = "pass"
    academic_entity = "ntua"

    test_create_admin(admin_name, password, academic_entity)


    # test_update_admin_pass("admin3", "newpass")
    # test_get_admin_academic(academic_entity)
    # test_remove_academic_admin("ntua_admin2")
