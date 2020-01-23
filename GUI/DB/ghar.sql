-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema proj
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema proj
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `proj` DEFAULT CHARACTER SET utf8 ;
USE `proj` ;

-- -----------------------------------------------------
-- Table `proj`.`contractors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proj`.`contractors` (
  `id_contractor` INT NOT NULL AUTO_INCREMENT,
  `firstname` VARCHAR(45) NOT NULL,
  `lastname` VARCHAR(45) NOT NULL,
  `speciality` VARCHAR(45) NOT NULL,
  `phone` INT NOT NULL,
  `email` VARCHAR(45) NULL,
  `active` TINYINT NOT NULL,
  PRIMARY KEY (`id_contractor`),
  UNIQUE INDEX `id_contractor_UNIQUE` (`id_contractor` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proj`.`timestamps`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proj`.`timestamps` (
  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` TIMESTAMP NULL);


-- -----------------------------------------------------
-- Table `proj`.`tenants`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proj`.`tenants` (
  `id_tenant` INT NOT NULL AUTO_INCREMENT,
  `prevAdress` VARCHAR(45) NULL,
  `forwardingAdress` VARCHAR(45) NULL,
  `firstname` VARCHAR(45) NOT NULL,
  `lastname` VARCHAR(45) NOT NULL,
  `phone` INT NULL,
  `email` VARCHAR(45) NOT NULL,
  `homeID` INT NOT NULL,
  PRIMARY KEY (`id_tenant`),
  UNIQUE INDEX `id_tenant_UNIQUE` (`id_tenant` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proj`.`landlords`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proj`.`landlords` (
  `id_landlord` INT NOT NULL AUTO_INCREMENT,
  `firstname` VARCHAR(45) NOT NULL,
  `lastname` VARCHAR(45) NOT NULL,
  `accountSince` DATE,
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_landlord`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proj`.`properties`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proj`.`properties` (
  `id_property` INT NOT NULL AUTO_INCREMENT,
  `rent` DECIMAL(2) NULL,
  `buyingPrice` DECIMAL(2) NOT NULL,
  `sellingPrice` DECIMAL(2) NULL,
  `active` TINYINT NOT NULL,
  `buyDate` DATE NOT NULL,
  `sellDate` DATE NULL,
  `notes` VARCHAR(45) NULL,
  `id_landlord` INT NOT NULL,
  PRIMARY KEY (`id_property`, `id_landlord`),
  UNIQUE INDEX `id_property_UNIQUE` (`id_property` ASC)  ,
  INDEX `fk_properties_landlords1_idx` (`id_landlord` ASC)   ,
  CONSTRAINT `fk_properties_landlords1`
    FOREIGN KEY (`id_landlord`)
    REFERENCES `proj`.`landlords` (`id_landlord`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proj`.`leaseDetails`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proj`.`leaseDetails` (
  `id_tenant` INT NOT NULL,
  `id_lease` VARCHAR(45) NOT NULL,
  `leaseLen` INT NOT NULL,
  `startDate` DATE NOT NULL,
  `begCondition` VARCHAR(45) NULL,
  `endCondition` VARCHAR(45) NULL,
  `damages` DECIMAL(2) NULL,
  `active` TINYINT NOT NULL,
  `propertyID` INT NOT NULL,
  `tenants_id_tenant` INT NOT NULL,
  `properties_id_property` INT NOT NULL,
  PRIMARY KEY (`id_tenant`, `id_lease`, `tenants_id_tenant`),
  INDEX `fk_leaseDetails_tenants_idx` (`tenants_id_tenant` ASC)   ,
  INDEX `fk_leaseDetails_properties1_idx` (`properties_id_property` ASC)   ,
  CONSTRAINT `fk_leaseDetails_tenants`
    FOREIGN KEY (`tenants_id_tenant`)
    REFERENCES `proj`.`tenants` (`id_tenant`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_leaseDetails_properties1`
    FOREIGN KEY (`properties_id_property`)
    REFERENCES `proj`.`properties` (`id_property`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proj`.`maintainence`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proj`.`maintainence` (
  `id_maintainence` INT NOT NULL AUTO_INCREMENT,
  `notes` VARCHAR(45) NULL,
  `startDate` DATE NULL,
  `active` TINYINT NOT NULL,
  `note` VARCHAR(45) NULL,
  `contractors_id_contractor` INT NOT NULL,
  `properties_id_property` INT NOT NULL,
  `requestor_id` INT NOT NULL,
  PRIMARY KEY (`id_maintainence`),
  INDEX `fk_maintainence_contractors1_idx` (`contractors_id_contractor` ASC)   ,
  INDEX `fk_maintainence_properties1_idx` (`properties_id_property` ASC)   ,
  CONSTRAINT `fk_maintainence_contractors1`
    FOREIGN KEY (`contractors_id_contractor`)
    REFERENCES `proj`.`contractors` (`id_contractor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_maintainence_properties1`
    FOREIGN KEY (`properties_id_property`)
    REFERENCES `proj`.`properties` (`id_property`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `proj` ;

-- -----------------------------------------------------
-- Placeholder table for view `proj`.`view1`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proj`.`view1` (`id` INT);

-- -----------------------------------------------------
--  routine1
-- -----------------------------------------------------

DELIMITER $$
USE `proj`$$
$$

DELIMITER ;

-- -----------------------------------------------------
-- View `proj`.`view1`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proj`.`view1`;
USE `proj`;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
