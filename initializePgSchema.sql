CREATE TABLE IF NOT EXISTS Exam (
    examID INT PRIMARY KEY,
    examName VARCHAR(50),
    total INT,
    weightage INT
);

CREATE TABLE IF NOT EXISTS Faculty (
    fID INT PRIMARY KEY,
    fName VARCHAR(100),
    email VARCHAR(100),
    phoneNo VARCHAR(15),
    DOB DATE
);

CREATE TABLE IF NOT EXISTS Faculty_Pass (
    fID INT REFERENCES Faculty(fID),
    hashed_password VARCHAR
);

CREATE TABLE IF NOT EXISTS Course (
    cID INT PRIMARY KEY,
    cName VARCHAR(100),
    fID INT REFERENCES Faculty(fID),
    credits INT
);

CREATE TABLE IF NOT EXISTS Student (
    regNo VARCHAR PRIMARY KEY,
    sName VARCHAR(100),
    Email VARCHAR(100),
    PhoneNo VARCHAR(15),
    DOB DATE
);

CREATE TABLE IF NOT EXISTS Student_Attendance (
    regNo VARCHAR REFERENCES Student(regNo),
    cID INT REFERENCES Course(cID),
    date DATE,
    attended BOOLEAN
);

CREATE TABLE IF NOT EXISTS Student_Course (
    regNo VARCHAR REFERENCES Student(regNo),
    cID INT REFERENCES Course(cID),
    PRIMARY KEY (regNo, cID)
);

CREATE TABLE IF NOT EXISTS Student_Marks (
    regNo VARCHAR REFERENCES Student(regNo),
    cID INT REFERENCES Course(cID),
    examID INT REFERENCES Exam(examID),
    scored INT,
    PRIMARY KEY (regNo, cID, examID)
);

CREATE TABLE IF NOT EXISTS Student_Pass (
    regNo VARCHAR REFERENCES Student(regNo),
    hashed_password VARCHAR
);

CREATE TABLE IF NOT EXISTS Admin (
    aID INT PRIMARY KEY,
    aName VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Admin_Pass (
    aID INT REFERENCES Admin(aID),
    hashed_password VARCHAR
);

INSERT INTO Exam (examID, examName, total, weightage)
VALUES 
(1, 'CAT1', 50, 15),
(2, 'CAT2', 50, 15),
(3, 'FAT', 100, 40),
(4, 'DA', 10, 10)
ON CONFLICT (examID)
DO NOTHING;

