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
CREATE DATABASE IF NOT EXISTS `reservacionesdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `reservacionesdb`;

-- Dumping structure for table reservacionesdb.auth_group
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table reservacionesdb.auth_group: ~0 rows (approximately)

-- Dumping structure for table reservacionesdb.auth_group_permissions
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

-- Dumping structure for table reservacionesdb.auth_permission
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table reservacionesdb.auth_permission: ~44 rows (approximately)
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
	(36, 'Can view favorito', 9, 'view_favorito'),
	(37, 'Can add servicio extra', 10, 'add_servicioextra'),
	(38, 'Can change servicio extra', 10, 'change_servicioextra'),
	(39, 'Can delete servicio extra', 10, 'delete_servicioextra'),
	(40, 'Can view servicio extra', 10, 'view_servicioextra'),
	(41, 'Can add profile', 11, 'add_profile'),
	(42, 'Can change profile', 11, 'change_profile'),
	(43, 'Can delete profile', 11, 'delete_profile'),
	(44, 'Can view profile', 11, 'view_profile');

-- Dumping structure for table reservacionesdb.auth_user
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
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table reservacionesdb.auth_user: ~2 rows (approximately)
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
	(12, 'pbkdf2_sha256$1000000$dSOJv6bDKdKxlND6CVXMqi$eol5saplhYZVlYfQOtYwZpmW5g+K0tzyUvH4jz6M5b0=', '2025-11-24 19:53:53.821642', 1, 'Nucalized', '', '', 'nucalized@gmail.com', 1, 1, '2025-11-03 08:15:50.948252'),
	(13, 'pbkdf2_sha256$1000000$Sw6VZQWoUAgNjPTCkh5mhc$T3zh40DgIBvR2IkJnRDQHGw1cUFqKobjuNH+KJzBZD0=', '2025-11-24 19:50:40.390386', 0, 'Marcela', '', '', 'marcela@gmail.com', 0, 1, '2025-11-22 05:47:16.544977');

-- Dumping structure for table reservacionesdb.auth_user_groups
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

-- Dumping structure for table reservacionesdb.auth_user_user_permissions
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

-- Dumping structure for table reservacionesdb.django_admin_log
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
INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
	(184, '2025-11-03 08:17:32.830094', '31', 'Espejos de Plata', 2, '[{"changed": {"fields": ["Descripcion"]}}]', 7, 12);

-- Dumping structure for table reservacionesdb.django_content_type
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table reservacionesdb.django_content_type: ~11 rows (approximately)
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(1, 'admin', 'logentry'),
	(2, 'auth', 'permission'),
	(3, 'auth', 'group'),
	(4, 'auth', 'user'),
	(5, 'contenttypes', 'contenttype'),
	(6, 'sessions', 'session'),
	(7, 'myapp', 'salon'),
	(8, 'myapp', 'reservacion'),
	(9, 'myapp', 'favorito'),
	(10, 'myapp', 'servicioextra'),
	(11, 'myapp', 'profile');

-- Dumping structure for table reservacionesdb.django_migrations
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table reservacionesdb.django_migrations: ~34 rows (approximately)
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
	(30, 'myapp', '0012_favorito', '2025-08-12 06:40:39.373236'),
	(31, 'myapp', '0002_alter_servicioextra_precio', '2025-11-17 21:58:52.444872'),
	(32, 'myapp', '0002_salon_created_at', '2025-11-18 04:27:57.673345'),
	(33, 'myapp', '0003_servicioextra_imagen', '2025-11-19 23:18:05.063274'),
	(34, 'myapp', '0004_profile', '2025-11-22 23:05:37.146138');

-- Dumping structure for table reservacionesdb.django_session
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table reservacionesdb.django_session: ~25 rows (approximately)
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('2cafz45tk5lhe3f1qi5dq9oewyxm3jf1', '.eJxVjDsOwyAQBe9CHSG-BlKm9xkQLLvBSYQlY1dR7h5bcpG0b2bem8W0rTVuHZc4FXZlUrHL75gTPLEdpDxSu88c5rYuU-aHwk_a-TgXfN1O9--gpl732hjUg0cVlLUETiQMAmTx5MllgUpRkVlpQ9K5YMOOhNFBJg0DEIjMPl_9tjgE:1vLR9a:yXmGMh63fnldb5syBECRrbaCDe2J9zN7RvWPKUoGYsQ', '2025-12-02 19:14:14.539124'),
	('2jpclhh8w7xvq6iut92yuo9hyjewydyk', '.eJxVjkEOgjAQRe_SNZJ22gJl6d4TGEOm7VRQBEPBmBjvbjEsdDvv__fnxRpc5rZZIk1N51nNBLDs92jRXWlYib_gcB5zNw7z1Nl8jeQbjflh9NTvt-yfoMXYprZSJIuKwIDWwZUcyXAnfBWqUFpOAMELC1IFUZZGm4S4kkagdIULjtsknSj5HtjMdLuz-sUi9uPw_VpnLJBrMe0AB70TYgcyNeg5TxhZfRTq9H5_AN-0S9w:1vNGSO:zPGhe4nA8iMYXQ98fh2WPKKYQMKKCeqflcQj7QJMxtI', '2025-12-07 20:13:12.236401'),
	('2wi855ys9f6jfpa05mj060u9h451u3q4', '.eJxVjDsOwyAQBe9CHSG-BlKm9xkQLLvBSYQlY1dR7h5bcpG0b2bem8W0rTVuHZc4FXZlUrHL75gTPLEdpDxSu88c5rYuU-aHwk_a-TgXfN1O9--gpl732hjUg0cVlLUETiQMAmTx5MllgUpRkVlpQ9K5YMOOhNFBJg0DEIjMPl_9tjgE:1vNcdF:FuOsju3ygOM0PYgwh3igg4PeSBG71Iu4oAl6ip743SQ', '2025-12-08 19:53:53.870637'),
	('3m2407f89qhi60yxi9v0ued6g1ta5sjz', '.eJxVjDsOwyAQBe9CHSG-BlKm9xkQLLvBSYQlY1dR7h5bcpG0b2bem8W0rTVuHZc4FXZlUrHL75gTPLEdpDxSu88c5rYuU-aHwk_a-TgXfN1O9--gpl732hjUg0cVlLUETiQMAmTx5MllgUpRkVlpQ9K5YMOOhNFBJg0DEIjMPl_9tjgE:1vLFA2:sBj9ZA4csNNxB0znFdJ-3ix1DsuoQusOBacbctguIWM', '2025-12-02 06:25:54.336129'),
	('6yfervzq8vxeb0iwcbv131x12fup62sp', 'e30:1vMwg0:fvJHUcLZxMlJIBvh603p1lcm9jhwW9RDrLodJngXUxs', '2025-12-06 23:05:56.801157'),
	('9gmi0v8n7po76up23klvoqf3c0mg25vm', '.eJxVjDsOwyAQRO9CHSG-Npsyvc-AFhaCkwgkY1dR7h5bcpE0U8x7M2_mcVuL33pa_EzsyiS7_HYB4zPVA9AD673x2Oq6zIEfCj9p51Oj9Lqd7t9BwV72NWSnKGchHSRwStvBCKWjgSilypacRhMpjwZSMGoEm_aUJCwR0hA0-3wBy-E3hA:1vEhxU:kbZT46ukESPAASr37PBeH85LVhxdPf3-kKocey9Gvyg', '2025-11-14 05:45:56.070023'),
	('c4yq0cenwuxdimz1i30zgdhyqohdrxuv', '.eJxVjDsOwyAQBe9CHSG-BlKm9xkQLLvBSYQlY1dR7h5bcpG0b2bem8W0rTVuHZc4FXZlUrHL75gTPLEdpDxSu88c5rYuU-aHwk_a-TgXfN1O9--gpl732hjUg0cVlLUETiQMAmTx5MllgUpRkVlpQ9K5YMOOhNFBJg0DEIjMPl_9tjgE:1vFpjK:Q4sdsmu3BptlmyUy61Qqw9Tf5Gh7Ms9tDlQY5G7dupk', '2025-11-17 08:15:58.192444'),
	('c52ficisjogqx8n28kwe04qrhr5z16e7', '.eJxVjM1uwyAQBt-Fc4Qwf4Uee88zoDW72KQuRAafqr57sRpF6R535ptvFuDoazga7SEje2eKXV5_M8RPKifAG5Sl8lhL3_PMT4U_aOPXirR9PNx_gRXaOtZeGRWlVRq1o-TJu6QiKiu0FMkizgbdm_SKnPBGamcFKDNTkomUxUmOaK8dtpBygW0EJ22c4GLcQEgtHlR6DXDfcgSsp2HlU4gV81JDLstO7Q_fa1ngiybBfn4BaH5TmA:1um4Oq:PsuFNBepgtQHhqJQFcwzRG32rKHpUXWd9Aedev7PFoA', '2025-08-27 05:51:48.823098'),
	('c7io88nm91fp8zeq07yq79zawy3iatli', '.eJxVjDEOAiEQRe9CbQjOAIKlvWcgwAyyaiBZdivj3XWTLbT9773_EiGuSw3r4DlMJM4CxeF3SzE_uG2A7rHdusy9LfOU5KbInQ557cTPy-7-HdQ46rf2aDCDRU3acfHsXcFMaJUGVSxRMuRO4JGd8ga0syqiSVygMFo6gnh_AM3KN1w:1umfhr:Zq3VbRwmRJqgQ6-MGQLIWd3N7kQO658i_m8y4NSJ6Wo', '2025-08-28 21:41:55.801304'),
	('f45r7e93ec0h7dgespopm9vvz5sv62wy', '.eJxVjDsOwyAQBe9CHSG-BlKm9xkQLLvBSYQlY1dR7h5bcpG0b2bem8W0rTVuHZc4FXZlUrHL75gTPLEdpDxSu88c5rYuU-aHwk_a-TgXfN1O9--gpl732hjUg0cVlLUETiQMAmTx5MllgUpRkVlpQ9K5YMOOhNFBJg0DEIjMPl_9tjgE:1vL7PQ:0JvBMqKM_jITPixLHtLtQNbwVJELrsxJ3SeIGg22w0g', '2025-12-01 22:09:16.332434'),
	('fq22zzxx3obw2b1lma7ptumo5yo2x4j5', '.eJxVjDsOwyAQBe9CHSG-BlKm9xkQLLvBSYQlY1dR7h5bcpG0b2bem8W0rTVuHZc4FXZlUrHL75gTPLEdpDxSu88c5rYuU-aHwk_a-TgXfN1O9--gpl732hjUg0cVlLUETiQMAmTx5MllgUpRkVlpQ9K5YMOOhNFBJg0DEIjMPl_9tjgE:1vNRWI:zPzicfkLvJyFrfJuZNDJK0Nyp0BETkH8kjX7SDaTwF0', '2025-12-08 08:01:58.649146'),
	('hbaevfysc41pwt3rbg2cijkntsbm9s33', 'e30:1vMwXd:I__pwV4bGnDnJ6V7mu76OcoiT0NHkl8LClAttABlcF4', '2025-12-06 22:57:17.386750'),
	('ikldgl9pklrd6i3ujiwtny35s3m7ndsz', '.eJxVj8EOgjAMht9lZyRrtwnj6N0nMIZ0WycqgmFoTIzv7jAe9Nrv79f-T9HSbe7aW-KpPQbRCEBR_A4d-TMPCwknGg5j6cdhno6uXCLll6ZyOwbuN9_sn6Cj1OVtrVmta0aLxkRfSWIrPYQ61rFykhFjAIdKR6gqa2xGUisLpPzaRy9dlk6cfXdqZ75cRfMUifpx-HyNhYjsO8p3UKJZAaxw6cGPeaIkmh2oAnQBZv96vQGlm0z6:1vMhQX:m4GD8KJiZ3I7UbJ9qRMRlFGbuNOq5je9I3OY3J32o1E', '2025-12-06 06:48:57.241368'),
	('krrfp35ts46ixixqog18t08gu54hiy5l', 'e30:1vMwf9:t15Jl13P-aqAcjY8_uO9Kt1gcN9tl6a0HYvZwxfNibo', '2025-12-06 23:05:03.683684'),
	('l7txregq4m9bv7eo9n87gvieokes9j4c', '.eJxVjDsOwyAQBe9CHSHAfFOm9xnQsqyDkwgkY1dR7h4huUjaNzPvzSIce4lHpy2umV2ZYpffLQE-qQ6QH1DvjWOr-7YmPhR-0s7nlul1O92_gwK9jFq5BUCjBSe1Q48Blwm8UZMjsAaEs5mSEl5Pkih4A0Gg1SQdCgkys88X8hU3-w:1ulxog:cJL1GQYBXCg4mkVKU_U-LXBa8XDRJOUXaWbeYvsq8eo', '2025-08-26 22:50:02.649280'),
	('ntpfu1omgrey8p7fn55exbbms8aalek6', '.eJxVjDsOwyAQBe9CHSG-BlKm9xkQLLvBSYQlY1dR7h5bcpG0b2bem8W0rTVuHZc4FXZlUrHL75gTPLEdpDxSu88c5rYuU-aHwk_a-TgXfN1O9--gpl732hjUg0cVlLUETiQMAmTx5MllgUpRkVlpQ9K5YMOOhNFBJg0DEIjMPl_9tjgE:1vN4bX:o2_j-29LWeuv3EeWxxEwqS-yM7wQeKUQ5lN0aMVf0wc', '2025-12-07 07:33:51.808744'),
	('nxwl0pqxwrba23q6n0m7e8ssxokd54yy', 'e30:1vMwgC:pNrfDFsGRUU-g85uj2WBaKMn93RepjXADIfE0EJ6nww', '2025-12-06 23:06:08.211410'),
	('o1eumjjp1qhdwol6s74e45q6wcryiziu', '.eJxVjkEOgjAQRe_SNZJ2KJSydO8JjCHTdioogqFgTAh3txgWup33__uzsBrnqannQGPdOlYxASz5PRq0d-o34m7YX4fUDv00tibdIulOQ3oaHHXHPfsnaDA0sS0lZUVJoCHPvVUcSXMrXOlLrwwnAO-EgUx6oZTOdURcZlpgZgvrLTdROlL0vbCe6PFk1cICdkP__VolzJNtMO4Ah_wgxAFkbNB7GjGw6lwm-rKuHyuPTBc:1vM0wS:U5639DXr2twyPM48wW89IswU_dJEkpyfKPyub4Q-sdc', '2025-12-04 09:27:04.632707'),
	('pdvl97mlj69cn4l05ew3ryvmkqbkxt8u', '.eJxVjssOgyAURP-FdUN4KeKy-34DucCl2gc0ot0Y_73YuGi3c2ZOZiUWlnmwS8HJjoH0hAty-g0d-DumnYQbpGumPqd5Gh3dK_SghV5ywMf56P4JBihDXSuFsu1QGNE00WsGaJjnoYtd1I6hEDFwJ6SKXGvTmIqYkoaD9K2PnrkqnbD63mBnfL5Iv5ICj5y-r-W2fQAxnUKt:1vMYI3:HhwqcX0DI5k8h51BaJmde9qF3qkinRjOZfX5-FuAcEc', '2025-12-05 21:03:35.044238'),
	('rmcwgd8suj6kb6j05pglzu3jz0yaqgap', '.eJxVjDsOwyAQBe9CHSG-BlKm9xkQLLvBSYQlY1dR7h5bcpG0b2bem8W0rTVuHZc4FXZlUrHL75gTPLEdpDxSu88c5rYuU-aHwk_a-TgXfN1O9--gpl732hjUg0cVlLUETiQMAmTx5MllgUpRkVlpQ9K5YMOOhNFBJg0DEIjMPl_9tjgE:1vMLuG:bgHJOEzZJJyHqa8DCV8HZoBEMg0SXX8swUvC2xpuKsw', '2025-12-05 07:50:12.738436'),
	('slhxe1z4b4a86msyjw8qx5zs973j98si', '.eJxVjDsOwyAQBe9CHSHAfFOm9xnQsqyDkwgkY1dR7h4huUjaNzPvzSIce4lHpy2umV2ZYpffLQE-qQ6QH1DvjWOr-7YmPhR-0s7nlul1O92_gwK9jFq5BUCjBSe1Q48Blwm8UZMjsAaEs5mSEl5Pkih4A0Gg1SQdCgkys88X8hU3-w:1ukuhU:dBzCAeA0Oz3PmcK5HRrcp1Z-kfhM1hrhtvD2i9pxkYY', '2025-08-24 01:18:16.770703'),
	('uix23skfibjmeatrwlibs591di8j4rlu', '.eJxVjssOgyAURP-FtSGAD8Rl9_2CpiEXuFT70AawaWL892Ljot3OmTmZhWiYU6_niEEPjnSEC1L8hgbsDceNuCuMl4naaUxhMHSr0J1Gepwc3g9790_QQ-zzuqqwbFoUStS1t5IBKma5a33rpWEohHfciLLyXEpVq4xYVSoOpW2st8xkacDse4FO-HiSbiER7tP4fS0Kgu8UIJLuJNh5XT_zo0cH:1vLcpN:-VEcskaEvJVmUafwfV-4jyIfRse2hy4smCJueoLa0-A', '2025-12-03 07:42:09.637475'),
	('xzangyhl5z7jaos38cp5legxwyusq2v5', '.eJxVjDEOAiEQRe9CbQjOAIKlvWcgwAyyaiBZdivj3XWTLbT9773_EiGuSw3r4DlMJM4CxeF3SzE_uG2A7rHdusy9LfOU5KbInQ557cTPy-7-HdQ46rf2aDCDRU3acfHsXcFMaJUGVSxRMuRO4JGd8ga0syqiSVygMFo6gnh_AM3KN1w:1ulyeX:fCVBHtb8wPgrlLQpsNa7HVm9IJ1s4jIR5rdy2FwG_X8', '2025-08-26 23:43:37.913697'),
	('z74wzxjumacoopqtauuymsifp47g2kf5', '.eJxVjDsOwyAQBe9CHSG-BlKm9xkQLLvBSYQlY1dR7h5bcpG0b2bem8W0rTVuHZc4FXZlUrHL75gTPLEdpDxSu88c5rYuU-aHwk_a-TgXfN1O9--gpl732hjUg0cVlLUETiQMAmTx5MllgUpRkVlpQ9K5YMOOhNFBJg0DEIjMPl_9tjgE:1vMwiG:M1UQsyHdJhAPUpKCtC58jFzAP7pGLdihB3VTxmGLKBc', '2025-12-06 23:08:16.819203'),
	('zj73oydb85bc5u15qogpehlvzt3kb6wa', '.eJxVjM0OwiAQhN-FsyG7dKXg0bvP0CywSNVA0p-T8d1tkx70NMl838xbDbwuZVhnmYYxqYtCVKffMnB8St1JenC9Nx1bXaYx6F3RB531rSV5XQ_376DwXLZ1x5wQGNkgidkyY0_BnzP01prOU8rEmMFHdA4EAJiw85aciSQS1ecL-N03ew:1vFgQE:nYurmq0IN8Y6q_8aTiCKxKy9IlHOuL4LrSazHz-X1l0', '2025-11-16 22:19:38.091734');

-- Dumping structure for table reservacionesdb.myapp_favorito
CREATE TABLE IF NOT EXISTS `myapp_favorito` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `salon_id` bigint(20) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `myapp_favorito_usuario_id_salon_id_45d7dd9d_uniq` (`usuario_id`,`salon_id`),
  KEY `myapp_favorito_salon_id_1b74d9d6_fk_myapp_salon_id` (`salon_id`),
  CONSTRAINT `myapp_favorito_salon_id_1b74d9d6_fk_myapp_salon_id` FOREIGN KEY (`salon_id`) REFERENCES `myapp_salon` (`id`),
  CONSTRAINT `myapp_favorito_usuario_id_e2c2e57d_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table reservacionesdb.myapp_favorito: ~4 rows (approximately)
