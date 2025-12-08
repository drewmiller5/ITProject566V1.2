/* ******************************************
  Drop and create the Campaign_Channel User
********************************************/

-- Drop user if exists
DROP USER IF EXISTS 'Campaign_Channel_user'@'%';

-- Create user if not exists
CREATE USER IF NOT EXISTS 'Campaign_Channel_user'@'%';
GRANT ALL PRIVILEGES ON *.* TO 'Campaign_Channel_user'@'%'; 
ALTER USER 'Campaign_Channel_user'@'%' 
	REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 0 
	MAX_CONNECTIONS_PER_HOUR 0 
	MAX_UPDATES_PER_HOUR 0 
	MAX_USER_CONNECTIONS 0;
GRANT ALL PRIVILEGES ON `Campaign\_Channel\_user\_%`.* 
	TO 'Campaign_Channel_user'@'%';
GRANT ALL PRIVILEGES ON `Campaign\_Channel`.* 
	TO 'Campaign_Channel_user'@'%' WITH GRANT OPTION;

COMMIT;