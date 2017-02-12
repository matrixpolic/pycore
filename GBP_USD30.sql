-- phpMyAdmin SQL Dump
-- version 4.4.10
-- http://www.phpmyadmin.net
--
-- Host: localhost:3306
-- Generation Time: 2017-01-24 05:39:06
-- 服务器版本： 5.5.42
-- PHP Version: 7.0.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `stock_zen`
--

-- --------------------------------------------------------

--
-- 表的结构 `GBP_USD30`
--

CREATE TABLE `USD_JPY30` (
  `code` varchar(10) COLLATE utf8_bin NOT NULL,
  `type` tinyint(1) NOT NULL,
  `open` double NOT NULL,
  `high` double NOT NULL,
  `close` double NOT NULL,
  `low` double NOT NULL,
  `date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `ma5` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- 表的结构 `GBP_USE_N_struct30`
--

CREATE TABLE `USD_JPY_N_struct30` (
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
-- Indexes for table `GBP_USD30`
--
ALTER TABLE `USD_JPY30`
  ADD PRIMARY KEY (`date`);
