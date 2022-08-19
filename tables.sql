-- USE dummy_1;
-- CREATE TABLE DEMO(PREP1 INT);
-- DROP TABLE DEMO;
-- CREATE TABLE DUMM_MAIL(NAME VARCHAR(30), MAIL VARCHAR(30));
-- select* from DUMM_MAIL;
-- drop table dumm_mail;
create database Organ_Managment_Sys;
use Organ_Managment_Sys;

CREATE TABLE login(
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL
);

-- INSERT INTO login VALUES ('admin','admin');

CREATE TABLE User(
    User_ID int PRIMARY KEY,
    Name varchar(20) NOT NULL,
    Date_of_Birth date NOT NULL,
    Medical_insurance int,
    Medical_history varchar(20),
    Street varchar(20),
    City varchar(20),
    State varchar(20)
);

CREATE TABLE User_phone_no(
    User_ID int NOT NULL,
    phone_no varchar(15),
    FOREIGN KEY(User_ID) REFERENCES User(User_ID) ON DELETE CASCADE
);

CREATE TABLE Organization(
  Organization_ID int primary key,
  Organization_name varchar(20) NOT NULL,
  Location varchar(20),
  Government_approved int
  
);

CREATE TABLE Doctor(
  Doctor_ID int primary key,
  Doctor_Name varchar(20) NOT NULL,
  Department_Name varchar(20) NOT NULL,
  organization_ID int NOT NULL,
  FOREIGN KEY(organization_ID) REFERENCES Organization(organization_ID) ON DELETE CASCADE
  
);

CREATE TABLE Patient(
    Patient_ID int NOT NULL,
    organ_req varchar(20) NOT NULL,
    reason_of_procurement varchar(20),
    Doctor_ID int NOT NULL,
    User_ID int NOT NULL,
    FOREIGN KEY(User_ID) REFERENCES User(User_ID) ON DELETE CASCADE,
    FOREIGN KEY(Doctor_ID) REFERENCES Doctor(Doctor_ID) ON DELETE CASCADE,
    PRIMARY KEY(Patient_Id, organ_req)
);



CREATE TABLE Organization_phone_no(
  Organization_ID int NOT NULL,
  Phone_no varchar(15),
  FOREIGN KEY(Organization_ID) REFERENCES Organization(Organization_ID) ON DELETE CASCADE
);

CREATE TABLE Doctor_phone_no(
  Doctor_ID int NOT NULL,
  Phone_no varchar(15),
  FOREIGN KEY(Doctor_ID) REFERENCES Doctor(Doctor_ID) ON DELETE CASCADE
);

CREATE TABLE Organization_head(
  Organization_ID int NOT NULL,
  Employee_ID int NOT NULL,
  Name varchar(20) NOT NULL,
  Date_of_joining date NOT NULL,
  Term_length int NOT NULL,
  FOREIGN KEY(Organization_ID) REFERENCES Organization(Organization_ID) ON DELETE CASCADE,
  PRIMARY KEY(Organization_ID,Employee_ID)
);


create table log (
  querytime datetime,
  comment varchar(255)
);

delimiter //
create trigger ADD_DONOR_LOG
after insert
on Donor
for each row
begin
insert into log values
(now(), concat("Inserted new Donor", cast(new.Donor_Id as char)));
end //



create trigger UPD_DONOR_LOG
after update
on Donor
for each row
begin
insert into log values
(now(), concat("Updated Donor Details", cast(new.Donor_Id as char)));
end //



delimiter //
create trigger DEL_DONOR_LOG
after delete
on Donor
for each row
begin
insert into log values
(now(), concat("Deleted Donor ", cast(old.Donor_Id as char)));
end //


create trigger ADD_PATIENT_LOG
after insert
on Patient
for each row
begin
insert into log values
(now(), concat("Inserted new Patient ", cast(new.Patient_Id as char)));
end //

