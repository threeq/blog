
-- ----------------------------
-- Table structure for class
-- ----------------------------
CREATE TABLE `class` (
  `c_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '班级 id，组件',
  `c_name` varchar(512) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '班级名称',
  `c_head_teacher` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '班主任名称',
  `c_start_time` date DEFAULT NULL COMMENT '开班日期',
  `c_end_time` date DEFAULT NULL COMMENT '结束日期',
  `c_status` int(11) NOT NULL COMMENT '班级状态【0：报名未开始，1：报名中，2：报名完成，3：已开学，4：已结业】',
  `c_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`c_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='班级信息表';

-- ----------------------------
-- Table structure for student
-- ----------------------------
CREATE TABLE `student` (
  `s_id` int(11) NOT NULL AUTO_INCREMENT COMMENT ' 学生 id',
  `s_name` varchar(64) NOT NULL COMMENT '学生名称',
  `s_sex` tinyint(4) DEFAULT NULL COMMENT '学生性别',
  `s_age` int(11) DEFAULT NULL COMMENT '学生年龄',
  `s_birthday` date NOT NULL COMMENT '学生生日',
  `s_addr` varchar(512) DEFAULT NULL COMMENT '学生地址',
  `s_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '加入时间',
  `s_status` int(11) DEFAULT NULL COMMENT '状态（0：禁用，1：可用）',
  PRIMARY KEY (`s_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COMMENT='学生信息表';

-- ----------------------------
-- Table structure for student_join_class
-- ----------------------------
CREATE TABLE `student_join_class` (
  `c_id` int(11) NOT NULL COMMENT '班级 id',
  `s_id` int(11) NOT NULL COMMENT '学生表',
  `cs_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '加入时间',
  PRIMARY KEY (`c_id`,`s_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学生班级关联表';

