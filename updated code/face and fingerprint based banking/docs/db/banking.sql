-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.0.17-nt - MySQL Community Edition (GPL)
-- Server OS:                    Win32
-- HeidiSQL Version:             9.4.0.5174
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for bank_system
CREATE DATABASE IF NOT EXISTS `bank_system` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `bank_system`;

-- Dumping structure for table bank_system.admin
CREATE TABLE IF NOT EXISTS `admin` (
  `id` int(11) NOT NULL auto_increment,
  `email` varchar(150) NOT NULL default '0',
  `password` varchar(150) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table bank_system.admin: ~1 rows (approximately)
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` (`id`, `email`, `password`) VALUES
	(1, 'admin@gmail.com', '123');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;

-- Dumping structure for table bank_system.customers
CREATE TABLE IF NOT EXISTS `customers` (
  `id` int(11) NOT NULL auto_increment,
  `full_name` varchar(200) NOT NULL default '0',
  `email` varchar(200) NOT NULL default '0',
  `phone` varchar(200) NOT NULL default '0',
  `gender` varchar(200) NOT NULL default '0',
  `dob` varchar(200) NOT NULL default '0',
  `aadhar` varchar(200) NOT NULL default '0',
  `pan` varchar(200) NOT NULL default '0',
  `picture` varchar(200) NOT NULL default '0',
  `fingerprint_id` varchar(200) NOT NULL default '0',
  `account_number` varchar(200) NOT NULL default '0',
  `balance` varchar(200) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table bank_system.customers: ~1 rows (approximately)
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` (`id`, `full_name`, `email`, `phone`, `gender`, `dob`, `aadhar`, `pan`, `picture`, `fingerprint_id`, `account_number`, `balance`) VALUES
	(1, 'shri', 'shri@gmail.com', '9632262392', 'Male', '1992-05-23', '741852963741', 'bsq1341g', '7654321.jpg', '0', '7654321', '390');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;

-- Dumping structure for table bank_system.transactions
CREATE TABLE IF NOT EXISTS `transactions` (
  `id` int(11) NOT NULL auto_increment,
  `userid` int(11) NOT NULL default '0',
  `transtype` varchar(150) NOT NULL default '0',
  `amount` varchar(150) NOT NULL default '0',
  `txdatetime` varchar(150) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `FK_transactions_customers` (`userid`),
  CONSTRAINT `FK_transactions_customers` FOREIGN KEY (`userid`) REFERENCES `customers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table bank_system.transactions: ~0 rows (approximately)
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` (`id`, `userid`, `transtype`, `amount`, `txdatetime`) VALUES
	(1, 1, 'debit', '50', '2025-08-26 16:46:21'),
	(2, 1, 'debit', '10', '2025-08-26 16:49:29'),
	(3, 1, 'debit', '30', '2025-08-26 17:04:55'),
	(4, 1, 'debit', '15', '2025-08-26 17:05:00'),
	(5, 1, 'debit', '5', '2025-08-26 17:05:04');
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