select* from User;
create trigger UPD_PATIENT_LOG
after update
on Patient
for each row
begin
insert into log values
(now(), concat("Updated Patient Details ", cast(new.Patient_Id as char)));
end //

create trigger DEL_PATIENT_LOG
after delete
on Donor
for each row
begin
insert into log values
(now(), concat("Deleted Patient ", cast(old.Donor_Id as char)));
end //



create trigger ADD_TRASACTION_LOG
after insert
on Transaction
for each row
begin
insert into log values
(now(), concat("Added Transaction :: Patient ID : ", cast(new.Patient_ID as char), "; Donor ID : " ,cast(new.Donor_ID as char)));
end //


--  Example Procedures 
delimiter //
CREATE procedure select_Login()
BEGIN
	SELECT * FROM login;
end; //
call select_Login();

  -- Procedure for removing
-- select* from User;
-- delete from User where User_ID = 3;


-- --------------------------------------------------------- Procedure to Remove Data from Table -----------------------------------------
-- Procedure to remove Data from User 
delimiter //
CREATE procedure remove_User( IN User_I_D int)
BEGIN
	delete from User where User_ID = User_I_D;
end; //
-- Remove Data from Child of User 
delimiter //
create trigger User_remov_Child before delete on User
for each row
begin
	delete from User_phone_no where User_ID = old.User_ID;
    delete from Donor where User_ID = old.User_ID;
    delete from Patient where User_ID = old.User_ID;
end //
call remove_User(5);
select* from User;



-- Procedure to remove Patient
delimiter //
CREATE procedure remove_Patient(IN Patient_I_D int, IN organ_required varchar(20)) 
begin
	delete from Patient where Patient_ID = Patient_I_D and organ_req = Organ_required;
end //
call remove_Patient(5,'Heart');
select* from Patient;


-- Procedure to remove Donor
delimiter //
CREATE procedure remove_Donor(IN Donor_I_D int, IN Organ_Dona varchar(20))
begin
	delete from Donor where Donor_ID = Donor_I_D and Organ_donated = Organ_Dona;
end //

-- select* from Donor;
-- select* from Organ_available;
delimiter //
create trigger Donor_remove_Child before delete on Donor
for each row
begin
	delete from Organ_available where old.Organ_ID = organ_id;
end //
call remove_Donor(5,'Kidney');
select* from Donor;




desc Donor;
desc Organ_available;


-- Procedure to remove Doctor
delimiter //
CREATE procedure remove_Doctor (IN Doctor_I_D int)
begin
	delete from doctor where Doctor_ID = Doctor_I_D;
end //
select* from Doctor;

call remove_Doctor(5);




-- Procedure to remove Organization
delimiter //
CREATE procedure remove_Organization(IN o_id int)
begin
	delete from Organization where Organization_ID = o_id;
end //

-- Trigger to remove data from child of Organization
delimiter //
CREATE trigger remove_Organization_child before delete on organization
for each row
begin
	delete from Organization_Head where Organization_ID = old.organization_ID;
	delete from Organization_Phone_no where Organization_ID = old.organization_ID;
    delete from Donor where Organization_ID = old.organization_ID;
	delete from Doctor where Organization_ID = old.organization_ID;
end //

call remove_Organization(4);

select* from Organization;



-- Procedure to remove Organization Head
delimiter //
CREATE procedure remove_Organization_Head(IN O_Id int, IN E_ID int)
begin
	delete from Organization_Head where Organization_ID = O_Id and Employee_ID = E_ID;
end //



desc Organization_Head;
select* from Organization_head;
select* from Organization;
desc Organization_Head;
commit;

desc Organization_Head;
insert into Organization_Head(21,2,'Employee-1','1990-9-12',3);
select* from Organization;
-- 1978-8-21
-- ----------------------------------------------------------- 
delimiter //
create trigger Doctor_error
after insert
on Doctor
for each row
begin
    if not exists(select Organization_ID from Organization where Organization_ID=new.Organization_ID) then
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Organization ID does not Exits in organization';

     end if;
 end //
 
 drop trigger Doctor_error;
 
