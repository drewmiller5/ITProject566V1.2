SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema campaign_channel
-- -----------------------------------------------------
USE `campaign_channel` ;

-- -----------------------------------------------------
-- Table `campaign_channel`.`Channel_Category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `campaign_channel`.`Channel_Category` ;


-- -----------------------------------------------------
-- Table `campaign_channel`.`Channel`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `campaign_channel`.`Channel` ;



-- -----------------------------------------------------
-- Table `campaign_channel`.`Campaign_Category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `campaign_channel`.`Campaign_Category` ;


-- -----------------------------------------------------
-- Table `campaign_channel`.`Company`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `campaign_channel`.`Company` ;



-- -----------------------------------------------------
-- Table `campaign_channel`.`Campaign`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `campaign_channel`.`Campaign` ;




-- -----------------------------------------------------
-- Table `campaign_channel`.`campaign_channel_xref`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `campaign_channel`.`campaign_channel_xref` ;

ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

COMMIT;