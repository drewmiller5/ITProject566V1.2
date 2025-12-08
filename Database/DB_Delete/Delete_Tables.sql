SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema Campaign_Channel
-- -----------------------------------------------------
USE `Campaign_Channel` ;

-- -----------------------------------------------------
-- Table `Campaign_Channel`.`Channel_Category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Campaign_Channel`.`Channel_Category` ;


-- -----------------------------------------------------
-- Table `Campaign_Channel`.`Channel`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Campaign_Channel`.`Channel` ;



-- -----------------------------------------------------
-- Table `Campaign_Channel`.`Campaign_Category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Campaign_Channel`.`Campaign_Category` ;


-- -----------------------------------------------------
-- Table `Campaign_Channel`.`Company`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Campaign_Channel`.`Company` ;



-- -----------------------------------------------------
-- Table `Campaign_Channel`.`Campaign`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Campaign_Channel`.`Campaign` ;




-- -----------------------------------------------------
-- Table `Campaign_Channel`.`Campaign_channel_xref`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Campaign_Channel`.`Campaign_channel_xref` ;

ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

COMMIT;