delimiter // 
create trigger organ_error
after insert
on Organ_available
for each row
begin
    if not exists(select Donor_ID from Donor where Donor_ID=new.Donor_ID) then
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Donor_ID ID does not Exits in Donor';

     end if;
 end //
 
drop trigger Organ_error;
 
 
delimiter //
create trigger Donor_error
after insert
on Donor
for each row
begin
    if (not exists(select User_ID from User where User_ID=new.User_ID)) then
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User_ID ID does not Exits in User';
    elseif  (not exists(select organization_ID from Organization where organization_ID=new.organization_ID)) then
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'organization_ID ID does not Exits in organization';
     end if;
end //
drop trigger Donor_error;


delimiter //
create trigger patient_error
after insert
on Patient
for each row
begin
    if (not exists(select User_ID from User where User_ID=new.User_ID) ) then
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Donor_ID ID dose not Exits in Donor';
    elseif (not exists(select Doctor_ID from Doctor where Doctor_ID=new.Doctor_ID)) then
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Doctor_ID ID dose not Exits in Doctor';
     end if;
end //
drop trigger Patient_error;

 
delimiter //
create trigger Organization_head_error
after insert
on Organization
for each row
begin
    if not exists(select organization_ID from Organization where organization_ID=new.organization_ID) then
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'organization_ID ID is not Exits in organization ';

     end if;
 end //
drop trigger Organization_Head_error;
 
delimiter //
create trigger Transaction_erro
after insert
on Transaction
for each row
begin
    if (not exists(select Patient_ID from Patient where Patient_ID=new.Patient_ID)) then
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Patient_ID ID does not Exits in Patient';
    elseif not exists(select Donor_ID from Donor where Donor_ID=new.Donor_ID) then
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Donor_ID ID does Exits in Donor';
     end if;
end; 
//
drop trigger Transaction_erro;
select* from Organization;
 -- ------------------------------------------------

CREATE TABLE Donor(
  Donor_ID int NOT NULL,
  Organ_ID int NOT NULL,
  organ_donated varchar(20) NOT NULL,
  reason_of_donation varchar(20),
  Organization_ID int NOT NULL,
  User_ID int NOT NULL,
  FOREIGN KEY(User_ID) REFERENCES User(User_ID) ON DELETE CASCADE,
  FOREIGN KEY(Organization_ID) REFERENCES Organization(Organization_ID) ON DELETE CASCADE,
  PRIMARY KEY(Donor_ID, organ_donated, Organ_ID)
);
drop table donor;
desc donor;
CREATE TABLE Transaction(
  Patient_ID int NOT NULL,
  Organ_ID int NOT NULL,
  Donor_ID int NOT NULL,
  organ_donated varchar(20) NOT NULL,
  Date_of_transaction date NOT NULL,
  Status int NOT NULL,
  -- FOREIGN KEY(Patient_ID) REFERENCES Patient(Patient_ID) ON DELETE CASCADE,
  -- FOREIGN KEY(Donor_ID, organ_donated, Organ_ID) REFERENCES donor(Donor_ID, organ_donated, Organ_ID)  ON DELETE CASCADE,
  PRIMARY KEY(Patient_ID,Organ_ID)
);
drop table transaction;
desc donor;
CREATE TABLE Organ_available(
  Organ_ID int NOT NULL AUTO_INCREMENT,
  Organ_name varchar(20) NOT NULL,
  Donor_ID int NOT NULL,
  FOREIGN KEY(Donor_ID, organ_Name, Organ_ID) REFERENCES Donor(Donor_ID, organ_donated, Organ_ID) ON DELETE CASCADE,
  PRIMARY KEY(Organ_ID)
);


desc donor;
desc Organ_available;
desc Transaction;




