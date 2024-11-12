-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 12 Nov 2024 pada 13.56
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
('23c4e4a43f7a');

-- --------------------------------------------------------

--
-- Struktur dari tabel `chat`
--

CREATE TABLE `chat` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `room_id` int(11) DEFAULT NULL,
  `message` text NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  `image_filename` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `chat`
--

INSERT INTO `chat` (`id`, `user_id`, `room_id`, `message`, `timestamp`, `image_filename`) VALUES
(267, 1, NULL, '', '2024-11-11 06:35:13', NULL),
(268, 1, NULL, '', '2024-11-11 06:35:21', NULL),
(269, 1, NULL, 'apa yang sudah ', '2024-11-11 06:35:34', NULL),
(271, 4, NULL, '', '2024-11-11 06:39:01', NULL),
(273, 1, NULL, '', '2024-11-11 06:54:03', NULL);

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
(11, 'hasninurul-abengsitorus', 4, 5),
(12, 'abengsitorus-saskeh92', 5, 2);

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
  `updated_at` datetime DEFAULT NULL,
  `gambar_filename` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password`, `created_at`, `updated_at`, `gambar_filename`) VALUES
(1, 'bayuwisnu92', 'bayuwisnu9294@gmail.com', '$2b$12$5UK7sCXLbC8LrafYFn7MEO2Ghw0OrqhErVCns7Vlvg0LFnlyidByy', '2024-11-04 07:52:35', '2024-11-12 06:20:09', 'profile_pics/XpRc_5wWSM1GZOlqXseqy-transformed.png'),
(2, 'saskeh92', 'ajiuchiha9294@gmail.com', '$2b$12$8w2BLQuaEoNUO2PGafefxeLFLEJA/.lWQxLbegk8N7ZWhOC6yM5PS', '2024-11-04 09:51:51', '2024-11-04 09:51:51', NULL),
(3, 'ujang9294', 'ujang9294@gmail.com', '$2b$12$iUCnoU7VyvIGKaRfOs10wOCftLNNsxtK1Wq/ECK4lN7taNyVqv3Hy', '2024-11-04 10:07:16', '2024-11-04 10:07:16', NULL),
(4, 'hasninurul', 'hasninurul9294@gmail.com', '$2b$12$N12l23nDqmdJwZA.aiqCdOi8heZU.FIzwe9Mev75NkZ.ncXLWpvgG', '2024-11-06 14:02:11', '2024-11-12 03:56:57', 'profile_pics/orang-orangan.jpg'),
(5, 'abengsitorus', 'abeng9294@gmail.com', '$2b$12$z5DtvNH3I/JzoXRCoVtcUOvmE5C7uLP6iIqThFWrcWRy9w95kcreC', '2024-11-08 21:42:15', '2024-11-12 07:56:07', 'profile_pics/monyet_besar.png'),
(6, 'hilman97', 'hilmansitorus9294@gmail.com', '$2b$12$n7T1HSA5A1RMTsKs5XXbjOf5UObmvJ4sHW2unoa.34oqpnXjG2RNa', '2024-11-08 21:44:56', '2024-11-08 21:44:56', NULL);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=322;

--
-- AUTO_INCREMENT untuk tabel `chat_room`
--
ALTER TABLE `chat_room`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

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
