use Fiesta;
DROP TRIGGER IF EXISTS deleteAct;
DROP TRIGGER IF EXISTS insertTicketAct;
DROP TRIGGER IF EXISTS insertAccount;
DROP TRIGGER IF EXISTS insertReviewStatus;

delimiter #
create trigger deleteAct after update on Activity for each row
begin
	if (New.act_Status = False) then
		update unexpiredActivity set Useable = False where unexpiredActivity.act_Id = New.Id;
		update ActivityJoinedList set Useable = False,Expired = true where ActivityJoinedList.act_Id = New.Id;
		update act_touchPeople set Useable = False where act_touchPeople.act_Id = New.Id;
	end if;
end
#
delimiter ;

delimiter #
create trigger insertTicketAct after insert on ActivityJoinedList for each row
begin
	update Ticket set Ticket.Remainder = Ticket.Remainder - 1 where Ticket.act_Id = NEW.act_Id and Ticket.ticketKinds = NEW.ticketkinds;
	insert into unexpiredActivity(act_Id,accountId,ticketKinds,ticketStatus,Useable) values(NEW.act_Id,NEW.accountId,NEW.ticketkinds,false,true);
	insert into act_touchPeople(act_Id,accountId,Useable) values(NEW.act_Id,NEW.accountId,true);	
end
#
delimiter ;

delimiter #
create trigger insertAccount after insert on FiestaAccount for each row
begin
declare reviewStatus int;
set reviewStatus = (select ifnull((select Id from ReviewStatus where accountId = NEW.Id limit 1),0));
if (reviewStatus = 0) then
	insert into ReviewStatus(accountId,Mail,reviewStatus,Useable) values(NEW.Id,New.Mail_1,false,true);
end if;
end
#
delimiter ;
