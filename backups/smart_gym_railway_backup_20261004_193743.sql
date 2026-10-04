-- ==================================================
-- SMART GYM DATABASE BACKUP
-- ==================================================
-- Database: railway
-- Created: 2026-10-04 19:37:46
-- Source: Railway MySQL
-- ==================================================

SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE='NO_AUTO_VALUE_ON_ZERO';
SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS `railway` CHARACTER SET utf8mb4;

USE `railway`;


-- --------------------------------------------------
-- TABLE: access_logs
-- --------------------------------------------------

DROP TABLE IF EXISTS `access_logs`;
CREATE TABLE `access_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `direction` varchar(5) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `result` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `reason` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=111 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (26, 'W0001', 'IN', 'ALLOW', 'VALID_WALKIN', '2026-03-24 20:34:31');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (27, 'M0001', 'IN', 'ALLOW', 'VALID_MEMBER', '2026-03-24 20:35:17');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (28, 'W0001', 'IN', 'ALLOW', 'VALID_WALKIN', '2026-03-30 15:25:58');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (29, 'M0001', 'IN', 'ALLOW', 'VALID_MEMBER', '2026-04-01 13:46:50');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (30, 'M0001', 'IN', 'ALLOW', 'VALID_MEMBER', '2026-04-01 14:14:01');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (31, 'M0001', 'IN', 'ALLOW', 'VALID_MEMBER', '2026-04-01 14:14:44');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (32, 'M0001', 'IN', 'ALLOW', 'VALID_MEMBER', '2026-04-01 14:32:26');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (33, 'M0001', 'IN', 'ALLOW', 'VALID_MEMBER', '2026-04-01 14:51:26');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (34, 'M0001', 'IN', 'ALLOW', 'VALID_MEMBER', '2026-04-01 14:59:47');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (35, 'M0001', 'IN', 'ALLOW', 'VALID_MEMBER', '2026-04-03 14:00:04');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (36, 'M0001', 'IN', 'ALLOW', 'VALID_MEMBER', '2026-04-03 14:05:07');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (37, 'M0001', 'IN', 'ALLOW', 'VALID_MEMBER', '2026-04-03 14:14:57');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (38, 'M0001', 'IN', 'ALLOW', 'VALID_MEMBER', '2026-04-03 14:22:42');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (39, 'M0001', 'IN', 'ALLOW', 'VALID_MEMBER', '2026-04-03 14:31:53');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (40, 'M0001', 'IN', 'ALLOW', 'VALID_MEMBER', '2026-04-03 14:50:26');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (41, 'M0001', 'IN', 'ALLOW', 'VALID_MEMBER', '2026-04-03 17:06:37');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (42, 'M0001', 'IN', 'ALLOW', 'VALID_MEMBER', '2026-04-06 14:24:05');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (43, 'W0001', 'IN', 'ALLOW', 'VALID_WALKIN', '2026-04-11 14:13:46');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (44, 'W0001', 'IN', 'ALLOW', 'VALID_WALKIN', '2026-04-11 14:30:56');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (45, 'W0001', 'IN', 'ALLOW', 'VALID_WALKIN', '2026-04-11 14:38:01');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (46, 'W0001', 'IN', 'ALLOW', 'VALID_WALKIN', '2026-04-11 14:38:56');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (47, 'W0001', 'IN', 'ALLOW', 'VALID_WALKIN', '2026-04-11 14:42:10');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (48, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-11 21:45:53');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (49, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-11 21:51:43');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (50, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-11 22:00:35');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (51, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-11 22:02:20');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (52, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-11 22:09:31');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (53, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-11 23:00:09');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (54, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-11 23:06:49');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (55, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-11 23:12:50');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (56, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-11 23:19:05');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (57, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-11 23:19:59');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (58, 'W0002', 'IN', 'ALLOW', 'VALID', '2026-04-12 15:42:45');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (59, 'M0002', 'IN', 'ALLOW', 'VALID', '2026-04-12 16:02:11');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (60, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-12 18:53:44');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (61, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-12 18:54:46');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (62, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-12 18:55:58');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (63, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-12 18:57:22');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (64, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-12 18:58:35');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (65, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-12 19:01:27');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (66, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-12 19:04:41');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (67, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-12 19:12:40');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (68, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-12 19:14:01');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (69, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-12 20:06:45');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (70, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-12 20:11:40');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (71, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-12 20:12:41');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (72, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-12 20:17:20');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (73, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-12 20:18:27');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (74, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-12 20:34:02');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (75, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-12 20:35:04');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (76, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-12 20:37:02');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (77, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-12 20:38:48');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (78, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-14 20:23:43');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (79, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-14 20:59:38');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (80, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-04-14 21:03:58');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (81, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-04-19 10:47:21');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (82, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-04-22 19:14:11');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (83, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-04-22 19:57:15');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (84, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-04-22 20:07:56');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (85, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-04-22 20:09:01');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (86, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-04-22 20:23:18');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (87, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-04-22 20:24:41');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (88, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-04-22 20:30:47');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (89, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-04-22 21:04:58');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (90, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-04-22 21:13:22');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (91, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-04-22 21:19:50');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (92, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-04-23 09:42:18');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (93, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-04-23 09:52:45');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (94, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-04-23 09:55:40');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (95, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-04-23 10:16:20');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (96, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-04-23 18:28:15');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (97, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-04-23 18:32:14');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (98, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-04-23 18:36:47');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (99, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-04-23 18:42:21');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (100, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-04-23 18:50:08');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (101, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-04-23 18:51:59');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (102, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-05-02 10:56:19');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (103, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-05-02 11:01:19');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (104, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-05-02 11:08:58');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (105, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-05-03 01:45:10');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (106, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-05-03 01:54:24');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (107, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-05-03 02:28:05');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (108, 'M0001', 'IN', 'ALLOW', 'VALID', '2026-05-03 05:50:46');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (109, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-05-03 13:34:30');
INSERT INTO `access_logs` (`id`, `user_id`, `direction`, `result`, `reason`, `timestamp`) VALUES (110, 'W0001', 'IN', 'ALLOW', 'VALID', '2026-05-09 19:03:26');


-- --------------------------------------------------
-- TABLE: attendance_sessions
-- --------------------------------------------------

DROP TABLE IF EXISTS `attendance_sessions`;
CREATE TABLE `attendance_sessions` (
  `session_id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `time_in` datetime DEFAULT NULL,
  `time_out` datetime DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`session_id`),
  KEY `idx_user_timeout` (`user_id`,`time_out`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (1, 'M0003', '2026-06-08 07:59:25', '2026-06-08 08:05:41', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (2, 'M0003', '2026-06-08 08:06:09', '2026-06-08 08:06:26', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (3, 'M0005', '2026-06-08 08:07:14', NULL, 'ACTIVE');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (4, 'M0002', '2026-06-08 08:08:41', '2026-06-08 08:08:56', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (5, 'M0003', '2026-06-08 08:09:11', '2026-06-08 09:38:30', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (6, 'W0002', '2026-06-08 09:37:07', '2026-06-08 09:37:16', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (7, 'M0003', '2026-06-08 09:46:46', '2026-06-08 11:21:03', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (8, 'W0002', '2026-06-08 11:29:01', NULL, 'ACTIVE');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (9, 'M0010', '2026-06-08 11:37:39', '2026-06-08 11:38:21', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (10, 'M0012', '2026-08-03 08:15:00', '2026-08-03 10:30:00', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (11, 'M0012', '2026-08-05 09:00:00', '2026-08-05 11:20:00', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (12, 'M0012', '2026-08-08 08:45:00', '2026-08-08 10:10:00', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (13, 'M0012', '2026-08-12 07:50:00', '2026-08-12 09:40:00', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (14, 'M0012', '2026-08-16 08:10:00', '2026-08-16 10:00:00', 'ACTIVE');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (15, 'M0012', '2026-08-16 11:46:30', '2026-08-24 17:51:04', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (16, 'M0010', '2026-08-24 20:43:34', '2026-08-24 21:02:35', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (17, 'M0010', '2026-08-24 21:09:44', '2026-08-24 21:16:44', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (18, 'M2001', '2026-09-11 08:30:00', '2026-09-11 12:45:00', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (19, 'W002', '2026-09-11 09:15:00', '2026-09-11 11:45:00', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (20, 'M2001', '2026-09-11 08:00:00', '2026-09-11 10:30:00', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (21, 'M2002', '2026-09-11 08:30:00', '2026-09-11 12:00:00', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (22, 'M2003', '2026-09-11 09:00:00', '2026-09-11 13:15:00', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (23, 'M2004', '2026-09-11 09:30:00', '2026-09-11 11:45:00', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (24, 'M2005', '2026-09-11 10:00:00', '2026-09-11 14:30:00', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (25, 'M2006', '2026-09-10 08:15:00', '2026-09-10 11:00:00', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (26, 'M2007', '2026-09-10 09:00:00', '2026-09-10 12:30:00', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (27, 'M2008', '2026-09-10 10:15:00', '2026-09-10 13:45:00', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (28, 'W002', '2026-09-11 09:15:00', '2026-09-11 11:45:00', 'COMPLETED');
INSERT INTO `attendance_sessions` (`session_id`, `user_id`, `time_in`, `time_out`, `status`) VALUES (29, 'W003', '2026-09-09 08:45:00', '2026-09-09 10:30:00', 'COMPLETED');


-- --------------------------------------------------
-- TABLE: fp_templates
-- --------------------------------------------------

DROP TABLE IF EXISTS `fp_templates`;
CREATE TABLE `fp_templates` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fp_id` int DEFAULT NULL,
  `template` longblob,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `fp_id` (`fp_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `fp_templates` (`id`, `user_id`, `fp_id`, `template`, `created_at`) VALUES (15, 'M0001', 0, X'30333033356232353134303133313031363830303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303031313030303330303831303030633030306330333366666666336666666565656666626165666165616165616261613661363539393535353536353539353635343535313031303030303034303130313031303130313031303130313031303130313031303130313031303130313031303130313031303130313031303130313031303130313031303130313031303130313031303130313031303130313031333131363565396537353134613331653362316239643165353439653637336537366133323462653234323735633165356461633132376535653331653762653263333730333765333762613939646531653139356533663632313738666466373031653865396636316130353139663531323635363366366461623530396636373338393135663533633235343366346131663161376334323261353666633334386464663564336138666130646433626161303039643439396164643361343433366163336135616239643339613563336336383761366330663863313935613139393264393430333735386439366539306532393634633134363162373537313735343537353139356132663535313936653333333466313761333531346439383239643130303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030333033356332353030303132303031363730303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030373030303330303762303030303030303063303030633033336666666666666666626262666262616565656561616161626139396136353935353535353535363535353435313034303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030', '2026-04-04 16:36:23');
INSERT INTO `fp_templates` (`id`, `user_id`, `fp_id`, `template`, `created_at`) VALUES (19, 'M0002', 3, X'30333033356533343134303133643031366130303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030353030303130303835303030303030303030633030303033333333666666666666666666666666656665656661656161616161616161363939393635393535353535353535353535353539343430313031303130313031303130313031303130313031303130313031303130313031303130313031303130313031303130313031303130313031303130313031303130313031303130313031303130313031313538366330666534383038343135653366386535393765363431643532646537316163353262653737393539313366333631663138666634626133313535663635326265386666343362306435316636633334353231663536333635323966333262353536626636396330393131663737633264313566343263316433396635323039353733633233396235643563336461373136666332303135303631643235316634323364326432343139396433343261393739643436333631336264343962396139356433643038303235613166303739373761323231323036316135643239353266613539306231353962333461353263646232626165393733623665303964333338333730613033313832313061383362383436323965613538363130623134393936343932363864393538613436393939356132363933373934383237643439393266616561633739333130613833353632343065343631363438386661633936363531376432643636363061393364373639386164343337363731363134353732613062303266343662633836376466336363383933396630303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030333033356233323030303132303031366230303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030323030303130303833303030303030303030303030303033333333336666666666666666666666666665656561616161616161616139613635393536353535353535353535353561393934343030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030', '2026-04-12 15:57:39');


-- --------------------------------------------------
-- TABLE: gym_access_types
-- --------------------------------------------------

DROP TABLE IF EXISTS `gym_access_types`;
CREATE TABLE `gym_access_types` (
  `id` int NOT NULL AUTO_INCREMENT,
  `access_name` varchar(50) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `duration_days` int NOT NULL,
  `status` enum('active','inactive') DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `gym_access_types` (`id`, `access_name`, `price`, `duration_days`, `status`, `created_at`) VALUES (1, 'Daily', 50.00, 1, 'active', '2026-10-03 13:40:04');
INSERT INTO `gym_access_types` (`id`, `access_name`, `price`, `duration_days`, `status`, `created_at`) VALUES (2, 'Monthly', 500.00, 30, 'active', '2026-10-03 13:40:04');


-- --------------------------------------------------
-- TABLE: locker_bookings
-- --------------------------------------------------

DROP TABLE IF EXISTS `locker_bookings`;
CREATE TABLE `locker_bookings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `locker_number` int DEFAULT NULL,
  `date` date DEFAULT NULL,
  `time` time DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_general_ci DEFAULT 'PENDING',
  `reason` text COLLATE utf8mb4_general_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `start_time` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `end_time` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=117 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (1, 'M0001', 1, '2026-04-08', '23:30:00', 'CANCELLED', 'fsafas', '2026-04-08 14:28:12', NULL, NULL);
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (2, 'M0001', 1, '2026-04-09', '16:40:00', 'CANCELLED', 'safasf', '2026-04-09 08:34:39', NULL, NULL);
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (3, 'M0001', 1, '2026-04-09', '17:00:00', 'CANCELLED', 'sffa', '2026-04-09 08:44:17', NULL, NULL);
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (4, 'M0001', 3, '2026-04-09', '17:00:00', 'CANCELLED', 'sfa', '2026-04-09 08:47:41', NULL, NULL);
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (5, 'M0001', 1, '2026-04-09', '17:10:00', 'CANCELLED', NULL, '2026-04-09 09:02:22', NULL, NULL);
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (6, 'M0001', 1, '2026-04-09', '18:00:00', 'CANCELLED', NULL, '2026-04-09 09:59:36', NULL, NULL);
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (7, 'M0001', 1, '2026-04-24', '9:20:00', 'CANCELLED', NULL, '2026-04-24 01:05:14', NULL, NULL);
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (8, 'M0002', 2, '2026-04-24', '9:13:00', 'CANCELLED', NULL, '2026-04-24 01:11:23', NULL, NULL);
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (9, 'M0001', 1, '2026-04-24', '10:30:00', 'CANCELLED', NULL, '2026-04-24 02:24:17', NULL, NULL);
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (10, 'M0001', 2, '2026-04-24', '10:53:00', 'CANCELLED', NULL, '2026-04-24 02:51:04', NULL, NULL);
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (11, 'S0001', 1, '2026-04-24', '11:42:00', 'CANCELLED', NULL, '2026-04-24 03:39:54', NULL, NULL);
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (12, 'M0001', 1, '2026-04-24', '12:15:00', 'CANCELLED', NULL, '2026-04-24 04:04:11', NULL, NULL);
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (13, 'M0001', 2, '2026-04-24', '12:57:00', 'CANCELLED', NULL, '2026-04-24 04:49:13', NULL, NULL);
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (14, 'M0001', 1, '2026-04-24', '13:20:00', 'CANCELLED', NULL, '2026-04-24 05:04:22', NULL, NULL);
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (15, 'M0001', 2, '2026-04-24', '14:05:00', 'CANCELLED', NULL, '2026-04-24 05:50:59', NULL, NULL);
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (16, 'M0001', 1, '2026-05-06', NULL, 'CANCELLED', 'sdasda', '2026-05-02 14:13:09', '08:00 AM', '11:00 AM');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (17, 'M0001', 3, '2026-05-01', NULL, 'CANCELLED', 'sdasdas', '2026-05-02 14:17:12', '08:00 AM', '11:00 AM');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (18, 'M0001', 1, '2026-05-02', NULL, 'CANCELLED', NULL, '2026-05-02 14:20:04', '08:00 AM', '11:00 AM');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (19, 'M0001', 2, '2026-05-02', NULL, 'CANCELLED', NULL, '2026-05-02 14:24:29', '08:00 AM', '11:00 AM');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (20, 'M0001', 1, '2026-05-03', NULL, 'CANCELLED', 'saas', '2026-05-02 14:33:28', '08:00 AM', '11:00 AM');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (21, 'M0001', 1, '2026-05-03', NULL, 'CANCELLED', 'sadas', '2026-05-02 14:33:28', '08:00 AM', '11:00 AM');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (22, 'M0001', 1, '2026-05-03', NULL, 'CANCELLED', 'sdas', '2026-05-02 14:33:28', '08:00 AM', '11:00 AM');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (23, 'M0001', 1, '2026-05-03', NULL, 'CANCELLED', NULL, '2026-05-02 14:33:28', '08:00 AM', '11:00 AM');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (24, 'M0001', 2, '2026-05-04', NULL, 'CANCELLED', 'ffsafsaf', '2026-05-02 14:43:36', '08:00 AM', '11:00 AM');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (25, 'M0001', 2, '2026-05-02', NULL, 'CANCELLED', NULL, '2026-05-02 14:49:08', '11:00 AM', '02:00 PM');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (26, 'M0001', 3, '2026-05-31', NULL, 'CANCELLED', NULL, '2026-05-02 15:05:20', '05:00 PM', '08:00 PM');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (27, 'M0001', 1, '2026-05-03', NULL, 'CANCELLED', NULL, '2026-05-02 15:29:03', '11:00 AM', '02:00 PM');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (28, 'M0001', 1, '2026-05-04', NULL, 'CANCELLED', NULL, '2026-05-02 15:49:29', '11:00 AM', '02:00 PM');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (29, 'M0001', 1, '2026-05-07', NULL, 'CANCELLED', 'hf', '2026-05-07 12:21:16', '21:00', '00:00');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (30, 'M0001', 1, '2026-05-08', NULL, 'CANCELLED', 'sfsafsaf', '2026-05-07 12:39:29', '01:39', '04:39');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (31, 'M0001', 1, '2026-05-16', NULL, 'CANCELLED', NULL, '2026-05-16 13:12:46', '21:20', '00:20');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (32, 'M0002', 2, '2026-05-16', NULL, 'CANCELLED', NULL, '2026-05-16 14:23:39', '22:33', '01:33');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (33, 'M0001', 1, '2026-05-17', NULL, 'CANCELLED', NULL, '2026-05-16 16:04:37', '00:12', '03:12');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (34, 'M0001', 1, '2026-05-17', NULL, 'CANCELLED', NULL, '2026-05-16 16:25:40', '00:30', '03:30');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (35, 'M0001', 1, '2026-05-17', NULL, 'CANCELLED', NULL, '2026-05-16 16:56:40', '01:00', '04:00');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (36, 'M0001', 1, '2026-05-17', NULL, 'CANCELLED', 'ghg', '2026-05-17 13:54:57', '22:57', '01:57');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (37, 'M0001', 1, '2026-05-17', NULL, 'CANCELLED', NULL, '2026-05-17 13:55:07', '22:00', '01:00');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (38, 'M0001', 1, '2026-05-17', NULL, 'CANCELLED', NULL, '2026-05-17 14:55:52', '23:05', '02:05');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (39, 'M0003', 1, '2026-05-18', NULL, 'CANCELLED', NULL, '2026-05-18 10:06:56', '18:10', '21:10');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (40, 'M0001', 1, '2026-05-19', NULL, 'CANCELLED', NULL, '2026-05-19 02:18:33', '10:25', '13:25');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (41, 'M0001', 1, '2026-05-19', NULL, 'CANCELLED', NULL, '2026-05-19 02:34:35', '14:50', '17:50');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (42, 'M0001', 1, '2026-05-20', NULL, 'CANCELLED', NULL, '2026-05-19 02:43:03', '01:34', '04:34');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (43, 'M0001', 1, '2026-05-19', NULL, 'CANCELLED', NULL, '2026-05-19 02:44:46', '18:50', '21:50');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (44, 'M0001', 2, '2026-05-19', NULL, 'CANCELLED', NULL, '2026-05-19 02:54:13', '22:00', '01:00');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (45, 'M0001', 3, '2026-05-19', NULL, 'CANCELLED', 'd', '2026-05-19 03:04:18', '19:10', '22:10');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (46, 'M0001', 1, '2026-05-19', NULL, 'CANCELLED', 'ds', '2026-05-19 03:09:23', '11:10', '14:10');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (47, 'M0001', 2, '2026-05-19', NULL, 'CANCELLED', 'dsfdg', '2026-05-19 03:13:38', '11:30', '14:30');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (48, 'M0001', 3, '2026-05-19', NULL, 'CANCELLED', 'dsdg', '2026-05-19 03:21:13', '11:30', '14:30');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (49, 'M0001', 2, '2026-05-19', NULL, 'CANCELLED', 'dssd', '2026-05-19 03:25:20', '17:25', '20:25');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (50, 'M0001', 1, '2026-05-19', NULL, 'CANCELLED', NULL, '2026-05-19 04:02:10', '12:08', '15:08');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (51, 'M0001', 2, '2026-05-19', NULL, 'CANCELLED', NULL, '2026-05-19 04:14:37', '12:20', '15:20');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (52, 'M0001', 2, '2026-05-19', NULL, 'CANCELLED', NULL, '2026-05-19 04:22:16', '15:30', '18:30');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (53, 'M0001', 1, '2026-05-19', NULL, 'CANCELLED', NULL, '2026-05-19 07:21:19', '15:40', '18:40');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (54, 'M0001', 3, '2026-05-19', NULL, 'CANCELLED', 'under development', '2026-05-19 09:37:03', '19:40', '22:40');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (55, 'M0001', 3, '2026-05-19', NULL, 'CANCELLED', 'under development', '2026-05-19 09:43:10', '19:45', '22:45');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (56, 'M0001', 3, '2026-05-19', NULL, 'CANCELLED', 'SYSTEM UNDER MAINTENANCE', '2026-05-19 09:50:14', '19:50', '22:50');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (57, 'M0001', 3, '2026-05-19', NULL, 'CANCELLED', 'UNDER MAINTENCAE', '2026-05-19 09:56:02', '19:55', '22:55');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (58, 'M0001', 3, '2026-05-19', NULL, 'CANCELLED', 'under maintenance', '2026-05-19 10:20:07', '20:20', '23:20');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (59, 'M0001', 3, '2026-05-19', NULL, 'CANCELLED', NULL, '2026-05-19 11:09:09', '19:30', '22:30');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (60, 'M0003', 2, '2026-05-19', NULL, 'CANCELLED', NULL, '2026-05-19 12:06:47', '20:25', '23:25');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (61, 'M0001', 1, '2026-05-20', NULL, 'CANCELLED', NULL, '2026-05-19 14:22:11', '00:50', '03:50');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (62, 'M0001', 2, '2026-05-20', NULL, 'CANCELLED', NULL, '2026-05-20 08:57:00', '01:00', '04:00');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (63, 'M0003', 2, '2026-05-20', NULL, 'CANCELLED', 'sfsdfsdf', '2026-05-20 08:59:11', '01:00', '04:00');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (64, 'M0003', 1, '2026-05-21', NULL, 'CANCELLED', 'kdhfdjshfsd', '2026-05-20 09:37:12', '17:40', '20:40');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (65, 'M0003', 1, '2026-05-20', NULL, 'CANCELLED', NULL, '2026-05-20 10:10:40', '01:00', '04:00');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (66, 'M0003', 2, '2026-05-20', NULL, 'CANCELLED', 'beh tama na ', '2026-05-20 10:13:39', '18:13', '21:13');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (67, 'M0003', 1, '2026-05-20', NULL, 'CANCELLED', 'hdsahdgajhdga', '2026-05-20 10:16:29', '18:16', '21:16');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (68, 'M0003', 3, '2026-05-20', NULL, 'CANCELLED', 'dsfsd', '2026-05-20 14:21:48', '01:25', '04:25');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (69, 'M0003', 3, '2026-05-20', NULL, 'CANCELLED', NULL, '2026-05-20 14:44:35', '10:44', '13:44');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (70, 'M0001', 1, '2026-05-20', NULL, 'CANCELLED', NULL, '2026-05-20 15:10:56', '23:30', '02:30');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (71, 'M0001', 1, '2026-05-21', NULL, 'CANCELLED', NULL, '2026-05-20 17:03:32', '01:20', '04:20');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (72, 'M0001', 1, '2026-05-21', NULL, 'CANCELLED', NULL, '2026-05-20 17:28:51', '05:32', '08:32');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (73, 'M0003', 1, '2026-05-21', NULL, 'CANCELLED', NULL, '2026-05-21 09:52:17', '17:53', '20:53');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (74, 'm0001', 1, '2026-05-21', NULL, 'CANCELLED', NULL, '2026-05-21 13:41:10', '21:45', '00:45');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (75, 'M0002', 1, '2026-05-21', NULL, 'CANCELLED', NULL, '2026-05-21 15:07:56', '23:25', '02:25');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (76, 'M0002', 1, '2026-05-21', NULL, 'CANCELLED', NULL, '2026-05-21 15:19:12', '23:35', '02:35');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (77, 'M0002', 2, '2026-05-22', NULL, 'CANCELLED', NULL, '2026-05-21 15:56:59', '00:10', '03:10');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (78, 'M0002', 1, '2026-05-22', NULL, 'CANCELLED', NULL, '2026-05-21 16:12:39', '00:30', '03:30');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (79, 'M0002', 1, '2026-05-22', NULL, 'CANCELLED', NULL, '2026-05-21 16:34:55', '00:50', '03:50');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (80, 'm0001', 2, '2026-05-25', NULL, 'CANCELLED', NULL, '2026-05-25 05:59:37', '13:59', '16:59');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (81, 'm0001', 3, '2026-05-25', NULL, 'CANCELLED', 'locker is use right now', '2026-05-25 06:11:59', '14:12', '17:12');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (82, 'm0001', 1, '2026-05-25', NULL, 'CANCELLED', 'user', '2026-05-25 06:13:08', '14:13', '17:13');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (83, 'm0001', 2, '2026-05-25', NULL, 'CANCELLED', 'dsgdfgdf', '2026-05-25 06:14:00', '18:17', '21:17');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (84, 'm0001', 2, '2026-05-25', NULL, 'CANCELLED', NULL, '2026-05-25 06:15:12', '02:18', '05:18');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (85, 'm0001', 1, '2026-05-25', NULL, 'CANCELLED', 'ascadasf', '2026-05-25 06:28:04', '02:32', '05:32');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (86, 'm0001', 1, '2026-05-25', NULL, 'CANCELLED', 'qwrsfsfs', '2026-05-25 10:58:16', '18:01', '21:01');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (87, 'm0005', 1, '2026-06-05', NULL, 'CANCELLED', 'dsdsd', '2026-06-05 12:54:39', '20:54', '23:54');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (88, 'm0002', 1, '2026-06-06', NULL, 'CANCELLED', NULL, '2026-06-06 03:00:26', '11:20', '14:20');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (89, 'm0005', 1, '2026-06-06', NULL, 'CANCELLED', NULL, '2026-06-06 04:58:21', '13:15', '16:15');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (90, 'm0004', 1, '2026-06-07', NULL, 'CANCELLED', NULL, '2026-06-06 17:24:44', '01:35', '04:35');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (91, 'm0004', 1, '2026-06-07', NULL, 'CANCELLED', NULL, '2026-06-06 17:58:42', '02:05', '05:05');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (92, 'm0004', 1, '2026-06-07', NULL, 'CANCELLED', NULL, '2026-06-07 01:31:25', '09:40', '12:40');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (93, 'm0004', 1, '2026-06-07', NULL, 'CANCELLED', NULL, '2026-06-07 02:17:12', '10:25', '13:25');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (94, 'M0004', 2, '2026-06-07', NULL, 'CANCELLED', NULL, '2026-06-07 05:28:34', '13:36', '16:36');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (95, 'M0004', 2, '2026-06-07', NULL, 'CANCELLED', NULL, '2026-06-07 07:36:31', '15:40', '18:40');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (96, 'M0004', 2, '2026-06-07', NULL, 'CANCELLED', NULL, '2026-06-07 07:44:29', '15:55', '18:55');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (97, 'M0004', 2, '2026-06-07', NULL, 'CANCELLED', NULL, '2026-06-07 08:19:50', '16:25', '19:25');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (98, 'M0004', 3, '2026-06-07', NULL, 'REJECTED', 'fssdaf', '2026-06-07 10:08:56', '18:02', '21:02');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (99, 'M0004', 1, '2026-06-07', NULL, 'CANCELLED', NULL, '2026-06-07 10:12:07', '18:13', '21:13');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (100, 'm0007', 3, '2026-06-08', NULL, 'PENDING', NULL, '2026-06-07 11:43:58', '22:43', '01:43');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (101, 'M0004', 1, '2026-06-08', NULL, 'CANCELLED', NULL, '2026-06-08 03:11:57', '11:15', '14:15');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (102, 'M0004', 1, '2026-06-08', NULL, 'CANCELLED', NULL, '2026-06-08 03:27:02', '11:28', '14:28');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (103, '73', 1, '2026-08-16', NULL, 'CANCELLED', NULL, '2026-08-16 09:16:52', '17:16', '20:16');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (104, '73', 3, '2026-08-16', NULL, 'REJECTED', 'waahh', '2026-08-16 09:35:17', '17:38', '20:38');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (105, '73', 1, '2026-08-17', NULL, 'REJECTED', 'ad', '2026-08-17 03:06:54', '11:06', '14:06');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (108, 'M0012', 1, '2026-08-18', NULL, 'REJECTED', 'k', '2026-08-18 06:15:36', '14:15', '17:15');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (109, 'M0012', 2, '2026-08-18', NULL, 'REJECTED', 'k', '2026-08-18 06:15:42', '14:15', '17:15');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (110, 'M0012', 3, '2026-08-18', NULL, 'REJECTED', 'k', '2026-08-18 06:15:53', '14:15', '17:15');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (112, 'M0011', 1, '2026-09-20', NULL, 'REJECTED', 'ayawko', '2026-09-20 02:57:58', '14:00', '17:00');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (114, 'M0011', 3, '2026-09-20', NULL, 'REJECTED', 'ayawk', '2026-09-20 03:17:25', '11:19', '14:19');
INSERT INTO `locker_bookings` (`id`, `user_id`, `locker_number`, `date`, `time`, `status`, `reason`, `created_at`, `start_time`, `end_time`) VALUES (115, 'M0011', 1, '2026-09-20', NULL, 'REJECTED', 'ayaw kolang', '2026-09-20 04:06:19', '12:06', '15:06');


-- --------------------------------------------------
-- TABLE: locker_sessions
-- --------------------------------------------------

DROP TABLE IF EXISTS `locker_sessions`;
CREATE TABLE `locker_sessions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `locker_number` int DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `overtime_paid` tinyint(1) DEFAULT '0',
  `status` varchar(20) COLLATE utf8mb4_general_ci DEFAULT 'active',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=214 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `locker_sessions` (`id`, `user_id`, `locker_number`, `start_time`, `end_time`, `overtime_paid`, `status`) VALUES (213, 'M0011', 2, '2026-09-26 14:53:01', NULL, 0, 'active');


-- --------------------------------------------------
-- TABLE: lockers
-- --------------------------------------------------

DROP TABLE IF EXISTS `lockers`;
CREATE TABLE `lockers` (
  `locker_number` int NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_general_ci DEFAULT 'AVAILABLE',
  PRIMARY KEY (`locker_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `lockers` (`locker_number`, `status`) VALUES (1, 'AVAILABLE');
INSERT INTO `lockers` (`locker_number`, `status`) VALUES (2, 'OCCUPIED');
INSERT INTO `lockers` (`locker_number`, `status`) VALUES (3, 'AVAILABLE');


-- --------------------------------------------------
-- TABLE: member_activation
-- --------------------------------------------------

DROP TABLE IF EXISTS `member_activation`;
CREATE TABLE `member_activation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `member_id` varchar(20) NOT NULL,
  `activation_token` varchar(255) NOT NULL,
  `status` enum('PENDING','USED') DEFAULT 'PENDING',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `used_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `activation_token` (`activation_token`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (8, 'M0012', 'dlYNysr4r31lfPrDzHept9q_FMUCZ8DeRxq_eNAwcuw', 'PENDING', '2026-08-24 09:57:50', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (9, 'M0012', 'XcuoWevghh5bLctScqeM8m7AXCMQIcxzivq02K6BMIE', 'PENDING', '2026-08-24 10:32:09', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (10, 'M0011', 'f_Y36lTuvUObS6CjeJcjU9DVZ1yY1l4_tbTOLYrf0Wk', 'PENDING', '2026-08-24 10:35:50', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (11, 'M0011', 'INvdzO0Hft4y2NkVdN4sqmcn_FcVHVgvmK6MvDzsz8c', 'PENDING', '2026-08-24 12:02:15', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (12, 'M0010', 'W-SfPhZL8E04YiJQb0qW28qQuEZFAQcELQTcoJY9d28', 'PENDING', '2026-08-24 12:21:18', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (13, 'M0010', 'iVuOF-cn7wM_pAG9cStntqbGbAtgGWoyv0-vs3hJUtU', 'PENDING', '2026-08-24 12:37:21', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (14, 'M0010', 'HRwucw8ctcTKwP_YUCTWcbYhoktakJAW-7fkZ7CVtgU', 'PENDING', '2026-08-28 11:51:55', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (15, 'M0011', 'E0rNj9bTBLSv_jA8yIPbr7L-dluSkjJ8jxYdmfeT3eY', 'PENDING', '2026-08-28 12:08:29', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (16, 'M0010', 'h02lrh4czqSjoh7l6q6WiCfvadv2-IGG4XwUzRP7tsg', 'PENDING', '2026-08-28 12:22:28', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (17, 'M0010', 'uSAAeZBAYmTcDBT8TqriIOF-ZMD2PO1mBO5HAA0ksq4', 'PENDING', '2026-08-28 12:40:19', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (18, 'M0007', '2qcYcAgzHV53hWywe3kEifFX31Zcz891S85XTu7GMUg', 'PENDING', '2026-08-28 14:49:00', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (19, 'M0008', 'sjqBh1Cpal7FkQiLnzuUz0U3fXJpol8lJvqijbvQj7o', 'PENDING', '2026-08-29 10:46:58', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (21, 'M0007', '7dCKdPGTr5-B25bQKYJdekuJusXz9uO6jTl3gJQGjbE', 'PENDING', '2026-08-29 11:15:59', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (23, 'M0007', 'tqy4LTgDJ918QiGV8HWk8RIFVpwKNQpGZadlncv_ZQI', 'PENDING', '2026-08-29 13:53:57', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (25, 'M0007', '_npDEFlxwIoVQvhMD1oM0XqCcYWu3J6X-7iTfjVIuEs', 'PENDING', '2026-08-29 14:01:38', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (27, 'M0007', 'lb-uuLjnoprhirGkRsfJQ4aVV8tJJT-GF3u-K6DbCcA', 'PENDING', '2026-08-29 15:35:07', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (29, 'M0001', 'EP1n6j5IXgmnwcdnqJ0ECu8fMe0u71PiA5hck6-O_FE', 'PENDING', '2026-08-30 03:43:21', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (31, 'M0001', 'GkcxKblIo3XGjC6LU42eTk8pONHBuTtQRyFxxby_UK0', 'PENDING', '2026-08-30 04:09:45', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (33, 'M0001', 'UUDGpLIifJG7kzsJOTO7kPclPobm9LOGkIALNxjfYYE', 'PENDING', '2026-10-04 07:04:49', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (36, 'M0001', 'CrJ1NHTBqia4fwshSQepptOmShLKRZteH5UpHMaFk0U', 'PENDING', '2026-10-04 08:22:46', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (38, 'M0001', 'GbKLvM_4ewJI7KIwlDl57EDR5G2Yc2lyaYuD5Ip9TxE', 'PENDING', '2026-10-04 08:38:15', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (40, 'M0001', 'sDjquU76udzsYQv4I0k6_NNfR9xMdeAJfp6m8LvCeP4', 'PENDING', '2026-10-04 08:38:28', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (42, 'M0002', 'rXvNHURBDpi9O2UWd18DqBlFk_dONk8P6_Lx1F43tvk', 'PENDING', '2026-10-04 09:09:23', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (44, 'M0003', '-qXgJdDfVpDJDqBX-cNEpvsxZt9ynQsyHqPOeivZj4s', 'PENDING', '2026-10-04 09:24:08', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (46, 'M0004', 'MLaPuhA1-tTpfWQbahUnDdGGnKAD9zEgKokgV42U7us', 'USED', '2026-10-04 10:28:49', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (48, 'M0005', 'GxvbVBwYYmKQpZ2EbWXWdfuwID7-a0AfYaTYmEHLmrQ', 'PENDING', '2026-10-04 10:44:10', NULL);
INSERT INTO `member_activation` (`id`, `member_id`, `activation_token`, `status`, `created_at`, `used_at`) VALUES (50, 'M0006', 'sNQkwjiL0y7bihYqhB1hkVxYzD-Nms73UwGnPdWg4jQ', 'PENDING', '2026-10-04 11:02:14', NULL);


-- --------------------------------------------------
-- TABLE: members
-- --------------------------------------------------

DROP TABLE IF EXISTS `members`;
CREATE TABLE `members` (
  `id` varchar(10) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `fingerprint_template` text,
  `phone_number` varchar(20) NOT NULL,
  `membership_type` varchar(20) DEFAULT NULL,
  `membership_expires` datetime DEFAULT NULL,
  `monthly_expires` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `last_sms_sent` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `members` (`id`, `full_name`, `fingerprint_template`, `phone_number`, `membership_type`, `membership_expires`, `monthly_expires`, `created_at`, `last_sms_sent`) VALUES ('M0001', 'aldrin', '030360270001200170000000000000000000000000000000000000000000000000000000000000000000000000000000010000007700000000000000033fffffffffffbbbbbaabaaaaaa9666659655555555554000000000000000000000000000000000000000000000000101010101010000000000000000000000000000005305235e6308a47e4494633e4f18641e3122515e4725e41e1eaa563e592ae49e112dd67e3fae0efe30af51fe53b54e5e718b24ff550fe31f2d12ce5f3b1462df6d19657f431f4ddf36b625df0809a47c430ae21c2d9ad09c131d1cbc1fa0673a1805645b2187649b1a08a4db1820985b4086cbb937878c393c078bd91595e2b91a96e439251a25b91718dff6241cd2160b8589d70d0660f71f99d6b70000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003036027000120017000000000000000000000000000000000000000000000000000000000000000000000000000000002000000790000000000000003cfffffffffffbbebbbaaaaaaaaa59996599555555555440000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', '09913354822', NULL, NULL, NULL, '2026-10-04 08:11:48', NULL);
INSERT INTO `members` (`id`, `full_name`, `fingerprint_template`, `phone_number`, `membership_type`, `membership_expires`, `monthly_expires`, `created_at`, `last_sms_sent`) VALUES ('M0002', 'atyiii', '0303562f000120016b000000000000000000000000000000000000000000000000000000000000000000000000000000030000007500000000000333cf3f3ffffffffbbbbabaaaa9a999959596556556554544000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000298445fe289606fe649ca5de5da7929e6233d23e4b2a183f56af157f2bb143ff1f321abf4b07e33d4c9f979a4386607b3c86851b3516075b3d8add18438cdf784ea296d84e0be3d9518e6479558f4df94891e159592213b953a2a919478ba1f63217de165a1710d748185d57569865574d1363b549145f75201fdcf53a1e1c5252184fb3529a2453319c4ad3301d22532624845329a21cb04f96e4913b2002514b97216f4c97982f36a396ef35a42bcf329ed70d319f6c2b309f81ab000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003035127000120016a000000000000000000000000000000000000000000000000000000000000000000000000000000020000007500000000000333cf3f3ffcfefffefbbbaeaaaa6a66656595959565555544000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', '09058609831', NULL, NULL, NULL, '2026-10-04 09:09:18', NULL);
INSERT INTO `members` (`id`, `full_name`, `fingerprint_template`, `phone_number`, `membership_type`, `membership_expires`, `monthly_expires`, `created_at`, `last_sms_sent`) VALUES ('M0003', 'sigabo', '03035f1f0001200165000000000000000000000000000000000000000000000000000000000000000000000000000000050000007b0000000000000ccff3fffffefefbbbeebbabaaaa6a9a995a5555555155151440000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e135efe33221fde6423d53e0c27889e1631093e46b55bbe3b14c93f6e18905f529d9eff162a1ebf603095ff3e85487c12b7dfdc2429073d28ab9dfd5807235a5287df1b45a1c97b44a4a0fb193648fb6289e3d8658be27857902138639523184784c9f94707a0596608ccd95d8e22d9540f20195f17dff96397e29900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003035f230001200165000000000000000000000000000000000000000000000000000000000000000000000000000000050000007b0000000000000ccffcfffffefefbbbeebbaeaaaa6a9a9959955554555454544000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', '09058609831', NULL, NULL, NULL, '2026-10-04 09:24:04', NULL);
INSERT INTO `members` (`id`, `full_name`, `fingerprint_template`, `phone_number`, `membership_type`, `membership_expires`, `monthly_expires`, `created_at`, `last_sms_sent`) VALUES ('M0004', 'luisidto', '03035532000120015d000000000000000000000000000000000000000000000000000000000000000000000000000000060000007700000000000333fcffffeffbbffbbbbbbaaaa9aaaa9955555555511155144000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006b900c9e1491499e6724d03e0da908de400a637f360d22df5a0d647f5b12249f3d97a27f241ae0bf159f889f0820091f0f35895f5586a47c2b13a1fc0f979e9c579be47c4e8863fd25871fba61890e1a660924ba268bca9a2890215a0c1407fa2b09a1db2fab1f7b35acc9f91b380899432c00d637a06177382e857734aee0773aa02cd44e9c62954e9d0cb5439f20f53625e475552ae6753825207138255951481fe26f4420ddaf45a0e96f5024958f4f25e9cf3fa728ef5ca4a5ec432489ed4424c04d3c27854d000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003035d1a00012001590000000000000000000000000000000000000000000000000000000000000000000000000000000800000071000000000033ff3ffffbffefeefbaba9a6aa6aaa66555555145145540400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', '09058609831', NULL, NULL, NULL, '2026-10-04 10:28:43', NULL);
INSERT INTO `members` (`id`, `full_name`, `fingerprint_template`, `phone_number`, `membership_type`, `membership_expires`, `monthly_expires`, `created_at`, `last_sms_sent`) VALUES ('M0005', 'sfas', '0303542b0001200166000000000000000000000000000000000000000000000000000000000000000000000000000000090000007d00000000333f303fff3ff33ffffeebabaaeaba99a9a666595565515514555444000000000000000000000000000000000000000000000000000000000000000000000000000000000000003c8489fe46069f3e268c1f1e62148cfe4196e15e2919603e6f9f8cde422361fe3f368f7e2f39e5de51be23be359860df602a8c1f4a2be2bc63b1a2dd66aecd3b1d22e0d918a45ff95329e2f9522c0cb93c3ea51915264d9743c026b7404068971aa72175422d0ed23b2761f333a7e2b32fa9e77318aa2153212c0e2f342ac8cd392d23ed39ade6cd392e0d8d22b0226d3429650b3329e32b36ab53eb382b9fab1b33c48b21b78127223823c700000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003035f140001200163000000000000000000000000000000000000000000000000000000000000000000000000000000090000007500000000cccfccf3fcff33ffcffeeaaaabaaaa69a6666555555145545544000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', '09913354822', 'monthly', '2027-10-04 18:43:43', '2026-11-03 18:43:43', '2026-10-04 10:43:59', NULL);
INSERT INTO `members` (`id`, `full_name`, `fingerprint_template`, `phone_number`, `membership_type`, `membership_expires`, `monthly_expires`, `created_at`, `last_sms_sent`) VALUES ('M0006', 'fsaffsaf', '03035732000120016f000000000000000000000000000000000000000000000000000000000000000000000000000000020000007d0000000000000000cfffffffffffeffbabbaaaaaaa66a6599596559565555544000000000000000000000000000000000000000000000000000000000000000000000000000000000000006f8d4efe362a429e18ad1c5e502f2b1e32359b3e4238821e62b8e99e6e85a2ff2905de9f6405e33f6b94e4ff6c9a50ff539aa8ff1c22c41f4faad73f75acd1df412f197f33af82df2630845f2736c3ff5821e8bc66a4e75c530a621d5196a7dd480c61ba5b26273a1c871bdb4f8d635b44176b5b6023525b5d2cd3d81b8920993c8bdf391b8f05794590a3194794a819602e28991e0d9d163f151657331940b52d1196d32b926c133e0fe24f3296acad3b101c4b3194140b38108269391157293811e0e93812a729000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003035832000120016f000000000000000000000000000000000000000000000000000000000000000000000000000000020000007d0000000000000000cfffffffffffeffbabbaaaaa9aa66a59659595656555554400000000000000000000000000000000000000000000000000000000000000000000000000000000000000', '09913354822', 'monthly', '2027-10-04 19:01:55', '2026-11-03 19:01:55', '2026-10-04 11:02:06', NULL);
INSERT INTO `members` (`id`, `full_name`, `fingerprint_template`, `phone_number`, `membership_type`, `membership_expires`, `monthly_expires`, `created_at`, `last_sms_sent`) VALUES ('M0011', 'Aldrin', NULL, '09123456789', 'Monthly', '2026-10-17 23:59:59', '2026-10-17 23:59:59', '2026-08-17 10:29:48', NULL);
INSERT INTO `members` (`id`, `full_name`, `fingerprint_template`, `phone_number`, `membership_type`, `membership_expires`, `monthly_expires`, `created_at`, `last_sms_sent`) VALUES ('M2001', 'Juan Dela Cruz', NULL, '09171234567', 'MONTHLY', '2026-09-30 00:00:00', '2026-09-30 00:00:00', '2026-09-06 14:29:13', NULL);
INSERT INTO `members` (`id`, `full_name`, `fingerprint_template`, `phone_number`, `membership_type`, `membership_expires`, `monthly_expires`, `created_at`, `last_sms_sent`) VALUES ('M2002', 'Maria Santos', NULL, '09182345678', 'MONTHLY', '2026-10-15 00:00:00', '2026-10-15 00:00:00', '2026-09-06 14:29:13', NULL);
INSERT INTO `members` (`id`, `full_name`, `fingerprint_template`, `phone_number`, `membership_type`, `membership_expires`, `monthly_expires`, `created_at`, `last_sms_sent`) VALUES ('M2003', 'Pedro Reyes', NULL, '09203456789', 'MONTHLY', '2026-08-20 00:00:00', '2026-08-20 00:00:00', '2026-09-06 14:29:13', NULL);
INSERT INTO `members` (`id`, `full_name`, `fingerprint_template`, `phone_number`, `membership_type`, `membership_expires`, `monthly_expires`, `created_at`, `last_sms_sent`) VALUES ('M2004', 'Ana Garcia', NULL, '09164567890', 'MONTHLY', '2026-11-05 00:00:00', '2026-11-05 00:00:00', '2026-09-06 14:29:13', NULL);
INSERT INTO `members` (`id`, `full_name`, `fingerprint_template`, `phone_number`, `membership_type`, `membership_expires`, `monthly_expires`, `created_at`, `last_sms_sent`) VALUES ('M2005', 'Carlo Mendoza', NULL, '09987654321', 'DAILY', '2026-09-07 00:00:00', NULL, '2026-09-06 14:29:13', NULL);
INSERT INTO `members` (`id`, `full_name`, `fingerprint_template`, `phone_number`, `membership_type`, `membership_expires`, `monthly_expires`, `created_at`, `last_sms_sent`) VALUES ('M2006', 'Sofia Cruz', NULL, '09198765432', 'DAILY', '2026-09-10 00:00:00', NULL, '2026-09-06 14:29:13', NULL);
INSERT INTO `members` (`id`, `full_name`, `fingerprint_template`, `phone_number`, `membership_type`, `membership_expires`, `monthly_expires`, `created_at`, `last_sms_sent`) VALUES ('M2007', 'Miguel Torres', NULL, '09321112222', 'DAILY', '2026-09-05 00:00:00', NULL, '2026-09-06 14:29:13', NULL);
INSERT INTO `members` (`id`, `full_name`, `fingerprint_template`, `phone_number`, `membership_type`, `membership_expires`, `monthly_expires`, `created_at`, `last_sms_sent`) VALUES ('M2008', 'Bianca Lim', NULL, '09453334444', 'DAILY', '2026-09-12 00:00:00', NULL, '2026-09-06 14:29:13', NULL);
INSERT INTO `members` (`id`, `full_name`, `fingerprint_template`, `phone_number`, `membership_type`, `membership_expires`, `monthly_expires`, `created_at`, `last_sms_sent`) VALUES ('M9999', 'Test Locker Member', NULL, '09999999999', 'Monthly', '2026-09-07 08:06:26', '2026-09-07 08:06:26', '2026-08-29 08:06:28', NULL);


-- --------------------------------------------------
-- TABLE: membership_types
-- --------------------------------------------------

DROP TABLE IF EXISTS `membership_types`;
CREATE TABLE `membership_types` (
  `id` int NOT NULL AUTO_INCREMENT,
  `membership_name` varchar(100) NOT NULL,
  `fee` decimal(10,2) NOT NULL,
  `validity_days` int NOT NULL,
  `status` enum('active','inactive') DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `membership_types` (`id`, `membership_name`, `fee`, `validity_days`, `status`, `created_at`) VALUES (1, 'Regular Membership', 600.00, 365, 'active', '2026-10-03 13:39:51');


-- --------------------------------------------------
-- TABLE: messages
-- --------------------------------------------------

DROP TABLE IF EXISTS `messages`;
CREATE TABLE `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(20) DEFAULT NULL,
  `sender_id` varchar(20) DEFAULT NULL,
  `sender_name` varchar(100) DEFAULT NULL,
  `sender_role` varchar(20) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `message` text,
  `reason` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `receiver_role` varchar(20) DEFAULT NULL,
  `is_read` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=107 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (4, 'M0012', NULL, NULL, NULL, 'BOOKING REJECTED', 'Your booking for Locker 3 was rejected.', 'k', '2026-08-18 06:16:03', NULL, 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (5, 'M0012', NULL, NULL, NULL, 'BOOKING REJECTED', 'Your booking for Locker 2 was rejected.', 'k', '2026-08-18 06:16:11', NULL, 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (6, 'M0012', NULL, NULL, NULL, 'BOOKING REJECTED', 'Your booking for Locker 1 was rejected.', 'k', '2026-08-18 06:16:14', NULL, 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (23, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-25 03:05:09', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (24, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-25 03:41:36', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (25, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-25 03:51:39', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (26, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-25 07:30:56', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (27, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-25 08:14:55', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (28, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-25 08:36:30', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (29, 'T0003', 'M0011', 'Aldrin', 'member', 'TRAINER RENEWAL', 'Aldrin renewed training with you.', '-', '2026-09-25 14:45:50', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (30, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-25 15:16:38', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (31, 'M0011', 'SYSTEM', 'Smart Gym', 'system', 'TRAINER FEE REMINDER', 'Your trainer is about to end in 3 days.', 'Trainer fee expiration reminder.', '2026-09-25 16:17:00', 'member', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (32, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-25 16:50:22', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (33, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-25 16:59:29', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (34, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-25 17:04:17', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (35, 'T0004', 'M0011', 'Aldrin', 'member', 'TRAINER CHANGE REQUEST', 'Aldrin requested to change trainer to you.', 'Member requested a trainer change.', '2026-09-26 09:53:32', 'trainer', 0);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (36, 'T0003', 'M0011', 'Aldrin', 'member', 'TRAINER CHANGE REQUEST', 'Aldrin requested to change trainer to you.', 'Member requested a trainer change.', '2026-09-26 10:06:16', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (37, 'T0004', 'M0011', 'Aldrin', 'member', 'TRAINER CHANGE REQUEST', 'Aldrin requested to change trainer to you.', 'Member requested a trainer change.', '2026-09-26 10:11:57', 'trainer', 0);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (38, 'T0003', 'M0011', 'Aldrin', 'member', 'TRAINER CHANGE REQUEST', 'Aldrin requested to change trainer to you.', 'Member requested a trainer change.', '2026-09-26 10:24:48', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (39, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Strength Training (PPL Strength).', 'Program change request: Strength Training - PPL Strength', '2026-09-26 11:36:36', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (40, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-26 11:45:46', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (41, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Build Muscle (Arnold Split).', 'Program change request: Build Muscle - Arnold Split', '2026-09-26 11:46:38', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (42, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Strength Training (Strength + Conditioning).', 'Program change request: Strength Training - Strength + Conditioning', '2026-09-26 11:52:04', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (43, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Build Muscle (PPL).', 'Program change request: Build Muscle - PPL', '2026-09-26 11:54:17', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (44, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Strength Training (Upper / Lower Strength).', 'Program change request: Strength Training - Upper / Lower Strength', '2026-09-26 11:55:06', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (45, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Build Muscle (PPL).', 'Program change request: Build Muscle - PPL', '2026-09-26 12:45:12', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (46, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Build Muscle (PPL).', 'Program change request: Build Muscle - PPL', '2026-09-26 12:54:01', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (47, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Weight Loss (Cardio & Full Body).', 'Program change request: Weight Loss - Cardio & Full Body', '2026-09-26 13:02:07', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (48, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Build Muscle (Upper / Lower).', 'Program change request: Build Muscle - Upper / Lower', '2026-09-26 13:03:56', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (49, 'ADMIN', NULL, NULL, NULL, 'NEW BOOKING', 'M0011 booked Locker 1 (09:59 AM - 12:59 PM)', '-', '2026-09-26 14:14:54', NULL, 0);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (50, 'M0011', 'S0001', 'Aldrin Dela Vega', 'staff', 'BOOKING ACCEPTED', 'Your booking for Locker 1 was accepted.', '-', '2026-09-26 14:15:16', 'member', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (51, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-28 03:55:54', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (52, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-28 04:03:10', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (53, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-28 05:09:23', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (54, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-28 07:20:42', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (55, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-28 07:50:35', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (56, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-28 07:55:47', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (57, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-28 08:55:19', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (58, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-28 09:47:00', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (59, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-28 09:52:01', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (60, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-28 11:04:17', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (61, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-28 11:22:17', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (62, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-28 11:34:59', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (63, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-28 12:09:51', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (64, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-28 12:31:22', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (65, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-28 12:36:40', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (66, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-28 12:56:05', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (67, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-28 12:56:05', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (68, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-28 13:30:36', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (69, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Build Muscle (PPL).', 'Program change request: Build Muscle - PPL', '2026-09-28 13:41:40', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (70, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-28 13:44:24', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (71, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Build Muscle (Arnold Split).', 'Program change request: Build Muscle - Arnold Split', '2026-09-28 13:46:07', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (72, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-28 13:52:21', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (73, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Build Muscle (Upper / Lower).', 'Program change request: Build Muscle - Upper / Lower', '2026-09-28 13:59:26', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (74, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Build Muscle (PPL).', 'Program change request: Build Muscle - PPL', '2026-09-28 14:23:36', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (75, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Build Muscle (Upper / Lower).', 'Program change request: Build Muscle - Upper / Lower', '2026-09-28 14:24:42', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (76, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Build Muscle (Arnold Split).', 'Program change request: Build Muscle - Arnold Split', '2026-09-28 14:31:58', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (77, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Build Muscle (PPL).', 'Program change request: Build Muscle - PPL', '2026-09-29 01:34:30', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (78, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to General Fitness (Full Body).', 'Program change request: General Fitness - Full Body', '2026-09-29 01:40:49', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (79, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Build Muscle (Bro Split).', 'Program change request: Build Muscle - Bro Split', '2026-09-29 01:41:42', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (80, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Build Muscle (Arnold Split).', 'Program change request: Build Muscle - Arnold Split', '2026-09-29 01:44:44', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (81, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-29 01:57:26', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (82, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Build Muscle (Arnold Split).', 'Program change request: Build Muscle - Arnold Split', '2026-09-29 02:07:06', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (83, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Build Muscle (PPL).', 'Program change request: Build Muscle - PPL', '2026-09-29 02:12:36', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (84, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-29 02:30:37', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (85, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-29 02:42:33', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (86, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-29 02:49:07', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (87, 'T0003', 'M0011', 'Aldrin', 'member', 'NEW TRAINER REQUEST', 'Aldrin sent you a trainer request.', '-', '2026-09-29 05:50:46', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (88, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Strength Training (PPL Strength).', 'Program change request: Strength Training - PPL Strength', '2026-09-29 06:22:25', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (89, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Build Muscle (PPL).', 'Program change request: Build Muscle - PPL', '2026-09-29 06:26:28', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (90, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Build Muscle (Arnold Split).', 'Program change request: Build Muscle - Arnold Split', '2026-09-29 06:42:57', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (91, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Build Muscle (PPL).', 'Program change request: Build Muscle - PPL', '2026-09-29 07:06:53', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (92, 'T0003', 'M0011', 'Aldrin', 'member', 'TRAINER RENEWAL REQUEST', 'Aldrin requested to renew their trainer rate with you.', 'Trainer renewal request - 1 Month', '2026-09-29 07:50:25', 'trainer', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (94, 'M0011', 'SYSTEM', 'Smart Gym', 'system', 'TRAINER FEE REMINDER', 'Your trainer is about to end tomorrow.', 'Trainer fee expiration reminder.', '2026-09-30 00:42:42', 'member', 1);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (95, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Build Muscle (Upper / Lower).', 'Program change request: Build Muscle - Upper / Lower', '2026-09-30 02:17:12', 'trainer', 0);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (96, 'T0003', 'M0011', 'Aldrin', 'member', 'PROGRAM CHANGE REQUEST', 'Aldrin requested to change program from their current program to Build Muscle (PPL).', 'Program change request: Build Muscle - PPL', '2026-09-30 02:55:56', 'trainer', 0);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (97, 'M0011', 'T0003', 'sfsaf', 'trainer', 'Program Change Accepted', 'Your program change request has been accepted by sfsaf.', 'program_change', '2026-09-30 02:56:13', NULL, 0);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (98, 'M2001', 'T0003', 'sfsaf', 'trainer', 'Trainer Request Accepted', 'Your trainer request has been accepted by sfsaf.', 'normal', '2026-09-30 15:16:22', NULL, 0);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (99, 'M2002', 'T0003', 'sfsaf', 'trainer', 'Trainer Request Accepted', 'Your trainer request has been accepted by sfsaf.', 'normal', '2026-09-30 15:16:26', NULL, 0);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (100, 'M2003', 'T0003', 'sfsaf', 'trainer', 'Trainer Request Accepted', 'Your trainer request has been accepted by sfsaf.', 'normal', '2026-09-30 15:16:27', NULL, 0);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (101, 'M2005', 'T0003', 'sfsaf', 'trainer', 'Trainer Request Accepted', 'Your trainer request has been accepted by sfsaf.', 'normal', '2026-09-30 15:16:28', NULL, 0);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (102, 'M2004', 'T0003', 'sfsaf', 'trainer', 'Trainer Request Accepted', 'Your trainer request has been accepted by sfsaf.', 'normal', '2026-09-30 15:16:29', NULL, 0);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (103, 'M2007', 'T0003', 'sfsaf', 'trainer', 'Trainer Request Accepted', 'Your trainer request has been accepted by sfsaf.', 'normal', '2026-09-30 15:16:30', NULL, 0);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (104, 'M2006', 'T0003', 'sfsaf', 'trainer', 'Trainer Request Accepted', 'Your trainer request has been accepted by sfsaf.', 'normal', '2026-09-30 15:16:30', NULL, 0);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (105, 'M2008', 'T0003', 'sfsaf', 'trainer', 'Trainer Request Accepted', 'Your trainer request has been accepted by sfsaf.', 'normal', '2026-09-30 15:16:31', NULL, 0);
INSERT INTO `messages` (`id`, `user_id`, `sender_id`, `sender_name`, `sender_role`, `title`, `message`, `reason`, `created_at`, `receiver_role`, `is_read`) VALUES (106, 'M9999', 'T0003', 'sfsaf', 'trainer', 'Trainer Request Accepted', 'Your trainer request has been accepted by sfsaf.', 'normal', '2026-09-30 15:16:31', NULL, 0);


-- --------------------------------------------------
-- TABLE: password_reset_otps
-- --------------------------------------------------

DROP TABLE IF EXISTS `password_reset_otps`;
CREATE TABLE `password_reset_otps` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(10) NOT NULL,
  `otp_hash` varchar(64) NOT NULL,
  `expires_at` datetime NOT NULL,
  `attempts` int NOT NULL DEFAULT '0',
  `used` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_password_reset_user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `password_reset_otps` (`id`, `user_id`, `otp_hash`, `expires_at`, `attempts`, `used`, `created_at`) VALUES (8, 'M0012', 'c9cadc9c0719d1198f8e816756337108d88dd5bf553bdd7ffeeb322aeba52b79', '2026-08-15 11:20:26', 0, 1, '2026-08-15 11:15:26');
INSERT INTO `password_reset_otps` (`id`, `user_id`, `otp_hash`, `expires_at`, `attempts`, `used`, `created_at`) VALUES (9, 'M0012', '51f2ff07a9f3bbbe31ce0dc24a7018da89b48e14e707f4e3a60e35569af35dc8', '2026-08-15 11:21:35', 0, 1, '2026-08-15 11:16:34');
INSERT INTO `password_reset_otps` (`id`, `user_id`, `otp_hash`, `expires_at`, `attempts`, `used`, `created_at`) VALUES (10, 'M0012', '3a45081f4e87a8ea387158c0fa8e9995dd0bf9be1c7294469a770cffefa29cd1', '2026-08-15 11:43:50', 0, 1, '2026-08-15 11:38:50');
INSERT INTO `password_reset_otps` (`id`, `user_id`, `otp_hash`, `expires_at`, `attempts`, `used`, `created_at`) VALUES (11, 'M0012', 'f02c66e48577feac80bea2f8ff49724c257621bb1eb17907a24b4161cfb69231', '2026-08-15 11:44:51', 0, 1, '2026-08-15 11:39:50');
INSERT INTO `password_reset_otps` (`id`, `user_id`, `otp_hash`, `expires_at`, `attempts`, `used`, `created_at`) VALUES (12, 'M0012', 'b9bab2173e54acf2657a55e8f7c358b421a8c24ab2c6e526472baf7f29906b1f', '2026-08-15 11:50:49', 1, 1, '2026-08-15 11:45:49');
INSERT INTO `password_reset_otps` (`id`, `user_id`, `otp_hash`, `expires_at`, `attempts`, `used`, `created_at`) VALUES (13, 'M0012', 'f52296b31f0cfaf361b6054959e2d66b0a0276f3cd13a0eb9b2cc1f82df778ea', '2026-08-15 11:57:42', 0, 1, '2026-08-15 11:52:42');
INSERT INTO `password_reset_otps` (`id`, `user_id`, `otp_hash`, `expires_at`, `attempts`, `used`, `created_at`) VALUES (14, 'M0012', '03b98d120dad10c3a83640d9dd6b223eefa9be35879f1c08bb2641b4a4eaad90', '2026-08-15 11:58:07', 0, 1, '2026-08-15 11:53:06');
INSERT INTO `password_reset_otps` (`id`, `user_id`, `otp_hash`, `expires_at`, `attempts`, `used`, `created_at`) VALUES (15, 'M0012', 'c75078b23db11d9821b2e3e8fa07fc66b2852cff59a8e2350cb3fb0b22e96dce', '2026-08-15 11:58:33', 0, 1, '2026-08-15 11:53:32');
INSERT INTO `password_reset_otps` (`id`, `user_id`, `otp_hash`, `expires_at`, `attempts`, `used`, `created_at`) VALUES (16, 'M0012', 'ed698cff1b4947db5435c72185d2997834cca0c442fd946e9e1df3a1eec6b689', '2026-08-15 12:00:27', 0, 1, '2026-08-15 11:55:26');
INSERT INTO `password_reset_otps` (`id`, `user_id`, `otp_hash`, `expires_at`, `attempts`, `used`, `created_at`) VALUES (17, 'M0012', '7ecec702d0e7c3879f47638736ebf6388c97f910eb9c17e0bb7f6db78c64b182', '2026-08-15 12:09:16', 0, 1, '2026-08-15 12:04:15');
INSERT INTO `password_reset_otps` (`id`, `user_id`, `otp_hash`, `expires_at`, `attempts`, `used`, `created_at`) VALUES (18, 'M0012', 'd8d5c374f7c10ca08c609a1cbc6afdc2af7287ee7e3f8dfaa18ecb32d4d40d8e', '2026-08-15 12:09:57', 0, 1, '2026-08-15 12:04:56');
INSERT INTO `password_reset_otps` (`id`, `user_id`, `otp_hash`, `expires_at`, `attempts`, `used`, `created_at`) VALUES (19, 'M0012', '596af8ffa3960d5bc9c5019dc761106137c3e05ecd3e943f1597d4262598886b', '2026-08-15 12:11:40', 1, 1, '2026-08-15 12:06:40');
INSERT INTO `password_reset_otps` (`id`, `user_id`, `otp_hash`, `expires_at`, `attempts`, `used`, `created_at`) VALUES (20, 'M0012', '2513af0b14193efae997c8ee2607a82654ac3dfcbc16156ba8be82c9f30d500c', '2026-08-15 12:16:01', 0, 1, '2026-08-15 12:11:01');
INSERT INTO `password_reset_otps` (`id`, `user_id`, `otp_hash`, `expires_at`, `attempts`, `used`, `created_at`) VALUES (21, 'M0012', '08992831405b9675b1d4183482e6582a7ea54206c5a70e4cca38500fd9f52616', '2026-08-15 12:16:18', 1, 1, '2026-08-15 12:11:17');
INSERT INTO `password_reset_otps` (`id`, `user_id`, `otp_hash`, `expires_at`, `attempts`, `used`, `created_at`) VALUES (22, 'M0012', 'f8e782e917ea0525db14c4f3955926d104cf1c8e2097162ed3c547ccbde28c9f', '2026-08-15 12:17:28', 1, 1, '2026-08-15 12:12:27');
INSERT INTO `password_reset_otps` (`id`, `user_id`, `otp_hash`, `expires_at`, `attempts`, `used`, `created_at`) VALUES (23, 'M0012', 'de4fc7831a08e6d52c3a899511b81bedd52074c548a2933abd5fdfefd11013ba', '2026-08-15 12:18:57', 0, 1, '2026-08-15 12:13:56');
INSERT INTO `password_reset_otps` (`id`, `user_id`, `otp_hash`, `expires_at`, `attempts`, `used`, `created_at`) VALUES (24, 'M0012', '54090803f6a190989c0ca04d7c2bc7d116966e40fd43138a55ac501db2c9f553', '2026-08-15 12:20:00', 1, 1, '2026-08-15 12:14:59');
INSERT INTO `password_reset_otps` (`id`, `user_id`, `otp_hash`, `expires_at`, `attempts`, `used`, `created_at`) VALUES (25, 'M0012', '9ede92ada3456d4572870d412766ce2d83a798dc2d23c216c83b897522a62075', '2026-08-15 12:21:51', 0, 1, '2026-08-15 12:16:51');
INSERT INTO `password_reset_otps` (`id`, `user_id`, `otp_hash`, `expires_at`, `attempts`, `used`, `created_at`) VALUES (26, 'M0012', '737cb600aa5a648a0c20178d8d959441f30092874de4b4b9d2c499bf6eb09e7b', '2026-08-15 12:23:19', 4, 1, '2026-08-15 12:18:18');
INSERT INTO `password_reset_otps` (`id`, `user_id`, `otp_hash`, `expires_at`, `attempts`, `used`, `created_at`) VALUES (27, 'M0012', '3479ad0127d9fb0f15ddb6f11c26610c8a5d69edb55b43a83f2a68b6a7983e81', '2026-08-15 12:25:03', 0, 1, '2026-08-15 12:20:02');
INSERT INTO `password_reset_otps` (`id`, `user_id`, `otp_hash`, `expires_at`, `attempts`, `used`, `created_at`) VALUES (28, 'M0012', '14aa76a40c19fb805e9112dfdf545c6e522516485636ecd0b7d2b0c972242e7b', '2026-08-15 12:36:03', 0, 1, '2026-08-15 12:31:02');


-- --------------------------------------------------
-- TABLE: payments
-- --------------------------------------------------

DROP TABLE IF EXISTS `payments`;
CREATE TABLE `payments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `payment_type` varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `trainer_id` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `paid_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `source_payment_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_source_payment_id` (`source_payment_id`),
  KEY `idx_user_payment` (`user_id`,`payment_type`)
) ENGINE=InnoDB AUTO_INCREMENT=247 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (37, 'M0001', 'MONTHLY', 0.00, NULL, '2026-03-24 20:34:09', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (38, 'W0002', 'WALKIN', 0.00, NULL, '2026-03-25 09:28:04', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (43, 'W0002', 'WALKIN', 0.00, NULL, '2026-03-25 09:59:39', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (44, 'W0002', 'WALKIN', 0.00, NULL, '2026-03-25 09:59:57', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (50, 'W0002', 'WALKIN', 0.00, NULL, '2026-03-25 11:39:15', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (61, '\\M0001', 'MONTHLY', 0.00, NULL, '2026-04-01 13:41:40', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (62, 'M0001', 'MEMBERSHIP', 0.00, NULL, '2026-04-01 13:46:34', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (63, 'M0001', 'LOCKER_OVERTIME', -78.00, NULL, '2026-04-01 14:58:10', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (64, 'M0001', 'LOCKER_OVERTIME', -86.00, NULL, '2026-04-01 15:07:42', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (65, 'M0001', 'MEMBERSHIP', 0.00, NULL, '2026-04-06 13:13:10', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (66, 'M0001', 'MONTHLY', 0.00, NULL, '2026-04-06 13:14:39', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (67, 'M0001', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-04-06 13:36:11', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (69, 'W0002', 'WALKIN', 0.00, NULL, '2026-04-12 15:39:36', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (70, 'M0002', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-04-12 15:41:56', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (71, 'M0002', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-04-12 15:57:53', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (83, 'M0001', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-05-02 10:55:10', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (85, 'M0001', 'DAILY', 0.00, NULL, '2026-05-03 05:47:19', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (91, 'M0001', 'MONTHLY', 0.00, NULL, '2026-05-17 11:35:51', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (92, 'M0001', 'MONTHLY', 0.00, NULL, '2026-05-17 11:51:16', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (93, 'M0001', 'MONTHLY', 0.00, NULL, '2026-05-17 11:54:58', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (94, 'M0001', 'MONTHLY', 0.00, NULL, '2026-05-17 12:09:24', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (95, 'M0001', 'MONTHLY', 0.00, NULL, '2026-05-17 12:13:55', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (96, 'M0002', 'MONTHLY', 0.00, NULL, '2026-05-17 12:15:56', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (97, 'M0003', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-05-17 13:27:06', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (98, 'M0003', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-05-17 13:51:48', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (99, 'M0004', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-05-17 14:06:33', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (100, 'M0001', 'MEMBERSHIP-DAILY', 0.00, NULL, '2026-05-17 19:19:50', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (102, 'M0001', 'DAILY', 0.00, NULL, '2026-05-18 17:27:12', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (103, 'M0001', 'MONTHLY', 0.00, NULL, '2026-05-18 17:28:59', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (104, 'M0002', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-05-18 17:32:59', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (105, 'M0003', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-05-18 17:42:46', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (108, 'M0004', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-05-20 17:22:35', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (109, 'W0002', 'WALKIN', 0.00, NULL, '2026-05-20 17:23:39', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (110, 'M0005', 'MEMBERSHIP-DAILY', 0.00, NULL, '2026-05-21 10:09:24', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (111, 'M0005', 'MEMBERSHIP-DAILY', 0.00, NULL, '2026-05-21 10:18:33', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (112, 'W0002', 'WALKIN', 0.00, NULL, '2026-05-21 18:57:22', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (113, 'M0006', 'MEMBERSHIP-DAILY', 0.00, NULL, '2026-05-21 19:06:43', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (114, 'M0001', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-05-21 19:27:06', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (115, 'M0001', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-05-21 19:38:01', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (116, 'M0002', 'MEMBERSHIP-DAILY', 0.00, NULL, '2026-05-21 19:43:17', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (117, 'M0002', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-05-21 19:46:32', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (118, 'M0003', 'MEMBERSHIP-DAILY', 0.00, NULL, '2026-05-21 19:54:18', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (119, 'M0004', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-05-21 20:25:01', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (120, 'M0004', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-05-21 20:35:42', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (124, 'M0005', 'MEMBERSHIP-DAILY', 0.00, NULL, '2026-05-22 09:19:09', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (125, 'M0001', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-05-22 09:49:45', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (127, 'M0002', 'MEMBERSHIP', 0.00, NULL, '2026-05-22 13:15:07', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (128, 'M0004', 'MEMBERSHIP-DAILY', 0.00, NULL, '2026-05-22 13:23:22', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (129, 'M0005', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-06-03 18:54:23', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (130, 'M0005', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-06-03 19:15:41', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (131, 'M0005', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-06-03 19:21:22', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (135, 'M0005', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-06-06 12:14:37', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (136, 'M0007', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-06-06 14:21:04', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (137, 'M0007', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-06-06 14:25:12', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (138, 'M0001', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-06-06 14:33:33', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (139, 'M0002', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-06-06 14:44:05', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (140, 'M0001', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-06-06 15:14:07', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (141, 'M0002', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-06-06 15:22:10', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (142, 'M0003', 'MEMBERSHIP-DAILY', 0.00, NULL, '2026-06-06 15:30:38', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (143, 'M0001', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-06-06 16:16:07', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (144, 'M0002', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-06-06 16:17:28', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (145, 'M0004', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-06-06 17:51:45', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (146, 'W00001', 'WALKIN', 0.00, NULL, '2026-06-07 08:34:41', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (148, 'M0004', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-06-07 10:01:33', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (149, 'M0003', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-06-07 12:05:35', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (150, 'M0002', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-06-07 12:05:44', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (151, 'M0004', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-06-07 13:10:44', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (152, 'M0005', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-06-07 15:15:53', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (154, 'M0006', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-06-07 19:37:53', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (155, 'M0007', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-06-07 19:41:25', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (156, 'M0008', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-06-07 20:25:16', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (157, 'M0009', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-06-07 20:29:31', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (158, 'W0002', 'WALKIN', 0.00, NULL, '2026-06-08 09:36:42', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (159, 'M0010', 'MEMBERSHIP-MONTHLY', 0.00, NULL, '2026-06-08 11:36:59', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (163, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (164, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (165, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (166, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (167, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (168, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (169, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (170, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (171, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (172, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (173, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (174, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (175, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (176, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (177, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (178, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (179, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (180, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (181, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (182, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (183, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (184, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (185, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (186, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (187, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (188, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (189, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (190, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (191, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (192, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (193, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (194, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (195, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (196, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (197, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (198, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (199, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (200, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (201, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (202, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (203, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (204, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (205, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (206, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (207, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (208, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (209, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (210, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (211, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (212, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (213, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (214, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (215, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (216, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (217, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (218, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (219, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (220, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (221, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (222, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (223, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (224, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (225, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (226, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (227, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (228, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (229, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (230, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (231, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (232, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (233, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (234, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (235, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (236, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (237, 'M0001', 'trainer_fee', 600.00, 'T0005', '2026-10-04 20:00:00', NULL);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (238, 'M0004', 'membership_fee', 600.00, NULL, NULL, 39);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (239, 'M0004', 'access_fee', 500.00, NULL, NULL, 40);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (240, 'M0004', 'trainer_fee', 3000.00, 'T0004', NULL, 41);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (241, 'M0005', 'membership_fee', 600.00, NULL, NULL, 42);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (242, 'M0005', 'access_fee', 500.00, NULL, NULL, 43);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (243, 'M0005', 'trainer_fee', 100.00, 'T0004', NULL, 44);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (244, 'M0006', 'membership_fee', 600.00, NULL, NULL, 45);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (245, 'M0006', 'access_fee', 500.00, NULL, NULL, 46);
INSERT INTO `payments` (`id`, `user_id`, `payment_type`, `amount`, `trainer_id`, `paid_at`, `source_payment_id`) VALUES (246, 'M0006', 'trainer_fee', 3000.00, 'T0004', NULL, 47);


-- --------------------------------------------------
-- TABLE: pending_members
-- --------------------------------------------------

DROP TABLE IF EXISTS `pending_members`;
CREATE TABLE `pending_members` (
  `id` int NOT NULL AUTO_INCREMENT,
  `account_id` int NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `status` enum('PENDING','ENROLLING','COMPLETED') NOT NULL DEFAULT 'PENDING',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `account_id` (`account_id`),
  CONSTRAINT `pending_members_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `user_accounts` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `pending_members` (`id`, `account_id`, `full_name`, `phone_number`, `status`, `created_at`) VALUES (27, 79, 'Aldrin', '09123456987', 'COMPLETED', '2026-08-17 10:29:48');
INSERT INTO `pending_members` (`id`, `account_id`, `full_name`, `phone_number`, `status`, `created_at`) VALUES (29, 102, 'aldrin delavega', '09913354822', 'PENDING', '2026-09-22 02:49:40');


-- --------------------------------------------------
-- TABLE: plan_day_body_parts
-- --------------------------------------------------

DROP TABLE IF EXISTS `plan_day_body_parts`;
CREATE TABLE `plan_day_body_parts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `plan_day_id` int NOT NULL,
  `body_part` varchar(100) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_plan_day_body_part` (`plan_day_id`,`body_part`),
  CONSTRAINT `fk_body_parts_plan_day` FOREIGN KEY (`plan_day_id`) REFERENCES `plan_days` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=128 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (1, 1, 'Chest', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (2, 2, 'Back', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (3, 3, 'Shoulders', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (4, 4, 'Biceps', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (5, 4, 'Triceps', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (6, 5, 'Legs', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (7, 6, 'Chest', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (8, 6, 'Back', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (9, 6, 'Shoulders', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (10, 6, 'Arms', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (11, 6, 'Legs', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (17, 8, 'Chest', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (18, 8, 'Back', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (19, 8, 'Shoulders', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (20, 8, 'Arms', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (21, 8, 'Legs', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (22, 9, 'Chest', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (23, 9, 'Back', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (24, 9, 'Shoulders', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (25, 9, 'Biceps', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (26, 9, 'Triceps', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (27, 10, 'Legs', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (34, 13, 'Full Body', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (35, 13, 'Cardio', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (36, 14, 'Cardio', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (37, 14, 'Core', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (38, 15, 'Full Body', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (39, 16, 'Cardio', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (40, 16, 'Core', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (41, 17, 'Full Body', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (42, 17, 'Cardio', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (43, 18, 'Cardio', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (44, 19, 'Core', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (45, 19, 'Cardio', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (46, 20, 'Full Body', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (47, 21, 'Cardio', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (48, 22, 'Core', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (49, 22, 'Cardio', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (50, 23, 'Full Body', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (51, 23, 'Conditioning', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (52, 24, 'Cardio', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (53, 25, 'Core', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (54, 25, 'Conditioning', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (55, 26, 'Cardio', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (56, 27, 'Full Body', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (57, 27, 'Conditioning', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (58, 28, 'Chest', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (59, 28, 'Shoulders', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (60, 28, 'Triceps', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (61, 29, 'Back', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (62, 29, 'Biceps', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (63, 30, 'Legs', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (64, 31, 'Chest', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (65, 31, 'Shoulders', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (66, 31, 'Triceps', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (67, 32, 'Back', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (68, 32, 'Biceps', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (69, 33, 'Legs', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (70, 34, 'Chest', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (71, 34, 'Back', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (72, 35, 'Shoulders', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (73, 35, 'Biceps', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (74, 35, 'Triceps', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (75, 36, 'Legs', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (76, 37, 'Chest', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (77, 37, 'Back', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (78, 38, 'Shoulders', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (79, 38, 'Biceps', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (80, 38, 'Triceps', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (81, 39, 'Legs', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (82, 40, 'Chest', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (83, 40, 'Back', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (84, 40, 'Shoulders', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (85, 40, 'Biceps', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (86, 40, 'Triceps', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (87, 41, 'Legs', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (88, 42, 'Chest', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (89, 42, 'Back', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (90, 42, 'Shoulders', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (91, 42, 'Biceps', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (92, 42, 'Triceps', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (93, 43, 'Legs', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (94, 44, 'Chest', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (95, 45, 'Back', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (96, 46, 'Shoulders', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (97, 47, 'Biceps', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (98, 47, 'Triceps', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (99, 48, 'Legs', 1);
INSERT INTO `plan_day_body_parts` (`id`, `plan_day_id`, `body_part`, `active`) VALUES (100, 49, 'Chest', 1);


-- --------------------------------------------------
-- TABLE: plan_days
-- --------------------------------------------------

DROP TABLE IF EXISTS `plan_days`;
CREATE TABLE `plan_days` (
  `id` int NOT NULL AUTO_INCREMENT,
  `plan_id` int NOT NULL,
  `day_number` int NOT NULL,
  `day_name` varchar(100) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_plan_day` (`plan_id`,`day_number`),
  CONSTRAINT `fk_plan_days_plan` FOREIGN KEY (`plan_id`) REFERENCES `program_plans` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=138 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (1, 1, 1, 'Chest', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (2, 1, 2, 'Back', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (3, 1, 3, 'Shoulders', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (4, 1, 4, 'Arms', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (5, 1, 5, 'Legs', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (6, 2, 1, 'Full Body', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (7, 2, 2, 'Rest', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (8, 2, 3, 'Full Body', 0);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (9, 3, 1, 'Upper Body', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (10, 3, 2, 'Lower Body', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (11, 3, 3, 'Rest', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (13, 4, 1, 'Full Body + Cardio', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (14, 4, 2, 'Cardio + Core', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (15, 4, 3, 'Full Body', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (16, 4, 4, 'Cardio + Core', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (17, 4, 5, 'Full Body + Cardio', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (18, 5, 1, 'Cardio', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (19, 5, 2, 'Core + Cardio', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (20, 5, 3, 'Full Body', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (21, 5, 4, 'Cardio', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (22, 5, 5, 'Core + Cardio', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (23, 6, 1, 'Full Body Conditioning', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (24, 6, 2, 'Cardio', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (25, 6, 3, 'Core + Conditioning', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (26, 6, 4, 'Cardio', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (27, 6, 5, 'Full Body Conditioning', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (28, 7, 1, 'Push', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (29, 7, 2, 'Pull', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (30, 7, 3, 'Legs', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (31, 7, 4, 'REST', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (32, 7, 5, 'Pull', 0);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (33, 7, 6, 'Legs', 0);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (34, 8, 1, 'Chest + Back', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (35, 8, 2, 'Shoulders + Arms', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (36, 8, 3, 'Legs', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (37, 8, 4, 'REST', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (38, 8, 5, 'Shoulders + Arms', 0);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (39, 8, 6, 'Legs', 0);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (40, 9, 1, 'Upper Body', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (41, 9, 2, 'Lower Body', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (42, 9, 3, 'REST', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (43, 9, 4, 'Lower Body', 0);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (44, 10, 1, 'Chest', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (45, 10, 2, 'Back', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (46, 10, 3, 'Shoulders', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (47, 10, 4, 'Arms', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (48, 10, 5, 'Legs', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (49, 11, 1, 'Upper Strength', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (50, 11, 2, 'Lower Strength', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (51, 11, 3, 'REST', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (52, 11, 4, 'Lower Strength', 0);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (53, 12, 1, 'Full Body Strength', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (54, 12, 2, 'REST', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (55, 12, 3, 'Full Body Strength', 0);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (56, 13, 1, 'Push Strength', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (57, 13, 2, 'Pull Strength', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (58, 13, 3, 'Legs Strength', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (59, 13, 4, 'REST', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (60, 13, 5, 'Pull Strength', 0);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (61, 13, 6, 'Legs Strength', 0);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (62, 14, 1, 'Upper Strength', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (63, 14, 2, 'Lower Strength', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (64, 14, 3, 'Conditioning', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (65, 14, 4, 'REST', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (66, 14, 5, 'Lower Strength', 0);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (67, 14, 6, 'Conditioning', 0);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (128, 1, 6, 'Rest', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (129, 6, 6, 'REST', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (130, 5, 6, 'REST', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (131, 4, 6, 'REST', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (132, 6, 7, 'REST', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (133, 5, 7, 'REST', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (134, 4, 7, 'REST', 1);
INSERT INTO `plan_days` (`id`, `plan_id`, `day_number`, `day_name`, `active`) VALUES (137, 10, 6, 'REST', 1);


-- --------------------------------------------------
-- TABLE: program_plans
-- --------------------------------------------------

DROP TABLE IF EXISTS `program_plans`;
CREATE TABLE `program_plans` (
  `id` int NOT NULL AUTO_INCREMENT,
  `program_id` int NOT NULL,
  `plan_name` varchar(100) NOT NULL,
  `description` text,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_program_plan` (`program_id`,`plan_name`),
  CONSTRAINT `fk_program_plans_program` FOREIGN KEY (`program_id`) REFERENCES `programs` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `program_plans` (`id`, `program_id`, `plan_name`, `description`, `active`, `created_at`) VALUES (1, 4, 'Bro Split', 'Balanced body-part split for general fitness.', 1, '2026-09-24 16:30:37');
INSERT INTO `program_plans` (`id`, `program_id`, `plan_name`, `description`, `active`, `created_at`) VALUES (2, 4, 'Full Body', 'Full-body training structure for overall fitness.', 1, '2026-09-24 16:30:37');
INSERT INTO `program_plans` (`id`, `program_id`, `plan_name`, `description`, `active`, `created_at`) VALUES (3, 4, 'Upper / Lower', 'Balanced upper-body and lower-body training.', 1, '2026-09-24 16:30:37');
INSERT INTO `program_plans` (`id`, `program_id`, `plan_name`, `description`, `active`, `created_at`) VALUES (4, 2, 'Cardio & Full Body', 'Combination of cardio and full-body training.', 1, '2026-09-24 16:30:37');
INSERT INTO `program_plans` (`id`, `program_id`, `plan_name`, `description`, `active`, `created_at`) VALUES (5, 2, 'Cardio / Core', 'Cardio and core-focused training structure.', 1, '2026-09-24 16:30:37');
INSERT INTO `program_plans` (`id`, `program_id`, `plan_name`, `description`, `active`, `created_at`) VALUES (6, 2, 'Conditioning', 'Conditioning-focused training for weight loss.', 1, '2026-09-24 16:30:37');
INSERT INTO `program_plans` (`id`, `program_id`, `plan_name`, `description`, `active`, `created_at`) VALUES (7, 1, 'PPL', 'Push, Pull, Legs bodybuilding split.', 1, '2026-09-24 16:30:37');
INSERT INTO `program_plans` (`id`, `program_id`, `plan_name`, `description`, `active`, `created_at`) VALUES (8, 1, 'Arnold Split', 'Chest/Back, Shoulders/Arms and Legs split.', 1, '2026-09-24 16:30:37');
INSERT INTO `program_plans` (`id`, `program_id`, `plan_name`, `description`, `active`, `created_at`) VALUES (9, 1, 'Upper / Lower', 'Upper-body and lower-body muscle-building split.', 1, '2026-09-24 16:30:37');
INSERT INTO `program_plans` (`id`, `program_id`, `plan_name`, `description`, `active`, `created_at`) VALUES (10, 1, 'Bro Split', 'Body-part focused muscle-building split.', 1, '2026-09-24 16:30:37');
INSERT INTO `program_plans` (`id`, `program_id`, `plan_name`, `description`, `active`, `created_at`) VALUES (11, 3, 'Upper / Lower Strength', 'Strength-focused upper and lower body split.', 1, '2026-09-24 16:30:37');
INSERT INTO `program_plans` (`id`, `program_id`, `plan_name`, `description`, `active`, `created_at`) VALUES (12, 3, 'Full Body Strength', 'Full-body strength training structure.', 1, '2026-09-24 16:30:37');
INSERT INTO `program_plans` (`id`, `program_id`, `plan_name`, `description`, `active`, `created_at`) VALUES (13, 3, 'PPL Strength', 'Push, Pull and Legs strength-focused split.', 1, '2026-09-24 16:30:37');
INSERT INTO `program_plans` (`id`, `program_id`, `plan_name`, `description`, `active`, `created_at`) VALUES (14, 3, 'Strength + Conditioning', 'Strength training combined with conditioning.', 1, '2026-09-24 16:30:37');


-- --------------------------------------------------
-- TABLE: programs
-- --------------------------------------------------

DROP TABLE IF EXISTS `programs`;
CREATE TABLE `programs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `program_name` varchar(100) NOT NULL,
  `description` text,
  `duration_days` int NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_program_name` (`program_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

