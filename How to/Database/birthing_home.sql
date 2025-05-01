-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 01, 2025 at 07:23 AM
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
  `accountstatus` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`ID`, `datesave`, `fullname`, `position`, `email`, `password`, `accountstatus`) VALUES
(8, '2025-04-08 03:26:51', 'Enrico Dungca', 'Nurse', 'dungcaenen@gmail.com', 'gAAAAABn9Jd7s7kyfB9LtR03e0e5P6ocsHgL9CbpUvfGKea6pPyIq41TynnyDqk2EH3nA7tgynRZcA-kW0sTkZoN3g9C4lhUCQ==', 'Active');

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

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`Id`, `Name`, `Gmail`, `Password`) VALUES
(2, 'VMUFBH_Admin', 'dungcaenen@gmail.com', '1BirthingHomeMSAdmin');

-- --------------------------------------------------------

--
-- Table structure for table `appointment`
--

CREATE TABLE `appointment` (
  `ID` int(11) NOT NULL,
  `datesave` timestamp NOT NULL DEFAULT current_timestamp(),
  `Fname` varchar(255) NOT NULL,
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

--
-- Dumping data for table `appointment`
--

INSERT INTO `appointment` (`ID`, `datesave`, `Fname`, `Lname`, `phonenum`, `email`, `apptDate`, `apptTime`, `apptType`, `provider`, `status`, `notes`, `staffID`) VALUES
(7, '2025-04-29 08:45:27', 'Enrico', 'Dungca', 2147483647, 'dungca@gmail.com', '2025-04-30', '03:15:00', 'Consultation', 'Dr. Smith', 'Completed', '', 8),
(8, '2025-04-29 19:56:22', 'Hill', 'Sauro', 9123123, 'hill@gmail.com', '2025-05-01', '20:30:00', 'Follow-up', 'Dr. Smith', 'Completed', 'N/A', 8);

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

--
-- Dumping data for table `billing`
--

INSERT INTO `billing` (`ID`, `datesave`, `patientID`, `patientName`, `itemused`, `totalpayment`, `totalcharges`, `balance`, `paymentMethod`, `paymentStatus`, `notes`, `staffID`) VALUES
(16, '2025-04-29 22:45:11', 8, 'Enrico Dungca', 'Flu Vaccine  x2  @ 500.00 = 1000.00', 1000, 1000, 0, 'Cash', 'Paid', 'N/A', 8);

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

--
-- Dumping data for table `checkup`
--

INSERT INTO `checkup` (`ID`, `datesave`, `patientID`, `patientName`, `date`, `bloodPressure`, `heartRate`, `respiratoryRate`, `temperature`, `oxygenSaturation`, `diagnosis`, `prescription`, `staffID`) VALUES
(8, '2025-04-29 22:42:37', 8, 'Enrico Dungca', '2025-04-30', '120/70', 55, 55, 37.2, 90, 'gastrointestinal disease\nhemorrhoids', 'pain reliever 3x a day', 8);

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

--
-- Dumping data for table `inventory`
--

INSERT INTO `inventory` (`ID`, `datesave`, `item`, `category`, `quantity`, `unitPrice`, `totalPrice`, `staffID`) VALUES
(6, '2025-04-24 02:30:37', 'IV Fluids', 'Medicine', 39, 250, 9750, 8),
(7, '2025-04-24 02:31:07', 'Flu Vaccine', 'Vaccine', 36, 500, 18000, 8),
(8, '2025-04-29 21:08:50', 'Covid-Vaccine', 'Vaccine', 38, 500, 19000, 8);

-- --------------------------------------------------------

--
-- Table structure for table `nsd`
--

CREATE TABLE `nsd` (
  `ID` int(11) NOT NULL,
  `datesave` timestamp NOT NULL DEFAULT current_timestamp(),
  `patientID` int(11) NOT NULL,
  `patientName` varchar(255) NOT NULL,
  `dateofdelivery` int(255) NOT NULL,
  `timeofdelivery` int(255) NOT NULL,
  `deliveryNote` varchar(255) NOT NULL,
  `Babyweight` float NOT NULL,
  `apgarScore` int(10) NOT NULL,
  `staffID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `nsd`
--

INSERT INTO `nsd` (`ID`, `datesave`, `patientID`, `patientName`, `dateofdelivery`, `timeofdelivery`, `deliveryNote`, `Babyweight`, `apgarScore`, `staffID`) VALUES
(5, '2025-04-29 22:43:42', 8, 'Enrico Dungca', 2025, 13, 'c section', 5, 123, 8);

-- --------------------------------------------------------

--
-- Table structure for table `registration`
--

CREATE TABLE `registration` (
  `ID` int(11) NOT NULL,
  `datesave` timestamp NOT NULL DEFAULT current_timestamp(),
  `fname` varchar(255) NOT NULL,
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
-- Dumping data for table `registration`
--

INSERT INTO `registration` (`ID`, `datesave`, `fname`, `lname`, `dob`, `gender`, `phonenum`, `email`, `Street`, `barangay`, `cityMunicipality`, `province`, `region`, `zip`, `ECname`, `ECrelationship`, `ECphone`, `ECemail`, `insuranceProvider`, `Policynum`, `GroupNum`, `PrimaryInsured`, `staffID`) VALUES
(8, '2025-04-29 22:40:01', 'Enrico', 'Dungca', '2003-10-12', 'Male', '0987654321', 'dungca@gmail.com', '1234', 'pob east', 'umingan', 'pangasinan', 'Ilocos Region (Region I)', '2443', 'henri', 'Brother', '0987654323', 'henri@gmail.com', 'philhealth', 1234, '1234-1234-1234-1234', '1234-1234-1234-1234', 8),
(9, '2025-05-01 05:19:58', 'Hill', 'Sauro', '2025-05-01', 'Male', '0987654321', 'hill@gmail.com', '123', 'pob west', 'San Carlos', 'Pangasinan', 'Ilocos Region (Region I)', '2420', 'hill Sauro', 'Brother', '12345667', 'hill@gmail.com', 'philhealth', 1234, '1234-1234-1234', '1234-1234-1234', 8);

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
  ADD KEY `staffID` (`staffID`);

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
  ADD KEY `staffID` (`staffID`);

--
-- Indexes for table `checkup`
--
ALTER TABLE `checkup`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `checkup_ibfk_1` (`patientID`),
  ADD KEY `staffID` (`staffID`);

--
-- Indexes for table `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `staffID` (`staffID`);

--
-- Indexes for table `nsd`
--
ALTER TABLE `nsd`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `nsd_ibfk_1` (`patientID`),
  ADD KEY `staffID` (`staffID`);

--
-- Indexes for table `registration`
--
ALTER TABLE `registration`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `staffID` (`staffID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts`
--
ALTER TABLE `accounts`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `appointment`
--
ALTER TABLE `appointment`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `attachment`
--
ALTER TABLE `attachment`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `billing`
--
ALTER TABLE `billing`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `checkup`
--
ALTER TABLE `checkup`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `inventory`
--
ALTER TABLE `inventory`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `nsd`
--
ALTER TABLE `nsd`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `registration`
--
ALTER TABLE `registration`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `appointment`
--
ALTER TABLE `appointment`
  ADD CONSTRAINT `appointment_ibfk_1` FOREIGN KEY (`staffID`) REFERENCES `accounts` (`ID`);

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
  ADD CONSTRAINT `billing_ibfk_2` FOREIGN KEY (`staffID`) REFERENCES `accounts` (`ID`);

--
-- Constraints for table `checkup`
--
ALTER TABLE `checkup`
  ADD CONSTRAINT `checkup_ibfk_1` FOREIGN KEY (`patientID`) REFERENCES `registration` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `checkup_ibfk_2` FOREIGN KEY (`staffID`) REFERENCES `accounts` (`ID`);

--
-- Constraints for table `inventory`
--
ALTER TABLE `inventory`
  ADD CONSTRAINT `inventory_ibfk_1` FOREIGN KEY (`staffID`) REFERENCES `accounts` (`ID`);

--
-- Constraints for table `nsd`
--
ALTER TABLE `nsd`
  ADD CONSTRAINT `nsd_ibfk_1` FOREIGN KEY (`patientID`) REFERENCES `registration` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `nsd_ibfk_2` FOREIGN KEY (`staffID`) REFERENCES `accounts` (`ID`);

--
-- Constraints for table `registration`
--
ALTER TABLE `registration`
  ADD CONSTRAINT `registration_ibfk_1` FOREIGN KEY (`staffID`) REFERENCES `accounts` (`ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
