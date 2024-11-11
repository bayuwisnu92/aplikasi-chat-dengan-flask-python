-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 11 Nov 2024 pada 05.48
-- Versi server: 10.4.27-MariaDB
-- Versi PHP: 8.3.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `chating`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('f29476febdf4');

-- --------------------------------------------------------

--
-- Struktur dari tabel `chat`
--

CREATE TABLE `chat` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `room_id` int(11) DEFAULT NULL,
  `message` text NOT NULL,
  `timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `chat`
--

INSERT INTO `chat` (`id`, `user_id`, `room_id`, `message`, `timestamp`) VALUES
(1, 2, 1, 'hay bayu\r\n', '2024-11-04 10:01:00'),
(2, 1, 1, 'naon bagong', '2024-11-04 10:02:02'),
(3, 3, 2, 'hay bay', '2024-11-04 10:07:58'),
(4, 1, 1, 'h\r\n', '2024-11-04 10:24:27'),
(5, 2, 1, 'naon koplok', '2024-11-04 10:29:15'),
(6, 2, 3, 'bay', '2024-11-04 12:55:48'),
(7, 2, 1, 'heeh siamah koplok\r\n', '2024-11-04 13:05:18'),
(8, 1, 1, 'naon ai sia', '2024-11-04 13:05:35'),
(9, 1, 1, 'iraha kawin', '2024-11-04 13:12:47'),
(10, 2, 1, 'naon euy', '2024-11-04 13:13:10'),
(11, 2, 1, 'bengeut maneh', '2024-11-04 13:13:26'),
(12, 1, 1, 'bay', '2024-11-04 13:13:55'),
(13, 1, 1, 'naon bray', '2024-11-04 13:16:27'),
(14, 2, 1, 'isuk urng rek kaimah ', '2024-11-04 13:19:17'),
(15, 1, 1, 'sok weh ai rek kaimah ', '2024-11-04 13:19:34'),
(16, 2, 1, 'kumaha damang', '2024-11-04 13:22:28'),
(17, 1, 1, 'damang', '2024-11-04 13:22:37'),
(18, 2, 1, 'koplok', '2024-11-04 13:32:27'),
(19, 1, 1, 'bay', '2024-11-04 13:32:48'),
(20, 2, 1, 'euy', '2024-11-04 13:33:34'),
(21, 1, 1, 'naon bajingan', '2024-11-04 13:33:55'),
(22, 1, 1, 'tai', '2024-11-04 13:40:52'),
(23, 2, 1, 'naon ai sia bajingan', '2024-11-04 13:41:04'),
(24, 2, 1, 'koplok', '2024-11-04 13:45:05'),
(26, 2, 1, 'heeh jigana kudu dibius heula ', '2024-11-04 13:46:00'),
(27, 2, 3, 'naon dasar bajingan', '2024-11-04 13:53:54'),
(28, 3, 3, 'naon ai sia ??', '2024-11-04 13:54:04'),
(29, 2, 3, 'bengeut sia jiga tutup termos', '2024-11-04 13:54:16'),
(30, 3, 3, 'beunget maneh jiga tutup panci', '2024-11-04 13:54:32'),
(31, 2, 3, 'naon sia nganjak gelud ?\n', '2024-11-04 13:54:43'),
(32, 3, 3, 'hayu wae aingamah', '2024-11-04 13:54:51'),
(33, 2, 1, 'b', '2024-11-04 14:45:34'),
(34, 3, 3, 'naon', '2024-11-04 14:46:01'),
(35, 1, 2, 'bay', '2024-11-04 14:47:58'),
(36, 3, 2, 'naon bray', '2024-11-04 14:48:05'),
(37, 1, 2, 'nini sia dagang', '2024-11-04 14:49:14'),
(38, 2, 3, 'beunget', '2024-11-04 14:50:49'),
(39, 3, 3, 'urang perkosa c nindi', '2024-11-04 14:52:40'),
(40, 2, 3, 'hayu', '2024-11-04 14:52:45'),
(41, 2, 3, 'perkosa sekalian weh c rahmana', '2024-11-04 15:56:46'),
(42, 3, 3, 'ngeunah jiganam', '2024-11-04 15:57:08'),
(43, 2, 3, 'kampret', '2024-11-04 21:37:06'),
(44, 3, 3, 'jahanam', '2024-11-04 21:37:22'),
(45, 2, 3, 'dasar mra\'bal', '2024-11-04 21:37:50'),
(46, 3, 3, 'naon bangsard', '2024-11-04 21:38:30'),
(47, 2, 3, 'naon ai sia ?', '2024-11-04 21:38:39'),
(48, 2, 3, 'hayu urang culik c nindi,rahma,jeung putri azzahra', '2024-11-04 21:45:32'),
(49, 3, 3, 'bray', '2024-11-04 22:04:48'),
(50, 3, 3, 'bray', '2024-11-04 22:04:54'),
(51, 3, 3, 'bra', '2024-11-04 22:06:33'),
(52, 2, 3, 'naon bangsad', '2024-11-04 22:06:41'),
(53, 3, 3, 'ekeur naon sia ?\n', '2024-11-04 22:06:59'),
(54, 2, 3, 'teu keur nanaon ', '2024-11-04 22:07:06'),
(55, 1, 2, 'bray', '2024-11-05 04:25:21'),
(56, 3, 2, 'naon ajig', '2024-11-05 04:25:29'),
(57, 1, 2, 'henteu nanya weh', '2024-11-05 04:25:42'),
(58, 3, 2, 'naon manehmah geje ah', '2024-11-05 04:25:51'),
(59, 1, 2, 'bae weh bangsad ', '2024-11-05 04:26:01'),
(60, 3, 2, 'hallo ajiga', '2024-11-05 07:43:33'),
(61, 1, 2, 'oy', '2024-11-05 07:43:48'),
(62, 1, 2, 'kenapa ', '2024-11-05 07:44:04'),
(63, 1, 2, 'bangsad ', '2024-11-05 07:44:25'),
(64, 3, 2, 'keur naon sia', '2024-11-05 07:44:52'),
(65, 1, 2, 'naon weh ajiga', '2024-11-05 07:44:58'),
(66, 3, 2, 'kaman wae ai maneh?', '2024-11-05 07:45:09'),
(67, 1, 2, 'aya ai maneh kamana ?\n', '2024-11-05 07:45:17'),
(68, 1, 2, 'hasni nurul wildaniah', '2024-11-05 08:33:14'),
(69, 3, 2, 'naon euy', '2024-11-05 08:33:27'),
(70, 1, 2, 'bangke', '2024-11-05 08:33:46'),
(71, 3, 2, 'naon ai sia bangke', '2024-11-05 08:33:52'),
(72, 1, 1, 'bay', '2024-11-05 11:17:05'),
(73, 3, 2, 'bray', '2024-11-05 11:18:10'),
(74, 1, 2, 'naon bangke', '2024-11-05 11:18:16'),
(75, 3, 2, 'henteu', '2024-11-05 11:18:20'),
(76, 1, 2, 'ai maneh kamawa wae ?', '2024-11-05 11:18:28'),
(77, 3, 2, 'aya diimah', '2024-11-05 11:18:35'),
(78, 1, 2, 'aya naon kitu ?', '2024-11-05 11:18:41'),
(79, 1, 2, 'naon ajig', '2024-11-05 12:25:22'),
(80, 1, 2, 'tes', '2024-11-05 12:26:04'),
(81, 1, 2, 'bansad', '2024-11-05 12:26:25'),
(82, 3, 2, 'naon ajig', '2024-11-05 12:26:37'),
(83, 1, 2, 'bangsad', '2024-11-05 12:26:59'),
(84, 1, 2, 'hayu urng ewe c nindi', '2024-11-05 12:27:36'),
(85, 3, 2, 'hayu,, urang bius heula , terus urng ewe', '2024-11-05 12:28:04'),
(86, 1, 2, 'kuy', '2024-11-05 12:30:06'),
(87, 1, 2, 'hayu ah sakalian ewe c rahma adina', '2024-11-05 12:30:45'),
(88, 3, 2, 'ah tai', '2024-11-05 12:31:22'),
(89, 1, 2, 'beungeut sia jika tutup termos', '2024-11-05 13:41:00'),
(90, 3, 2, 'ohayo gozaimasu', '2024-11-06 03:06:05'),
(91, 1, 2, 'naon gong ?', '2024-11-06 03:06:15'),
(92, 3, 2, 'henteu', '2024-11-06 03:06:22'),
(93, 3, 2, 'bangke', '2024-11-06 03:43:27'),
(94, 3, 2, 'naon brader ', '2024-11-06 03:44:37'),
(95, 1, 2, 'naon euy riewuh', '2024-11-06 03:44:49'),
(96, 3, 2, 'maneh rek kamana poe ayeuna ? ', '2024-11-06 03:45:25'),
(97, 1, 2, 'rek diimah weh urngmah', '2024-11-06 03:45:34'),
(98, 3, 2, 'naha ?', '2024-11-06 03:45:39'),
(99, 1, 2, 'teuing atuh', '2024-11-06 03:45:45'),
(100, 3, 2, 'aku ingin terban tinggi seperti elang ', '2024-11-06 05:39:38'),
(101, 1, 1, 'kumaha maneh weh koplok', '2024-11-06 09:32:39'),
(102, 1, 1, 'kenapa kamu menggunakan byakugan ?', '2024-11-06 09:57:45'),
(103, 1, 2, 'pengen ewean sama widi,rahma,nindi,putri azzahra, rizka', '2024-11-06 10:35:50'),
(104, 3, 2, 'kuy atuh urng ewe cewe2 eta wkwk waitlist wkwk', '2024-11-06 10:44:01'),
(105, 3, 2, 'haha', '2024-11-06 10:44:28'),
(106, 3, 3, 'bangke', '2024-11-06 12:04:22'),
(107, 3, 2, 'bay isuk aya diimah ?', '2024-11-06 12:27:38'),
(108, 3, 2, 'mun aya urng rek kaimah', '2024-11-06 12:28:50'),
(109, 3, 2, 'waras euy maneh', '2024-11-06 12:47:50'),
(110, 3, 2, 'urang ulin yuah kateun c ridwan hasanudin', '2024-11-06 12:48:31'),
(111, 3, 2, 'urang aya piobroleun', '2024-11-06 12:50:06'),
(112, 3, 2, 'bay', '2024-11-06 12:50:27'),
(113, 3, 2, 'woy', '2024-11-06 12:50:54'),
(114, 3, 2, 'ajig teh diajak ngobrol teh ', '2024-11-06 12:54:09'),
(115, 3, 2, 'heeh atuh', '2024-11-06 12:57:20'),
(116, 3, 2, 'beunget', '2024-11-06 12:58:08'),
(117, 3, 2, 'dan kamu', '2024-11-06 12:59:38'),
(118, 1, 2, 'naon bangke', '2024-11-06 12:59:51'),
(119, 1, 2, 'urng rek kateun', '2024-11-06 13:00:10'),
(120, 3, 2, 'hyu atuh', '2024-11-06 13:00:46'),
(121, 3, 2, 'bray', '2024-11-06 13:03:48'),
(122, 3, 2, 'ohayou gozaimasu', '2024-11-06 13:05:07'),
(123, 3, 2, 'ah urang ge', '2024-11-06 13:06:25'),
(124, 3, 2, 'brangsak ', '2024-11-06 13:13:16'),
(125, 3, 2, 'kaman wae ai maneh', '2024-11-06 13:13:42'),
(126, 1, 2, 'aya urng ', '2024-11-06 13:13:55'),
(127, 1, 2, 'ai sia', '2024-11-06 13:14:21'),
(128, 3, 2, 'urang rek kaimah maneh', '2024-11-06 13:14:33'),
(129, 3, 2, 'kumaha maneh weh', '2024-11-06 13:18:31'),
(131, 1, 2, 'kaman wae maneh jang ', '2024-11-06 13:18:56'),
(132, 1, 2, 'urang rek kaimah maneh', '2024-11-06 13:19:08'),
(133, 3, 2, 'bay', '2024-11-06 13:53:14'),
(135, 2, 1, 'karena kamu ganteng', '2024-11-06 13:58:40'),
(136, 2, 1, 'ai sia', '2024-11-06 13:59:10'),
(137, 2, 1, 'naon bray', '2024-11-06 14:01:05'),
(155, 2, 1, 'naon bogeng ?', '2024-11-07 15:10:42'),
(156, 2, 5, 'naon gong', '2024-11-07 21:35:53'),
(159, 2, 5, 'gpp', '2024-11-07 21:43:24'),
(161, 2, 1, 'alhamdulillah', '2024-11-07 21:45:00'),
(166, 1, 1, 'hayu urng mekprek', '2024-11-08 00:18:05'),
(167, 1, 1, 'kenapa kamu pengen mekprek', '2024-11-08 00:18:28'),
(168, 2, 1, 'kapanap ', '2024-11-08 00:36:08'),
(169, 2, 1, 'kamu', '2024-11-08 00:36:11'),
(170, 2, 1, 'pengen ngeew hasni', '2024-11-08 00:36:16'),
(171, 2, 1, 'apa kamu', '2024-11-08 00:36:29'),
(172, 2, 1, 'apakaah kamu pengen ewean?', '2024-11-08 00:37:22'),
(173, 2, 1, 'naon sia', '2024-11-08 00:38:01'),
(174, 4, 4, 'bay', '2024-11-08 00:44:31'),
(175, 4, 4, 'naon', '2024-11-08 00:44:47'),
(176, 4, 4, 'naon', '2024-11-08 00:44:56'),
(177, 1, 4, 'hasni pengen diewe sama kang bayu', '2024-11-08 01:26:59'),
(178, 1, 4, 'hasni pengen di ewe sama kang bayu', '2024-11-08 01:27:27'),
(179, 1, 4, 'hay', '2024-11-08 02:11:11'),
(180, 1, 4, 'naon ajig', '2024-11-08 02:11:36'),
(181, 1, 4, 'hasni', '2024-11-08 02:12:47'),
(182, 4, 4, 'hay', '2024-11-08 02:14:23'),
(183, 1, 4, 'hasni cantik', '2024-11-08 02:14:49'),
(184, 1, 4, 'kapan kamu pengen diewe', '2024-11-08 02:15:00'),
(185, 4, 4, 'apa', '2024-11-08 02:15:49'),
(186, 1, 4, 'kapan', '2024-11-08 02:40:36'),
(187, 1, 4, 'kaan', '2024-11-08 02:40:41'),
(188, 1, 4, 'naon', '2024-11-08 02:40:47'),
(189, 4, 4, 'na', '2024-11-08 02:40:56'),
(190, 4, 4, 'naon', '2024-11-08 02:41:01'),
(191, 4, 4, 'hasni', '2024-11-08 02:41:09'),
(192, 1, 4, 'nsdf', '2024-11-08 02:41:30'),
(193, 4, 4, 'naon ai sia', '2024-11-08 02:41:46'),
(194, 1, 4, 'apa', '2024-11-08 02:42:14'),
(195, 4, 4, 'apa', '2024-11-08 02:42:24'),
(196, 1, 4, 'naon', '2024-11-08 05:21:59'),
(197, 1, 4, 'bray', '2024-11-08 05:22:04'),
(198, 1, 4, 'mas bayu kita mekprek yu', '2024-11-08 11:10:30'),
(199, 1, 4, 'kapan kita ', '2024-11-08 11:10:47'),
(200, 4, 4, 'apa ', '2024-11-08 11:10:53'),
(202, 4, 4, 'kuy', '2024-11-08 13:34:48'),
(204, 4, 5, 'bray', '2024-11-08 21:39:38'),
(205, 5, 7, 'bay kumaha damang', '2024-11-08 21:42:45'),
(207, 1, 8, 'man kumaha kabar', '2024-11-08 21:45:53'),
(213, 6, 8, 'kamana wae', '2024-11-09 03:06:30'),
(214, 6, 8, 'atuh', '2024-11-09 03:06:43'),
(215, 6, 8, 'urng ngobrol penting', '2024-11-09 03:07:46'),
(216, 6, 8, 'urng', '2024-11-09 03:08:12'),
(217, 6, 8, 'naon', '2024-11-09 03:08:14'),
(218, 6, 8, 'kamana waae', '2024-11-09 03:08:23'),
(219, 6, 8, 'ulin atuh', '2024-11-09 03:08:49'),
(220, 6, 8, 'haha', '2024-11-09 03:08:52'),
(221, 6, 8, 'wkwk', '2024-11-09 03:08:53'),
(222, 6, 9, 'bro', '2024-11-09 12:27:19'),
(223, 6, 9, 'kaman wae euy ?', '2024-11-09 12:27:29'),
(224, 6, 9, 'kamana wae maneh', '2024-11-09 12:27:40'),
(225, 6, 9, 'urang rek kaimah bisa ?', '2024-11-09 12:27:45'),
(227, 1, 4, 'asslam hasni sayang', '2024-11-10 04:23:53'),
(228, 1, 4, '<div><a href=\"https://www.youtube.com/watch?v=AGTjXPn-1hU\"><br>https://www.youtube.com/watch?v=AGTjXPn-1hU</a></div>', '2024-11-10 04:25:19'),
(229, 1, 4, '<div></div>', '2024-11-10 04:25:48'),
(230, 1, 4, '<div><a href=\"https://www.youtube.com/watch?v=AGTjXPn-1hU\">(487) GEDUNG LENYAP DALAM 20 DETIK Saat Banyak Pengunjung Berada di Dalamnya! TRAGEDl MALL SAMPO0NG - YouTube</a></div>', '2024-11-10 04:26:52'),
(231, 1, 4, '<div>kapan<br><br></div>', '2024-11-10 04:27:11'),
(232, 1, 4, '<div>kamu mau main lagi ke rumah aku</div>', '2024-11-10 04:27:21'),
(237, 1, 7, 'appan tuh', '2024-11-11 00:15:28'),
(243, 1, 7, '<div>kenapa kamu sangat</div>', '2024-11-11 00:30:41'),
(259, 5, 7, 'kapan', '2024-11-11 02:24:43'),
(260, 5, 7, 'kapan kamu sangat inign kawin sama kharia', '2024-11-11 02:27:25'),
(262, 1, 4, 'pengen diewe ?', '2024-11-11 03:06:04'),
(263, 4, 4, 'hayu atuh kang bayu kita ewean ', '2024-11-11 03:09:01'),
(264, 4, 5, 'karena wanita ingin dimngerti', '2024-11-11 05:10:48'),
(265, 4, 4, 'hasni pengen punya banyak anak sama kang bayu ', '2024-11-11 05:11:15'),
(266, 1, 4, 'hayu atuh kita mekprek', '2024-11-11 05:11:31');

-- --------------------------------------------------------

--
-- Struktur dari tabel `chat_room`
--

CREATE TABLE `chat_room` (
  `id` int(11) NOT NULL,
  `room_name` varchar(100) NOT NULL,
  `user1_id` int(11) NOT NULL,
  `user2_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `chat_room`
