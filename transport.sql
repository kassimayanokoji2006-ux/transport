-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : jeu. 09 oct. 2025 à 13:06
-- Version du serveur : 9.1.0
-- Version de PHP : 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `transport`
--

-- --------------------------------------------------------

--
-- Structure de la table `eleves`
--

DROP TABLE IF EXISTS `eleves`;
CREATE TABLE IF NOT EXISTS `eleves` (
  `id_Eleve` int NOT NULL AUTO_INCREMENT,
  `nomE` varchar(100) NOT NULL,
  `prenomE` varchar(100) NOT NULL,
  `dateN` date NOT NULL,
  `classe` varchar(15) NOT NULL,
  `adresse` varchar(50) NOT NULL,
  `telParent` varchar(13) NOT NULL,
  PRIMARY KEY (`id_Eleve`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb3;

--
-- Déchargement des données de la table `eleves`
--

INSERT INTO `eleves` (`id_Eleve`, `nomE`, `prenomE`, `dateN`, `classe`, `adresse`, `telParent`) VALUES
(2, 'Razaka', 'Ndrema', '2025-08-19', 'CP2', 'Tanjombato', '038+81+129+43'),
(3, 'Zakabe', 'Setra', '2025-10-06', 'CP2', 'Radama', '0331059633'),
(5, 'GG', 'GGG', '2025-10-23', 't', 'FCGVHB', '0331059633'),
(6, 'Zakabe', 'Setra', '2025-10-06', 'CP2', 'Radama', '0331059633'),
(9, 'Zakabe', 'Setra', '2025-10-06', 'CP2', 'Radama', '0331059633'),
(22, 'Zakabe', 'Setra', '2025-10-06', 'CP2', 'Radama', '0331059633'),
(66, 'Zakabe', 'Setra', '2025-10-06', 'CP2', 'Radama', '0331059633');

-- --------------------------------------------------------

--
-- Structure de la table `trans`
--

DROP TABLE IF EXISTS `trans`;
CREATE TABLE IF NOT EXISTS `trans` (
  `refTrans` int NOT NULL AUTO_INCREMENT,
  `dateTrans` date NOT NULL,
  `idEleve` int DEFAULT NULL,
  `idVehicule` int DEFAULT NULL,
  PRIMARY KEY (`refTrans`),
  KEY `idEleve` (`idEleve`),
  KEY `idVehicule` (`idVehicule`)
) ENGINE=MyISAM AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb3;

--
-- Déchargement des données de la table `trans`
--

INSERT INTO `trans` (`refTrans`, `dateTrans`, `idEleve`, `idVehicule`) VALUES
(1, '2025-10-08', 1, 1),
(22, '2025-09-30', 2, 12),
(23, '2025-09-30', 2, 12),
(2, '2025-09-30', 2, 12);

-- --------------------------------------------------------

--
-- Structure de la table `vehicules`
--

DROP TABLE IF EXISTS `vehicules`;
CREATE TABLE IF NOT EXISTS `vehicules` (
  `idVehicule` int NOT NULL AUTO_INCREMENT,
  `matricule` varchar(20) DEFAULT NULL,
  `marque` varchar(50) DEFAULT NULL,
  `capacite` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`idVehicule`),
  UNIQUE KEY `matricule` (`matricule`)
) ENGINE=MyISAM AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb3;

--
-- Déchargement des données de la table `vehicules`
--

INSERT INTO `vehicules` (`idVehicule`, `matricule`, `marque`, `capacite`) VALUES
(1, '6621+TBI', 'Sprinter+CDI', '32'),
(12, '6621+TBE', 'Sprinter+CDI', '32'),
(18, '6624TBE', 'Sprinter+CDI', '32'),
(14, '66TBE', 'Sprinter+CDI', '32'),
(15, '6631TBE', 'Sprinter+CDI', '32');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
