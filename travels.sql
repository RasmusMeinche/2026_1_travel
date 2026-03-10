-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Vært: mariadb
-- Genereringstid: 10. 03 2026 kl. 19:46:38
-- Serverversion: 10.6.20-MariaDB-ubu2004
-- PHP-version: 8.3.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `2026_1_travel`
--

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `travels`
--

CREATE TABLE `travels` (
  `travel_pk` char(32) NOT NULL,
  `user_fk` char(32) NOT NULL,
  `title` varchar(100) NOT NULL,
  `country` varchar(56) NOT NULL,
  `location` varchar(50) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `description` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `travels`
--

INSERT INTO `travels` (`travel_pk`, `user_fk`, `title`, `country`, `location`, `start_date`, `end_date`, `description`) VALUES
('1', '9670f117b85443b190e2cbfdc51c1105', 'Aa', 'b', 'c', '2025-05-05', '2026-05-05', 'text');

--
-- Begrænsninger for dumpede tabeller
--

--
-- Indeks for tabel `travels`
--
ALTER TABLE `travels`
  ADD PRIMARY KEY (`travel_pk`),
  ADD KEY `user_fk` (`user_fk`);

--
-- Begrænsninger for dumpede tabeller
--

--
-- Begrænsninger for tabel `travels`
--
ALTER TABLE `travels`
  ADD CONSTRAINT `travels_ibfk_1` FOREIGN KEY (`user_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
