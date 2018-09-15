/*
Navicat MySQL Data Transfer

Source Server         : Mysql_localhost
Source Server Version : 50528
Source Host           : 127.0.0.1:3306
Source Database       : python

Target Server Type    : MYSQL
Target Server Version : 50528
File Encoding         : 65001

Date: 2018-09-15 18:24:20
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for jianshu_30day
-- ----------------------------
DROP TABLE IF EXISTS `jianshu_30day`;
CREATE TABLE `jianshu_30day` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `author` varchar(255) DEFAULT NULL,
  `up_time` varchar(255) DEFAULT NULL,
  `word_num` int(11) DEFAULT NULL,
  `view_num` int(11) DEFAULT NULL,
  `comment_num` int(11) DEFAULT NULL,
  `like_num` int(11) DEFAULT NULL,
  `rewards_num` int(11) DEFAULT NULL,
  `article_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8;
