SHOW VARIABLES LIKE 'event_scheduler';
DROP EVENT IF EXISTS updateOverTimeAct;
CREATE EVENT updateOverTimeAct
	ON SCHEDULE EVERY 1 minute STARTS CURRENT_TIMESTAMP
	DO 
		update Activity set act_Status = False WHERE Id IN (
			SELECT temp.Id FROM (
				select Id from Activity where endTime < sysdate() and act_Status = true
			) AS temp
		);
       update FiestaGroup set timeStatus = False WHERE Id IN (
			SELECT temp.Id FROM (
				select Id from FiestaGroup where deadLine < sysdate() and timeStatus = true
			) AS temp
		);