-- Trigger for Organ Available from Donor

DELIMITER \\
create TRIGGER ADD_Organ_avab after insert
on Donor for each row
begin
	insert into Organ_available(Donor_ID, organ_Name, Organ_ID) values(NEW.Donor_ID, NEW.organ_donated, NEW.Organ_ID);
end;
drop trigger ADD_Organ_avab;


DELIMITER $$
create TRIGGER remove_Organ after INSERT
on Transaction for each row
begin
	delete from Organ_available where new.Organ_ID = Organ_ID;
    delete from Donor where new.Donor_ID = Donor_ID;
    delete from patient where new.Patient_ID = Patient_ID;
end;

drop trigger remove_Organ;
Desc Organ_available;
DESC Donor;



-- CREATE TRIGGER trigger_name  trigger_time trigger_event  
-- ON table_name FOR EACH ROW  
-- BEGIN  
--     --variable declarations  
--     --trigger code  
-- END;    



select* from login;
insert into login values('Kathan', '1234');
select* from login where username = 'Kathan';
insert into login values('Dev','123456');

desc User;
insert into User values(1 ,'Name-1','1978-8-21',1,'NIL','Street-1','New Delhi','Delhi');



select* from user;

desc Donor;
desc Organ_available;
desc Organization;
desc Organization_head;
desc Doctor;
desc Transaction;
desc log;
desc User;
select* from User where User_id=1;
desc donor;




select* from User;
delete from User where User_ID!=0;



delete from User where User_id = 99;

desc user;





delete from Donor where Donor_ID!=0;
desc donor;
desc User;
select* from User;
select* from User_phone_no;
select* from Patient;
-- select* from User where Medical_history = 'No-No-NO';
desc User;
select* from User where User_id = 100;

select* from User;
select* from Donor;
select* from Organization;
desc Donor;
-- insert into donor values(16,16,'Lung','Reason-16',50,18);

select* from Donor;
-- delete from donor where Donor_ID = 15;
insert into Donor values (15,15,'Heart','Reason-15',50,53);
rollback;
insert into Donor values (15,15,'Heart','Reason-15',50,53);
select* from donor where Donor_id = 17;



select* from doctor where Doctor_ID = 200;
desc doctor;
select* from organization;
select* from Doctor_phone_no;
select* from Organization where Organization_ID = 100;
desc Organization;

desc Organization_phone_no;
select* from Organization_phone_no;

desc organization_head;
select* from organization_head;

desc Transaction;
select* from Transaction;
select* from Organ_available;



SELECT* FROM PATIENt;
select* from Organ_available;
select* from Donor where donor_ID = 15;
select* from donor where organ_donated = 'Kidney';
desc transaction;
select* from Transaction;
select* from donor where donor_ID = 7;
select* from patient where patient_ID = 4;
select* from User where User_ID = 1;
select* from Doctor;
select* from Organization;
select* from login;
insert into login values('Kishan','1234567');

desc Patient;
select* from Patient where User_ID = 1;
select* from Donor where User_ID = 1;
select* from donor d, patient p where d.User_ID = p.User_ID;
select* from User where User_ID = 3;
select* from User;
select* from Patient;
select* from Donor;
select* from Doctor;
select* from Organization;
select* from Organization_Head;
desc Transaction;

select* from User where User_ID =1;
select* from User_Phone_no where user_Id =1;

commit;

select* from Organization where Organization_ID = 4;
desc Organization;
select* from User;
select* from Donor;
desc Donor;
select* from Patient;
desc Transaction;
select* from Organ_available where Organ_name = 'Pancreas';
select* from Donor where Organ_donated = 'Pancreas';
desc Organ_available;


select* from Patient;
select* from Organ_available;
select* from Donor;
select* from Donor where Donor_ID =2;
select* from Patient where User_ID = 58;
select User_ID,count(Patient_ID) from Patient group by (User_ID);
select* from User where User_ID = 41;
select* from Doctor;
-- -------------------------Functions for Removing Data  -------------------------

