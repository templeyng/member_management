# 瑜伽馆会员管理系统 - SDD 软件设计文档
**文档编号**: YOGA-003
**版本**: v2.0
**创建日期**: 2026-04-03
**更新日期**: 2026-04-05
**负责人**: 开发

---

## 1. 引言

### 1.1 编写目的
本文档描述瑜伽馆会员管理系统软件架构设计、模块划分、接口定义及数据库设计，为开发实现提供技术指导。

### 1.2 适用范围
本文档适用于系统的开发、测试及维护人员。

### 1.3 参考资料
- 《需求规格说明书》(YOGA-002)
- 《项目立项简报》(YOGA-001)

---

## 2. 系统架构

### 2.1 整体架构
采用前后端分离的 B/S 架构，三层结构：

```
┌─────────────────────────────────────────┐
│ 前端展示层                               │
│ (Vue 3 / React SPA 应用)                   │
└─────────────────┬───────────────────────┘
                  │ HTTP/HTTPS
┌─────────────────▼───────────────────────┐
│ 业务逻辑层                               │
│ (RESTful API 服务)                        │
└─────────────────┬───────────────────────┘
                  │ JDBC/ORM
┌─────────────────▼───────────────────────┐
│ 数据访问层                               │
│ (关系型数据库 + 文件存储)                   │
└─────────────────────────────────────────┘
```

### 2.2 技术栈（待开发确认）
| 层次 | 技术选型（候选方案） |
|------|----------------------|
| 前端 | Vue 3 + Element Plus / React + Ant Design |
| 后端 | Spring Boot / Node.js (NestJS) / Python (FastAPI) |
| 数据库 | MySQL 8.0 / PostgreSQL |
| 缓存 | Redis |
| 文件存储 | 本地存储 / 阿里云 OSS / 腾讯云 COS |
| AI 服务 | 自建模型 / 调用大模型 API |
| 部署 | Docker + Nginx |

---

## 3. 模块设计

### 3.1 模块划分
```
瑜伽馆会员管理系统
├── 会员管理模块 (member)
│   ├── 会员档案管理
│   ├── 会员标签管理
│   └── 会员池管理
├── 课程出勤模块 (course)
│   ├── 课程管理
│   ├── 预约管理
│   └── 出勤跟踪
├── 效果对比模块 (progress)
│   ├── 对比图管理
│   └── 身体数据记录
├── 续课管理模块 (renewal)
│   ├── 课程包管理
│   └── 续课跟踪
├── 反馈满意度模块 (feedback)
│   ├── 反馈记录
│   └── 满意度调查
├── AI 分析模块 (ai)
│   ├── 会员画像分析
│   ├── 智能建议生成
│   └── 提醒中心
├── 数据报表模块 (report)
│   ├── 会员报表
│   ├── 课程报表
│   └── 经营报表
└── 系统管理模块 (system)
    ├── 用户管理
    ├── 权限管理
    └── 系统配置
```

### 3.2 模块详细设计

#### 3.2.1 会员管理模块
**功能清单**:
- 会员 CRUD 操作
- 会员标签管理
- 会员状态流转（活跃/沉睡/流失）
- 会员分级管理

**核心实体**:
- Member（会员）
- MemberTag（会员标签）
- MemberLevel（会员等级）

#### 3.2.2 课程出勤模块
**功能清单**:
- 课程类型管理
- 课程时间安排
- 预约管理（预约/取消/改签）
- 签到/签退
- 出勤统计

**核心实体**:
- Course（课程）
- CourseType（课程类型）
- Appointment（预约）
- Attendance（出勤记录）

#### 3.2.3 效果对比模块
**功能清单**:
- 对比图上传与管理
- 对比图时间线展示
- 身体数据记录（体重、体脂等）
- 数据趋势图表

**核心实体**:
- ProgressPhoto（对比图）
- BodyData（身体数据）

#### 3.2.4 续课管理模块
**功能清单**:
- 课程套餐定义
- 课时记录与扣减
- 到期提醒
- 续课记录

**核心实体**:
- CoursePackage（课程包）
- Renewal（续课记录）

#### 3.2.5 反馈满意度模块
**功能清单**:
- 反馈录入与分类
- 反馈处理跟踪
- 满意度问卷
- 满意度统计

**核心实体**:
- Feedback（反馈）
- SatisfactionSurvey（满意度调查）

#### 3.2.6 AI 分析模块
**功能清单**:
- 会员行为分析
- 会员价值分层（RFM 模型）
- 流失风险预测
- 智能建议生成
- 提醒任务调度

**核心实体**:
- MemberProfile（会员画像）
- AISuggestion（AI 建议）
- ReminderTask（提醒任务）

#### 3.2.7 数据报表模块
**功能清单**:
- 会员增长趋势
- 出勤率统计
- 续课率统计
- 营收分析
- 满意度趋势

#### 3.2.8 系统管理模块
**功能清单**:
- 用户增删改查
- 角色权限配置
- 数据字典管理
- 操作日志记录

**核心实体**:
- User（用户）
- Role（角色）
- Permission（权限）
- Dict（字典）
- OperationLog（操作日志）

---

## 4. 数据库设计

### 4.1 ER 图概览
```
User ──< UserRole >── Role ──< RolePermission >── Permission
│
├──< Member >──< MemberTag
│   ├──< ProgressPhoto
│   ├──< BodyData
│   ├──< Appointment >── Course
│   ├──< Attendance
│   ├──< Feedback
│   └──< CoursePackage >── Renewal
│
└──< AISuggestion
└──< ReminderTask
```

