INSERT INTO Volunteer (FirstName, LastName, Username, Password) VALUES
("Isabelle", "Tang", "enenflash", "12345"),
("Ryan", "Beikrasouli", "General_Hex", "i spelt this right"),
("Anisha", "Imran", "anisha", "imran"),
("Berkay", "Topal", "chiefwace", "becky"),
("Emily", "Godin", "LJSimp", "podophobia"),
("Imogen", "Petrovski", "big buff manly roach", "secretly kaveh"),
("Shing", "Feng", "potato", "egghead");

INSERT INTO Skill (Name) VALUES
("Pen tapping"),
("Drawing wobbly lines"),
("Balloon animals"),
("Cup stacking"),
("Can solve a Rubik's cube");

INSERT INTO VolunteerSkill (VolunteerID, SkillID) VALUES
(1, 1), (1, 5),
(2, 2), (2, 5),
(3, 1), (3, 3), (3, 4),
(4, 1), (4, 4), (4, 5);

INSERT INTO Organisation (Name) VALUES
("RoboCup Junior"),
("Wanted Waffles"),
("Bowling for soup"),
("Alakajam!"),
("Rossmoyne Senior High School");

INSERT INTO Location (Name) VALUES
("The bottom of Bibra Lake"),
("Edith Cowan University"),
("The Dark Web"),
("King's Park"),
("Rossmoyne Senior High School");

INSERT INTO EventType (Name) VALUES
("Competition"),
("Festival"),
("Food"),
("Fundraiser"),
("Social"),
("Educational"),
("Music");

INSERT INTO Event (Name, StartDate, EndDate, LocationID, OrganisationID) VALUES
("AKJ Tournament", "2025-08-08 00:00:00", "2025-08-22 23:59:00", 3, 4),
("RCJ WA State Event", "2025-09-13 08:00:00", "2025-09-14 16:00:00", 2, 1),
("22nd Alakajam!", "2025-09-19 00:00:00", "2025-09-21 23:59:00", 3, 4),
("Soup-off", "2025-08-30 09:00:00", "2025-08-30 15:00:00", 4, 3),
("Waffle Making", "2025-09-07 07:00:00", "2025-09-07 11:00:00", 4, 2),
("RCJ WA Metro Event", "2025-08-30 08:00:00", "2025-08-30 16:00:00", 1, 1),
("Rossy's Got Talent", "2025-08-29 17:00:00", "2025-08-29 20:00:00", 5, 5);

INSERT INTO EventTypeJunction (TypeID, EventID) VALUES
(1, 1), (1, 6), (1, 4),
(2, 1), (2, 6),
(3, 1), (3, 6), (3, 5),
(4, 3), (4, 5),
(5, 2), (5, 3), (5, 6),
(6, 1), (6, 6), (6, 4),
(7, 1), (7, 7);

INSERT INTO VolunteerOpportunity (VolunteerID, EventID) VALUES
(1, 3), (1, 4),
(4, 2), (4, 7),
(7, 6),
(NULL, 1), (NULL, 1), (NULL, 5);

INSERT INTO OpportunitySkill (OpportunityID, SkillID) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 1), (7, 2);

