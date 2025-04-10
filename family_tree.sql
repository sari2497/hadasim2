
DROP TABLE IF EXISTS family_Tree;
DROP TABLE IF EXISTS person;
--הגדרת הטבלאות והערכים שלהן
Create table person 
(
person_id varchar(20),
personal_name varchar(50),
family_name varchar(50),
Gender varchar(20) CHECK (Gender IN ('female', 'male')), 
father_id varchar(20),
mother_id varchar(20),
spouse_id varchar(20),
primary key (person_id)
);

Create table family_Tree
(
person_id varchar(20),
relative_id varchar(20),
connection_type varchar(50),
foreign key (person_id) references person(person_id)
);




-----------------------------------2-----------------------------------------
--person טריגר שפועל לפי חלוקה למקרים לאחר כל עדכון או הכנסה לטבלה--
create or replace function trigf1()
returns trigger as $$

begin
--קשר של אבא
	if new.father_id is not null and exists (select * from person p 
	                              where p.person_id = new.father_id)

    then
	    insert into family_Tree(person_id , relative_id , connection_type)
	    values (new.person_id, new.father_id, 'father');
	end if;
--קשר של אמא	
	if new.mother_id is not null and exists (select * from person p where p.person_id = new.mother_id)

    then
		insert into family_Tree(person_id , relative_id , connection_type)
		values (new.person_id, new.mother_id, 'mother');
	end if;
--קשר של אח		
	if new.father_id is not null and new.mother_id is not null and exists (select p.person_id from person p
	where new.person_id != p.person_id and new.father_id = p.father_id and new.mother_id = p.mother_id and p.gender = 'male')
	then
		insert into family_Tree(person_id , relative_id , connection_type)
		select new.person_id, p.person_id, 'brother'
        from person p
    	where p.person_id != new.person_id and p.gender = 'male' and p.person_id != new.father_id;
	end if;	
	
--קשר של אחות
	if new.father_id is not null and new.mother_id is not null and exists (select 1 from person p
	where new.person_id != p.person_id and (new.father_id = p.father_id 
	   or new.mother_id = p.mother_id) and p.gender = 'female')
	then
		insert into family_Tree(person_id , relative_id , connection_type)
		select new.person_id, p.person_id, 'sister'
    	from person p
    	where p.person_id != new.person_id and p.gender = 'female' and (new.father_id = p.father_id 
	   or new.mother_id = p.mother_id);
	end if;	
	
--קשר של בן
	if new.father_id is not null and new.mother_id is not null 
	then
		insert into family_Tree(person_id , relative_id , connection_type)
		select new.person_id, p.person_id, 'son'
    	from person p
    	where (new.person_id = p.father_id or new.person_id = p.mother_id) and p.gender = 'male' ;
	end if;	
	
--קשר של בת
	if new.father_id is not null and new.mother_id is not null 
	then
		insert into family_Tree(person_id , relative_id , connection_type)
		select new.person_id, p.person_id, 'daughter'
    	from person p
    	where (new.person_id = p.father_id or new.person_id = p.mother_id) and p.gender = 'female' ;
	end if;	

--קשר של בן זוג
	if new.gender = 'female' and new.spouse_id is not null 
	then
		insert into family_Tree(person_id , relative_id , connection_type)
		select new.person_id, p.person_id, 'boyfreind'
    	from person p
    	where p.person_id = new.spouse_id ;
	end if;	
	
--קשר של בת זוג
	if new.gender = 'male' and new.spouse_id is not null 
	then
		insert into family_Tree(person_id , relative_id , connection_type)
		select new.person_id, p.person_id, 'girlfreind'
    	from person p
    	where p.person_id = new.spouse_id ;
	end if;
	
--עדכון בן זוג עבור אדם שהן זוג שלו קיים המערכת אבל לא נמצא ברשומות שלו
	if new.spouse_id is not null and exists(select 1 from person p where new.spouse_id = p.person_id and p.spouse_id is null)
	then
		update person
		set spouse_id = new.person_id
    	where person_id = new.spouse_id;
   	end if;
	   
    return new;
	
end;
$$ language plpgsql;


create trigger T1
after insert or update on person
for each row
execute function trigf1();



insert into person
values('037335528', 'eli' , 'eisenbach', 'female', '456789123' , '789456123' , '037282480'),
('325462901', 'sari' , 'eisenbach', 'female', '037282480' , '037335528' , '123456789'),
('123456789', 'someone' , 'somebody', 'male' , '000000000' , '111111111' , '325462901'),
('037282480', 'yanki' , 'eisenbach', 'male', '555555555' , '666666666' , '037335528'), 
('7777777', 'non' , 'nan', 'male', '121212121' , '232323232' , null),
('326292725', 'brachi' , 'eisenbach', 'female', '037282480' , '037335528' , '7777777')

;
select * 
from family_Tree;

-- select * 
-- from person;

