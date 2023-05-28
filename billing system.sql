--CREATE DATABASE alfabet;


use alfabet;


CREATE TABLE `transactions` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `src` varchar(120),
  `dst` varchar(120),
  `amount` float,
  `direction` varchar(6)
);

CREATE TABLE `status` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `transaction_timestamp` timestamp DEFAULT (now()),
  `transaction_id` integer,
  `payment_id` integer,
  `transaction_status` boolean
);

CREATE TABLE `payments_plan` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `payment_scheduled_to` varchar(7),
  `expected_amount` float,
  `loan_id` integer
);

CREATE TABLE `loans` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `total_loan_amount` float,
  `borrower` varchar(120),
  `loan_id` integer,
  `origination_timestamp` timestamp DEFAULT (now())
);
