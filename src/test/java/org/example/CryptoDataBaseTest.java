package org.example;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.sql.*;

import static org.example.CryptoDataBase.createCryptoData;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class CryptoDataBaseTest {

    private static final String DB_URL = "jdbc:sqlite:CryptoTest.db";
    private static Connection conn;

    @BeforeEach
    public void setUp() throws SQLException {
        conn = DriverManager.getConnection(DB_URL);
    }


    @AfterEach
    public void tearDown() throws SQLException {
        try (Statement stmt = conn.createStatement()) {
            stmt.executeUpdate("DROP TABLE IF EXISTS CryptoData;");
        }
    }

    @Test
    public void testCreateCryptoData() throws SQLException {
        createCryptoData(conn);

        try (Statement stmt = conn.createStatement()) {
            ResultSet rs = stmt.executeQuery("SELECT name FROM sqlite_master WHERE type='table' AND name='CryptoData';");
            assertTrue(rs.next(), "La table CryptoData n'a pas été créée.");

            rs = stmt.executeQuery("PRAGMA table_info(CryptoData);");
            boolean columnExists = false;
            while (rs.next()) {
                if ("crypto_id".equals(rs.getString("name"))) {
                    columnExists = true;
                    break;
                }
            }
            assertTrue(columnExists, "La colonne crypto_id n'existe pas dans CryptoData.");

        }
    }


}