### 4.2 核心表结构

#### 用户表 (sys_user)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键 |
| username | VARCHAR(50) | 用户名 |
| password | VARCHAR(255) | 密码（加密） |
| real_name | VARCHAR(50) | 真实姓名 |
| email | VARCHAR(100) | 邮箱 |
| phone | VARCHAR(20) | 手机号 |
| status | TINYINT | 状态 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### 会员表 (t_member)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键 |
| name | VARCHAR(50) | 姓名 |
| gender | TINYINT | 性别 |
| birthday | DATE | 生日 |
| phone | VARCHAR(20) | 电话 |
| wechat | VARCHAR(50) | 微信号 |
| join_date | DATE | 入会日期 |
| expire_date | DATE | 到期日期 |
| level_id | BIGINT | 等级 ID |
| status | VARCHAR(20) | 状态（活跃/沉睡/流失） |
| tags | JSON | 标签列表 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### 课程表 (t_course)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键 |
| name | VARCHAR(100) | 课程名称 |
| type_id | BIGINT | 课程类型 ID |
| coach_id | BIGINT | 教练 ID |
| start_time | DATETIME | 开始时间 |
| end_time | DATETIME | 结束时间 |
| max_capacity | INT | 最大人数 |
| booked_count | INT | 已预约人数 |
| status | VARCHAR(20) | 状态 |

#### 预约表 (t_appointment)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键 |
| member_id | BIGINT | 会员 ID |
| course_id | BIGINT | 课程 ID |
| status | VARCHAR(20) | 状态（已预约/已签到/已取消/已完成） |
| book_time | DATETIME | 预约时间 |
| sign_in_time | DATETIME | 签到时间 |
| sign_out_time | DATETIME | 签退时间 |

#### 对比图表 (t_progress_photo)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键 |
| member_id | BIGINT | 会员 ID |
| photo_url | VARCHAR(255) | 图片 URL |
| photo_type | VARCHAR(20) | 类型（前/后） |
| take_date | DATE | 拍摄日期 |
| remark | VARCHAR(255) | 备注 |
| created_at | DATETIME | 创建时间 |

#### 身体数据表 (t_body_data)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键 |
| member_id | BIGINT | 会员 ID |
| weight | DECIMAL(5,2) | 体重 (kg) |
| body_fat | DECIMAL(5,2) | 体脂率 (%) |
| waist | DECIMAL(5,2) | 腰围 (cm) |
| measure_date | DATE | 测量日期 |
| remark | VARCHAR(255) | 备注 |

#### AI 建议表 (t_ai_suggestion)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键 |
| member_id | BIGINT | 会员 ID |
| suggestion_type | VARCHAR(50) | 建议类型 |
| content | TEXT | 建议内容 |
| priority | INT | 优先级 |
| status | VARCHAR(20) | 状态（待处理/已处理/已忽略） |
| generated_at | DATETIME | 生成时间 |

#### 提醒任务表 (t_reminder_task)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键 |
| member_id | BIGINT | 会员 ID |
| task_type | VARCHAR(50) | 提醒类型（生日/到期/沉睡/特殊日期） |
| task_date | DATE | 提醒日期 |
| content | TEXT | 提醒内容 |
| status | VARCHAR(20) | 状态（待发送/已发送/已忽略） |
| sent_at | DATETIME | 发送时间 |

---

## 5. 接口设计

### 5.1 会员管理接口
- `POST /api/members` - 创建会员
- `GET /api/members` - 查询会员列表
- `GET /api/members/{id}` - 获取会员详情
- `PUT /api/members/{id}` - 更新会员
- `DELETE /api/members/{id}` - 删除会员
- `POST /api/members/{id}/tags` - 添加标签
- `GET /api/members/{id}/progress` - 获取会员进度

### 5.2 课程管理接口
- `POST /api/courses` - 创建课程
- `GET /api/courses` - 查询课程列表
- `POST /api/courses/{id}/book` - 预约课程
- `POST /api/courses/{id}/cancel` - 取消预约
- `POST /api/courses/{id}/signin` - 签到
- `POST /api/courses/{id}/signout` - 签退

### 5.3 AI 分析接口
- `POST /api/ai/analyze` - 触发 AI 分析
- `GET /api/ai/suggestions` - 获取 AI 建议列表
- `PUT /api/ai/suggestions/{id}` - 更新建议状态
- `GET /api/ai/reminders` - 获取提醒列表

---

## 6. 技术约束

### 6.1 图片存储
- 对比图需考虑存储成本和加载速度
- 建议使用云存储（OSS/COS）+ CDN 加速
- 图片需压缩处理

### 6.2 AI 服务
- 可选方案：
  - 自建模型（需要训练数据和算力）
  - 调用大模型 API（如文心一言、通义千问等）
- 建议：初期调用 API，后期根据数据量考虑自建

### 6.3 安全性
- 敏感数据（手机号、微信）需加密存储
- 接口需做权限校验
- 操作日志完整记录

---

## 7. 待确认事项

- [ ] 技术栈最终选择
- [ ] 图片存储方案
- [ ] AI 服务选型
- [ ] 部署环境
- [ ] 是否需要小程序/公众号对接

---

*本文档将随项目进展持续更新*