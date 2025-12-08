/* ******************************************
  Drop and create the campaign_channel User
********************************************/

-- Drop user if exists
DROP USER IF EXISTS 'campaign_channel_user'@'%';

-- Create user if not exists
CREATE USER IF NOT EXISTS 'campaign_channel_user'@'%';
GRANT ALL PRIVILEGES ON *.* TO 'campaign_channel_user'@'%'; 
ALTER USER 'campaign_channel_user'@'%' 
	REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 0 
	MAX_CONNECTIONS_PER_HOUR 0 
	MAX_UPDATES_PER_HOUR 0 
	MAX_USER_CONNECTIONS 0;
GRANT ALL PRIVILEGES ON `Campaign\_Channel\_user\_%`.* 
	TO 'campaign_channel_user'@'%';
GRANT ALL PRIVILEGES ON `Campaign\_Channel`.* 
	TO 'campaign_channel_user'@'%' WITH GRANT OPTION;

COMMIT;