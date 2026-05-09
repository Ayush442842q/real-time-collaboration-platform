# Database Schema
## Entity Overview
The following entities will be used in the database schema:
* **Users**: stores information about registered users
* **Teams**: stores information about teams
* **Team_Members**: stores information about team members
* **Virtual_Whiteboards**: stores information about virtual whiteboards
* **Documents**: stores information about documents
* **Tasks**: stores information about tasks
* **Messages**: stores information about messages

## Schema Tables
### 1. Users Table
| Column Name | Data Type | Constraints |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | NOT NULL, UNIQUE |
| username | TEXT | NOT NULL, UNIQUE |
| password | TEXT | NOT NULL |
| email | TEXT | NOT NULL, UNIQUE |

### 2. Teams Table
| Column Name | Data Type | Constraints |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | NOT NULL, UNIQUE |
| name | TEXT | NOT NULL, UNIQUE |
| description | TEXT |  |

### 3. Team_Members Table
| Column Name | Data Type | Constraints |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | NOT NULL, UNIQUE |
| team_id | INTEGER | NOT NULL, FOREIGN KEY REFERENCES Teams(id) |
| user_id | INTEGER | NOT NULL, FOREIGN KEY REFERENCES Users(id) |

### 4. Virtual_Whiteboards Table
| Column Name | Data Type | Constraints |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | NOT NULL, UNIQUE |
| team_id | INTEGER | NOT NULL, FOREIGN KEY REFERENCES Teams(id) |
| name | TEXT | NOT NULL |
| description | TEXT |  |

### 5. Documents Table
| Column Name | Data Type | Constraints |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | NOT NULL, UNIQUE |
| team_id | INTEGER | NOT NULL, FOREIGN KEY REFERENCES Teams(id) |
| name | TEXT | NOT NULL |
| content | TEXT |  |

### 6. Tasks Table
| Column Name | Data Type | Constraints |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | NOT NULL, UNIQUE |
| team_id | INTEGER | NOT NULL, FOREIGN KEY REFERENCES Teams(id) |
| name | TEXT | NOT NULL |
| description | TEXT |  |
| status | TEXT |  |

### 7. Messages Table
| Column Name | Data Type | Constraints |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | NOT NULL, UNIQUE |
| team_id | INTEGER | NOT NULL, FOREIGN KEY REFERENCES Teams(id) |
| user_id | INTEGER | NOT NULL, FOREIGN KEY REFERENCES Users(id) |
| content | TEXT | NOT NULL |
| timestamp | TEXT | NOT NULL |

## Indexes
* Create an index on the `team_id` column in the `Team_Members` table
* Create an index on the `team_id` column in the `Virtual_Whiteboards` table
* Create an index on the `team_id` column in the `Documents` table
* Create an index on the `team_id` column in the `Tasks` table
* Create an index on the `team_id` column in the `Messages` table

## Relationships
The following relationships exist between the entities:
* A user can be a member of many teams (one-to-many)
* A team can have many members (one-to-many)
* A team can have many virtual whiteboards (one-to-many)
* A team can have many documents (one-to-many)
* A team can have many tasks (one-to-many)
* A team can have many messages (one-to-many)

```
+---------------+
|  Users      |
+---------------+
           |
           |  one-to-many
           v
+---------------+
|  Team_Members |
+---------------+
           |
           |  many-to-one
           v
+---------------+
|  Teams      |
+---------------+
           |
           |  one-to-many
           v
+---------------+
|  Virtual_Whiteboards |
+---------------+
           |
           |  one-to-many
           v
+---------------+
|  Documents    |
+---------------+
           |
           |  one-to-many
           v
+---------------+
|  Tasks       |
+---------------+
           |
           |  one-to-many
           v
+---------------+
|  Messages    |
+---------------+
```

## Sample Queries
1. Get all teams for a user:
```sql
SELECT t.* 
FROM Teams t 
JOIN Team_Members tm ON t.id = tm.team_id 
WHERE tm.user_id = ?;
```
2. Get all members of a team:
```sql
SELECT u.* 
FROM Users u 
JOIN Team_Members tm ON u.id = tm.user_id 
WHERE tm.team_id = ?;
```
3. Create a new team:
```sql
INSERT INTO Teams (name, description) 
VALUES (?, ?);
```
4. Add a new member to a team:
```sql
INSERT INTO Team_Members (team_id, user_id) 
VALUES (?, ?);
```
5. Get all messages for a team:
```sql
SELECT m.* 
FROM Messages m 
WHERE m.team_id = ?;
```

## Migration Notes
1. Create the `Users` table
2. Create the `Teams` table
3. Create the `Team_Members` table with foreign key constraints
4. Create the `Virtual_Whiteboards` table with foreign key constraints
5. Create the `Documents` table with foreign key constraints
6. Create the `Tasks` table with foreign key constraints
7. Create the `Messages` table with foreign key constraints
8. Create indexes on the `team_id` columns in the `Team_Members`, `Virtual_Whiteboards`, `Documents`, `Tasks`, and `Messages` tables