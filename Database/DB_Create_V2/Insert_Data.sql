/* ============================================
   INSERT CAMPAIGN CATEGORIES
============================================ */
INSERT INTO Campaign_Category (Campaign_CategoryName) VALUES
('Brand Awareness'),
('Sales Promotion'),
('Social Movement'),
('Super Bowl'),
('User-Generated'),
('Product Advertising'),
('Event Marketing');

/* ============================================
   INSERT COMPANIES
============================================ */
INSERT INTO Company (CompanyName) VALUES
('Lamborghini'),
('Nike'),
('Amazon'),
('Coca-Cola'),
('Coinbase'),
('Red Bull'),
('ALS Association'),
('Spotify'),
('California Milk Processor Board'),
('Dos Equis'),
('Apple'),
('Doritos'),
('Old Spice');

/* ============================================
   INSERT CHANNEL CATEGORIES
============================================ */
INSERT INTO Channel_Category (Channel_CategoryName) VALUES
('Digital'),
('Social Media'),
('Television'),
('Print'),
('Outdoor'),
('Event'),
('User-Generated'),
('Word of Mouth');

/* ============================================
   INSERT CHANNELS
============================================ */
INSERT INTO Channel (ChannelName, idChannel_Category) VALUES
('Website Ads', 1),
('Online Video', 1),
('Email Marketing', 1),

('Instagram', 2),
('TikTok', 2),
('Facebook', 2),
('Twitter', 2),

('National TV', 3),
('Olympic TV', 3),
('Super Bowl Broadcast', 3),

('Magazines', 4),

('Billboards', 5),

('Super Bowl', 6),
('Olympics', 6),
('Prime Day Event', 6),

('User Submission', 7),
('Influencer Content', 7),

('Word of Mouth', 8);

/* ============================================
   INSERT ALL 13 CAMPAIGNS
============================================ */

INSERT INTO Campaign
(Campaign_Name, StartDate, EndDate, idCompany, idCampaign_Category, Budget, Revenue)
VALUES
-- 1 Lamborghini (no ads)
('No Advertising Philosophy', NULL, NULL, 1, 1, 0.00, 0.00),

-- 2 Nike Find Your Greatness (2012 Olympics)
('Find Your Greatness', '2012-07-27', '2012-08-13', 2, 1, 100000000.00, 501000000.00),

-- 3 Amazon Prime Day
('Prime Day', '2015-07-15', NULL, 3, 2, 40300000000.00, 87880000000.00),

-- 4 Coca-Cola Share a Coke
('Share a Coke', '2014-01-01', '2014-12-31', 4, 1, 15000000.00, 1320000000.00),

-- 5 Coinbase QR Super Bowl Ad
('Coinbase QR Super Bowl', '2022-02-13', '2022-02-13', 5, 4, 13000000.00, 400000000.00),

-- 6 Red Bull Racing F1
('Red Bull Racing F1', '2022-01-01', '2024-12-31', 6, 1, 54000000.00, 6520000.00),

-- 7 ALS Ice Bucket Challenge
('ALS Ice Bucket Challenge', '2014-07-01', '2014-09-01', 7, 3, 500000.00, 115000000.00),

-- 8 Spotify Wrapped
('Spotify Wrapped', '2016-12-01', NULL, 8, 1, 40000000.00, 1140000000.00),

-- 9 Got Milk
('Got Milk', '1993-01-01', '2014-12-31', 9, 1, 775000000.00, 23500000000.00),

-- 10 Dos Equis Most Interesting Man
('Most Interesting Man', '2006-01-01', '2016-01-01', 10, 1, 180000000.00, 8000000000.00),

-- 11 Apple Shot on iPhone
('Shot on iPhone', '2015-01-01', NULL, 11, 5, 435000000.00, 85000000000.00),

-- 12 Doritos Crash the Super Bowl
('Crash the Super Bowl', '2006-01-01', '2016-01-01', 12, 4, 65000000.00, 19690000000.00),

-- 13 Old Spice "The Man You Could Smell Like"
('The Man You Could Smell Like', '2010-02-04', '2010-07-31', 13, 1, 28000000.00, 125000000.00);

/* ============================================
   INSERT CAMPAIGN–CHANNEL RELATIONSHIPS
============================================ */

INSERT INTO Campaign_channel_xref (idChannel, idCampaign) VALUES
-- 1 Lamborghini
(18,1),

-- 2 Nike Find Your Greatness
(9,2), (2,2), (4,2),

-- 3 Amazon Prime Day
(1,3), (3,3), (4,3), (15,3),

-- 4 Share a Coke
(11,4), (4,4), (6,4),

-- 5 Coinbase QR
(10,5), (13,5),

-- 6 Red Bull Racing F1
(2,6), (4,6), (15,6),

-- 7 ALS Ice Bucket
(16,7), (4,7), (5,7),

-- 8 Spotify Wrapped
(1,8), (4,8), (5,8), (7,8),

-- 9 Got Milk
(8,9), (11,9), (12,9),

-- 10 Dos Equis
(8,10), (11,10), (4,10),

-- 11 Shot on iPhone
(11,11), (4,11), (16,11),

-- 12 Crash the Super Bowl
(13,12), (10,12), (16,12),

-- 13 Old Spice
(8,13), (2,13), (4,13);

