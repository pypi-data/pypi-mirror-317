import sys
import os
# from simple_query_builder import *
from querybuilder import *
from tablebuilder import *
# from simple_query_builder.querybuilder import *


print('=== Simple QueryBuilder Example ===')
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

qb = QueryBuilder(DataBase(), 'db.db')

"""
SELECT `id`, `name` FROM `cabs` UNION SELECT id, name FROM `printer_models` WHERE (`id` < 10);
-----------------
SELECT `name`, `age` FROM `clients` UNION SELECT `name`, `age` FROM `employees`;
-----------------
SELECT name, age, account_sum + account_sum * 0.1 AS total_sum FROM clients WHERE account_sum < 3000
UNION
SELECT name, age, account_sum + account_sum * 0.3 AS total_sum FROM clients WHERE account_sum >= 3000;
-----------------
SELECT `name`, `age`, account_sum + account_sum * 0.1 AS `total_sum` FROM `clients` WHERE (`account_sum` < 3000)
UNION
SELECT `name`, `age`, account_sum + account_sum * 0.3 AS `total_sum` FROM `clients` WHERE (`account_sum` >= 3000)
-----------------
q = qb.select('clients', ['name', 'age', {'total_sum': 'account_sum + account_sum * 0.1'}]).where([['account_sum', '<', 3000]])\
     .union()\
     .select('clients', ['name', 'age', {'total_sum': 'account_sum + account_sum * 0.3'}]).where([['account_sum', '>=', 3000]])
-----------------
=== !TODO! ===
SELECT * FROM `tab1` WHERE (`a` IS NOT NULL) AND (`b` = 5)
-----------------
Используя класс on conflict оператора insert, можно добавить новую строку, а при уже имеющейся с таким же значением по ключу, обновить.
create table vocabulary (word text primary key, count int default 1);
insert into vocabulary (word) values ('jovial') on conflict (word) do update set count = count + 1;

https://habr.com/ru/articles/528882/
-----------------
q = qb.select("'a' || ' 123 ' || null")
SELECT 'a' || ' 123 ' || null
-----------------
q = qb.select("strftime('%Y-%m-%d %H:%M', 'now')")
SELECT strftime('%Y-%m-%d %H:%M', 'now')
-----------------
q = qb.select("strftime('%d-%m-%Y %H:%M:%S', 1605961514, 'unixepoch', 'localtime')")
SELECT strftime('%d-%m-%Y %H:%M:%S', 1605961514, 'unixepoch', 'localtime')
-----------------
q = qb.select("generate_series(5, 100, 5)", ['value'])
SELECT value FROM generate_series(5, 100, 5)
"""
# res = qb.select('branches').where([['id', 1]]).all()
# sql = qb.select({'u': 'users'}, ['u.id', 'u.name']).where([['id', 10]])\
#     .union()\
#     .select('posts').where([['category_id', 25]])\
#     .get_sql()
# q = qb.select('cabs', ['id', 'name']).like('name', 'Каб%')\
#         .union_select('printer_models', True).where([['id', '<', 10]])
"""
SELECT `name`, `age`, account_sum + account_sum * 0.1 AS `total_sum` FROM `clients` WHERE (`account_sum` < 3000)
UNION
SELECT `name`, `age`, account_sum + account_sum * 0.3 AS `total_sum` FROM `clients` WHERE (`account_sum` >= 3000);
"""
q = qb.select('clients', ['name', 'age', {'total_sum': 'account_sum + account_sum * 0.1'}])\
     .where([['account_sum', '<', 3000]]).union()\
     .select('clients', ['name', 'age', {'total_sum': 'account_sum + account_sum * 0.3'}])\
     .where([['account_sum', '>=', 3000]])