--

INSERT INTO `chat_room` (`id`, `room_name`, `user1_id`, `user2_id`) VALUES
(1, 'saskeh92-bayuwisnu92', 2, 1),
(2, 'ujang9294-bayuwisnu92', 3, 1),
(3, 'ujang9294-saskeh92', 3, 2),
(4, 'hasninurul-bayuwisnu92', 4, 1),
(5, 'saskeh92-hasninurul', 2, 4),
(6, 'hasninurul-ujang9294', 4, 3),
(7, 'abengsitorus-bayuwisnu92', 5, 1),
(8, 'bayuwisnu92-hilman97', 1, 6),
(9, 'hilman97-abengsitorus', 6, 5),
(10, 'hasninurul-hilman97', 4, 6),
(11, 'hasninurul-abengsitorus', 4, 5);

-- --------------------------------------------------------

--
-- Struktur dari tabel `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(60) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password`, `created_at`, `updated_at`) VALUES
(1, 'bayuwisnu92', 'bayuwisnu9294@gmail.com', '$2b$12$5UK7sCXLbC8LrafYFn7MEO2Ghw0OrqhErVCns7Vlvg0LFnlyidByy', '2024-11-04 07:52:35', '2024-11-04 07:52:35'),
(2, 'saskeh92', 'ajiuchiha9294@gmail.com', '$2b$12$8w2BLQuaEoNUO2PGafefxeLFLEJA/.lWQxLbegk8N7ZWhOC6yM5PS', '2024-11-04 09:51:51', '2024-11-04 09:51:51'),
(3, 'ujang9294', 'ujang9294@gmail.com', '$2b$12$iUCnoU7VyvIGKaRfOs10wOCftLNNsxtK1Wq/ECK4lN7taNyVqv3Hy', '2024-11-04 10:07:16', '2024-11-04 10:07:16'),
(4, 'hasninurul', 'hasninurul9294@gmail.com', '$2b$12$N12l23nDqmdJwZA.aiqCdOi8heZU.FIzwe9Mev75NkZ.ncXLWpvgG', '2024-11-06 14:02:11', '2024-11-06 14:02:11'),
(5, 'abengsitorus', 'abeng9294@gmail.com', '$2b$12$z5DtvNH3I/JzoXRCoVtcUOvmE5C7uLP6iIqThFWrcWRy9w95kcreC', '2024-11-08 21:42:15', '2024-11-08 21:42:15'),
(6, 'hilman97', 'hilmansitorus9294@gmail.com', '$2b$12$n7T1HSA5A1RMTsKs5XXbjOf5UObmvJ4sHW2unoa.34oqpnXjG2RNa', '2024-11-08 21:44:56', '2024-11-08 21:44:56');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indeks untuk tabel `chat`
--
ALTER TABLE `chat`
  ADD PRIMARY KEY (`id`),
  ADD KEY `room_id` (`room_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indeks untuk tabel `chat_room`
--
ALTER TABLE `chat_room`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `room_name` (`room_name`),
  ADD KEY `user1_id` (`user1_id`),
  ADD KEY `user2_id` (`user2_id`);

--
-- Indeks untuk tabel `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `chat`
--
ALTER TABLE `chat`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=267;

--
-- AUTO_INCREMENT untuk tabel `chat_room`
--
ALTER TABLE `chat_room`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT untuk tabel `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `chat`
--
ALTER TABLE `chat`
  ADD CONSTRAINT `chat_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `chat_room` (`id`),
  ADD CONSTRAINT `chat_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Ketidakleluasaan untuk tabel `chat_room`
--
ALTER TABLE `chat_room`
  ADD CONSTRAINT `chat_room_ibfk_1` FOREIGN KEY (`user1_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `chat_room_ibfk_2` FOREIGN KEY (`user2_id`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
