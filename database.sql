/*
SQLyog Community v13.1.6 (64 bit)
MySQL - 5.7.9 : Database - art
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`art` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE`art`;

/*Table structure for table `tbl_card` */

DROP TABLE IF EXISTS `tbl_card`;

CREATE TABLE `tbl_card` (
  `card_id` int(5) NOT NULL AUTO_INCREMENT,
  `uid` int(5) NOT NULL,
  `card_num` decimal(25,0) NOT NULL,
  `card_own` varchar(20) NOT NULL,
  `card_exp` date NOT NULL,
  `card_status` tinyint(1) NOT NULL,
  PRIMARY KEY (`card_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `tbl_card` */

insert  into `tbl_card`(`card_id`,`uid`,`card_num`,`card_own`,`card_exp`,`card_status`) values 
(1,4,1111333344445555,'Mary Jane','2026-05-15',1),
(2,4,2222333355556666,'Mary Jane','2027-06-15',1),
(3,3,1111222255559999,'Devika','2026-10-22',1),
(4,2,1234567812345678,'Merin','2024-06-28',1);

/*Table structure for table `tbl_cart_child` */

DROP TABLE IF EXISTS `tbl_cart_child`;

CREATE TABLE `tbl_cart_child` (
  `cc_id` int(5) NOT NULL AUTO_INCREMENT,
  `cm_id` int(5) NOT NULL,
  `item_id` int(5) NOT NULL,
  PRIMARY KEY (`cc_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `tbl_cart_child` */

insert  into `tbl_cart_child`(`cc_id`,`cm_id`,`item_id`) values 
(1,1,7),
(2,2,3),
(3,3,2);

/*Table structure for table `tbl_cart_master` */

DROP TABLE IF EXISTS `tbl_cart_master`;

CREATE TABLE `tbl_cart_master` (
  `cm_id` int(5) NOT NULL AUTO_INCREMENT,
  `uid` int(5) NOT NULL,
  `cart_status` varchar(10) NOT NULL,
  `c_tot_amount` decimal(6,0) NOT NULL,
  `order_date` date NOT NULL,
  PRIMARY KEY (`cm_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `tbl_cart_master` */

insert  into `tbl_cart_master`(`cm_id`,`uid`,`cart_status`,`c_tot_amount`,`order_date`) values 
(1,3,'paid',10800,'2023-03-03'),
(2,3,'paid',84000,'2023-03-03'),
(3,3,'paid',36000,'2023-03-03');

/*Table structure for table `tbl_category` */

DROP TABLE IF EXISTS `tbl_category`;

CREATE TABLE `tbl_category` (
  `cat_id` int(5) NOT NULL AUTO_INCREMENT,
  `cat_name` varchar(100) NOT NULL,
  `cat_status` tinyint(1) NOT NULL,
  PRIMARY KEY (`cat_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `tbl_category` */

insert  into `tbl_category`(`cat_id`,`cat_name`,`cat_status`) values 
(1,'Realism',1),
(2,'History',1),
(3,'Portrait',1),
(4,'Expressionism',1),
(5,' Realism ',1);

/*Table structure for table `tbl_courier` */

DROP TABLE IF EXISTS `tbl_courier`;

CREATE TABLE `tbl_courier` (
  `cou_id` int(5) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `cou_name` varchar(10) NOT NULL,
  `cou_phone` decimal(10,0) NOT NULL,
  `cou_place` varchar(20) NOT NULL,
  `cou_status` tinyint(1) NOT NULL,
  PRIMARY KEY (`cou_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `tbl_courier` */

insert  into `tbl_courier`(`cou_id`,`username`,`cou_name`,`cou_phone`,`cou_place`,`cou_status`) values 
(1,'dane@gmail.com','Danny',9988776655,'Idukki',1),
(2,'jommy@gmail.com','Jose',9988776633,'Kottayam',1),
(3,'dhl@gmail.com','DHL',1234567890,'Idukki',1);

/*Table structure for table `tbl_delivery` */

DROP TABLE IF EXISTS `tbl_delivery`;

CREATE TABLE `tbl_delivery` (
  `del_id` int(5) NOT NULL AUTO_INCREMENT,
  `cou_id` int(5) NOT NULL,
  `cm_id` int(5) NOT NULL,
  `d_date` date NOT NULL,
  `d_time` timestamp NOT NULL,
  PRIMARY KEY (`del_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `tbl_delivery` */

/*Table structure for table `tbl_exhibition` */

DROP TABLE IF EXISTS `tbl_exhibition`;

CREATE TABLE `tbl_exhibition` (
  `ex_id` int(5) NOT NULL AUTO_INCREMENT,
  `ex_date` date NOT NULL,
  `ex_venu` varchar(20) NOT NULL,
  `ticket` decimal(4,0) NOT NULL,
  `ex_name` varchar(30) NOT NULL,
  PRIMARY KEY (`ex_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `tbl_exhibition` */

insert  into `tbl_exhibition`(`ex_id`,`ex_date`,`ex_venu`,`ticket`,`ex_name`) values 
(1,'2023-03-23','Hdsss',900,'Dane');

/*Table structure for table `tbl_item` */

DROP TABLE IF EXISTS `tbl_item`;

CREATE TABLE `tbl_item` (
  `item_id` int(11) NOT NULL AUTO_INCREMENT,
  `sub_id` int(11) DEFAULT NULL,
  `uid` int(5) NOT NULL,
  `item_name` varchar(100) DEFAULT NULL,
  `item_des` varchar(100) DEFAULT NULL,
  `item_price` varchar(100) DEFAULT NULL,
  `item_image` varchar(500) DEFAULT NULL,
  `item_approval` varchar(100) DEFAULT NULL,
  `finalcost` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`item_id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

/*Data for the table `tbl_item` */

insert  into `tbl_item`(`item_id`,`sub_id`,`uid`,`item_name`,`item_des`,`item_price`,`item_image`,`item_approval`,`finalcost`) values 
(1,2,2,'Lifeness','A life','50000','static/image/3a1ee49c-08f7-4805-9b16-89499b898e7bpreal.jpg','approved','60000'),
(2,2,2,'Woman','A woman','30000','static/image/131a66fa-1581-4514-921b-e235f4cd1d40tornie.jpg','paid','36000'),
(3,2,2,'Girl','A girl','70000','static/image/abcb9a9f-622b-46c1-b2c7-baa0bea4b4a2img1.jpg','paid','84000'),
(9,1,2,'Artt','ddfg','4000','static/image/c85971c4-bd33-4c56-93e3-91ed3ec57792sur.jpg','approved','4800'),
(4,3,2,'Time','A time','10000','static/image/1b0a06f3-b0f1-4b67-9308-430d88f47290clock.jpg','approved','12000'),
(8,3,4,'New','ddffgh','1400','static/image/7efedee3-bff4-439f-8bb0-228aac5bd985gestural abstraction.jfif','approved','1680'),
(7,2,6,'Old age','Shows old age','9000','static/image/83f3c19d-e709-4649-8ea7-7ca99f3355e4download.jfif','paid','10800');

/*Table structure for table `tbl_item_ex` */

DROP TABLE IF EXISTS `tbl_item_ex`;

CREATE TABLE `tbl_item_ex` (
  `iex_id` int(5) NOT NULL AUTO_INCREMENT,
  `item_id` int(5) NOT NULL,
  `ex_id` int(5) NOT NULL,
  PRIMARY KEY (`iex_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `tbl_item_ex` */

insert  into `tbl_item_ex`(`iex_id`,`item_id`,`ex_id`) values 
(1,9,1);

/*Table structure for table `tbl_login` */

DROP TABLE IF EXISTS `tbl_login`;

CREATE TABLE `tbl_login` (
  `username` varchar(30) NOT NULL,
  `password` varchar(10) NOT NULL,
  `type` varchar(20) NOT NULL,
  `login_status` tinyint(1) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `tbl_login` */

insert  into `tbl_login`(`username`,`password`,`type`,`login_status`) values 
('admin@gmail.com','admin','admin',1),
('merin@gmail.com','merin','user',1),
('devika@gmail.com','devika','staff',1),
('dane@gmail.com','dane','courier',1),
('jommy@gmail.com','jommy','courier',1),
('mary@gmail.com','mary','user',1),
('zeba@gmail.com','zeba','staff',1),
('rose@gmail.com','rose','user',1),
('nayana@gmail.com','nayana','user',1),
('divineflu@gmail.com','divine','user',1),
('dhl@gmail.com','dhl','courier',1);

/*Table structure for table `tbl_payment` */

DROP TABLE IF EXISTS `tbl_payment`;

CREATE TABLE `tbl_payment` (
  `pay_id` int(5) NOT NULL AUTO_INCREMENT,
  `card_id` int(5) NOT NULL,
  `pay_date` date NOT NULL,
  `pay_status` varchar(10) NOT NULL,
  PRIMARY KEY (`pay_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `tbl_payment` */

insert  into `tbl_payment`(`pay_id`,`card_id`,`pay_date`,`pay_status`) values 
(1,3,'2023-03-03','paid'),
(2,3,'2023-03-03','paid'),
(3,3,'2023-03-03','paid');

/*Table structure for table `tbl_personnel` */

DROP TABLE IF EXISTS `tbl_personnel`;

CREATE TABLE `tbl_personnel` (
  `p_id` int(5) NOT NULL,
  `username` varchar(30) NOT NULL,
  `p_fname` varchar(10) NOT NULL,
  `p_lname` varchar(10) NOT NULL,
  `p_dob` date NOT NULL,
  `p_gender` varchar(6) NOT NULL,
  `p_phone` decimal(10,0) NOT NULL,
  `p_hno` decimal(5,0) NOT NULL,
  `p_street` varchar(15) NOT NULL,
  `p_district` varchar(20) NOT NULL,
  `p_pin` decimal(6,0) NOT NULL,
  `p_status` tinyint(1) NOT NULL,
  `p_approval` tinyint(1) NOT NULL,
  PRIMARY KEY (`p_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `tbl_personnel` */

/*Table structure for table `tbl_subcategory` */

DROP TABLE IF EXISTS `tbl_subcategory`;

CREATE TABLE `tbl_subcategory` (
  `sub_id` int(5) NOT NULL AUTO_INCREMENT,
  `cat_id` int(5) NOT NULL,
  `sub_name` varchar(30) NOT NULL,
  `sub_status` tinyint(1) NOT NULL,
  PRIMARY KEY (`sub_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `tbl_subcategory` */

insert  into `tbl_subcategory`(`sub_id`,`cat_id`,`sub_name`,`sub_status`) values 
(1,1,'Photorealism',1),
(2,3,'Tornie',1),
(3,4,'Surrealism',1);

/*Table structure for table `tbl_user` */

DROP TABLE IF EXISTS `tbl_user`;

CREATE TABLE `tbl_user` (
  `uid` int(5) NOT NULL AUTO_INCREMENT,
  `u_fname` varchar(10) NOT NULL,
  `u_lname` varchar(10) NOT NULL,
  `u_gender` varchar(6) NOT NULL,
  `u_dob` date NOT NULL,
  `u_phone` decimal(10,0) NOT NULL,
  `u_hname` varchar(30) NOT NULL,
  `u_street` varchar(30) NOT NULL,
  `u_district` varchar(30) NOT NULL,
  `u_pin` decimal(6,0) NOT NULL,
  `username` varchar(30) NOT NULL,
  `u_status` tinyint(1) NOT NULL,
  `u_type` varchar(10) NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `tbl_user` */

insert  into `tbl_user`(`uid`,`u_fname`,`u_lname`,`u_gender`,`u_dob`,`u_phone`,`u_hname`,`u_street`,`u_district`,`u_pin`,`username`,`u_status`,`u_type`) values 
(1,'Alan','Ann','male','2002-01-11',9988776655,'Alan House','Alan Street','Ernakulam',111111,'alan@gmail.com',1,'user'),
(2,'Merin','Mathew','female','2010-05-14',9988776655,'Merrin House','Merin street','Thrissur',666666,'merin@gmail.com',1,'user'),
(3,'Devika','S','female','2023-01-14',9988774433,'SSSSS','Devika street','Idukki',333333,'devika@gmail.com',1,'staff'),
(4,'Mary','Mon','female','2002-01-18',9988776655,'Mary House','Mary Street','Ernakulam',112233,'mary@gmail.com',1,'user'),
(5,'Zeba','Manu','female','1996-01-02',9876655443,'Zeba House','Zeba street','Alappuzha',334455,'zeba@gmail.com',1,'staff'),
(6,'Rose','Amy','female','2008-02-22',9988776633,'Rose House','Rose Street','Ernakulam',111199,'rose@gmail.com',1,'user'),
(7,'Nayana','Smitha','female','2000-12-04',6238673277,'Nayana House','Nayana Street','Ernakulam',337799,'nayana@gmail.com',1,'user'),
(8,'Divine','Paul','male','2000-12-31',9223328322,'divine house','divine street','Kasargod',691560,'divineflu@gmail.com',1,'user');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
