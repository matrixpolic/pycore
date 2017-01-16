-- phpMyAdmin SQL Dump
-- version 4.4.10
-- http://www.phpmyadmin.net
--
-- Host: localhost:3306
-- Generation Time: Jan 16, 2017 at 12:00 PM
-- Server version: 5.5.42
-- PHP Version: 5.6.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `stock_zen`
--
CREATE TABLE `EUR_USD` (
  `code` char(10) CHARACTER SET utf8 DEFAULT NULL,
  `type` tinyint(1) DEFAULT NULL,
  `open` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `close` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `ma5` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `USD_JPY`
--
ALTER TABLE `EUR_USD`
  ADD PRIMARY KEY (`date`),
  ADD UNIQUE KEY `date_UNIQUE` (`date`);

-- --------------------------------------------------------

--
-- Table structure for table `GBP_USE_N_struct`
--

CREATE TABLE `EUR_USD_N_struct` (
  `code` char(20) CHARACTER SET utf8 DEFAULT NULL,
  `type` char(20) CHARACTER SET utf8 DEFAULT NULL,
  `n1` datetime DEFAULT NULL,
  `n2` datetime DEFAULT NULL,
  `n3` datetime DEFAULT NULL,
  `n4` datetime DEFAULT NULL,
  `n1_duration` int(11) DEFAULT NULL,
  `n2_duration` int(11) DEFAULT NULL,
  `n3_duration` int(11) DEFAULT NULL,
  `n4_duration` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `GBP_USE_N_struct`
--
ALTER TABLE `EUR_USD_N_struct`
  ADD UNIQUE KEY `index1` (`n4`,`type`,`code`);
