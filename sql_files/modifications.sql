ALTER TABLE Volunteer DROP COLUMN Email;
ALTER TABLE Volunteer RENAME COLUMN Username TO Email;
UPDATE Volunteer SET Email=Email || "@gmail.com";
UPDATE Volunteer SET Email="big_buff_manly_roach@gmail.com" WHERE ID=6;
ALTER TABLE Volunteer ADD COLUMN Admin BOOLEAN;
UPDATE Volunteer SET Admin=TRUE WHERE ID=1;
UPDATE Volunteer SET Admin=FALSE WHERE ID!=1;