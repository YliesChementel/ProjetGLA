package org.example;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.sql.*;

import static org.example.CryptoDataBase.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class CryptoDataBaseTest {

    private static Connection conn;

    @Mock
    private Connection connection;

    @BeforeEach
    public void setUp() throws SQLException {
        conn = DriverManager.getConnection("jdbc:sqlite::memory:");
        MockitoAnnotations.openMocks(this);
    }


    @Test
    public void shouldCreateCrypto() throws SQLException {
        createCrypto(conn);

        try (Statement stmt = conn.createStatement()) {
            ResultSet rs = stmt.executeQuery("SELECT name FROM sqlite_master WHERE type='table' AND name='Crypto';");
            assertTrue(rs.next(), "La table CryptoData n'a pas été créée.");

            rs = stmt.executeQuery("PRAGMA table_info(Crypto);");
            boolean columnExists = false;
            while (rs.next()) {
                if ("id".equals(rs.getString("name"))) {
                    columnExists = true;
                    break;
                }
            }
            assertTrue(columnExists, "La colonne crypto_id n'existe pas dans CryptoData.");
        }
    }

    @Test
    public void shouldThrowWhenCreateCrypto() throws SQLException {
        when(connection.createStatement()).thenThrow(new SQLException("Erreur de connexion"));  // Simule une erreur

        createCrypto(connection);

        verify(connection, times(1)).createStatement();
    }


    @Test
    public void shouldCreateCryptoData() throws SQLException {
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

    @Test
    public void shouldThrowWhenCreateCryptoData() throws SQLException {
        when(connection.createStatement()).thenThrow(new SQLException("Erreur de connexion"));  // Simule une erreur

        createCryptoData(connection);

        verify(connection, times(1)).createStatement();
    }

    @Test
    public void shouldCheckIfTableExist() throws SQLException {
        assertFalse(tableExists(conn, "Crypto"));

        assertFalse(tableExists(conn, "CryptoData"));

        createCrypto(conn);
        assertTrue(tableExists(conn, "Crypto"));

        createCryptoData(conn);
        assertTrue(tableExists(conn, "CryptoData"));
    }

    @Test
    public void shouldReturnFalseWhenGetMetaDataFails() {
        boolean exists = tableExists(connection, "Crypto");

        // On s'attend à ce que tableExists renvoie false en cas d'exception
        assertFalse(exists, "La table ne devrait pas exister lorsque getMetaData échoue");
    }

    @Test
    public void shouldInsertIntoCrypto() throws SQLException {
        createCrypto(conn);
        insertIntoCrypto(conn,"0","TEST","test");
        try (PreparedStatement stmt = conn.prepareStatement("SELECT * FROM Crypto")) {
            ResultSet rs = stmt.executeQuery();

            assertTrue(rs.next());

            assertEquals("0", rs.getString("id"));
            assertEquals("TEST", rs.getString("symbol"));
            assertEquals("test", rs.getString("name"));
        }
    }

    @Test
    public void shouldThrowWhenIntoCrypto() throws SQLException {
        String sql = "INSERT INTO Crypto(id, symbol, name) VALUES(?, ?, ?)" + "ON CONFLICT(id) DO NOTHING";
        when(connection.prepareStatement(sql)).thenThrow(new SQLException("[SQLITE_ERROR] SQL error or missing database (no such table: Crypto)"));  // Simule une erreur

        insertIntoCrypto(connection,"0","TEST","test");

        verify(connection, times(1)).prepareStatement(sql);
    }

    @Test
    public void shouldInsertIntoCryptoData() throws SQLException {
        createCryptoData(conn);
        insertIntoCryptoData(conn,"0",1,1.0,1.0,"dimanche");
        try (PreparedStatement stmt = conn.prepareStatement("SELECT * FROM CryptoData")) {
            ResultSet rs = stmt.executeQuery();

            assertTrue(rs.next());

            assertEquals(1, Integer.parseInt(rs.getString("rank")));
            assertEquals(1.0, Integer.parseInt(rs.getString("volume")));
            assertEquals(1.0, Integer.parseInt(rs.getString("price")));
            assertEquals("dimanche", rs.getString("fetchTime"));
        }
    }

    @Test
    public void shouldThrowWhenIntoCryptoData() throws SQLException {
        String sql = "INSERT INTO CryptoData(crypto_id, rank, volume, price, fetchTime) VALUES(?, ?, ?, ?, ?)";
        when(connection.prepareStatement(sql)).thenThrow(new SQLException("[SQLITE_ERROR] SQL error or missing database (no such table: CryptoData)"));  // Simule une erreur

        insertIntoCryptoData(connection,"0",1,1.0,1.0,"dimanche");

        verify(connection, times(1)).prepareStatement(sql);
    }

    @Test
    public void shouldThrowWhenDisplayCrypto() throws SQLException {
        when(connection.createStatement()).thenThrow(new SQLException("Erreur de connexion"));  // Simule une erreur

        displayCrypto(connection);

        verify(connection, times(1)).createStatement();
    }

    @Test
    public void shouldThrowWhenDisplayCryptoData() throws SQLException {
        when(connection.createStatement()).thenThrow(new SQLException("Erreur de connexion"));  // Simule une erreur

        displayCryptoData(connection);

        verify(connection, times(1)).createStatement();
    }

}
