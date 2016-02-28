CREATE TABLE `pages` (
  `page_id` int(11) NOT NULL AUTO_INCREMENT,
  `page_url` varchar(45) NOT NULL,
  `status` enum('processed','unprocessed','in_processing','page_not_found','bad_internet_connection') NOT NULL DEFAULT 'unprocessed',
  PRIMARY KEY (`page_id`),
  UNIQUE KEY `page_url_UNIQUE` (`page_url`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;



CREATE TABLE `references`
(
    root INT(11) NOT NULL,
    child INT(11) NOT NULL
);
CREATE INDEX root_index ON `references` (root);