INSERT INTO `myapp_favorito` (`id`, `salon_id`, `usuario_id`) VALUES
	(38, 3, 12),
	(39, 4, 12),
	(41, 6, 12),
	(42, 2, 12);

-- Dumping structure for table reservacionesdb.myapp_profile
CREATE TABLE IF NOT EXISTS `myapp_profile` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `avatar` varchar(100) NOT NULL,
  `full_name` varchar(150) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `address` longtext NOT NULL,
  `birth_date` date DEFAULT NULL,
  `gender` varchar(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `myapp_profile_user_id_9fe34268_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table reservacionesdb.myapp_profile: ~2 rows (approximately)
INSERT INTO `myapp_profile` (`id`, `avatar`, `full_name`, `phone`, `address`, `birth_date`, `gender`, `user_id`) VALUES
	(1, 'avatars/Screenshot_2025-11-23_002334.png', 'mike tyson', '424342343', 'fawefwefawefewfeawf', '2002-02-22', 'Otro', 12),
	(2, 'avatars/default.png', '', '', '', NULL, '', 13);

-- Dumping structure for table reservacionesdb.myapp_reservacion
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
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table reservacionesdb.myapp_reservacion: ~23 rows (approximately)
INSERT INTO `myapp_reservacion` (`id`, `estado`, `usuario_id`, `salon_id`, `fecha_reserva`, `pagada`, `precio_total`) VALUES
	(49, 'pendiente', 12, 11, '2025-11-12', 0, 11000.00),
	(50, 'pendiente', 12, 3, '2025-11-18', 0, 27000.00),
	(51, 'confirmada', 12, 4, '2025-11-22', 0, 28700.00),
	(52, 'confirmada', 12, 3, '2025-11-23', 0, 27500.00),
	(53, 'confirmada', 12, 4, '2025-11-23', 0, 36199.00),
	(54, 'confirmada', 12, 8, '2025-11-28', 0, 28200.00),
	(55, 'confirmada', 12, 3, '2025-11-28', 0, 27500.00),
	(56, 'confirmada', 12, 10, '2025-11-23', 0, 22059.00),
	(57, 'confirmada', 12, 10, '2025-11-24', 0, 15500.00),
	(58, 'confirmada', 12, 10, '2025-11-25', 0, 18700.00),
	(59, 'confirmada', 12, 10, '2025-11-27', 0, 20059.00),
	(60, 'confirmada', 12, 10, '2025-11-30', 0, 32159.00),
	(61, 'confirmada', 12, 11, '2025-11-28', 0, 18059.00),
	(62, 'confirmada', 12, 2, '2025-11-25', 0, 30800.00),
	(63, 'confirmada', 12, 9, '2025-11-29', 0, 49399.00),
	(64, 'confirmada', 12, 9, '2025-11-28', 0, 50999.00),
	(65, 'confirmada', 12, 3, '2025-11-24', 0, 32059.00),
	(66, 'confirmada', 12, 3, '2025-11-25', 0, 34059.00),
	(67, 'confirmada', 12, 3, '2025-11-29', 0, 44159.00),
	(68, 'confirmada', 12, 2, '2025-10-15', 1, 20000.00),
	(69, 'confirmada', 12, 6, '2025-11-28', 0, 92858.00),
	(70, 'confirmada', 12, 5, '2025-11-29', 0, 88658.00),
	(71, 'confirmada', 13, 2, '2025-11-29', 0, 27600.00);

-- Dumping structure for table reservacionesdb.myapp_reservacion_servicios_extra
CREATE TABLE IF NOT EXISTS `myapp_reservacion_servicios_extra` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `reservacion_id` bigint(20) NOT NULL,
  `servicioextra_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_reservacion_servicio` (`reservacion_id`,`servicioextra_id`),
  UNIQUE KEY `myapp_reservacion_servic_reservacion_id_servicioe_1b403761_uniq` (`reservacion_id`,`servicioextra_id`),
  CONSTRAINT `myapp_reservacion_se_reservacion_id_0e16cdf9_fk_myapp_res` FOREIGN KEY (`reservacion_id`) REFERENCES `myapp_reservacion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table reservacionesdb.myapp_reservacion_servicios_extra: ~59 rows (approximately)
INSERT INTO `myapp_reservacion_servicios_extra` (`id`, `reservacion_id`, `servicioextra_id`) VALUES
	(1, 52, 3),
	(2, 53, 10),
	(3, 54, 14),
	(4, 55, 3),
	(5, 56, 2),
	(6, 56, 3),
	(7, 56, 4),
	(8, 57, 3),
	(9, 58, 3),
	(10, 58, 5),
	(11, 59, 3),
	(12, 59, 4),
	(13, 60, 2),
	(14, 60, 3),
	(15, 60, 4),
	(16, 60, 5),
	(17, 60, 6),
	(18, 60, 7),
	(19, 60, 26),
	(20, 61, 2),
	(21, 61, 3),
	(22, 61, 4),
	(23, 62, 16),
	(24, 62, 14),
	(25, 62, 15),
	(26, 63, 17),
	(27, 63, 13),
	(28, 63, 14),
	(29, 64, 13),
	(30, 64, 14),
	(31, 64, 15),
	(32, 65, 3),
	(33, 65, 4),
	(34, 66, 2),
	(35, 66, 3),
	(36, 66, 4),
	(37, 67, 2),
	(38, 67, 3),
	(39, 67, 4),
	(40, 67, 5),
	(41, 67, 6),
	(42, 67, 7),
	(43, 67, 26),
	(44, 68, 2),
	(45, 69, 13),
	(46, 69, 14),
	(47, 69, 15),
	(48, 69, 16),
	(49, 69, 17),
	(50, 69, 18),
	(51, 69, 19),
	(52, 69, 20),
	(53, 70, 17),
	(54, 70, 18),
	(55, 70, 13),
	(56, 70, 15),
	(57, 71, 17),
	(58, 71, 19),
	(59, 71, 20);

-- Dumping structure for table reservacionesdb.myapp_salon
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
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table reservacionesdb.myapp_salon: ~30 rows (approximately)
INSERT INTO `myapp_salon` (`id`, `nombre`, `capacidad`, `descripcion`, `disponible`, `imagen`, `precio`, `calificacion`, `categoria`, `ciudad`, `created_at`) VALUES
	(2, 'Salon XV años', 300, 'El Salón XV Años es amplio y elegante, ideal para quinceañeras, con pista de baile, escenario, área de banquetes y decoración personalizable para una celebración inolvidable.', 0, 'salones/salon_xv.jpg', 20000.00, 4.7, 'fiestas', 'Queretaro', '2025-11-18 04:27:57.650741'),
	(3, 'Salón Torre Reforma', 70, 'El Salón Torre Reforma es moderno y elegante, ideal para reuniones corporativas y talleres, con iluminación adecuada, distribución versátil y tecnología para garantizar encuentros profesionales exitosos.', 0, 'salones/salon_reuniones1-300x200.jpg', 27000.00, 4.3, 'reuniones', 'CDMX', '2025-11-18 04:27:57.650741'),
	(4, 'Salon expo', 420, 'El Salón Expo es amplio y versátil, perfecto para ferias y exposiciones, con iluminación, tecnología y espacios organizados que facilitan la movilidad y comodidad de los asistentes.', 0, 'salones/salon_expo-300x200.jpg', 28700.00, 4.6, 'expos', 'CDMX', '2025-11-18 04:27:57.650741'),
	(5, 'Luz de Luna', 300, 'El Salón Luz de Luna ofrece un ambiente elegante y acogedor para bodas, quinceañeras y eventos, con espacios amplios, iluminación cálida y áreas para pista de baile y mesas.', 0, 'salones/salon_boda1-300x200.jpg', 40000.00, 4.8, 'fiestas', 'Queretaro', '2025-11-18 04:27:57.650741'),
	(6, 'Jardines del Sol', 250, 'El Salón Jardines del Sol combina elegancia y naturaleza, con espacios amplios y áreas verdes, ideal para bodas y eventos, incluyendo pista de baile, mesas y zonas de entretenimiento.', 0, 'salones/salon_jardin-300x200.jpg', 31000.00, 4.8, 'fiestas', 'CDMX', '2025-11-18 04:27:57.650741'),
	(7, 'Palacio Esmeralda', 300, 'El Salón Palacio Esmeralda es sofisticado y elegante, ideal para bodas y eventos, con iluminación cuidada y amplias áreas para pista de baile, mesas y actividades especiales.', 0, 'salones/salon_boda_palacio-300x200.jpg', 50000.00, 4.9, 'fiestas', 'Puebla', '2025-11-18 04:27:57.650741'),
	(8, 'Cristal Real', 300, 'El Salón Cristal Real combina modernidad y elegancia, ideal para bodas y eventos, con iluminación destacada y amplias áreas para pista de baile, mesas y entretenimiento.', 0, 'salones/salon_cristal_real.jpg', 23000.00, 4.7, 'fiestas', 'CDMX', '2025-11-18 04:27:57.650741'),
	(9, 'Flor de Mayo', 350, 'El Salón Flor de Mayo es amplio y elegante, ideal para bodas y eventos, con iluminación cálida y áreas cómodas para pista de baile, mesas y entretenimiento.', 0, 'salones/salon_flor_mayo.jpg', 33000.00, 4.6, 'fiestas', 'Nuevo León', '2025-11-18 04:27:57.650741'),
	(10, 'Salón Chapultepec', 100, 'El Salón Chapultepec es funcional y acogedor, ideal para reuniones y talleres, con iluminación adecuada y espacios versátiles para mesas, presentaciones y sesiones interactivas.', 0, 'salones/salonChapultepec.jpg', 15000.00, 4.5, 'reuniones', 'CDMX', '2025-11-18 04:27:57.650741'),
	(11, 'Salón Torre Latino', 60, 'El Salón Torre Latino es íntimo y profesional, ideal para reuniones y talleres, con ambiente moderno, buena iluminación y distribución flexible para mesas, presentaciones y sesiones interactivas.', 0, 'salones/salonTorreLatino.png', 11000.00, 4.3, 'reuniones', 'CDMX', '2025-11-18 04:27:57.650741'),
	(12, 'Salón Alameda', 130, 'El Salón Alameda es moderno y versátil, ideal para reuniones, conferencias y talleres, con buena iluminación y distribución adaptable que facilita mesas, presentaciones y sesiones colaborativas.', 0, 'salones/salonalameda.png', 13000.00, 4.4, 'reuniones', 'Puebla', '2025-11-18 04:27:57.650741'),
	(13, 'Salón Insurgentes', 30, 'El Salón Insurgentes es acogedor y funcional, ideal para reuniones y talleres, con buena iluminación y distribución versátil que facilita mesas, presentaciones y sesiones interactivas.', 0, 'salones/salonInsurgentes.png', 17000.00, 4.8, 'reuniones', 'Baja California Sur', '2025-11-18 04:27:57.650741'),
	(14, 'Salón Ciudadela', 100, 'El Salón Ciudadela es moderno y funcional, ideal para reuniones y talleres, con buena iluminación y distribución flexible que facilita mesas, presentaciones y sesiones colaborativas.', 0, 'salones/salonCiudadela.jpeg', 12000.00, 4.4, 'reuniones', 'CDMX', '2025-11-18 04:27:57.650741'),
	(15, 'Salón Coyoacán', 220, 'El Salón Coyoacán es amplio y versátil, ideal para reuniones, conferencias y seminarios, con buena iluminación y disposición flexible que facilita presentaciones y sesiones interactivas.', 0, 'salones/salonCoyoacan.jpg', 16000.00, 4.8, 'reuniones', 'CDMX', '2025-11-18 04:27:57.650741'),
	(16, 'Salón Santa Fe', 20, 'El Salón Santa Fe es íntimo y acogedor, perfecto para reuniones pequeñas o ejecutivas, con buena iluminación y distribución flexible que facilita trabajo y presentaciones efectivas.', 0, 'salones/salonSantafe.jpeg', 10000.00, 4.9, 'reuniones', 'CDMX', '2025-11-18 04:27:57.650741'),
	(17, 'Salón San Ángel', 100, 'El Salón San Ángel es elegante y funcional, ideal para reuniones, talleres o conferencias, con buena iluminación y distribución versátil que facilita concentración y colaboración efectiva.', 0, 'salones/salonSanAngel.jpeg', 20000.00, 3.5, 'reuniones', 'Nuevo León', '2025-11-18 04:27:57.650741'),
	(18, 'Salón Zócalo', 100, 'El Salón Zócalo es moderno y versátil, ideal para reuniones, talleres y conferencias, con buena iluminación y distribución flexible que facilita concentración y colaboración profesional.', 0, 'salones/salonZocalo.jpeg', 22000.00, 4.3, 'reuniones', 'Baja California Sur', '2025-11-18 04:27:57.650741'),
	(19, 'Salón Áurea', 150, 'El Salón Áurea es moderno y versátil, ideal para exposiciones y ferias, con diseño iluminado y abierto que facilita exhibiciones organizadas y experiencias cómodas y profesionales.', 0, 'salones/salonAurea.jpeg', 23000.00, 4.9, 'expos', 'Guadalajara', '2025-11-18 04:27:57.650741'),
	(20, 'Salón Estelar', 200, 'El Salón Estelar es amplio y moderno, ideal para exposiciones y ferias, con diseño abierto, buena iluminación y tecnología que garantiza eventos cómodos, funcionales y profesionales.', 0, 'salones/salonEstelar_tOK2Cf1.jpeg', 18000.00, 4.3, 'expos', 'Nuevo León', '2025-11-18 04:27:57.650741'),
	(21, 'Salón Horizonte', 200, 'El Salón Horizonte es amplio y moderno, ideal para exposiciones y ferias, con buena iluminación, tecnología y accesibilidad, garantizando un evento cómodo, eficiente y profesional para todos.', 0, 'salones/salonHorizonte.jpeg', 20000.00, 4.5, 'expos', 'CDMX', '2025-11-18 04:27:57.650741'),
	(22, 'Salón Galería Central', 10000, 'El Salón Galería Central es amplio y versátil, ideal para exposiciones y ferias, con buena iluminación, tecnología avanzada y accesibilidad, asegurando comodidad y un entorno profesional para grandes eventos.', 0, 'salones/salonGaleriaCentral.jpeg', 30000.00, 4.9, 'expos', 'Guadalajara', '2025-11-18 04:27:57.650741'),
	(23, 'Salón Óptima', 200, 'El Salón Óptima es moderno y funcional, ideal para exposiciones y ferias, con buena iluminación, tecnología y distribución versátil, ofreciendo comodidad y un entorno profesional para eventos exitosos.', 0, 'salones/salonOptima.jpeg', 17000.00, 4.3, 'expos', 'CDMX', '2025-11-18 04:27:57.650741'),
	(24, 'Salón Prisma', 200, 'El Salón Prisma es amplio y moderno, perfecto para exposiciones y ferias, con buena iluminación, tecnología y distribución abierta, ofreciendo comodidad y un entorno profesional para eventos exitosos.', 0, 'salones/salonPrisma.jpeg', 19000.00, 4.5, 'expos', 'Baja California Sur', '2025-11-18 04:27:57.650741'),
	(25, 'Salón Nexus', 500, 'El Salón Nexus es amplio y moderno, ideal para exposiciones y ferias, con buena iluminación, tecnología avanzada y accesibilidad, ofreciendo comodidad y un entorno profesional para grandes eventos.', 0, 'salones/salonNexus.jpeg', 29999.00, 4.6, 'expos', 'CDMX', '2025-11-18 04:27:57.650741'),
	(26, 'Salón Innovación', 300, 'El Salón Innovación es moderno y versátil, ideal para exposiciones y ferias, con buena iluminación, tecnología accesible y cómoda, ofreciendo un entorno profesional y eficiente para cada evento.', 0, 'salones/salonInovacion.jpeg', 31000.00, 4.5, 'expos', 'Puebla', '2025-11-18 04:27:57.650741'),
	(27, 'Salón Vértice', 330, 'El Salón Vértice es moderno y amplio, ideal para exposiciones y ferias, con buena iluminación, tecnología y espacios organizados que ofrecen comodidad y eficiencia para todos los participantes.', 0, 'salones/SalonVertice.jpeg', 15000.00, 4.5, 'expos', 'CDMX', '2025-11-18 04:27:57.650741'),
	(28, 'Salón Cúpula', 1000, 'El Salón Cúpula es amplio y versátil, ideal para exposiciones y ferias, con buena iluminación, tecnología avanzada y espacios funcionales que aseguran comodidad y fluidez.', 0, 'salones/salonCupula.jpeg', 40000.00, 4.4, 'expos', 'CDMX', '2025-11-18 04:27:57.650741'),
	(29, 'Salón Encanto', 300, 'El Salón Encanto es elegante y acogedor, ideal para bodas y eventos sociales, con áreas para baile, mesas y entretenimiento, garantizando una celebración cómoda y memorable.', 0, 'salones/salonEncanto_sXTf8cp.jpeg', 32000.00, 4.9, 'fiestas', 'Guadalajara', '2025-11-18 04:27:57.650741'),
	(30, 'Aurora Dorada', 500, 'El Salón Aurora Dorada es elegante y majestuoso, ideal para bodas y grandes celebraciones, con amplias áreas para baile, mesas y actividades, garantizando comodidad y un evento inolvidable.', 0, 'salones/salonAuroraDorada_MQ8PZg5.jpeg', 40000.00, 4.5, 'fiestas', 'Queretaro', '2025-11-18 04:27:57.650741'),
	(31, 'Espejos de Plata', 300, 'El Salón Espejos de Plata ofrece un ambiente elegante y brillante, ideal para bodas y eventos sociales, con amplias áreas para baile, mesas y entretenimiento.', 0, 'salones/salonEspejosDePlata.jpeg', 50000.00, 4.5, 'fiestas', 'Nuevo León', '2025-11-18 04:27:57.650741');

-- Dumping structure for table reservacionesdb.myapp_salon_servicios_extras
CREATE TABLE IF NOT EXISTS `myapp_salon_servicios_extras` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `salon_id` bigint(20) NOT NULL,
  `servicioextra_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `myapp_salon_servicios_ex_salon_id_servicioextra_i_7ff53323_uniq` (`salon_id`,`servicioextra_id`),
  CONSTRAINT `myapp_salon_servicios_extras_salon_id_553a6b7b_fk_myapp_salon_id` FOREIGN KEY (`salon_id`) REFERENCES `myapp_salon` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table reservacionesdb.myapp_salon_servicios_extras: ~0 rows (approximately)

-- Dumping structure for table reservacionesdb.myapp_servicioextra
CREATE TABLE IF NOT EXISTS `myapp_servicioextra` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `tipo_salon` varchar(20) NOT NULL,
  `imagen` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table reservacionesdb.myapp_servicioextra: ~20 rows (approximately)
INSERT INTO `myapp_servicioextra` (`id`, `nombre`, `precio`, `tipo_salon`, `imagen`) VALUES
	(2, 'Proyector y pantalla', 2000.00, 'reuniones', 'servicios/proyector_y_pantalla_DUDEUF6.png'),
	(3, 'Micrófonos', 500.00, 'reuniones', 'servicios/microfonos_XeSKaNt.png'),
	(4, 'Mesas adicionales', 4559.00, 'reuniones', 'servicios/mesas_adicionales_Dyfb5Lp.png'),
	(5, 'Café y snacks', 3200.00, 'reuniones', 'servicios/cafe_y_snacks_zao8Usr.png'),
	(6, 'Servicio de agua', 1200.00, 'reuniones', 'servicios/servicio_agua_9vGc7xR.png'),
	(7, 'Rotafolios / pizarras', 700.00, 'reuniones', 'servicios/rotafolios_pizarras_ygbAxFu.png'),
	(8, 'Stands modulares o personalizados', 8749.00, 'expos', 'servicios/stands_qtnJpjj.png'),
	(9, 'Mesas y sillas adicionales para expositores', 899.00, 'expos', 'servicios/mesas_sillas_expos_qMUW3JB.png'),
	(10, 'Pantallas LED / proyectores para presentaciones', 7499.00, 'expos', 'servicios/pantalla_led_JyWLyWu.png'),
	(11, 'Sistema de sonido para anuncios y charlas', 3129.00, 'expos', 'servicios/sistema_sonido_i0VT9uP.png'),
	(12, 'Catering para expositores y asistentes', 2300.00, 'expos', 'servicios/catering_hv2DtlN.png'),
	(13, 'Banquete / catering', 9399.00, 'fiestas', 'servicios/banquete_c0klXWZ.png'),
	(14, 'Decoración temática', 5200.00, 'fiestas', 'servicios/decoracion_yV9gEHR.png'),
	(15, 'Música / DJ', 3400.00, 'fiestas', 'servicios/musica_SeoYHL0.png'),
	(16, 'Fotografía y video', 2200.00, 'fiestas', 'servicios/fotografia_video_iMpNrXQ.png'),
	(17, 'Meseros', 1800.00, 'fiestas', 'servicios/meseros_xGpTLx6.png'),
	(18, 'Luces y ambientación', 34059.00, 'fiestas', 'servicios/luces_ambientacion_9f8max5.png'),
	(19, 'Pastel y repostería', 2200.00, 'fiestas', 'servicios/pastel_ctZ6slU.png'),
	(20, 'Barra libre o bebidas', 3600.00, 'fiestas', 'servicios/barra_libre_8igq5JP.png'),
	(26, 'Equipo de sonido', 5000.00, 'reuniones', 'servicios/equipo_sonido_0NUw9hY.png');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
