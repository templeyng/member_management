# 客户关系管理系统 - SDD软件设计文档

**文档编号**: CRM-003  
**版本**: v1.0  
**创建日期**: 2026-04-03  
**负责人**: 私人助手（伊）

---

## 1. 引言

### 1.1 编写目的
本文档描述客户关系管理系统（CRM）的软件架构设计、模块划分、接口定义及数据库设计，为开发实现提供技术指导。

### 1.2 适用范围
本文档适用于CRM系统的开发、测试及维护人员。

### 1.3 参考资料
- 《需求规格说明书》(CRM-002)
- 《项目立项简报》(CRM-001)

---

## 2. 系统架构

### 2.1 整体架构
采用前后端分离的B/S架构，三层结构：

```
┌─────────────────────────────────────────┐
│            前端展示层                    │
│    (Vue.js / React SPA应用)             │
└─────────────────┬───────────────────────┘
                  │ HTTP/HTTPS
┌─────────────────▼───────────────────────┐
│            业务逻辑层                    │
│    (RESTful API服务)                    │
└─────────────────┬───────────────────────┘
                  │ JDBC/ORM
┌─────────────────▼───────────────────────┐
│            数据访问层                    │
│    (关系型数据库)                        │
└─────────────────────────────────────────┘
```

### 2.2 技术栈（待确认）

| 层次 | 技术选型（候选方案） |
|------|----------------------|
| 前端 | Vue 3 + Element Plus / React + Ant Design |
| 后端 | Spring Boot / Node.js (NestJS) |
| 数据库 | MySQL 8.0 / PostgreSQL |
| 缓存 | Redis |
| 消息队列 | RabbitMQ（可选） |
| 部署 | Docker + Nginx |

---

## 3. 模块设计

### 3.1 模块划分

```
CRM系统
├── 客户管理模块 (customer)
│   ├── 客户档案管理
│   ├── 联系人管理
│   └── 客户池管理
├── 销售管理模块 (sales)
│   ├── 线索管理
│   ├── 商机管理
│   └── 销售漏斗
├── 服务支持模块 (service)
│   ├── 工单管理
│   └── 服务记录
├── 数据报表模块 (report)
│   ├── 销售报表
│   └── 服务报表
└── 系统管理模块 (system)
    ├── 用户管理
    ├── 权限管理
    └── 系统配置
```

### 3.2 模块详细设计

#### 3.2.1 客户管理模块

**功能清单**:
- 客户CRUD操作
- 客户查重
- 客户分配/转移/回收
- 联系人管理
- 公海池/私海池切换

**核心实体**:
- Customer（客户）
- Contact（联系人）
- CustomerPool（客户池）

#### 3.2.2 销售管理模块

**功能清单**:
- 线索录入/导入/分配/转化
- 商机创建/跟进/阶段流转
- 销售漏斗可视化

**核心实体**:
- Lead（线索）
- Opportunity（商机）
- SalesStage（销售阶段）

#### 3.2.3 服务支持模块

**功能清单**:
- 工单创建/分配/处理/关闭
- 工单优先级管理
- 服务满意度记录

**核心实体**:
- Ticket（工单）
- ServiceRecord（服务记录）

#### 3.2.4 数据报表模块

**功能清单**:
- 销售业绩统计
- 商机转化分析
- 工单效率统计
- 图表可视化

#### 3.2.5 系统管理模块

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

### 4.1 ER图概览

```
User ──< UserRole >── Role ──< RolePermission >── Permission
  │
  └──< Customer >──< Contact
         │
         ├──< Opportunity
         │
         └──< Ticket >──< ServiceRecord
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

#### 客户表 (crm_customer)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键 |
| name | VARCHAR(100) | 客户名称 |
| industry | VARCHAR(50) | 行业 |
| scale | VARCHAR(20) | 规模 |
| address | VARCHAR(255) | 地址 |
| source | VARCHAR(50) | 来源 |
| status | VARCHAR(20) | 状态 |
| owner_id | BIGINT | 负责人ID |
| pool_type | VARCHAR(20) | 池类型(公海/私海) |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### 联系人表 (crm_contact)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键 |
| customer_id | BIGINT | 客户ID |
| name | VARCHAR(50) | 姓名 |
| position | VARCHAR(50) | 职位 |
| phone | VARCHAR(20) | 电话 |
| email | VARCHAR(100) | 邮箱 |
| is_primary | TINYINT | 是否主联系人 |
| created_at | DATETIME | 创建时间 |

#### 商机表 (crm_opportunity)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键 |
| customer_id | BIGINT | 客户ID |
| name | VARCHAR(100) | 商机名称 |
| stage | VARCHAR(50) | 阶段 |
| amount | DECIMAL(12,2) | 预计金额 |
| probability | INT | 成交概率 |
| expected_date | DATE | 预计成交日期 |
| owner_id | BIGINT | 负责人ID |
| status | VARCHAR(20) | 状态 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### 工单表 (crm_ticket)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键 |
| customer_id | BIGINT | 客户ID |
| title | VARCHAR(200) | 标题 |
| content | TEXT | 内容 |
| priority | VARCHAR(20) | 优先级 |
| status | VARCHAR(20) | 状态 |
| assignee_id | BIGINT | 处理人ID |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |
| closed_at | DATETIME | 关闭时间 |

---

## 5. 接口设计

### 5.1 接口规范

- 基础路径: `/api/v1`
- 认证方式: JWT Token
- 响应格式: JSON

**统一响应结构**:
```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

### 5.2 核心接口列表

#### 客户管理
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /customers | 客户列表 |
| GET | /customers/{id} | 客户详情 |
| POST | /customers | 新增客户 |
| PUT | /customers/{id} | 更新客户 |
| DELETE | /customers/{id} | 删除客户 |
| POST | /customers/{id}/transfer | 转移客户 |
| POST | /customers/{id}/recycle | 回收客户 |

#### 商机管理
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /opportunities | 商机列表 |
| GET | /opportunities/{id} | 商机详情 |
| POST | /opportunities | 新增商机 |
| PUT | /opportunities/{id} | 更新商机 |
| PUT | /opportunities/{id}/stage | 更新阶段 |
| DELETE | /opportunities/{id} | 删除商机 |

#### 工单管理
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /tickets | 工单列表 |
| GET | /tickets/{id} | 工单详情 |
| POST | /tickets | 新增工单 |
| PUT | /tickets/{id} | 更新工单 |
| PUT | /tickets/{id}/assign | 分配工单 |
| PUT | /tickets/{id}/close | 关闭工单 |

---

## 6. 验收标准

### 6.1 功能验收
- 所有需求规格说明书中的功能正常实现
- 接口返回数据正确
- 业务流程完整可运行

### 6.2 性能验收
- 页面响应时间 < 2秒
- 接口响应时间 < 500ms
- 支持100并发用户

### 6.3 安全验收
- 用户认证有效
- 权限控制正确
- 敏感数据已加密
- 无SQL注入、XSS等安全漏洞

---

## 7. 里程碑计划

| 阶段 | 交付物 | 时间 |
|------|--------|------|
| 设计确认 | SDD定稿 | 待定 |
| 开发阶段1 | 客户管理模块 | 待定 |
| 开发阶段2 | 销售管理模块 | 待定 |
| 开发阶段3 | 服务支持模块 | 待定 |
| 开发阶段4 | 报表+系统管理 | 待定 |
| 测试阶段 | 测试报告 | 待定 |
| 上线阶段 | 系统上线 | 待定 |

---

*本文档将随项目进展持续更新*
