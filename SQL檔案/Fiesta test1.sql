create database if not exists Fiesta;
use Fiesta;
create table if not exists FiestaAccount(
	Id int not null auto_increment,
    userName varchar(41) not null,
    nickName varchar(41) ,
    userId varchar(41) not null,
    userPassword char(41) not null,
    Tag varchar(200),
    avgCost int,
    Mail_1 varchar(41) not null,
    Mail_2 varchar(41),
    Birthday date,
    Address varchar(100),
    Phone varchar(20),
    ID_CARD varchar(20),
    Sex char(1),
    Photo varchar(100),
    School varchar(20),
    Latitude float,
    Longitude float,
    Distance int ,
    deviceToken text,
    Useable boolean not null,
    primary key (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1;
create table if not exists GroupMember(
	Id int not null auto_increment,
    groupId int,
    accountId int,
    Authority int,
    Useable boolean not null,
    primary key (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;
create table if not exists FiestaGroup(
	Id int not null auto_increment,
    groupName text not null,
    Tag varchar(200),
    Mail text,
    Phone text,
    Address text,
    timeStatus boolean,
    viewStatus boolean,
    deadLine datetime,
    Photo text,
    Useable boolean not null,
    primary key (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;
create table if not exists Activity(
	Id int not null auto_increment,
    act_Name varchar(100) not null,
    groupId int not null,
    Tag varchar(200),
    peopleMaxium int,
    Location varchar(100),
    Latitude float,
    Longitude float,
    startTime datetime,
    endTime datetime,
    Price int,
    act_Description text,
    joinedCount int,
    act_Status boolean not null,
    viewStatus boolean,
    Models text,
    Photo text,
    Useable boolean not null,
    primary key (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;
create table if not exists act_touchPeople(
	Id int not null auto_increment,
    act_Id int,
    accountId int,
    Useable boolean not null,
    primary key (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;
create table if not exists ActivityJoinedList(
	Id int not null auto_increment,
    act_Id int,
    accountId int,
    ticketKinds varchar(20),
    ticketStatus boolean,
    Expired boolean,
    Useable boolean not null,
    primary key (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;
create table if not exists unexpiredActivity(
	Id int not null auto_increment,
    act_Id int,
    accountId int,
    ticketKinds varchar(30),
    ticketStatus boolean,
    Useable boolean not null,
    primary key (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;
create table if not exists Ticket(
	Id int not null auto_increment,
    act_Id int not null,
    ticketKinds varchar(30) not null,
    Mounts int,
    Remainder int,
    Price int,
    Useable boolean not null,
    primary key (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;
create table if not exists showList(
	Id int not null auto_increment,
    act_Id int,
    showName varchar(50) not null,
    Detail text,
    showTime datetime,
    showStatus boolean,
    Useable boolean not null,
    primary key (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;
create table if not exists lotteList(
	Id int not null auto_increment,
    act_Id int,
    accountId int,
    Prize text,
    lotteTime time,
    Useable boolean not null,
    primary key (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;
create table if not exists ReviewStatus(
	Id int not null auto_increment,
    accountId int not null,
    Mail text,
    reviewStatus boolean, 
    Useable boolean not null,
    primary key (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;
create table if not exists ActivityHistory(
	Id int not null auto_increment,
    act_Id int,
    groupId int,
    accountId int,
    act_Date date,
    Price int,
    accountStatus boolean,
    Useable boolean not null,
    primary key (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;
create table if not exists ActivityScore(
	Id int not null auto_increment,
    act_Id int,
    accountId int,
    score_Date date,
    Detail text,
    Stars int,
    Price int,
    Music int,
    Flow int,
    Vibe int,
    Light int,
    Moveline int,
    Site int,
    Staff int,
    Useable boolean not null,
    primary key (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;
create table if not exists showScore(
	Id int not null auto_increment,
    showId int,
    accountId int,
    Detail text,
    score_Date date,
    Useable boolean not null,
    primary key (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;
create table if not exists act_UserFeedBack(
	Id int not null auto_increment,
    act_Id int,
    act_scoreId int,
    Useable boolean not null,
    primary key (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;
create table if not exists show_UserFeedBack(
	Id int not null auto_increment,
    act_Id int,
    show_scoreId int,
    Useable boolean not null,
    primary key (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;
create table if not exists TagList(
	Id int not null auto_increment ,
    TagName text,
    TagScore int,
    Photo text,
    Useable boolean not null,
    primary key (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;
ALTER TABLE GroupMember ADD CONSTRAINT GroupMember_Fk1 FOREIGN KEY (accountId) REFERENCES FiestaAccount(Id);
ALTER TABLE GroupMember ADD CONSTRAINT GroupMember_Fk2 FOREIGN KEY (groupId) REFERENCES FiestaGroup(Id);
ALTER TABLE Activity ADD CONSTRAINT Activity_Fk FOREIGN KEY (groupId) REFERENCES FiestaGroup(Id);
ALTER TABLE act_touchPeople ADD CONSTRAINT act_touchPeople_Fk1 FOREIGN KEY (act_Id) REFERENCES Activity(Id);
ALTER TABLE act_touchPeople ADD CONSTRAINT act_touchPeople_Fk2 FOREIGN KEY (accountId) REFERENCES FiestaAccount(Id);
ALTER TABLE ActivityJoinedList ADD CONSTRAINT ActivityJoinedList_Fk1 FOREIGN KEY (act_Id) REFERENCES Activity(Id);
ALTER TABLE ActivityJoinedList ADD CONSTRAINT ActivityJoinedList_Fk2 FOREIGN KEY (accountId) REFERENCES FiestaAccount(Id);
ALTER TABLE unexpiredActivity ADD CONSTRAINT unexpiredActivity_Fk1 FOREIGN KEY (act_Id) REFERENCES Activity(Id);
ALTER TABLE unexpiredActivity ADD CONSTRAINT unexpiredActivity_Fk2 FOREIGN KEY (accountId) REFERENCES FiestaAccount(Id);
ALTER TABLE showList ADD CONSTRAINT showList_Fk1 FOREIGN KEY (act_Id) REFERENCES Activity(Id);
ALTER TABLE lotteList ADD CONSTRAINT lotteList_Fk1 FOREIGN KEY (act_Id) REFERENCES Activity(Id);
ALTER TABLE lotteList ADD CONSTRAINT lotteList_Fk2 FOREIGN KEY (accountId) REFERENCES FiestaAccount(Id);
ALTER TABLE ActivityHistory ADD CONSTRAINT ActivityHistory_Fk1 FOREIGN KEY (act_Id) REFERENCES Activity(Id);
ALTER TABLE ActivityHistory ADD CONSTRAINT ActivityHistory_Fk2 FOREIGN KEY (groupId) REFERENCES FiestaGroup(Id);
ALTER TABLE ActivityHistory ADD CONSTRAINT ActivityHistory_Fk3 FOREIGN KEY (accountId) REFERENCES FiestaAccount(Id);
ALTER TABLE ActivityScore ADD CONSTRAINT ActivityScore_Fk1 FOREIGN KEY (act_Id) REFERENCES Activity(Id);
ALTER TABLE ActivityScore ADD CONSTRAINT ActivityScore_Fk2 FOREIGN KEY (accountId) REFERENCES FiestaAccount(Id);
ALTER TABLE showScore ADD CONSTRAINT showScore_Fk1 FOREIGN KEY (showId) REFERENCES showList(Id);
ALTER TABLE showScore ADD CONSTRAINT showScore_Fk2 FOREIGN KEY (accountId) REFERENCES FiestaAccount(Id);
ALTER TABLE act_UserFeedBack ADD CONSTRAINT act_UserFeedBack_Fk1 FOREIGN KEY (act_Id) REFERENCES Activity(Id);
ALTER TABLE act_UserFeedBack ADD CONSTRAINT act_UserFeedBack_Fk2 FOREIGN KEY (act_scoreId) REFERENCES ActivityScore(Id);
ALTER TABLE show_UserFeedBack ADD CONSTRAINT show_UserFeedBack_Fk1 FOREIGN KEY (act_Id) REFERENCES Activity(Id);
ALTER TABLE show_UserFeedBack ADD CONSTRAINT show_UserFeedBack_Fk2 FOREIGN KEY (show_scoreId) REFERENCES showScore(Id);
