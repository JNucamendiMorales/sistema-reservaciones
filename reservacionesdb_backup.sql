-- --------------------------------------------------------
-- Host:                         localhost
-- Server version:               11.8.2-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.11.0.7065
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for reservacionesdb
DROP DATABASE IF EXISTS `reservacionesdb`;
CREATE DATABASE IF NOT EXISTS `reservacionesdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `reservacionesdb`;

-- Dumping structure for table reservacionesdb.auth_group
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table reservacionesdb.auth_group: ~0 rows (approximately)
DELETE FROM `auth_group`;

-- Dumping structure for table reservacionesdb.auth_group_permissions
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table reservacionesdb.auth_group_permissions: ~0 rows (approximately)
DELETE FROM `auth_group_permissions`;

-- Dumping structure for table reservacionesdb.auth_permission
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table reservacionesdb.auth_permission: ~32 rows (approximately)
DELETE FROM `auth_permission`;
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add log entry', 1, 'add_logentry'),
	(2, 'Can change log entry', 1, 'change_logentry'),
	(3, 'Can delete log entry', 1, 'delete_logentry'),
	(4, 'Can view log entry', 1, 'view_logentry'),
	(5, 'Can add permission', 2, 'add_permission'),
	(6, 'Can change permission', 2, 'change_permission'),
	(7, 'Can delete permission', 2, 'delete_permission'),
	(8, 'Can view permission', 2, 'view_permission'),
	(9, 'Can add group', 3, 'add_group'),
	(10, 'Can change group', 3, 'change_group'),
	(11, 'Can delete group', 3, 'delete_group'),
	(12, 'Can view group', 3, 'view_group'),
	(13, 'Can add user', 4, 'add_user'),
	(14, 'Can change user', 4, 'change_user'),
	(15, 'Can delete user', 4, 'delete_user'),
	(16, 'Can view user', 4, 'view_user'),
	(17, 'Can add content type', 5, 'add_contenttype'),
	(18, 'Can change content type', 5, 'change_contenttype'),
	(19, 'Can delete content type', 5, 'delete_contenttype'),
	(20, 'Can view content type', 5, 'view_contenttype'),
	(21, 'Can add session', 6, 'add_session'),
	(22, 'Can change session', 6, 'change_session'),
	(23, 'Can delete session', 6, 'delete_session'),
	(24, 'Can view session', 6, 'view_session'),
	(25, 'Can add salon', 7, 'add_salon'),
	(26, 'Can change salon', 7, 'change_salon'),
	(27, 'Can delete salon', 7, 'delete_salon'),
	(28, 'Can view salon', 7, 'view_salon'),
	(29, 'Can add reservacion', 8, 'add_reservacion'),
	(30, 'Can change reservacion', 8, 'change_reservacion'),
	(31, 'Can delete reservacion', 8, 'delete_reservacion'),
	(32, 'Can view reservacion', 8, 'view_reservacion'),
	(33, 'Can add favorito', 9, 'add_favorito'),
	(34, 'Can change favorito', 9, 'change_favorito'),
	(35, 'Can delete favorito', 9, 'delete_favorito'),
	(36, 'Can view favorito', 9, 'view_favorito');

-- Dumping structure for table reservacionesdb.auth_user
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table reservacionesdb.auth_user: ~1 rows (approximately)
DELETE FROM `auth_user`;
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
	(12, 'pbkdf2_sha256$1000000$dSOJv6bDKdKxlND6CVXMqi$eol5saplhYZVlYfQOtYwZpmW5g+K0tzyUvH4jz6M5b0=', '2025-11-03 08:15:58.190885', 1, 'Nucalized', '', '', 'nucalized@gmail.com', 1, 1, '2025-11-03 08:15:50.948252');

-- Dumping structure for table reservacionesdb.auth_user_groups
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table reservacionesdb.auth_user_groups: ~0 rows (approximately)
DELETE FROM `auth_user_groups`;

-- Dumping structure for table reservacionesdb.auth_user_user_permissions
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table reservacionesdb.auth_user_user_permissions: ~0 rows (approximately)
DELETE FROM `auth_user_user_permissions`;

-- Dumping structure for table reservacionesdb.django_admin_log
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=185 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table reservacionesdb.django_admin_log: ~1 rows (approximately)
DELETE FROM `django_admin_log`;
INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
	(184, '2025-11-03 08:17:32.830094', '31', 'Espejos de Plata', 2, '[{"changed": {"fields": ["Descripcion"]}}]', 7, 12);

-- Dumping structure for table reservacionesdb.django_content_type
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table reservacionesdb.django_content_type: ~8 rows (approximately)
DELETE FROM `django_content_type`;
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(1, 'admin', 'logentry'),
	(2, 'auth', 'permission'),
	(3, 'auth', 'group'),
	(4, 'auth', 'user'),
	(5, 'contenttypes', 'contenttype'),
	(6, 'sessions', 'session'),
	(7, 'myapp', 'salon'),
	(8, 'myapp', 'reservacion'),
	(9, 'myapp', 'favorito');

-- Dumping structure for table reservacionesdb.django_migrations
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table reservacionesdb.django_migrations: ~22 rows (approximately)
DELETE FROM `django_migrations`;
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'contenttypes', '0001_initial', '2025-08-01 20:15:46.730354'),
	(2, 'auth', '0001_initial', '2025-08-01 20:15:46.877171'),
	(3, 'admin', '0001_initial', '2025-08-01 20:15:46.910634'),
	(4, 'admin', '0002_logentry_remove_auto_add', '2025-08-01 20:15:46.938384'),
	(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-08-01 20:15:46.942840'),
	(6, 'contenttypes', '0002_remove_content_type_name', '2025-08-01 20:15:46.970200'),
	(7, 'auth', '0002_alter_permission_name_max_length', '2025-08-01 20:15:46.987293'),
	(8, 'auth', '0003_alter_user_email_max_length', '2025-08-01 20:15:46.998841'),
	(9, 'auth', '0004_alter_user_username_opts', '2025-08-01 20:15:47.003125'),
	(10, 'auth', '0005_alter_user_last_login_null', '2025-08-01 20:15:47.018021'),
	(11, 'auth', '0006_require_contenttypes_0002', '2025-08-01 20:15:47.018984'),
	(12, 'auth', '0007_alter_validators_add_error_messages', '2025-08-01 20:15:47.023112'),
	(13, 'auth', '0008_alter_user_username_max_length', '2025-08-01 20:15:47.034907'),
	(14, 'auth', '0009_alter_user_last_name_max_length', '2025-08-01 20:15:47.047638'),
	(15, 'auth', '0010_alter_group_name_max_length', '2025-08-01 20:15:47.059768'),
	(16, 'auth', '0011_update_proxy_permissions', '2025-08-01 20:15:47.064389'),
	(17, 'auth', '0012_alter_user_first_name_max_length', '2025-08-01 20:15:47.076269'),
	(18, 'myapp', '0001_initial', '2025-08-01 20:15:47.081892'),
	(19, 'myapp', '0002_task', '2025-08-01 20:15:47.101631'),
	(20, 'myapp', '0003_task_done', '2025-08-01 20:15:47.118716'),
	(21, 'myapp', '0004_salon_remove_task_project_reservacion_delete_project_and_more', '2025-08-01 20:15:47.317005'),
	(22, 'sessions', '0001_initial', '2025-08-01 20:15:47.332082'),
	(23, 'myapp', '0005_salon_ciudad_salon_imagen_salon_precio_salon_rating', '2025-08-06 17:39:10.918672'),
	(24, 'myapp', '0006_remove_salon_ciudad_remove_salon_rating_and_more', '2025-08-08 18:19:03.855677'),
	(25, 'myapp', '0007_salon_categoria', '2025-08-08 19:18:24.842592'),
	(26, 'myapp', '0008_salon_ciudad', '2025-08-08 19:33:37.263906'),
	(27, 'myapp', '0009_remove_reservacion_fecha_fin_and_more', '2025-08-10 00:00:41.668899'),
	(28, 'myapp', '0010_reservacion_pagada_alter_reservacion_unique_together', '2025-08-10 18:51:20.340009'),
	(29, 'myapp', '0011_reservacion_precio_total', '2025-08-11 05:54:14.373337'),
	(30, 'myapp', '0012_favorito', '2025-08-12 06:40:39.373236');

-- Dumping structure for table reservacionesdb.django_session
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table reservacionesdb.django_session: ~8 rows (approximately)
DELETE FROM `django_session`;
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('9gmi0v8n7po76up23klvoqf3c0mg25vm', '.eJxVjDsOwyAQRO9CHSG-Npsyvc-AFhaCkwgkY1dR7h5bcpE0U8x7M2_mcVuL33pa_EzsyiS7_HYB4zPVA9AD673x2Oq6zIEfCj9p51Oj9Lqd7t9BwV72NWSnKGchHSRwStvBCKWjgSilypacRhMpjwZSMGoEm_aUJCwR0hA0-3wBy-E3hA:1vEhxU:kbZT46ukESPAASr37PBeH85LVhxdPf3-kKocey9Gvyg', '2025-11-14 05:45:56.070023'),
	('c4yq0cenwuxdimz1i30zgdhyqohdrxuv', '.eJxVjDsOwyAQBe9CHSG-BlKm9xkQLLvBSYQlY1dR7h5bcpG0b2bem8W0rTVuHZc4FXZlUrHL75gTPLEdpDxSu88c5rYuU-aHwk_a-TgXfN1O9--gpl732hjUg0cVlLUETiQMAmTx5MllgUpRkVlpQ9K5YMOOhNFBJg0DEIjMPl_9tjgE:1vFpjK:Q4sdsmu3BptlmyUy61Qqw9Tf5Gh7Ms9tDlQY5G7dupk', '2025-11-17 08:15:58.192444'),
	('c52ficisjogqx8n28kwe04qrhr5z16e7', '.eJxVjM1uwyAQBt-Fc4Qwf4Uee88zoDW72KQuRAafqr57sRpF6R535ptvFuDoazga7SEje2eKXV5_M8RPKifAG5Sl8lhL3_PMT4U_aOPXirR9PNx_gRXaOtZeGRWlVRq1o-TJu6QiKiu0FMkizgbdm_SKnPBGamcFKDNTkomUxUmOaK8dtpBygW0EJ22c4GLcQEgtHlR6DXDfcgSsp2HlU4gV81JDLstO7Q_fa1ngiybBfn4BaH5TmA:1um4Oq:PsuFNBepgtQHhqJQFcwzRG32rKHpUXWd9Aedev7PFoA', '2025-08-27 05:51:48.823098'),
	('c7io88nm91fp8zeq07yq79zawy3iatli', '.eJxVjDEOAiEQRe9CbQjOAIKlvWcgwAyyaiBZdivj3XWTLbT9773_EiGuSw3r4DlMJM4CxeF3SzE_uG2A7rHdusy9LfOU5KbInQ557cTPy-7-HdQ46rf2aDCDRU3acfHsXcFMaJUGVSxRMuRO4JGd8ga0syqiSVygMFo6gnh_AM3KN1w:1umfhr:Zq3VbRwmRJqgQ6-MGQLIWd3N7kQO658i_m8y4NSJ6Wo', '2025-08-28 21:41:55.801304'),
	('l7txregq4m9bv7eo9n87gvieokes9j4c', '.eJxVjDsOwyAQBe9CHSHAfFOm9xnQsqyDkwgkY1dR7h4huUjaNzPvzSIce4lHpy2umV2ZYpffLQE-qQ6QH1DvjWOr-7YmPhR-0s7nlul1O92_gwK9jFq5BUCjBSe1Q48Blwm8UZMjsAaEs5mSEl5Pkih4A0Gg1SQdCgkys88X8hU3-w:1ulxog:cJL1GQYBXCg4mkVKU_U-LXBa8XDRJOUXaWbeYvsq8eo', '2025-08-26 22:50:02.649280'),
	('slhxe1z4b4a86msyjw8qx5zs973j98si', '.eJxVjDsOwyAQBe9CHSHAfFOm9xnQsqyDkwgkY1dR7h4huUjaNzPvzSIce4lHpy2umV2ZYpffLQE-qQ6QH1DvjWOr-7YmPhR-0s7nlul1O92_gwK9jFq5BUCjBSe1Q48Blwm8UZMjsAaEs5mSEl5Pkih4A0Gg1SQdCgkys88X8hU3-w:1ukuhU:dBzCAeA0Oz3PmcK5HRrcp1Z-kfhM1hrhtvD2i9pxkYY', '2025-08-24 01:18:16.770703'),
	('xzangyhl5z7jaos38cp5legxwyusq2v5', '.eJxVjDEOAiEQRe9CbQjOAIKlvWcgwAyyaiBZdivj3XWTLbT9773_EiGuSw3r4DlMJM4CxeF3SzE_uG2A7rHdusy9LfOU5KbInQ557cTPy-7-HdQ46rf2aDCDRU3acfHsXcFMaJUGVSxRMuRO4JGd8ga0syqiSVygMFo6gnh_AM3KN1w:1ulyeX:fCVBHtb8wPgrlLQpsNa7HVm9IJ1s4jIR5rdy2FwG_X8', '2025-08-26 23:43:37.913697'),
	('zj73oydb85bc5u15qogpehlvzt3kb6wa', '.eJxVjM0OwiAQhN-FsyG7dKXg0bvP0CywSNVA0p-T8d1tkx70NMl838xbDbwuZVhnmYYxqYtCVKffMnB8St1JenC9Nx1bXaYx6F3RB531rSV5XQ_376DwXLZ1x5wQGNkgidkyY0_BnzP01prOU8rEmMFHdA4EAJiw85aciSQS1ecL-N03ew:1vFgQE:nYurmq0IN8Y6q_8aTiCKxKy9IlHOuL4LrSazHz-X1l0', '2025-11-16 22:19:38.091734');

-- Dumping structure for table reservacionesdb.myapp_favorito
DROP TABLE IF EXISTS `myapp_favorito`;
CREATE TABLE IF NOT EXISTS `myapp_favorito` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `salon_id` bigint(20) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `myapp_favorito_usuario_id_salon_id_45d7dd9d_uniq` (`usuario_id`,`salon_id`),
  KEY `myapp_favorito_salon_id_1b74d9d6_fk_myapp_salon_id` (`salon_id`),
  CONSTRAINT `myapp_favorito_salon_id_1b74d9d6_fk_myapp_salon_id` FOREIGN KEY (`salon_id`) REFERENCES `myapp_salon` (`id`),
  CONSTRAINT `myapp_favorito_usuario_id_e2c2e57d_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table reservacionesdb.myapp_favorito: ~0 rows (approximately)
