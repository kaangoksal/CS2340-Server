# MySQL COnfiguration Instructions  


First we need to create a database  
`create DATABASE waterapp
`

Then we will create the neccessary tables  



**Water Report Table**

CREATE TABLE `reports` (  
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,  
  `report_number` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,  
  `reporter` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,  
  `location` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,  
  `data` text COLLATE utf8mb4_unicode_ci NOT NULL,  
  PRIMARY KEY (`report_number`)  
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci; 

**Users Table**  

CREATE TABLE `users` (  
  `username` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,  
  `password` text COLLATE utf8mb4_unicode_ci NOT NULL,  
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,  
  `email` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,  
  `account_type` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT 'user',  
  `token` varchar(4096) COLLATE utf8mb4_unicode_ci DEFAULT '',  
  `device_type` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT '',  
  `number` varchar(25) COLLATE utf8mb4_unicode_ci DEFAULT NULL,  
  PRIMARY KEY (`username`),  
  UNIQUE KEY `i_users_email` (`email`)  
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;  


After that we will create a user account to access the MySQL server.  
`CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';`


The default user has no permissions, so it cant do anything on the server without us giving permissions
`GRANT [type of permission] ON [database name].[table name] TO ‘[username]’@'localhost’;`


**Type of Permissions**  

ALL PRIVILEGES- as we saw previously, this would allow a MySQL user all access to a designated database (or if no database is selected, across the system)  
CREATE- allows them to create new tables or databases  
DROP- allows them to them to delete tables or databases  
DELETE- allows them to delete rows from tables  
INSERT- allows them to insert rows into tables  
SELECT- allows them to use the Select command to read through databases  
UPDATE- allow them to update table rows  
GRANT OPTION- allows them to grant or remove other users' privileges  


**We are going to grant the following**

grant select on waterapp.users to 'username'@'localhost';  
grant insert on waterapp.users to 'username'@'localhost';  
grant delete on waterapp.users to 'username'@'localhost';  
grant update on waterapp.users to 'username'@'localhost';  

grant select on waterapp.reports to 'python_backend'@'localhost';  
grant insert on waterapp.reports to 'python_backend'@'localhost';  
grant delete on waterapp.reports to 'python_backend'@'localhost';  
grant update on waterapp.reports to 'python_backend'@'localhost';  

