/*
SQLyog Community Edition- MySQL GUI v8.03 
MySQL - 5.5.20-log : Database - database
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`database` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `database`;

/*Table structure for table `block` */

DROP TABLE IF EXISTS `block`;

CREATE TABLE `block` (
  `block_id` int(11) NOT NULL AUTO_INCREMENT,
  `hash` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`block_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;

/*Data for the table `block` */

insert  into `block`(`block_id`,`hash`) values (1,'72f10db1c0bfadeceb2b04f0d8472a3b48cbfa1d0d4b80463edcffd581156c3c'),(2,'c5006e119bdb053676e0df64783decab5a1ab30404cdc390d96d981f707eefda'),(3,'9fe21870df2f20babbc4dfab279d3682cd83747109ea8c75cc4954df47c04020'),(4,'6c67dd965b5a7cc7ea743932775b1f6739e05a53b603c26159a2109300b85a3e'),(5,'bf054304b6206cd949ae49f2ecec47d8db4cc1606be707d46a79c63d34f61f85'),(6,'88c4c8789398e5ec0dbbf3cbf8a1d25048903edc033249389704b3dbaa8c3afa'),(7,'aa9b42cdff54e7a9942867db888c07c3064ed8f219cb212a32098ffde0bf8e37'),(8,'d8f0ec9097fd0c624d1f575b8ca98c3f623fdc20fd7c62dd2c3bcb56be28adcf'),(9,'5390baeff8da6d94685fb67bef5c56807809eb9fa45e75562b681a73c839ae98'),(10,'2cd89779ae061c9b2310a2def02933f0793937b401d1ce61bbd76865e8afd02e'),(11,'e9d1409a2010e05eac89a76091ca1063602f28ae3a25bf35ef20d4a043e346fb'),(12,'4a0c58258197085cc1faa20d639cfdf3f9050c32447df6e13ad97706dec66376'),(13,'5caa6e9beac34e3ac327b70a5a53f343c6b13d286a716a768bc1c9f04eacf2c5'),(14,'4f6ea15553f87c554cd189282b8c741db829dcb5e83b26eb3d37b913258361d4'),(15,'64d9037d0465a801adc321d4ffa0c49ad2f64e19397b8c7f28a9b99f8216e806'),(16,'7d85b27db0af371c939e3f757552307456d38640a097b079097aa5090f86bedb');

/*Table structure for table `fileupload` */

DROP TABLE IF EXISTS `fileupload`;

CREATE TABLE `fileupload` (
  `file_id` int(10) NOT NULL AUTO_INCREMENT,
  `file` varchar(200) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`file_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `fileupload` */

insert  into `fileupload`(`file_id`,`file`,`date`) values (1,'20200229-161757fileblok.txt','2020-02-29'),(2,'20200229-161838fileblok.txt','2020-02-29');

/*Table structure for table `indexes` */

DROP TABLE IF EXISTS `indexes`;

CREATE TABLE `indexes` (
  `index_id` int(11) NOT NULL AUTO_INCREMENT,
  `block_id` int(11) DEFAULT NULL,
  `file_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`index_id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=latin1;

/*Data for the table `indexes` */

insert  into `indexes`(`index_id`,`block_id`,`file_id`) values (1,1,1),(2,2,1),(3,3,1),(4,4,1),(5,5,1),(6,6,1),(7,7,1),(8,8,1),(9,9,1),(10,10,1),(11,11,1),(12,12,1),(13,13,1),(14,14,1),(15,15,1),(16,16,1),(17,1,2),(18,2,2),(19,3,2),(20,4,2),(21,5,2),(22,6,2),(23,7,2),(24,8,2),(25,9,2),(26,10,2),(27,11,2),(28,12,2),(29,13,2),(30,14,2),(31,15,2),(32,16,2);

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) DEFAULT NULL,
  `password` varchar(10) DEFAULT NULL,
  `user_type` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`user_type`) values (1,'admin','admin','admin'),(3,'zx@gmail.com','345','user'),(4,'ab@gmail.com','ab','user'),(5,'rizvana@gmail.com','111','user');

/*Table structure for table `signup` */

DROP TABLE IF EXISTS `signup`;

CREATE TABLE `signup` (
  `sign_id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(20) DEFAULT NULL,
  `Dob` date DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `phone_no` bigint(20) DEFAULT NULL,
  `email` varchar(20) DEFAULT NULL,
  `login_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`sign_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `signup` */

insert  into `signup`(`sign_id`,`Name`,`Dob`,`gender`,`phone_no`,`email`,`login_id`) values (1,'Rizvana','1997-07-26','female',2147483647,'rizvana.k98@gmail.co',0),(3,'zx','1997-08-21','male',2147483647,'zx@gmail.com',3),(4,'ab','1997-08-21','male',9856734245,'ab@gmail.com',4),(5,'rizvana','1997-08-21','female',9856734245,'rizvana@gmail.com',5);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
