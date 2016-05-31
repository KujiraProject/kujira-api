# -*- coding: utf-8 -*- 

class Add(Plugin):
    user_descr = "add"
    def is_valid(self):
        return True, None

    def can_run(self):
        return (True, None)

    def ceph_query(self):
        pass
