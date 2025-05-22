-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 22, 2025 at 09:17 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `birthing_home`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

CREATE TABLE `accounts` (
  `ID` int(11) NOT NULL,
  `datesave` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `fullname` varchar(255) NOT NULL,
  `position` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `accountstatus` varchar(255) NOT NULL,
  `otpStatus` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `Id` int(11) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Gmail` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `appointment`
--

CREATE TABLE `appointment` (
  `ID` int(11) NOT NULL,
  `datesave` timestamp NOT NULL DEFAULT current_timestamp(),
  `Fname` varchar(255) NOT NULL,
  `mname` varchar(255) NOT NULL,
  `Lname` varchar(255) NOT NULL,
  `phonenum` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `apptDate` date NOT NULL,
  `apptTime` time NOT NULL,
  `apptType` varchar(255) NOT NULL,
  `provider` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  `notes` varchar(255) NOT NULL,
  `staffID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `attachment`
--

CREATE TABLE `attachment` (
  `ID` int(11) NOT NULL,
  `datesave` timestamp NOT NULL DEFAULT current_timestamp(),
  `patientID` int(11) NOT NULL,
  `filename` text NOT NULL,
  `attachment` longblob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `billing`
--

CREATE TABLE `billing` (
  `ID` int(11) NOT NULL,
  `datesave` timestamp NOT NULL DEFAULT current_timestamp(),
  `patientID` int(11) NOT NULL,
  `patientName` varchar(255) NOT NULL,
  `itemused` varchar(255) NOT NULL,
  `totalpayment` bigint(20) NOT NULL,
  `totalcharges` bigint(20) NOT NULL,
  `balance` bigint(20) NOT NULL,
  `paymentMethod` varchar(255) NOT NULL,
  `paymentStatus` varchar(255) NOT NULL,
  `notes` varchar(255) NOT NULL,
  `staffID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `checkup`
--

CREATE TABLE `checkup` (
  `ID` int(11) NOT NULL,
  `datesave` timestamp NOT NULL DEFAULT current_timestamp(),
  `patientID` int(11) NOT NULL,
  `patientName` varchar(255) NOT NULL,
  `date` date NOT NULL,
  `bloodPressure` varchar(50) NOT NULL,
  `heartRate` int(5) NOT NULL,
  `respiratoryRate` int(5) NOT NULL,
  `temperature` float NOT NULL,
  `oxygenSaturation` int(5) NOT NULL,
  `diagnosis` varchar(1000) NOT NULL,
  `prescription` varchar(1000) NOT NULL,
  `staffID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

CREATE TABLE `inventory` (
  `ID` int(11) NOT NULL,
  `datesave` timestamp NOT NULL DEFAULT current_timestamp(),
  `item` varchar(255) NOT NULL,
  `category` varchar(255) NOT NULL,
  `quantity` bigint(20) NOT NULL,
  `unitPrice` float NOT NULL,
  `totalPrice` float NOT NULL,
  `staffID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `nsd`
--

CREATE TABLE `nsd` (
  `ID` int(11) NOT NULL,
  `datesave` timestamp NOT NULL DEFAULT current_timestamp(),
  `patientID` int(11) NOT NULL,
  `patientName` varchar(255) NOT NULL,
  `dateofdelivery` date NOT NULL,
  `timeofdelivery` varchar(255) NOT NULL,
  `deliveryNote` varchar(255) NOT NULL,
  `Babyweight` float NOT NULL,
  `apgarScore` int(10) NOT NULL,
  `staffID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `registration`
--

CREATE TABLE `registration` (
  `ID` int(11) NOT NULL,
  `datesave` timestamp NOT NULL DEFAULT current_timestamp(),
  `fname` varchar(255) NOT NULL,
  `mname` varchar(255) NOT NULL,
  `lname` varchar(255) NOT NULL,
  `dob` date NOT NULL,
  `gender` varchar(255) NOT NULL,
  `phonenum` varchar(15) NOT NULL,
  `email` varchar(255) NOT NULL,
  `Street` varchar(255) NOT NULL,
  `barangay` varchar(255) NOT NULL,
  `cityMunicipality` varchar(255) NOT NULL,
  `province` varchar(255) NOT NULL,
  `region` varchar(255) NOT NULL,
  `zip` varchar(255) NOT NULL,
  `ECname` varchar(255) NOT NULL,
  `ECrelationship` varchar(255) NOT NULL,
  `ECphone` varchar(15) NOT NULL,
  `ECemail` varchar(255) NOT NULL,
  `insuranceProvider` varchar(255) NOT NULL,
  `Policynum` int(50) NOT NULL,
  `GroupNum` varchar(255) NOT NULL,
  `PrimaryInsured` varchar(255) NOT NULL,
  `staffID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `appointment`
--
ALTER TABLE `appointment`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `appointment_ibfk_1` (`staffID`);

--
-- Indexes for table `attachment`
--
ALTER TABLE `attachment`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `attachment_ibfk_1` (`patientID`);

--
-- Indexes for table `billing`
--
ALTER TABLE `billing`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `billing_ibfk_1` (`patientID`),
  ADD KEY `billing_ibfk_2` (`staffID`);

--
-- Indexes for table `checkup`
--
ALTER TABLE `checkup`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `checkup_ibfk_1` (`patientID`),
  ADD KEY `checkup_ibfk_2` (`staffID`);

--
-- Indexes for table `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `inventory_ibfk_1` (`staffID`);

--
-- Indexes for table `nsd`
--
ALTER TABLE `nsd`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `nsd_ibfk_1` (`patientID`),
  ADD KEY `nsd_ibfk_2` (`staffID`);

--
-- Indexes for table `registration`
--
ALTER TABLE `registration`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `registration_ibfk_1` (`staffID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts`
--
ALTER TABLE `accounts`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `appointment`
--
ALTER TABLE `appointment`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `attachment`
--
ALTER TABLE `attachment`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `billing`
--
ALTER TABLE `billing`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `checkup`
--
ALTER TABLE `checkup`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `inventory`
--
ALTER TABLE `inventory`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `nsd`
--
ALTER TABLE `nsd`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `registration`
--
ALTER TABLE `registration`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `appointment`
--
ALTER TABLE `appointment`
  ADD CONSTRAINT `appointment_ibfk_1` FOREIGN KEY (`staffID`) REFERENCES `accounts` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `attachment`
--
ALTER TABLE `attachment`
  ADD CONSTRAINT `attachment_ibfk_1` FOREIGN KEY (`PatientID`) REFERENCES `registration` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `billing`
--
ALTER TABLE `billing`
  ADD CONSTRAINT `billing_ibfk_1` FOREIGN KEY (`patientID`) REFERENCES `registration` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `billing_ibfk_2` FOREIGN KEY (`staffID`) REFERENCES `accounts` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `checkup`
--
ALTER TABLE `checkup`
  ADD CONSTRAINT `checkup_ibfk_1` FOREIGN KEY (`patientID`) REFERENCES `registration` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `checkup_ibfk_2` FOREIGN KEY (`staffID`) REFERENCES `accounts` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `inventory`
--
ALTER TABLE `inventory`
  ADD CONSTRAINT `inventory_ibfk_1` FOREIGN KEY (`staffID`) REFERENCES `accounts` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `nsd`
--
ALTER TABLE `nsd`
  ADD CONSTRAINT `nsd_ibfk_1` FOREIGN KEY (`patientID`) REFERENCES `registration` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `nsd_ibfk_2` FOREIGN KEY (`staffID`) REFERENCES `accounts` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `registration`
--
ALTER TABLE `registration`
  ADD CONSTRAINT `registration_ibfk_1` FOREIGN KEY (`staffID`) REFERENCES `accounts` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
