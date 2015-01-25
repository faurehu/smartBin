import db

add_cmds = '''
  CREATE TABLE IF NOT EXISTS `users` (
    `id` int unsigned auto_increment primary key,
    `name` varchar(255) not null unique,
    `created` timestamp not null default current_timestamp
  );
  CREATE TABLE IF NOT EXISTS `user_images` (
    `id` int unsigned auto_increment primary key,
    `user_id` int unsigned not null,
    img longblob not null,
    created timestamp not null default current_timestamp
  );
  CREATE TABLE IF NOT EXISTS `trash_dumps` (
    `id` int unsigned auto_increment primary key,
    height_offset double not null default 0,
    user_id int unsigned not null,
    user_mug longblob not null,
    created timestamp not null default current_timestamp
  );
  CREATE TABLE IF NOT EXISTS `trash_takeout` (
    `id` int unsigned auto_increment primary key,
    height_offset double not null default 0,
    created timestamp not null default current_timestamp,
    user_id int unsigned
  );
'''.split(";")

db = db.DB()

for cmd in add_cmds:
  db.query(cmd)