DELETE FROM `myapp_favorito`;

-- Dumping structure for table reservacionesdb.myapp_reservacion
DROP TABLE IF EXISTS `myapp_reservacion`;
CREATE TABLE IF NOT EXISTS `myapp_reservacion` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `estado` varchar(20) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `salon_id` bigint(20) NOT NULL,
  `fecha_reserva` date DEFAULT NULL,
  `pagada` tinyint(1) NOT NULL,
  `precio_total` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `myapp_reservacion_salon_id_fecha_reserva_491fd373_uniq` (`salon_id`,`fecha_reserva`),
  KEY `myapp_reservacion_usuario_id_cf61ee58_fk_auth_user_id` (`usuario_id`),
  CONSTRAINT `myapp_reservacion_salon_id_ed2a568c_fk_myapp_salon_id` FOREIGN KEY (`salon_id`) REFERENCES `myapp_salon` (`id`),
  CONSTRAINT `myapp_reservacion_usuario_id_cf61ee58_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table reservacionesdb.myapp_reservacion: ~1 rows (approximately)
DELETE FROM `myapp_reservacion`;
INSERT INTO `myapp_reservacion` (`id`, `estado`, `usuario_id`, `salon_id`, `fecha_reserva`, `pagada`, `precio_total`) VALUES
	(49, 'pendiente', 12, 11, '2025-11-12', 0, 11000.00);

-- Dumping structure for table reservacionesdb.myapp_salon
DROP TABLE IF EXISTS `myapp_salon`;
CREATE TABLE IF NOT EXISTS `myapp_salon` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `capacidad` int(11) NOT NULL,
  `descripcion` longtext NOT NULL,
  `disponible` tinyint(1) NOT NULL,
  `imagen` varchar(100) DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL,
  `calificacion` decimal(2,1) NOT NULL,
  `categoria` varchar(20) NOT NULL,
  `ciudad` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table reservacionesdb.myapp_salon: ~28 rows (approximately)
DELETE FROM `myapp_salon`;
INSERT INTO `myapp_salon` (`id`, `nombre`, `capacidad`, `descripcion`, `disponible`, `imagen`, `precio`, `calificacion`, `categoria`, `ciudad`) VALUES
	(2, 'Salon XV años', 300, '**Salón XV Años**\r\nAmplio y elegante espacio con capacidad para 300 invitados, diseñado especialmente para celebrar quinceañeras con estilo y comodidad. Cuenta con pista de baile iluminada, escenario para presentaciones, decoración personalizable y área de banquetes equipada, ideal para crear una noche inolvidable.', 1, 'salones/salon_xv.jpg', 20000.00, 4.7, 'fiestas', 'CDMX'),
	(3, 'Salón Torre Reforma', 70, 'El Salón Torre Reforma es un espacio moderno y elegante ideal para reuniones corporativas, talleres y eventos profesionales. Cuenta con una atmósfera tranquila y bien iluminada que favorece la concentración y la comunicación efectiva. Su diseño funcional permite una distribución versátil del mobiliario, adaptándose fácilmente a presentaciones, mesas de trabajo o sesiones interactivas. Ubicado en una zona accesible, ofrece todas las facilidades tecnológicas necesarias para asegurar el éxito de tus encuentros de negocio.', 1, 'salones/salon_reuniones1-300x200.jpg', 27000.00, 4.2, 'reuniones', 'CDMX'),
	(4, 'Salon expo', 420, 'El Salón Expo es un amplio y versátil espacio diseñado para exposiciones, ferias y eventos de gran escala. Su estructura abierta y bien iluminada permite exhibir productos, instalaciones artísticas o stands de manera organizada y atractiva. Equipado con tecnología de punta y fácil acceso, facilita la logística de montaje y la movilidad de los asistentes. Ideal para eventos que requieren amplitud, visibilidad y una experiencia cómoda para grandes públicos.', 1, 'salones/salon_expo-300x200.jpg', 28700.00, 4.6, 'expos', 'CDMX'),
	(5, 'Luz de Luna', 300, 'El Salón Luz de Luna ofrece un ambiente elegante y festivo, perfecto para celebraciones inolvidables como bodas, quinceañeras y eventos sociales. Su iluminación cálida y su decoración sofisticada crean un entorno acogedor que realza cada detalle de la celebración. Con un espacio amplio y versátil, permite acomodar cómodamente a todos los invitados, además de ofrecer áreas ideales para pista de baile, montaje de mesas y actividades especiales.', 1, 'salones/salon_boda1-300x200.jpg', 40000.00, 4.8, 'fiestas', 'Queretaro'),
	(6, 'Jardines del Sol', 250, 'El Salón Jardines del Sol combina elegancia y naturaleza, ofreciendo un entorno ideal para celebraciones íntimas y especiales. Sus amplios espacios y áreas verdes proporcionan una atmósfera fresca y relajante, perfecta para bodas, cumpleaños y eventos sociales. La versatilidad del lugar permite organizar cómodamente la pista de baile, mesas de invitados y zonas de entretenimiento, asegurando una experiencia memorable para todos los asistentes.', 1, 'salones/salon_jardin-300x200.jpg', 31000.00, 4.8, 'fiestas', 'CDMX'),
	(7, 'Palacio Esmeralda', 300, 'El Salón Palacio Esmeralda es un espacio sofisticado y majestuoso, ideal para celebraciones elegantes como bodas, quinceañeras y eventos sociales destacados. Su decoración refinada y su iluminación cuidadosamente diseñada crean un ambiente encantador y acogedor. Con amplias áreas para pista de baile, montaje de mesas y actividades especiales, garantiza que cada celebración sea única e inolvidable para todos los invitados.', 1, 'salones/salon_boda_palacio-300x200.jpg', 50000.00, 4.9, 'fiestas', 'Puebla'),
	(8, 'Cristal Real', 300, 'El Salón Cristal Real combina sofisticación y modernidad, ofreciendo un espacio ideal para celebraciones memorables como bodas, quinceañeras y eventos sociales. Su iluminación brillante y elegante resalta cada detalle de la decoración, mientras que su distribución amplia permite organizar cómodamente la pista de baile, mesas y áreas de entretenimiento. Perfecto para quienes buscan un ambiente elegante y festivo que deje una impresión duradera en sus invitados.', 1, 'salones/salon_cristal_real.jpg', 23000.00, 4.7, 'fiestas', 'CDMX'),
	(9, 'Flor de Mayo', 350, 'El Salón Flor de Mayo es un espacio amplio y elegante, diseñado para celebraciones vibrantes y memorables como bodas, quinceañeras y eventos sociales. Su ambiente cálido y acogedor, junto con una iluminación cuidadosamente pensada, realza la decoración y crea un entorno festivo. La distribución versátil permite organizar cómodamente la pista de baile, mesas y zonas de entretenimiento, garantizando una experiencia inolvidable para todos los invitados.', 1, 'salones/salon_flor_mayo.jpg', 33000.00, 4.6, 'fiestas', 'Monterrey'),
	(10, 'Salón Chapultepec', 100, 'El Salón Chapultepec es un espacio funcional y acogedor, ideal para reuniones corporativas, talleres y juntas ejecutivas. Su ambiente tranquilo y bien iluminado favorece la concentración y la comunicación efectiva. Con un diseño versátil, permite organizar cómodamente mesas de trabajo, presentaciones y sesiones interactivas, ofreciendo todas las facilidades necesarias para el éxito de cualquier encuentro profesional.', 1, 'salones/salonChapultepec.jpg', 15000.00, 4.5, 'reuniones', 'CDMX'),
	(11, 'Salón Torre Latino', 60, 'El Salón Torre Latino es un espacio íntimo y profesional, perfecto para reuniones pequeñas, juntas ejecutivas y talleres especializados. Su ambiente moderno y bien iluminado facilita la concentración y la colaboración entre los participantes. Con una distribución flexible, permite acomodar cómodamente mesas de trabajo, presentaciones o sesiones interactivas, garantizando un entorno eficiente y agradable para cualquier encuentro corporativo.', 1, 'salones/salonTorreLatino.png', 11000.00, 4.3, 'reuniones', 'CDMX'),
	(12, 'Salón Alameda', 130, 'El Salón Alameda es un espacio moderno y versátil, ideal para reuniones corporativas, conferencias y talleres. Su ambiente luminoso y tranquilo favorece la concentración y la interacción entre los participantes. Con una distribución adaptable, permite organizar cómodamente mesas de trabajo, presentaciones o sesiones colaborativas, asegurando que cada encuentro profesional se desarrolle de manera eficiente y cómoda.', 1, 'salones/salonalameda.png', 13000.00, 4.4, 'reuniones', 'Puebla'),
	(13, 'Salón Insurgentes', 30, 'El Salón Insurgentes es un espacio acogedor y funcional, ideal para reuniones pequeñas, juntas ejecutivas o talleres especializados. Su ambiente tranquilo y bien iluminado permite una comunicación fluida y concentración total. Con un diseño versátil, ofrece la posibilidad de organizar mesas de trabajo, presentaciones o sesiones interactivas de manera cómoda y eficiente, asegurando un entorno profesional y agradable para todos los asistentes.', 1, 'salones/salonInsurgentes.png', 17000.00, 4.8, 'reuniones', 'Quintana Roo'),
	(14, 'Salón Ciudadela', 100, 'El Salón Ciudadela es un espacio moderno y funcional, perfecto para reuniones corporativas, conferencias y talleres. Su ambiente bien iluminado y tranquilo favorece la concentración y la interacción entre los asistentes. Con una distribución flexible, permite organizar cómodamente mesas de trabajo, presentaciones o sesiones colaborativas, garantizando un entorno profesional y eficiente para todo tipo de encuentros de negocio.', 1, 'salones/salonCiudadela.jpeg', 12000.00, 4.4, 'reuniones', 'CDMX'),
	(15, 'Salón Coyoacán', 220, 'El Salón Coyoacán es un amplio y versátil espacio diseñado para reuniones corporativas, conferencias y seminarios de gran tamaño. Su ambiente moderno y bien iluminado facilita la concentración y la comunicación efectiva entre los participantes. La disposición flexible del mobiliario permite organizar cómodamente presentaciones, mesas de trabajo y sesiones interactivas, asegurando un entorno profesional y eficiente para eventos empresariales de cualquier magnitud.', 1, 'salones/salonCoyoacan.jpg', 16000.00, 4.8, 'reuniones', 'CDMX'),
	(16, 'Salón Santa Fe', 20, 'El Salón Santa Fe es un espacio íntimo y acogedor, ideal para reuniones pequeñas, juntas ejecutivas o sesiones de trabajo concentradas. Su ambiente tranquilo y bien iluminado facilita la comunicación efectiva y la colaboración entre los participantes. Con un diseño versátil, permite acomodar cómodamente mesas de trabajo o presentaciones, ofreciendo un entorno profesional y cómodo para encuentros corporativos reducidos.', 1, 'salones/salonSantafe.jpeg', 10000.00, 4.9, 'reuniones', 'CDMX'),
	(17, 'Salón San Ángel', 100, 'El Salón San Ángel es un espacio elegante y funcional, ideal para reuniones corporativas, talleres y conferencias. Su ambiente tranquilo y bien iluminado favorece la concentración y la interacción efectiva entre los participantes. Con una distribución versátil, permite organizar cómodamente mesas de trabajo, presentaciones y sesiones interactivas, garantizando un entorno profesional y eficiente para cualquier evento empresarial.', 1, 'salones/salonSanAngel.jpeg', 20000.00, 4.3, 'reuniones', 'Campeche'),
	(18, 'Salón Zócalo', 100, 'El Salón Zócalo es un espacio moderno y versátil, ideal para reuniones corporativas, talleres y conferencias. Su ambiente bien iluminado y tranquilo favorece la concentración y la comunicación entre los asistentes. Con una distribución flexible, permite organizar cómodamente mesas de trabajo, presentaciones y sesiones colaborativas, asegurando un entorno profesional y eficiente para cualquier encuentro empresarial.', 1, 'salones/salonZocalo.jpeg', 22000.00, 4.3, 'reuniones', 'Baja California Sur'),
	(19, 'Salón Áurea', 150, 'El Salón Áurea es un espacio moderno y versátil, perfecto para exposiciones, ferias y presentaciones de mediana escala. Su diseño abierto y bien iluminado permite exhibir productos, obras o stands de manera organizada y atractiva. Equipado con facilidades tecnológicas y buena accesibilidad, garantiza que tanto expositores como visitantes disfruten de un evento cómodo y profesional, ideal para mostrar proyectos con estilo y eficiencia.', 1, 'salones/salonAurea.jpeg', 23000.00, 4.9, 'expos', 'Guadalajara'),
	(20, 'Salón Estelar', 200, 'El Salón Estelar es un espacio amplio y moderno, diseñado para exposiciones, ferias y eventos de mediano a gran tamaño. Su estructura abierta y bien iluminada permite organizar stands, exhibiciones o presentaciones de manera atractiva y funcional. Con facilidades tecnológicas y una distribución versátil, garantiza comodidad y fluidez tanto para expositores como para visitantes, asegurando una experiencia profesional y eficiente en cada evento.', 1, 'salones/salonEstelar_tOK2Cf1.jpeg', 18000.00, 4.3, 'expos', 'Chihuahua'),
	(21, 'Salón Horizonte', 200, 'El Salón Horizonte es un espacio amplio y versátil, ideal para exposiciones, ferias y presentaciones de mediana escala. Su diseño moderno y bien iluminado permite exhibir productos, obras o stands de manera organizada y atractiva. Equipado con facilidades tecnológicas y con buena accesibilidad, proporciona un entorno cómodo y profesional, asegurando que tanto expositores como visitantes disfruten de un evento eficiente y exitoso.', 1, 'salones/salonHorizonte.jpeg', 20000.00, 4.5, 'expos', 'CDMX'),
	(22, 'Salón Galería Central', 10000, 'El Salón Galería Central es un espacio imponente y versátil, diseñado para exposiciones, ferias y eventos de gran escala. Su amplia estructura abierta y su iluminación estratégica permiten organizar stands, exhibiciones y presentaciones de manera funcional y atractiva. Equipado con tecnología avanzada y fácil acceso, garantiza comodidad y fluidez para expositores y visitantes, ofreciendo un entorno profesional ideal para grandes eventos y experiencias memorables.', 1, 'salones/salonGaleriaCentral.jpeg', 30000.00, 4.9, 'expos', 'Guadalajara'),
	(23, 'Salón Óptima', 200, 'El Salón Óptima es un espacio moderno y funcional, ideal para exposiciones, ferias y presentaciones de mediana escala. Su diseño abierto y bien iluminado permite exhibir productos, obras o stands de manera organizada y atractiva. Con facilidades tecnológicas y una distribución versátil, asegura comodidad y eficiencia para expositores y visitantes, ofreciendo un entorno profesional para eventos exitosos y memorables.', 1, 'salones/salonOptima.jpeg', 17000.00, 4.3, 'expos', 'CDMX'),
	(24, 'Salón Prisma', 200, 'El Salón Prisma es un espacio amplio y moderno, ideal para exposiciones, ferias y presentaciones de mediana escala. Su iluminación cuidadosamente diseñada y su distribución abierta permiten exhibir productos, obras o stands de manera atractiva y funcional. Equipado con facilidades tecnológicas y fácil accesibilidad, garantiza comodidad y eficiencia tanto para expositores como para visitantes, creando un entorno profesional para eventos exitosos y memorables.', 1, 'salones/salonPrisma.jpeg', 19000.00, 4.5, 'expos', 'Quintana Roo'),
	(25, 'Salón Nexus', 500, 'El Salón Nexus es un espacio amplio y moderno, diseñado para exposiciones, ferias y eventos de gran escala. Su estructura abierta y bien iluminada permite organizar stands, exhibiciones y presentaciones de manera funcional y atractiva. Equipado con tecnología avanzada y con excelente accesibilidad, garantiza comodidad y fluidez para expositores y visitantes, proporcionando un entorno profesional ideal para grandes eventos y experiencias memorables.', 1, 'salones/salonNexus.jpeg', 29999.00, 4.6, 'expos', 'CDMX'),
	(26, 'Salón Innovación', 300, 'El Salón Innovación es un espacio moderno y versátil, ideal para exposiciones, ferias y presentaciones de mediana a gran escala. Su diseño abierto y bien iluminado permite organizar stands, exhibiciones y demostraciones de manera atractiva y funcional. Con facilidades tecnológicas y fácil accesibilidad, garantiza comodidad y eficiencia para expositores y visitantes, asegurando un entorno profesional que potencia el éxito de cada evento.', 1, 'salones/salonInovacion.jpeg', 31000.00, 4.5, 'expos', 'Puebla'),
	(27, 'Salón Vértice', 330, 'El Salón Vértice es un espacio amplio y moderno, perfecto para exposiciones, ferias y presentaciones de mediana a gran escala. Su iluminación estratégica y diseño abierto permiten organizar stands, exhibiciones y demostraciones de manera ordenada y atractiva. Equipado con facilidades tecnológicas y buena accesibilidad, ofrece comodidad y eficiencia tanto para expositores como para visitantes, creando un entorno profesional ideal para eventos exitosos y memorables.', 1, 'salones/SalonVertice.jpeg', 15000.00, 4.5, 'expos', 'CDMX'),
	(28, 'Salón Cúpula', 1000, 'El Salón Cúpula es un espacio imponente y versátil, diseñado para exposiciones, ferias y eventos de gran magnitud. Su estructura amplia y bien iluminada permite organizar stands, exhibiciones y presentaciones de manera funcional y atractiva. Equipado con tecnología avanzada y fácil acceso, garantiza comodidad y fluidez para expositores y visitantes, ofreciendo un entorno profesional ideal para grandes eventos y experiencias memorables.', 1, 'salones/salonCupula.jpeg', 40000.00, 4.4, 'expos', 'CDMX'),
	(29, 'Salón Encanto', 300, 'El Salón Encanto es un espacio elegante y acogedor, perfecto para celebraciones memorables como bodas, quinceañeras y eventos sociales. Su iluminación cálida y su decoración sofisticada crean un ambiente festivo y armonioso. Con áreas amplias para pista de baile, montaje de mesas y zonas de entretenimiento, garantiza una experiencia cómoda y encantadora para todos los invitados, haciendo de cada celebración un evento inolvidable.', 1, 'salones/salonEncanto_sXTf8cp.jpeg', 32000.00, 4.9, 'fiestas', 'Guadalajara'),
	(30, 'Aurora Dorada', 500, 'El Salón Aurora Dorada es un espacio majestuoso y elegante, ideal para grandes celebraciones como bodas, quinceañeras y eventos sociales destacados. Su iluminación sofisticada y su decoración refinada crean un ambiente deslumbrante que realza cada detalle de la ocasión. Con amplias áreas para pista de baile, montaje de mesas y actividades especiales, ofrece comodidad y versatilidad, asegurando que cada evento sea espectacular e inolvidable para todos los invitados.', 1, 'salones/salonAuroraDorada_MQ8PZg5.jpeg', 40000.00, 4.5, 'fiestas', 'Queretaro'),
	(31, 'Espejos de Plata', 300, 'El Salón Espejos de Plata ofrece un ambiente elegante y sofisticado, ideal para celebraciones como bodas, quinceañeras y eventos sociales. Sus detalles reflectantes y su iluminación cuidadosamente diseñada crean un espacio brillante y acogedor. Con áreas amplias para pista de baile, montaje de mesas y zonas de entretenimiento, garantiza una experiencia memorable y confortable para todos los invitados, convirtiendo cada celebración en un evento especial e inolvidable .', 1, 'salones/salonEspejosDePlata.jpeg', 50000.00, 4.5, 'fiestas', 'Nuevo León');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