select* from Organization_Head;
select* from Patient;

desc User;
desc Patient;
desc donor;






-- -----Function for Updating-------




delimiter//
CREATE FUNCTION Update_user (User_I_D int, Name_In int, Date_of_Birth_In int, M_Ins_IN int, M_His_In varchar(30), stree_IN varchar(30), city_In varchar(30), State_in varchar(30))
RETURNS varchar(1000)
BEGIN
	DECLARE C_D CURSOR FOR SELECT * FROM Donor;
    DECLARE C_P CURSOR FOR SELECT * FROM Patient;
    DECLARE retstr varchar(1000);
	
	SET retstr = concat(User_I_D , Name_In , Date_of_Birth_In , M_Ins_IN , M_His_In , stree_IN,city_In, State_in);
    open C_P;
    get_Patient:loop
	fetch C_P into P_Id,O_req,R_o_Pro,Do_ID,Us_Id;
    select P_Id,O_req,R_o_Pro,Do_ID,Us_Id;
    if User_I_D = Us_Id then
    SET retstr =  concat(retstr,P_Id , O_req, R_o_Pro, Do_ID);
    leave get_Patient;
    end if;
    end loop get_Patient;
    close C_P;
    
    
    open C_D;
	get_Donor:loop
	fetch C_D into D_ID, O_ID, Or_Do,R_O_Don,Or_ID,US_Id;
    select D_ID, O_ID, Or_Do,R_O_Don,Or_ID,US_Id;
    if User_I_D = US_Id then
    SET retstr =  concat(retstr,D_ID, O_ID, Or_Do,R_O_Don,Or_ID);
    leave get_Donor;
    end if;
    end loop get_Donor;
    close C_D;
    Update User set Name = Name_In, Date_of_Birth = Date_of_Birth_In, Medical_Insurance = M_Ins_IN, Medical_history = M_His_IN, Street = stree_IN, City = city_In, State = State_in where User_Id = User_I_D;
    
RETURN retstr;
end//

desc Patient;
desc Donor;
desc User;

show error;





-- --

delimiter//
CREATE FUNCTION Update_user (User_I_D int, Name_In int, Date_of_Birth_In int, M_Ins_IN int, M_His_In varchar(30), stree_IN varchar(30), city_In varchar(30), State_in varchar(30))
RETURNS varchar(100)
BEGIN
	DECLARE C_D CURSOR FOR SELECT * from Patient where User_ID = User_I_D;
    DECLARE C_P CURSOR FOR SELECT * FROM Donor where User_ID = User_I_D;
    DECLARE SAMP varchar(10);
    DECLARE retstr varchar(1000);
    SET SAMP = ' ';
	
    SET retstr = concat(User_I_D , Name_In , Date_of_Birth_In , M_Ins_IN , M_His_In , stree_IN,city_In, State_in,SAMP);
    open C_P;
	fetch C_P into P_Id,O_req,R_o_Pro,Do_ID,Us_Id;
    select P_Id,O_req,R_o_Pro,Do_ID,Us_Id;
    SET retstr =  concat(retstr,P_Id , O_req, R_o_Pro, Do_ID,SAMP);
    close C_P;
    
    open C_D;
	fetch C_D into D_ID, O_ID, Or_Do,R_O_Don,Or_ID,US_Id;
    select D_ID, O_ID, Or_Do,R_O_Don,Or_ID,US_Id;
    SET retstr =  concat(retstr,D_ID, O_ID, Or_Do,R_O_Don,Or_ID);
    close C_D;
    Update User set Name = Name_In, Date_of_Birth = Date_of_Birth_In, Medical_Insurance = M_Ins_IN, Medical_history = M_His_IN, Street = stree_IN, City = city_In, State = State_in where User_Id = User_I_D;
RETURN retstr;
end//




desc Patient;