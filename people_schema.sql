
DROP TABLE IF EXISTS people;

create table `people` (
  `given_name` varchar(80),
  `family_name` varchar(80) ,
  `date_of_birth` date,
  `place_of_birth` varchar(80)
);
