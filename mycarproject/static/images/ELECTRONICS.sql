CREATE TABLE gadgets (gadget_id serial primary key, gadget varchar(25), price real, del_date date);
select * from gadgets;
insert into gadgets(gadget, price, del_date)
values ('laptop', 1000000, current_date); 
truncate table gadgets;
update gadgets set gadget = 'monitor',  price = 500000 where gadget_id =6;
select * from gadgets order by gadget_id;
alter table gadgets rename column cost to gadget_cost;
ALTER TABLE gadgets
ALTER COLUMN gadget_cost TYPE MONEY;
ALTER TABLE gadgets
DROP COLUMN  del_date;/