# q = qb.select('clients', ['name', 'age']).where([['id', '<', 10]])\
#          .union_select('employees').where([['id', 1]])
# q = qb.select("generate_series(5, 100, 5)", ['value'])
# q = qb.select("substr('Hello world!', 1, 5) as 'str'")
# q = qb.select("1+5 as 'res'")
# q = qb.select('cabs', ['id + 10 AS new_id', "concat(`name`, '_qwe') AS new_name"]).where([['id', '<', 5]])
# q = qb.select('cabs', ['`id` + 10 AS new_id', "`name` || '_qwe' AS new_name"]).where([['id', '<', 5]])
# q = qb.select('cabs', [{'new_id': '`id` + 10'}, "`name` || '_qwe' AS new_name"]).where([['id', '<', 5]])
# q = qb.select('cabs', ['id', 'name']).where([['id', '<', 5]])
# q = qb.select('(' + qb.select('cabs').where([['id', '<', 10]]).get_sql() + ')', ['id', 'name']).where([['id', '<', 5]])
# q = qb.select(f'({qb.select('cabs').where([['id', '<', 10]]).get_sql()})', ['id', 'name']).where([['id', '<', 5]])
# q1 = qb.select('cabs').where([['id', '<', 10]])
# q = qb.select(f'({q1})', ['id', 'name']).where([['id', '<', 5]])
"""SELECT `id`, `name` FROM (SELECT * FROM `cabs` WHERE (`id` < 10)) WHERE (`id` < 5)"""
# q1 = qb.select('cabs').where([['id', '<', 10]])
# q1 = qb.select('categories').where([['parent_id', 0]])
# print(f'q1 = {q1}')
# print('SQL1 =', q1.get_sql())
# print('fields1 =', q1._fields)
# print('params1 =', q1.get_params())
# q = qb.select(f'{q1}', ['id', 'name']).where([['id', '<', 5]])
# q = qb.select(qb.select('categories').where([['parent_id', 0]]).get_sql(), ['id', 'name']).where([['id', '<=', 5]])
# q1 = qb.select('cabs').where([['id', '<', 10]])
# q = qb.select(['users', 'cabs'], ['users.id', 'cabs.name']).where([['id', '<', 5]])
# q = qb.insert('groups', {'name': 'Moderator', 'permissions': 'moderator'})
# q = qb.select("sqlite_version() as tm")
# q = qb.call('my_func()')
print('SQL =', q.get_sql())
print('fields =', q._fields)
print('params =', q.get_params())
if q.has_error():
    print(q.get_error_message())
# res = q.all()
# print(res, len(res))
# for i in res:
#     print(i)
exit()

tb = TableBuilder(DataBase(), 'db.db')

tb.table('users')
tb.increments('id')
tb.string('login', 100).unique().not_null()
tb.string('password').not_null()
tb.create()
# tb.save()

print(f'sql = {tb.get_sql()}')
if tb.get_error():
    print(f'error = {tb.get_error_message()}')
exit()

# res = qb.select('cabs').all()
# SELECT * FROM `users`
# print(res)

# res = qb.select('cabs').order_by('id', 'DESC').all()
# res = qb.select('cabs').order_by('id DESC').all()
# res = qb.select('cabs_printers', ['id', 'cab_id', 'printer_id', 'comment']).order_by(['cab_id', 'printer_id DESC']).all()
# SELECT * FROM `cabs` ORDER BY `id` DESC, `branch_id` ASC;

# res = qb.select({'cp': 'cabs_printers'}, ['id', 'cab_id', 'printer_id', 'comment']).group_by(['cab_id', 'printer_id']).all()
# print(qb._prepare_fieldlist(['cab_id', 'cp.cab_id', 'cp.cab_id AS cid', 'COUNT(*)', 'COUNT(cab_id)', 'SUM(cp.cab_id)']))
# print(qb.get_sql())
# print(res)
# for r in res:
#     print(r)

# printers = qb.select({'cp': 'cabs_printers'},
#             ['cp.id', 'cp.cab_id', {'cab_name': 'cb.name'}, 'cp.printer_id',
#             {'printer_name': 'p.name'}, {'cartridge_type': 'c.name'}, 'cp.comment'])\
#         .join({'cb': 'cabs'}, ['cp.cab_id', 'cb.id'])\
#         .join({'p': 'printer_models'}, ['cp.printer_id', 'p.id'])\
#         .join({'c': 'cartridge_types'}, 'p.cartridge_id=c.id')\
#         .where([['cp.printer_id', 2], 'or', ['cp.cab_id', [11, 12, 13]]])\
#         .all()
# .where([['cp.cab_id', 'in', [11, 12, 13]], 'or', ['cp.cab_id', '=', 5]])\
# param = qb.insert('params', [['param', 'value', 'comment'],
#                              ['asd', 'asd1', 'asd2'],
#                              ['qwe', 'qwe1', 'qwe2'],
#                              ['zxc', 'zxc1', 'zxc2'],
#                              ])
# param = qb.insert('groups', {'name': 'Moderator', 'permissions': 'moderator'})
# param = qb.insert({'g': 'groups'}, [['name', 'role'], ['Moderator', 'moderator'], ['Moderator2', 'moderator'], ['User', 'user'], ['User2', 'user']])

