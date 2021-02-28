-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 27, 2021 at 07:48 AM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `filed`
--

-- --------------------------------------------------------

--
-- Table structure for table `file`
--

CREATE TABLE `file` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `duration` int(11) NOT NULL CHECK (`duration` > 0),
  `uploadtime` datetime NOT NULL,
  `host` varchar(100) DEFAULT NULL,
  `author` varchar(100) DEFAULT NULL,
  `narrator` varchar(100) DEFAULT NULL,
  `participants` text DEFAULT NULL,
  `ftype` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `file`
--

INSERT INTO `file` (`id`, `name`, `duration`, `uploadtime`, `host`, `author`, `narrator`, `participants`, `ftype`) VALUES
(1, 'testfile1', 20, '2021-02-23 19:31:58', NULL, NULL, NULL, NULL, 1),
(2, 'testfile2', 500, '2021-02-23 19:34:10', 'testinghost', NULL, NULL, 'testing12, testing13', 2),
(4, 'testfile4', 78754, '2021-02-23 23:06:05', NULL, 'testingauthor', NULL, NULL, 3),
(10, 'hellotestsong', 1232, '2021-02-26 00:00:00', NULL, NULL, NULL, NULL, 1),
(11, 'hellotestsong', 1232, '2021-02-26 00:00:00', NULL, NULL, NULL, NULL, 1),
(12, 'hellotestsong', 1232, '2021-02-26 00:00:00', NULL, NULL, NULL, NULL, 1),
(13, 'hellotestsong', 1232, '2021-02-26 00:00:00', NULL, NULL, NULL, NULL, 1),
(14, 'hellotestsong', 1232, '2021-02-26 00:00:00', 'testhost', NULL, NULL, '[\'one1\', \'two2\', \'three3\']', 2),
(15, 'hellotestsong3', 123223, '2021-02-26 00:00:00', NULL, 'testauthorupoader', 'myoldnarrator', NULL, 3);

-- --------------------------------------------------------

--
-- Table structure for table `filetemp`
--

CREATE TABLE `filetemp` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `duration` int(11) NOT NULL CHECK (`duration` > 0),
  `uploadtime` datetime NOT NULL,
  `host` varchar(100) DEFAULT NULL,
  `author` varchar(100) DEFAULT NULL,
  `narrator` varchar(100) DEFAULT NULL,
  `ftype` int(11) NOT NULL,
  `correctdate` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `filetype`
--

CREATE TABLE `filetype` (
  `id` int(11) NOT NULL,
  `filetype` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `filetype`
--

INSERT INTO `filetype` (`id`, `filetype`) VALUES
(1, 'song'),
(2, 'podcast'),
(3, 'audiobook');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `file`
--
ALTER TABLE `file`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `filetemp`
--
ALTER TABLE `filetemp`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `filetype`
--
ALTER TABLE `filetype`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `file`
--
ALTER TABLE `file`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `filetemp`
--
ALTER TABLE `filetemp`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `filetype`
--
ALTER TABLE `filetype`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
