from db_contextmanager import CreateUserContextManager


with CreateUserContextManager() as cu:
    # first_name = input('firstname')
    # last_name = input('last name')
    # password = input('password')
    # phone = input('phone')
    # email = input('email')
    # role = input('role')
    cu.create_user(first_name='m', last_name='x', password='ABCabc123', phone='09114251202', email='a@mail.com', role=1)
    with CreateUserContextManager() as xxx:
        xxx.create_user(cur=cu.cur, con=cu.conn)
print(cu.err)
print(cu.result)
print(cu.user)
print(cu.cur)
print(cu.conn)