# param = qb.delete({'g': 'groups'}).where([['g.id', '=', 17]])
# results = qb.select('users').where([['id', '>', 1], 'and', ['group_id', 2]])
# results = qb.select('users').where([['id', 10]])
# results = qb.select('posts').where([['user_id', 3]]).offset(14).limit(7)
# results = qb.select({'b': 'branches'}, ['b.id', 'b.name'])\
#     .where([['b.id', '>', 1], 'and', ['b.parent_id', 1]])\
#     .order_by('b.id desc')
# qb.select('orders', {'month_num': 'MONTH(`created_at`)', 'total': 'SUM(`total`)'})\
#     .where([['YEAR(`created_at`)', 2020]])\
#     .group_by('month_num')\
#     .having([['total', 20000]])
# results = qb.select('posts', ['id', 'category', 'title'])\
#     .where([['views', '>=', 1000]])\
#     .group_by('category')
# results = qb.select('orders', {
#         'day_num': 'DAY(`created_at`)',
#         'month_num': 'MONTH(`created_at`)',
#         'total': 'SUM(`total`)'
#     })\
#     .where([['user_id', 10]])\
#     .group_by(['day_num', 'month_num'])
"""SELECT cp.id, cp.cab_id, cb.name, cp.printer_id, p.name as `printer_name`, c.id as `cartridge_id`,
c.name as `cartridge_type`, cp.comment
FROM `cabs_printers` AS `cp`
JOIN `cabs` AS `cb` ON cp.cab_id=cb.id
JOIN `printer_models` AS `p` ON cp.printer_id=p.id
JOIN `cartridge_types` AS `c` ON p.cartridge_id=c.id
GROUP BY printer_id, cartridge_id
ORDER BY cab_id, printer_id;"""
# printers = qb.select({'cp': 'cabs_printers'},
#             ['cp.id', 'cp.cab_id', {'cab_name': 'cb.name'}, 'cp.printer_id', {'cartridge_id': 'c.id'},
#             {'printer_name': 'p.name'}, {'cartridge_type': 'c.name'}, 'cp.comment'])\
#         .join({'cb': 'cabs'}, ['cp.cab_id', 'cb.id'])\
#         .join({'p': 'printer_models'}, ['cp.printer_id', 'p.id'])\
#         .join({'c': 'cartridge_types'}, ['p.cartridge_id', 'c.id'])\
#         .group_by(['cp.printer_id', 'cartridge_id'])\
#         .order_by(['cp.cab_id', 'cp.printer_id desc'])\
#         .all()
# qb.update('users', {
#         'username': 'John Doe',
#         'status': 'new status'
#     })\
#     .where([['id', 7]])\
#     .limit()
# qb.delete('users').where([['name', 'John']]).limit()
# qb.delete('comments').where([['user_id', 10]])
# qb.update({'u': 'users'}, {
#         'u.username': 'John Doe',
#         'g.status': 'new status'
#     })\
#     .where([['u.id', '=', 7]])\
#     .limit()\

# param = qb.select('orders', {'month_num': 'MONTH(`created_at`)', 'total': 'SUM(`total`)'})\
# 	.where([['YEAR(`created_at`)', '=', 2020]])\
# 	.group_by('month_num')\
# 	.having([['total', '>', 20000]])

# printers = qb.select().join(
#     {'p': 'printer_models', 'c': 'cartridge_types'},
#     {1: 'p.*', 'cartridge_type': 'c.name'},
#     ['p.cartridge_id', '=', 'c.id']
#     ).all()

# printers = qb.select('cabs').where([['branch_id', 2]]).pluck(0, 2)
# printers = qb.select('cabs').where([['branch_id', 2]]).pluck('id', 'name')
printers = qb.select('cabs').where([['branch_id', 2]]).column('name')
# printers = qb.select('cabs_printers').like('comment', 'у %').all()

print('sql =', qb.get_sql())
print('count =', qb.get_count())
if qb.get_error():
    print('error =', qb.get_error_message())
# print('printers =', printers)
for p in printers:
    print(p)

# param = qb.drop('users')

"""SELECT `cp`.`id`, `cp`.`cab_id`, `cb`.`name` AS `cab_name`, `cp`.`printer_id`," \
"`p`.`name` AS `printer_name`, `c`.`name` AS `cartridge_type`, `cp`.`comment`" \
"FROM `cabs_printers` AS `cp`" \
"INNER JOIN `cabs` AS `cb` ON `cp`.`cab_id` = `cb`.`id`" \
"INNER JOIN `printer_models` AS `p` ON `cp`.`printer_id` = `p`.`id`" \
"INNER JOIN `cartridge_types` AS `c` ON p.cartridge_id=c.id" \
"WHERE (`cp`.`cab_id` IN (?,?,?)) OR (`cp`.`cab_id` = ?);"""
