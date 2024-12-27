# dbine
Auxiliary tools related to databases

## Concept
PDF output from database table definitions

### Database table definitions(MySQL)
```sql
DROP DATABASE IF EXISTS db;
CREATE DATABASE db;

DROP USER IF EXISTS _user_;
CREATE USER _user_ IDENTIFIED BY 'pass';

GRANT ALL ON db.* TO _user_;

DROP TABLE IF EXISTS no_comments;
CREATE TABLE no_comments (
  id INT PRIMARY KEY,
  name VARCHAR(10)
) COMMENT 'コメントなしテーブル';

DROP TABLE IF EXISTS with_comments;
CREATE TABLE with_comments (
  id INT PRIMARY KEY COMMENT 'ID',
  name VARCHAR(10) COMMENT '名前'
) COMMENT 'コメントつきテーブル';

DROP TABLE IF EXISTS relations;
CREATE TABLE relations (
  id INT PRIMARY KEY COMMENT 'ID',
  no_comment_id INT COMMENT 'コメントなしテーブルのID',
  with_comment_id INT COMMENT 'コメントつきテーブルのID'
);
```

### PDF(PNG)
![](./images/database_mysql.png)

## What is possible
1. Log in to the database and get table definition information
2. Output table definition information as an ER diagram-like image in PDF
3. Convert PDF to image

## Reason for development
- I want to output the relationships between database table definitions as a PDF or image so that I can understand them at a glance

## Supported database types
- PostgreSQL
- MySQL
- SQLite

## Versions

|Version|Summary|
|:--|:--|
|0.1.6|Added SQLite to supported databases|
|0.1.4|Improved ease of use|
|0.1.3|Release dbine|

## Installation
### [dbine](https://pypi.org/project/dbine/)
`pip install dbine`

### [Graphviz](https://graphviz.org/download/)
Required for PDF output

### [Poppler](https://github.com/Belval/pdf2image?tab=readme-ov-file)
Required for PDF image conversion

## CLI
### pdf.write
Write database table definition to PDF

#### 1. Prepare database connection config file(database.yaml)
**[database.yaml]**
```yaml
Type: MySQL
DatabaseName: db
UserName: _user_
Password: pass
Host: localhost
Port: 0
```

#### 2. PDF write by CLI execution

```
pdf.write # <yaml file path> <pdf file path>
```
`dbine pdf.write database.yaml database.pdf`
```
database.pdf is done.
```

### pdf.convert
Convert PDF to image

#### 1. Image(PNG) conversion by CLI execution

```
pdf.convert # <pdf file path> <image file path>
```
`dbine pdf.convert database.pdf database.png`
```
database.png is done.
```
