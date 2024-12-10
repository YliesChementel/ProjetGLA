package org.example;

import java.sql.*;
import java.util.logging.Logger;

public class CryptoDataBase {

    static Logger logger = Logger.getLogger(CryptoDataBase.class.getName());

    private CryptoDataBase() {
    }

    static void createCrypto(Connection conn) {
        String sql = "CREATE TABLE IF NOT EXISTS Crypto (" +
                "id TEXT PRIMARY KEY," +
                "symbol TEXT NOT NULL," +
                "name TEXT NOT NULL);";

        try (Statement stmt = conn.createStatement()) {
            stmt.execute(sql);
            logger.info("Table 'Crypto' créée !");
        } catch (SQLException e) {
            logger.info(e.getMessage());
        }
    }

    static void createCryptoData(Connection conn) {
        String sql = "CREATE TABLE IF NOT EXISTS CryptoData (" +
                "id INTEGER PRIMARY KEY AUTOINCREMENT," +
                "crypto_id TEXT NOT NULL," +
                "rank INTEGER NOT NULL," +
                "volume DECIMAL(30,10)," +
                "price DECIMAL(30,10)," +
                "fetchTime TIMESTAMP NOT NULL," +
                "FOREIGN KEY(crypto_id) REFERENCES Crypto(id));";

        try (Statement stmt = conn.createStatement()) {
            stmt.execute(sql);
            logger.info("Table 'CryptoData' créée !");
        } catch (SQLException e) {
            logger.info(e.getMessage());
        }
    }

    static boolean tableExists(Connection conn, String tableName) {
        try (ResultSet rs = conn.getMetaData().getTables(null, null, tableName, null)) {
            return rs.next();
        } catch (SQLException e) {
            logger.info(e.getMessage());
            return false;
        }
    }

    static void insertIntoCrypto(Connection conn, String id,String symbol, String name) {
        String sql = "INSERT INTO Crypto(id, symbol, name) VALUES(?, ?, ?)" + "ON CONFLICT(id) DO NOTHING";

        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, id);
            pstmt.setString(2, symbol);
            pstmt.setString(3, name);
            pstmt.executeUpdate();
            logger.info("Données insérées : " + id + ", " + name + ", " + symbol);
        } catch (SQLException e) {
            logger.info(e.getMessage());
        }
    }

    static void insertIntoCryptoData(Connection conn, String cryptoId, int rank, double volume, double price, String fetchTime) {
        String sql = "INSERT INTO CryptoData(crypto_id, rank, volume, price, fetchTime) VALUES(?, ?, ?, ?, ?)";

        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, cryptoId);
            pstmt.setInt(2, rank);
            pstmt.setDouble(3, volume);
            pstmt.setDouble(4, price);
            pstmt.setString(5, fetchTime);
            pstmt.executeUpdate();
            logger.info("Données insérées dans 'CryptoData': " + cryptoId + ", " + rank + ", " + volume + ", " + price + ", " + fetchTime);
        } catch (SQLException e) {
            logger.info(e.getMessage());
        }
    }

    static void displayCrypto(Connection conn) {
        String sql = "SELECT id, symbol, name FROM Crypto";

        try (Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {

            while (rs.next()) {
                logger.info("ID: " + rs.getString("id") + ", Symbole: " + rs.getString("symbol") + ", Nom: " + rs.getString("name"));
            }
        } catch (SQLException e) {
            logger.info(e.getMessage());
        }
    }

    static void displayCryptoData(Connection conn) {
        String sql = "SELECT id, crypto_id, rank, volume, price, fetchTime FROM CryptoData";

        try (Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {

            while (rs.next()) {
                logger.info("ID: " + rs.getString("id") + ", CryptoId: " + rs.getString("crypto_id") + ", Rank: " + rs.getString("rank") + ", Volume: " + rs.getString("volume") + ", Price: " + rs.getString("price") + ", FetchTime: " + rs.getString("fetchTime"));
            }
        } catch (SQLException e) {
            logger.info(e.getMessage());
        }
    }

}
